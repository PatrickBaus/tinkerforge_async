"""Tests for the Hall Effect Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_hall_effect import BrickletHallEffect, EdgeCountEvent, EdgeInterrupt, GetEdgeCountConfig
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletHallEffect
FunctionID = BrickletHallEffect.FunctionID
CallbackID = BrickletHallEffect.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_VALUE": 1,
    "GET_EDGE_COUNT": 2,
    "SET_EDGE_COUNT_CONFIG": 3,
    "GET_EDGE_COUNT_CONFIG": 4,
    "SET_EDGE_INTERRUPT": 5,
    "GET_EDGE_INTERRUPT": 6,
    "SET_EDGE_COUNT_CALLBACK_PERIOD": 7,
    "GET_EDGE_COUNT_CALLBACK_PERIOD": 8,
    "EDGE_INTERRUPT": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"EDGE_COUNT": 10}

CALLS: list[Call] = [
    Call("get_value", FunctionID.GET_VALUE, (), reply=("!", (True,)), result=True),
    Call("get_edge_count", FunctionID.GET_EDGE_COUNT, (True,), sent=("!", (True,)), reply=("I", (3,)), result=3),
    Call(
        "set_edge_count_config",
        FunctionID.SET_EDGE_COUNT_CONFIG,
        (DEVICE.EdgeType.BOTH, Decimal("0.003")),
        sent=("B B", (2, 3)),
    ),
    Call(
        "set_edge_count_config",
        FunctionID.SET_EDGE_COUNT_CONFIG,
        (DEVICE.EdgeType.BOTH, Decimal("0.003"), False),
        sent=("B B", (2, 3)),
        response_expected=False,
    ),
    Call(
        "get_edge_count_config",
        FunctionID.GET_EDGE_COUNT_CONFIG,
        (),
        reply=("B B", (2, 4)),
        result=GetEdgeCountConfig(DEVICE.EdgeType.BOTH, Decimal("0.004")),
    ),
    Call("set_edge_interrupt", FunctionID.SET_EDGE_INTERRUPT, (3,), sent=("I", (3,))),
    Call("set_edge_interrupt", FunctionID.SET_EDGE_INTERRUPT, (3, False), sent=("I", (3,)), response_expected=False),
    Call("get_edge_interrupt", FunctionID.GET_EDGE_INTERRUPT, (), reply=("I", (3,)), result=3),
    Call(
        "set_edge_count_callback_period",
        FunctionID.SET_EDGE_COUNT_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_edge_count_callback_period",
        FunctionID.SET_EDGE_COUNT_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_edge_count_callback_period",
        FunctionID.GET_EDGE_COUNT_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("edge_interrupt", FunctionID.EDGE_INTERRUPT, (), reply=("I !", (3, True)), result=EdgeInterrupt(3, True)),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_edge_count_config", (12345, Decimal("0.003"))),
    ("set_edge_count_config", (DEVICE.EdgeType.BOTH, Decimal("0.256"))),
    ("set_edge_interrupt", (4294967296,)),
    ("set_edge_count_callback_period", (Decimal("4294967.296"),)),
]


def test_identity(device: BrickletHallEffect) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 240
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Hall Effect Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_edge_count(device: BrickletHallEffect, connection: FakeConnection) -> None:
    """The callback EDGE_COUNT is converted to an event."""
    connection.callback(CallbackID.EDGE_COUNT, "I !", *(3, True))
    assert summary(read_events(device)) == [(0, CallbackID.EDGE_COUNT, EdgeCountEvent(3, True))]
