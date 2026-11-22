"""Tests for the OLED 64x48 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_oled_64x48 import BrickletOLED64x48, GetDisplayConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletOLED64x48
FunctionID = BrickletOLED64x48.FunctionID
CallbackID = BrickletOLED64x48.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "WRITE": 1,
    "NEW_WINDOW": 2,
    "CLEAR_DISPLAY": 3,
    "SET_DISPLAY_CONFIGURATION": 4,
    "GET_DISPLAY_CONFIGURATION": 5,
    "WRITE_LINE": 6,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = [
    Call("write", FunctionID.WRITE, ([i % 256 for i in range(64)],), sent=("64B", ([i % 256 for i in range(64)],))),
    Call(
        "write",
        FunctionID.WRITE,
        ([i % 256 for i in range(64)], False),
        sent=("64B", ([i % 256 for i in range(64)],)),
        response_expected=False,
    ),
    Call("new_window", FunctionID.NEW_WINDOW, (3, 3, 3, 3), sent=("B B B B", (3, 3, 3, 3))),
    Call(
        "new_window",
        FunctionID.NEW_WINDOW,
        (3, 3, 3, 3, False),
        sent=("B B B B", (3, 3, 3, 3)),
        response_expected=False,
    ),
    Call("clear_display", FunctionID.CLEAR_DISPLAY, ()),
    Call("clear_display", FunctionID.CLEAR_DISPLAY, (False,), response_expected=False),
    Call("set_display_configuration", FunctionID.SET_DISPLAY_CONFIGURATION, (3, True), sent=("B !", (3, True))),
    Call(
        "set_display_configuration",
        FunctionID.SET_DISPLAY_CONFIGURATION,
        (3, True, False),
        sent=("B !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_display_configuration",
        FunctionID.GET_DISPLAY_CONFIGURATION,
        (),
        reply=("B !", (3, True)),
        result=GetDisplayConfiguration(3, True),
    ),
    Call("write_line", FunctionID.WRITE_LINE, (3, 3, "abc"), sent=("B B 13s", (3, 3, b"abc"))),
    Call(
        "write_line",
        FunctionID.WRITE_LINE,
        (3, 3, "abc", False),
        sent=("B B 13s", (3, 3, b"abc")),
        response_expected=False,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write", (([i % 256 for i in range(64)])[:-1],)),
    ("new_window", (64, 3, 3, 3)),
    ("new_window", (3, 64, 3, 3)),
    ("new_window", (3, 3, 6, 3)),
    ("new_window", (3, 3, 3, 6)),
    ("set_display_configuration", (256, True)),
    ("write_line", (6, 3, "abc")),
    ("write_line", (3, 13, "abc")),
    ("write_line", (3, 3, "aaaaaaaaaaaaaa")),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 264
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("OLED 64x48 Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""
