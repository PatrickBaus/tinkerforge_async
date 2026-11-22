"""Tests for the Industrial Counter Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_counter import (
    BrickletIndustrialCounter,
    GetAllSignalData,
    GetCounterConfiguration,
    GetSignalData,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialCounter
FunctionID = BrickletIndustrialCounter.FunctionID
CallbackID = BrickletIndustrialCounter.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_COUNTER": 1,
    "GET_ALL_COUNTER": 2,
    "SET_COUNTER": 3,
    "SET_ALL_COUNTER": 4,
    "GET_SIGNAL_DATA": 5,
    "GET_ALL_SIGNAL_DATA": 6,
    "SET_COUNTER_ACTIVE": 7,
    "SET_ALL_COUNTER_ACTIVE": 8,
    "GET_COUNTER_ACTIVE": 9,
    "GET_ALL_COUNTER_ACTIVE": 10,
    "SET_COUNTER_CONFIGURATION": 11,
    "GET_COUNTER_CONFIGURATION": 12,
    "SET_ALL_COUNTER_CALLBACK_CONFIGURATION": 13,
    "GET_ALL_COUNTER_CALLBACK_CONFIGURATION": 14,
    "SET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION": 15,
    "GET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION": 16,
    "SET_CHANNEL_LED_CONFIG": 17,
    "GET_CHANNEL_LED_CONFIG": 18,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"ALL_COUNTER": 19, "ALL_SIGNAL_DATA": 20}

CALLS: list[Call] = [
    Call(
        "get_counter",
        FunctionID.GET_COUNTER,
        (DEVICE.Channel.CHANNEL_3,),
        sent=("B", (3,)),
        reply=("q", (3,)),
        result=3,
    ),
    Call("get_all_counter", FunctionID.GET_ALL_COUNTER, (), reply=("4q", ([3] * 4,)), result=(3,) * 4),
    Call("set_counter", FunctionID.SET_COUNTER, (DEVICE.Channel.CHANNEL_3, 3), sent=("B q", (3, 3))),
    Call(
        "set_counter",
        FunctionID.SET_COUNTER,
        (DEVICE.Channel.CHANNEL_3, 3, False),
        sent=("B q", (3, 3)),
        response_expected=False,
    ),
    Call("set_all_counter", FunctionID.SET_ALL_COUNTER, ([3] * 4,), sent=("4q", ([3] * 4,))),
    Call(
        "set_all_counter",
        FunctionID.SET_ALL_COUNTER,
        ([3] * 4, False),
        sent=("4q", ([3] * 4,)),
        response_expected=False,
    ),
    Call(
        "get_signal_data",
        FunctionID.GET_SIGNAL_DATA,
        (DEVICE.Channel.CHANNEL_3,),
        sent=("B", (3,)),
        reply=("H Q I !", (3, 4, 5, True)),
        result=GetSignalData(Decimal("0.03"), Decimal("4E-9"), Decimal("0.005"), True),
    ),
    Call(
        "get_all_signal_data",
        FunctionID.GET_ALL_SIGNAL_DATA,
        (),
        reply=("4H 4Q 4I 4!", ([3] * 4, [4] * 4, [5] * 4, [i % 2 == 0 for i in range(4)])),
        result=GetAllSignalData(
            (Decimal("0.03"),) * 4, (Decimal("4E-9"),) * 4, (Decimal("0.005"),) * 4, tuple(i % 2 == 0 for i in range(4))
        ),
    ),
    Call(
        "set_counter_active", FunctionID.SET_COUNTER_ACTIVE, (DEVICE.Channel.CHANNEL_3, True), sent=("B !", (3, True))
    ),
    Call(
        "set_counter_active",
        FunctionID.SET_COUNTER_ACTIVE,
        (DEVICE.Channel.CHANNEL_3, True, False),
        sent=("B !", (3, True)),
        response_expected=False,
    ),
    Call(
        "set_all_counter_active",
        FunctionID.SET_ALL_COUNTER_ACTIVE,
        ([i % 2 == 0 for i in range(4)],),
        sent=("4!", ([i % 2 == 0 for i in range(4)],)),
    ),
    Call(
        "set_all_counter_active",
        FunctionID.SET_ALL_COUNTER_ACTIVE,
        ([i % 2 == 0 for i in range(4)], False),
        sent=("4!", ([i % 2 == 0 for i in range(4)],)),
        response_expected=False,
    ),
    Call(
        "get_counter_active",
        FunctionID.GET_COUNTER_ACTIVE,
        (DEVICE.Channel.CHANNEL_3,),
        sent=("B", (3,)),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "get_all_counter_active",
        FunctionID.GET_ALL_COUNTER_ACTIVE,
        (),
        reply=("4!", ([i % 2 == 0 for i in range(4)],)),
        result=tuple(i % 2 == 0 for i in range(4)),
    ),
    Call(
        "set_counter_configuration",
        FunctionID.SET_COUNTER_CONFIGURATION,
        (
            DEVICE.Channel.CHANNEL_3,
            DEVICE.CountEdge.BOTH,
            DEVICE.CountDirection.EXTERNAL_DOWN,
            DEVICE.DutyCyclePrescaler.DUTY_CYCLE_PRESCALER_32768,
            DEVICE.FrequencyIntegrationTime.FREQUENCY_INTEGRATION_TIME_32768_MS,
        ),
        sent=("B B B B B", (3, 2, 3, 15, 8)),
    ),
    Call(
        "set_counter_configuration",
        FunctionID.SET_COUNTER_CONFIGURATION,
        (
            DEVICE.Channel.CHANNEL_3,
            DEVICE.CountEdge.BOTH,
            DEVICE.CountDirection.EXTERNAL_DOWN,
            DEVICE.DutyCyclePrescaler.DUTY_CYCLE_PRESCALER_32768,
            DEVICE.FrequencyIntegrationTime.FREQUENCY_INTEGRATION_TIME_32768_MS,
            False,
        ),
        sent=("B B B B B", (3, 2, 3, 15, 8)),
        response_expected=False,
    ),
    Call(
        "get_counter_configuration",
        FunctionID.GET_COUNTER_CONFIGURATION,
        (DEVICE.Channel.CHANNEL_3,),
        sent=("B", (3,)),
        reply=("B B B B", (2, 3, 15, 8)),
        result=GetCounterConfiguration(
            DEVICE.CountEdge.BOTH,
            DEVICE.CountDirection.EXTERNAL_DOWN,
            DEVICE.DutyCyclePrescaler.DUTY_CYCLE_PRESCALER_32768,
            DEVICE.FrequencyIntegrationTime.FREQUENCY_INTEGRATION_TIME_32768_MS,
        ),
    ),
    Call(
        "set_all_counter_callback_configuration",
        FunctionID.SET_ALL_COUNTER_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_all_counter_callback_configuration",
        FunctionID.SET_ALL_COUNTER_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_all_counter_callback_configuration",
        FunctionID.GET_ALL_COUNTER_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_all_signal_data_callback_configuration",
        FunctionID.SET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_all_signal_data_callback_configuration",
        FunctionID.SET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_all_signal_data_callback_configuration",
        FunctionID.GET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_channel_led_config",
        FunctionID.SET_CHANNEL_LED_CONFIG,
        (DEVICE.Channel.CHANNEL_3, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS),
        sent=("B B", (3, 3)),
    ),
    Call(
        "set_channel_led_config",
        FunctionID.SET_CHANNEL_LED_CONFIG,
        (DEVICE.Channel.CHANNEL_3, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS, False),
        sent=("B B", (3, 3)),
        response_expected=False,
    ),
    Call(
        "get_channel_led_config",
        FunctionID.GET_CHANNEL_LED_CONFIG,
        (DEVICE.Channel.CHANNEL_3,),
        sent=("B", (3,)),
        reply=("B", (3,)),
        result=DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS,
    ),
    Call("get_value", FunctionID.GET_ALL_COUNTER, (0,), reply=("4q", ([3] * 4,)), result=(3,) * 4),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALL_COUNTER_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALL_COUNTER_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("get_counter", (12345,)),
    ("set_counter", (12345, 3)),
    ("set_counter", (DEVICE.Channel.CHANNEL_3, 140737488355328)),
    ("set_all_counter", (([3] * 4)[:-1],)),
    ("get_signal_data", (12345,)),
    ("set_counter_active", (12345, True)),
    ("set_all_counter_active", (([i % 2 == 0 for i in range(4)])[:-1],)),
    ("get_counter_active", (12345,)),
    (
        "set_counter_configuration",
        (
            12345,
            DEVICE.CountEdge.BOTH,
            DEVICE.CountDirection.EXTERNAL_DOWN,
            DEVICE.DutyCyclePrescaler.DUTY_CYCLE_PRESCALER_32768,
            DEVICE.FrequencyIntegrationTime.FREQUENCY_INTEGRATION_TIME_32768_MS,
        ),
    ),
    (
        "set_counter_configuration",
        (
            DEVICE.Channel.CHANNEL_3,
            12345,
            DEVICE.CountDirection.EXTERNAL_DOWN,
            DEVICE.DutyCyclePrescaler.DUTY_CYCLE_PRESCALER_32768,
            DEVICE.FrequencyIntegrationTime.FREQUENCY_INTEGRATION_TIME_32768_MS,
        ),
    ),
    (
        "set_counter_configuration",
        (
            DEVICE.Channel.CHANNEL_3,
            DEVICE.CountEdge.BOTH,
            12345,
            DEVICE.DutyCyclePrescaler.DUTY_CYCLE_PRESCALER_32768,
            DEVICE.FrequencyIntegrationTime.FREQUENCY_INTEGRATION_TIME_32768_MS,
        ),
    ),
    (
        "set_counter_configuration",
        (
            DEVICE.Channel.CHANNEL_3,
            DEVICE.CountEdge.BOTH,
            DEVICE.CountDirection.EXTERNAL_DOWN,
            12345,
            DEVICE.FrequencyIntegrationTime.FREQUENCY_INTEGRATION_TIME_32768_MS,
        ),
    ),
    (
        "set_counter_configuration",
        (
            DEVICE.Channel.CHANNEL_3,
            DEVICE.CountEdge.BOTH,
            DEVICE.CountDirection.EXTERNAL_DOWN,
            DEVICE.DutyCyclePrescaler.DUTY_CYCLE_PRESCALER_32768,
            12345,
        ),
    ),
    ("get_counter_configuration", (12345,)),
    ("set_all_counter_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_all_signal_data_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_channel_led_config", (12345, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS)),
    ("set_channel_led_config", (DEVICE.Channel.CHANNEL_3, 12345)),
    ("get_channel_led_config", (12345,)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 293
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Counter Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_all_counter(device, connection):
    """The callback ALL_COUNTER is converted to an event."""
    connection.callback(CallbackID.ALL_COUNTER, "4q", *([3] * 4,))
    assert summary(read_events(device)) == [(0, CallbackID.ALL_COUNTER, (3,) * 4)]


def test_callback_all_signal_data(device, connection):
    """The callback ALL_SIGNAL_DATA is converted to an event."""
    connection.callback(
        CallbackID.ALL_SIGNAL_DATA, "4H 4Q 4I 4!", *([3] * 4, [4] * 4, [5] * 4, [i % 2 == 0 for i in range(4)])
    )
    assert summary(read_events(device)) == [
        (
            1,
            CallbackID.ALL_SIGNAL_DATA,
            GetAllSignalData(
                (Decimal("0.03"),) * 4,
                (Decimal("4E-9"),) * 4,
                (Decimal("0.005"),) * 4,
                tuple(i % 2 == 0 for i in range(4)),
            ),
        )
    ]
