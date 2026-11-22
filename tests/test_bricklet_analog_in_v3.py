"""Tests for the Analog In Bricklet 3.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_analog_in_v3 import BrickletAnalogInV3, GetCalibration
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletAnalogInV3
FunctionID = BrickletAnalogInV3.FunctionID
CallbackID = BrickletAnalogInV3.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_VOLTAGE": 1,
    "SET_VOLTAGE_CALLBACK_CONFIGURATION": 2,
    "GET_VOLTAGE_CALLBACK_CONFIGURATION": 3,
    "SET_OVERSAMPLING": 5,
    "GET_OVERSAMPLING": 6,
    "SET_CALIBRATION": 7,
    "GET_CALIBRATION": 8,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"VOLTAGE": 4}

CALLS: list[Call] = [
    Call("get_voltage", FunctionID.GET_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "set_voltage_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003")),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_voltage_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_voltage_callback_configuration",
        FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c H H", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.006"), Decimal("0.007")
        ),
    ),
    Call("set_oversampling", FunctionID.SET_OVERSAMPLING, (DEVICE.Oversampling.OVERSAMPLING_16384,), sent=("B", (9,))),
    Call(
        "set_oversampling",
        FunctionID.SET_OVERSAMPLING,
        (DEVICE.Oversampling.OVERSAMPLING_16384, False),
        sent=("B", (9,)),
        response_expected=False,
    ),
    Call(
        "get_oversampling",
        FunctionID.GET_OVERSAMPLING,
        (),
        reply=("B", (9,)),
        result=DEVICE.Oversampling.OVERSAMPLING_16384,
    ),
    Call("set_calibration", FunctionID.SET_CALIBRATION, (Decimal("0.003"), 3, 3), sent=("h H H", (3, 3, 3))),
    Call(
        "set_calibration",
        FunctionID.SET_CALIBRATION,
        (Decimal("0.003"), 3, 3, False),
        sent=("h H H", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_calibration",
        FunctionID.GET_CALIBRATION,
        (),
        reply=("h H H", (3, 4, 5)),
        result=GetCalibration(Decimal("0.003"), 4, 5),
    ),
    Call("get_value", FunctionID.GET_VOLTAGE, (0,), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
        sent=("I ! c H H", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c H H", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_voltage_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_voltage_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_voltage_callback_configuration", (Decimal("0.003"), True, "o", Decimal("65.536"), Decimal("0.003"))),
    ("set_voltage_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("65.536"))),
    ("set_oversampling", (12345,)),
    ("set_calibration", (Decimal("32.768"), 3, 3)),
    ("set_calibration", (Decimal("0.003"), 65536, 3)),
    ("set_calibration", (Decimal("0.003"), 3, 65536)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 295
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Analog In Bricklet 3.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_voltage(device, connection):
    """The callback VOLTAGE is converted to an event."""
    connection.callback(CallbackID.VOLTAGE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.VOLTAGE, Decimal("0.003"))]
