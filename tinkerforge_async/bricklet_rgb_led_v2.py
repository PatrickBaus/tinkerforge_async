"""
Module for the Tinkerforge RGB LED Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDV2_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, DeviceIdentifier, _FunctionID
from .helper import check_range
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

    SET_RGB_VALUE = 1
    GET_RGB_VALUE = 2


class GetRGBValue(NamedTuple):
    r: int
    g: int
    b: int


class BrickletRGBLEDV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Controls one RGB LED
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_RGB_LED_V2
    DEVICE_DISPLAY_NAME = "RGB LED Bricklet 2.0"

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

    async def set_rgb_value(self, r: int, g: int, b: int, response_expected: bool = True) -> None:
        """
        Sets the *r*, *g* and *b* values for the LED.
        """
        r = int(r)
        check_range("r", r, 0, 255)
        g = int(g)
        check_range("g", g, 0, 255)
        b = int(b)
        check_range("b", b, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RGB_VALUE,
            data=pack_payload((r, g, b), "B B B"),
            response_expected=response_expected,
        )

    async def get_rgb_value(self) -> GetRGBValue:
        """
        Returns the *r*, *g* and *b* values of the LED as set by :func:`set_rgb_value`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RGB_VALUE, response_expected=True
        )
        r, g, b = unpack_payload(payload, "B B B")
        return GetRGBValue(r, g, b)
