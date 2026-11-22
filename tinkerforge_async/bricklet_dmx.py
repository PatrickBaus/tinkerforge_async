"""
Module for the Tinkerforge DMX Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DMX_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

import asyncio
from collections.abc import Iterable, Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, Event, _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .streams import Chunk, StreamAssembler, read_stream, write_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    FRAME_STARTED = 14
    FRAME_AVAILABLE = 15
    FRAME = 16
    FRAME_ERROR_COUNT = 17


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_DMX_MODE = 1
    GET_DMX_MODE = 2
    WRITE_FRAME_LOW_LEVEL = 3
    READ_FRAME_LOW_LEVEL = 4
    SET_FRAME_DURATION = 5
    GET_FRAME_DURATION = 6
    GET_FRAME_ERROR_COUNT = 7
    SET_COMMUNICATION_LED_CONFIG = 8
    GET_COMMUNICATION_LED_CONFIG = 9
    SET_ERROR_LED_CONFIG = 10
    GET_ERROR_LED_CONFIG = 11
    SET_FRAME_CALLBACK_CONFIG = 12
    GET_FRAME_CALLBACK_CONFIG = 13


@unique
class DMXMode(Enum):
    """
    The dmx mode options
    """

    MASTER = 0
    SLAVE = 1


@unique
class CommunicationLEDConfig(Enum):
    """
    The communication led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_COMMUNICATION = 3


@unique
class ErrorLEDConfig(Enum):
    """
    The error led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_ERROR = 3


class ReadFrame(NamedTuple):
    frame_length: int
    frame_chunk_offset: int
    frame_chunk_data: tuple[int, ...]
    frame_number: int


class ReadFrameResult(NamedTuple):
    frame_number: int
    frame: bytes


class GetFrameErrorCount(NamedTuple):
    overrun_error_count: int
    framing_error_count: int


class GetFrameCallbackConfig(NamedTuple):
    frame_started_callback_enabled: bool
    frame_available_callback_enabled: bool
    frame_callback_enabled: bool
    frame_error_count_callback_enabled: bool


class FrameEvent(NamedTuple):
    frame_number: int
    frame: bytes


class BrickletDMX(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    DMX master and slave
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DMX
    DEVICE_DISPLAY_NAME = "DMX Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    DMXMode: TypeAlias = DMXMode
    CommunicationLEDConfig: TypeAlias = CommunicationLEDConfig
    ErrorLEDConfig: TypeAlias = ErrorLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.FRAME_STARTED: "",
        CallbackID.FRAME_AVAILABLE: "I",
        CallbackID.FRAME: "H H 56B I",
        CallbackID.FRAME_ERROR_COUNT: "I I",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.FRAME_STARTED,)),
        Channel(1, callbacks=(CallbackID.FRAME_AVAILABLE,)),
        Channel(2, callbacks=(CallbackID.FRAME_ERROR_COUNT,)),
        Channel(3, callbacks=(CallbackID.FRAME,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()
        self._stream_assemblers = {
            CallbackID.FRAME: StreamAssembler(),
        }

    async def set_dmx_mode(self, dmx_mode: DMXMode | int = DMXMode.MASTER, response_expected: bool = True) -> None:
        """
        Sets the DMX mode to either master or slave.

        Calling this function sets frame number to 0.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DMX_MODE,
            data=pack_payload((DMXMode(dmx_mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_dmx_mode(self) -> DMXMode:
        """
        Returns the DMX mode, as set by :func:`set_dmx_mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DMX_MODE, response_expected=True
        )
        return DMXMode(unpack_payload(payload, "B"))

    async def write_frame_low_level(
        self,
        frame_length: int,
        frame_chunk_offset: int,
        frame_chunk_data: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Writes a DMX frame. The maximum frame size is 512 byte. Each byte represents one channel.

        The next frame can be written after the :attr:`CallbackID.FRAME_STARTED` callback was called. The frame
        is double buffered, so a new frame can be written as soon as the writing of the prior frame
        starts.

        The data will be transfered when the next frame duration ends, see :func:`set_frame_duration`.

        Generic approach:

        * Set the frame duration to a value that represents the number of frames per second you want to achieve.
        * Set channels for first frame.
        * Wait for the :attr:`CallbackID.FRAME_STARTED` callback.
        * Set channels for next frame.
        * Wait for the :attr:`CallbackID.FRAME_STARTED` callback.
        * and so on.

        This approach ensures that you can set new DMX data with a fixed frame rate.

        This function can only be called in master mode.
        """
        frame_length = int(frame_length)
        check_range("frame_length", frame_length, 0, 512)
        frame_chunk_offset = int(frame_chunk_offset)
        check_range("frame_chunk_offset", frame_chunk_offset, 0, 65535)
        check_length("frame_chunk_data", frame_chunk_data, 60)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_FRAME_LOW_LEVEL,
            data=pack_payload((frame_length, frame_chunk_offset, list(map(int, frame_chunk_data))), "H H 60B"),
            response_expected=response_expected,
        )

    async def write_frame(self, frame: bytes | Sequence[int]) -> None:
        """
        Writes a DMX frame. The maximum frame size is 512 byte. Each byte represents one channel.

        The next frame can be written after the :attr:`CallbackID.FRAME_STARTED` callback was called. The frame
        is double buffered, so a new frame can be written as soon as the writing of the prior frame
        starts.

        The data will be transfered when the next frame duration ends, see :func:`set_frame_duration`.

        Generic approach:

        * Set the frame duration to a value that represents the number of frames per second you want to achieve.
        * Set channels for first frame.
        * Wait for the :attr:`CallbackID.FRAME_STARTED` callback.
        * Set channels for next frame.
        * Wait for the :attr:`CallbackID.FRAME_STARTED` callback.
        * and so on.

        This approach ensures that you can set new DMX data with a fixed frame rate.

        This function can only be called in master mode.

        This function transfers the complete frame stream and calls :func:`write_frame_low_level` as often as necessary.
        Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.write_frame_low_level(length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk, [int(item) for item in frame], name="frame", chunk_size=60, padding=0, max_length=65535
            )

    async def read_frame_low_level(self) -> ReadFrame:
        """
        Returns the last frame that was written by the DMX master. The size of the array
        is equivalent to the number of channels in the frame. Each byte represents one channel.

        The next frame is available after the :attr:`CallbackID.FRAME_AVAILABLE` callback was called.

        Generic approach:

        * Call :func:`read_frame` to get first frame.
        * Wait for the :attr:`CallbackID.FRAME_AVAILABLE` callback.
        * Call :func:`read_frame` to get second frame.
        * Wait for the :attr:`CallbackID.FRAME_AVAILABLE` callback.
        * and so on.

        Instead of polling this function you can also use the :attr:`CallbackID.FRAME` callback.
        You can enable it with :func:`set_frame_callback_config`.

        The frame number starts at 0 and it is increased by one with each received frame.

        This function can only be called in slave mode.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READ_FRAME_LOW_LEVEL, response_expected=True
        )
        frame_length, frame_chunk_offset, frame_chunk_data, frame_number = unpack_payload(payload, "H H 56B I")
        return ReadFrame(frame_length, frame_chunk_offset, tuple(frame_chunk_data), frame_number)

    async def read_frame(self) -> ReadFrameResult:
        """
        Returns the last frame that was written by the DMX master. The size of the array
        is equivalent to the number of channels in the frame. Each byte represents one channel.

        The next frame is available after the :attr:`CallbackID.FRAME_AVAILABLE` callback was called.

        Generic approach:

        * Call :func:`read_frame` to get first frame.
        * Wait for the :attr:`CallbackID.FRAME_AVAILABLE` callback.
        * Call :func:`read_frame` to get second frame.
        * Wait for the :attr:`CallbackID.FRAME_AVAILABLE` callback.
        * and so on.

        Instead of polling this function you can also use the :attr:`CallbackID.FRAME` callback.
        You can enable it with :func:`set_frame_callback_config`.

        The frame number starts at 0 and it is increased by one with each received frame.

        This function can only be called in slave mode.

        This function transfers the complete frame stream and calls :func:`read_frame_low_level` as often as necessary.
        Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.read_frame_low_level()
            return Chunk(result.frame_length, result.frame_chunk_offset, result.frame_chunk_data, result)

        async with self._stream_lock:
            data, result = await read_stream(read_chunk, name="frame", chunk_size=56)
        return ReadFrameResult(result.frame_number, bytes(data))

    async def set_frame_duration(
        self, frame_duration: Duration = Decimal("0.1"), response_expected: bool = True
    ) -> None:
        """
        Sets the duration of a frame.

        Example: If you want to achieve 20 frames per second, you should
        set the frame duration to 50ms (50ms * 20 = 1 second).

        If you always want to send a frame as fast as possible you can set
        this value to 0.

        This setting is only used in master mode.

        Units: frame_duration in s.
        """
        frame_duration_raw = seconds_to_ms(frame_duration)
        check_range("frame_duration", frame_duration_raw, 0, 65535, frame_duration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_DURATION,
            data=pack_payload((frame_duration_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_frame_duration(self) -> Decimal:
        """
        Returns the frame duration as set by :func:`set_frame_duration`.

        Units: frame_duration in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_DURATION, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "H"))

    async def get_frame_error_count(self) -> GetFrameErrorCount:
        """
        Returns the current number of overrun and framing errors.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_ERROR_COUNT, response_expected=True
        )
        overrun_error_count, framing_error_count = unpack_payload(payload, "I I")
        return GetFrameErrorCount(overrun_error_count, framing_error_count)

    async def set_communication_led_config(
        self,
        config: CommunicationLEDConfig | int = CommunicationLEDConfig.SHOW_COMMUNICATION,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the communication LED configuration. By default the LED shows
        communication traffic, it flickers once for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COMMUNICATION_LED_CONFIG,
            data=pack_payload((CommunicationLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_communication_led_config(self) -> CommunicationLEDConfig:
        """
        Returns the configuration as set by :func:`set_communication_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COMMUNICATION_LED_CONFIG, response_expected=True
        )
        return CommunicationLEDConfig(unpack_payload(payload, "B"))

    async def set_error_led_config(
        self, config: ErrorLEDConfig | int = ErrorLEDConfig.SHOW_ERROR, response_expected: bool = True
    ) -> None:
        """
        Sets the error LED configuration.

        By default the error LED turns on if there is any error (see :attr:`CallbackID.FRAME_ERROR_COUNT`
        callback). If you call this function with the Show-Error option again, the LED
        will turn off until the next error occurs.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ERROR_LED_CONFIG,
            data=pack_payload((ErrorLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_error_led_config(self) -> ErrorLEDConfig:
        """
        Returns the configuration as set by :func:`set_error_led_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_LED_CONFIG, response_expected=True
        )
        return ErrorLEDConfig(unpack_payload(payload, "B"))

    async def set_frame_callback_config(
        self,
        frame_started_callback_enabled: bool = True,
        frame_available_callback_enabled: bool = True,
        frame_callback_enabled: bool = False,
        frame_error_count_callback_enabled: bool = False,
        response_expected: bool = True,
    ) -> None:
        """
        Enables/Disables the different callbacks. By default the
        :attr:`CallbackID.FRAME_STARTED` callback and :attr:`CallbackID.FRAME_AVAILABLE` callback are enabled while
        the :attr:`CallbackID.FRAME` callback and :attr:`CallbackID.FRAME_ERROR_COUNT` callback are disabled.

        If you want to use the :attr:`CallbackID.FRAME` callback you can enable it and disable
        the :attr:`CallbackID.FRAME_AVAILABLE` callback at the same time. It becomes redundant in
        this case.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_CALLBACK_CONFIG,
            data=pack_payload(
                (
                    bool(frame_started_callback_enabled),
                    bool(frame_available_callback_enabled),
                    bool(frame_callback_enabled),
                    bool(frame_error_count_callback_enabled),
                ),
                "! ! ! !",
            ),
            response_expected=response_expected,
        )

    async def get_frame_callback_config(self) -> GetFrameCallbackConfig:
        """
        Returns the frame callback config as set by :func:`set_frame_callback_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_CALLBACK_CONFIG, response_expected=True
        )
        (
            frame_started_callback_enabled,
            frame_available_callback_enabled,
            frame_callback_enabled,
            frame_error_count_callback_enabled,
        ) = unpack_payload(payload, "! ! ! !")
        return GetFrameCallbackConfig(
            frame_started_callback_enabled,
            frame_available_callback_enabled,
            frame_callback_enabled,
            frame_error_count_callback_enabled,
        )

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.FRAME_STARTED:
            return 0, None
        if callback_id is CallbackID.FRAME_AVAILABLE:
            return 1, value
        overrun_error_count, framing_error_count = value
        return 2, GetFrameErrorCount(overrun_error_count, framing_error_count)

    @override
    def _to_events(  # pylint: disable=too-many-locals,too-many-return-statements,too-many-branches
        self, callback_id: CallbackID, value: Any, sids: Sequence[int] | None
    ) -> Iterable[Event]:
        if callback_id is CallbackID.FRAME:
            frame_length, frame_chunk_offset, frame_chunk_data, frame_number = value
            data = self._stream_assemblers[CallbackID.FRAME].add(frame_length, frame_chunk_offset, frame_chunk_data)
            if data is None:
                return ()
            return (Event(self, 3, callback_id, FrameEvent(frame_number, bytes(data))),)
        return super()._to_events(callback_id, value, sids)
