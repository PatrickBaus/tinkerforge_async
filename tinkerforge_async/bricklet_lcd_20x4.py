"""
Module for the Tinkerforge LCD 20x4 Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/LCD20x4_Bricklet_Python.html) implemented using
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

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    BUTTON_PRESSED = 9
    BUTTON_RELEASED = 10


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    WRITE_LINE = 1
    CLEAR_DISPLAY = 2
    BACKLIGHT_ON = 3
    BACKLIGHT_OFF = 4
    IS_BACKLIGHT_ON = 5
    SET_CONFIG = 6
    GET_CONFIG = 7
    IS_BUTTON_PRESSED = 8
    SET_CUSTOM_CHARACTER = 11
    GET_CUSTOM_CHARACTER = 12
    SET_DEFAULT_TEXT = 13
    GET_DEFAULT_TEXT = 14
    SET_DEFAULT_TEXT_COUNTER = 15
    GET_DEFAULT_TEXT_COUNTER = 16


class GetConfig(NamedTuple):
    cursor: bool
    blinking: bool


class BrickletLCD20x4(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    20x4 character alphanumeric display with blue backlight
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_LCD_20X4
    DEVICE_DISPLAY_NAME = "LCD 20x4 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.BUTTON_PRESSED: "B",
        CallbackID.BUTTON_RELEASED: "B",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.BUTTON_PRESSED,)),
        Channel(1, callbacks=(CallbackID.BUTTON_RELEASED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 2)

    async def write_line(self, line: int, position: int, text: str, response_expected: bool = True) -> None:
        """
        Writes text to a specific line with a specific position.
        The text can have a maximum of 20 characters.

        For example: (0, 7, "Hello") will write *Hello* in the middle of the
        first line of the display.

        The display uses a special charset that includes all ASCII characters except
        backslash and tilde. The LCD charset also includes several other non-ASCII characters, see
        the `charset specification
        <https://github.com/Tinkerforge/lcd-20x4-bricklet/raw/master/datasheets/standard_charset.pdf>`__
        for details. The Unicode example above shows how to specify non-ASCII characters
        and how to translate from Unicode to the LCD charset.
        """
        line = int(line)
        check_range("line", line, 0, 3)
        position = int(position)
        check_range("position", position, 0, 19)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_LINE,
            data=pack_payload((line, position, str(text).encode("latin-1")), "B B 20s"),
            response_expected=response_expected,
        )

    async def clear_display(self, response_expected: bool = True) -> None:
        """
        Deletes all characters from the display.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.CLEAR_DISPLAY, response_expected=response_expected
        )

    async def backlight_on(self, response_expected: bool = True) -> None:
        """
        Turns the backlight on.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.BACKLIGHT_ON, response_expected=response_expected
        )

    async def backlight_off(self, response_expected: bool = True) -> None:
        """
        Turns the backlight off.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.BACKLIGHT_OFF, response_expected=response_expected
        )

    async def is_backlight_on(self) -> bool:
        """
        Returns *true* if the backlight is on and *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_BACKLIGHT_ON, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_config(self, cursor: bool = False, blinking: bool = False, response_expected: bool = True) -> None:
        """
        Configures if the cursor (shown as "_") should be visible and if it
        should be blinking (shown as a blinking block). The cursor position
        is one character behind the the last text written with
        :func:`write_line`.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIG,
            data=pack_payload((bool(cursor), bool(blinking)), "! !"),
            response_expected=response_expected,
        )

    async def get_config(self) -> GetConfig:
        """
        Returns the configuration as set by :func:`set_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIG, response_expected=True
        )
        cursor, blinking = unpack_payload(payload, "! !")
        return GetConfig(cursor, blinking)

    async def is_button_pressed(self, button: int) -> bool:
        """
        Returns *true* if the button (0 to 2 or 0 to 3 since hardware version 1.2)
        is pressed.

        If you want to react on button presses and releases it is recommended to use
        the :attr:`CallbackID.BUTTON_PRESSED` and :attr:`CallbackID.BUTTON_RELEASED` callbacks.
        """
        button = int(button)
        check_range("button", button, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.IS_BUTTON_PRESSED,
            data=pack_payload((button,), "B"),
            response_expected=True,
        )
        return unpack_payload(payload, "!")

    async def set_custom_character(
        self, index: int, character: bytes | Sequence[int], response_expected: bool = True
    ) -> None:
        r"""
        The LCD 20x4 Bricklet can store up to 8 custom characters. The characters
        consist of 5x8 pixels and can be addressed with the index 0-7. To describe
        the pixels, the first 5 bits of 8 bytes are used. For example, to make
        a custom character "H", you should transfer the following:

        * ``character[0] = 0b00010001`` (decimal value 17)
        * ``character[1] = 0b00010001`` (decimal value 17)
        * ``character[2] = 0b00010001`` (decimal value 17)
        * ``character[3] = 0b00011111`` (decimal value 31)
        * ``character[4] = 0b00010001`` (decimal value 17)
        * ``character[5] = 0b00010001`` (decimal value 17)
        * ``character[6] = 0b00010001`` (decimal value 17)
        * ``character[7] = 0b00000000`` (decimal value 0)

        The characters can later be written with :func:`write_line` by using the
        characters with the byte representation 8 ("\\x08" or "\\u0008") to 15
        ("\\x0F" or "\\u000F").

        You can play around with the custom characters in Brick Viewer version
        since 2.0.1.

        Custom characters are stored by the LCD in RAM, so they have to be set
        after each startup.

        .. versionadded:: 2.0.1 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 7)
        check_length("character", character, 8)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CUSTOM_CHARACTER,
            data=pack_payload((index, list(map(int, character))), "B 8B"),
            response_expected=response_expected,
        )

    async def get_custom_character(self, index: int) -> tuple[int, ...]:
        """
        Returns the custom character for a given index, as set with
        :func:`set_custom_character`.

        .. versionadded:: 2.0.1 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 7)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CUSTOM_CHARACTER,
            data=pack_payload((index,), "B"),
            response_expected=True,
        )
        return tuple(unpack_payload(payload, "8B"))

    async def set_default_text(self, line: int, text: str, response_expected: bool = True) -> None:
        """
        Sets the default text for lines 0-3. The max number of characters
        per line is 20.

        The default text is shown on the LCD, if the default text counter
        expires, see :func:`set_default_text_counter`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        line = int(line)
        check_range("line", line, 0, 3)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEFAULT_TEXT,
            data=pack_payload((line, str(text).encode("latin-1")), "B 20s"),
            response_expected=response_expected,
        )

    async def get_default_text(self, line: int) -> str:
        """
        Returns the default text for a given line (0-3) as set by
        :func:`set_default_text`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        line = int(line)
        check_range("line", line, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_DEFAULT_TEXT,
            data=pack_payload((line,), "B"),
            response_expected=True,
        )
        return unpack_payload(payload, "20s")

    async def set_default_text_counter(
        self, counter: Duration = Decimal("-0.001"), response_expected: bool = True
    ) -> None:
        """
        Sets the default text counter. This counter is decremented each
        ms by the LCD firmware. If the counter reaches 0, the default text
        (see :func:`set_default_text`) is shown on the LCD.

        This functionality can be used to show a default text if the controlling
        program crashes or the connection is interrupted.

        A possible approach is to call :func:`set_default_text_counter` every
        minute with the parameter 1000*60*2 (2 minutes). In this case the
        default text will be shown no later than 2 minutes after the
        controlling program crashes.

        A negative counter turns the default text functionality off.

        Units: counter in s.

        .. versionadded:: 2.0.2 (Firmware)
        """
        counter_raw = seconds_to_ms(counter)
        check_range("counter", counter_raw, -2147483648, 2147483647, counter)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEFAULT_TEXT_COUNTER,
            data=pack_payload((counter_raw,), "i"),
            response_expected=response_expected,
        )

    async def get_default_text_counter(self) -> Decimal:
        """
        Returns the current value of the default text counter.

        Units: counter in s.

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEFAULT_TEXT_COUNTER, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "i"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.BUTTON_PRESSED:
            return 0, value
        return 1, value
