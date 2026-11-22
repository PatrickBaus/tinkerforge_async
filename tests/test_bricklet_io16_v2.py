"""Tests for the IO-16 Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_io16_v2 import (
    AllInputValueEvent,
    BrickletIO16V2,
    GetConfiguration,
    GetEdgeCountConfiguration,
    GetMonoflop,
    InputValueEvent,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletIO16V2
FunctionID = BrickletIO16V2.FunctionID
CallbackID = BrickletIO16V2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_VALUE": 1,
    "GET_VALUE": 2,
    "SET_SELECTED_VALUE": 3,
    "SET_CONFIGURATION": 4,
    "GET_CONFIGURATION": 5,
    "SET_INPUT_VALUE_CALLBACK_CONFIGURATION": 6,
    "GET_INPUT_VALUE_CALLBACK_CONFIGURATION": 7,
    "SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION": 8,
    "GET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION": 9,
    "SET_MONOFLOP": 10,
    "GET_MONOFLOP": 11,
    "GET_EDGE_COUNT": 12,
    "SET_EDGE_COUNT_CONFIGURATION": 13,
    "GET_EDGE_COUNT_CONFIGURATION": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"INPUT_VALUE": 15, "ALL_INPUT_VALUE": 16, "MONOFLOP_DONE": 17}

CALLS: list[Call] = [
    Call(
        "set_value",
        FunctionID.SET_VALUE,
        ([i % 2 == 0 for i in range(16)],),
        sent=("16!", ([i % 2 == 0 for i in range(16)],)),
    ),
    Call(
        "set_value",
        FunctionID.SET_VALUE,
        ([i % 2 == 0 for i in range(16)], False),
        sent=("16!", ([i % 2 == 0 for i in range(16)],)),
        response_expected=False,
    ),
    Call(
        "get_value",
        FunctionID.GET_VALUE,
        (),
        reply=("16!", ([i % 2 == 0 for i in range(16)],)),
        result=tuple(i % 2 == 0 for i in range(16)),
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
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
        reply=("c !", ("o", True)),
        result=GetConfiguration(DEVICE.Direction.OUT, True),
    ),
    Call(
        "set_input_value_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (3, Decimal("0.003"), True),
        sent=("B I !", (3, 3, True)),
    ),
    Call(
        "set_input_value_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (3, Decimal("0.003"), True, False),
        sent=("B I !", (3, 3, True)),
        response_expected=False,
    ),
    Call(
        "get_input_value_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_all_input_value_callback_configuration",
        FunctionID.SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_all_input_value_callback_configuration",
        FunctionID.SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_all_input_value_callback_configuration",
        FunctionID.GET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
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
    Call("get_edge_count", FunctionID.GET_EDGE_COUNT, (3, True), sent=("B !", (3, True)), reply=("I", (3,)), result=3),
    Call(
        "set_edge_count_configuration",
        FunctionID.SET_EDGE_COUNT_CONFIGURATION,
        (3, DEVICE.EdgeType.BOTH, Decimal("0.003")),
        sent=("B B B", (3, 2, 3)),
    ),
    Call(
        "set_edge_count_configuration",
        FunctionID.SET_EDGE_COUNT_CONFIGURATION,
        (3, DEVICE.EdgeType.BOTH, Decimal("0.003"), False),
        sent=("B B B", (3, 2, 3)),
        response_expected=False,
    ),
    Call(
        "get_edge_count_configuration",
        FunctionID.GET_EDGE_COUNT_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
        reply=("B B", (2, 4)),
        result=GetEdgeCountConfiguration(DEVICE.EdgeType.BOTH, Decimal("0.004")),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("B I !", (0, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (0,),
        sent=("B", (0,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("B I !", (1, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (1,),
        sent=("B", (1,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (2, 1, True),
        sent=("B I !", (2, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (2,),
        sent=("B", (2,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (3, 1, True),
        sent=("B I !", (3, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (4, 1, True),
        sent=("B I !", (4, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (4,),
        sent=("B", (4,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (5, 1, True),
        sent=("B I !", (5, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (5,),
        sent=("B", (5,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (6, 1, True),
        sent=("B I !", (6, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (6,),
        sent=("B", (6,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (7, 1, True),
        sent=("B I !", (7, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (7,),
        sent=("B", (7,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (8, 1, True),
        sent=("B I !", (8, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (8,),
        sent=("B", (8,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (9, 1, True),
        sent=("B I !", (9, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (9,),
        sent=("B", (9,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (10, 1, True),
        sent=("B I !", (10, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (10,),
        sent=("B", (10,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (11, 1, True),
        sent=("B I !", (11, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (11,),
        sent=("B", (11,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (12, 1, True),
        sent=("B I !", (12, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (12,),
        sent=("B", (12,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (13, 1, True),
        sent=("B I !", (13, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (13,),
        sent=("B", (13,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (14, 1, True),
        sent=("B I !", (14, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (14,),
        sent=("B", (14,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (15, 1, True),
        sent=("B I !", (15, 1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (15,),
        sent=("B", (15,)),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (16, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (16,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_value", (([i % 2 == 0 for i in range(16)])[:-1],)),
    ("set_selected_value", (16, True)),
    ("set_configuration", (16, DEVICE.Direction.OUT, True)),
    ("set_configuration", (3, "?", True)),
    ("get_configuration", (16,)),
    ("set_input_value_callback_configuration", (16, Decimal("0.003"), True)),
    ("set_input_value_callback_configuration", (3, Decimal("4294967.296"), True)),
    ("get_input_value_callback_configuration", (16,)),
    ("set_all_input_value_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_monoflop", (16, True, Decimal("0.003"))),
    ("set_monoflop", (3, True, Decimal("4294967.296"))),
    ("get_monoflop", (16,)),
    ("get_edge_count", (16, True)),
    ("set_edge_count_configuration", (16, DEVICE.EdgeType.BOTH, Decimal("0.003"))),
    ("set_edge_count_configuration", (3, 12345, Decimal("0.003"))),
    ("set_edge_count_configuration", (3, DEVICE.EdgeType.BOTH, Decimal("0.256"))),
    ("get_edge_count_configuration", (16,)),
    ("set_callback_configuration", (33,)),
    ("get_callback_configuration", (33,)),
]


def test_identity(device: BrickletIO16V2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2114
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("IO-16 Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_input_value(device: BrickletIO16V2, connection: FakeConnection) -> None:
    """The callback INPUT_VALUE is converted to an event."""
    connection.callback(CallbackID.INPUT_VALUE, "B ! !", *(15, True, True))
    assert summary(read_events(device)) == [(15, CallbackID.INPUT_VALUE, InputValueEvent(True, True))]


def test_callback_all_input_value(device: BrickletIO16V2, connection: FakeConnection) -> None:
    """The callback ALL_INPUT_VALUE is converted to an event."""
    connection.callback(
        CallbackID.ALL_INPUT_VALUE, "16! 16!", *([i % 2 == 0 for i in range(16)], [i % 2 == 0 for i in range(16)])
    )
    assert summary(read_events(device)) == [
        (
            16,
            CallbackID.ALL_INPUT_VALUE,
            AllInputValueEvent(tuple(i % 2 == 0 for i in range(16)), tuple(i % 2 == 0 for i in range(16))),
        )
    ]


def test_callback_monoflop_done(device: BrickletIO16V2, connection: FakeConnection) -> None:
    """The callback MONOFLOP_DONE is converted to an event."""
    connection.callback(CallbackID.MONOFLOP_DONE, "B !", *(15, True))
    assert summary(read_events(device)) == [(32, CallbackID.MONOFLOP_DONE, True)]
