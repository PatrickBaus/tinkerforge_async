"""
Module for the Tinkerforge Dual Button Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DualButton_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    STATE_CHANGED = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_LED_STATE = 1
    GET_LED_STATE = 2
    GET_BUTTON_STATE = 3
    SET_SELECTED_LED_STATE = 5


@unique
class LEDState(Enum):
    """
    The led state options
    """

    AUTO_TOGGLE_ON = 0
    AUTO_TOGGLE_OFF = 1
    ON = 2
    OFF = 3


@unique
class ButtonState(Enum):
    """
    The button state options
    """

    PRESSED = 0
    RELEASED = 1


@unique
class LED(Enum):
    """
    The led options
    """

    LEFT = 0
    RIGHT = 1


class GetLEDState(NamedTuple):
    led_l: LEDState
    led_r: LEDState


class GetButtonState(NamedTuple):
    button_l: ButtonState
    button_r: ButtonState


class StateChangedEvent(NamedTuple):
    button_l: ButtonState
    button_r: ButtonState
    led_l: LEDState
    led_r: LEDState


class BrickletDualButton(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Two tactile buttons with built-in blue LEDs
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DUAL_BUTTON
    DEVICE_DISPLAY_NAME = "Dual Button Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    LEDState: TypeAlias = LEDState
    ButtonState: TypeAlias = ButtonState
    LED: TypeAlias = LED

    CALLBACK_FORMATS = {
        CallbackID.STATE_CHANGED: "B B B B",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.STATE_CHANGED,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_led_state(
        self,
        led_l: LEDState | int = LEDState.AUTO_TOGGLE_OFF,
        led_r: LEDState | int = LEDState.AUTO_TOGGLE_OFF,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the state of the LEDs. Possible states are:

        * 0 = AutoToggleOn: Enables auto toggle with initially enabled LED.
        * 1 = AutoToggleOff: Activates auto toggle with initially disabled LED.
        * 2 = On: Enables LED (auto toggle is disabled).
        * 3 = Off: Disables LED (auto toggle is disabled).

        In auto toggle mode the LED is toggled automatically at each press of a button.

        If you just want to set one of the LEDs and don't know the current state
        of the other LED, you can get the state with :func:`get_led_state` or you
        can use :func:`set_selected_led_state`.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_LED_STATE,
            data=pack_payload((LEDState(led_l).value, LEDState(led_r).value), "B B"),
            response_expected=response_expected,
        )

    async def get_led_state(self) -> GetLEDState:
        """
        Returns the current state of the LEDs, as set by :func:`set_led_state`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_LED_STATE, response_expected=True
        )
        led_l, led_r = unpack_payload(payload, "B B")
        return GetLEDState(LEDState(led_l), LEDState(led_r))

    async def get_button_state(self) -> GetButtonState:
        """
        Returns the current state for both buttons. Possible states are:

        * 0 = pressed
        * 1 = released
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BUTTON_STATE, response_expected=True
        )
        button_l, button_r = unpack_payload(payload, "B B")
        return GetButtonState(ButtonState(button_l), ButtonState(button_r))

    async def set_selected_led_state(
        self, led: LED | int, state: LEDState | int, response_expected: bool = True
    ) -> None:
        """
        Sets the state of the selected LED (0 or 1).

        The other LED remains untouched.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_LED_STATE,
            data=pack_payload((LED(led).value, LEDState(state).value), "B B"),
            response_expected=response_expected,
        )

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        button_l, button_r, led_l, led_r = value
        return 0, StateChangedEvent(ButtonState(button_l), ButtonState(button_r), LEDState(led_l), LEDState(led_r))
