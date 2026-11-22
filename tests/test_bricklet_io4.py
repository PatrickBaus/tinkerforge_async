"""Tests for the IO-4 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_io4 import (
    BrickletIO4,
    GetConfiguration,
    GetEdgeCountConfig,
    GetMonoflop,
    InterruptEvent,
    MonoflopDoneEvent,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletIO4
FunctionID = BrickletIO4.FunctionID
CallbackID = BrickletIO4.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_VALUE": 1,
    "GET_VALUE": 2,
    "SET_CONFIGURATION": 3,
    "GET_CONFIGURATION": 4,
    "SET_DEBOUNCE_PERIOD": 5,
    "GET_DEBOUNCE_PERIOD": 6,
    "SET_INTERRUPT": 7,
    "GET_INTERRUPT": 8,
    "SET_MONOFLOP": 10,
    "GET_MONOFLOP": 11,
    "SET_SELECTED_VALUES": 13,
    "GET_EDGE_COUNT": 14,
    "SET_EDGE_COUNT_CONFIG": 15,
    "GET_EDGE_COUNT_CONFIG": 16,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"INTERRUPT": 9, "MONOFLOP_DONE": 12}

CALLS: list[Call] = [
    Call("set_value", FunctionID.SET_VALUE, (3,), sent=("B", (3,))),
    Call("set_value", FunctionID.SET_VALUE, (3, False), sent=("B", (3,)), response_expected=False),
    Call("get_value", FunctionID.GET_VALUE, (), reply=("B", (3,)), result=3),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (3, DEVICE.Direction.OUT, True),
        sent=("B c !", (3, "o", True)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (3, DEVICE.Direction.OUT, True, False),
        sent=("B c !", (3, "o", True)),
        response_expected=False,
    ),
    Call("get_configuration", FunctionID.GET_CONFIGURATION, (), reply=("B B", (3, 4)), result=GetConfiguration(3, 4)),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_debounce_period",
        FunctionID.SET_DEBOUNCE_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("set_interrupt", FunctionID.SET_INTERRUPT, (3,), sent=("B", (3,))),
    Call("set_interrupt", FunctionID.SET_INTERRUPT, (3, False), sent=("B", (3,)), response_expected=False),
    Call("get_interrupt", FunctionID.GET_INTERRUPT, (), reply=("B", (3,)), result=3),
    Call("set_monoflop", FunctionID.SET_MONOFLOP, (3, 3, Decimal("0.003")), sent=("B B I", (3, 3, 3))),
    Call(
        "set_monoflop",
        FunctionID.SET_MONOFLOP,
        (3, 3, Decimal("0.003"), False),
        sent=("B B I", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_monoflop",
        FunctionID.GET_MONOFLOP,
        (3,),
        sent=("B", (3,)),
        reply=("B I I", (1, 4, 5)),
        result=GetMonoflop(1, Decimal("0.004"), Decimal("0.005")),
    ),
    Call("set_selected_values", FunctionID.SET_SELECTED_VALUES, (3, 3), sent=("B B", (3, 3))),
    Call(
        "set_selected_values",
        FunctionID.SET_SELECTED_VALUES,
        (3, 3, False),
        sent=("B B", (3, 3)),
        response_expected=False,
    ),
    Call("get_edge_count", FunctionID.GET_EDGE_COUNT, (3, True), sent=("B !", (3, True)), reply=("I", (3,)), result=3),
    Call(
        "set_edge_count_config",
        FunctionID.SET_EDGE_COUNT_CONFIG,
        (3, DEVICE.EdgeType.BOTH, Decimal("0.003")),
        sent=("B B B", (3, 2, 3)),
    ),
    Call(
        "set_edge_count_config",
        FunctionID.SET_EDGE_COUNT_CONFIG,
        (3, DEVICE.EdgeType.BOTH, Decimal("0.003"), False),
        sent=("B B B", (3, 2, 3)),
        response_expected=False,
    ),
    Call(
        "get_edge_count_config",
        FunctionID.GET_EDGE_COUNT_CONFIG,
        (3,),
        sent=("B", (3,)),
        reply=("B B", (2, 4)),
        result=GetEdgeCountConfig(DEVICE.EdgeType.BOTH, Decimal("0.004")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_value", (16,)),
    ("set_configuration", (16, DEVICE.Direction.OUT, True)),
    ("set_configuration", (3, "?", True)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_interrupt", (16,)),
    ("set_monoflop", (16, 3, Decimal("0.003"))),
    ("set_monoflop", (3, 16, Decimal("0.003"))),
    ("set_monoflop", (3, 3, Decimal("4294967.296"))),
    ("get_monoflop", (4,)),
    ("set_selected_values", (16, 3)),
    ("set_selected_values", (3, 16)),
    ("get_edge_count", (4, True)),
    ("set_edge_count_config", (16, DEVICE.EdgeType.BOTH, Decimal("0.003"))),
    ("set_edge_count_config", (3, 12345, Decimal("0.003"))),
    ("set_edge_count_config", (3, DEVICE.EdgeType.BOTH, Decimal("0.256"))),
    ("get_edge_count_config", (4,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 29
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("IO-4 Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_interrupt(device, connection):
    """The callback INTERRUPT is converted to an event."""
    connection.callback(CallbackID.INTERRUPT, "B B", *(3, 4))
    assert summary(read_events(device)) == [(0, CallbackID.INTERRUPT, InterruptEvent(3, 4))]


def test_callback_monoflop_done(device, connection):
    """The callback MONOFLOP_DONE is converted to an event."""
    connection.callback(CallbackID.MONOFLOP_DONE, "B B", *(3, 4))
    assert summary(read_events(device)) == [(1, CallbackID.MONOFLOP_DONE, MonoflopDoneEvent(3, 4))]
