"""Tests for the Industrial Dual AC In Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_dual_ac_in import AllValueEvent, BrickletIndustrialDualACIn, ValueEvent
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialDualACIn
FunctionID = BrickletIndustrialDualACIn.FunctionID
CallbackID = BrickletIndustrialDualACIn.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_VALUE": 1,
    "SET_VALUE_CALLBACK_CONFIGURATION": 2,
    "GET_VALUE_CALLBACK_CONFIGURATION": 3,
    "SET_ALL_VALUE_CALLBACK_CONFIGURATION": 4,
    "GET_ALL_VALUE_CALLBACK_CONFIGURATION": 5,
    "SET_CHANNEL_LED_CONFIG": 6,
    "GET_CHANNEL_LED_CONFIG": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"VALUE": 8, "ALL_VALUE": 9}

CALLS: list[Call] = [
    Call(
        "get_value",
        FunctionID.GET_VALUE,
        (),
        reply=("2!", ([i % 2 == 0 for i in range(2)],)),
        result=tuple(i % 2 == 0 for i in range(2)),
    ),
    Call(
        "set_value_callback_configuration",
        FunctionID.SET_VALUE_CALLBACK_CONFIGURATION,
        (DEVICE.Channel.CHANNEL_1, Decimal("0.003"), True),
        sent=("B I !", (1, 3, True)),
    ),
    Call(
        "set_value_callback_configuration",
        FunctionID.SET_VALUE_CALLBACK_CONFIGURATION,
        (DEVICE.Channel.CHANNEL_1, Decimal("0.003"), True, False),
        sent=("B I !", (1, 3, True)),
        response_expected=False,
    ),
    Call(
        "get_value_callback_configuration",
        FunctionID.GET_VALUE_CALLBACK_CONFIGURATION,
        (DEVICE.Channel.CHANNEL_1,),
        sent=("B", (1,)),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_all_value_callback_configuration",
        FunctionID.SET_ALL_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_all_value_callback_configuration",
        FunctionID.SET_ALL_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_all_value_callback_configuration",
        FunctionID.GET_ALL_VALUE_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_channel_led_config",
        FunctionID.SET_CHANNEL_LED_CONFIG,
        (DEVICE.Channel.CHANNEL_1, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS),
        sent=("B B", (1, 3)),
    ),
    Call(
        "set_channel_led_config",
        FunctionID.SET_CHANNEL_LED_CONFIG,
        (DEVICE.Channel.CHANNEL_1, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS, False),
        sent=("B B", (1, 3)),
        response_expected=False,
    ),
    Call(
        "get_channel_led_config",
        FunctionID.GET_CHANNEL_LED_CONFIG,
        (DEVICE.Channel.CHANNEL_1,),
        sent=("B", (1,)),
        reply=("B", (3,)),
        result=DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALL_VALUE_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALL_VALUE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_value_callback_configuration", (12345, Decimal("0.003"), True)),
    ("set_value_callback_configuration", (DEVICE.Channel.CHANNEL_1, Decimal("4294967.296"), True)),
    ("get_value_callback_configuration", (12345,)),
    ("set_all_value_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_channel_led_config", (12345, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS)),
    ("set_channel_led_config", (DEVICE.Channel.CHANNEL_1, 12345)),
    ("get_channel_led_config", (12345,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device: BrickletIndustrialDualACIn) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2174
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Dual AC In Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_value(device: BrickletIndustrialDualACIn, connection: FakeConnection) -> None:
    """The callback VALUE is converted to an event."""
    connection.callback(CallbackID.VALUE, "B ! !", *(1, True, True))
    assert summary(read_events(device)) == [(0, CallbackID.VALUE, ValueEvent(DEVICE.Channel.CHANNEL_1, True, True))]


def test_callback_all_value(device: BrickletIndustrialDualACIn, connection: FakeConnection) -> None:
    """The callback ALL_VALUE is converted to an event."""
    connection.callback(
        CallbackID.ALL_VALUE, "2! 2!", *([i % 2 == 0 for i in range(2)], [i % 2 == 0 for i in range(2)])
    )
    assert summary(read_events(device)) == [
        (
            1,
            CallbackID.ALL_VALUE,
            AllValueEvent(tuple(i % 2 == 0 for i in range(2)), tuple(i % 2 == 0 for i in range(2))),
        )
    ]
