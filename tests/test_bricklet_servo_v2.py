"""Tests for the Servo Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_servo_v2 import (
    BrickletServoV2,
    GetDegree,
    GetMotionConfiguration,
    GetPulseWidth,
    GetStatus,
    PositionReachedEvent,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletServoV2
FunctionID = BrickletServoV2.FunctionID
CallbackID = BrickletServoV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_STATUS": 1,
    "SET_ENABLE": 2,
    "GET_ENABLED": 3,
    "SET_POSITION": 4,
    "GET_POSITION": 5,
    "GET_CURRENT_POSITION": 6,
    "GET_CURRENT_VELOCITY": 7,
    "SET_MOTION_CONFIGURATION": 8,
    "GET_MOTION_CONFIGURATION": 9,
    "SET_PULSE_WIDTH": 10,
    "GET_PULSE_WIDTH": 11,
    "SET_DEGREE": 12,
    "GET_DEGREE": 13,
    "SET_PERIOD": 14,
    "GET_PERIOD": 15,
    "GET_SERVO_CURRENT": 16,
    "SET_SERVO_CURRENT_CONFIGURATION": 17,
    "GET_SERVO_CURRENT_CONFIGURATION": 18,
    "SET_INPUT_VOLTAGE_CONFIGURATION": 19,
    "GET_INPUT_VOLTAGE_CONFIGURATION": 20,
    "GET_OVERALL_CURRENT": 21,
    "GET_INPUT_VOLTAGE": 22,
    "SET_CURRENT_CALIBRATION": 23,
    "GET_CURRENT_CALIBRATION": 24,
    "SET_POSITION_REACHED_CALLBACK_CONFIGURATION": 25,
    "GET_POSITION_REACHED_CALLBACK_CONFIGURATION": 26,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"POSITION_REACHED": 27}

CALLS: list[Call] = [
    Call(
        "get_status",
        FunctionID.GET_STATUS,
        (),
        reply=("10! 10h 10h 10H H", ([i % 2 == 0 for i in range(10)], [4] * 10, [5] * 10, [6] * 10, 7)),
        result=GetStatus(
            tuple(i % 2 == 0 for i in range(10)),
            (Decimal("0.04"),) * 10,
            (Decimal("0.05"),) * 10,
            (Decimal("0.006"),) * 10,
            Decimal("0.007"),
        ),
    ),
    Call("set_enable", FunctionID.SET_ENABLE, (3, True), sent=("H !", (3, True))),
    Call("set_enable", FunctionID.SET_ENABLE, (3, True, False), sent=("H !", (3, True)), response_expected=False),
    Call("get_enabled", FunctionID.GET_ENABLED, (3,), sent=("H", (3,)), reply=("!", (True,)), result=True),
    Call("set_position", FunctionID.SET_POSITION, (3, Decimal("0.03")), sent=("H h", (3, 3))),
    Call(
        "set_position",
        FunctionID.SET_POSITION,
        (3, Decimal("0.03"), False),
        sent=("H h", (3, 3)),
        response_expected=False,
    ),
    Call("get_position", FunctionID.GET_POSITION, (3,), sent=("H", (3,)), reply=("h", (3,)), result=Decimal("0.03")),
    Call(
        "get_current_position",
        FunctionID.GET_CURRENT_POSITION,
        (3,),
        sent=("H", (3,)),
        reply=("h", (3,)),
        result=Decimal("0.03"),
    ),
    Call(
        "get_current_velocity",
        FunctionID.GET_CURRENT_VELOCITY,
        (3,),
        sent=("H", (3,)),
        reply=("H", (3,)),
        result=Decimal("0.03"),
    ),
    Call(
        "set_motion_configuration",
        FunctionID.SET_MOTION_CONFIGURATION,
        (3, Decimal("0.03"), Decimal("0.03"), Decimal("0.03")),
        sent=("H I I I", (3, 3, 3, 3)),
    ),
    Call(
        "set_motion_configuration",
        FunctionID.SET_MOTION_CONFIGURATION,
        (3, Decimal("0.03"), Decimal("0.03"), Decimal("0.03"), False),
        sent=("H I I I", (3, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_motion_configuration",
        FunctionID.GET_MOTION_CONFIGURATION,
        (3,),
        sent=("H", (3,)),
        reply=("I I I", (3, 4, 5)),
        result=GetMotionConfiguration(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")),
    ),
    Call(
        "set_pulse_width",
        FunctionID.SET_PULSE_WIDTH,
        (3, Decimal("0.000003"), Decimal("0.000003")),
        sent=("H I I", (3, 3, 3)),
    ),
    Call(
        "set_pulse_width",
        FunctionID.SET_PULSE_WIDTH,
        (3, Decimal("0.000003"), Decimal("0.000003"), False),
        sent=("H I I", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_pulse_width",
        FunctionID.GET_PULSE_WIDTH,
        (3,),
        sent=("H", (3,)),
        reply=("I I", (3, 4)),
        result=GetPulseWidth(Decimal("0.000003"), Decimal("0.000004")),
    ),
    Call("set_degree", FunctionID.SET_DEGREE, (3, Decimal("0.03"), Decimal("0.03")), sent=("H h h", (3, 3, 3))),
    Call(
        "set_degree",
        FunctionID.SET_DEGREE,
        (3, Decimal("0.03"), Decimal("0.03"), False),
        sent=("H h h", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_degree",
        FunctionID.GET_DEGREE,
        (3,),
        sent=("H", (3,)),
        reply=("h h", (3, 4)),
        result=GetDegree(Decimal("0.03"), Decimal("0.04")),
    ),
    Call("set_period", FunctionID.SET_PERIOD, (3, Decimal("0.000003")), sent=("H I", (3, 3))),
    Call(
        "set_period",
        FunctionID.SET_PERIOD,
        (3, Decimal("0.000003"), False),
        sent=("H I", (3, 3)),
        response_expected=False,
    ),
    Call("get_period", FunctionID.GET_PERIOD, (3,), sent=("H", (3,)), reply=("I", (3,)), result=Decimal("0.000003")),
    Call(
        "get_servo_current",
        FunctionID.GET_SERVO_CURRENT,
        (3,),
        sent=("H", (3,)),
        reply=("H", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_servo_current_configuration",
        FunctionID.SET_SERVO_CURRENT_CONFIGURATION,
        (3, Decimal("0.003")),
        sent=("H B", (3, 3)),
    ),
    Call(
        "set_servo_current_configuration",
        FunctionID.SET_SERVO_CURRENT_CONFIGURATION,
        (3, Decimal("0.003"), False),
        sent=("H B", (3, 3)),
        response_expected=False,
    ),
    Call(
        "get_servo_current_configuration",
        FunctionID.GET_SERVO_CURRENT_CONFIGURATION,
        (3,),
        sent=("H", (3,)),
        reply=("B", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_input_voltage_configuration",
        FunctionID.SET_INPUT_VOLTAGE_CONFIGURATION,
        (Decimal("0.003"),),
        sent=("B", (3,)),
    ),
    Call(
        "set_input_voltage_configuration",
        FunctionID.SET_INPUT_VOLTAGE_CONFIGURATION,
        (Decimal("0.003"), False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_input_voltage_configuration",
        FunctionID.GET_INPUT_VOLTAGE_CONFIGURATION,
        (),
        reply=("B", (3,)),
        result=Decimal("0.003"),
    ),
    Call("get_overall_current", FunctionID.GET_OVERALL_CURRENT, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("get_input_voltage", FunctionID.GET_INPUT_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "set_current_calibration",
        FunctionID.SET_CURRENT_CALIBRATION,
        ([Decimal("0.003")] * 10,),
        sent=("10h", ([3] * 10,)),
    ),
    Call(
        "set_current_calibration",
        FunctionID.SET_CURRENT_CALIBRATION,
        ([Decimal("0.003")] * 10, False),
        sent=("10h", ([3] * 10,)),
        response_expected=False,
    ),
    Call(
        "get_current_calibration",
        FunctionID.GET_CURRENT_CALIBRATION,
        (),
        reply=("10h", ([3] * 10,)),
        result=(Decimal("0.003"),) * 10,
    ),
    Call(
        "set_position_reached_callback_configuration",
        FunctionID.SET_POSITION_REACHED_CALLBACK_CONFIGURATION,
        (3, True),
        sent=("H !", (3, True)),
    ),
    Call(
        "set_position_reached_callback_configuration",
        FunctionID.SET_POSITION_REACHED_CALLBACK_CONFIGURATION,
        (3, True, False),
        sent=("H !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_position_reached_callback_configuration",
        FunctionID.GET_POSITION_REACHED_CALLBACK_CONFIGURATION,
        (3,),
        sent=("H", (3,)),
        reply=("!", (True,)),
        result=True,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_enable", (65536, True)),
    ("get_enabled", (10,)),
    ("set_position", (65536, Decimal("0.03"))),
    ("set_position", (3, Decimal("327.68"))),
    ("get_position", (10,)),
    ("get_current_position", (10,)),
    ("get_current_velocity", (10,)),
    ("set_motion_configuration", (65536, Decimal("0.03"), Decimal("0.03"), Decimal("0.03"))),
    ("set_motion_configuration", (3, Decimal("5000.01"), Decimal("0.03"), Decimal("0.03"))),
    ("set_motion_configuration", (3, Decimal("0.03"), Decimal("5000.01"), Decimal("0.03"))),
    ("set_motion_configuration", (3, Decimal("0.03"), Decimal("0.03"), Decimal("5000.01"))),
    ("get_motion_configuration", (10,)),
    ("set_pulse_width", (65536, Decimal("0.000003"), Decimal("0.000003"))),
    ("set_pulse_width", (3, Decimal("4294.967296"), Decimal("0.000003"))),
    ("set_pulse_width", (3, Decimal("0.000003"), Decimal("4294.967296"))),
    ("get_pulse_width", (10,)),
    ("set_degree", (65536, Decimal("0.03"), Decimal("0.03"))),
    ("set_degree", (3, Decimal("327.68"), Decimal("0.03"))),
    ("set_degree", (3, Decimal("0.03"), Decimal("327.68"))),
    ("get_degree", (10,)),
    ("set_period", (65536, Decimal("0.000003"))),
    ("set_period", (3, Decimal("1.000001"))),
    ("get_period", (10,)),
    ("get_servo_current", (10,)),
    ("set_servo_current_configuration", (65536, Decimal("0.003"))),
    ("set_servo_current_configuration", (3, Decimal("0.256"))),
    ("get_servo_current_configuration", (10,)),
    ("set_input_voltage_configuration", (Decimal("0.256"),)),
    ("set_current_calibration", (([Decimal("0.003")] * 10)[:-1],)),
    ("set_position_reached_callback_configuration", (65536, True)),
    ("get_position_reached_callback_configuration", (10,)),
]


def test_identity(device: BrickletServoV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2157
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Servo Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_position_reached(device: BrickletServoV2, connection: FakeConnection) -> None:
    """The callback POSITION_REACHED is converted to an event."""
    connection.callback(CallbackID.POSITION_REACHED, "H h", *(3, 4))
    assert summary(read_events(device)) == [(0, CallbackID.POSITION_REACHED, PositionReachedEvent(3, Decimal("0.04")))]
