"""Tests for the Load Cell Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_load_cell import BrickletLoadCell, GetConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletLoadCell
FunctionID = BrickletLoadCell.FunctionID
CallbackID = BrickletLoadCell.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_WEIGHT": 1,
    "SET_WEIGHT_CALLBACK_PERIOD": 2,
    "GET_WEIGHT_CALLBACK_PERIOD": 3,
    "SET_WEIGHT_CALLBACK_THRESHOLD": 4,
    "GET_WEIGHT_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "SET_MOVING_AVERAGE": 8,
    "GET_MOVING_AVERAGE": 9,
    "LED_ON": 10,
    "LED_OFF": 11,
    "IS_LED_ON": 12,
    "CALIBRATE": 13,
    "TARE": 14,
    "SET_CONFIGURATION": 15,
    "GET_CONFIGURATION": 16,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"WEIGHT": 17, "WEIGHT_REACHED": 18}

CALLS: list[Call] = [
    Call("get_weight", FunctionID.GET_WEIGHT, (), reply=("i", (3,)), result=Decimal("0.003")),
    Call("set_weight_callback_period", FunctionID.SET_WEIGHT_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_weight_callback_period",
        FunctionID.SET_WEIGHT_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_weight_callback_period",
        FunctionID.GET_WEIGHT_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_weight_callback_threshold",
        FunctionID.SET_WEIGHT_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003")),
        sent=("c i i", ("o", 3, 3)),
    ),
    Call(
        "set_weight_callback_threshold",
        FunctionID.SET_WEIGHT_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("c i i", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_weight_callback_threshold",
        FunctionID.GET_WEIGHT_CALLBACK_THRESHOLD,
        (),
        reply=("c i i", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.004"), Decimal("0.005")),
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
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3,), sent=("B", (3,))),
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3, False), sent=("B", (3,)), response_expected=False),
    Call("get_moving_average", FunctionID.GET_MOVING_AVERAGE, (), reply=("B", (3,)), result=3),
    Call("led_on", FunctionID.LED_ON, ()),
    Call("led_on", FunctionID.LED_ON, (False,), response_expected=False),
    Call("led_off", FunctionID.LED_OFF, ()),
    Call("led_off", FunctionID.LED_OFF, (False,), response_expected=False),
    Call("is_led_on", FunctionID.IS_LED_ON, (), reply=("!", (True,)), result=True),
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
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_weight_callback_period", (Decimal("4294967.296"),)),
    ("set_weight_callback_threshold", ("?", Decimal("0.003"), Decimal("0.003"))),
    ("set_weight_callback_threshold", ("o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_weight_callback_threshold", ("o", Decimal("0.003"), Decimal("2147483.648"))),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_moving_average", (41,)),
    ("calibrate", (Decimal("4294967.296"),)),
    ("set_configuration", (12345, DEVICE.Gain.GAIN_32X)),
    ("set_configuration", (DEVICE.Rate.RATE_80HZ, 12345)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 253
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Load Cell Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device, connection):
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_WEIGHT_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_WEIGHT_CALLBACK_THRESHOLD, "c i i", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_WEIGHT_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_WEIGHT_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")
    )


def test_callback_weight(device, connection):
    """The callback WEIGHT is converted to an event."""
    connection.callback(CallbackID.WEIGHT, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.WEIGHT, Decimal("0.003"))]


def test_callback_weight_reached(device, connection):
    """The callback WEIGHT_REACHED is converted to an event."""
    connection.callback(CallbackID.WEIGHT_REACHED, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.WEIGHT_REACHED, Decimal("0.003"))]
