"""Tests for the Rotary Poti Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_rotary_poti_v2 import BrickletRotaryPotiV2
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletRotaryPotiV2
FunctionID = BrickletRotaryPotiV2.FunctionID
CallbackID = BrickletRotaryPotiV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_POSITION": 1,
    "SET_POSITION_CALLBACK_CONFIGURATION": 2,
    "GET_POSITION_CALLBACK_CONFIGURATION": 3,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"POSITION": 4}

CALLS: list[Call] = [
    Call("get_position", FunctionID.GET_POSITION, (), reply=("h", (3,)), result=Decimal("3")),
    Call(
        "set_position_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("3"), Decimal("3")),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_position_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("3"), Decimal("3"), False),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_position_callback_configuration",
        FunctionID.GET_POSITION_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c h h", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call("get_value", FunctionID.GET_POSITION, (0,), reply=("h", (3,)), result=Decimal("3")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
        sent=("I ! c h h", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_POSITION_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c h h", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_position_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("3"), Decimal("3"))),
    ("set_position_callback_configuration", (Decimal("0.003"), True, "?", Decimal("3"), Decimal("3"))),
    ("set_position_callback_configuration", (Decimal("0.003"), True, "o", Decimal("32768"), Decimal("3"))),
    ("set_position_callback_configuration", (Decimal("0.003"), True, "o", Decimal("3"), Decimal("32768"))),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2140
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Rotary Poti Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_position(device, connection):
    """The callback POSITION is converted to an event."""
    connection.callback(CallbackID.POSITION, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.POSITION, Decimal("3"))]
