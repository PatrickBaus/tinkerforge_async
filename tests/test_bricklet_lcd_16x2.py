"""Tests for the LCD 16x2 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_lcd_16x2 import BrickletLCD16x2, GetConfig
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletLCD16x2
FunctionID = BrickletLCD16x2.FunctionID
CallbackID = BrickletLCD16x2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "WRITE_LINE": 1,
    "CLEAR_DISPLAY": 2,
    "BACKLIGHT_ON": 3,
    "BACKLIGHT_OFF": 4,
    "IS_BACKLIGHT_ON": 5,
    "SET_CONFIG": 6,
    "GET_CONFIG": 7,
    "IS_BUTTON_PRESSED": 8,
    "SET_CUSTOM_CHARACTER": 11,
    "GET_CUSTOM_CHARACTER": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"BUTTON_PRESSED": 9, "BUTTON_RELEASED": 10}

CALLS: list[Call] = [
    Call("write_line", FunctionID.WRITE_LINE, (1, 3, "abc"), sent=("B B 16s", (1, 3, b"abc"))),
    Call(
        "write_line",
        FunctionID.WRITE_LINE,
        (1, 3, "abc", False),
        sent=("B B 16s", (1, 3, b"abc")),
        response_expected=False,
    ),
    Call("clear_display", FunctionID.CLEAR_DISPLAY, ()),
    Call("clear_display", FunctionID.CLEAR_DISPLAY, (False,), response_expected=False),
    Call("backlight_on", FunctionID.BACKLIGHT_ON, ()),
    Call("backlight_on", FunctionID.BACKLIGHT_ON, (False,), response_expected=False),
    Call("backlight_off", FunctionID.BACKLIGHT_OFF, ()),
    Call("backlight_off", FunctionID.BACKLIGHT_OFF, (False,), response_expected=False),
    Call("is_backlight_on", FunctionID.IS_BACKLIGHT_ON, (), reply=("!", (True,)), result=True),
    Call("set_config", FunctionID.SET_CONFIG, (True, True), sent=("! !", (True, True))),
    Call("set_config", FunctionID.SET_CONFIG, (True, True, False), sent=("! !", (True, True)), response_expected=False),
    Call("get_config", FunctionID.GET_CONFIG, (), reply=("! !", (True, True)), result=GetConfig(True, True)),
    Call("is_button_pressed", FunctionID.IS_BUTTON_PRESSED, (2,), sent=("B", (2,)), reply=("!", (True,)), result=True),
    Call(
        "set_custom_character",
        FunctionID.SET_CUSTOM_CHARACTER,
        (3, [i % 256 for i in range(8)]),
        sent=("B 8B", (3, [i % 256 for i in range(8)])),
    ),
    Call(
        "set_custom_character",
        FunctionID.SET_CUSTOM_CHARACTER,
        (3, [i % 256 for i in range(8)], False),
        sent=("B 8B", (3, [i % 256 for i in range(8)])),
        response_expected=False,
    ),
    Call(
        "get_custom_character",
        FunctionID.GET_CUSTOM_CHARACTER,
        (3,),
        sent=("B", (3,)),
        reply=("8B", ([i % 256 for i in range(8)],)),
        result=tuple(i % 256 for i in range(8)),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write_line", (2, 3, "abc")),
    ("write_line", (1, 16, "abc")),
    ("write_line", (1, 3, "aaaaaaaaaaaaaaaaa")),
    ("is_button_pressed", (3,)),
    ("set_custom_character", (8, [i % 256 for i in range(8)])),
    ("set_custom_character", (3, ([i % 256 for i in range(8)])[:-1])),
    ("get_custom_character", (8,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 211
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("LCD 16x2 Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_button_pressed(device, connection):
    """The callback BUTTON_PRESSED is converted to an event."""
    connection.callback(CallbackID.BUTTON_PRESSED, "B", *(2,))
    assert summary(read_events(device)) == [(0, CallbackID.BUTTON_PRESSED, 2)]


def test_callback_button_released(device, connection):
    """The callback BUTTON_RELEASED is converted to an event."""
    connection.callback(CallbackID.BUTTON_RELEASED, "B", *(2,))
    assert summary(read_events(device)) == [(1, CallbackID.BUTTON_RELEASED, 2)]
