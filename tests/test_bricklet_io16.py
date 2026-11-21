"""Tests for the IO-16 Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

import pytest

from tinkerforge_async.bricklet_io16 import (
    BrickletIO16,
    GetEdgeCountConfiguration,
    GetPortConfiguration,
    GetPortMonoflop,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, InvalidSidError

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, request, run, summary

DEVICE = BrickletIO16
FunctionID = BrickletIO16.FunctionID
CallbackID = BrickletIO16.CallbackID
Port = BrickletIO16.Port
Direction = BrickletIO16.Direction
InputConfiguration = BrickletIO16.InputConfiguration
OutputConfiguration = BrickletIO16.OutputConfiguration
EdgeType = BrickletIO16.EdgeType

CALLS = [
    Call("set_port", FunctionID.SET_PORT, (Port.A, 0b10101010), sent=("c B", (b"a", 0b10101010))),
    # The port may be given as a string in upper or lower case
    Call("set_port", FunctionID.SET_PORT, ("B", 255, False), sent=("c B", (b"b", 255)), response_expected=False),
    Call("get_port", FunctionID.GET_PORT, (Port.B,), sent=("c", (b"b",)), reply=("B", (0b1111,)), result=0b1111),
    Call("get_port", FunctionID.GET_PORT, ("a",), sent=("c", (b"a",)), reply=("B", (0,)), result=0),
    Call(
        "set_port_configuration",
        FunctionID.SET_PORT_CONFIGURATION,
        (Port.A, 0b11, Direction.IN),
        sent=("c B c !", (b"a", 0b11, b"i", False)),
    ),
    Call(
        "set_port_configuration",
        FunctionID.SET_PORT_CONFIGURATION,
        ("b", 255, "i", InputConfiguration.PULL_UP),
        sent=("c B c !", (b"b", 255, b"i", True)),
    ),
    Call(
        "set_port_configuration",
        FunctionID.SET_PORT_CONFIGURATION,
        ("b", 1, "o", OutputConfiguration.LOW),
        sent=("c B c !", (b"b", 1, b"o", False)),
    ),
    Call(
        "set_port_configuration",
        FunctionID.SET_PORT_CONFIGURATION,
        ("a", 1, Direction.OUT, True),
        sent=("c B c !", (b"a", 1, b"o", True)),
    ),
    Call(
        "get_port_configuration",
        FunctionID.GET_PORT_CONFIGURATION,
        (Port.A,),
        sent=("c", (b"a",)),
        reply=("B B", (0b1100, 0b0101)),
        result=GetPortConfiguration(0b1100, 0b0101),
    ),
    Call(
        "get_port_configuration",
        FunctionID.GET_PORT_CONFIGURATION,
        ("B",),
        sent=("c", (b"b",)),
        reply=("B B", (0, 0)),
        result=GetPortConfiguration(0, 0),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (2,), sent=("I", (2000,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
    Call("set_port_interrupt", FunctionID.SET_PORT_INTERRUPT, (Port.A, 0b11), sent=("c B", (b"a", 0b11))),
    Call("set_port_interrupt", FunctionID.SET_PORT_INTERRUPT, ("b", 0), sent=("c B", (b"b", 0))),
    Call(
        "get_port_interrupt", FunctionID.GET_PORT_INTERRUPT, (Port.A,), sent=("c", (b"a",)), reply=("B", (3,)), result=3
    ),
    Call("get_port_interrupt", FunctionID.GET_PORT_INTERRUPT, ("b",), sent=("c", (b"b",)), reply=("B", (0,)), result=0),
    Call(
        "set_port_monoflop",
        FunctionID.SET_PORT_MONOFLOP,
        (Port.A, 0b11, 0b01, Decimal("1.5")),
        sent=("c B B I", (b"a", 0b11, 0b01, 1500)),
    ),
    Call(
        "set_port_monoflop",
        FunctionID.SET_PORT_MONOFLOP,
        ("b", 255, 0, 0),
        sent=("c B B I", (b"b", 255, 0, 0)),
    ),
    Call(
        "get_port_monoflop",
        FunctionID.GET_PORT_MONOFLOP,
        (Port.A, 7),
        sent=("c B", (b"a", 7)),
        reply=("B I I", (1, 1500, 500)),
        result=GetPortMonoflop(1, Decimal("1.5"), Decimal("0.5")),
    ),
    Call(
        "get_port_monoflop",
        FunctionID.GET_PORT_MONOFLOP,
        ("b", 0),
        sent=("c B", (b"b", 0)),
        reply=("B I I", (0, 0, 0)),
        result=GetPortMonoflop(0, Decimal(0), Decimal(0)),
    ),
    Call(
        "set_selected_values",
        FunctionID.SET_SELECTED_VALUES,
        (Port.A, 0b11, 0b01),
        sent=("c B B", (b"a", 0b11, 0b01)),
    ),
    Call("set_selected_values", FunctionID.SET_SELECTED_VALUES, ("b", 255, 255), sent=("c B B", (b"b", 255, 255))),
    Call("get_edge_count", FunctionID.GET_EDGE_COUNT, (0,), sent=("B !", (0, False)), reply=("I", (42,)), result=42),
    Call("get_edge_count", FunctionID.GET_EDGE_COUNT, (1, True), sent=("B !", (1, True)), reply=("I", (0,)), result=0),
    Call("set_edge_count_config", FunctionID.SET_EDGE_COUNT_CONFIG, (0,), sent=("B B B", (0, 0, 100))),
    Call(
        "set_edge_count_config",
        FunctionID.SET_EDGE_COUNT_CONFIG,
        (1, EdgeType.BOTH, Decimal("0.255")),
        sent=("B B B", (1, 2, 255)),
    ),
    Call("set_edge_count_config", FunctionID.SET_EDGE_COUNT_CONFIG, (1, 1, 0), sent=("B B B", (1, 1, 0))),
    Call(
        "get_edge_count_config",
        FunctionID.GET_EDGE_COUNT_CONFIG,
        (1,),
        sent=("B", (1,)),
        reply=("B B", (1, 100)),
        result=GetEdgeCountConfiguration(EdgeType.FALLING, Decimal("0.1")),
    ),
]

REJECTED = [
    ("set_port", ("c", 0)),
    ("set_port", ("a", -1)),
    ("set_port", ("a", 256)),
    ("set_port", ("a", 1.0)),
    ("get_port", ("c",)),
    ("set_port_configuration", ("c", 0, "i")),
    ("set_port_configuration", ("a", -1, "i")),
    ("set_port_configuration", ("a", 256, "i")),
    ("set_port_configuration", ("a", 0, "x")),
    ("get_port_configuration", ("c",)),
    ("set_debounce_period", (-1,)),
    ("set_port_interrupt", ("c", 0)),
    ("set_port_interrupt", ("a", -1)),
    ("set_port_interrupt", ("a", 256)),
    ("get_port_interrupt", ("c",)),
    ("set_port_monoflop", ("c", 0, 0, 1)),
    ("set_port_monoflop", ("a", 256, 0, 1)),
    ("set_port_monoflop", ("a", 0, 256, 1)),
    ("set_port_monoflop", ("a", 0, 0, -1)),
    ("get_port_monoflop", ("c", 0)),
    ("get_port_monoflop", ("a", 8)),
    ("get_port_monoflop", ("a", -1)),
    ("set_selected_values", ("c", 0, 0)),
    ("set_selected_values", ("a", 256, 0)),
    ("set_selected_values", ("a", 0, 256)),
    ("get_edge_count", (2,)),
    ("set_edge_count_config", (2,)),
    ("set_edge_count_config", (0, 3)),
    ("set_edge_count_config", (0, 0, -1)),
    ("set_edge_count_config", (0, 0, Decimal("0.256"))),
    ("get_edge_count_config", (2,)),
    # The sids are the pins 0 to 15
    ("set_callback_configuration", (16,)),
    ("get_callback_configuration", (-1,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 28
    assert bricklet.get_api_version() == (2, 0, 1)
    assert str(bricklet).startswith("IO-16 Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


@pytest.mark.parametrize(
    "sid, period, port, old_mask, new_mask",
    [
        (0, 1, b"a", 0b0000_0000, 0b0000_0001),  # enable the first pin of port a
        (7, 1, b"a", 0b0000_0001, 0b1000_0001),  # the interrupts of the other pins are kept
        (7, 0, b"a", 0b1000_0001, 0b0000_0001),  # disable
        (0, 0, b"a", 0b0000_0000, 0b0000_0000),  # disable an interrupt, that is not enabled
        (8, 1, b"b", 0b0000_0000, 0b0000_0001),  # the first pin of port b
        (15, Decimal("0.1"), b"b", 0b0000_1111, 0b1000_1111),
    ],
)
def test_set_callback_configuration(
    bricklet, connection, sid, period, port, old_mask, new_mask
):  # pylint: disable=too-many-arguments,too-many-positional-arguments
    """A period other than 0 enables the interrupt of the pin. The interrupts have neither a period nor thresholds."""
    connection.reply(FunctionID.GET_PORT_INTERRUPT, "B", old_mask)
    run(bricklet.set_callback_configuration(sid, period))
    assert connection.requests == [
        request(FunctionID.GET_PORT_INTERRUPT, "c", port),
        request(FunctionID.SET_PORT_INTERRUPT, "c B", port, new_mask),
    ]


@pytest.mark.parametrize(
    "sid, port, mask, enabled",
    [(0, b"a", 0b1, True), (1, b"a", 0b1, False), (8, b"b", 0b1, True), (15, b"b", 0b0111_1111, False)],
)
def test_get_callback_configuration(
    bricklet, connection, sid, port, mask, enabled
):  # pylint: disable=too-many-arguments,too-many-positional-arguments
    """The period is 1, if the interrupt of the pin is enabled."""
    connection.reply(FunctionID.GET_PORT_INTERRUPT, "B", mask)
    assert run(bricklet.get_callback_configuration(sid)) == AdvancedCallbackConfiguration(
        Decimal(int(enabled)), False, None, None, None
    )
    assert connection.requests == [request(FunctionID.GET_PORT_INTERRUPT, "c", port)]


def test_events_of_ports(bricklet, connection):
    """Without a filter by sid, one event per port is yielded. Its sid is 16, the payload is the value of all pins."""
    connection.callback(CallbackID.INTERRUPT, "c B B", "a", 0b0000_0101, 0b0000_0100)
    connection.callback(CallbackID.MONOFLOP_DONE, "c B B", "b", 0b0000_0001, 0b1000_0001)
    events = read_events(bricklet)
    assert summary(events) == [
        (16, CallbackID.INTERRUPT, 0b0000_0100),
        (16, CallbackID.MONOFLOP_DONE, 0b1000_0001_0000_0000),  # The port b are the upper 8 bits
    ]
    # The pins that changed
    assert [event.additional for event in events] == [0b0000_0101, 0b0000_0001_0000_0000]
    assert summary(read_events(bricklet, events=(CallbackID.INTERRUPT,))) == [(16, CallbackID.INTERRUPT, 0b0000_0100)]


def test_events_of_pins(bricklet, connection):
    """With a filter by sid, one event is yielded for each of the pins that changed. The payload is the new value."""
    connection.callback(CallbackID.INTERRUPT, "c B B", "a", 0b0000_0101, 0b0000_0100)
    connection.callback(CallbackID.INTERRUPT, "c B B", "b", 0b0000_0011, 0b1000_0001)
    assert summary(read_events(bricklet, sids=range(16))) == [
        (0, CallbackID.INTERRUPT, False),
        (2, CallbackID.INTERRUPT, True),
        (8, CallbackID.INTERRUPT, True),
        (9, CallbackID.INTERRUPT, False),
    ]
    assert summary(read_events(bricklet, sids=(2, 9, 15))) == [
        (2, CallbackID.INTERRUPT, True),
        (9, CallbackID.INTERRUPT, False),
    ]


def test_invalid_event_filters_are_rejected(bricklet):
    """The events are either filtered by callback or by sid. Unknown sids are rejected."""
    with pytest.raises(ValueError):
        read_events(bricklet, events=(CallbackID.INTERRUPT,), sids=(0,))
    with pytest.raises(InvalidSidError):
        read_events(bricklet, sids=(16,))
