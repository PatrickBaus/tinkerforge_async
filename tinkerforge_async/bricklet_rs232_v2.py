"""
Module for the RS232 Bricklet 2.0 (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RS232_V2.html) implemented
using Python asyncIO. It does the low-level communication with the Tinkerforge ip connection and also handles conversion
of raw units to SI units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

import asyncio
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple

from .devices import BrickletWithMCU, DeviceIdentifier, Event, _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


class Rs232IOError(Exception):
    """
    An exception raised when there is a read or write error
    """


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    READ = 12
    ERROR_COUNT = 13
    FRAME_READABLE = 16


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The functions available to this bricklet
    """

    WRITE_LOW_LEVEL = 1
    READ_LOW_LEVEL = 2
    ENABLE_READ_CALLBACK = 3
    DISABLE_READ_CALLBACK = 4
    IS_READ_CALLBACK_ENABLED = 5
    SET_CONFIGURATION = 6
    GET_CONFIGURATION = 7
    SET_BUFFER_CONFIG = 8
    GET_BUFFER_CONFIG = 9
    GET_BUFFER_STATUS = 10
    GET_ERROR_COUNT = 11
    SET_FRAME_READABLE_CALLBACK_CONFIGURATION = 14
    GET_FRAME_READABLE_CALLBACK_CONFIGURATION = 15


@unique
class Parity(Enum):
    """
    The parity bit used for error correction. NONE disables parity
    """

    NONE = 0
    ODD = 1
    EVEN = 2


_Parity = Parity  # We need the alias for MyPy type hinting


@unique
class StopBits(Enum):
    """
    The number of empty bits after each byte. Use 2 stop bits for very long
    lines to have more settling time.
    """

    ONE = 1
    TWO = 2


_StopBits = StopBits  # We need the alias for MyPy type hinting


@unique
class WordLength(Enum):
    """
    The number of bits per data word
    """

    LENGTH_5 = 5
    LENGTH_6 = 6
    LENGTH_7 = 7
    LENGTH_8 = 8


_WordLength = WordLength


@unique
class FlowControl(Enum):
    """
    Sets out-of-band hardware flow control using the DTR/DSR and RTS/CTS signals
    """

    OFF = 0
    SOFTWARE = 1
    HARDWARE = 2


_FlowControl = FlowControl


class GetConfiguration(NamedTuple):
    baudrate: int
    parity: Parity
    stopbits: StopBits
    wordlength: WordLength
    flowcontrol: FlowControl


class GetBufferConfig(NamedTuple):
    send_buffer_size: int
    receive_buffer_size: int


class GetBufferStatus(GetBufferConfig):
    pass


class GetErrorCount(NamedTuple):
    error_count_overrun: int
    error_count_parity: int


class BrickletRS232V2(BrickletWithMCU):
    """
    Communicates with RS232 devices
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_RS232_V2
    DEVICE_DISPLAY_NAME = "RS232 Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    Parity = Parity
    StopBits = StopBits
    WordLength = WordLength
    FlowControl = FlowControl

    CALLBACK_FORMATS = {
        CallbackID.READ: "H H 60B",
        CallbackID.ERROR_COUNT: "I I",
        CallbackID.FRAME_READABLE: "H",
    }

    SID_TO_CALLBACK = {0: (CallbackID.READ, CallbackID.ERROR_COUNT, CallbackID.FRAME_READABLE)}

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.__lock: asyncio.Lock | None = None  # We create the lock when needed to ensure the loop is running
        self.__callback_read_buffer = bytearray()

        self.api_version = (2, 0, 1)

    async def __read_low_level(self, length: int) -> tuple[int, bytes]:
        """
        Returns up to *length* characters from receive buffer.

        Instead of polling with this function, you can also use
        callbacks. But note that this function will return available
        data only when the read callback is disabled.
        See :func:`Enable Read Callback` and :cb:`Read` callback.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_LOW_LEVEL,
            data=pack_payload((int(length),), "H"),
            response_expected=True,
        )
        bytes_read: int
        offset: int
        data: bytes
        (
            bytes_read,
            offset,
            data,
        ) = unpack_payload(payload, "H H 60B")
        data = bytes(data[: bytes_read - offset])  # Strip null bytes that are not part of the message
        return offset, data

    async def __write_low_level(self, message_length: int, offset: int, data: bytes) -> int:
        """
        Writes characters to the RS232 interface. The characters can be binary data,
        ASCII or similar is not necessary.

        The return value is the number of characters that were written.

        See :func:`Set Configuration` for configuration possibilities
        regarding baud rate, parity and so on.
        """
        assert len(data) <= 60
        msg = bytearray(data)
        length = len(msg)
        msg.extend([0] * (60 - length))  # always send 60 bytes

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_LOW_LEVEL,
            data=pack_payload(
                (
                    message_length,
                    int(offset),
                    msg,
                ),
                "H H 60B",
            ),
            response_expected=True,
        )
        bytes_written = unpack_payload(payload, "B")
        if bytes_written != length:
            raise Rs232IOError(
                f"Error writing message {data!r}, offset: {offset}. "
                f"{bytes_written} bytes written out of {length} bytes."
            )
        return bytes_written

    async def set_read_callback(self, enable: bool = False, response_expected: bool = True) -> None:
        """
        Enables/Disables the :cb:`Read` callback. When enabled, it will disable the :cb:`Frame Readable` callback.

        By default the callback is disabled.
        """
        if enable:
            await self.ipcon.send_request(
                device=self, function_id=FunctionID.ENABLE_READ_CALLBACK, response_expected=response_expected
            )
        else:
            await self.ipcon.send_request(
                device=self, function_id=FunctionID.DISABLE_READ_CALLBACK, response_expected=response_expected
            )

    async def is_read_callback_enabled(self) -> bool:
        """
        Returns *true* if the :cb:`Read` callback is enabled,
        *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_READ_CALLBACK_ENABLED, response_expected=True
        )

        return unpack_payload(payload, "!")

    async def set_configuration(  # pylint: disable=too-many-arguments
        self,
        baudrate: int = 115200,
        parity: _Parity | int = Parity.NONE,
        stopbits: _StopBits | int = StopBits.ONE,
        wordlength: _WordLength | int = WordLength.LENGTH_8,
        flowcontrol: _FlowControl | int = FlowControl.OFF,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration for the RS232 communication.
        """
        assert 100 <= baudrate <= 2000000
        parity = Parity(parity)
        stopbits = StopBits(stopbits)
        wordlength = WordLength(wordlength)
        flowcontrol = FlowControl(flowcontrol)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload(
                (
                    int(baudrate),
                    parity.value,
                    stopbits.value,
                    wordlength.value,
                    flowcontrol.value,
                ),
                "I B B B B",
            ),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`Set Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )

        baudrate, parity, stopbits, wordlength, flowcontrol = unpack_payload(payload, "I B B B B")
        return GetConfiguration(
            baudrate,
            Parity(parity),
            StopBits(stopbits),
            WordLength(wordlength),
            FlowControl(flowcontrol),
        )

    async def set_buffer_config(
        self, send_buffer_size: int = 5120, receive_buffer_size: int = 5120, response_expected: bool = True
    ) -> None:
        """
        Sets the send and receive buffer size in byte. In total the buffers have to be
        10240 byte (10KiB) in size, the minimum buffer size is 1024 byte (1KiB) for each.

        The current buffer content is lost if this function is called.

        The send buffer holds data that is given by :func:`Write` and
        can not be written yet. The receive buffer holds data that is
        received through RS232 but could not yet be send to the
        user, either by :func:`Read` or through :cb:`Read` callback.
        """
        assert 1024 <= send_buffer_size <= 9216
        assert 1024 <= receive_buffer_size <= 9216
        assert send_buffer_size + receive_buffer_size <= 10240

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BUFFER_CONFIG,
            data=pack_payload((int(send_buffer_size), int(receive_buffer_size)), "H H"),
            response_expected=response_expected,
        )

    async def get_buffer_config(self) -> GetBufferConfig:
        """
        Returns the buffer configuration as set by :func:`Set Buffer Config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BUFFER_CONFIG, response_expected=True
        )

        return GetBufferConfig(*unpack_payload(payload, "H H"))

    async def get_buffer_status(self) -> GetBufferStatus:
        """
        Returns the number of bytes in use by the send and receive buffer.

        See :func:`Set Buffer Config` for buffer size configuration.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BUFFER_STATUS, response_expected=True
        )

        return GetBufferStatus(*unpack_payload(payload, "H H"))

    async def get_error_count(self) -> GetErrorCount:
        """
        Returns the current number of overrun and parity errors.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_COUNT, response_expected=True
        )

        return GetErrorCount(*unpack_payload(payload, "I I"))

    async def set_frame_readable_callback_configuration(
        self, frame_size: int = 0, response_expected: bool = True
    ) -> None:
        """
        Configures the :cb:`Frame Readable` callback. The frame size is the number of bytes, that have to be readable to
        trigger the callback. A frame size of 0 disables the callback. A frame size greater than 0 enables the callback
        and disables the :cb:`Read` callback.

        By default, the callback is disabled.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        assert 0 <= frame_size <= 9216

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
            data=pack_payload((int(frame_size),), "H"),
            response_expected=response_expected,
        )

    async def get_frame_readable_callback_configuration(self) -> int:
        """
        Returns the callback configuration as set by :func:`Set Frame Readable Callback Configuration`.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION, response_expected=True
        )

        return unpack_payload(payload, "H")

    async def write(self, message: bytes | str) -> int:
        """
        Writes characters to the RS232 interface. The characters can be binary data,
        ASCII or similar is not necessary.

        The return value is the number of characters that were written.

        See :func:`Set Configuration` for configuration possibilities
        regarding baud rate, parity and so on.
        """
        if not isinstance(message, bytes):
            message = message.encode("utf-8")
        if len(message) > 65535:
            raise RuntimeError("Message length must not exceed 65535 bytes.")

        # Split the message in chunks of 60 bytes
        try:
            chunks = [message[i : i + 60] for i in range(0, len(message), 60)]
        except ValueError:
            # Raised if the length is 0
            chunks = [
                b"",
            ]

        if self.__lock is None:
            self.__lock = asyncio.Lock()

        # lock the connection to ensure, that the message does not get chopped up
        bytes_written = 0
        async with self.__lock:
            for count, chunk in enumerate(chunks):
                bytes_written += await self.__write_low_level(
                    message_length=len(message), offset=count * 60, data=chunk
                )

        return bytes_written

    async def __find_first_block(self, length: int) -> tuple[int, bytes]:
        """
        Read the RS232 interface until we find a chunk with id 0, the start of a new
        transaction.
        """
        while "buffer not cleared":
            offset, data = await self.__read_low_level(length)
            if offset == 0:
                return offset, data

        assert False, "unreachable"

    async def read(self, length: int) -> bytes:
        """
        Returns up to *length* characters from receive buffer.

        Instead of polling with this function, you can also use
        callbacks. But note that this function will return available
        data only when the read callback is disabled.
        See :func:`Enable Read Callback` and :cb:`Read` callback.
        """
        if length == 0:
            return b""

        if self.__lock is None:
            self.__lock = asyncio.Lock()

        async with self.__lock:
            result = bytearray()
            number_of_chunks = length // 60 + 1 * bool(length % 60)

            # Get the first chunk and check if it is in sync
            offset, data = await self.__read_low_level(length)
            if offset != 0:
                # Drop all chunks, until we find chunk 0
                offset, data = await self.__find_first_block(length)
            result.extend(data)

            for i in range(1, number_of_chunks):
                offset, data = await self.__read_low_level(length)
                if len(data) == 0 and offset == 0:
                    # The bricklet returns 0, if there is no more data
                    break
                if offset != i * 60:
                    # If someone else is reading our stream, they will snatch a block.
                    # Abort the read and throw an error. A new call to read() will clean up the
                    # mess and drop all remaining chunks.
                    raise Rs232IOError(f"Read out of sync. Wanted chunk {i}, got chunk {offset//60}. Data: {data!r}.")
                result.extend(data)
            return bytes(result)

    async def read_events(  # pylint: disable=too-many-branches
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        registered_events = set()
        if events:
            for event in events:
                registered_events.add(self.CallbackID(event))
        if sids is not None:
            for sid in sids:
                for callback in self.SID_TO_CALLBACK.get(sid, []):
                    registered_events.add(callback)

        if events is None and sids is None:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                if function_id is CallbackID.READ:
                    final_size, offset, data = value
                    if final_size > offset + 60:
                        # There is at least one more chunk to read, so we just read the full length and append it
                        self.__callback_read_buffer.extend(data)
                    else:
                        # Read the last chunk, which does not have the full length
                        self.__callback_read_buffer.extend(data[: final_size - offset])
                    if len(self.__callback_read_buffer) == final_size:
                        # If we are done reading, flush the buffer and yield the result
                        result = bytes(self.__callback_read_buffer)
                        self.__callback_read_buffer = bytearray()
                        yield Event(self, 0, function_id, result)
                    else:
                        continue
                else:
                    yield Event(self, 1, function_id, value)
