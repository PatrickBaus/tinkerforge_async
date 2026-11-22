"""
Module for the Tinkerforge OLED 64x48 Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/OLED64x48_Bricklet_Python.html) implemented using
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
from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple, TypeAlias

from .devices import Device, DeviceIdentifier, _FunctionID
from .helper import check_length, check_range, encode_string
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    WRITE = 1
    NEW_WINDOW = 2
    CLEAR_DISPLAY = 3
    SET_DISPLAY_CONFIGURATION = 4
    GET_DISPLAY_CONFIGURATION = 5
    WRITE_LINE = 6


class GetDisplayConfiguration(NamedTuple):
    contrast: int
    invert: bool


class BrickletOLED64x48(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    0.0168 m (0.66") OLED display with 64x48 pixels
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_OLED_64X48
    DEVICE_DISPLAY_NAME = "OLED 64x48 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {}

    SID_TO_CALLBACK = {}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def write(self, data: bytes | Sequence[int], response_expected: bool = True) -> None:
        """
        Appends 64 byte of data to the window as set by :func:`new_window`.

        Each row has a height of 8 pixels which corresponds to one byte of data.

        Example: if you call :func:`new_window` with column from 0 to 63 and row
        from 0 to 5 (the whole display) each call of :func:`write` (red arrow) will
        write one row.

        .. image:: /Images/Bricklets/bricklet_oled_64x48_display.png
           :scale: 100 %
           :alt: Display pixel order
           :align: center
           :target: ../../_images/Bricklets/bricklet_oled_64x48_display.png

        The LSB (D0) of each data byte is at the top and the MSB (D7) is at the
        bottom of the row.

        The next call of :func:`write` will write the second row and so on. To
        fill the whole display you need to call :func:`write` 6 times.
        """
        check_length("data", data, 64)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE,
            data=pack_payload((list(map(int, data)),), "64B"),
            response_expected=response_expected,
        )

    async def new_window(
        self, column_from: int, column_to: int, row_from: int, row_to: int, response_expected: bool = True
    ) -> None:
        """
        Sets the window in which you can write with :func:`write`. One row
        has a height of 8 pixels.
        """
        column_from = int(column_from)
        check_range("column_from", column_from, 0, 63)
        column_to = int(column_to)
        check_range("column_to", column_to, 0, 63)
        row_from = int(row_from)
        check_range("row_from", row_from, 0, 5)
        row_to = int(row_to)
        check_range("row_to", row_to, 0, 5)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.NEW_WINDOW,
            data=pack_payload((column_from, column_to, row_from, row_to), "B B B B"),
            response_expected=response_expected,
        )

    async def clear_display(self, response_expected: bool = True) -> None:
        """
        Clears the current content of the window as set by :func:`new_window`.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.CLEAR_DISPLAY, response_expected=response_expected
        )

    async def set_display_configuration(
        self, contrast: int = 143, invert: bool = False, response_expected: bool = True
    ) -> None:
        """
        Sets the configuration of the display.

        You can set a contrast value from 0 to 255 and you can invert the color
        (black/white) of the display.
        """
        contrast = int(contrast)
        check_range("contrast", contrast, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISPLAY_CONFIGURATION,
            data=pack_payload((contrast, bool(invert)), "B !"),
            response_expected=response_expected,
        )

    async def get_display_configuration(self) -> GetDisplayConfiguration:
        """
        Returns the configuration as set by :func:`set_display_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISPLAY_CONFIGURATION, response_expected=True
        )
        contrast, invert = unpack_payload(payload, "B !")
        return GetDisplayConfiguration(contrast, invert)

    async def write_line(self, line: int, position: int, text: str, response_expected: bool = True) -> None:
        """
        Writes text to a specific line with a specific position.
        The text can have a maximum of 13 characters.

        For example: (1, 4, "Hello") will write *Hello* in the middle of the
        second line of the display.

        You can draw to the display with :func:`write` and then add text to it
        afterwards.

        The display uses a special 5x7 pixel charset. You can view the characters
        of the charset in Brick Viewer.

        The font conforms to code page 437.
        """
        line = int(line)
        check_range("line", line, 0, 5)
        position = int(position)
        check_range("position", position, 0, 12)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_LINE,
            data=pack_payload((line, position, encode_string("text", text, 13)), "B B 13s"),
            response_expected=response_expected,
        )
