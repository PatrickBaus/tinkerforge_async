"""Tests for the Load Cell Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_load_cell_v2 import BrickletLoadCellV2, GetConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletLoadCellV2
FunctionID = BrickletLoadCellV2.FunctionID
CallbackID = BrickletLoadCellV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_WEIGHT": 1,
    "SET_WEIGHT_CALLBACK_CONFIGURATION": 2,
    "GET_WEIGHT_CALLBACK_CONFIGURATION": 3,
    "SET_MOVING_AVERAGE": 5,
    "GET_MOVING_AVERAGE": 6,
    "SET_INFO_LED_CONFIG": 7,
    "GET_INFO_LED_CONFIG": 8,
    "CALIBRATE": 9,
    "TARE": 10,
    "SET_CONFIGURATION": 11,
    "GET_CONFIGURATION": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"WEIGHT": 4}

CALLS: list[Call] = [
    Call("get_weight", FunctionID.GET_WEIGHT, (), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_weight_callback_configuration",
        FunctionID.SET_WEIGHT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_weight_callback_configuration",
        FunctionID.SET_WEIGHT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_weight_callback_configuration",
        FunctionID.GET_WEIGHT_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.006"), Decimal("0.007")
        ),
    ),
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3,), sent=("H", (3,))),
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3, False), sent=("H", (3,)), response_expected=False),
    Call("get_moving_average", FunctionID.GET_MOVING_AVERAGE, (), reply=("H", (3,)), result=3),
    Call(
        "set_info_led_config", FunctionID.SET_INFO_LED_CONFIG, (DEVICE.InfoLEDConfig.SHOW_HEARTBEAT,), sent=("B", (2,))
    ),
    Call(
        "set_info_led_config",
        FunctionID.SET_INFO_LED_CONFIG,
        (DEVICE.InfoLEDConfig.SHOW_HEARTBEAT, False),
        sent=("B", (2,)),
        response_expected=False,
    ),
    Call(
        "get_info_led_config",
        FunctionID.GET_INFO_LED_CONFIG,
        (),
        reply=("B", (2,)),
        result=DEVICE.InfoLEDConfig.SHOW_HEARTBEAT,
    ),
    Call("calibrate", FunctionID.CALIBRATE, (Decimal("0.003"),), sent=("I", (3,))),
    Call("calibrate", FunctionID.CALIBRATE, (Decimal("0.003"), False), sent=("I", (3,)), response_expected=False),
    Call("tare", FunctionID.TARE, ()),
    Call("tare", FunctionID.TARE, (False,), response_expected=False),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.Rate.RATE_80HZ, DEVICE.Gain.GAIN_32X),
        sent=("B B", (1, 2)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.Rate.RATE_80HZ, DEVICE.Gain.GAIN_32X, False),
        sent=("B B", (1, 2)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B", (1, 2)),
        result=GetConfiguration(DEVICE.Rate.RATE_80HZ, DEVICE.Gain.GAIN_32X),
    ),
    Call("get_value", FunctionID.GET_WEIGHT, (0,), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_WEIGHT_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_WEIGHT_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_weight_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_weight_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_weight_callback_configuration", (Decimal("0.003"), True, "o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_weight_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("2147483.648"))),
    ("set_moving_average", (101,)),
    ("set_info_led_config", (12345,)),
    ("calibrate", (Decimal("4294967.296"),)),
    ("set_configuration", (12345, DEVICE.Gain.GAIN_32X)),
    ("set_configuration", (DEVICE.Rate.RATE_80HZ, 12345)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device: BrickletLoadCellV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2104
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Load Cell Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_weight(device: BrickletLoadCellV2, connection: FakeConnection) -> None:
    """The callback WEIGHT is converted to an event."""
    connection.callback(CallbackID.WEIGHT, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.WEIGHT, Decimal("0.003"))]
