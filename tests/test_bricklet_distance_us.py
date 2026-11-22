"""Tests for the Distance US Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_distance_us import BrickletDistanceUS
from tinkerforge_async.devices import BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletDistanceUS
FunctionID = BrickletDistanceUS.FunctionID
CallbackID = BrickletDistanceUS.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_DISTANCE_VALUE": 1,
    "SET_DISTANCE_CALLBACK_PERIOD": 2,
    "GET_DISTANCE_CALLBACK_PERIOD": 3,
    "SET_DISTANCE_CALLBACK_THRESHOLD": 4,
    "GET_DISTANCE_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "SET_MOVING_AVERAGE": 10,
    "GET_MOVING_AVERAGE": 11,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DISTANCE": 8, "DISTANCE_REACHED": 9}

CALLS: list[Call] = [
    Call("get_distance_value", FunctionID.GET_DISTANCE_VALUE, (), reply=("H", (3,)), result=3),
    Call(
        "set_distance_callback_period", FunctionID.SET_DISTANCE_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))
    ),
    Call(
        "set_distance_callback_period",
        FunctionID.SET_DISTANCE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_distance_callback_period",
        FunctionID.GET_DISTANCE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_distance_callback_threshold",
        FunctionID.SET_DISTANCE_CALLBACK_THRESHOLD,
        ("o", 3, 3),
        sent=("c H H", ("o", 3, 3)),
    ),
    Call(
        "set_distance_callback_threshold",
        FunctionID.SET_DISTANCE_CALLBACK_THRESHOLD,
        ("o", 3, 3, False),
        sent=("c H H", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_distance_callback_threshold",
        FunctionID.GET_DISTANCE_CALLBACK_THRESHOLD,
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
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3,), sent=("B", (3,))),
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3, False), sent=("B", (3,)), response_expected=False),
    Call("get_moving_average", FunctionID.GET_MOVING_AVERAGE, (), reply=("B", (3,)), result=3),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_distance_callback_period", (Decimal("4294967.296"),)),
    ("set_distance_callback_threshold", ("?", 3, 3)),
    ("set_distance_callback_threshold", ("o", 4096, 3)),
    ("set_distance_callback_threshold", ("o", 3, 4096)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_moving_average", (101,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 229
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Distance US Bricklet with uid 12345")


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
    connection.callback(CallbackID.DISTANCE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.DISTANCE, 3)]


def test_callback_distance_reached(device, connection):
    """The callback DISTANCE_REACHED is converted to an event."""
    connection.callback(CallbackID.DISTANCE_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.DISTANCE_REACHED, 3)]
