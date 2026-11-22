"""Tests for the Industrial Analog Out Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_analog_out_v2 import (
    BrickletIndustrialAnalogOutV2,
    GetConfiguration,
    GetOutLEDStatusConfig,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialAnalogOutV2
FunctionID = BrickletIndustrialAnalogOutV2.FunctionID
CallbackID = BrickletIndustrialAnalogOutV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_ENABLED": 1,
    "GET_ENABLED": 2,
    "SET_VOLTAGE": 3,
    "GET_VOLTAGE": 4,
    "SET_CURRENT": 5,
    "GET_CURRENT": 6,
    "SET_CONFIGURATION": 7,
    "GET_CONFIGURATION": 8,
    "SET_OUT_LED_CONFIG": 9,
    "GET_OUT_LED_CONFIG": 10,
    "SET_OUT_LED_STATUS_CONFIG": 11,
    "GET_OUT_LED_STATUS_CONFIG": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = [
    Call("set_enabled", FunctionID.SET_ENABLED, (True,), sent=("!", (True,))),
    Call("set_enabled", FunctionID.SET_ENABLED, (True, False), sent=("!", (True,)), response_expected=False),
    Call("get_enabled", FunctionID.GET_ENABLED, (), reply=("!", (True,)), result=True),
    Call("set_voltage", FunctionID.SET_VOLTAGE, (Decimal("0.003"),), sent=("H", (3,))),
    Call("set_voltage", FunctionID.SET_VOLTAGE, (Decimal("0.003"), False), sent=("H", (3,)), response_expected=False),
    Call("get_voltage", FunctionID.GET_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_current", FunctionID.SET_CURRENT, (Decimal("0.000003"),), sent=("H", (3,))),
    Call(
        "set_current", FunctionID.SET_CURRENT, (Decimal("0.000003"), False), sent=("H", (3,)), response_expected=False
    ),
    Call("get_current", FunctionID.GET_CURRENT, (), reply=("H", (3,)), result=Decimal("0.000003")),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.VoltageRange.VOLTAGE_RANGE_0_TO_10V, DEVICE.CurrentRange.CURRENT_RANGE_0_TO_24MA),
        sent=("B B", (1, 2)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.VoltageRange.VOLTAGE_RANGE_0_TO_10V, DEVICE.CurrentRange.CURRENT_RANGE_0_TO_24MA, False),
        sent=("B B", (1, 2)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B", (1, 2)),
        result=GetConfiguration(
            DEVICE.VoltageRange.VOLTAGE_RANGE_0_TO_10V, DEVICE.CurrentRange.CURRENT_RANGE_0_TO_24MA
        ),
    ),
    Call("set_out_led_config", FunctionID.SET_OUT_LED_CONFIG, (DEVICE.OutLEDConfig.SHOW_OUT_STATUS,), sent=("B", (3,))),
    Call(
        "set_out_led_config",
        FunctionID.SET_OUT_LED_CONFIG,
        (DEVICE.OutLEDConfig.SHOW_OUT_STATUS, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_out_led_config",
        FunctionID.GET_OUT_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.OutLEDConfig.SHOW_OUT_STATUS,
    ),
    Call(
        "set_out_led_status_config",
        FunctionID.SET_OUT_LED_STATUS_CONFIG,
        (3, 3, DEVICE.OutLEDStatusConfig.INTENSITY),
        sent=("H H B", (3, 3, 1)),
    ),
    Call(
        "set_out_led_status_config",
        FunctionID.SET_OUT_LED_STATUS_CONFIG,
        (3, 3, DEVICE.OutLEDStatusConfig.INTENSITY, False),
        sent=("H H B", (3, 3, 1)),
        response_expected=False,
    ),
    Call(
        "get_out_led_status_config",
        FunctionID.GET_OUT_LED_STATUS_CONFIG,
        (),
        reply=("H H B", (3, 4, 1)),
        result=GetOutLEDStatusConfig(3, 4, DEVICE.OutLEDStatusConfig.INTENSITY),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_voltage", (Decimal("10.001"),)),
    ("set_current", (Decimal("0.024001"),)),
    ("set_configuration", (12345, DEVICE.CurrentRange.CURRENT_RANGE_0_TO_24MA)),
    ("set_configuration", (DEVICE.VoltageRange.VOLTAGE_RANGE_0_TO_10V, 12345)),
    ("set_out_led_config", (12345,)),
    ("set_out_led_status_config", (24001, 3, DEVICE.OutLEDStatusConfig.INTENSITY)),
    ("set_out_led_status_config", (3, 24001, DEVICE.OutLEDStatusConfig.INTENSITY)),
    ("set_out_led_status_config", (3, 3, 12345)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2116
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Analog Out Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""
