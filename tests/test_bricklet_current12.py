"""Tests for the Current12 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_current12 import BrickletCurrent12
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletCurrent12
FunctionID = BrickletCurrent12.FunctionID
CallbackID = BrickletCurrent12.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_CURRENT": 1,
    "CALIBRATE": 2,
    "IS_OVER_CURRENT": 3,
    "GET_ANALOG_VALUE": 4,
    "SET_CURRENT_CALLBACK_PERIOD": 5,
    "GET_CURRENT_CALLBACK_PERIOD": 6,
    "SET_ANALOG_VALUE_CALLBACK_PERIOD": 7,
    "GET_ANALOG_VALUE_CALLBACK_PERIOD": 8,
    "SET_CURRENT_CALLBACK_THRESHOLD": 9,
    "GET_CURRENT_CALLBACK_THRESHOLD": 10,
    "SET_ANALOG_VALUE_CALLBACK_THRESHOLD": 11,
    "GET_ANALOG_VALUE_CALLBACK_THRESHOLD": 12,
    "SET_DEBOUNCE_PERIOD": 13,
    "GET_DEBOUNCE_PERIOD": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "CURRENT": 15,
    "ANALOG_VALUE": 16,
    "CURRENT_REACHED": 17,
    "ANALOG_VALUE_REACHED": 18,
    "OVER_CURRENT": 19,
}

CALLS: list[Call] = [
    Call("get_current", FunctionID.GET_CURRENT, (), reply=("h", (3,)), result=Decimal("0.003")),
    Call("calibrate", FunctionID.CALIBRATE, ()),
    Call("calibrate", FunctionID.CALIBRATE, (False,), response_expected=False),
    Call("is_over_current", FunctionID.IS_OVER_CURRENT, (), reply=("!", (True,)), result=True),
    Call("get_analog_value", FunctionID.GET_ANALOG_VALUE, (), reply=("H", (3,)), result=3),
    Call("set_current_callback_period", FunctionID.SET_CURRENT_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_current_callback_period",
        FunctionID.SET_CURRENT_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_current_callback_period",
        FunctionID.GET_CURRENT_CALLBACK_PERIOD,
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
        "set_current_callback_threshold",
        FunctionID.SET_CURRENT_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003")),
        sent=("c h h", ("o", 3, 3)),
    ),
    Call(
        "set_current_callback_threshold",
        FunctionID.SET_CURRENT_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("c h h", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_current_callback_threshold",
        FunctionID.GET_CURRENT_CALLBACK_THRESHOLD,
        (),
        reply=("c h h", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.004"), Decimal("0.005")),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        ("o", 3, 3),
        sent=("c H H", ("o", 3, 3)),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        ("o", 3, 3, False),
        sent=("c H H", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_analog_value_callback_threshold",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        (),
        reply=("c H H", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("4"), Decimal("5")),
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
    Call("get_value", FunctionID.GET_CURRENT, (0,), reply=("h", (3,)), result=Decimal("0.003")),
    Call("get_value", FunctionID.GET_ANALOG_VALUE, (1,), reply=("H", (3,)), result=3),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_current_callback_period", (Decimal("4294967.296"),)),
    ("set_analog_value_callback_period", (Decimal("4294967.296"),)),
    ("set_current_callback_threshold", ("?", Decimal("0.003"), Decimal("0.003"))),
    ("set_current_callback_threshold", ("o", Decimal("32.768"), Decimal("0.003"))),
    ("set_current_callback_threshold", ("o", Decimal("0.003"), Decimal("32.768"))),
    ("set_analog_value_callback_threshold", ("?", 3, 3)),
    ("set_analog_value_callback_threshold", ("o", 65536, 3)),
    ("set_analog_value_callback_threshold", ("o", 3, 65536)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("get_value", (3,)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 23
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Current12 Bricklet with uid 12345")


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
            request(FunctionID.SET_CURRENT_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_CURRENT_CALLBACK_THRESHOLD, "c h h", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_CURRENT_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_CURRENT_CALLBACK_THRESHOLD, "c h h", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")
    )


def test_callback_configuration_of_sid_1(device, connection):
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(1, 1, True, Threshold.OUTSIDE, 3, 4))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD, "c H H", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_ANALOG_VALUE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD, "c H H", "o", 3, 4)
    assert run(device.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")
    )


def test_callback_current(device, connection):
    """The callback CURRENT is converted to an event."""
    connection.callback(CallbackID.CURRENT, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.CURRENT, Decimal("0.003"))]


def test_callback_analog_value(device, connection):
    """The callback ANALOG_VALUE is converted to an event."""
    connection.callback(CallbackID.ANALOG_VALUE, "H", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.ANALOG_VALUE, 3)]


def test_callback_current_reached(device, connection):
    """The callback CURRENT_REACHED is converted to an event."""
    connection.callback(CallbackID.CURRENT_REACHED, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.CURRENT_REACHED, Decimal("0.003"))]


def test_callback_analog_value_reached(device, connection):
    """The callback ANALOG_VALUE_REACHED is converted to an event."""
    connection.callback(CallbackID.ANALOG_VALUE_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.ANALOG_VALUE_REACHED, 3)]


def test_callback_over_current(device, connection):
    """The callback OVER_CURRENT is converted to an event."""
    connection.callback(CallbackID.OVER_CURRENT)
    assert summary(read_events(device)) == [(2, CallbackID.OVER_CURRENT, None)]
