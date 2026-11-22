"""Tests for the RGB LED Button Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_rgb_led_button import BrickletRGBLEDButton, GetColor, GetColorCalibration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletRGBLEDButton
FunctionID = BrickletRGBLEDButton.FunctionID
CallbackID = BrickletRGBLEDButton.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_COLOR": 1,
    "GET_COLOR": 2,
    "GET_BUTTON_STATE": 3,
    "SET_COLOR_CALIBRATION": 5,
    "GET_COLOR_CALIBRATION": 6,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"BUTTON_STATE_CHANGED": 4}

CALLS: list[Call] = [
    Call("set_color", FunctionID.SET_COLOR, (3, 3, 3), sent=("B B B", (3, 3, 3))),
    Call("set_color", FunctionID.SET_COLOR, (3, 3, 3, False), sent=("B B B", (3, 3, 3)), response_expected=False),
    Call("get_color", FunctionID.GET_COLOR, (), reply=("B B B", (3, 4, 5)), result=GetColor(3, 4, 5)),
    Call("get_button_state", FunctionID.GET_BUTTON_STATE, (), reply=("B", (1,)), result=DEVICE.ButtonState.RELEASED),
    Call(
        "set_color_calibration",
        FunctionID.SET_COLOR_CALIBRATION,
        (Decimal("3"), Decimal("3"), Decimal("3")),
        sent=("B B B", (3, 3, 3)),
    ),
    Call(
        "set_color_calibration",
        FunctionID.SET_COLOR_CALIBRATION,
        (Decimal("3"), Decimal("3"), Decimal("3"), False),
        sent=("B B B", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_color_calibration",
        FunctionID.GET_COLOR_CALIBRATION,
        (),
        reply=("B B B", (3, 4, 5)),
        result=GetColorCalibration(Decimal("3"), Decimal("4"), Decimal("5")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_color", (256, 3, 3)),
    ("set_color", (3, 256, 3)),
    ("set_color", (3, 3, 256)),
    ("set_color_calibration", (Decimal("101"), Decimal("3"), Decimal("3"))),
    ("set_color_calibration", (Decimal("3"), Decimal("101"), Decimal("3"))),
    ("set_color_calibration", (Decimal("3"), Decimal("3"), Decimal("101"))),
]


def test_identity(device: BrickletRGBLEDButton) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 282
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("RGB LED Button Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_button_state_changed(device: BrickletRGBLEDButton, connection: FakeConnection) -> None:
    """The callback BUTTON_STATE_CHANGED is converted to an event."""
    connection.callback(CallbackID.BUTTON_STATE_CHANGED, "B", *(1,))
    assert summary(read_events(device)) == [(0, CallbackID.BUTTON_STATE_CHANGED, DEVICE.ButtonState.RELEASED)]
