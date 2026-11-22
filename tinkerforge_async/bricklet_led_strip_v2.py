"""
Module for the Tinkerforge LED Strip Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/LEDStripV2_Bricklet_Python.html) implemented using
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
from collections.abc import Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity
from .streams import Chunk, read_stream, write_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    FRAME_STARTED = 6


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_LED_VALUES_LOW_LEVEL = 1
    GET_LED_VALUES_LOW_LEVEL = 2
    SET_FRAME_DURATION = 3
    GET_FRAME_DURATION = 4
    GET_SUPPLY_VOLTAGE = 5
    SET_CLOCK_FREQUENCY = 7
    GET_CLOCK_FREQUENCY = 8
    SET_CHIP_TYPE = 9
    GET_CHIP_TYPE = 10
    SET_CHANNEL_MAPPING = 11
    GET_CHANNEL_MAPPING = 12
    SET_FRAME_STARTED_CALLBACK_CONFIGURATION = 13
    GET_FRAME_STARTED_CALLBACK_CONFIGURATION = 14
    START_FRAME = 15
    TRUNCATE_FRAME = 16
    SET_AUTO_TRUNCATE = 17
    GET_AUTO_TRUNCATE = 18


@unique
class ChipType(Enum):
    """
    The chip type options
    """

    WS2801 = 2801
    WS2811 = 2811
    WS2812 = 2812
    LPD8806 = 8806
    APA102 = 102


@unique
class ChannelMapping(Enum):
    """
    The channel mapping options
    """

    RGB = 6
    RBG = 9
    BRG = 33
    BGR = 36
    GRB = 18
    GBR = 24
    RGBW = 27
    RGWB = 30
    RBGW = 39
    RBWG = 45
    RWGB = 54
    RWBG = 57
    GRWB = 78
    GRBW = 75
    GBWR = 108
    GBRW = 99
    GWBR = 120
    GWRB = 114
    BRGW = 135
    BRWG = 141
    BGRW = 147
    BGWR = 156
    BWRG = 177
    BWGR = 180
    WRBG = 201
    WRGB = 198
    WGBR = 216
    WGRB = 210
    WBGR = 228
    WBRG = 225


class GetLEDValues(NamedTuple):
    value_length: int
    value_chunk_offset: int
    value_chunk_data: tuple[int, ...]


HERTZ = LinearQuantity(1)  # raw: 1/1 Hertz, returned in Hz
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletLEDStripV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Controls up to 2048 RGB(W) LEDs
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_LED_STRIP_V2
    DEVICE_DISPLAY_NAME = "LED Strip Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ChipType: TypeAlias = ChipType
    ChannelMapping: TypeAlias = ChannelMapping

    CALLBACK_FORMATS = {
        CallbackID.FRAME_STARTED: "H",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.FRAME_STARTED,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 2)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()

    async def set_led_values_low_level(
        self,
        index: int,
        value_length: int,
        value_chunk_offset: int,
        value_chunk_data: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Sets the RGB(W) values for the LEDs starting from *index*.
        You can set at most 2048 RGB values or 1536 RGBW values (6144 byte each).

        To make the colors show correctly you need to configure the chip type
        (see :func:`set_chip_type`) and a channel mapping (see :func:`set_channel_mapping`)
        according to the connected LEDs.

        If the channel mapping has 3 colors, you need to give the data in the sequence
        RGBRGBRGB... if the channel mapping has 4 colors you need to give data in the
        sequence RGBWRGBWRGBW...

        The data is double buffered and the colors will be transfered to the
        LEDs when the next frame duration ends (see :func:`set_frame_duration`).

        Generic approach:

        * Set the frame duration to a value that represents the number of frames per
          second you want to achieve.
        * Set all of the LED colors for one frame.
        * Wait for the :attr:`CallbackID.FRAME_STARTED` callback.
        * Set all of the LED colors for next frame.
        * Wait for the :attr:`CallbackID.FRAME_STARTED` callback.
        * And so on.

        This approach ensures that you can change the LED colors with a fixed frame rate.
        """
        index = int(index)
        check_range("index", index, 0, 6144)
        value_length = int(value_length)
        check_range("value_length", value_length, 0, 6144)
        value_chunk_offset = int(value_chunk_offset)
        check_range("value_chunk_offset", value_chunk_offset, 0, 65535)
        check_length("value_chunk_data", value_chunk_data, 58)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_LED_VALUES_LOW_LEVEL,
            data=pack_payload((index, value_length, value_chunk_offset, list(map(int, value_chunk_data))), "H H H 58B"),
            response_expected=response_expected,
        )

    async def set_led_values(self, index: int, value: bytes | Sequence[int]) -> None:
        """
        Sets the RGB(W) values for the LEDs starting from *index*.
        You can set at most 2048 RGB values or 1536 RGBW values (6144 byte each).

        To make the colors show correctly you need to configure the chip type
        (see :func:`set_chip_type`) and a channel mapping (see :func:`set_channel_mapping`)
        according to the connected LEDs.

        If the channel mapping has 3 colors, you need to give the data in the sequence
        RGBRGBRGB... if the channel mapping has 4 colors you need to give data in the
        sequence RGBWRGBWRGBW...

        The data is double buffered and the colors will be transfered to the
        LEDs when the next frame duration ends (see :func:`set_frame_duration`).

        Generic approach:

        * Set the frame duration to a value that represents the number of frames per
          second you want to achieve.
        * Set all of the LED colors for one frame.
        * Wait for the :attr:`CallbackID.FRAME_STARTED` callback.
        * Set all of the LED colors for next frame.
        * Wait for the :attr:`CallbackID.FRAME_STARTED` callback.
        * And so on.

        This approach ensures that you can change the LED colors with a fixed frame rate.

        This function transfers the complete value stream and calls :func:`set_led_values_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.set_led_values_low_level(index, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk, [int(item) for item in value], name="value", chunk_size=58, padding=0, max_length=65535
            )

    async def get_led_values_low_level(self, index: int, length: int) -> GetLEDValues:
        """
        Returns *length* RGB(W) values starting from the
        given *index*.

        If the channel mapping has 3 colors, you will get the data in the sequence
        RGBRGBRGB... if the channel mapping has 4 colors you will get the data in the
        sequence RGBWRGBWRGBW...
        (assuming you start at an index divisible by 3 (RGB) or 4 (RGBW)).
        """
        index = int(index)
        check_range("index", index, 0, 6144)
        length = int(length)
        check_range("length", length, 0, 6144)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_LED_VALUES_LOW_LEVEL,
            data=pack_payload((index, length), "H H"),
            response_expected=True,
        )
        value_length, value_chunk_offset, value_chunk_data = unpack_payload(payload, "H H 60B")
        return GetLEDValues(value_length, value_chunk_offset, tuple(value_chunk_data))

    async def get_led_values(self, index: int, length: int) -> bytes:
        """
        Returns *length* RGB(W) values starting from the
        given *index*.

        If the channel mapping has 3 colors, you will get the data in the sequence
        RGBRGBRGB... if the channel mapping has 4 colors you will get the data in the
        sequence RGBWRGBWRGBW...
        (assuming you start at an index divisible by 3 (RGB) or 4 (RGBW)).

        This function transfers the complete value stream and calls :func:`get_led_values_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.get_led_values_low_level(index, length)
            return Chunk(result.value_length, result.value_chunk_offset, result.value_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="value", chunk_size=60)
        return bytes(data)

    async def set_frame_duration(self, duration: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the frame duration.

        Example: If you want to achieve 20 frames per second, you should
        set the frame duration to 50ms (50ms * 20 = 1 second).

        For an explanation of the general approach see :func:`set_led_values`.

        A frame duration of 0ms will disable automatic frame transfer. In this case,
        :func:`start_frame` must be called to start a transfer.

        Default value: 100ms (10 frames per second).

        Units: duration in s.
        """
        duration_raw = seconds_to_ms(duration)
        check_range("duration", duration_raw, 0, 65535, duration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_DURATION,
            data=pack_payload((duration_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_frame_duration(self) -> Decimal:
        """
        Returns the frame duration as set by :func:`set_frame_duration`.

        Units: duration in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_DURATION, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "H"))

    async def get_supply_voltage(self) -> Decimal:
        """
        Returns the current supply voltage of the LEDs.

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SUPPLY_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def set_clock_frequency(self, frequency: float | Decimal = 1666666, response_expected: bool = True) -> None:
        """
        Sets the frequency of the clock.

        The Bricklet will choose the nearest achievable frequency, which may
        be off by a few Hz. You can get the exact frequency that is used by
        calling :func:`get_clock_frequency`.

        If you have problems with flickering LEDs, they may be bits flipping. You
        can fix this by either making the connection between the LEDs and the
        Bricklet shorter or by reducing the frequency.

        With a decreasing frequency your maximum frames per second will decrease
        too.

        Units: frequency in Hz (10000 to 2000000 Hz).
        """
        frequency_raw = HERTZ.from_si(frequency)
        check_range("frequency", frequency_raw, 10000, 2000000, frequency)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CLOCK_FREQUENCY,
            data=pack_payload((frequency_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_clock_frequency(self) -> Decimal:
        """
        Returns the currently used clock frequency as set by :func:`set_clock_frequency`.

        Units: frequency in Hz (10000 to 2000000 Hz).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CLOCK_FREQUENCY, response_expected=True
        )
        return HERTZ.to_si(unpack_payload(payload, "I"))

    async def set_chip_type(self, chip: ChipType | int = ChipType.WS2801, response_expected: bool = True) -> None:
        """
        Sets the type of the LED driver chip. We currently support the chips

        * WS2801,
        * WS2811,
        * WS2812 / SK6812 / NeoPixel RGB,
        * SK6812RGBW / NeoPixel RGBW (Chip Type = WS2812),
        * WS2813 / WS2815 (Chip Type = WS2812)
        * LPD8806 and
        * APA102 / DotStar.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIP_TYPE,
            data=pack_payload((ChipType(chip).value,), "H"),
            response_expected=response_expected,
        )

    async def get_chip_type(self) -> ChipType:
        """
        Returns the currently used chip type as set by :func:`set_chip_type`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIP_TYPE, response_expected=True
        )
        return ChipType(unpack_payload(payload, "H"))

    async def set_channel_mapping(
        self, mapping: ChannelMapping | int = ChannelMapping.BGR, response_expected: bool = True
    ) -> None:
        """
        Sets the channel mapping for the connected LEDs.

        If the mapping has 4 colors, the function :func:`set_led_values` expects 4
        values per pixel and if the mapping has 3 colors it expects 3 values per pixel.

        The function always expects the order RGB(W). The connected LED driver chips
        might have their 3 or 4 channels in a different order. For example, the WS2801
        chips typically use BGR order, then WS2812 chips typically use GRB order and
        the APA102 chips typically use WBGR order.

        The APA102 chips are special. They have three 8-bit channels for RGB
        and an additional 5-bit channel for the overall brightness of the RGB LED
        making them 4-channel chips. Internally the brightness channel is the first
        channel, therefore one of the Wxyz channel mappings should be used. Then
        the W channel controls the brightness.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_MAPPING,
            data=pack_payload((ChannelMapping(mapping).value,), "B"),
            response_expected=response_expected,
        )

    async def get_channel_mapping(self) -> ChannelMapping:
        """
        Returns the currently used channel mapping as set by :func:`set_channel_mapping`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHANNEL_MAPPING, response_expected=True
        )
        return ChannelMapping(unpack_payload(payload, "B"))

    async def set_frame_started_callback_configuration(
        self, enable: bool = True, response_expected: bool = True
    ) -> None:
        """
        Enables/disables the :attr:`CallbackID.FRAME_STARTED` callback.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_STARTED_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enable),), "!"),
            response_expected=response_expected,
        )

    async def get_frame_started_callback_configuration(self) -> bool:
        """
        Returns the configuration as set by
        :func:`set_frame_started_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_STARTED_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def start_frame(self, response_expected: bool = True) -> None:
        """
        Start transferring the current frame, irrespective of the configured frame
        duration.

        This function can be used to update the LEDs with a variable frame rate.
        The automatic transfer of frames should be disabled by setting the frame
        duration to zero.

        .. versionadded:: 2.2.0 (Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.START_FRAME, response_expected=response_expected
        )

    async def truncate_frame(self, length: int, response_expected: bool = True) -> None:
        """
        Truncates the length of the frame stored on the bricklet to the specified
        value.

        Normally, the maximum amount of previously set LED values is transferred for
        every frame. For example, if values for 256 LEDs have been set, every frame
        update will transfer the data for all 256 LEDs, regardless of how many LED
        values had actually changed. By truncating the frame, the amount of transferred
        LED values can be reduced again. This can be used to quickly update the
        beginning of an LED strip and is usually only useful with a dynamic frame rate.

        Truncating to a length of zero will stop automatic frame updates until any LED
        value is set again.

        .. versionadded:: 2.3.0 (Firmware)
        """
        length = int(length)
        check_range("length", length, 0, 6144)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.TRUNCATE_FRAME,
            data=pack_payload((length,), "H"),
            response_expected=response_expected,
        )

    async def set_auto_truncate(self, length: int = 6144, response_expected: bool = True) -> None:
        """
        Automatically truncates the frame after it was sent.
        See :func:`truncate_frame`.

        .. versionadded:: 2.3.0 (Firmware)
        """
        length = int(length)
        check_range("length", length, 0, 6144)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AUTO_TRUNCATE,
            data=pack_payload((length,), "H"),
            response_expected=response_expected,
        )

    async def get_auto_truncate(self) -> int:
        """
        Returns length to which the frame will automatically be truncated, as set by
        :func:`set_auto_truncate`.

        .. versionadded:: 2.3.0 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AUTO_TRUNCATE, response_expected=True
        )
        return unpack_payload(payload, "H")

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, value
