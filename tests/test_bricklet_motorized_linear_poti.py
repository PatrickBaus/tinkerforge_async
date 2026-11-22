"""Tests for the Motorized Linear Poti Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_motorized_linear_poti import BrickletMotorizedLinearPoti, GetMotorPosition
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletMotorizedLinearPoti
FunctionID = BrickletMotorizedLinearPoti.FunctionID
CallbackID = BrickletMotorizedLinearPoti.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_POSITION": 1,
    "SET_POSITION_CALLBACK_CONFIGURATION": 2,
    "GET_POSITION_CALLBACK_CONFIGURATION": 3,
    "SET_MOTOR_POSITION": 5,
    "GET_MOTOR_POSITION": 6,
    "CALIBRATE": 7,
    "SET_POSITION_REACHED_CALLBACK_CONFIGURATION": 8,
    "GET_POSITION_REACHED_CALLBACK_CONFIGURATION": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"POSITION": 4, "POSITION_REACHED": 10}

CALLS: list[Call] = [
    Call("get_position", FunctionID.GET_POSITION, (), reply=("H", (3,)), result=3),
    Call(
        "set_position_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_position_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3, False),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_position_callback_configuration",
        FunctionID.GET_POSITION_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c H H", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call(
        "set_motor_position",
        FunctionID.SET_MOTOR_POSITION,
        (3, DEVICE.DriveMode.SMOOTH, True),
        sent=("H B !", (3, 1, True)),
    ),
    Call(
        "set_motor_position",
        FunctionID.SET_MOTOR_POSITION,
        (3, DEVICE.DriveMode.SMOOTH, True, False),
        sent=("H B !", (3, 1, True)),
        response_expected=False,
    ),
    Call(
        "get_motor_position",
        FunctionID.GET_MOTOR_POSITION,
        (),
        reply=("H B ! !", (3, 1, True, True)),
        result=GetMotorPosition(3, DEVICE.DriveMode.SMOOTH, True, True),
    ),
    Call("calibrate", FunctionID.CALIBRATE, ()),
    Call("calibrate", FunctionID.CALIBRATE, (False,), response_expected=False),
    Call(
        "set_position_reached_callback_configuration",
        FunctionID.SET_POSITION_REACHED_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_position_reached_callback_configuration",
        FunctionID.SET_POSITION_REACHED_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_position_reached_callback_configuration",
        FunctionID.GET_POSITION_REACHED_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call("get_value", FunctionID.GET_POSITION, (0,), reply=("H", (3,)), result=3),
    Call(
        "set_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, 3, 4),
        sent=("I ! c H H", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_POSITION_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c H H", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_position_callback_configuration", (Decimal("4294967.296"), True, "o", 3, 3)),
    ("set_position_callback_configuration", (Decimal("0.003"), True, "?", 3, 3)),
    ("set_position_callback_configuration", (Decimal("0.003"), True, "o", 65536, 3)),
    ("set_position_callback_configuration", (Decimal("0.003"), True, "o", 3, 65536)),
    ("set_motor_position", (101, DEVICE.DriveMode.SMOOTH, True)),
    ("set_motor_position", (3, 12345, True)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device: BrickletMotorizedLinearPoti) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 267
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Motorized Linear Poti Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_position(device: BrickletMotorizedLinearPoti, connection: FakeConnection) -> None:
    """The callback POSITION is converted to an event."""
    connection.callback(CallbackID.POSITION, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.POSITION, 3)]


def test_callback_position_reached(device: BrickletMotorizedLinearPoti, connection: FakeConnection) -> None:
    """The callback POSITION_REACHED is converted to an event."""
    connection.callback(CallbackID.POSITION_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.POSITION_REACHED, 3)]
