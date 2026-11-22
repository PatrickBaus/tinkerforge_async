"""Tests for the LCD 20x4 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_lcd_20x4 import BrickletLCD20x4, GetConfig
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletLCD20x4
FunctionID = BrickletLCD20x4.FunctionID
CallbackID = BrickletLCD20x4.CallbackID

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
    "SET_DEFAULT_TEXT": 13,
    "GET_DEFAULT_TEXT": 14,
    "SET_DEFAULT_TEXT_COUNTER": 15,
    "GET_DEFAULT_TEXT_COUNTER": 16,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"BUTTON_PRESSED": 9, "BUTTON_RELEASED": 10}

CALLS: list[Call] = [
    Call("write_line", FunctionID.WRITE_LINE, (3, 3, "abc"), sent=("B B 20s", (3, 3, b"abc"))),
    Call(
        "write_line",
        FunctionID.WRITE_LINE,
        (3, 3, "abc", False),
        sent=("B B 20s", (3, 3, b"abc")),
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
    Call("is_button_pressed", FunctionID.IS_BUTTON_PRESSED, (3,), sent=("B", (3,)), reply=("!", (True,)), result=True),
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
    Call("set_default_text", FunctionID.SET_DEFAULT_TEXT, (3, "abc"), sent=("B 20s", (3, b"abc"))),
    Call(
        "set_default_text",
        FunctionID.SET_DEFAULT_TEXT,
        (3, "abc", False),
        sent=("B 20s", (3, b"abc")),
        response_expected=False,
    ),
    Call(
        "get_default_text", FunctionID.GET_DEFAULT_TEXT, (3,), sent=("B", (3,)), reply=("20s", (b"abc",)), result="abc"
    ),
    Call("set_default_text_counter", FunctionID.SET_DEFAULT_TEXT_COUNTER, (Decimal("0.003"),), sent=("i", (3,))),
    Call(
        "set_default_text_counter",
        FunctionID.SET_DEFAULT_TEXT_COUNTER,
        (Decimal("0.003"), False),
        sent=("i", (3,)),
        response_expected=False,
    ),
    Call(
        "get_default_text_counter", FunctionID.GET_DEFAULT_TEXT_COUNTER, (), reply=("i", (3,)), result=Decimal("0.003")
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write_line", (4, 3, "abc")),
    ("write_line", (3, 20, "abc")),
    ("is_button_pressed", (4,)),
    ("set_custom_character", (8, [i % 256 for i in range(8)])),
    ("set_custom_character", (3, ([i % 256 for i in range(8)])[:-1])),
    ("get_custom_character", (8,)),
    ("set_default_text", (4, "abc")),
    ("get_default_text", (4,)),
    ("set_default_text_counter", (Decimal("2147483.648"),)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 212
    assert device.get_api_version() == (2, 0, 2)
    assert str(device).startswith("LCD 20x4 Bricklet with uid 12345")


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
    connection.callback(CallbackID.BUTTON_PRESSED, "B", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.BUTTON_PRESSED, 3)]


def test_callback_button_released(device, connection):
    """The callback BUTTON_RELEASED is converted to an event."""
    connection.callback(CallbackID.BUTTON_RELEASED, "B", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.BUTTON_RELEASED, 3)]
