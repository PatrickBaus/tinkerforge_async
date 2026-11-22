"""Tests for the Joystick Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_joystick import (
    BrickletJoystick,
    GetAnalogValue,
    GetAnalogValueCallbackThreshold,
    GetPosition,
    GetPositionCallbackThreshold,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletJoystick
FunctionID = BrickletJoystick.FunctionID
CallbackID = BrickletJoystick.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_POSITION": 1,
    "IS_PRESSED": 2,
    "GET_ANALOG_VALUE": 3,
    "CALIBRATE": 4,
    "SET_POSITION_CALLBACK_PERIOD": 5,
    "GET_POSITION_CALLBACK_PERIOD": 6,
    "SET_ANALOG_VALUE_CALLBACK_PERIOD": 7,
    "GET_ANALOG_VALUE_CALLBACK_PERIOD": 8,
    "SET_POSITION_CALLBACK_THRESHOLD": 9,
    "GET_POSITION_CALLBACK_THRESHOLD": 10,
    "SET_ANALOG_VALUE_CALLBACK_THRESHOLD": 11,
    "GET_ANALOG_VALUE_CALLBACK_THRESHOLD": 12,
    "SET_DEBOUNCE_PERIOD": 13,
    "GET_DEBOUNCE_PERIOD": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "POSITION": 15,
    "ANALOG_VALUE": 16,
    "POSITION_REACHED": 17,
    "ANALOG_VALUE_REACHED": 18,
    "PRESSED": 19,
    "RELEASED": 20,
}

CALLS: list[Call] = [
    Call("get_position", FunctionID.GET_POSITION, (), reply=("h h", (3, 4)), result=GetPosition(3, 4)),
    Call("is_pressed", FunctionID.IS_PRESSED, (), reply=("!", (True,)), result=True),
    Call("get_analog_value", FunctionID.GET_ANALOG_VALUE, (), reply=("H H", (3, 4)), result=GetAnalogValue(3, 4)),
    Call("calibrate", FunctionID.CALIBRATE, ()),
    Call("calibrate", FunctionID.CALIBRATE, (False,), response_expected=False),
    Call(
        "set_position_callback_period", FunctionID.SET_POSITION_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))
    ),
    Call(
        "set_position_callback_period",
        FunctionID.SET_POSITION_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_position_callback_period",
        FunctionID.GET_POSITION_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_analog_value_callback_period",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_analog_value_callback_period",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_analog_value_callback_period",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_position_callback_threshold",
        FunctionID.SET_POSITION_CALLBACK_THRESHOLD,
        ("o", 3, 3, 3, 3),
        sent=("c h h h h", ("o", 3, 3, 3, 3)),
    ),
    Call(
        "set_position_callback_threshold",
        FunctionID.SET_POSITION_CALLBACK_THRESHOLD,
        ("o", 3, 3, 3, 3, False),
        sent=("c h h h h", ("o", 3, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_position_callback_threshold",
        FunctionID.GET_POSITION_CALLBACK_THRESHOLD,
        (),
        reply=("c h h h h", ("o", 4, 5, 6, 7)),
        result=GetPositionCallbackThreshold(Threshold.OUTSIDE, 4, 5, 6, 7),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        ("o", 3, 3, 3, 3),
        sent=("c H H H H", ("o", 3, 3, 3, 3)),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        ("o", 3, 3, 3, 3, False),
        sent=("c H H H H", ("o", 3, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_analog_value_callback_threshold",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        (),
        reply=("c H H H H", ("o", 4, 5, 6, 7)),
        result=GetAnalogValueCallbackThreshold(Threshold.OUTSIDE, 4, 5, 6, 7),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_debounce_period",
        FunctionID.SET_DEBOUNCE_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_position_callback_period", (Decimal("4294967.296"),)),
    ("set_analog_value_callback_period", (Decimal("4294967.296"),)),
    ("set_position_callback_threshold", ("?", 3, 3, 3, 3)),
    ("set_position_callback_threshold", ("o", 32768, 3, 3, 3)),
    ("set_position_callback_threshold", ("o", 3, 32768, 3, 3)),
    ("set_position_callback_threshold", ("o", 3, 3, 32768, 3)),
    ("set_position_callback_threshold", ("o", 3, 3, 3, 32768)),
    ("set_analog_value_callback_threshold", ("?", 3, 3, 3, 3)),
    ("set_analog_value_callback_threshold", ("o", 65536, 3, 3, 3)),
    ("set_analog_value_callback_threshold", ("o", 3, 65536, 3, 3)),
    ("set_analog_value_callback_threshold", ("o", 3, 3, 65536, 3)),
    ("set_analog_value_callback_threshold", ("o", 3, 3, 3, 65536)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 210
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Joystick Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_position(device, connection):
    """The callback POSITION is converted to an event."""
    connection.callback(CallbackID.POSITION, "h h", *(3, 4))
    assert summary(read_events(device)) == [(0, CallbackID.POSITION, GetPosition(3, 4))]


def test_callback_analog_value(device, connection):
    """The callback ANALOG_VALUE is converted to an event."""
    connection.callback(CallbackID.ANALOG_VALUE, "H H", *(3, 4))
    assert summary(read_events(device)) == [(1, CallbackID.ANALOG_VALUE, GetAnalogValue(3, 4))]


def test_callback_position_reached(device, connection):
    """The callback POSITION_REACHED is converted to an event."""
    connection.callback(CallbackID.POSITION_REACHED, "h h", *(3, 4))
    assert summary(read_events(device)) == [(2, CallbackID.POSITION_REACHED, GetPosition(3, 4))]


def test_callback_analog_value_reached(device, connection):
    """The callback ANALOG_VALUE_REACHED is converted to an event."""
    connection.callback(CallbackID.ANALOG_VALUE_REACHED, "H H", *(3, 4))
    assert summary(read_events(device)) == [(3, CallbackID.ANALOG_VALUE_REACHED, GetAnalogValue(3, 4))]


def test_callback_pressed(device, connection):
    """The callback PRESSED is converted to an event."""
    connection.callback(CallbackID.PRESSED)
    assert summary(read_events(device)) == [(4, CallbackID.PRESSED, None)]


def test_callback_released(device, connection):
    """The callback RELEASED is converted to an event."""
    connection.callback(CallbackID.RELEASED)
    assert summary(read_events(device)) == [(5, CallbackID.RELEASED, None)]
