"""Tests for the Accelerometer Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_accelerometer_v2 import (
    BrickletAccelerometerV2,
    GetAcceleration,
    GetConfiguration,
    GetContinuousAccelerationConfiguration,
    GetFilterConfiguration,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletAccelerometerV2
FunctionID = BrickletAccelerometerV2.FunctionID
CallbackID = BrickletAccelerometerV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_ACCELERATION": 1,
    "SET_CONFIGURATION": 2,
    "GET_CONFIGURATION": 3,
    "SET_ACCELERATION_CALLBACK_CONFIGURATION": 4,
    "GET_ACCELERATION_CALLBACK_CONFIGURATION": 5,
    "SET_INFO_LED_CONFIG": 6,
    "GET_INFO_LED_CONFIG": 7,
    "SET_CONTINUOUS_ACCELERATION_CONFIGURATION": 9,
    "GET_CONTINUOUS_ACCELERATION_CONFIGURATION": 10,
    "SET_FILTER_CONFIGURATION": 13,
    "GET_FILTER_CONFIGURATION": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "ACCELERATION": 8,
    "CONTINUOUS_ACCELERATION_16_BIT": 11,
    "CONTINUOUS_ACCELERATION_8_BIT": 12,
}

CALLS: list[Call] = [
    Call(
        "get_acceleration",
        FunctionID.GET_ACCELERATION,
        (),
        reply=("i i i", (3, 4, 5)),
        result=GetAcceleration(Decimal("0.002941995"), Decimal("0.00392266"), Decimal("0.004903325")),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.DataRate.DATA_RATE_25600HZ, DEVICE.FullScale.FULL_SCALE_8G),
        sent=("B B", (15, 2)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.DataRate.DATA_RATE_25600HZ, DEVICE.FullScale.FULL_SCALE_8G, False),
        sent=("B B", (15, 2)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B", (15, 2)),
        result=GetConfiguration(DEVICE.DataRate.DATA_RATE_25600HZ, DEVICE.FullScale.FULL_SCALE_8G),
    ),
    Call(
        "set_acceleration_callback_configuration",
        FunctionID.SET_ACCELERATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_acceleration_callback_configuration",
        FunctionID.SET_ACCELERATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_acceleration_callback_configuration",
        FunctionID.GET_ACCELERATION_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_info_led_config", FunctionID.SET_INFO_LED_CONFIG, (DEVICE.InfoLEDConfig.SHOW_HEARTBEAT,), sent=("B", (2,))
    ),
    Call(
        "set_info_led_config",
        FunctionID.SET_INFO_LED_CONFIG,
        (DEVICE.InfoLEDConfig.SHOW_HEARTBEAT, False),
        sent=("B", (2,)),
        response_expected=False,
    ),
    Call(
        "get_info_led_config",
        FunctionID.GET_INFO_LED_CONFIG,
        (),
        reply=("B", (2,)),
        result=DEVICE.InfoLEDConfig.SHOW_HEARTBEAT,
    ),
    Call(
        "set_continuous_acceleration_configuration",
        FunctionID.SET_CONTINUOUS_ACCELERATION_CONFIGURATION,
        (True, True, True, DEVICE.Resolution.RESOLUTION_16BIT),
        sent=("! ! ! B", (True, True, True, 1)),
    ),
    Call(
        "set_continuous_acceleration_configuration",
        FunctionID.SET_CONTINUOUS_ACCELERATION_CONFIGURATION,
        (True, True, True, DEVICE.Resolution.RESOLUTION_16BIT, False),
        sent=("! ! ! B", (True, True, True, 1)),
        response_expected=False,
    ),
    Call(
        "get_continuous_acceleration_configuration",
        FunctionID.GET_CONTINUOUS_ACCELERATION_CONFIGURATION,
        (),
        reply=("! ! ! B", (True, True, True, 1)),
        result=GetContinuousAccelerationConfiguration(True, True, True, DEVICE.Resolution.RESOLUTION_16BIT),
    ),
    Call(
        "set_filter_configuration",
        FunctionID.SET_FILTER_CONFIGURATION,
        (DEVICE.IIRBypass.BYPASSED, DEVICE.LowPassFilter.HALF),
        sent=("B B", (1, 1)),
    ),
    Call(
        "set_filter_configuration",
        FunctionID.SET_FILTER_CONFIGURATION,
        (DEVICE.IIRBypass.BYPASSED, DEVICE.LowPassFilter.HALF, False),
        sent=("B B", (1, 1)),
        response_expected=False,
    ),
    Call(
        "get_filter_configuration",
        FunctionID.GET_FILTER_CONFIGURATION,
        (),
        reply=("B B", (1, 1)),
        result=GetFilterConfiguration(DEVICE.IIRBypass.BYPASSED, DEVICE.LowPassFilter.HALF),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ACCELERATION_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ACCELERATION_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_configuration", (12345, DEVICE.FullScale.FULL_SCALE_8G)),
    ("set_configuration", (DEVICE.DataRate.DATA_RATE_25600HZ, 12345)),
    ("set_acceleration_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_info_led_config", (12345,)),
    ("set_continuous_acceleration_configuration", (True, True, True, 12345)),
    ("set_filter_configuration", (12345, DEVICE.LowPassFilter.HALF)),
    ("set_filter_configuration", (DEVICE.IIRBypass.BYPASSED, 12345)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device: BrickletAccelerometerV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2130
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Accelerometer Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_acceleration(device: BrickletAccelerometerV2, connection: FakeConnection) -> None:
    """The callback ACCELERATION is converted to an event."""
    connection.callback(CallbackID.ACCELERATION, "i i i", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.ACCELERATION,
            GetAcceleration(Decimal("0.002941995"), Decimal("0.00392266"), Decimal("0.004903325")),
        )
    ]


def test_callback_continuous_acceleration_16_bit(device: BrickletAccelerometerV2, connection: FakeConnection) -> None:
    """The callback CONTINUOUS_ACCELERATION_16_BIT is converted to an event."""
    connection.callback(CallbackID.CONTINUOUS_ACCELERATION_16_BIT, "30h", *([3] * 30,))
    assert summary(read_events(device)) == [(1, CallbackID.CONTINUOUS_ACCELERATION_16_BIT, (3,) * 30)]


def test_callback_continuous_acceleration_8_bit(device: BrickletAccelerometerV2, connection: FakeConnection) -> None:
    """The callback CONTINUOUS_ACCELERATION_8_BIT is converted to an event."""
    connection.callback(CallbackID.CONTINUOUS_ACCELERATION_8_BIT, "60b", *([3] * 60,))
    assert summary(read_events(device)) == [(2, CallbackID.CONTINUOUS_ACCELERATION_8_BIT, (3,) * 60)]
