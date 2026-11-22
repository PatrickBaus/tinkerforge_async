"""Tests for the XMC1400 Breakout Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_xmc1400_breakout import BrickletXMC1400Breakout
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletXMC1400Breakout
FunctionID = BrickletXMC1400Breakout.FunctionID
CallbackID = BrickletXMC1400Breakout.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_GPIO_CONFIG": 1,
    "GET_GPIO_INPUT": 2,
    "SET_ADC_CHANNEL_CONFIG": 3,
    "GET_ADC_CHANNEL_CONFIG": 4,
    "GET_ADC_CHANNEL_VALUE": 5,
    "GET_ADC_VALUES": 6,
    "SET_ADC_VALUES_CALLBACK_CONFIGURATION": 7,
    "GET_ADC_VALUES_CALLBACK_CONFIGURATION": 8,
    "GET_COUNT": 10,
    "SET_COUNT_CALLBACK_CONFIGURATION": 11,
    "GET_COUNT_CALLBACK_CONFIGURATION": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"ADC_VALUES": 9, "COUNT": 13}

CALLS: list[Call] = [
    Call(
        "set_gpio_config",
        FunctionID.SET_GPIO_CONFIG,
        (3, 3, DEVICE.GPIOMode.OUTPUT_OPEN_DRAIN, DEVICE.GPIOInputHysteresis.LARGE, True),
        sent=("B B B B !", (3, 3, 9, 4, True)),
    ),
    Call(
        "set_gpio_config",
        FunctionID.SET_GPIO_CONFIG,
        (3, 3, DEVICE.GPIOMode.OUTPUT_OPEN_DRAIN, DEVICE.GPIOInputHysteresis.LARGE, True, False),
        sent=("B B B B !", (3, 3, 9, 4, True)),
        response_expected=False,
    ),
    Call("get_gpio_input", FunctionID.GET_GPIO_INPUT, (3, 3), sent=("B B", (3, 3)), reply=("!", (True,)), result=True),
    Call("set_adc_channel_config", FunctionID.SET_ADC_CHANNEL_CONFIG, (3, True), sent=("B !", (3, True))),
    Call(
        "set_adc_channel_config",
        FunctionID.SET_ADC_CHANNEL_CONFIG,
        (3, True, False),
        sent=("B !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_adc_channel_config",
        FunctionID.GET_ADC_CHANNEL_CONFIG,
        (3,),
        sent=("B", (3,)),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "get_adc_channel_value", FunctionID.GET_ADC_CHANNEL_VALUE, (3,), sent=("B", (3,)), reply=("H", (3,)), result=3
    ),
    Call("get_adc_values", FunctionID.GET_ADC_VALUES, (), reply=("8H", ([3] * 8,)), result=(3,) * 8),
    Call(
        "set_adc_values_callback_configuration",
        FunctionID.SET_ADC_VALUES_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_adc_values_callback_configuration",
        FunctionID.SET_ADC_VALUES_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_adc_values_callback_configuration",
        FunctionID.GET_ADC_VALUES_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("get_count", FunctionID.GET_COUNT, (), reply=("I", (3,)), result=3),
    Call(
        "set_count_callback_configuration",
        FunctionID.SET_COUNT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3),
        sent=("I ! c I I", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_count_callback_configuration",
        FunctionID.SET_COUNT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3, False),
        sent=("I ! c I I", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_count_callback_configuration",
        FunctionID.GET_COUNT_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c I I", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call("get_value", FunctionID.GET_ADC_VALUES, (0,), reply=("8H", ([3] * 8,)), result=(3,) * 8),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ADC_VALUES_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ADC_VALUES_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call("get_value", FunctionID.GET_COUNT, (1,), reply=("I", (3,)), result=3),
    Call(
        "set_callback_configuration",
        FunctionID.SET_COUNT_CALLBACK_CONFIGURATION,
        (1, 1, True, Threshold.OUTSIDE, 3, 4),
        sent=("I ! c I I", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_COUNT_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c I I", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_gpio_config", (5, 3, DEVICE.GPIOMode.OUTPUT_OPEN_DRAIN, DEVICE.GPIOInputHysteresis.LARGE, True)),
    ("set_gpio_config", (3, 256, DEVICE.GPIOMode.OUTPUT_OPEN_DRAIN, DEVICE.GPIOInputHysteresis.LARGE, True)),
    ("set_gpio_config", (3, 3, 12345, DEVICE.GPIOInputHysteresis.LARGE, True)),
    ("set_gpio_config", (3, 3, DEVICE.GPIOMode.OUTPUT_OPEN_DRAIN, 12345, True)),
    ("get_gpio_input", (5, 3)),
    ("get_gpio_input", (3, 256)),
    ("set_adc_channel_config", (8, True)),
    ("get_adc_channel_config", (8,)),
    ("get_adc_channel_value", (8,)),
    ("set_adc_values_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_count_callback_configuration", (Decimal("4294967.296"), True, "o", 3, 3)),
    ("set_count_callback_configuration", (Decimal("0.003"), True, "?", 3, 3)),
    ("set_count_callback_configuration", (Decimal("0.003"), True, "o", 4294967296, 3)),
    ("set_count_callback_configuration", (Decimal("0.003"), True, "o", 3, 4294967296)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 279
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("XMC1400 Breakout Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_adc_values(device, connection):
    """The callback ADC_VALUES is converted to an event."""
    connection.callback(CallbackID.ADC_VALUES, "8H", *([3] * 8,))
    assert summary(read_events(device)) == [(0, CallbackID.ADC_VALUES, (3,) * 8)]


def test_callback_count(device, connection):
    """The callback COUNT is converted to an event."""
    connection.callback(CallbackID.COUNT, "I", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.COUNT, 3)]
