"""
Module for the Tinkerforge RGB LED Button Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDButton_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .helper import check_range
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    BUTTON_STATE_CHANGED = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_COLOR = 1
    GET_COLOR = 2
    GET_BUTTON_STATE = 3
    SET_COLOR_CALIBRATION = 5
    GET_COLOR_CALIBRATION = 6


@unique
class ButtonState(Enum):
    """
    The button state options
    """

    PRESSED = 0
    RELEASED = 1


class GetColor(NamedTuple):
    red: int
    green: int
    blue: int


class GetColorCalibration(NamedTuple):
    red: Decimal
    green: Decimal
    blue: Decimal


PERCENT = LinearQuantity(1)  # raw: 1/1 Percent, returned in %


class BrickletRGBLEDButton(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Push button with built-in RGB LED
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_RGB_LED_BUTTON
    DEVICE_DISPLAY_NAME = "RGB LED Button Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ButtonState: TypeAlias = ButtonState

    CALLBACK_FORMATS = {
        CallbackID.BUTTON_STATE_CHANGED: "B",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.BUTTON_STATE_CHANGED,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_color(self, red: int = 0, green: int = 0, blue: int = 0, response_expected: bool = True) -> None:
        """
        Sets the color of the LED.
        """
        red = int(red)
        check_range("red", red, 0, 255)
        green = int(green)
        check_range("green", green, 0, 255)
        blue = int(blue)
        check_range("blue", blue, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COLOR,
            data=pack_payload((red, green, blue), "B B B"),
            response_expected=response_expected,
        )

    async def get_color(self) -> GetColor:
        """
        Returns the LED color as set by :func:`set_color`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR, response_expected=True
        )
        red, green, blue = unpack_payload(payload, "B B B")
        return GetColor(red, green, blue)

    async def get_button_state(self) -> ButtonState:
        """
        Returns the current state of the button (either pressed or released).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BUTTON_STATE, response_expected=True
        )
        return ButtonState(unpack_payload(payload, "B"))

    async def set_color_calibration(
        self,
        red: float | Decimal = 100,
        green: float | Decimal = 100,
        blue: float | Decimal = 55,
        response_expected: bool = True,
    ) -> None:
        """
        Sets a color calibration. Some colors appear brighter then others,
        so a calibration may be necessary for uniform colors.

        The calibration is saved in flash. You don't need to call this
        function on every startup.

        Units: red in % (0 to 100 %), green in % (0 to 100 %), blue in % (0 to 100 %).
        """
        red_raw = PERCENT.from_si(red)
        check_range("red", red_raw, 0, 100, red)
        green_raw = PERCENT.from_si(green)
        check_range("green", green_raw, 0, 100, green)
        blue_raw = PERCENT.from_si(blue)
        check_range("blue", blue_raw, 0, 100, blue)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COLOR_CALIBRATION,
            data=pack_payload((red_raw, green_raw, blue_raw), "B B B"),
            response_expected=response_expected,
        )

    async def get_color_calibration(self) -> GetColorCalibration:
        """
        Returns the color calibration as set by :func:`set_color_calibration`.

        Units: red in % (0 to 100 %), green in % (0 to 100 %), blue in % (0 to 100 %).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR_CALIBRATION, response_expected=True
        )
        red, green, blue = unpack_payload(payload, "B B B")
        return GetColorCalibration(PERCENT.to_si(red), PERCENT.to_si(green), PERCENT.to_si(blue))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, ButtonState(value)
