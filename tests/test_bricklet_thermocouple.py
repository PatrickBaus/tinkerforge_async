"""Tests for the Thermocouple Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_thermocouple import BrickletThermocouple, GetConfiguration, GetErrorState
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletThermocouple
FunctionID = BrickletThermocouple.FunctionID
CallbackID = BrickletThermocouple.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_TEMPERATURE": 1,
    "SET_TEMPERATURE_CALLBACK_PERIOD": 2,
    "GET_TEMPERATURE_CALLBACK_PERIOD": 3,
    "SET_TEMPERATURE_CALLBACK_THRESHOLD": 4,
    "GET_TEMPERATURE_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "SET_CONFIGURATION": 10,
    "GET_CONFIGURATION": 11,
    "GET_ERROR_STATE": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"TEMPERATURE": 8, "TEMPERATURE_REACHED": 9, "ERROR_STATE": 13}

CALLS: list[Call] = [
    Call("get_temperature", FunctionID.GET_TEMPERATURE, (), reply=("i", (3,)), result=Decimal("273.18")),
    Call(
        "set_temperature_callback_period",
        FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_temperature_callback_period",
        FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_temperature_callback_period",
        FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_temperature_callback_threshold",
        FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
        ("o", Decimal("273.18"), Decimal("273.18")),
        sent=("c i i", ("o", 3, 3)),
    ),
    Call(
        "set_temperature_callback_threshold",
        FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
        ("o", Decimal("273.18"), Decimal("273.18"), False),
        sent=("c i i", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_temperature_callback_threshold",
        FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD,
        (),
        reply=("c i i", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("273.19"), Decimal("273.20")),
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
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.Averaging.AVERAGING_16, DEVICE.SensorType.TYPE_G32, DEVICE.FilterOption.FILTER_OPTION_60HZ),
        sent=("B B B", (16, 9, 1)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.Averaging.AVERAGING_16, DEVICE.SensorType.TYPE_G32, DEVICE.FilterOption.FILTER_OPTION_60HZ, False),
        sent=("B B B", (16, 9, 1)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B B", (16, 9, 1)),
        result=GetConfiguration(
            DEVICE.Averaging.AVERAGING_16, DEVICE.SensorType.TYPE_G32, DEVICE.FilterOption.FILTER_OPTION_60HZ
        ),
    ),
    Call(
        "get_error_state", FunctionID.GET_ERROR_STATE, (), reply=("! !", (True, True)), result=GetErrorState(True, True)
    ),
    Call("get_value", FunctionID.GET_TEMPERATURE, (0,), reply=("i", (3,)), result=Decimal("273.18")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_temperature_callback_period", (Decimal("4294967.296"),)),
    ("set_temperature_callback_threshold", ("?", Decimal("273.18"), Decimal("273.18"))),
    ("set_temperature_callback_threshold", ("o", Decimal("21475109.63"), Decimal("273.18"))),
    ("set_temperature_callback_threshold", ("o", Decimal("273.18"), Decimal("21475109.63"))),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_configuration", (12345, DEVICE.SensorType.TYPE_G32, DEVICE.FilterOption.FILTER_OPTION_60HZ)),
    ("set_configuration", (DEVICE.Averaging.AVERAGING_16, 12345, DEVICE.FilterOption.FILTER_OPTION_60HZ)),
    ("set_configuration", (DEVICE.Averaging.AVERAGING_16, DEVICE.SensorType.TYPE_G32, 12345)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 266
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Thermocouple Bricklet with uid 12345")


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
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("273.18"), Decimal("273.19")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD, "c i i", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("273.18"), Decimal("273.19")
    )


def test_callback_temperature(device, connection):
    """The callback TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.TEMPERATURE, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.TEMPERATURE, Decimal("273.18"))]


def test_callback_temperature_reached(device, connection):
    """The callback TEMPERATURE_REACHED is converted to an event."""
    connection.callback(CallbackID.TEMPERATURE_REACHED, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.TEMPERATURE_REACHED, Decimal("273.18"))]


def test_callback_error_state(device, connection):
    """The callback ERROR_STATE is converted to an event."""
    connection.callback(CallbackID.ERROR_STATE, "! !", *(True, True))
    assert summary(read_events(device)) == [(1, CallbackID.ERROR_STATE, GetErrorState(True, True))]
