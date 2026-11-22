"""Tests for the CAN Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_can import (
    BrickletCAN,
    FrameReadEvent,
    GetConfiguration,
    GetErrorLog,
    GetReadFilter,
    ReadFrame,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletCAN
FunctionID = BrickletCAN.FunctionID
CallbackID = BrickletCAN.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "WRITE_FRAME": 1,
    "READ_FRAME": 2,
    "ENABLE_FRAME_READ_CALLBACK": 3,
    "DISABLE_FRAME_READ_CALLBACK": 4,
    "IS_FRAME_READ_CALLBACK_ENABLED": 5,
    "SET_CONFIGURATION": 6,
    "GET_CONFIGURATION": 7,
    "SET_READ_FILTER": 8,
    "GET_READ_FILTER": 9,
    "GET_ERROR_LOG": 10,
    "SET_FRAME_READABLE_CALLBACK_CONFIGURATION": 12,
    "GET_FRAME_READABLE_CALLBACK_CONFIGURATION": 13,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"FRAME_READ": 11, "FRAME_READABLE": 14}

CALLS: list[Call] = [
    Call(
        "write_frame",
        FunctionID.WRITE_FRAME,
        (DEVICE.FrameType.EXTENDED_REMOTE, 3, [i % 256 for i in range(8)], 3),
        sent=("B I 8B B", (3, 3, [i % 256 for i in range(8)], 3)),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "read_frame",
        FunctionID.READ_FRAME,
        (),
        reply=("! B I 8B B", (True, 3, 5, [i % 256 for i in range(8)], 7)),
        result=ReadFrame(True, DEVICE.FrameType.EXTENDED_REMOTE, 5, tuple(i % 256 for i in range(8)), 7),
    ),
    Call("enable_frame_read_callback", FunctionID.ENABLE_FRAME_READ_CALLBACK, ()),
    Call("enable_frame_read_callback", FunctionID.ENABLE_FRAME_READ_CALLBACK, (False,), response_expected=False),
    Call("disable_frame_read_callback", FunctionID.DISABLE_FRAME_READ_CALLBACK, ()),
    Call("disable_frame_read_callback", FunctionID.DISABLE_FRAME_READ_CALLBACK, (False,), response_expected=False),
    Call(
        "is_frame_read_callback_enabled",
        FunctionID.IS_FRAME_READ_CALLBACK_ENABLED,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.BaudRate.BAUD_RATE_1000KBPS, DEVICE.TransceiverMode.READ_ONLY, 3),
        sent=("B B i", (7, 2, 3)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.BaudRate.BAUD_RATE_1000KBPS, DEVICE.TransceiverMode.READ_ONLY, 3, False),
        sent=("B B i", (7, 2, 3)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B i", (7, 2, 5)),
        result=GetConfiguration(DEVICE.BaudRate.BAUD_RATE_1000KBPS, DEVICE.TransceiverMode.READ_ONLY, 5),
    ),
    Call(
        "set_read_filter",
        FunctionID.SET_READ_FILTER,
        (DEVICE.FilterMode.MATCH_EXTENDED, 3, 3, 3),
        sent=("B I I I", (4, 3, 3, 3)),
    ),
    Call(
        "set_read_filter",
        FunctionID.SET_READ_FILTER,
        (DEVICE.FilterMode.MATCH_EXTENDED, 3, 3, 3, False),
        sent=("B I I I", (4, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_read_filter",
        FunctionID.GET_READ_FILTER,
        (),
        reply=("B I I I", (4, 4, 5, 6)),
        result=GetReadFilter(DEVICE.FilterMode.MATCH_EXTENDED, 4, 5, 6),
    ),
    Call(
        "get_error_log",
        FunctionID.GET_ERROR_LOG,
        (),
        reply=("B B ! I I I", (3, 4, True, 6, 7, 8)),
        result=GetErrorLog(3, 4, True, 6, 7, 8),
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_frame_readable_callback_configuration",
        FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write_frame", (12345, 3, [i % 256 for i in range(8)], 3)),
    ("write_frame", (DEVICE.FrameType.EXTENDED_REMOTE, 1073741824, [i % 256 for i in range(8)], 3)),
    ("write_frame", (DEVICE.FrameType.EXTENDED_REMOTE, 3, ([i % 256 for i in range(8)])[:-1], 3)),
    ("write_frame", (DEVICE.FrameType.EXTENDED_REMOTE, 3, [i % 256 for i in range(8)], 16)),
    ("set_configuration", (12345, DEVICE.TransceiverMode.READ_ONLY, 3)),
    ("set_configuration", (DEVICE.BaudRate.BAUD_RATE_1000KBPS, 12345, 3)),
    ("set_configuration", (DEVICE.BaudRate.BAUD_RATE_1000KBPS, DEVICE.TransceiverMode.READ_ONLY, 2147483648)),
    ("set_read_filter", (12345, 3, 3, 3)),
    ("set_read_filter", (DEVICE.FilterMode.MATCH_EXTENDED, 1073741824, 3, 3)),
    ("set_read_filter", (DEVICE.FilterMode.MATCH_EXTENDED, 3, 1073741824, 3)),
    ("set_read_filter", (DEVICE.FilterMode.MATCH_EXTENDED, 3, 3, 1073741824)),
]


def test_identity(device: BrickletCAN) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 270
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("CAN Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_frame_read(device: BrickletCAN, connection: FakeConnection) -> None:
    """The callback FRAME_READ is converted to an event."""
    connection.callback(CallbackID.FRAME_READ, "B I 8B B", *(3, 4, [i % 256 for i in range(8)], 6))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.FRAME_READ,
            FrameReadEvent(DEVICE.FrameType.EXTENDED_REMOTE, 4, tuple(i % 256 for i in range(8)), 6),
        )
    ]


def test_callback_frame_readable(device: BrickletCAN, connection: FakeConnection) -> None:
    """The callback FRAME_READABLE is converted to an event."""
    connection.callback(CallbackID.FRAME_READABLE)
    assert summary(read_events(device)) == [(1, CallbackID.FRAME_READABLE, None)]
