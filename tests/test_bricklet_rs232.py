"""Tests for the RS232 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_rs232 import BrickletRS232, GetConfiguration, Read, ReadEvent, ReadFrame
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletRS232
FunctionID = BrickletRS232.FunctionID
CallbackID = BrickletRS232.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "WRITE": 1,
    "READ": 2,
    "ENABLE_READ_CALLBACK": 3,
    "DISABLE_READ_CALLBACK": 4,
    "IS_READ_CALLBACK_ENABLED": 5,
    "SET_CONFIGURATION": 6,
    "GET_CONFIGURATION": 7,
    "SET_BREAK_CONDITION": 10,
    "SET_FRAME_READABLE_CALLBACK_CONFIGURATION": 11,
    "GET_FRAME_READABLE_CALLBACK_CONFIGURATION": 12,
    "READ_FRAME": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"READ": 8, "ERROR": 9, "FRAME_READABLE": 13}

CALLS: list[Call] = [
    Call(
        "write",
        FunctionID.WRITE,
        (("abcdefgh" * 60)[:60], 3),
        sent=("60c B", (list(("abcdefgh" * 60)[:60]), 3)),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "read",
        FunctionID.READ,
        (),
        reply=("60c B", (list(("abcdefgh" * 60)[:60]), 4)),
        result=Read(tuple(("abcdefgh" * 60)[:60]), 4),
    ),
    Call("enable_read_callback", FunctionID.ENABLE_READ_CALLBACK, ()),
    Call("enable_read_callback", FunctionID.ENABLE_READ_CALLBACK, (False,), response_expected=False),
    Call("disable_read_callback", FunctionID.DISABLE_READ_CALLBACK, ()),
    Call("disable_read_callback", FunctionID.DISABLE_READ_CALLBACK, (False,), response_expected=False),
    Call("is_read_callback_enabled", FunctionID.IS_READ_CALLBACK_ENABLED, (), reply=("!", (True,)), result=True),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (
            DEVICE.Baudrate.BAUDRATE_230400,
            DEVICE.Parity.FORCED_PARITY_0,
            DEVICE.Stopbits.STOPBITS_2,
            DEVICE.Wordlength.WORDLENGTH_8,
            DEVICE.HardwareFlowcontrol.ON,
            DEVICE.SoftwareFlowcontrol.ON,
        ),
        sent=("B B B B B B", (12, 4, 2, 8, 1, 1)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (
            DEVICE.Baudrate.BAUDRATE_230400,
            DEVICE.Parity.FORCED_PARITY_0,
            DEVICE.Stopbits.STOPBITS_2,
            DEVICE.Wordlength.WORDLENGTH_8,
            DEVICE.HardwareFlowcontrol.ON,
            DEVICE.SoftwareFlowcontrol.ON,
            False,
        ),
        sent=("B B B B B B", (12, 4, 2, 8, 1, 1)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B B B B B", (12, 4, 2, 8, 1, 1)),
        result=GetConfiguration(
            DEVICE.Baudrate.BAUDRATE_230400,
            DEVICE.Parity.FORCED_PARITY_0,
            DEVICE.Stopbits.STOPBITS_2,
            DEVICE.Wordlength.WORDLENGTH_8,
            DEVICE.HardwareFlowcontrol.ON,
            DEVICE.SoftwareFlowcontrol.ON,
        ),
    ),
    Call("set_break_condition", FunctionID.SET_BREAK_CONDITION, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_break_condition",
        FunctionID.SET_BREAK_CONDITION,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (3, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_frame_readable_callback_configuration",
        FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "read_frame",
        FunctionID.READ_FRAME,
        (),
        reply=("60c B", (list(("abcdefgh" * 60)[:60]), 4)),
        result=ReadFrame(tuple(("abcdefgh" * 60)[:60]), 4),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write", ((("abcdefgh" * 60)[:60])[:-1], 3)),
    ("write", (("abcdefgh" * 60)[:60], 61)),
    (
        "set_configuration",
        (
            12345,
            DEVICE.Parity.FORCED_PARITY_0,
            DEVICE.Stopbits.STOPBITS_2,
            DEVICE.Wordlength.WORDLENGTH_8,
            DEVICE.HardwareFlowcontrol.ON,
            DEVICE.SoftwareFlowcontrol.ON,
        ),
    ),
    (
        "set_configuration",
        (
            DEVICE.Baudrate.BAUDRATE_230400,
            12345,
            DEVICE.Stopbits.STOPBITS_2,
            DEVICE.Wordlength.WORDLENGTH_8,
            DEVICE.HardwareFlowcontrol.ON,
            DEVICE.SoftwareFlowcontrol.ON,
        ),
    ),
    (
        "set_configuration",
        (
            DEVICE.Baudrate.BAUDRATE_230400,
            DEVICE.Parity.FORCED_PARITY_0,
            12345,
            DEVICE.Wordlength.WORDLENGTH_8,
            DEVICE.HardwareFlowcontrol.ON,
            DEVICE.SoftwareFlowcontrol.ON,
        ),
    ),
    (
        "set_configuration",
        (
            DEVICE.Baudrate.BAUDRATE_230400,
            DEVICE.Parity.FORCED_PARITY_0,
            DEVICE.Stopbits.STOPBITS_2,
            12345,
            DEVICE.HardwareFlowcontrol.ON,
            DEVICE.SoftwareFlowcontrol.ON,
        ),
    ),
    (
        "set_configuration",
        (
            DEVICE.Baudrate.BAUDRATE_230400,
            DEVICE.Parity.FORCED_PARITY_0,
            DEVICE.Stopbits.STOPBITS_2,
            DEVICE.Wordlength.WORDLENGTH_8,
            12345,
            DEVICE.SoftwareFlowcontrol.ON,
        ),
    ),
    (
        "set_configuration",
        (
            DEVICE.Baudrate.BAUDRATE_230400,
            DEVICE.Parity.FORCED_PARITY_0,
            DEVICE.Stopbits.STOPBITS_2,
            DEVICE.Wordlength.WORDLENGTH_8,
            DEVICE.HardwareFlowcontrol.ON,
            12345,
        ),
    ),
    ("set_break_condition", (Decimal("65.536"),)),
    ("set_frame_readable_callback_configuration", (101,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 254
    assert device.get_api_version() == (2, 0, 3)
    assert str(device).startswith("RS232 Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_read(device, connection):
    """The callback READ is converted to an event."""
    connection.callback(CallbackID.READ, "60c B", *(list(("abcdefgh" * 60)[:60]), 4))
    assert summary(read_events(device)) == [(0, CallbackID.READ, ReadEvent(tuple(("abcdefgh" * 60)[:60]), 4))]


def test_callback_error(device, connection):
    """The callback ERROR is converted to an event."""
    connection.callback(CallbackID.ERROR, "B", *(4,))
    assert summary(read_events(device)) == [(1, CallbackID.ERROR, DEVICE.Error.FRAMING)]


def test_callback_frame_readable(device, connection):
    """The callback FRAME_READABLE is converted to an event."""
    connection.callback(CallbackID.FRAME_READABLE, "B", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.FRAME_READABLE, 3)]
