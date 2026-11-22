"""Tests for the Dual Button Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_dual_button_v2 import (
    BrickletDualButtonV2,
    GetButtonState,
    GetLEDState,
    StateChangedEvent,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletDualButtonV2
FunctionID = BrickletDualButtonV2.FunctionID
CallbackID = BrickletDualButtonV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_LED_STATE": 1,
    "GET_LED_STATE": 2,
    "GET_BUTTON_STATE": 3,
    "SET_SELECTED_LED_STATE": 5,
    "SET_STATE_CHANGED_CALLBACK_CONFIGURATION": 6,
    "GET_STATE_CHANGED_CALLBACK_CONFIGURATION": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"STATE_CHANGED": 4}

CALLS: list[Call] = [
    Call("set_led_state", FunctionID.SET_LED_STATE, (DEVICE.LEDState.OFF, DEVICE.LEDState.OFF), sent=("B B", (3, 3))),
    Call(
        "set_led_state",
        FunctionID.SET_LED_STATE,
        (DEVICE.LEDState.OFF, DEVICE.LEDState.OFF, False),
        sent=("B B", (3, 3)),
        response_expected=False,
    ),
    Call(
        "get_led_state",
        FunctionID.GET_LED_STATE,
        (),
        reply=("B B", (3, 3)),
        result=GetLEDState(DEVICE.LEDState.OFF, DEVICE.LEDState.OFF),
    ),
    Call(
        "get_button_state",
        FunctionID.GET_BUTTON_STATE,
        (),
        reply=("B B", (1, 1)),
        result=GetButtonState(DEVICE.ButtonState.RELEASED, DEVICE.ButtonState.RELEASED),
    ),
    Call(
        "set_selected_led_state",
        FunctionID.SET_SELECTED_LED_STATE,
        (DEVICE.LED.RIGHT, DEVICE.LEDState.OFF),
        sent=("B B", (1, 3)),
    ),
    Call(
        "set_selected_led_state",
        FunctionID.SET_SELECTED_LED_STATE,
        (DEVICE.LED.RIGHT, DEVICE.LEDState.OFF, False),
        sent=("B B", (1, 3)),
        response_expected=False,
    ),
    Call(
        "set_state_changed_callback_configuration",
        FunctionID.SET_STATE_CHANGED_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_state_changed_callback_configuration",
        FunctionID.SET_STATE_CHANGED_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_state_changed_callback_configuration",
        FunctionID.GET_STATE_CHANGED_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_led_state", (12345, DEVICE.LEDState.OFF)),
    ("set_led_state", (DEVICE.LEDState.OFF, 12345)),
    ("set_selected_led_state", (12345, DEVICE.LEDState.OFF)),
    ("set_selected_led_state", (DEVICE.LED.RIGHT, 12345)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2119
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Dual Button Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_state_changed(device, connection):
    """The callback STATE_CHANGED is converted to an event."""
    connection.callback(CallbackID.STATE_CHANGED, "B B B B", *(1, 1, 3, 3))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.STATE_CHANGED,
            StateChangedEvent(
                DEVICE.ButtonState.RELEASED, DEVICE.ButtonState.RELEASED, DEVICE.LEDState.OFF, DEVICE.LEDState.OFF
            ),
        )
    ]
