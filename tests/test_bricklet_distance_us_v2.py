"""Tests for the Distance US Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_distance_us_v2 import BrickletDistanceUSV2
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletDistanceUSV2
FunctionID = BrickletDistanceUSV2.FunctionID
CallbackID = BrickletDistanceUSV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_DISTANCE": 1,
    "SET_DISTANCE_CALLBACK_CONFIGURATION": 2,
    "GET_DISTANCE_CALLBACK_CONFIGURATION": 3,
    "SET_UPDATE_RATE": 5,
    "GET_UPDATE_RATE": 6,
    "SET_DISTANCE_LED_CONFIG": 7,
    "GET_DISTANCE_LED_CONFIG": 8,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DISTANCE": 4}

CALLS: list[Call] = [
    Call("get_distance", FunctionID.GET_DISTANCE, (), reply=("H", (300,)), result=Decimal("0.3")),
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
    Call("set_update_rate", FunctionID.SET_UPDATE_RATE, (DEVICE.UpdateRate.UPDATE_RATE_10_HZ,), sent=("B", (1,))),
    Call(
        "set_update_rate",
        FunctionID.SET_UPDATE_RATE,
        (DEVICE.UpdateRate.UPDATE_RATE_10_HZ, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call(
        "get_update_rate", FunctionID.GET_UPDATE_RATE, (), reply=("B", (1,)), result=DEVICE.UpdateRate.UPDATE_RATE_10_HZ
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
    Call("get_value", FunctionID.GET_DISTANCE, (0,), reply=("H", (300,)), result=Decimal("0.3")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.3")),
        sent=("I ! c H H", (1000, True, "o", 300, 300)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_DISTANCE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c H H", (1000, True, "o", 300, 300)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.3")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_distance_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "o", Decimal("65.536"), Decimal("0.003"))),
    ("set_distance_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("65.536"))),
    ("set_update_rate", (12345,)),
    ("set_distance_led_config", (12345,)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 299
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Distance US Bricklet 2.0 with uid 12345")


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
    connection.callback(CallbackID.DISTANCE, "H", *(300,))
    assert summary(read_events(device)) == [(0, CallbackID.DISTANCE, Decimal("0.3"))]
