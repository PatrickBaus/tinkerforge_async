"""
This module implements the underlying ip connection to the Bricks and Bricklets.
See https://www.tinkerforge.com/de/doc/Low_Level_Protocols/TCPIP.html for details.
"""
from __future__ import annotations

import asyncio
import errno  # The error numbers can be found in /usr/include/asm-generic/errno.h
import hashlib
import hmac
import logging
import os
import struct
from asyncio import StreamReader, StreamWriter
from dataclasses import dataclass
from enum import Enum, Flag, unique
from types import TracebackType
from typing import AsyncGenerator, Literal, Type, cast, overload

from .device_factory import device_factory

try:
    from typing import Self  # type: ignore # Python 3.11
except ImportError:
    from typing_extensions import Self

from .async_event_bus import EventBus
from .devices import Device, DeviceIdentifier, _FunctionID
from .ip_connection_helper import base58decode, pack_payload, unpack_payload


class NotConnectedError(ConnectionError):
    """
    Raised if there is no connection
    """


class InvalidDataError(ValueError):
    """
    Raised if there is no connection
    """


class NetworkUnreachableError(ConnectionError):
    """
    Raised if the network is unreachable. Error number errno.ENETUNREACH (101) or errno.EHOSTUNREACH (113).
    """


@unique
class FunctionID(_FunctionID):
    """
    Function calls needed to establish a connection and enumerate Bricks and
    Bricklets
    """

    GET_AUTHENTICATION_NONCE = 1
    AUTHENTICATE = 2
    DISCONNECT_PROBE = 128
    CALLBACK_ENUMERATE = 253
    ENUMERATE = 254


@unique
class EnumerationType(Enum):
    """
    The type of event, that triggered the enumeration.
    """

    AVAILABLE = 0
    CONNECTED = 1
    DISCONNECTED = 2


class Flags(Flag):
    """
    Error codes used by the protocol
    """

    OK = 0
    INVALID_PARAMETER = 64
    FUNCTION_NOT_SUPPORTED = 128


@dataclass
class EnumerationPayload:
    uid: int  # Stop the base58 encoded nonsense and use the uint32_t id
    connected_uid: int | None
    position: str | int | None
    hardware_version: tuple[int, int, int] | None
    firmware_version: tuple[int, int, int] | None
    device_id: int | DeviceIdentifier | None
    enumeration_type: EnumerationType


@dataclass
class HeaderPayload:
    uid: int  # Stop the base58 encoded nonsense and use the uint32_t id
    sequence_number: int | None
    response_expected: bool
    function_id: _FunctionID | int
    flags: Flags | int


DEFAULT_WAIT_TIMEOUT = 2.5  # in seconds


class IPConnectionAsync:  # pylint: disable=too-many-instance-attributes
    """
    The implementation of the Tinkerforge TCP/IP protocol. See
    https://www.tinkerforge.com/en/doc/Low_Level_Protocols/TCPIP.html for details.
    """

    BROADCAST_UID = 0  # The uid used to broadcast enumeration events

    HEADER_FORMAT = "<IBBBB"  # little endian (<), uid (I, uint32), size (B, uint8), function id, sequence number, flags

    @property
    def uid(self) -> int:
        """
        The uid used by the IP connection for authentication. It needs a unique id (uid) to talk to the user.
        """
        return 1

    @property
    def hostname(self) -> str | None:
        """
        The hostname of the connection.
        """
        return self.__host

    @property
    def port(self) -> int:
        """
        The remote port of the connection.
        """
        return self.__port

    @property
    def timeout(self) -> float:
        """
        Returns the timeout for async operations in seconds.
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, value: float) -> None:
        """
        The timeout used for reading and writing packets, if not set, the
        DEFAULT_WAIT_TIMEOUT will be used.
        """
        self.__timeout = None if value is None else abs(float(value))

    @property
    def is_connected(self) -> bool:
        """
        Returns *True* if, the connection is established.
        """
        return self.__writer is not None and not self.__writer.is_closing()

    def __init__(
        self,
        host: str | None = None,
        port: int = 4223,
        authentication_secret: str | bytes | None = None,
        timeout: float | None = None,
    ) -> None:
        self.__host = host
        self.__port = port
        self.__authentication_secret = authentication_secret

        self.timeout = DEFAULT_WAIT_TIMEOUT if timeout is None else timeout
        self.__pending_requests: dict[int, asyncio.Future[tuple[HeaderPayload, bytes]]] = {}
        self.__next_nonce: int = 0

        self.__running_tasks: set[asyncio.Task] = set()

        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.WARNING)  # Only log really important messages

        # These will be assigned during connect()
        self.__reader: StreamReader | None = None
        self.__writer: StreamWriter | None = None
        self.__lock: asyncio.Lock | None = None  # Used by connect()

        self.__sequence_number_queue: asyncio.Queue[int] = asyncio.Queue(maxsize=15)
        for i in range(1, 16):
            self.__sequence_number_queue.put_nowait(i)
            # This queue is not supposed to be joined but could be joined any time, because it has no open tasks
            self.__sequence_number_queue.task_done()

        self.__event_bus = EventBus()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            f"(host={self.__host}, port={self.__port}, "
            f"authentication_secret={None if self.__authentication_secret is None else '*****'})"
        )

    def __str__(self) -> str:
        return f"IPConnectionAsync({self.__host}:{self.__port})"

    async def __aenter__(self) -> Self:
        await self.connect()
        return self

    async def __aexit__(
        self, exc_type: Type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None
    ) -> None:
        await self.disconnect()

    @staticmethod
    def __parse_header(data: bytes) -> tuple[int, HeaderPayload]:
        """
        Raises
        ----------
        struct.error
            if the header is invalid, may be raised by struct.unpack_from
        """
        uid: int
        payload_size: int
        function_id: int | FunctionID  # It is parsed as int, then later converted to FunctionID
        options: int
        flags: int | Flags
        uid, payload_size, function_id, options, flags = struct.unpack_from(IPConnectionAsync.HEADER_FORMAT, data)

        try:
            function_id = FunctionID(function_id)
            if function_id in (FunctionID.GET_AUTHENTICATION_NONCE, FunctionID.AUTHENTICATE) and not uid == 1:
                # Only the special uid 1 can reply with GET_AUTHENTICATION_NONCE or AUTHENTICATE
                function_id = function_id.value
        except ValueError:
            # Do not assign an enum, leave the int
            pass
        # There is no sequence number if it is a callback (sequence_number == 0)
        sequence_number = None if (options >> 4) & 0b1111 == 0 else (options >> 4) & 0b1111
        response_expected = bool(options >> 3 & 0b1)
        # options = options & 0b111 # Options for future use
        try:
            flags = Flags(flags)
        except ValueError:
            # Do not assign an enum, leave the int
            pass

        return payload_size, HeaderPayload(uid, sequence_number, response_expected, function_id, flags)

    @staticmethod
    def __create_packet_header(
        sequence_number: int, payload_size: int, function_id: int, uid=None, response_expected=False
    ) -> bytes:
        uid = IPConnectionAsync.BROADCAST_UID if uid is None else uid
        packet_size = payload_size + struct.calcsize(IPConnectionAsync.HEADER_FORMAT)
        response_expected = bool(response_expected)

        sequence_number_and_options = (sequence_number << 4) | response_expected << 3

        return struct.pack(
            IPConnectionAsync.HEADER_FORMAT, uid, packet_size, function_id, sequence_number_and_options, Flags.OK.value
        )

    @staticmethod
    def __parse_enumerate_payload(payload) -> EnumerationPayload:
        uid: str
        connected_uid: str
        position: str | int
        hardware_version: tuple[int, int, int]
        firmware_version: tuple[int, int, int]
        device_identifier: int | DeviceIdentifier
        enumeration_type: int | EnumerationType
        (
            uid,
            connected_uid,
            position,
            hardware_version,
            firmware_version,
            device_identifier,
            enumeration_type,
        ) = unpack_payload(payload, "8s 8s c 3B 3B H B")

        enumeration_type = EnumerationType(enumeration_type)

        try:
            device_identifier = DeviceIdentifier(device_identifier)
        except ValueError:
            # Do not assign an enum, leave the int
            pass

        try:
            position = int(position)
        except ValueError:
            # It is probably a bricklet, which does have an alphabetic position descriptor
            pass

        # See https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html#callbacks for details on the payload
        # We will return None for all 'invalid' fields instead of garbage like the Tinkerforge API
        return EnumerationPayload(
            base58decode(uid),
            None
            if (enumeration_type is EnumerationType.DISCONNECTED or connected_uid == "0")
            else base58decode(connected_uid),
            None if enumeration_type is EnumerationType.DISCONNECTED else position,
            None if enumeration_type is EnumerationType.DISCONNECTED else hardware_version,
            None if enumeration_type is EnumerationType.DISCONNECTED else firmware_version,
            None if enumeration_type is EnumerationType.DISCONNECTED else device_identifier,
            enumeration_type,
        )

    async def read_events(self, uid: int) -> AsyncGenerator[tuple[HeaderPayload, bytes], None]:
        data: tuple[HeaderPayload, bytes]
        async for data in self.__event_bus.register(f"/events/{uid}"):
            yield data

    async def read_enumeration(self, uid: int = None) -> AsyncGenerator[tuple[EnumerationType, Device], None]:
        data: EnumerationPayload
        async for data in self.__event_bus.register("/enumerations"):
            if uid is None or uid == data.uid:
                try:
                    yield data.enumeration_type, device_factory.get(self, data.device_id, data.uid)  # type: ignore
                except ValueError:
                    self.__logger.warning("No driver for device id '%i' found.", data.device_id)

    async def enumerate(self) -> None:
        """
        Broadcasts an enumerate request. All devices will respond with their id
        Returns: None, it does not support 'response_expected'
        """
        self.__logger.debug("Enumerating Node.")
        await self.send_request(device=None, function_id=FunctionID.ENUMERATE)

    async def ping(self) -> None:
        self.__logger.debug("Sending ping to host %s:%i", self.__host, self.__port)
        await self.send_request(device=None, function_id=FunctionID.DISCONNECT_PROBE)

    @overload
    async def send_request(
        self,
        device: Device | IPConnectionAsync | None,
        function_id: _FunctionID,
        data: bytes = b"",
        *,
        response_expected: Literal[True],
    ) -> tuple[HeaderPayload, bytes]:
        ...

    @overload
    async def send_request(
        self,
        device: Device | IPConnectionAsync | None,
        function_id: _FunctionID,
        data: bytes = b"",
        *,
        response_expected: Literal[False] = ...,
    ) -> None:
        ...

    @overload
    async def send_request(
        self,
        device: Device | IPConnectionAsync | None,
        function_id: _FunctionID,
        data: bytes = b"",
        *,
        response_expected: bool = ...,
    ) -> tuple[HeaderPayload, bytes] | None:
        ...

    async def send_request(
        self,
        device: Device | IPConnectionAsync | None,
        function_id: _FunctionID,
        data: bytes = b"",
        *,
        response_expected: bool = False,
    ) -> tuple[HeaderPayload, bytes] | None:
        """
        Creates a request, by prepending a header to the data and sending it to
        the Tinkerforge host.
        Returns: None, if 'response_expected' is *False*, else it will return
        a tuple (header, payload) as returned by the host.
        """
        if not self.is_connected:
            raise NotConnectedError("Tinkerforge IP Connection not connected.")
        assert self.__writer is not None

        sequence_number = await self.__sequence_number_queue.get()
        try:  # To make sure, that we return the sequence number
            header = self.__create_packet_header(
                sequence_number=sequence_number,
                payload_size=len(data),
                function_id=function_id.value,
                uid=0 if device is None else device.uid,
                response_expected=response_expected,
            )

            request = header + data

            # If we are waiting for a response, send the request, then pass on the response as a future
            self.__logger.debug(
                "Sending request to device %(device)s (%(uid)s) and function %(function_id)s with sequence_number "
                "%(sequence_number)s: %(header)s - %(payload)s.",
                {
                    "device": device if device is not None else "all",
                    "uid": device.uid if device is not None else "all",
                    "function_id": function_id,
                    "sequence_number": sequence_number,
                    "header": header,
                    "payload": data,
                },
            )

            self.__writer.write(request)
            if response_expected:
                self.__logger.debug("Waiting for reply for request number %i.", sequence_number)
                # The future will be resolved by the main_loop() and __process_packet()
                self.__pending_requests[sequence_number] = asyncio.Future()
                try:
                    result_header, payload = await asyncio.wait_for(
                        self.__pending_requests[sequence_number], self.__timeout
                    )
                except asyncio.TimeoutError:
                    asyncio.create_task(self.disconnect())
                    raise
                finally:
                    # Cleanup. Note: The sequence number, might not be in the dict anymore, because
                    # if the remote endpoint shuts down the connection, __close_transport() is called,
                    # which clears all pending requests.
                    self.__pending_requests.pop(sequence_number, None)
                self.__logger.debug(
                    "Got reply for request number %(sequence_number)i: %(header)s - %(payload)s.",
                    {"sequence_number": sequence_number, "header": result_header, "payload": payload},
                )
                return result_header, payload
            return None
        finally:
            # Return the sequence number. We misuse the queue a little, so we
            # set the task to done immediately.
            self.__sequence_number_queue.put_nowait(sequence_number)
            self.__sequence_number_queue.task_done()

    async def __process_packet(  # pylint: disable=too-many-branches
        self, header: HeaderPayload, payload: bytes
    ) -> None:
        # There are two types of packets:
        # - Broadcasts/Callbacks
        # - Replies
        # We need to treat them differently

        # Callbacks first, because most packets will be callbacks,
        # so it is more efficient to do them first
        if header.sequence_number is None:
            try:
                # Check if it is either an enumeration event
                header.function_id = FunctionID(header.function_id)
            except ValueError:
                # If we do not know the type of event, try to pass it on to
                # a listening device
                self.__event_bus.publish(f"/events/{header.uid}", (header, payload))
            else:
                if header.function_id is FunctionID.CALLBACK_ENUMERATE:
                    decoded_payload = self.__parse_enumerate_payload(payload)
                    self.__logger.debug(
                        "Received enumeration: %(header)s - %(payload)s.",
                        {"header": header, "payload": decoded_payload},
                    )
                    self.__event_bus.publish("/enumerations", decoded_payload)
        elif header.response_expected:
            try:
                # Mark the future as done
                future = self.__pending_requests[header.sequence_number]
                if not future.cancelled():
                    if header.flags is Flags.OK:
                        future.set_result((header, payload))
                    elif header.flags is Flags.FUNCTION_NOT_SUPPORTED:
                        future.set_exception(AttributeError(f"Function not supported: {header.function_id}."))
                    elif header.flags is Flags.INVALID_PARAMETER:
                        future.set_exception(ValueError("Invalid parameter."))
                    else:
                        future.set_result((header, payload))
            except KeyError:
                # Drop the packet, because it is not our sequence number
                pass
            except asyncio.InvalidStateError:
                self.__logger.error(
                    "Invalid sequence number: %i. The request was already processed", header.sequence_number
                )
        else:
            self.__logger.info("Unknown packet: %(header)s - %(payload)s.", {"header": header, "payload": payload})

    async def __read_packets(
        self,
    ) -> AsyncGenerator[tuple[HeaderPayload, bytes], None]:
        while "loop not canceled":
            if not self.is_connected:
                raise NotConnectedError("Tinkerforge IP Connection not connected.")
            assert self.__reader is not None
            data: bytes | None = None
            try:
                data = await self.__reader.readexactly(struct.calcsize(IPConnectionAsync.HEADER_FORMAT))
                packet_size, header = self.__parse_header(data)

                payload = await self.__reader.readexactly(
                    packet_size - struct.calcsize(IPConnectionAsync.HEADER_FORMAT)
                )

                yield header, payload
            except (struct.error, ValueError):
                # ValueError may be raised by readexactly() if the argument is <0
                self.__logger.debug("Invalid data received. data: %s", data)
            except (asyncio.IncompleteReadError, ConnectionResetError) as exc:
                # We got an EOF
                # Only the Brick daemon does shutdown gracefully, sending an EOF.
                # If the Ethernet or Wi-Fi extension goes offline, the connection is typically severed unexpectedly
                raise NotConnectedError("Tinkerforge IP Connection not connected.") from exc

    async def __main_loop(self) -> None:
        """
        The main loop, that is responsible for processing incoming packets.
        """
        try:
            async for header, payload in self.__read_packets():
                try:
                    # Read packets from the socket and process them.
                    await self.__process_packet(header, payload)
                except (InvalidDataError, asyncio.TimeoutError):
                    # May be raised by __read_packet()
                    # Either no data or invalid data.
                    pass
        except NotConnectedError:
            asyncio.create_task(self.disconnect())
        except Exception:  # pylint: disable=broad-except  # Catch-all, since we process data from external inputs
            self.__logger.exception("Error reading packet from host %s:%i", self.__host, self.__port)
            asyncio.create_task(self.disconnect())

    async def __get_client_nonce(self) -> bytes:
        """
        Returns a nonce as a bytestring with length 4.
        """
        if self.__next_nonce == 0:
            # os.urandom can block after boot, so we will put it into the executor
            nonce_raw = await asyncio.get_running_loop().run_in_executor(None, os.urandom, 4)
            self.__next_nonce = int.from_bytes(nonce_raw, byteorder="little")

        # Take the next nonce and prepare a new one
        nonce: int = self.__next_nonce
        self.__next_nonce = (self.__next_nonce + 1) % (1 << 32)

        return nonce.to_bytes(4, byteorder="little")  # return as bytes

    async def __get_server_nonce(self) -> bytes:
        """
        Query the server for its nonce. Returns a bytestring  with length 4.
        """
        _, payload = cast(
            tuple[HeaderPayload, bytes],
            await self.send_request(
                device=self, function_id=FunctionID.GET_AUTHENTICATION_NONCE, response_expected=True
            ),
        )
        return payload  # As bytestring with length 4

    async def __authenticate(self, authentication_secret: bytes) -> None:
        self.__logger.debug("Authenticating with secret %s.", authentication_secret)
        client_nonce: bytes
        server_nonce: bytes
        client_nonce, server_nonce = await asyncio.gather(self.__get_client_nonce(), self.__get_server_nonce())

        mac = hmac.new(authentication_secret, digestmod=hashlib.sha1)
        mac.update(server_nonce)
        mac.update(client_nonce)

        digest = mac.digest()
        del mac  # remove it from memory

        await self.send_request(
            device=self,
            function_id=FunctionID.AUTHENTICATE,
            data=pack_payload((client_nonce, digest), "4B 20B"),
            response_expected=False,
        )

    async def __connect(self, authentication_secret: str | bytes | None = None) -> None:
        """
        The __connect() call should be wrapped in a task, so it can be canceled
        by the disconnect() function call. It must be protected by
        `self.__lock`.
        """
        try:
            self.__reader, self.__writer = await asyncio.wait_for(
                asyncio.open_connection(self.__host, self.__port), self.__timeout
            )
        except asyncio.TimeoutError:
            # Catch and reraise the timeout, because we want to get rid of
            # the CancelledError raised by asyncio.wait_for() and also add
            # our own message.
            raise asyncio.TimeoutError(f"Timeout during connection attempt to '{self.__host}:{self.__port}'") from None

        # If we are connected, start the listening task
        self.__running_tasks.add(asyncio.create_task(self.__main_loop()))
        if authentication_secret is not None:
            if isinstance(authentication_secret, str):
                authentication_secret = authentication_secret.encode("ascii")

            await self.__authenticate(authentication_secret)

        self.__logger.info("Tinkerforge IP connection (%s:%i) connected.", self.__host, self.__port)

    async def connect(
        self, host: str | None = None, port: int | None = None, authentication_secret: str | bytes | None = None
    ) -> None:
        """
        Connect to a Tinkerforge host/stack. The parameters host, port and
        authentication_secret are optional and can already be set at object
        creation time. If any of host, port, authentication_secret are set, they
        will overwrite the ones set at creation time.
        The connect() call handles authentication transparently if
        `authentication_secret` is set either at creation or runtime. There is no
        further user intervention necessary.
        """
        if self.__lock is None:
            self.__lock = asyncio.Lock()
        try:
            async with self.__lock:
                if not self.is_connected:
                    # Update all connection parameters before connecting
                    if host is not None:
                        self.__host = host
                    if port is not None:
                        self.__port = port
                    if self.__host is None or self.__port is None:
                        raise TypeError("Invalid hostname")
                    if authentication_secret is None:
                        authentication_secret = self.__authentication_secret

                    # We need to wrap the connection attempt into a task,
                    # because we want to be able to cancel it any time using the
                    # disconnect() call
                    task = asyncio.create_task(self.__connect(authentication_secret))
                    self.__running_tasks.add(task)
                    try:
                        # wait for the task to finish or have it canceled by a
                        # call to disconnect()
                        await task
                    finally:
                        self.__running_tasks.remove(task)
        except OSError as exc:
            if exc.errno == errno.ECONNREFUSED:
                raise ConnectionRefusedError(f"Connection refused by host '{self.__host}:{self.__port}'") from None
            if exc.errno in (errno.ENETUNREACH, errno.EHOSTUNREACH):
                raise NetworkUnreachableError(
                    f"The network for host '{self.__host}:{self.__port}' is unreachable"
                ) from None
            raise

    async def disconnect(self) -> None:
        """
        Cancel all running tasks. The cleanup will be done by the __main_loop.
        Note: Always schedule this as a task, because if the caller is a
        running task, it will cancel it.
        """
        # Cancel any pending connection attempt and disconnect now!
        for task in self.__running_tasks:
            if not task.done():
                task.cancel()

        if self.__lock is None:
            self.__lock = asyncio.Lock()
        async with self.__lock:
            try:
                await asyncio.gather(*self.__running_tasks)
            except asyncio.CancelledError:
                # We cancelled the tasks, so asyncio.CancelledError is expected.
                pass
            finally:
                self.__running_tasks.clear()
            if self.is_connected:
                await self.__close_transport()
                self.__logger.info("Tinkerforge IP connection (%s:%i) closed.", self.__host, self.__port)

    async def __close_transport(self) -> None:
        # Flush data
        assert self.__writer is not None
        try:
            self.__writer.write_eof()
            await self.__writer.drain()
            self.__writer.close()
            await self.__writer.wait_closed()
        except OSError as exc:
            if exc.errno == errno.ENOTCONN:
                pass  # Socket is no longer connected, so we can't send the EOF.
            else:
                raise
        finally:
            self.__writer, self.__reader = None, None
            # Cancel all pending requests, that have not been resolved
            for _, future in self.__pending_requests.items():
                if not future.done():
                    future.set_exception(NotConnectedError("Tinkerforge IP Connection closed."))
            self.__pending_requests = {}
