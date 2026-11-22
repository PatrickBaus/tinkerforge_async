"""Tests for the Voltage/Current Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_voltage_current import BrickletVoltageCurrent, GetCalibration, GetConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletVoltageCurrent
FunctionID = BrickletVoltageCurrent.FunctionID
CallbackID = BrickletVoltageCurrent.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_CURRENT": 1,
    "GET_VOLTAGE": 2,
    "GET_POWER": 3,
    "SET_CONFIGURATION": 4,
    "GET_CONFIGURATION": 5,
    "SET_CALIBRATION": 6,
    "GET_CALIBRATION": 7,
    "SET_CURRENT_CALLBACK_PERIOD": 8,
    "GET_CURRENT_CALLBACK_PERIOD": 9,
    "SET_VOLTAGE_CALLBACK_PERIOD": 10,
    "GET_VOLTAGE_CALLBACK_PERIOD": 11,
    "SET_POWER_CALLBACK_PERIOD": 12,
    "GET_POWER_CALLBACK_PERIOD": 13,
    "SET_CURRENT_CALLBACK_THRESHOLD": 14,
    "GET_CURRENT_CALLBACK_THRESHOLD": 15,
    "SET_VOLTAGE_CALLBACK_THRESHOLD": 16,
    "GET_VOLTAGE_CALLBACK_THRESHOLD": 17,
    "SET_POWER_CALLBACK_THRESHOLD": 18,
    "GET_POWER_CALLBACK_THRESHOLD": 19,
    "SET_DEBOUNCE_PERIOD": 20,
    "GET_DEBOUNCE_PERIOD": 21,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "CURRENT": 22,
    "VOLTAGE": 23,
    "POWER": 24,
    "CURRENT_REACHED": 25,
    "VOLTAGE_REACHED": 26,
    "POWER_REACHED": 27,
}

CALLS: list[Call] = [
    Call("get_current", FunctionID.GET_CURRENT, (), reply=("i", (3,)), result=Decimal("0.003")),
    Call("get_voltage", FunctionID.GET_VOLTAGE, (), reply=("i", (3,)), result=Decimal("0.003")),
    Call("get_power", FunctionID.GET_POWER, (), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (
            DEVICE.Averaging.AVERAGING_1024,
            DEVICE.ConversionTime.CONVERSION_TIME_8_244MS,
            DEVICE.ConversionTime.CONVERSION_TIME_8_244MS,
        ),
        sent=("B B B", (7, 7, 7)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (
            DEVICE.Averaging.AVERAGING_1024,
            DEVICE.ConversionTime.CONVERSION_TIME_8_244MS,
            DEVICE.ConversionTime.CONVERSION_TIME_8_244MS,
            False,
        ),
        sent=("B B B", (7, 7, 7)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B B", (7, 7, 7)),
        result=GetConfiguration(
            DEVICE.Averaging.AVERAGING_1024,
            DEVICE.ConversionTime.CONVERSION_TIME_8_244MS,
            DEVICE.ConversionTime.CONVERSION_TIME_8_244MS,
        ),
    ),
    Call("set_calibration", FunctionID.SET_CALIBRATION, (3, 3), sent=("H H", (3, 3))),
    Call("set_calibration", FunctionID.SET_CALIBRATION, (3, 3, False), sent=("H H", (3, 3)), response_expected=False),
    Call("get_calibration", FunctionID.GET_CALIBRATION, (), reply=("H H", (3, 4)), result=GetCalibration(3, 4)),
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
    Call("set_voltage_callback_period", FunctionID.SET_VOLTAGE_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_voltage_callback_period",
        FunctionID.SET_VOLTAGE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_voltage_callback_period",
        FunctionID.GET_VOLTAGE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("set_power_callback_period", FunctionID.SET_POWER_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_power_callback_period",
        FunctionID.SET_POWER_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_power_callback_period",
        FunctionID.GET_POWER_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_current_callback_threshold",
        FunctionID.SET_CURRENT_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003")),
        sent=("c i i", ("o", 3, 3)),
    ),
    Call(
        "set_current_callback_threshold",
        FunctionID.SET_CURRENT_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("c i i", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_current_callback_threshold",
        FunctionID.GET_CURRENT_CALLBACK_THRESHOLD,
        (),
        reply=("c i i", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.004"), Decimal("0.005")),
    ),
    Call(
        "set_voltage_callback_threshold",
        FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003")),
        sent=("c i i", ("o", 3, 3)),
    ),
    Call(
        "set_voltage_callback_threshold",
        FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("c i i", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_voltage_callback_threshold",
        FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD,
        (),
        reply=("c i i", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.004"), Decimal("0.005")),
    ),
    Call(
        "set_power_callback_threshold",
        FunctionID.SET_POWER_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003")),
        sent=("c i i", ("o", 3, 3)),
    ),
    Call(
        "set_power_callback_threshold",
        FunctionID.SET_POWER_CALLBACK_THRESHOLD,
        ("o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("c i i", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_power_callback_threshold",
        FunctionID.GET_POWER_CALLBACK_THRESHOLD,
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
    Call("get_value", FunctionID.GET_CURRENT, (0,), reply=("i", (3,)), result=Decimal("0.003")),
    Call("get_value", FunctionID.GET_VOLTAGE, (1,), reply=("i", (3,)), result=Decimal("0.003")),
    Call("get_value", FunctionID.GET_POWER, (2,), reply=("i", (3,)), result=Decimal("0.003")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    (
        "set_configuration",
        (12345, DEVICE.ConversionTime.CONVERSION_TIME_8_244MS, DEVICE.ConversionTime.CONVERSION_TIME_8_244MS),
    ),
    ("set_configuration", (DEVICE.Averaging.AVERAGING_1024, 12345, DEVICE.ConversionTime.CONVERSION_TIME_8_244MS)),
    ("set_configuration", (DEVICE.Averaging.AVERAGING_1024, DEVICE.ConversionTime.CONVERSION_TIME_8_244MS, 12345)),
    ("set_calibration", (65536, 3)),
    ("set_calibration", (3, 65536)),
    ("set_current_callback_period", (Decimal("4294967.296"),)),
    ("set_voltage_callback_period", (Decimal("4294967.296"),)),
    ("set_power_callback_period", (Decimal("4294967.296"),)),
    ("set_current_callback_threshold", ("?", Decimal("0.003"), Decimal("0.003"))),
    ("set_current_callback_threshold", ("o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_current_callback_threshold", ("o", Decimal("0.003"), Decimal("2147483.648"))),
    ("set_voltage_callback_threshold", ("?", Decimal("0.003"), Decimal("0.003"))),
    ("set_voltage_callback_threshold", ("o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_voltage_callback_threshold", ("o", Decimal("0.003"), Decimal("2147483.648"))),
    ("set_power_callback_threshold", ("?", Decimal("0.003"), Decimal("0.003"))),
    ("set_power_callback_threshold", ("o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_power_callback_threshold", ("o", Decimal("0.003"), Decimal("2147483.648"))),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("get_value", (3,)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 227
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Voltage/Current Bricklet with uid 12345")


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
            request(FunctionID.SET_CURRENT_CALLBACK_THRESHOLD, "c i i", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_CURRENT_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_CURRENT_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")
    )


def test_callback_configuration_of_sid_1(device, connection):
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(1, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_VOLTAGE_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD, "c i i", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_VOLTAGE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")
    )


def test_callback_configuration_of_sid_2(device, connection):
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(2, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_POWER_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_POWER_CALLBACK_THRESHOLD, "c i i", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_POWER_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_POWER_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(2)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")
    )


def test_callback_current(device, connection):
    """The callback CURRENT is converted to an event."""
    connection.callback(CallbackID.CURRENT, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.CURRENT, Decimal("0.003"))]


def test_callback_voltage(device, connection):
    """The callback VOLTAGE is converted to an event."""
    connection.callback(CallbackID.VOLTAGE, "i", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.VOLTAGE, Decimal("0.003"))]


def test_callback_power(device, connection):
    """The callback POWER is converted to an event."""
    connection.callback(CallbackID.POWER, "i", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.POWER, Decimal("0.003"))]


def test_callback_current_reached(device, connection):
    """The callback CURRENT_REACHED is converted to an event."""
    connection.callback(CallbackID.CURRENT_REACHED, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.CURRENT_REACHED, Decimal("0.003"))]


def test_callback_voltage_reached(device, connection):
    """The callback VOLTAGE_REACHED is converted to an event."""
    connection.callback(CallbackID.VOLTAGE_REACHED, "i", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.VOLTAGE_REACHED, Decimal("0.003"))]


def test_callback_power_reached(device, connection):
    """The callback POWER_REACHED is converted to an event."""
    connection.callback(CallbackID.POWER_REACHED, "i", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.POWER_REACHED, Decimal("0.003"))]
