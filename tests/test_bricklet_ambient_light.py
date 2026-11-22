"""Tests for the Ambient Light Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_ambient_light import BrickletAmbientLight
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletAmbientLight
FunctionID = BrickletAmbientLight.FunctionID
CallbackID = BrickletAmbientLight.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_ILLUMINANCE": 1,
    "GET_ANALOG_VALUE": 2,
    "SET_ILLUMINANCE_CALLBACK_PERIOD": 3,
    "GET_ILLUMINANCE_CALLBACK_PERIOD": 4,
    "SET_ANALOG_VALUE_CALLBACK_PERIOD": 5,
    "GET_ANALOG_VALUE_CALLBACK_PERIOD": 6,
    "SET_ILLUMINANCE_CALLBACK_THRESHOLD": 7,
    "GET_ILLUMINANCE_CALLBACK_THRESHOLD": 8,
    "SET_ANALOG_VALUE_CALLBACK_THRESHOLD": 9,
    "GET_ANALOG_VALUE_CALLBACK_THRESHOLD": 10,
    "SET_DEBOUNCE_PERIOD": 11,
    "GET_DEBOUNCE_PERIOD": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "ILLUMINANCE": 13,
    "ANALOG_VALUE": 14,
    "ILLUMINANCE_REACHED": 15,
    "ANALOG_VALUE_REACHED": 16,
}

CALLS: list[Call] = [
    Call("get_illuminance", FunctionID.GET_ILLUMINANCE, (), reply=("H", (3,)), result=Decimal("0.3")),
    Call("get_analog_value", FunctionID.GET_ANALOG_VALUE, (), reply=("H", (3,)), result=3),
    Call(
        "set_illuminance_callback_period",
        FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_illuminance_callback_period",
        FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_illuminance_callback_period",
        FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD,
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
        "set_illuminance_callback_threshold",
        FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD,
        ("o", Decimal("0.3"), Decimal("0.3")),
        sent=("c H H", ("o", 3, 3)),
    ),
    Call(
        "set_illuminance_callback_threshold",
        FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD,
        ("o", Decimal("0.3"), Decimal("0.3"), False),
        sent=("c H H", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_illuminance_callback_threshold",
        FunctionID.GET_ILLUMINANCE_CALLBACK_THRESHOLD,
        (),
        reply=("c H H", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.4"), Decimal("0.5")),
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
    Call("get_value", FunctionID.GET_ILLUMINANCE, (0,), reply=("H", (3,)), result=Decimal("0.3")),
    Call("get_value", FunctionID.GET_ANALOG_VALUE, (1,), reply=("H", (3,)), result=3),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_illuminance_callback_period", (Decimal("4294967.296"),)),
    ("set_analog_value_callback_period", (Decimal("4294967.296"),)),
    ("set_illuminance_callback_threshold", ("?", Decimal("0.3"), Decimal("0.3"))),
    ("set_illuminance_callback_threshold", ("o", Decimal("6553.6"), Decimal("0.3"))),
    ("set_illuminance_callback_threshold", ("o", Decimal("0.3"), Decimal("6553.6"))),
    ("set_analog_value_callback_threshold", ("?", 3, 3)),
    ("set_analog_value_callback_threshold", ("o", 65536, 3)),
    ("set_analog_value_callback_threshold", ("o", 3, 65536)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 21
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Ambient Light Bricklet with uid 12345")


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
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.4")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD, "c H H", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_ILLUMINANCE_CALLBACK_THRESHOLD, "c H H", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.4")
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


def test_callback_illuminance(device, connection):
    """The callback ILLUMINANCE is converted to an event."""
    connection.callback(CallbackID.ILLUMINANCE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.ILLUMINANCE, Decimal("0.3"))]


def test_callback_analog_value(device, connection):
    """The callback ANALOG_VALUE is converted to an event."""
    connection.callback(CallbackID.ANALOG_VALUE, "H", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.ANALOG_VALUE, 3)]


def test_callback_illuminance_reached(device, connection):
    """The callback ILLUMINANCE_REACHED is converted to an event."""
    connection.callback(CallbackID.ILLUMINANCE_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.ILLUMINANCE_REACHED, Decimal("0.3"))]


def test_callback_analog_value_reached(device, connection):
    """The callback ANALOG_VALUE_REACHED is converted to an event."""
    connection.callback(CallbackID.ANALOG_VALUE_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.ANALOG_VALUE_REACHED, 3)]
