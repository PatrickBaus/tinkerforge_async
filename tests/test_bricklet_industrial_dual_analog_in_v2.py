"""Tests for the Industrial Dual Analog In Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_industrial_dual_analog_in_v2 import (
    BrickletIndustrialDualAnalogInV2,
    GetCalibration,
    GetChannelLEDStatusConfig,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, LedConfig, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, summary

DEVICE = BrickletIndustrialDualAnalogInV2
FunctionID = BrickletIndustrialDualAnalogInV2.FunctionID
CallbackID = BrickletIndustrialDualAnalogInV2.CallbackID
SamplingRate = BrickletIndustrialDualAnalogInV2.SamplingRate
ChannelLedStatusConfig = BrickletIndustrialDualAnalogInV2.ChannelLedStatusConfig

CONFIGURATION = AdvancedCallbackConfiguration(Decimal("0.5"), True, Threshold.OUTSIDE, Decimal("-1.5"), Decimal(35))

CALLS = [
    # The voltage is transferred in mV
    Call("get_voltage", FunctionID.GET_VOLTAGE, (0,), sent=("B", (0,)), reply=("i", (-1500,)), result=Decimal("-1.5")),
    Call("get_value", FunctionID.GET_VOLTAGE, (1,), sent=("B", (1,)), reply=("i", (35000,)), result=Decimal(35)),
    Call(
        "get_all_voltages",
        FunctionID.GET_ALL_VOLTAGES,
        reply=("2i", ((-1500, 35000),)),
        result=(Decimal("-1.5"), Decimal(35)),
    ),
    Call(
        "get_value",
        FunctionID.GET_ALL_VOLTAGES,
        (2,),
        reply=("2i", ((1, 2),)),
        result=(Decimal("0.001"), Decimal("0.002")),
    ),
    Call(
        "set_voltage_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (0,),
        sent=("B I ! c i i", (0, 0, False, b"x", 0, 0)),
    ),
    Call(
        "set_voltage_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (1, Decimal("0.5"), True, "o", Decimal("-1.5"), 35, False),
        sent=("B I ! c i i", (1, 500, True, b"o", -1500, 35000)),
        response_expected=False,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
        (1, 1, False, Threshold.GREATER_THAN, 0.29),
        sent=("B I ! c i i", (1, 1000, False, b">", 290, 0)),
    ),
    Call(
        "get_voltage_callback_configuration",
        FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION,
        (0,),
        sent=("B", (0,)),
        reply=("I ! c i i", (500, True, "o", -1500, 35000)),
        result=CONFIGURATION,
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION,
        (1,),
        sent=("B", (1,)),
        reply=("I ! c i i", (500, True, "o", -1500, 35000)),
        result=CONFIGURATION,
    ),
    Call(
        "set_all_voltages_callback_configuration",
        FunctionID.SET_ALL_VOLTAGES_CALLBACK_CONFIGURATION,
        sent=("I !", (0, False)),
    ),
    Call(
        "set_all_voltages_callback_configuration",
        FunctionID.SET_ALL_VOLTAGES_CALLBACK_CONFIGURATION,
        (Decimal("0.5"), True),
        sent=("I !", (500, True)),
    ),
    # The callback of all voltages has no thresholds. They are ignored.
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALL_VOLTAGES_CALLBACK_CONFIGURATION,
        (2, 2, True, Threshold.GREATER_THAN, 1, 2),
        sent=("I !", (2000, True)),
    ),
    Call(
        "get_all_voltages_callback_configuration",
        FunctionID.GET_ALL_VOLTAGES_CALLBACK_CONFIGURATION,
        reply=("I !", (500, True)),
        result=SimpleCallbackConfiguration(Decimal("0.5"), True),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALL_VOLTAGES_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I !", (500, True)),
        result=AdvancedCallbackConfiguration(Decimal("0.5"), True, None, None, None),
    ),
    Call("set_sample_rate", FunctionID.SET_SAMPLE_RATE, (SamplingRate.RATE_1_SPS,), sent=("B", (7,))),
    Call("set_sample_rate", FunctionID.SET_SAMPLE_RATE, (0,), sent=("B", (0,))),
    Call("get_sample_rate", FunctionID.GET_SAMPLE_RATE, reply=("B", (6,)), result=SamplingRate.RATE_2_SPS),
    Call(
        "set_calibration",
        FunctionID.SET_CALIBRATION,
        ((-1, 2), [3, -4]),
        sent=("2i 2i", ((-1, 2), (3, -4))),
    ),
    Call(
        "get_calibration",
        FunctionID.GET_CALIBRATION,
        reply=("2i 2i", ((-1, 2), (3, -4))),
        result=GetCalibration((-1, 2), (3, -4)),
    ),
    Call("get_adc_values", FunctionID.GET_ADC_VALUES, reply=("2i", ((-100, 100),)), result=(-100, 100)),
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
        (0, Decimal("-1.5"), 35, ChannelLedStatusConfig.INTENSITY),
        sent=("B i i B", (0, -1500, 35000, 1)),
    ),
    Call(
        "set_channel_led_status_config",
        FunctionID.SET_CHANNEL_LED_STATUS_CONFIG,
        (1, 0, Decimal("0.01"), 0),
        sent=("B i i B", (1, 0, 10, 0)),
    ),
    Call(
        "get_channel_led_status_config",
        FunctionID.GET_CHANNEL_LED_STATUS_CONFIG,
        (1,),
        sent=("B", (1,)),
        reply=("i i B", (-1500, 35000, 1)),
        result=GetChannelLEDStatusConfig(Decimal("-1.5"), Decimal(35), ChannelLedStatusConfig.INTENSITY),
    ),
]

REJECTED = [
    ("get_voltage", (2,)),
    ("set_voltage_callback_configuration", (2,)),
    ("set_voltage_callback_configuration", (0, -1)),
    ("set_voltage_callback_configuration", (0, 1, False, "?")),
    ("set_all_voltages_callback_configuration", (-1,)),
    ("set_sample_rate", (8,)),
    ("set_channel_led_config", (2, 0)),
    ("set_channel_led_config", (0, 4)),
    ("get_channel_led_config", (2,)),
    ("set_channel_led_status_config", (2, 0, 0, 0)),
    ("set_channel_led_status_config", (0, 0, 0, 2)),
    ("get_channel_led_status_config", (2,)),
    # The sids are the channels 0 and 1, and 2 for both channels
    ("get_value", (3,)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2121
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Industrial Dual Analog In Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet, connection):
    """
    The channel is part of the payload of the voltage callback and becomes the sid. The callback of all voltages is
    sid 2. The voltages are converted to V.
    """
    connection.callback(CallbackID.VOLTAGE, "B i", 0, -1500)
    connection.callback(CallbackID.VOLTAGE, "B i", 1, 35000)
    connection.callback(CallbackID.ALL_VOLTAGES, "2i", (-1500, 35000))
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.VOLTAGE, Decimal("-1.5")),
        (1, CallbackID.VOLTAGE, Decimal(35)),
        (2, CallbackID.ALL_VOLTAGES, (Decimal("-1.5"), Decimal(35))),
    ]
    # Both channels use the same callback, so the events of the other channel must be dropped
    assert summary(read_events(bricklet, sids=(1,))) == [(1, CallbackID.VOLTAGE, Decimal(35))]
    assert summary(read_events(bricklet, sids=(2,))) == [(2, CallbackID.ALL_VOLTAGES, (Decimal("-1.5"), Decimal(35)))]
    assert len(read_events(bricklet, events=(CallbackID.VOLTAGE,))) == 2
