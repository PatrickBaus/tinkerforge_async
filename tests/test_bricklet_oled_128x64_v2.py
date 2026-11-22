"""Tests for the OLED 128x64 Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_oled_128x64_v2 import BrickletOLED128x64V2, GetDisplayConfiguration, ReadPixels
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletOLED128x64V2
FunctionID = BrickletOLED128x64V2.FunctionID
CallbackID = BrickletOLED128x64V2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "WRITE_PIXELS_LOW_LEVEL": 1,
    "READ_PIXELS_LOW_LEVEL": 2,
    "CLEAR_DISPLAY": 3,
    "SET_DISPLAY_CONFIGURATION": 4,
    "GET_DISPLAY_CONFIGURATION": 5,
    "WRITE_LINE": 6,
    "DRAW_BUFFERED_FRAME": 7,
    "WRITE_LINE_2": 8,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = [
    Call(
        "write_pixels_low_level",
        FunctionID.WRITE_PIXELS_LOW_LEVEL,
        (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)]),
        sent=("B B B B H H 448!", (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
    ),
    Call(
        "write_pixels_low_level",
        FunctionID.WRITE_PIXELS_LOW_LEVEL,
        (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)], False),
        sent=("B B B B H H 448!", (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
        response_expected=False,
    ),
    Call(
        "read_pixels_low_level",
        FunctionID.READ_PIXELS_LOW_LEVEL,
        (3, 3, 3, 3),
        sent=("B B B B", (3, 3, 3, 3)),
        reply=("H H 480!", (3, 4, [i % 2 == 0 for i in range(480)])),
        result=ReadPixels(3, 4, tuple(i % 2 == 0 for i in range(480))),
    ),
    Call("clear_display", FunctionID.CLEAR_DISPLAY, ()),
    Call("clear_display", FunctionID.CLEAR_DISPLAY, (False,), response_expected=False),
    Call(
        "set_display_configuration",
        FunctionID.SET_DISPLAY_CONFIGURATION,
        (3, True, True),
        sent=("B ! !", (3, True, True)),
    ),
    Call(
        "set_display_configuration",
        FunctionID.SET_DISPLAY_CONFIGURATION,
        (3, True, True, False),
        sent=("B ! !", (3, True, True)),
        response_expected=False,
    ),
    Call(
        "get_display_configuration",
        FunctionID.GET_DISPLAY_CONFIGURATION,
        (),
        reply=("B ! !", (3, True, True)),
        result=GetDisplayConfiguration(3, True, True),
    ),
    Call("write_line", FunctionID.WRITE_LINE, (3, 3, "abc"), sent=("B B 22s", (3, 3, b"abc"))),
    Call(
        "write_line",
        FunctionID.WRITE_LINE,
        (3, 3, "abc", False),
        sent=("B B 22s", (3, 3, b"abc")),
        response_expected=False,
    ),
    Call("draw_buffered_frame", FunctionID.DRAW_BUFFERED_FRAME, (True,), sent=("!", (True,))),
    Call(
        "draw_buffered_frame",
        FunctionID.DRAW_BUFFERED_FRAME,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call("write_line_2", FunctionID.WRITE_LINE_2, (3, 3, 1, "abc"), sent=("B B B 26s", (3, 3, 1, b"abc"))),
    Call(
        "write_line_2",
        FunctionID.WRITE_LINE_2,
        (3, 3, 1, "abc", False),
        sent=("B B B 26s", (3, 3, 1, b"abc")),
        response_expected=False,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write_pixels_low_level", (128, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 64, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 128, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 3, 64, 3, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 3, 3, 8193, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 3, 3, 3, 65536, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 3, 3, 3, 3, ([i % 2 == 0 for i in range(448)])[:-1])),
    ("write_pixels", (3, 3, 3, 3, [True] * 65536)),
    ("read_pixels_low_level", (128, 3, 3, 3)),
    ("read_pixels_low_level", (3, 64, 3, 3)),
    ("read_pixels_low_level", (3, 3, 128, 3)),
    ("read_pixels_low_level", (3, 3, 3, 64)),
    ("set_display_configuration", (256, True, True)),
    ("write_line", (8, 3, "abc")),
    ("write_line", (3, 22, "abc")),
    ("write_line", (3, 3, "aaaaaaaaaaaaaaaaaaaaaaa")),
    ("write_line_2", (8, 3, 1, "abc")),
    ("write_line_2", (3, 26, 1, "abc")),
    ("write_line_2", (3, 3, 2, "abc")),
    ("write_line_2", (3, 3, 1, "aaaaaaaaaaaaaaaaaaaaaaaaaaa")),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2112
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("OLED 128x64 Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_write_pixels_transfers_the_stream(device, connection):
    """The high-level function write_pixels() uses write_pixels_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    result = run(device.write_pixels(*(3, 3, 3, 3, data)))
    assert connection.requests == [
        request(
            FunctionID.WRITE_PIXELS_LOW_LEVEL,
            "B B B B H H 448!",
            *(3, 3, 3, 3, 3, offset, chunk([i % 2 == 0 for i in range(3)], offset, 448, False)),
        )
        for offset in range(0, 1, 448)
    ]
    assert result is None


def test_read_pixels_transfers_the_stream(device, connection):
    """The high-level function read_pixels() uses read_pixels_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    for offset in range(0, 1, 480):
        connection.reply(FunctionID.READ_PIXELS_LOW_LEVEL, "H H 480!", *(3, offset, chunk(data, offset, 480, False)))
    result = run(device.read_pixels(*(3, 3, 3, 3)))
    assert connection.requests == [request(FunctionID.READ_PIXELS_LOW_LEVEL, "B B B B", *(3, 3, 3, 3))] * 1
    assert result == tuple(i % 2 == 0 for i in range(3))
