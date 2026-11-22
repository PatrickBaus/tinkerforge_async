"""Tests for the Industrial Dual AC Relay Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_dual_ac_relay import BrickletIndustrialDualACRelay, GetMonoflop, GetValue
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialDualACRelay
FunctionID = BrickletIndustrialDualACRelay.FunctionID
CallbackID = BrickletIndustrialDualACRelay.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_VALUE": 1,
    "GET_VALUE": 2,
    "SET_CHANNEL_LED_CONFIG": 3,
    "GET_CHANNEL_LED_CONFIG": 4,
    "SET_MONOFLOP": 5,
    "GET_MONOFLOP": 6,
    "SET_SELECTED_VALUE": 8,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"MONOFLOP_DONE": 7}

CALLS: list[Call] = [
    Call("set_value", FunctionID.SET_VALUE, (True, True), sent=("! !", (True, True))),
    Call("set_value", FunctionID.SET_VALUE, (True, True, False), sent=("! !", (True, True)), response_expected=False),
    Call("get_value", FunctionID.GET_VALUE, (), reply=("! !", (True, True)), result=GetValue(True, True)),
    Call(
        "set_channel_led_config",
        FunctionID.SET_CHANNEL_LED_CONFIG,
        (1, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS),
        sent=("B B", (1, 3)),
    ),
    Call(
        "set_channel_led_config",
        FunctionID.SET_CHANNEL_LED_CONFIG,
        (1, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS, False),
        sent=("B B", (1, 3)),
        response_expected=False,
    ),
    Call(
        "get_channel_led_config",
        FunctionID.GET_CHANNEL_LED_CONFIG,
        (1,),
        sent=("B", (1,)),
        reply=("B", (3,)),
        result=DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS,
    ),
    Call("set_monoflop", FunctionID.SET_MONOFLOP, (1, True, Decimal("0.003")), sent=("B ! I", (1, True, 3))),
    Call(
        "set_monoflop",
        FunctionID.SET_MONOFLOP,
        (1, True, Decimal("0.003"), False),
        sent=("B ! I", (1, True, 3)),
        response_expected=False,
    ),
    Call(
        "get_monoflop",
        FunctionID.GET_MONOFLOP,
        (1,),
        sent=("B", (1,)),
        reply=("! I I", (True, 4, 5)),
        result=GetMonoflop(True, Decimal("0.004"), Decimal("0.005")),
    ),
    Call("set_selected_value", FunctionID.SET_SELECTED_VALUE, (1, True), sent=("B !", (1, True))),
    Call(
        "set_selected_value",
        FunctionID.SET_SELECTED_VALUE,
        (1, True, False),
        sent=("B !", (1, True)),
        response_expected=False,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_channel_led_config", (2, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS)),
    ("set_channel_led_config", (1, 12345)),
    ("get_channel_led_config", (2,)),
    ("set_monoflop", (2, True, Decimal("0.003"))),
    ("set_monoflop", (1, True, Decimal("4294967.296"))),
    ("get_monoflop", (2,)),
    ("set_selected_value", (2, True)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2162
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Dual AC Relay Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_monoflop_done(device, connection):
    """The callback MONOFLOP_DONE is converted to an event."""
    connection.callback(CallbackID.MONOFLOP_DONE, "B !", *(1, True))
    assert summary(read_events(device)) == [(1, CallbackID.MONOFLOP_DONE, True)]
