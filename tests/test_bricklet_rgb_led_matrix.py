"""Tests for the RGB LED Matrix Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_rgb_led_matrix import BrickletRGBLEDMatrix
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletRGBLEDMatrix
FunctionID = BrickletRGBLEDMatrix.FunctionID
CallbackID = BrickletRGBLEDMatrix.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_RED": 1,
    "GET_RED": 2,
    "SET_GREEN": 3,
    "GET_GREEN": 4,
    "SET_BLUE": 5,
    "GET_BLUE": 6,
    "SET_FRAME_DURATION": 7,
    "GET_FRAME_DURATION": 8,
    "DRAW_FRAME": 9,
    "GET_SUPPLY_VOLTAGE": 10,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"FRAME_STARTED": 11}

CALLS: list[Call] = [
    Call("set_red", FunctionID.SET_RED, ([i % 256 for i in range(64)],), sent=("64B", ([i % 256 for i in range(64)],))),
    Call(
        "set_red",
        FunctionID.SET_RED,
        ([i % 256 for i in range(64)], False),
        sent=("64B", ([i % 256 for i in range(64)],)),
        response_expected=False,
    ),
    Call(
        "get_red",
        FunctionID.GET_RED,
        (),
        reply=("64B", ([i % 256 for i in range(64)],)),
        result=tuple(i % 256 for i in range(64)),
    ),
    Call(
        "set_green",
        FunctionID.SET_GREEN,
        ([i % 256 for i in range(64)],),
        sent=("64B", ([i % 256 for i in range(64)],)),
    ),
    Call(
        "set_green",
        FunctionID.SET_GREEN,
        ([i % 256 for i in range(64)], False),
        sent=("64B", ([i % 256 for i in range(64)],)),
        response_expected=False,
    ),
    Call(
        "get_green",
        FunctionID.GET_GREEN,
        (),
        reply=("64B", ([i % 256 for i in range(64)],)),
        result=tuple(i % 256 for i in range(64)),
    ),
    Call(
        "set_blue", FunctionID.SET_BLUE, ([i % 256 for i in range(64)],), sent=("64B", ([i % 256 for i in range(64)],))
    ),
    Call(
        "set_blue",
        FunctionID.SET_BLUE,
        ([i % 256 for i in range(64)], False),
        sent=("64B", ([i % 256 for i in range(64)],)),
        response_expected=False,
    ),
    Call(
        "get_blue",
        FunctionID.GET_BLUE,
        (),
        reply=("64B", ([i % 256 for i in range(64)],)),
        result=tuple(i % 256 for i in range(64)),
    ),
    Call("set_frame_duration", FunctionID.SET_FRAME_DURATION, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_frame_duration",
        FunctionID.SET_FRAME_DURATION,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_frame_duration", FunctionID.GET_FRAME_DURATION, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("draw_frame", FunctionID.DRAW_FRAME, ()),
    Call("draw_frame", FunctionID.DRAW_FRAME, (False,), response_expected=False),
    Call("get_supply_voltage", FunctionID.GET_SUPPLY_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_red", (([i % 256 for i in range(64)])[:-1],)),
    ("set_green", (([i % 256 for i in range(64)])[:-1],)),
    ("set_blue", (([i % 256 for i in range(64)])[:-1],)),
    ("set_frame_duration", (Decimal("65.536"),)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 272
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("RGB LED Matrix Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_frame_started(device, connection):
    """The callback FRAME_STARTED is converted to an event."""
    connection.callback(CallbackID.FRAME_STARTED, "I", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.FRAME_STARTED, 3)]
