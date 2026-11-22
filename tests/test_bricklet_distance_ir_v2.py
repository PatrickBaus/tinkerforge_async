"""Tests for the Distance IR Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_distance_ir_v2 import BrickletDistanceIRV2
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletDistanceIRV2
FunctionID = BrickletDistanceIRV2.FunctionID
CallbackID = BrickletDistanceIRV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_DISTANCE": 1,
    "SET_DISTANCE_CALLBACK_CONFIGURATION": 2,
    "GET_DISTANCE_CALLBACK_CONFIGURATION": 3,
    "GET_ANALOG_VALUE": 5,
    "SET_ANALOG_VALUE_CALLBACK_CONFIGURATION": 6,
    "GET_ANALOG_VALUE_CALLBACK_CONFIGURATION": 7,
    "SET_MOVING_AVERAGE_CONFIGURATION": 9,
    "GET_MOVING_AVERAGE_CONFIGURATION": 10,
    "SET_DISTANCE_LED_CONFIG": 11,
    "GET_DISTANCE_LED_CONFIG": 12,
    "SET_SENSOR_TYPE": 13,
    "GET_SENSOR_TYPE": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DISTANCE": 4, "ANALOG_VALUE": 8}

CALLS: list[Call] = [
    Call("get_distance", FunctionID.GET_DISTANCE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "set_distance_callback_configuration",
        FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003")),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_distance_callback_configuration",
        FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_distance_callback_configuration",
        FunctionID.GET_DISTANCE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c H H", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.006"), Decimal("0.007")
        ),
    ),
    Call("get_analog_value", FunctionID.GET_ANALOG_VALUE, (), reply=("I", (3,)), result=3),
    Call(
        "set_analog_value_callback_configuration",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3),
        sent=("I ! c I I", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_analog_value_callback_configuration",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3, False),
        sent=("I ! c I I", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_analog_value_callback_configuration",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c I I", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call("set_moving_average_configuration", FunctionID.SET_MOVING_AVERAGE_CONFIGURATION, (3,), sent=("H", (3,))),
    Call(
        "set_moving_average_configuration",
        FunctionID.SET_MOVING_AVERAGE_CONFIGURATION,
        (3, False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call(
        "get_moving_average_configuration", FunctionID.GET_MOVING_AVERAGE_CONFIGURATION, (), reply=("H", (3,)), result=3
    ),
    Call(
        "set_distance_led_config",
        FunctionID.SET_DISTANCE_LED_CONFIG,
        (DEVICE.DistanceLEDConfig.SHOW_DISTANCE,),
        sent=("B", (3,)),
    ),
    Call(
        "set_distance_led_config",
        FunctionID.SET_DISTANCE_LED_CONFIG,
        (DEVICE.DistanceLEDConfig.SHOW_DISTANCE, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_distance_led_config",
        FunctionID.GET_DISTANCE_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.DistanceLEDConfig.SHOW_DISTANCE,
    ),
    Call("set_sensor_type", FunctionID.SET_SENSOR_TYPE, (DEVICE.SensorType.SENSOR_TYPE_2Y0A02,), sent=("B", (2,))),
    Call(
        "set_sensor_type",
        FunctionID.SET_SENSOR_TYPE,
        (DEVICE.SensorType.SENSOR_TYPE_2Y0A02, False),
        sent=("B", (2,)),
        response_expected=False,
    ),
    Call(
        "get_sensor_type",
        FunctionID.GET_SENSOR_TYPE,
        (),
        reply=("B", (2,)),
        result=DEVICE.SensorType.SENSOR_TYPE_2Y0A02,
    ),
    Call("get_value", FunctionID.GET_DISTANCE, (0,), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
        sent=("I ! c H H", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_DISTANCE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c H H", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
    ),
    Call("get_value", FunctionID.GET_ANALOG_VALUE, (1,), reply=("I", (3,)), result=3),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_CONFIGURATION,
        (1, 1, True, Threshold.OUTSIDE, 3, 4),
        sent=("I ! c I I", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c I I", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_distance_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "o", Decimal("65.536"), Decimal("0.003"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("65.536"))),
    ("set_analog_value_callback_configuration", (Decimal("4294967.296"), True, "o", 3, 3)),
    ("set_analog_value_callback_configuration", (Decimal("0.003"), True, "?", 3, 3)),
    ("set_analog_value_callback_configuration", (Decimal("0.003"), True, "o", 4294967296, 3)),
    ("set_analog_value_callback_configuration", (Decimal("0.003"), True, "o", 3, 4294967296)),
    ("set_moving_average_configuration", (1001,)),
    ("set_distance_led_config", (12345,)),
    ("set_sensor_type", (12345,)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device: BrickletDistanceIRV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2125
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Distance IR Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_distance(device: BrickletDistanceIRV2, connection: FakeConnection) -> None:
    """The callback DISTANCE is converted to an event."""
    connection.callback(CallbackID.DISTANCE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.DISTANCE, Decimal("0.003"))]


def test_callback_analog_value(device: BrickletDistanceIRV2, connection: FakeConnection) -> None:
    """The callback ANALOG_VALUE is converted to an event."""
    connection.callback(CallbackID.ANALOG_VALUE, "I", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.ANALOG_VALUE, 3)]
