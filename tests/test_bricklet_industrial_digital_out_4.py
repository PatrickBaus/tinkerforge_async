"""Tests for the Industrial Digital Out 4 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_digital_out_4 import (
    BrickletIndustrialDigitalOut4,
    GetMonoflop,
    MonoflopDoneEvent,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialDigitalOut4
FunctionID = BrickletIndustrialDigitalOut4.FunctionID
CallbackID = BrickletIndustrialDigitalOut4.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_VALUE": 1,
    "GET_VALUE": 2,
    "SET_MONOFLOP": 3,
    "GET_MONOFLOP": 4,
    "SET_GROUP": 5,
    "GET_GROUP": 6,
    "GET_AVAILABLE_FOR_GROUP": 7,
    "SET_SELECTED_VALUES": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"MONOFLOP_DONE": 8}

CALLS: list[Call] = [
    Call("set_value", FunctionID.SET_VALUE, (3,), sent=("H", (3,))),
    Call("set_value", FunctionID.SET_VALUE, (3, False), sent=("H", (3,)), response_expected=False),
    Call("get_value", FunctionID.GET_VALUE, (), reply=("H", (3,)), result=3),
    Call("set_monoflop", FunctionID.SET_MONOFLOP, (3, 3, Decimal("0.003")), sent=("H H I", (3, 3, 3))),
    Call(
        "set_monoflop",
        FunctionID.SET_MONOFLOP,
        (3, 3, Decimal("0.003"), False),
        sent=("H H I", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_monoflop",
        FunctionID.GET_MONOFLOP,
        (3,),
        sent=("B", (3,)),
        reply=("H I I", (1, 4, 5)),
        result=GetMonoflop(1, Decimal("0.004"), Decimal("0.005")),
    ),
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
    Call("set_selected_values", FunctionID.SET_SELECTED_VALUES, (3, 3), sent=("H H", (3, 3))),
    Call(
        "set_selected_values",
        FunctionID.SET_SELECTED_VALUES,
        (3, 3, False),
        sent=("H H", (3, 3)),
        response_expected=False,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_value", (65536,)),
    ("set_monoflop", (65536, 3, Decimal("0.003"))),
    ("set_monoflop", (3, 65536, Decimal("0.003"))),
    ("set_monoflop", (3, 3, Decimal("4294967.296"))),
    ("get_monoflop", (16,)),
    ("set_group", ((("abcdefgh" * 4)[:4])[:-1],)),
    ("set_selected_values", (65536, 3)),
    ("set_selected_values", (3, 65536)),
]


def test_identity(device: BrickletIndustrialDigitalOut4) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 224
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Digital Out 4 Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_monoflop_done(device: BrickletIndustrialDigitalOut4, connection: FakeConnection) -> None:
    """The callback MONOFLOP_DONE is converted to an event."""
    connection.callback(CallbackID.MONOFLOP_DONE, "H H", *(3, 4))
    assert summary(read_events(device)) == [(0, CallbackID.MONOFLOP_DONE, MonoflopDoneEvent(3, 4))]
