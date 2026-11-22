"""Tests for the E-Paper 296x128 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_e_paper_296x128 import BrickletEPaper296x128, ReadBlackWhite, ReadColor
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletEPaper296x128
FunctionID = BrickletEPaper296x128.FunctionID
CallbackID = BrickletEPaper296x128.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "DRAW": 1,
    "GET_DRAW_STATUS": 2,
    "WRITE_BLACK_WHITE_LOW_LEVEL": 3,
    "READ_BLACK_WHITE_LOW_LEVEL": 4,
    "WRITE_COLOR_LOW_LEVEL": 5,
    "READ_COLOR_LOW_LEVEL": 6,
    "FILL_DISPLAY": 7,
    "DRAW_TEXT": 8,
    "DRAW_LINE": 9,
    "DRAW_BOX": 10,
    "SET_UPDATE_MODE": 12,
    "GET_UPDATE_MODE": 13,
    "SET_DISPLAY_TYPE": 14,
    "GET_DISPLAY_TYPE": 15,
    "SET_DISPLAY_DRIVER": 16,
    "GET_DISPLAY_DRIVER": 17,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DRAW_STATUS": 11}

CALLS: list[Call] = [
    Call("draw", FunctionID.DRAW, ()),
    Call("draw", FunctionID.DRAW, (False,), response_expected=False),
    Call("get_draw_status", FunctionID.GET_DRAW_STATUS, (), reply=("B", (2,)), result=DEVICE.DrawStatus.DRAWING),
    Call(
        "write_black_white_low_level",
        FunctionID.WRITE_BLACK_WHITE_LOW_LEVEL,
        (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)]),
        sent=("H B H B H H 432!", (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
    ),
    Call(
        "write_black_white_low_level",
        FunctionID.WRITE_BLACK_WHITE_LOW_LEVEL,
        (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)], False),
        sent=("H B H B H H 432!", (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
        response_expected=False,
    ),
    Call(
        "read_black_white_low_level",
        FunctionID.READ_BLACK_WHITE_LOW_LEVEL,
        (3, 3, 3, 3),
        sent=("H B H B", (3, 3, 3, 3)),
        reply=("H H 464!", (3, 4, [i % 2 == 0 for i in range(464)])),
        result=ReadBlackWhite(3, 4, tuple(i % 2 == 0 for i in range(464))),
    ),
    Call(
        "write_color_low_level",
        FunctionID.WRITE_COLOR_LOW_LEVEL,
        (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)]),
        sent=("H B H B H H 432!", (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
    ),
    Call(
        "write_color_low_level",
        FunctionID.WRITE_COLOR_LOW_LEVEL,
        (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)], False),
        sent=("H B H B H H 432!", (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
        response_expected=False,
    ),
    Call(
        "read_color_low_level",
        FunctionID.READ_COLOR_LOW_LEVEL,
        (3, 3, 3, 3),
        sent=("H B H B", (3, 3, 3, 3)),
        reply=("H H 464!", (3, 4, [i % 2 == 0 for i in range(464)])),
        result=ReadColor(3, 4, tuple(i % 2 == 0 for i in range(464))),
    ),
    Call("fill_display", FunctionID.FILL_DISPLAY, (DEVICE.Color.GRAY,), sent=("B", (2,))),
    Call(
        "fill_display", FunctionID.FILL_DISPLAY, (DEVICE.Color.GRAY, False), sent=("B", (2,)), response_expected=False
    ),
    Call(
        "draw_text",
        FunctionID.DRAW_TEXT,
        (3, 3, DEVICE.Font.FONT_24X32, DEVICE.Color.GRAY, DEVICE.Orientation.VERTICAL, "abc"),
        sent=("H B B B B 50s", (3, 3, 9, 2, 1, b"abc")),
    ),
    Call(
        "draw_text",
        FunctionID.DRAW_TEXT,
        (3, 3, DEVICE.Font.FONT_24X32, DEVICE.Color.GRAY, DEVICE.Orientation.VERTICAL, "abc", False),
        sent=("H B B B B 50s", (3, 3, 9, 2, 1, b"abc")),
        response_expected=False,
    ),
    Call("draw_line", FunctionID.DRAW_LINE, (3, 3, 3, 3, DEVICE.Color.GRAY), sent=("H B H B B", (3, 3, 3, 3, 2))),
    Call(
        "draw_line",
        FunctionID.DRAW_LINE,
        (3, 3, 3, 3, DEVICE.Color.GRAY, False),
        sent=("H B H B B", (3, 3, 3, 3, 2)),
        response_expected=False,
    ),
    Call(
        "draw_box",
        FunctionID.DRAW_BOX,
        (3, 3, 3, 3, True, DEVICE.Color.GRAY),
        sent=("H B H B ! B", (3, 3, 3, 3, True, 2)),
    ),
    Call(
        "draw_box",
        FunctionID.DRAW_BOX,
        (3, 3, 3, 3, True, DEVICE.Color.GRAY, False),
        sent=("H B H B ! B", (3, 3, 3, 3, True, 2)),
        response_expected=False,
    ),
    Call("set_update_mode", FunctionID.SET_UPDATE_MODE, (DEVICE.UpdateMode.DELTA,), sent=("B", (2,))),
    Call(
        "set_update_mode",
        FunctionID.SET_UPDATE_MODE,
        (DEVICE.UpdateMode.DELTA, False),
        sent=("B", (2,)),
        response_expected=False,
    ),
    Call("get_update_mode", FunctionID.GET_UPDATE_MODE, (), reply=("B", (2,)), result=DEVICE.UpdateMode.DELTA),
    Call("set_display_type", FunctionID.SET_DISPLAY_TYPE, (DEVICE.DisplayType.BLACK_WHITE_GRAY,), sent=("B", (1,))),
    Call(
        "set_display_type",
        FunctionID.SET_DISPLAY_TYPE,
        (DEVICE.DisplayType.BLACK_WHITE_GRAY, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call(
        "get_display_type",
        FunctionID.GET_DISPLAY_TYPE,
        (),
        reply=("B", (1,)),
        result=DEVICE.DisplayType.BLACK_WHITE_GRAY,
    ),
    Call("set_display_driver", FunctionID.SET_DISPLAY_DRIVER, (DEVICE.DisplayDriver.SSD1680,), sent=("B", (1,))),
    Call(
        "set_display_driver",
        FunctionID.SET_DISPLAY_DRIVER,
        (DEVICE.DisplayDriver.SSD1680, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call(
        "get_display_driver", FunctionID.GET_DISPLAY_DRIVER, (), reply=("B", (1,)), result=DEVICE.DisplayDriver.SSD1680
    ),
    Call("get_value", FunctionID.GET_DRAW_STATUS, (0,), reply=("B", (2,)), result=DEVICE.DrawStatus.DRAWING),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write_black_white_low_level", (296, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
    ("write_black_white_low_level", (3, 128, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
    ("write_black_white_low_level", (3, 3, 296, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
    ("write_black_white_low_level", (3, 3, 3, 128, 3, 3, [i % 2 == 0 for i in range(432)])),
    ("write_black_white_low_level", (3, 3, 3, 3, 37889, 3, [i % 2 == 0 for i in range(432)])),
    ("write_black_white_low_level", (3, 3, 3, 3, 3, 65536, [i % 2 == 0 for i in range(432)])),
    ("write_black_white_low_level", (3, 3, 3, 3, 3, 3, ([i % 2 == 0 for i in range(432)])[:-1])),
    ("write_black_white", (3, 3, 3, 3, [True] * 65536)),
    ("read_black_white_low_level", (296, 3, 3, 3)),
    ("read_black_white_low_level", (3, 128, 3, 3)),
    ("read_black_white_low_level", (3, 3, 296, 3)),
    ("read_black_white_low_level", (3, 3, 3, 128)),
    ("write_color_low_level", (296, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
    ("write_color_low_level", (3, 128, 3, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
    ("write_color_low_level", (3, 3, 296, 3, 3, 3, [i % 2 == 0 for i in range(432)])),
    ("write_color_low_level", (3, 3, 3, 128, 3, 3, [i % 2 == 0 for i in range(432)])),
    ("write_color_low_level", (3, 3, 3, 3, 37889, 3, [i % 2 == 0 for i in range(432)])),
    ("write_color_low_level", (3, 3, 3, 3, 3, 65536, [i % 2 == 0 for i in range(432)])),
    ("write_color_low_level", (3, 3, 3, 3, 3, 3, ([i % 2 == 0 for i in range(432)])[:-1])),
    ("write_color", (3, 3, 3, 3, [True] * 65536)),
    ("read_color_low_level", (296, 3, 3, 3)),
    ("read_color_low_level", (3, 128, 3, 3)),
    ("read_color_low_level", (3, 3, 296, 3)),
    ("read_color_low_level", (3, 3, 3, 128)),
    ("fill_display", (12345,)),
    ("draw_text", (296, 3, DEVICE.Font.FONT_24X32, DEVICE.Color.GRAY, DEVICE.Orientation.VERTICAL, "abc")),
    ("draw_text", (3, 128, DEVICE.Font.FONT_24X32, DEVICE.Color.GRAY, DEVICE.Orientation.VERTICAL, "abc")),
    ("draw_text", (3, 3, 12345, DEVICE.Color.GRAY, DEVICE.Orientation.VERTICAL, "abc")),
    ("draw_text", (3, 3, DEVICE.Font.FONT_24X32, 12345, DEVICE.Orientation.VERTICAL, "abc")),
    ("draw_text", (3, 3, DEVICE.Font.FONT_24X32, DEVICE.Color.GRAY, 12345, "abc")),
    (
        "draw_text",
        (
            3,
            3,
            DEVICE.Font.FONT_24X32,
            DEVICE.Color.GRAY,
            DEVICE.Orientation.VERTICAL,
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        ),
    ),
    ("draw_line", (296, 3, 3, 3, DEVICE.Color.GRAY)),
    ("draw_line", (3, 128, 3, 3, DEVICE.Color.GRAY)),
    ("draw_line", (3, 3, 296, 3, DEVICE.Color.GRAY)),
    ("draw_line", (3, 3, 3, 128, DEVICE.Color.GRAY)),
    ("draw_line", (3, 3, 3, 3, 12345)),
    ("draw_box", (296, 3, 3, 3, True, DEVICE.Color.GRAY)),
    ("draw_box", (3, 128, 3, 3, True, DEVICE.Color.GRAY)),
    ("draw_box", (3, 3, 296, 3, True, DEVICE.Color.GRAY)),
    ("draw_box", (3, 3, 3, 128, True, DEVICE.Color.GRAY)),
    ("draw_box", (3, 3, 3, 3, True, 12345)),
    ("set_update_mode", (12345,)),
    ("set_display_type", (12345,)),
    ("set_display_driver", (12345,)),
    ("get_value", (1,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2146
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("E-Paper 296x128 Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_write_black_white_transfers_the_stream(device, connection):
    """The high-level function write_black_white() uses write_black_white_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    result = run(device.write_black_white(*(3, 3, 3, 3, data)))
    assert connection.requests == [
        request(
            FunctionID.WRITE_BLACK_WHITE_LOW_LEVEL,
            "H B H B H H 432!",
            *(3, 3, 3, 3, 3, offset, chunk([i % 2 == 0 for i in range(3)], offset, 432, False)),
        )
        for offset in range(0, 1, 432)
    ]
    assert result is None


def test_read_black_white_transfers_the_stream(device, connection):
    """The high-level function read_black_white() uses read_black_white_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    for offset in range(0, 1, 464):
        connection.reply(
            FunctionID.READ_BLACK_WHITE_LOW_LEVEL, "H H 464!", *(3, offset, chunk(data, offset, 464, False))
        )
    result = run(device.read_black_white(*(3, 3, 3, 3)))
    assert connection.requests == [request(FunctionID.READ_BLACK_WHITE_LOW_LEVEL, "H B H B", *(3, 3, 3, 3))] * 1
    assert result == tuple(i % 2 == 0 for i in range(3))


def test_write_color_transfers_the_stream(device, connection):
    """The high-level function write_color() uses write_color_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    result = run(device.write_color(*(3, 3, 3, 3, data)))
    assert connection.requests == [
        request(
            FunctionID.WRITE_COLOR_LOW_LEVEL,
            "H B H B H H 432!",
            *(3, 3, 3, 3, 3, offset, chunk([i % 2 == 0 for i in range(3)], offset, 432, False)),
        )
        for offset in range(0, 1, 432)
    ]
    assert result is None


def test_read_color_transfers_the_stream(device, connection):
    """The high-level function read_color() uses read_color_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    for offset in range(0, 1, 464):
        connection.reply(FunctionID.READ_COLOR_LOW_LEVEL, "H H 464!", *(3, offset, chunk(data, offset, 464, False)))
    result = run(device.read_color(*(3, 3, 3, 3)))
    assert connection.requests == [request(FunctionID.READ_COLOR_LOW_LEVEL, "H B H B", *(3, 3, 3, 3))] * 1
    assert result == tuple(i % 2 == 0 for i in range(3))


def test_callback_draw_status(device, connection):
    """The callback DRAW_STATUS is converted to an event."""
    connection.callback(CallbackID.DRAW_STATUS, "B", *(2,))
    assert summary(read_events(device)) == [(0, CallbackID.DRAW_STATUS, DEVICE.DrawStatus.DRAWING)]
