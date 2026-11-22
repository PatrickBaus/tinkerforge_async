"""Tests for the Industrial Dual Relay Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_dual_relay import BrickletIndustrialDualRelay, GetMonoflop, GetValue
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialDualRelay
FunctionID = BrickletIndustrialDualRelay.FunctionID
CallbackID = BrickletIndustrialDualRelay.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_VALUE": 1,
    "GET_VALUE": 2,
    "SET_MONOFLOP": 3,
    "GET_MONOFLOP": 4,
    "SET_SELECTED_VALUE": 6,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"MONOFLOP_DONE": 5}

CALLS: list[Call] = [
    Call("set_value", FunctionID.SET_VALUE, (True, True), sent=("! !", (True, True))),
    Call("set_value", FunctionID.SET_VALUE, (True, True, False), sent=("! !", (True, True)), response_expected=False),
    Call("get_value", FunctionID.GET_VALUE, (), reply=("! !", (True, True)), result=GetValue(True, True)),
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
    ("set_monoflop", (2, True, Decimal("0.003"))),
    ("set_monoflop", (1, True, Decimal("4294967.296"))),
    ("get_monoflop", (2,)),
    ("set_selected_value", (2, True)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 284
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Dual Relay Bricklet with uid 12345")


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
