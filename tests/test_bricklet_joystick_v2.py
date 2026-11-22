"""Tests for the Joystick Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_joystick_v2 import BrickletJoystickV2, GetPosition
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletJoystickV2
FunctionID = BrickletJoystickV2.FunctionID
CallbackID = BrickletJoystickV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_POSITION": 1,
    "IS_PRESSED": 2,
    "CALIBRATE": 3,
    "SET_POSITION_CALLBACK_CONFIGURATION": 4,
    "GET_POSITION_CALLBACK_CONFIGURATION": 5,
    "SET_PRESSED_CALLBACK_CONFIGURATION": 7,
    "GET_PRESSED_CALLBACK_CONFIGURATION": 8,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"POSITION": 6, "PRESSED": 9}

CALLS: list[Call] = [
    Call("get_position", FunctionID.GET_POSITION, (), reply=("h h", (3, 4)), result=GetPosition(3, 4)),
    Call("is_pressed", FunctionID.IS_PRESSED, (), reply=("!", (True,)), result=True),
    Call("calibrate", FunctionID.CALIBRATE, ()),
    Call("calibrate", FunctionID.CALIBRATE, (False,), response_expected=False),
    Call(
        "set_position_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_position_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_position_callback_configuration",
        FunctionID.GET_POSITION_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_pressed_callback_configuration",
        FunctionID.SET_PRESSED_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_pressed_callback_configuration",
        FunctionID.SET_PRESSED_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_pressed_callback_configuration",
        FunctionID.GET_PRESSED_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_POSITION_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_PRESSED_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_PRESSED_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_position_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_pressed_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2138
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Joystick Bricklet 2.0 with uid 12345")


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


def test_callback_pressed(device, connection):
    """The callback PRESSED is converted to an event."""
    connection.callback(CallbackID.PRESSED, "!", *(True,))
    assert summary(read_events(device)) == [(1, CallbackID.PRESSED, True)]
