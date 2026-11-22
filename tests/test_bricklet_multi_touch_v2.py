"""Tests for the Multi Touch Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_multi_touch_v2 import BrickletMultiTouchV2
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletMultiTouchV2
FunctionID = BrickletMultiTouchV2.FunctionID
CallbackID = BrickletMultiTouchV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_TOUCH_STATE": 1,
    "SET_TOUCH_STATE_CALLBACK_CONFIGURATION": 2,
    "GET_TOUCH_STATE_CALLBACK_CONFIGURATION": 3,
    "RECALIBRATE": 5,
    "SET_ELECTRODE_CONFIG": 6,
    "GET_ELECTRODE_CONFIG": 7,
    "SET_ELECTRODE_SENSITIVITY": 8,
    "GET_ELECTRODE_SENSITIVITY": 9,
    "SET_TOUCH_LED_CONFIG": 10,
    "GET_TOUCH_LED_CONFIG": 11,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"TOUCH_STATE": 4}

CALLS: list[Call] = [
    Call(
        "get_touch_state",
        FunctionID.GET_TOUCH_STATE,
        (),
        reply=("13!", ([i % 2 == 0 for i in range(13)],)),
        result=tuple(i % 2 == 0 for i in range(13)),
    ),
    Call(
        "set_touch_state_callback_configuration",
        FunctionID.SET_TOUCH_STATE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_touch_state_callback_configuration",
        FunctionID.SET_TOUCH_STATE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_touch_state_callback_configuration",
        FunctionID.GET_TOUCH_STATE_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("recalibrate", FunctionID.RECALIBRATE, ()),
    Call("recalibrate", FunctionID.RECALIBRATE, (False,), response_expected=False),
    Call(
        "set_electrode_config",
        FunctionID.SET_ELECTRODE_CONFIG,
        ([i % 2 == 0 for i in range(13)],),
        sent=("13!", ([i % 2 == 0 for i in range(13)],)),
    ),
    Call(
        "set_electrode_config",
        FunctionID.SET_ELECTRODE_CONFIG,
        ([i % 2 == 0 for i in range(13)], False),
        sent=("13!", ([i % 2 == 0 for i in range(13)],)),
        response_expected=False,
    ),
    Call(
        "get_electrode_config",
        FunctionID.GET_ELECTRODE_CONFIG,
        (),
        reply=("13!", ([i % 2 == 0 for i in range(13)],)),
        result=tuple(i % 2 == 0 for i in range(13)),
    ),
    Call("set_electrode_sensitivity", FunctionID.SET_ELECTRODE_SENSITIVITY, (5,), sent=("B", (5,))),
    Call(
        "set_electrode_sensitivity",
        FunctionID.SET_ELECTRODE_SENSITIVITY,
        (5, False),
        sent=("B", (5,)),
        response_expected=False,
    ),
    Call("get_electrode_sensitivity", FunctionID.GET_ELECTRODE_SENSITIVITY, (), reply=("B", (5,)), result=5),
    Call(
        "set_touch_led_config", FunctionID.SET_TOUCH_LED_CONFIG, (DEVICE.TouchLEDConfig.SHOW_TOUCH,), sent=("B", (3,))
    ),
    Call(
        "set_touch_led_config",
        FunctionID.SET_TOUCH_LED_CONFIG,
        (DEVICE.TouchLEDConfig.SHOW_TOUCH, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_touch_led_config",
        FunctionID.GET_TOUCH_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.TouchLEDConfig.SHOW_TOUCH,
    ),
    Call(
        "get_value",
        FunctionID.GET_TOUCH_STATE,
        (0,),
        reply=("13!", ([i % 2 == 0 for i in range(13)],)),
        result=tuple(i % 2 == 0 for i in range(13)),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TOUCH_STATE_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TOUCH_STATE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_touch_state_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_electrode_config", (([i % 2 == 0 for i in range(13)])[:-1],)),
    ("set_electrode_sensitivity", (202,)),
    ("set_touch_led_config", (12345,)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device: BrickletMultiTouchV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2129
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Multi Touch Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_touch_state(device: BrickletMultiTouchV2, connection: FakeConnection) -> None:
    """The callback TOUCH_STATE is converted to an event."""
    connection.callback(CallbackID.TOUCH_STATE, "13!", *([i % 2 == 0 for i in range(13)],))
    assert summary(read_events(device)) == [(0, CallbackID.TOUCH_STATE, tuple(i % 2 == 0 for i in range(13)))]
