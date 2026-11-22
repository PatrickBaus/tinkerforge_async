"""Tests for the Temperature IR Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_temperature_ir import BrickletTemperatureIR
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletTemperatureIR
FunctionID = BrickletTemperatureIR.FunctionID
CallbackID = BrickletTemperatureIR.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_AMBIENT_TEMPERATURE": 1,
    "GET_OBJECT_TEMPERATURE": 2,
    "SET_EMISSIVITY": 3,
    "GET_EMISSIVITY": 4,
    "SET_AMBIENT_TEMPERATURE_CALLBACK_PERIOD": 5,
    "GET_AMBIENT_TEMPERATURE_CALLBACK_PERIOD": 6,
    "SET_OBJECT_TEMPERATURE_CALLBACK_PERIOD": 7,
    "GET_OBJECT_TEMPERATURE_CALLBACK_PERIOD": 8,
    "SET_AMBIENT_TEMPERATURE_CALLBACK_THRESHOLD": 9,
    "GET_AMBIENT_TEMPERATURE_CALLBACK_THRESHOLD": 10,
    "SET_OBJECT_TEMPERATURE_CALLBACK_THRESHOLD": 11,
    "GET_OBJECT_TEMPERATURE_CALLBACK_THRESHOLD": 12,
    "SET_DEBOUNCE_PERIOD": 13,
    "GET_DEBOUNCE_PERIOD": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "AMBIENT_TEMPERATURE": 15,
    "OBJECT_TEMPERATURE": 16,
    "AMBIENT_TEMPERATURE_REACHED": 17,
    "OBJECT_TEMPERATURE_REACHED": 18,
}

CALLS: list[Call] = [
    Call(
        "get_ambient_temperature", FunctionID.GET_AMBIENT_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("273.45")
    ),
    Call("get_object_temperature", FunctionID.GET_OBJECT_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("273.45")),
    Call(
        "set_emissivity", FunctionID.SET_EMISSIVITY, (Decimal("0.00004577706569008926527809567407"),), sent=("H", (3,))
    ),
    Call(
        "set_emissivity",
        FunctionID.SET_EMISSIVITY,
        (Decimal("0.00004577706569008926527809567407"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call(
        "get_emissivity",
        FunctionID.GET_EMISSIVITY,
        (),
        reply=("H", (3,)),
        result=Decimal("0.00004577706569008926527809567407"),
    ),
    Call(
        "set_ambient_temperature_callback_period",
        FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_ambient_temperature_callback_period",
        FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_ambient_temperature_callback_period",
        FunctionID.GET_AMBIENT_TEMPERATURE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_object_temperature_callback_period",
        FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_object_temperature_callback_period",
        FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_object_temperature_callback_period",
        FunctionID.GET_OBJECT_TEMPERATURE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_ambient_temperature_callback_threshold",
        FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_THRESHOLD,
        ("o", Decimal("273.45"), Decimal("273.45")),
        sent=("c h h", ("o", 3, 3)),
    ),
    Call(
        "set_ambient_temperature_callback_threshold",
        FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_THRESHOLD,
        ("o", Decimal("273.45"), Decimal("273.45"), False),
        sent=("c h h", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_ambient_temperature_callback_threshold",
        FunctionID.GET_AMBIENT_TEMPERATURE_CALLBACK_THRESHOLD,
        (),
        reply=("c h h", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("273.55"), Decimal("273.65")),
    ),
    Call(
        "set_object_temperature_callback_threshold",
        FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_THRESHOLD,
        ("o", Decimal("273.45"), Decimal("273.45")),
        sent=("c h h", ("o", 3, 3)),
    ),
    Call(
        "set_object_temperature_callback_threshold",
        FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_THRESHOLD,
        ("o", Decimal("273.45"), Decimal("273.45"), False),
        sent=("c h h", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_object_temperature_callback_threshold",
        FunctionID.GET_OBJECT_TEMPERATURE_CALLBACK_THRESHOLD,
        (),
        reply=("c h h", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("273.55"), Decimal("273.65")),
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
    Call("get_value", FunctionID.GET_AMBIENT_TEMPERATURE, (0,), reply=("h", (3,)), result=Decimal("273.45")),
    Call("get_value", FunctionID.GET_OBJECT_TEMPERATURE, (1,), reply=("h", (3,)), result=Decimal("273.45")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_emissivity", (Decimal("1.000015259021896696421759365"),)),
    ("set_ambient_temperature_callback_period", (Decimal("4294967.296"),)),
    ("set_object_temperature_callback_period", (Decimal("4294967.296"),)),
    ("set_ambient_temperature_callback_threshold", ("?", Decimal("273.45"), Decimal("273.45"))),
    ("set_ambient_temperature_callback_threshold", ("o", Decimal("3549.95"), Decimal("273.45"))),
    ("set_ambient_temperature_callback_threshold", ("o", Decimal("273.45"), Decimal("3549.95"))),
    ("set_object_temperature_callback_threshold", ("?", Decimal("273.45"), Decimal("273.45"))),
    ("set_object_temperature_callback_threshold", ("o", Decimal("3549.95"), Decimal("273.45"))),
    ("set_object_temperature_callback_threshold", ("o", Decimal("273.45"), Decimal("3549.95"))),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 217
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Temperature IR Bricklet with uid 12345")


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
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("273.45"), Decimal("273.55")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_THRESHOLD, "c h h", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_AMBIENT_TEMPERATURE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_AMBIENT_TEMPERATURE_CALLBACK_THRESHOLD, "c h h", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("273.45"), Decimal("273.55")
    )


def test_callback_configuration_of_sid_1(device, connection):
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(1, 1, True, Threshold.OUTSIDE, Decimal("273.45"), Decimal("273.55")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_THRESHOLD, "c h h", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_OBJECT_TEMPERATURE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_OBJECT_TEMPERATURE_CALLBACK_THRESHOLD, "c h h", "o", 3, 4)
    assert run(device.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("273.45"), Decimal("273.55")
    )


def test_callback_ambient_temperature(device, connection):
    """The callback AMBIENT_TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.AMBIENT_TEMPERATURE, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.AMBIENT_TEMPERATURE, Decimal("273.45"))]


def test_callback_object_temperature(device, connection):
    """The callback OBJECT_TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.OBJECT_TEMPERATURE, "h", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.OBJECT_TEMPERATURE, Decimal("273.45"))]


def test_callback_ambient_temperature_reached(device, connection):
    """The callback AMBIENT_TEMPERATURE_REACHED is converted to an event."""
    connection.callback(CallbackID.AMBIENT_TEMPERATURE_REACHED, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.AMBIENT_TEMPERATURE_REACHED, Decimal("273.45"))]


def test_callback_object_temperature_reached(device, connection):
    """The callback OBJECT_TEMPERATURE_REACHED is converted to an event."""
    connection.callback(CallbackID.OBJECT_TEMPERATURE_REACHED, "h", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.OBJECT_TEMPERATURE_REACHED, Decimal("273.45"))]
