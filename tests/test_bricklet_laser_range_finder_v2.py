"""Tests for the Laser Range Finder Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_laser_range_finder_v2 import (
    BrickletLaserRangeFinderV2,
    GetConfiguration,
    GetMovingAverage,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletLaserRangeFinderV2
FunctionID = BrickletLaserRangeFinderV2.FunctionID
CallbackID = BrickletLaserRangeFinderV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_DISTANCE": 1,
    "SET_DISTANCE_CALLBACK_CONFIGURATION": 2,
    "GET_DISTANCE_CALLBACK_CONFIGURATION": 3,
    "GET_VELOCITY": 5,
    "SET_VELOCITY_CALLBACK_CONFIGURATION": 6,
    "GET_VELOCITY_CALLBACK_CONFIGURATION": 7,
    "SET_ENABLE": 9,
    "GET_ENABLE": 10,
    "SET_CONFIGURATION": 11,
    "GET_CONFIGURATION": 12,
    "SET_MOVING_AVERAGE": 13,
    "GET_MOVING_AVERAGE": 14,
    "SET_OFFSET_CALIBRATION": 15,
    "GET_OFFSET_CALIBRATION": 16,
    "SET_DISTANCE_LED_CONFIG": 17,
    "GET_DISTANCE_LED_CONFIG": 18,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DISTANCE": 4, "VELOCITY": 8}

CALLS: list[Call] = [
    Call("get_distance", FunctionID.GET_DISTANCE, (), reply=("h", (3,)), result=Decimal("0.03")),
    Call(
        "set_distance_callback_configuration",
        FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("0.03")),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_distance_callback_configuration",
        FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("0.03"), False),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_distance_callback_configuration",
        FunctionID.GET_DISTANCE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c h h", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.06"), Decimal("0.07")
        ),
    ),
    Call("get_velocity", FunctionID.GET_VELOCITY, (), reply=("h", (3,)), result=Decimal("0.03")),
    Call(
        "set_velocity_callback_configuration",
        FunctionID.SET_VELOCITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("0.03")),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_velocity_callback_configuration",
        FunctionID.SET_VELOCITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("0.03"), False),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_velocity_callback_configuration",
        FunctionID.GET_VELOCITY_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c h h", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.06"), Decimal("0.07")
        ),
    ),
    Call("set_enable", FunctionID.SET_ENABLE, (True,), sent=("!", (True,))),
    Call("set_enable", FunctionID.SET_ENABLE, (True, False), sent=("!", (True,)), response_expected=False),
    Call("get_enable", FunctionID.GET_ENABLE, (), reply=("!", (True,)), result=True),
    Call(
        "set_configuration", FunctionID.SET_CONFIGURATION, (3, True, 3, Decimal("0")), sent=("B ! B H", (3, True, 3, 0))
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (3, True, 3, Decimal("0"), False),
        sent=("B ! B H", (3, True, 3, 0)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B ! B H", (3, True, 5, 0)),
        result=GetConfiguration(3, True, 5, Decimal("0")),
    ),
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3, 3), sent=("B B", (3, 3))),
    Call(
        "set_moving_average",
        FunctionID.SET_MOVING_AVERAGE,
        (3, 3, False),
        sent=("B B", (3, 3)),
        response_expected=False,
    ),
    Call("get_moving_average", FunctionID.GET_MOVING_AVERAGE, (), reply=("B B", (3, 4)), result=GetMovingAverage(3, 4)),
    Call("set_offset_calibration", FunctionID.SET_OFFSET_CALIBRATION, (Decimal("0.03"),), sent=("h", (3,))),
    Call(
        "set_offset_calibration",
        FunctionID.SET_OFFSET_CALIBRATION,
        (Decimal("0.03"), False),
        sent=("h", (3,)),
        response_expected=False,
    ),
    Call("get_offset_calibration", FunctionID.GET_OFFSET_CALIBRATION, (), reply=("h", (3,)), result=Decimal("0.03")),
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
    Call("get_value", FunctionID.GET_DISTANCE, (0,), reply=("h", (3,)), result=Decimal("0.03")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")),
        sent=("I ! c h h", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_DISTANCE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c h h", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")),
    ),
    Call("get_value", FunctionID.GET_VELOCITY, (1,), reply=("h", (3,)), result=Decimal("0.03")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_VELOCITY_CALLBACK_CONFIGURATION,
        (1, 1, True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")),
        sent=("I ! c h h", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_VELOCITY_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c h h", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_distance_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.03"), Decimal("0.03"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.03"), Decimal("0.03"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "o", Decimal("327.68"), Decimal("0.03"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("327.68"))),
    ("set_velocity_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.03"), Decimal("0.03"))),
    ("set_velocity_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.03"), Decimal("0.03"))),
    ("set_velocity_callback_configuration", (Decimal("0.003"), True, "o", Decimal("327.68"), Decimal("0.03"))),
    ("set_velocity_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("327.68"))),
    ("set_configuration", (256, True, 3, Decimal("0"))),
    ("set_configuration", (3, True, 256, Decimal("0"))),
    ("set_configuration", (3, True, 3, Decimal("65536"))),
    ("set_moving_average", (256, 3)),
    ("set_moving_average", (3, 256)),
    ("set_offset_calibration", (Decimal("327.68"),)),
    ("set_distance_led_config", (12345,)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2144
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Laser Range Finder Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_distance(device, connection):
    """The callback DISTANCE is converted to an event."""
    connection.callback(CallbackID.DISTANCE, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.DISTANCE, Decimal("0.03"))]


def test_callback_velocity(device, connection):
    """The callback VELOCITY is converted to an event."""
    connection.callback(CallbackID.VELOCITY, "h", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.VELOCITY, Decimal("0.03"))]
