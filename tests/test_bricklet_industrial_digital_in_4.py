"""Tests for the Industrial Digital In 4 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_digital_in_4 import (
    BrickletIndustrialDigitalIn4,
    GetEdgeCountConfig,
    InterruptEvent,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialDigitalIn4
FunctionID = BrickletIndustrialDigitalIn4.FunctionID
CallbackID = BrickletIndustrialDigitalIn4.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_VALUE": 1,
    "SET_GROUP": 2,
    "GET_GROUP": 3,
    "GET_AVAILABLE_FOR_GROUP": 4,
    "SET_DEBOUNCE_PERIOD": 5,
    "GET_DEBOUNCE_PERIOD": 6,
    "SET_INTERRUPT": 7,
    "GET_INTERRUPT": 8,
    "GET_EDGE_COUNT": 10,
    "SET_EDGE_COUNT_CONFIG": 11,
    "GET_EDGE_COUNT_CONFIG": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"INTERRUPT": 9}

CALLS: list[Call] = [
    Call("get_value", FunctionID.GET_VALUE, (), reply=("H", (3,)), result=3),
    Call("set_group", FunctionID.SET_GROUP, (("abcdefgh" * 4)[:4],), sent=("4c", (list(("abcdefgh" * 4)[:4]),))),
    Call(
        "set_group",
        FunctionID.SET_GROUP,
        (("abcdefgh" * 4)[:4], False),
        sent=("4c", (list(("abcdefgh" * 4)[:4]),)),
        response_expected=False,
    ),
    Call(
        "get_group",
        FunctionID.GET_GROUP,
        (),
        reply=("4c", (list(("abcdefgh" * 4)[:4]),)),
        result=tuple(("abcdefgh" * 4)[:4]),
    ),
    Call("get_available_for_group", FunctionID.GET_AVAILABLE_FOR_GROUP, (), reply=("B", (3,)), result=3),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_debounce_period",
        FunctionID.SET_DEBOUNCE_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("set_interrupt", FunctionID.SET_INTERRUPT, (3,), sent=("H", (3,))),
    Call("set_interrupt", FunctionID.SET_INTERRUPT, (3, False), sent=("H", (3,)), response_expected=False),
    Call("get_interrupt", FunctionID.GET_INTERRUPT, (), reply=("H", (3,)), result=3),
    Call("get_edge_count", FunctionID.GET_EDGE_COUNT, (3, True), sent=("B !", (3, True)), reply=("I", (3,)), result=3),
    Call(
        "set_edge_count_config",
        FunctionID.SET_EDGE_COUNT_CONFIG,
        (3, DEVICE.EdgeType.BOTH, Decimal("0.003")),
        sent=("H B B", (3, 2, 3)),
    ),
    Call(
        "set_edge_count_config",
        FunctionID.SET_EDGE_COUNT_CONFIG,
        (3, DEVICE.EdgeType.BOTH, Decimal("0.003"), False),
        sent=("H B B", (3, 2, 3)),
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
    ("set_group", ((("abcdefgh" * 4)[:4])[:-1],)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_interrupt", (65536,)),
    ("get_edge_count", (4, True)),
    ("set_edge_count_config", (65536, DEVICE.EdgeType.BOTH, Decimal("0.003"))),
    ("set_edge_count_config", (3, 12345, Decimal("0.003"))),
    ("set_edge_count_config", (3, DEVICE.EdgeType.BOTH, Decimal("0.256"))),
    ("get_edge_count_config", (256,)),
]


def test_identity(device: BrickletIndustrialDigitalIn4) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 223
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Industrial Digital In 4 Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_interrupt(device: BrickletIndustrialDigitalIn4, connection: FakeConnection) -> None:
    """The callback INTERRUPT is converted to an event."""
    connection.callback(CallbackID.INTERRUPT, "H H", *(3, 4))
    assert summary(read_events(device)) == [(0, CallbackID.INTERRUPT, InterruptEvent(3, 4))]
