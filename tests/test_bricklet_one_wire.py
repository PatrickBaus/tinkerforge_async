"""Tests for the One Wire Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_one_wire import BrickletOneWire, Read, SearchBus
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletOneWire
FunctionID = BrickletOneWire.FunctionID
CallbackID = BrickletOneWire.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SEARCH_BUS_LOW_LEVEL": 1,
    "RESET_BUS": 2,
    "WRITE": 3,
    "READ": 4,
    "WRITE_COMMAND": 5,
    "SET_COMMUNICATION_LED_CONFIG": 6,
    "GET_COMMUNICATION_LED_CONFIG": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = [
    Call(
        "search_bus_low_level",
        FunctionID.SEARCH_BUS_LOW_LEVEL,
        (),
        reply=("H H 7Q B", (3, 4, [5] * 7, 4)),
        result=SearchBus(3, 4, (5,) * 7, DEVICE.Status.ERROR),
    ),
    Call("reset_bus", FunctionID.RESET_BUS, (), reply=("B", (4,)), result=DEVICE.Status.ERROR),
    Call("write", FunctionID.WRITE, (3,), sent=("B", (3,)), reply=("B", (4,)), result=DEVICE.Status.ERROR),
    Call("read", FunctionID.READ, (), reply=("B B", (3, 4)), result=Read(3, DEVICE.Status.ERROR)),
    Call(
        "write_command",
        FunctionID.WRITE_COMMAND,
        (3, 3),
        sent=("Q B", (3, 3)),
        reply=("B", (4,)),
        result=DEVICE.Status.ERROR,
    ),
    Call(
        "set_communication_led_config",
        FunctionID.SET_COMMUNICATION_LED_CONFIG,
        (DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION,),
        sent=("B", (3,)),
    ),
    Call(
        "set_communication_led_config",
        FunctionID.SET_COMMUNICATION_LED_CONFIG,
        (DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_communication_led_config",
        FunctionID.GET_COMMUNICATION_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write", (256,)),
    ("write_command", (18446744073709551616, 3)),
    ("write_command", (3, 256)),
    ("set_communication_led_config", (12345,)),
]


def test_identity(device: BrickletOneWire) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2123
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("One Wire Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_search_bus_transfers_the_stream(device: BrickletOneWire, connection: FakeConnection) -> None:
    """The high-level function search_bus() uses search_bus_low_level()."""
    data = [3] * 3
    for offset in range(0, 1, 7):
        connection.reply(FunctionID.SEARCH_BUS_LOW_LEVEL, "H H 7Q B", *(3, offset, chunk(data, offset, 7, 0), 4))
    result = run(device.search_bus())
    assert connection.requests == [request(FunctionID.SEARCH_BUS_LOW_LEVEL)] * 1
    assert result.identifier == (3,) * 3
