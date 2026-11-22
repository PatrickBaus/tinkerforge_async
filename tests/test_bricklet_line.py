"""Tests for the Line Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_line import BrickletLine
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletLine
FunctionID = BrickletLine.FunctionID
CallbackID = BrickletLine.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_REFLECTIVITY": 1,
    "SET_REFLECTIVITY_CALLBACK_PERIOD": 2,
    "GET_REFLECTIVITY_CALLBACK_PERIOD": 3,
    "SET_REFLECTIVITY_CALLBACK_THRESHOLD": 4,
    "GET_REFLECTIVITY_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"REFLECTIVITY": 8, "REFLECTIVITY_REACHED": 9}

CALLS: list[Call] = [
    Call("get_reflectivity", FunctionID.GET_REFLECTIVITY, (), reply=("H", (3,)), result=3),
    Call(
        "set_reflectivity_callback_period",
        FunctionID.SET_REFLECTIVITY_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_reflectivity_callback_period",
        FunctionID.SET_REFLECTIVITY_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_reflectivity_callback_period",
        FunctionID.GET_REFLECTIVITY_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_reflectivity_callback_threshold",
        FunctionID.SET_REFLECTIVITY_CALLBACK_THRESHOLD,
        ("o", 3, 3),
        sent=("c H H", ("o", 3, 3)),
    ),
    Call(
        "set_reflectivity_callback_threshold",
        FunctionID.SET_REFLECTIVITY_CALLBACK_THRESHOLD,
        ("o", 3, 3, False),
        sent=("c H H", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_reflectivity_callback_threshold",
        FunctionID.GET_REFLECTIVITY_CALLBACK_THRESHOLD,
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
    Call("get_value", FunctionID.GET_REFLECTIVITY, (0,), reply=("H", (3,)), result=3),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_reflectivity_callback_period", (Decimal("4294967.296"),)),
    ("set_reflectivity_callback_threshold", ("?", 3, 3)),
    ("set_reflectivity_callback_threshold", ("o", 65536, 3)),
    ("set_reflectivity_callback_threshold", ("o", 3, 65536)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 241
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Line Bricklet with uid 12345")


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
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, 3, 4))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_REFLECTIVITY_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_REFLECTIVITY_CALLBACK_THRESHOLD, "c H H", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_REFLECTIVITY_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_REFLECTIVITY_CALLBACK_THRESHOLD, "c H H", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")
    )


def test_callback_reflectivity(device, connection):
    """The callback REFLECTIVITY is converted to an event."""
    connection.callback(CallbackID.REFLECTIVITY, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.REFLECTIVITY, 3)]


def test_callback_reflectivity_reached(device, connection):
    """The callback REFLECTIVITY_REACHED is converted to an event."""
    connection.callback(CallbackID.REFLECTIVITY_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.REFLECTIVITY_REACHED, 3)]
