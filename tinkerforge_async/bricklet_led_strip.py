"""
Module for the Tinkerforge LED Strip Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/LEDStrip_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    FRAME_RENDERED = 6


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_RGB_VALUES = 1
    GET_RGB_VALUES = 2
    SET_FRAME_DURATION = 3
    GET_FRAME_DURATION = 4
    GET_SUPPLY_VOLTAGE = 5
    SET_CLOCK_FREQUENCY = 7
    GET_CLOCK_FREQUENCY = 8
    SET_CHIP_TYPE = 9
    GET_CHIP_TYPE = 10
    SET_RGBW_VALUES = 11
    GET_RGBW_VALUES = 12
    SET_CHANNEL_MAPPING = 13
    GET_CHANNEL_MAPPING = 14
    ENABLE_FRAME_RENDERED_CALLBACK = 15
    DISABLE_FRAME_RENDERED_CALLBACK = 16
    IS_FRAME_RENDERED_CALLBACK_ENABLED = 17


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


class GetRGBValues(NamedTuple):
    r: tuple[int, ...]
    g: tuple[int, ...]
    b: tuple[int, ...]


class GetRGBWValues(NamedTuple):
    r: tuple[int, ...]
    g: tuple[int, ...]
    b: tuple[int, ...]
    w: tuple[int, ...]


HERTZ = LinearQuantity(1)  # raw: 1/1 Hertz, returned in Hz
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletLEDStrip(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Controls up to 320 RGB LEDs
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_LED_STRIP
    DEVICE_DISPLAY_NAME = "LED Strip Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ChipType: TypeAlias = ChipType
    ChannelMapping: TypeAlias = ChannelMapping

    CALLBACK_FORMATS = {
        CallbackID.FRAME_RENDERED: "H",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.FRAME_RENDERED,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 3)

    async def set_rgb_values(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        index: int,
        length: int,
        r: bytes | Sequence[int],
        g: bytes | Sequence[int],
        b: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Sets *length* RGB values for the LEDs starting from *index*.

        To make the colors show correctly you need to configure the chip type
        (:func:`set_chip_type`) and a 3-channel channel mapping (:func:`set_channel_mapping`)
        according to the connected LEDs.

        Example: If you set

        * index to 5,
        * length to 3,
        * r to |r_values|,
        * g to |g_values| and
        * b to |b_values|

        the LED with index 5 will be red, 6 will be green and 7 will be blue.

        .. note:: Depending on the LED circuitry colors can be permuted.

        The colors will be transfered to actual LEDs when the next
        frame duration ends, see :func:`set_frame_duration`.

        Generic approach:

        * Set the frame duration to a value that represents
          the number of frames per second you want to achieve.
        * Set all of the LED colors for one frame.
        * Wait for the :attr:`CallbackID.FRAME_RENDERED` callback.
        * Set all of the LED colors for next frame.
        * Wait for the :attr:`CallbackID.FRAME_RENDERED` callback.
        * and so on.

        This approach ensures that you can change the LED colors with
        a fixed frame rate.

        The actual number of controllable LEDs depends on the number of free
        Bricklet ports. See ``here <led_strip_bricklet_ram_constraints>`` for more
        information. A call of :func:`set_rgb_values` with index + length above the
        bounds is ignored completely.
        """
        index = int(index)
        check_range("index", index, 0, 319)
        length = int(length)
        check_range("length", length, 0, 16)
        check_length("r", r, 16)
        check_length("g", g, 16)
        check_length("b", b, 16)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RGB_VALUES,
            data=pack_payload(
                (index, length, list(map(int, r)), list(map(int, g)), list(map(int, b))), "H B 16B 16B 16B"
            ),
            response_expected=response_expected,
        )

    async def get_rgb_values(self, index: int, length: int) -> GetRGBValues:
        """
        Returns *length* R, G and B values starting from the
        given LED *index*.

        The values are the last values that were set by :func:`set_rgb_values`.
        """
        index = int(index)
        check_range("index", index, 0, 319)
        length = int(length)
        check_range("length", length, 0, 16)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RGB_VALUES,
            data=pack_payload((index, length), "H B"),
            response_expected=True,
        )
        r, g, b = unpack_payload(payload, "16B 16B 16B")
        return GetRGBValues(tuple(r), tuple(g), tuple(b))

    async def set_frame_duration(self, duration: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the frame duration.

        Example: If you want to achieve 20 frames per second, you should
        set the frame duration to 50ms (50ms * 20 = 1 second).

        For an explanation of the general approach see :func:`set_rgb_values`.

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

        .. note::
         The frequency in firmware version 2.0.0 is fixed at 2MHz.

        Units: frequency in Hz (10000 to 2000000 Hz).

        .. versionadded:: 2.0.1 (Firmware)
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

        .. versionadded:: 2.0.1 (Firmware)
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
        * LPD8806 and
        * APA102 / DotStar.

        .. versionadded:: 2.0.2 (Firmware)
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

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIP_TYPE, response_expected=True
        )
        return ChipType(unpack_payload(payload, "H"))

    async def set_rgbw_values(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        index: int,
        length: int,
        r: bytes | Sequence[int],
        g: bytes | Sequence[int],
        b: bytes | Sequence[int],
        w: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Sets *length* RGBW values for the LEDs starting from *index*.

        To make the colors show correctly you need to configure the chip type
        (:func:`set_chip_type`) and a 4-channel channel mapping (:func:`set_channel_mapping`)
        according to the connected LEDs.

        The maximum length is 12, the index goes from 0 to 239 and the rgbw values
        have 8 bits each.

        Example: If you set

        * index to 5,
        * length to 4,
        * r to |r_values|,
        * g to |g_values|,
        * b to |b_values| and
        * w to |b_values|

        the LED with index 5 will be red, 6 will be green, 7 will be blue and 8 will be white.

        .. note:: Depending on the LED circuitry colors can be permuted.

        The colors will be transfered to actual LEDs when the next
        frame duration ends, see :func:`set_frame_duration`.

        Generic approach:

        * Set the frame duration to a value that represents
          the number of frames per second you want to achieve.
        * Set all of the LED colors for one frame.
        * Wait for the :attr:`CallbackID.FRAME_RENDERED` callback.
        * Set all of the LED colors for next frame.
        * Wait for the :attr:`CallbackID.FRAME_RENDERED` callback.
        * and so on.

        This approach ensures that you can change the LED colors with
        a fixed frame rate.

        The actual number of controllable LEDs depends on the number of free
        Bricklet ports. See ``here <led_strip_bricklet_ram_constraints>`` for more
        information. A call of :func:`set_rgbw_values` with index + length above the
        bounds is ignored completely.

        The LPD8806 LED driver chips have 7-bit channels for RGB. Internally the LED
        Strip Bricklets divides the 8-bit values set using this function by 2 to make
        them 7-bit. Therefore, you can just use the normal value range (0-255) for
        LPD8806 LEDs.

        The brightness channel of the APA102 LED driver chips has 5-bit. Internally the
        LED Strip Bricklets divides the 8-bit values set using this function by 8 to make
        them 5-bit. Therefore, you can just use the normal value range (0-255) for
        the brightness channel of APA102 LEDs.

        .. versionadded:: 2.0.6 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 239)
        length = int(length)
        check_range("length", length, 0, 12)
        check_length("r", r, 12)
        check_length("g", g, 12)
        check_length("b", b, 12)
        check_length("w", w, 12)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RGBW_VALUES,
            data=pack_payload(
                (index, length, list(map(int, r)), list(map(int, g)), list(map(int, b)), list(map(int, w))),
                "H B 12B 12B 12B 12B",
            ),
            response_expected=response_expected,
        )

    async def get_rgbw_values(self, index: int, length: int) -> GetRGBWValues:
        """
        Returns *length* RGBW values starting from the given *index*.

        The values are the last values that were set by :func:`set_rgbw_values`.

        .. versionadded:: 2.0.6 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 239)
        length = int(length)
        check_range("length", length, 0, 12)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RGBW_VALUES,
            data=pack_payload((index, length), "H B"),
            response_expected=True,
        )
        r, g, b, w = unpack_payload(payload, "12B 12B 12B 12B")
        return GetRGBWValues(tuple(r), tuple(g), tuple(b), tuple(w))

    async def set_channel_mapping(
        self, mapping: ChannelMapping | int = ChannelMapping.BGR, response_expected: bool = True
    ) -> None:
        """
        Sets the channel mapping for the connected LEDs.

        :func:`set_rgb_values` and :func:`set_rgbw_values` take the data in RGB(W) order.
        But the connected LED driver chips might have their 3 or 4 channels in a
        different order. For example, the WS2801 chips typically use BGR order, the
        WS2812 chips typically use GRB order and the APA102 chips typically use WBGR
        order.

        The APA102 chips are special. They have three 8-bit channels for RGB
        and an additional 5-bit channel for the overall brightness of the RGB LED
        making them 4-channel chips. Internally the brightness channel is the first
        channel, therefore one of the Wxyz channel mappings should be used. Then
        the W channel controls the brightness.

        If a 3-channel mapping is selected then :func:`set_rgb_values` has to be used.
        Calling :func:`set_rgbw_values` with a 3-channel mapping will produce incorrect
        results. Vice-versa if a 4-channel mapping is selected then
        :func:`set_rgbw_values` has to be used. Calling :func:`set_rgb_values` with a
        4-channel mapping will produce incorrect results.

        .. versionadded:: 2.0.6 (Firmware)
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

        .. versionadded:: 2.0.6 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHANNEL_MAPPING, response_expected=True
        )
        return ChannelMapping(unpack_payload(payload, "B"))

    async def enable_frame_rendered_callback(self, response_expected: bool = True) -> None:
        """
        Enables the :attr:`CallbackID.FRAME_RENDERED` callback.

        By default the callback is enabled.

        .. versionadded:: 2.0.6 (Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_FRAME_RENDERED_CALLBACK, response_expected=response_expected
        )

    async def disable_frame_rendered_callback(self, response_expected: bool = True) -> None:
        """
        Disables the :attr:`CallbackID.FRAME_RENDERED` callback.

        By default the callback is enabled.

        .. versionadded:: 2.0.6 (Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_FRAME_RENDERED_CALLBACK, response_expected=response_expected
        )

    async def is_frame_rendered_callback_enabled(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.FRAME_RENDERED` callback is enabled, *false* otherwise.

        .. versionadded:: 2.0.6 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_FRAME_RENDERED_CALLBACK_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, value
