# -*- coding: utf-8 -*-
"""
This module implements the underlying ip connection to the Bricks and Bricklets.
See https://www.tinkerforge.com/de/doc/Low_Level_Protocols/TCPIP.html for
details.
"""
import asyncio
from enum import Enum, Flag, unique
import errno    # The error numbers can be found in /usr/include/asm-generic/errno.h
import hmac
import hashlib
import logging
import os
import struct

from async_timeout import timeout

from .ip_connection_helper import base58decode, pack_payload, unpack_payload
from .devices import DeviceIdentifier, UnknownFunctionError


class NotConnectedError(ConnectionError):
    """
    Raised if there is no connection
    """


@unique
class FunctionID(Enum):
    """
    Function calls needed to establish a connection and enumerate Bricks and
    Bricklets
    """
    GET_AUTHENTICATION_NONCE = 1
    AUTHENTICATE = 2
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


DEFAULT_WAIT_TIMEOUT = 2.5  # in seconds


class IPConnectionAsync:
    """
    The implementation of the Tinkerforge TCP/IP protocol. See
    See https://www.tinkerforge.com/en/doc/Low_Level_Protocols/TCPIP.html
    for details.
    """
    BROADCAST_UID = 0  # The uid used to broadcast enumeration events

    HEADER_FORMAT = '<IBBBB'  # little endian (<), uid (I, uint32), size (B, uint8), function id, squence number, flags

    @property
    def uid(self):
        """
        The uid used by the IP connection for authentication. It needs a uid
        to talk to the user.
        """
        return 1

    @property
    def enumeration_queue(self):
        """
        Returns the enumeration queue, used to signal sensors joining or leaving
        the network.
        """
        return self.__enumeration_queue

    @property
    def timeout(self):
        """
        Returns the timeout for async operations in seconds.
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        """
        The timeout used for reading and writing packets, if not set, the
        DEFAULT_WAIT_TIMEOUT will be used.
        """
        self.__timeout = abs(int(value))

    @property
    def is_connected(self):
        """
        Returns *True* if, the connection is established.
        """
        return self.__writer is not None and not self.__writer.is_closing()

    def __init__(self, host=None, port=4223, authentication_secret=None):
        self.__host = host
        self.__port = port
        self.__authentication_secret = authentication_secret

        self.__sequence_number = 0
        self.__timeout = DEFAULT_WAIT_TIMEOUT
        self.__pending_requests = {}
        self.__next_nonce = 0

        self.__devices = {}

        self.__logger = logging.getLogger(__name__)

        # These will be assigned during connect()
        self.__connection_task = None
        self.__reader, self.__writer = None, None
        self.__main_task = None
        self.__lock = None
        self.__sequence_number_queue = None
        self.__enumeration_queue = None

    def __repr__(self):
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}(host={self.__host}, port={self.__port}, authentication_secret={self.__authentication_secret})"

    def __str__(self):
        return f"IPConnectionAsync({self.__host}:{self.__port})"

    @staticmethod
    def __parse_header(data):
        uid, payload_size, function_id, options, flags = struct.unpack_from(IPConnectionAsync.HEADER_FORMAT, data)
        try:
            function_id = FunctionID(function_id)
            if function_id in (FunctionID.GET_AUTHENTICATION_NONCE, FunctionID.AUTHENTICATE) and not uid == 1:
                # Only the special uid 1 can reply with GET_AUTHENTICATION_NONCE or AUTHENTICATE
                function_id = function_id.value
        except ValueError:
            # Do not assign an enum, leave the int
            pass
        sequence_number = None if (options >> 4) & 0b1111 == 0 else (options >> 4) & 0b1111   # There is no sequence number if it is a callback (sequence_number == 0)
        response_expected = bool(options >> 3 & 0b1)
    #    options = options & 0b111 # Options for future use
        try:
            flags = Flags(flags)
        except ValueError:
            # Do not assign an enum, leave the int
            pass

        return payload_size, \
            {
                'uid': uid,
                'sequence_number': sequence_number,
                'response_expected': response_expected,
                'function_id': function_id,
                'flags': flags,
            }

    async def __create_packet_header(self, payload_size, function_id, uid=None, response_expected=False):
        uid = IPConnectionAsync.BROADCAST_UID if uid is None else uid
        packet_size = payload_size + struct.calcsize(IPConnectionAsync.HEADER_FORMAT)
        sequence_number = await self.__sequence_number_queue.get()
        response_expected = bool(response_expected)

        sequence_number_and_options = (sequence_number << 4) | response_expected << 3

        return (struct.pack(IPConnectionAsync.HEADER_FORMAT, uid, packet_size, function_id, sequence_number_and_options, Flags.OK.value),  # pylint: disable=no-member
                sequence_number)

    def add_device(self, device):
        """
        Add a brick or bricklet to the ip connection. This is required for
        callbacks.
        """
        self.__logger.debug("Adding device: %s.", device)
        self.__devices[device.uid] = device

    async def enumerate(self):
        """
        Broadcasts an enumerate request. All devices will respond with an
        enumerate callback.
        Returns: None, it does not support 'response_expected'
        """
        self.__logger.debug("Enumerating Node.")
        await self.send_request(
            device=None,
            function_id=FunctionID.ENUMERATE
        )

    async def send_request(self, device, function_id, data=b'', response_expected=False):
        """
        Creates a request, by prepending a header to the data and sends it to
        the Tinkerforge host.
        Returns: None, if 'response_expected' is *False*, else it will return
        a tuple (header, payload) returned by the host.
        """
        if not self.is_connected:
            raise NotConnectedError("Tinkerforge IP Connection not connected.")

        header, sequence_number = await self.__create_packet_header(
            payload_size=len(data),
            function_id=function_id.value,
            uid=0 if device is None else device.uid,
            response_expected=response_expected,
        )

        request = header + data

        # If we are waiting for a response, send the request, then pass on the response as a future
        self.__logger.debug("Sending request to device %(device)s (%(uid)s) and function %(function_id)s with sequence_number %(sequence_number)s: %(header)s - %(payload)s.", {'device': device if device is not None else "all", 'uid': device.uid if device is not None else "all", 'function_id': function_id, 'sequence_number': sequence_number, 'header': header, 'payload': data})
        try:
            self.__writer.write(request)
            if response_expected:
                self.__logger.debug("Waiting for reply for request number %i.", sequence_number)
                # The future will be resolved by the main_loop() and __process_packet()
                self.__pending_requests[sequence_number] = asyncio.Future()
                header, payload = await asyncio.wait_for(self.__pending_requests[sequence_number], self.__timeout)
                self.__logger.debug('Got reply for request number %(sequence_number)s: %(header)s - %(payload)s.', {'sequence_number': sequence_number, 'header': header, 'payload': payload})
                return header, payload
        finally:
            # Return the sequence number
            self.__sequence_number_queue.put_nowait(sequence_number)

    @staticmethod
    def __parse_enumerate_payload(payload):
        uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type \
            = unpack_payload(payload, '8s 8s c 3B 3B H B')

        enumeration_type = EnumerationType(enumeration_type)

        try:
            device_identifier = DeviceIdentifier(device_identifier)
        except ValueError:
            # Do not assign an enum, leave the int
            pass

        try:
            position = int(position)
        except ValueError:
            # It is probably a bricklet, which does have an alphabetic position desciptor
            pass

        # See https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html#callbacks for details on the payload
        # We will return None for all 'invalid' fields instead of garbage like the Tinkerforge API
        return {'uid': base58decode(uid),   # Stop the base58 encoded nonsense and use the uint32_t id
                'connected_uid': None if (enumeration_type is EnumerationType.DISCONNECTED or connected_uid == '0') else base58decode(connected_uid),
                'position':  None if enumeration_type is EnumerationType.DISCONNECTED else position,
                'hardware_version': None if enumeration_type is EnumerationType.DISCONNECTED else hardware_version,
                'firmware_version': None if enumeration_type is EnumerationType.DISCONNECTED else firmware_version,
                'device_id': None if enumeration_type is EnumerationType.DISCONNECTED else device_identifier,
                'enumeration_type': enumeration_type,
                }

    async def __read_packet(self):
        if not self.is_connected:
            raise NotConnectedError("Tinkerforge IP Connection not connected.")
        try:
            async with timeout(self.__timeout):
                data = await self.__reader.read(struct.calcsize(IPConnectionAsync.HEADER_FORMAT))
                packet_size, header = self.__parse_header(data)

                payload = await self.__reader.read(packet_size - struct.calcsize(IPConnectionAsync.HEADER_FORMAT))

                return header, payload
        except asyncio.TimeoutError:
            return None, None   # No new packets. Nothing to do here.
        except ConnectionResetError as exc:
            raise NotConnectedError("Tinkerforge IP Connection not connected.") from exc

    async def __process_packet(self, header, payload):
        # There are two types of packets:
        # - Broadcasts/Callbacks
        # - Replies
        # We need to treat them differently

        # Callbacks first, because most packets will be callbacks,
        # so it is more efficient to do them first
        if header['sequence_number'] is None:
            try:
                # Try to process the callback by handing it to the device
                self.__devices[header['uid']]._process_callback(header, payload)
            except (KeyError, UnknownFunctionError):
                # KeyError: raised if either the device is not registered with us or there is no output queue registered
                # UnknownFunctionError is raised by _process_callback if there is no local function to process the callback.
                # Maybe it is a global callback like an enumeration callback
                try:
                    header['function_id'] = FunctionID(header['function_id'])
                    # This packet must be processed by the ip connection
                    if header['function_id'] is FunctionID.CALLBACK_ENUMERATE:
                        payload = self.__parse_enumerate_payload(payload)
                        self.__logger.debug("Received enumeration: %(header)s - %(payload)s.", {'header': header, 'payload': payload})
                        try:
                            self.__enumeration_queue.put_nowait(payload)
                        except asyncio.QueueFull:
                            dropped_payload = self.__enumeration_queue.get_nowait()
                            self.__logger.warning("Dropping packets. Too many callbacks. Dropped payload: %s.", dropped_payload)
                            self.__enumeration_queue.put_nowait(payload)

                except ValueError:
                    # raised if the functionID is unknown. This can happen if there was no device output queue
                    # registered with the callback.
                    pass
        elif header['response_expected']:
            try:
                # Mark the future as done
                future = self.__pending_requests.pop(header['sequence_number'])
                if header['flags'] is Flags.OK:
                    future.set_result((header, payload))
                elif header['flags'] is Flags.FUNCTION_NOT_SUPPORTED:
                    future.set_exception(AttributeError(f"Function not supported: {header['function_id']}."))
                elif header['flags'] is Flags.INVALID_PARAMETER:
                    future.set_exception(ValueError("Invalid parameter."))
                else:
                    future.set_result((header, payload))
            except KeyError:
                # Drop the packet, because it is not our sequence number
                pass
            except asyncio.InvalidStateError:
                self.__logger.exception("Invalid sequence number: %i.", header['sequence_number'])
        else:
            self.__logger.info("Unknown packet: %(header)s - %(payload)s.", {'header': header, 'payload': payload})

    async def main_loop(self):
        """
        The main loop, that is responsible for processing incoming packets.
        """
        try:
            while "loop not canceled":
                # Read packets from the socket and process them.
                header, payload = await self.__read_packet()
                if header is not None:
                    await self.__process_packet(header, payload)
        except (asyncio.CancelledError, NotConnectedError):
            # No cleanup required
            pass
        finally:
            self.__main_task = None
            if self.is_connected:
                await self.__close_transport()

    async def __get_client_nonce(self):
        """
        Returns a nonce as a bytestring  with length 4.
        """
        if self.__next_nonce == 0:
            # os.urandom can block after boot, so we will put it into the executor
            nonce = await asyncio.get_running_loop().run_in_executor(None, os.urandom, 4)
            self.__next_nonce = int.from_bytes(nonce, byteorder='little')

        # Take the next nonce and prepare a new one
        nonce = self.__next_nonce
        self.__next_nonce = (self.__next_nonce + 1) % (1 << 32)

        return nonce.to_bytes(4, byteorder='little')    # return as bytes

    async def __get_server_nonce(self):
        """
        Query the server for its nonce. Returns a bytestring  with length 4.
        """
        _, payload = await self.send_request(
            device=self,
            function_id=FunctionID.GET_AUTHENTICATION_NONCE,
            response_expected=True
        )
        return payload    # As bytestring with length 4

    async def __authenticate(self, authentication_secret):
        self.__logger.debug("Authenticating with secret %s.", authentication_secret)
        client_nonce, server_nonce = await asyncio.gather(self.__get_client_nonce(), self.__get_server_nonce())

        mac = hmac.new(authentication_secret, digestmod=hashlib.sha1)
        mac.update(server_nonce)
        mac.update(client_nonce)

        digest = mac.digest()
        del mac     # remove it from memory

        await self.send_request(
            device=self,
            function_id=FunctionID.AUTHENTICATE,
            data=pack_payload((client_nonce, digest), '4B 20B'),
            response_expected=False,
        )

    async def __connect(self, host=None, port=None, authentication_secret=None):
        """
        The __connect() call should be wrapped in a task, so it can be canceled
        by the disconnect() function call. It must be protected by
        `self.__lock`.
        """
        try:
            self.__reader, self.__writer = await asyncio.wait_for(
                asyncio.open_connection(self.__host, self.__port),
                self.__timeout
            )
        except asyncio.TimeoutError:
            # Catch and reraise the timeout, because we want to get rid of
            # the CancelledError raised by asyncio.wait_for() and also add
            # our own message.
            raise asyncio.TimeoutError(
                f"Timeout during connection attempt to {self.__host}:{self.__port}"
            ) from None

        # If we are connected, start the listening task
        self.__main_task = asyncio.create_task(self.main_loop())
        if authentication_secret is not None:
            try:
                authentication_secret = authentication_secret.encode('ascii')
            except AttributeError:
                pass    # already a bytestring

            await self.__authenticate(authentication_secret)

        self.__logger.info("Tinkerforge IP connection connected.")

    async def connect(self, host=None, port=None, authentication_secret=None):
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
        async with self.__lock:
            if not self.is_connected:
                try:
                    # Update all connection parameters before connecting
                    if host is not None:
                        self.__host = host
                    if port is not None:
                        self.__port = port
                    if self.__host is None or self.__port is None:
                        raise TypeError('Invalid hostname')
                    if authentication_secret is None:
                        authentication_secret = self.__authentication_secret

                    self.__enumeration_queue = asyncio.Queue(maxsize=20)
                    self.__sequence_number_queue = asyncio.Queue(maxsize=15)
                    for i in range(1, 16):
                        self.__sequence_number_queue.put_nowait(i)
                    # We need to wrap the connection attempt into a task,
                    # because we want to be able to cancel it any time using the
                    # disconnect() call
                    self.__connection_task = asyncio.create_task(
                        self.__connect(host, port, authentication_secret)
                    )
                    # Actually wait for the task to finish
                    await self.__connection_task
                finally:
                    self.__connection_task = None

    async def disconnect(self):
        """
        Disconnect from a tinkerforge host and clean up.
        """
        if self.__lock is None:
            self.__lock = asyncio.Lock()
        if self.__connection_task is not None:
            self.__connection_task.cancel()
            try:
                await self.__connection_task
            except asyncio.CancelledError:
                pass

        async with self.__lock:
            try:
                if self.__main_task is not None and not self.__main_task.done():
                    self.__main_task.cancel()
                    try:
                        await self.__main_task
                    except asyncio.CancelledError:
                        pass
            finally:
                self.__lock = None

    async def __close_transport(self):
        # Flush data
        try:
            self.__writer.write_eof()
            await self.__writer.drain()
            self.__writer.close()
            await self.__writer.wait_closed()
        except OSError as exc:
            if exc.errno == errno.ENOTCONN:
                pass    # Socket is no longer connected, so we can't send the EOF.
            else:
                raise
        finally:
            self.__writer, self.__reader = None, None
            # Cancel all pending requests, that have not been resolved
            for _, future in self.__pending_requests.items():
                if not future.done():
                    future.set_exception(NotConnectedError("Tinkerforge IP Connection closed."))
            self.__pending_requests = {}
            self.__logger.info("Tinkerforge IP connection (%s:%i) closed.", self.__host, self.__port)
