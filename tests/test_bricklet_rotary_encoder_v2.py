"""Tests for the Rotary Encoder Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_rotary_encoder_v2 import BrickletRotaryEncoderV2
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletRotaryEncoderV2
FunctionID = BrickletRotaryEncoderV2.FunctionID
CallbackID = BrickletRotaryEncoderV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_COUNT": 1,
    "SET_COUNT_CALLBACK_CONFIGURATION": 2,
    "GET_COUNT_CALLBACK_CONFIGURATION": 3,
    "IS_PRESSED": 5,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"COUNT": 4, "PRESSED": 6, "RELEASED": 7}

CALLS: list[Call] = [
    Call("get_count", FunctionID.GET_COUNT, (True,), sent=("!", (True,)), reply=("i", (3,)), result=3),
    Call(
        "set_count_callback_configuration",
        FunctionID.SET_COUNT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_count_callback_configuration",
        FunctionID.SET_COUNT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3, False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_count_callback_configuration",
        FunctionID.GET_COUNT_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call("is_pressed", FunctionID.IS_PRESSED, (), reply=("!", (True,)), result=True),
    Call(
        "set_callback_configuration",
        FunctionID.SET_COUNT_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, 3, 4),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_COUNT_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_count_callback_configuration", (Decimal("4294967.296"), True, "o", 3, 3)),
    ("set_count_callback_configuration", (Decimal("0.003"), True, "?", 3, 3)),
    ("set_count_callback_configuration", (Decimal("0.003"), True, "o", 2147483648, 3)),
    ("set_count_callback_configuration", (Decimal("0.003"), True, "o", 3, 2147483648)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 294
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Rotary Encoder Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_count(device, connection):
    """The callback COUNT is converted to an event."""
    connection.callback(CallbackID.COUNT, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.COUNT, 3)]


def test_callback_pressed(device, connection):
    """The callback PRESSED is converted to an event."""
    connection.callback(CallbackID.PRESSED)
    assert summary(read_events(device)) == [(1, CallbackID.PRESSED, None)]


def test_callback_released(device, connection):
    """The callback RELEASED is converted to an event."""
    connection.callback(CallbackID.RELEASED)
    assert summary(read_events(device)) == [(2, CallbackID.RELEASED, None)]
