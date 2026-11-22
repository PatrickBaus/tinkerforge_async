"""Tests for the Industrial Dual 0-20mA Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_industrial_dual_0_20ma_v2 import (
    BrickletIndustrialDual020mAV2,
    GetChannelLEDStatusConfig,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, LedConfig
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, read_events, summary

DEVICE = BrickletIndustrialDual020mAV2
FunctionID = BrickletIndustrialDual020mAV2.FunctionID
CallbackID = BrickletIndustrialDual020mAV2.CallbackID
SamplingRate = BrickletIndustrialDual020mAV2.SamplingRate
Gain = BrickletIndustrialDual020mAV2.Gain
ChannelLedStatusConfig = BrickletIndustrialDual020mAV2.ChannelLedStatusConfig

CONFIGURATION = AdvancedCallbackConfiguration(
    Decimal("0.5"), True, Threshold.OUTSIDE, Decimal("0.004"), Decimal("0.02")
)

CALLS = [
    # The current is transferred in nA
    Call(
        "get_current", FunctionID.GET_CURRENT, (0,), sent=("B", (0,)), reply=("i", (4000000,)), result=Decimal("0.004")
    ),
    Call("get_value", FunctionID.GET_CURRENT, (1,), sent=("B", (1,)), reply=("i", (1,)), result=Decimal("1E-9")),
    Call(
        "set_current_callback_configuration",
        FunctionID.SET_CURRENT_CALLBACK_CONFIGURATION,
        (0,),
        sent=("B I ! c i i", (0, 0, False, b"x", 0, 0)),
    ),
    Call(
        "set_current_callback_configuration",
        FunctionID.SET_CURRENT_CALLBACK_CONFIGURATION,
        (1, Decimal("0.5"), True, "o", Decimal("0.004"), 0.02, False),
        sent=("B I ! c i i", (1, 500, True, b"o", 4000000, 20000000)),
        response_expected=False,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_CURRENT_CALLBACK_CONFIGURATION,
        (1, 1, False, Threshold.GREATER_THAN, Decimal("0.0029")),
        sent=("B I ! c i i", (1, 1000, False, b">", 2900000, 0)),
    ),
    Call(
        "get_current_callback_configuration",
        FunctionID.GET_CURRENT_CALLBACK_CONFIGURATION,
        (0,),
        sent=("B", (0,)),
        reply=("I ! c i i", (500, True, "o", 4000000, 20000000)),
        result=CONFIGURATION,
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_CURRENT_CALLBACK_CONFIGURATION,
        (1,),
        sent=("B", (1,)),
        reply=("I ! c i i", (500, True, "o", 4000000, 20000000)),
        result=CONFIGURATION,
    ),
    Call("set_sample_rate", FunctionID.SET_SAMPLE_RATE, (SamplingRate.RATE_4_SPS,), sent=("B", (3,))),
    Call("set_sample_rate", FunctionID.SET_SAMPLE_RATE, (0,), sent=("B", (0,))),
    Call("get_sample_rate", FunctionID.GET_SAMPLE_RATE, reply=("B", (2,)), result=SamplingRate.RATE_15_SPS),
    Call("set_gain", FunctionID.SET_GAIN, (Gain.GAIN_8X,), sent=("B", (3,))),
    Call("set_gain", FunctionID.SET_GAIN, (0,), sent=("B", (0,))),
    Call("get_gain", FunctionID.GET_GAIN, reply=("B", (1,)), result=Gain.GAIN_2X),
    Call("set_channel_led_config", FunctionID.SET_CHANNEL_LED_CONFIG, (0, LedConfig.OFF), sent=("B B", (0, 0))),
    Call("set_channel_led_config", FunctionID.SET_CHANNEL_LED_CONFIG, (1, 3), sent=("B B", (1, 3))),
    Call(
        "get_channel_led_config",
        FunctionID.GET_CHANNEL_LED_CONFIG,
        (1,),
        sent=("B", (1,)),
        reply=("B", (2,)),
        result=LedConfig.SHOW_HEARTBEAT,
    ),
    Call(
        "set_channel_led_status_config",
        FunctionID.SET_CHANNEL_LED_STATUS_CONFIG,
        (0, Decimal("0.004"), 0.02, ChannelLedStatusConfig.INTENSITY),
        sent=("B i i B", (0, 4000000, 20000000, 1)),
    ),
    Call(
        "set_channel_led_status_config",
        FunctionID.SET_CHANNEL_LED_STATUS_CONFIG,
        (1, 0, Decimal("0.01"), 0),
        sent=("B i i B", (1, 0, 10000000, 0)),
    ),
    Call(
        "get_channel_led_status_config",
        FunctionID.GET_CHANNEL_LED_STATUS_CONFIG,
        (1,),
        sent=("B", (1,)),
        reply=("i i B", (4000000, 20000000, 1)),
        result=GetChannelLEDStatusConfig(Decimal("0.004"), Decimal("0.02"), ChannelLedStatusConfig.INTENSITY),
    ),
]

REJECTED = [
    ("get_current", (2,)),
    ("set_current_callback_configuration", (2,)),
    ("set_current_callback_configuration", (0, -1)),
    ("set_current_callback_configuration", (0, 1, False, "?")),
    ("get_current_callback_configuration", (2,)),
    ("set_sample_rate", (4,)),
    ("set_gain", (4,)),
    ("set_channel_led_config", (2, 0)),
    ("set_channel_led_config", (0, 4)),
    ("get_channel_led_config", (2,)),
    ("set_channel_led_status_config", (2, 0, 0, 0)),
    ("set_channel_led_status_config", (0, 0, 0, 2)),
    ("get_channel_led_status_config", (2,)),
    # The sids are the channels 0 and 1
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(bricklet: BrickletIndustrialDual020mAV2) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2120
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Industrial Dual 0-20mA Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet: BrickletIndustrialDual020mAV2, connection: FakeConnection) -> None:
    """The channel is part of the payload and becomes the sid. The current is converted to A."""
    connection.callback(CallbackID.CURRENT, "B i", 0, 4000000)
    connection.callback(CallbackID.CURRENT, "B i", 1, 20000000)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.CURRENT, Decimal("0.004")),
        (1, CallbackID.CURRENT, Decimal("0.02")),
    ]
    # Both channels use the same callback, so the events of the other channel must be dropped
    assert summary(read_events(bricklet, sids=(1,))) == [(1, CallbackID.CURRENT, Decimal("0.02"))]
    assert len(read_events(bricklet, events=(CallbackID.CURRENT,))) == 2
