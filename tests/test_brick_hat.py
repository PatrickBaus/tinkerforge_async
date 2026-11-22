"""Tests for the HAT Brick. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_hat import BrickHAT, GetSleepMode, GetVoltages
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickHAT
FunctionID = BrickHAT.FunctionID
CallbackID = BrickHAT.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_SLEEP_MODE": 1,
    "GET_SLEEP_MODE": 2,
    "SET_BRICKLET_POWER": 3,
    "GET_BRICKLET_POWER": 4,
    "GET_VOLTAGES": 5,
    "SET_VOLTAGES_CALLBACK_CONFIGURATION": 6,
    "GET_VOLTAGES_CALLBACK_CONFIGURATION": 7,
    "SET_RTC_DRIVER": 9,
    "GET_RTC_DRIVER": 10,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"VOLTAGES": 8}

CALLS: list[Call] = [
    Call(
        "set_sleep_mode",
        FunctionID.SET_SLEEP_MODE,
        (Decimal("3"), Decimal("3"), True, True, True),
        sent=("I I ! ! !", (3, 3, True, True, True)),
    ),
    Call(
        "set_sleep_mode",
        FunctionID.SET_SLEEP_MODE,
        (Decimal("3"), Decimal("3"), True, True, True, False),
        sent=("I I ! ! !", (3, 3, True, True, True)),
        response_expected=False,
    ),
    Call(
        "get_sleep_mode",
        FunctionID.GET_SLEEP_MODE,
        (),
        reply=("I I ! ! !", (3, 4, True, True, True)),
        result=GetSleepMode(Decimal("3"), Decimal("4"), True, True, True),
    ),
    Call("set_bricklet_power", FunctionID.SET_BRICKLET_POWER, (True,), sent=("!", (True,))),
    Call(
        "set_bricklet_power", FunctionID.SET_BRICKLET_POWER, (True, False), sent=("!", (True,)), response_expected=False
    ),
    Call("get_bricklet_power", FunctionID.GET_BRICKLET_POWER, (), reply=("!", (True,)), result=True),
    Call(
        "get_voltages",
        FunctionID.GET_VOLTAGES,
        (),
        reply=("H H", (3, 4)),
        result=GetVoltages(Decimal("0.003"), Decimal("0.004")),
    ),
    Call(
        "set_voltages_callback_configuration",
        FunctionID.SET_VOLTAGES_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_voltages_callback_configuration",
        FunctionID.SET_VOLTAGES_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_voltages_callback_configuration",
        FunctionID.GET_VOLTAGES_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("set_rtc_driver", FunctionID.SET_RTC_DRIVER, (DEVICE.RTCDriver.DS1338,), sent=("B", (1,))),
    Call(
        "set_rtc_driver",
        FunctionID.SET_RTC_DRIVER,
        (DEVICE.RTCDriver.DS1338, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call("get_rtc_driver", FunctionID.GET_RTC_DRIVER, (), reply=("B", (1,)), result=DEVICE.RTCDriver.DS1338),
    Call(
        "set_callback_configuration",
        FunctionID.SET_VOLTAGES_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_VOLTAGES_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_sleep_mode", (Decimal("4294967296"), Decimal("3"), True, True, True)),
    ("set_sleep_mode", (Decimal("3"), Decimal("4294967296"), True, True, True)),
    ("set_voltages_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_rtc_driver", (12345,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device: BrickHAT) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 111
    assert device.get_api_version() == (2, 0, 2)
    assert str(device).startswith("HAT Brick with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_voltages(device: BrickHAT, connection: FakeConnection) -> None:
    """The callback VOLTAGES is converted to an event."""
    connection.callback(CallbackID.VOLTAGES, "H H", *(3, 4))
    assert summary(read_events(device)) == [(0, CallbackID.VOLTAGES, GetVoltages(Decimal("0.003"), Decimal("0.004")))]
