"""Tests for the Voltage/Current Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_voltage_current_v2 import BrickletVoltageCurrentV2, GetCalibration, GetConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletVoltageCurrentV2
FunctionID = BrickletVoltageCurrentV2.FunctionID
CallbackID = BrickletVoltageCurrentV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_CURRENT": 1,
    "SET_CURRENT_CALLBACK_CONFIGURATION": 2,
    "GET_CURRENT_CALLBACK_CONFIGURATION": 3,
    "GET_VOLTAGE": 5,
    "SET_VOLTAGE_CALLBACK_CONFIGURATION": 6,
    "GET_VOLTAGE_CALLBACK_CONFIGURATION": 7,
    "GET_POWER": 9,
    "SET_POWER_CALLBACK_CONFIGURATION": 10,
    "GET_POWER_CALLBACK_CONFIGURATION": 11,
    "SET_CONFIGURATION": 13,
    "GET_CONFIGURATION": 14,
    "SET_CALIBRATION": 15,
    "GET_CALIBRATION": 16,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"CURRENT": 4, "VOLTAGE": 8, "POWER": 12}

CALLS: list[Call] = [
    Call("get_current", FunctionID.GET_CURRENT, (), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_current_callback_configuration",
        FunctionID.SET_CURRENT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_current_callback_configuration",
        FunctionID.SET_CURRENT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_current_callback_configuration",
        FunctionID.GET_CURRENT_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.006"), Decimal("0.007")
        ),
    ),
    Call("get_voltage", FunctionID.GET_VOLTAGE, (), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_voltage_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_voltage_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_voltage_callback_configuration",
        FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.006"), Decimal("0.007")
        ),
    ),
    Call("get_power", FunctionID.GET_POWER, (), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_power_callback_configuration",
        FunctionID.SET_POWER_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_power_callback_configuration",
        FunctionID.SET_POWER_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_power_callback_configuration",
        FunctionID.GET_POWER_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.006"), Decimal("0.007")
        ),
    ),
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
    Call("set_calibration", FunctionID.SET_CALIBRATION, (3, 3, 3, 3), sent=("H H H H", (3, 3, 3, 3))),
    Call(
        "set_calibration",
        FunctionID.SET_CALIBRATION,
        (3, 3, 3, 3, False),
        sent=("H H H H", (3, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_calibration",
        FunctionID.GET_CALIBRATION,
        (),
        reply=("H H H H", (3, 4, 5, 6)),
        result=GetCalibration(3, 4, 5, 6),
    ),
    Call("get_value", FunctionID.GET_CURRENT, (0,), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_CURRENT_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_CURRENT_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
    ),
    Call("get_value", FunctionID.GET_VOLTAGE, (1,), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (1, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
    ),
    Call("get_value", FunctionID.GET_POWER, (2,), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_POWER_CALLBACK_CONFIGURATION,
        (2, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_POWER_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_current_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_current_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_current_callback_configuration", (Decimal("0.003"), True, "o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_current_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("2147483.648"))),
    ("set_voltage_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_voltage_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_voltage_callback_configuration", (Decimal("0.003"), True, "o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_voltage_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("2147483.648"))),
    ("set_power_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_power_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_power_callback_configuration", (Decimal("0.003"), True, "o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_power_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("2147483.648"))),
    (
        "set_configuration",
        (12345, DEVICE.ConversionTime.CONVERSION_TIME_8_244MS, DEVICE.ConversionTime.CONVERSION_TIME_8_244MS),
    ),
    ("set_configuration", (DEVICE.Averaging.AVERAGING_1024, 12345, DEVICE.ConversionTime.CONVERSION_TIME_8_244MS)),
    ("set_configuration", (DEVICE.Averaging.AVERAGING_1024, DEVICE.ConversionTime.CONVERSION_TIME_8_244MS, 12345)),
    ("set_calibration", (65536, 3, 3, 3)),
    ("set_calibration", (3, 65536, 3, 3)),
    ("set_calibration", (3, 3, 65536, 3)),
    ("set_calibration", (3, 3, 3, 65536)),
    ("get_value", (3,)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device: BrickletVoltageCurrentV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2105
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Voltage/Current Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_current(device: BrickletVoltageCurrentV2, connection: FakeConnection) -> None:
    """The callback CURRENT is converted to an event."""
    connection.callback(CallbackID.CURRENT, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.CURRENT, Decimal("0.003"))]


def test_callback_voltage(device: BrickletVoltageCurrentV2, connection: FakeConnection) -> None:
    """The callback VOLTAGE is converted to an event."""
    connection.callback(CallbackID.VOLTAGE, "i", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.VOLTAGE, Decimal("0.003"))]


def test_callback_power(device: BrickletVoltageCurrentV2, connection: FakeConnection) -> None:
    """The callback POWER is converted to an event."""
    connection.callback(CallbackID.POWER, "i", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.POWER, Decimal("0.003"))]
