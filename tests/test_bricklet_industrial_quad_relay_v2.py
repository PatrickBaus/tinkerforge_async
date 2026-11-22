"""Tests for the Industrial Quad Relay Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2, GetMonoflop
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialQuadRelayV2
FunctionID = BrickletIndustrialQuadRelayV2.FunctionID
CallbackID = BrickletIndustrialQuadRelayV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_VALUE": 1,
    "GET_VALUE": 2,
    "SET_MONOFLOP": 3,
    "GET_MONOFLOP": 4,
    "SET_SELECTED_VALUE": 5,
    "SET_CHANNEL_LED_CONFIG": 6,
    "GET_CHANNEL_LED_CONFIG": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"MONOFLOP_DONE": 8}

CALLS: list[Call] = [
    Call(
        "set_value",
        FunctionID.SET_VALUE,
        ([i % 2 == 0 for i in range(4)],),
        sent=("4!", ([i % 2 == 0 for i in range(4)],)),
    ),
    Call(
        "set_value",
        FunctionID.SET_VALUE,
        ([i % 2 == 0 for i in range(4)], False),
        sent=("4!", ([i % 2 == 0 for i in range(4)],)),
        response_expected=False,
    ),
    Call(
        "get_value",
        FunctionID.GET_VALUE,
        (),
        reply=("4!", ([i % 2 == 0 for i in range(4)],)),
        result=tuple(i % 2 == 0 for i in range(4)),
    ),
    Call("set_monoflop", FunctionID.SET_MONOFLOP, (3, True, Decimal("0.003")), sent=("B ! I", (3, True, 3))),
    Call(
        "set_monoflop",
        FunctionID.SET_MONOFLOP,
        (3, True, Decimal("0.003"), False),
        sent=("B ! I", (3, True, 3)),
        response_expected=False,
    ),
    Call(
        "get_monoflop",
        FunctionID.GET_MONOFLOP,
        (3,),
        sent=("B", (3,)),
        reply=("! I I", (True, 4, 5)),
        result=GetMonoflop(True, Decimal("0.004"), Decimal("0.005")),
    ),
    Call("set_selected_value", FunctionID.SET_SELECTED_VALUE, (3, True), sent=("B !", (3, True))),
    Call(
        "set_selected_value",
        FunctionID.SET_SELECTED_VALUE,
        (3, True, False),
        sent=("B !", (3, True)),
        response_expected=False,
    ),
    Call(
        "set_channel_led_config",
        FunctionID.SET_CHANNEL_LED_CONFIG,
        (3, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS),
        sent=("B B", (3, 3)),
    ),
    Call(
        "set_channel_led_config",
        FunctionID.SET_CHANNEL_LED_CONFIG,
        (3, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS, False),
        sent=("B B", (3, 3)),
        response_expected=False,
    ),
    Call(
        "get_channel_led_config",
        FunctionID.GET_CHANNEL_LED_CONFIG,
        (3,),
        sent=("B", (3,)),
        reply=("B", (3,)),
        result=DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_value", (([i % 2 == 0 for i in range(4)])[:-1],)),
    ("set_monoflop", (4, True, Decimal("0.003"))),
    ("set_monoflop", (3, True, Decimal("4294967.296"))),
    ("get_monoflop", (4,)),
    ("set_selected_value", (4, True)),
    ("set_channel_led_config", (4, DEVICE.ChannelLEDConfig.SHOW_CHANNEL_STATUS)),
    ("set_channel_led_config", (3, 12345)),
    ("get_channel_led_config", (4,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2102
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Quad Relay Bricklet 2.0 with uid 12345")


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
    connection.callback(CallbackID.MONOFLOP_DONE, "B !", *(3, True))
    assert summary(read_events(device)) == [(3, CallbackID.MONOFLOP_DONE, True)]
