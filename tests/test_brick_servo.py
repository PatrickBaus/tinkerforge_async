"""Tests for the Servo Brick. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_servo import (
    BrickServo,
    GetDegree,
    GetProtocol1BrickletName,
    GetPulseWidth,
    PositionReachedEvent,
    VelocityReachedEvent,
)
from tinkerforge_async.devices import GetSPITFPBaudrateConfig, GetSPITFPErrorCount
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickServo
FunctionID = BrickServo.FunctionID
CallbackID = BrickServo.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "ENABLE": 1,
    "DISABLE": 2,
    "IS_ENABLED": 3,
    "SET_POSITION": 4,
    "GET_POSITION": 5,
    "GET_CURRENT_POSITION": 6,
    "SET_VELOCITY": 7,
    "GET_VELOCITY": 8,
    "GET_CURRENT_VELOCITY": 9,
    "SET_ACCELERATION": 10,
    "GET_ACCELERATION": 11,
    "SET_OUTPUT_VOLTAGE": 12,
    "GET_OUTPUT_VOLTAGE": 13,
    "SET_PULSE_WIDTH": 14,
    "GET_PULSE_WIDTH": 15,
    "SET_DEGREE": 16,
    "GET_DEGREE": 17,
    "SET_PERIOD": 18,
    "GET_PERIOD": 19,
    "GET_SERVO_CURRENT": 20,
    "GET_OVERALL_CURRENT": 21,
    "GET_STACK_INPUT_VOLTAGE": 22,
    "GET_EXTERNAL_INPUT_VOLTAGE": 23,
    "SET_MINIMUM_VOLTAGE": 24,
    "GET_MINIMUM_VOLTAGE": 25,
    "ENABLE_POSITION_REACHED_CALLBACK": 29,
    "DISABLE_POSITION_REACHED_CALLBACK": 30,
    "IS_POSITION_REACHED_CALLBACK_ENABLED": 31,
    "ENABLE_VELOCITY_REACHED_CALLBACK": 32,
    "DISABLE_VELOCITY_REACHED_CALLBACK": 33,
    "IS_VELOCITY_REACHED_CALLBACK_ENABLED": 34,
    "SET_SPITFP_BAUDRATE_CONFIG": 231,
    "GET_SPITFP_BAUDRATE_CONFIG": 232,
    "GET_SEND_TIMEOUT_COUNT": 233,
    "SET_SPITFP_BAUDRATE": 234,
    "GET_SPITFP_BAUDRATE": 235,
    "GET_SPITFP_ERROR_COUNT": 237,
    "ENABLE_STATUS_LED": 238,
    "DISABLE_STATUS_LED": 239,
    "IS_STATUS_LED_ENABLED": 240,
    "GET_PROTOCOL1_BRICKLET_NAME": 241,
    "GET_CHIP_TEMPERATURE": 242,
    "WRITE_BRICKLET_PLUGIN": 246,
    "READ_BRICKLET_PLUGIN": 247,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"UNDER_VOLTAGE": 26, "POSITION_REACHED": 27, "VELOCITY_REACHED": 28}

CALLS: list[Call] = [
    Call("enable", FunctionID.ENABLE, (3,), sent=("B", (3,))),
    Call("enable", FunctionID.ENABLE, (3, False), sent=("B", (3,)), response_expected=False),
    Call("disable", FunctionID.DISABLE, (3,), sent=("B", (3,))),
    Call("disable", FunctionID.DISABLE, (3, False), sent=("B", (3,)), response_expected=False),
    Call("is_enabled", FunctionID.IS_ENABLED, (3,), sent=("B", (3,)), reply=("!", (True,)), result=True),
    Call("set_position", FunctionID.SET_POSITION, (3, Decimal("0.03")), sent=("B h", (3, 3))),
    Call(
        "set_position",
        FunctionID.SET_POSITION,
        (3, Decimal("0.03"), False),
        sent=("B h", (3, 3)),
        response_expected=False,
    ),
    Call("get_position", FunctionID.GET_POSITION, (3,), sent=("B", (3,)), reply=("h", (3,)), result=Decimal("0.03")),
    Call(
        "get_current_position",
        FunctionID.GET_CURRENT_POSITION,
        (3,),
        sent=("B", (3,)),
        reply=("h", (3,)),
        result=Decimal("0.03"),
    ),
    Call("set_velocity", FunctionID.SET_VELOCITY, (3, Decimal("0.03")), sent=("B H", (3, 3))),
    Call(
        "set_velocity",
        FunctionID.SET_VELOCITY,
        (3, Decimal("0.03"), False),
        sent=("B H", (3, 3)),
        response_expected=False,
    ),
    Call("get_velocity", FunctionID.GET_VELOCITY, (3,), sent=("B", (3,)), reply=("H", (3,)), result=Decimal("0.03")),
    Call(
        "get_current_velocity",
        FunctionID.GET_CURRENT_VELOCITY,
        (3,),
        sent=("B", (3,)),
        reply=("H", (3,)),
        result=Decimal("0.03"),
    ),
    Call("set_acceleration", FunctionID.SET_ACCELERATION, (3, Decimal("0.03")), sent=("B H", (3, 3))),
    Call(
        "set_acceleration",
        FunctionID.SET_ACCELERATION,
        (3, Decimal("0.03"), False),
        sent=("B H", (3, 3)),
        response_expected=False,
    ),
    Call(
        "get_acceleration",
        FunctionID.GET_ACCELERATION,
        (3,),
        sent=("B", (3,)),
        reply=("H", (3,)),
        result=Decimal("0.03"),
    ),
    Call("set_output_voltage", FunctionID.SET_OUTPUT_VOLTAGE, (Decimal("2"),), sent=("H", (2000,))),
    Call(
        "set_output_voltage",
        FunctionID.SET_OUTPUT_VOLTAGE,
        (Decimal("2"), False),
        sent=("H", (2000,)),
        response_expected=False,
    ),
    Call("get_output_voltage", FunctionID.GET_OUTPUT_VOLTAGE, (), reply=("H", (2000,)), result=Decimal("2")),
    Call(
        "set_pulse_width",
        FunctionID.SET_PULSE_WIDTH,
        (3, Decimal("0.000003"), Decimal("0.000003")),
        sent=("B H H", (3, 3, 3)),
    ),
    Call(
        "set_pulse_width",
        FunctionID.SET_PULSE_WIDTH,
        (3, Decimal("0.000003"), Decimal("0.000003"), False),
        sent=("B H H", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_pulse_width",
        FunctionID.GET_PULSE_WIDTH,
        (3,),
        sent=("B", (3,)),
        reply=("H H", (3, 4)),
        result=GetPulseWidth(Decimal("0.000003"), Decimal("0.000004")),
    ),
    Call("set_degree", FunctionID.SET_DEGREE, (3, Decimal("0.03"), Decimal("0.03")), sent=("B h h", (3, 3, 3))),
    Call(
        "set_degree",
        FunctionID.SET_DEGREE,
        (3, Decimal("0.03"), Decimal("0.03"), False),
        sent=("B h h", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_degree",
        FunctionID.GET_DEGREE,
        (3,),
        sent=("B", (3,)),
        reply=("h h", (3, 4)),
        result=GetDegree(Decimal("0.03"), Decimal("0.04")),
    ),
    Call("set_period", FunctionID.SET_PERIOD, (3, Decimal("0.000003")), sent=("B H", (3, 3))),
    Call(
        "set_period",
        FunctionID.SET_PERIOD,
        (3, Decimal("0.000003"), False),
        sent=("B H", (3, 3)),
        response_expected=False,
    ),
    Call("get_period", FunctionID.GET_PERIOD, (3,), sent=("B", (3,)), reply=("H", (3,)), result=Decimal("0.000003")),
    Call(
        "get_servo_current",
        FunctionID.GET_SERVO_CURRENT,
        (3,),
        sent=("B", (3,)),
        reply=("H", (3,)),
        result=Decimal("0.003"),
    ),
    Call("get_overall_current", FunctionID.GET_OVERALL_CURRENT, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("get_stack_input_voltage", FunctionID.GET_STACK_INPUT_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "get_external_input_voltage",
        FunctionID.GET_EXTERNAL_INPUT_VOLTAGE,
        (),
        reply=("H", (3,)),
        result=Decimal("0.003"),
    ),
    Call("set_minimum_voltage", FunctionID.SET_MINIMUM_VOLTAGE, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_minimum_voltage",
        FunctionID.SET_MINIMUM_VOLTAGE,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_minimum_voltage", FunctionID.GET_MINIMUM_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("enable_position_reached_callback", FunctionID.ENABLE_POSITION_REACHED_CALLBACK, ()),
    Call(
        "enable_position_reached_callback",
        FunctionID.ENABLE_POSITION_REACHED_CALLBACK,
        (False,),
        response_expected=False,
    ),
    Call("disable_position_reached_callback", FunctionID.DISABLE_POSITION_REACHED_CALLBACK, ()),
    Call(
        "disable_position_reached_callback",
        FunctionID.DISABLE_POSITION_REACHED_CALLBACK,
        (False,),
        response_expected=False,
    ),
    Call(
        "is_position_reached_callback_enabled",
        FunctionID.IS_POSITION_REACHED_CALLBACK_ENABLED,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call("enable_velocity_reached_callback", FunctionID.ENABLE_VELOCITY_REACHED_CALLBACK, ()),
    Call(
        "enable_velocity_reached_callback",
        FunctionID.ENABLE_VELOCITY_REACHED_CALLBACK,
        (False,),
        response_expected=False,
    ),
    Call("disable_velocity_reached_callback", FunctionID.DISABLE_VELOCITY_REACHED_CALLBACK, ()),
    Call(
        "disable_velocity_reached_callback",
        FunctionID.DISABLE_VELOCITY_REACHED_CALLBACK,
        (False,),
        response_expected=False,
    ),
    Call(
        "is_velocity_reached_callback_enabled",
        FunctionID.IS_VELOCITY_REACHED_CALLBACK_ENABLED,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "set_spitfp_baudrate_config",
        FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
        (True, 400000),
        sent=("! I", (True, 400000)),
    ),
    Call(
        "set_spitfp_baudrate_config",
        FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
        (True, 400000, False),
        sent=("! I", (True, 400000)),
        response_expected=False,
    ),
    Call(
        "get_spitfp_baudrate_config",
        FunctionID.GET_SPITFP_BAUDRATE_CONFIG,
        (),
        reply=("! I", (True, 4)),
        result=GetSPITFPBaudrateConfig(True, 4),
    ),
    Call(
        "get_send_timeout_count",
        FunctionID.GET_SEND_TIMEOUT_COUNT,
        (DEVICE.CommunicationMethod.WIFI_V2,),
        sent=("B", (7,)),
        reply=("I", (3,)),
        result=3,
    ),
    Call("set_spitfp_baudrate", FunctionID.SET_SPITFP_BAUDRATE, ("b", 400000), sent=("c I", ("b", 400000))),
    Call(
        "set_spitfp_baudrate",
        FunctionID.SET_SPITFP_BAUDRATE,
        ("b", 400000, False),
        sent=("c I", ("b", 400000)),
        response_expected=False,
    ),
    Call(
        "get_spitfp_baudrate", FunctionID.GET_SPITFP_BAUDRATE, ("b",), sent=("c", ("b",)), reply=("I", (3,)), result=3
    ),
    Call(
        "get_spitfp_error_count",
        FunctionID.GET_SPITFP_ERROR_COUNT,
        ("b",),
        sent=("c", ("b",)),
        reply=("I I I I", (3, 4, 5, 6)),
        result=GetSPITFPErrorCount(3, 4, 5, 6),
    ),
    Call("enable_status_led", FunctionID.ENABLE_STATUS_LED, ()),
    Call("enable_status_led", FunctionID.ENABLE_STATUS_LED, (False,), response_expected=False),
    Call("disable_status_led", FunctionID.DISABLE_STATUS_LED, ()),
    Call("disable_status_led", FunctionID.DISABLE_STATUS_LED, (False,), response_expected=False),
    Call("is_status_led_enabled", FunctionID.IS_STATUS_LED_ENABLED, (), reply=("!", (True,)), result=True),
    Call(
        "get_protocol1_bricklet_name",
        FunctionID.GET_PROTOCOL1_BRICKLET_NAME,
        ("b",),
        sent=("c", ("b",)),
        reply=("B 3B 40s", (3, [i % 256 for i in range(3)], b"abc")),
        result=GetProtocol1BrickletName(3, tuple(i % 256 for i in range(3)), "abc"),
    ),
    Call("get_chip_temperature", FunctionID.GET_CHIP_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("273.45")),
    Call(
        "write_bricklet_plugin",
        FunctionID.WRITE_BRICKLET_PLUGIN,
        ("b", 3, [i % 256 for i in range(32)]),
        sent=("c B 32B", ("b", 3, [i % 256 for i in range(32)])),
    ),
    Call(
        "write_bricklet_plugin",
        FunctionID.WRITE_BRICKLET_PLUGIN,
        ("b", 3, [i % 256 for i in range(32)], False),
        sent=("c B 32B", ("b", 3, [i % 256 for i in range(32)])),
        response_expected=False,
    ),
    Call(
        "read_bricklet_plugin",
        FunctionID.READ_BRICKLET_PLUGIN,
        ("b", 3),
        sent=("c B", ("b", 3)),
        reply=("32B", ([i % 256 for i in range(32)],)),
        result=tuple(i % 256 for i in range(32)),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("enable", (256,)),
    ("disable", (256,)),
    ("is_enabled", (7,)),
    ("set_position", (256, Decimal("0.03"))),
    ("set_position", (3, Decimal("327.68"))),
    ("get_position", (7,)),
    ("get_current_position", (7,)),
    ("set_velocity", (256, Decimal("0.03"))),
    ("set_velocity", (3, Decimal("655.36"))),
    ("get_velocity", (7,)),
    ("get_current_velocity", (7,)),
    ("set_acceleration", (256, Decimal("0.03"))),
    ("set_acceleration", (3, Decimal("655.36"))),
    ("get_acceleration", (7,)),
    ("set_output_voltage", (Decimal("9.001"),)),
    ("set_pulse_width", (256, Decimal("0.000003"), Decimal("0.000003"))),
    ("set_pulse_width", (3, Decimal("0.065536"), Decimal("0.000003"))),
    ("set_pulse_width", (3, Decimal("0.000003"), Decimal("0.065536"))),
    ("get_pulse_width", (7,)),
    ("set_degree", (256, Decimal("0.03"), Decimal("0.03"))),
    ("set_degree", (3, Decimal("327.68"), Decimal("0.03"))),
    ("set_degree", (3, Decimal("0.03"), Decimal("327.68"))),
    ("get_degree", (7,)),
    ("set_period", (256, Decimal("0.000003"))),
    ("set_period", (3, Decimal("0.065536"))),
    ("get_period", (7,)),
    ("get_servo_current", (7,)),
    ("set_minimum_voltage", (Decimal("65.536"),)),
    ("set_spitfp_baudrate_config", (True, 2000001)),
    ("get_send_timeout_count", (12345,)),
    ("set_spitfp_baudrate", ("b", 2000001)),
    ("write_bricklet_plugin", ("b", 256, [i % 256 for i in range(32)])),
    ("write_bricklet_plugin", ("b", 3, ([i % 256 for i in range(32)])[:-1])),
    ("read_bricklet_plugin", ("b", 256)),
]


def test_identity(device: BrickServo) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 14
    assert device.get_api_version() == (2, 0, 4)
    assert str(device).startswith("Servo Brick with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_under_voltage(device: BrickServo, connection: FakeConnection) -> None:
    """The callback UNDER_VOLTAGE is converted to an event."""
    connection.callback(CallbackID.UNDER_VOLTAGE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.UNDER_VOLTAGE, Decimal("0.003"))]


def test_callback_position_reached(device: BrickServo, connection: FakeConnection) -> None:
    """The callback POSITION_REACHED is converted to an event."""
    connection.callback(CallbackID.POSITION_REACHED, "B h", *(3, 4))
    assert summary(read_events(device)) == [(1, CallbackID.POSITION_REACHED, PositionReachedEvent(3, Decimal("0.04")))]


def test_callback_velocity_reached(device: BrickServo, connection: FakeConnection) -> None:
    """The callback VELOCITY_REACHED is converted to an event."""
    connection.callback(CallbackID.VELOCITY_REACHED, "B h", *(3, 4))
    assert summary(read_events(device)) == [(2, CallbackID.VELOCITY_REACHED, VelocityReachedEvent(3, Decimal("0.04")))]
