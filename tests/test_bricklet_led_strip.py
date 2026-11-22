"""Tests for the LED Strip Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_led_strip import BrickletLEDStrip, GetRGBValues, GetRGBWValues
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletLEDStrip
FunctionID = BrickletLEDStrip.FunctionID
CallbackID = BrickletLEDStrip.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_RGB_VALUES": 1,
    "GET_RGB_VALUES": 2,
    "SET_FRAME_DURATION": 3,
    "GET_FRAME_DURATION": 4,
    "GET_SUPPLY_VOLTAGE": 5,
    "SET_CLOCK_FREQUENCY": 7,
    "GET_CLOCK_FREQUENCY": 8,
    "SET_CHIP_TYPE": 9,
    "GET_CHIP_TYPE": 10,
    "SET_RGBW_VALUES": 11,
    "GET_RGBW_VALUES": 12,
    "SET_CHANNEL_MAPPING": 13,
    "GET_CHANNEL_MAPPING": 14,
    "ENABLE_FRAME_RENDERED_CALLBACK": 15,
    "DISABLE_FRAME_RENDERED_CALLBACK": 16,
    "IS_FRAME_RENDERED_CALLBACK_ENABLED": 17,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"FRAME_RENDERED": 6}

CALLS: list[Call] = [
    Call(
        "set_rgb_values",
        FunctionID.SET_RGB_VALUES,
        (3, 3, [i % 256 for i in range(16)], [i % 256 for i in range(16)], [i % 256 for i in range(16)]),
        sent=(
            "H B 16B 16B 16B",
            (3, 3, [i % 256 for i in range(16)], [i % 256 for i in range(16)], [i % 256 for i in range(16)]),
        ),
    ),
    Call(
        "set_rgb_values",
        FunctionID.SET_RGB_VALUES,
        (3, 3, [i % 256 for i in range(16)], [i % 256 for i in range(16)], [i % 256 for i in range(16)], False),
        sent=(
            "H B 16B 16B 16B",
            (3, 3, [i % 256 for i in range(16)], [i % 256 for i in range(16)], [i % 256 for i in range(16)]),
        ),
        response_expected=False,
    ),
    Call(
        "get_rgb_values",
        FunctionID.GET_RGB_VALUES,
        (3, 3),
        sent=("H B", (3, 3)),
        reply=(
            "16B 16B 16B",
            ([i % 256 for i in range(16)], [i % 256 for i in range(16)], [i % 256 for i in range(16)]),
        ),
        result=GetRGBValues(
            tuple(i % 256 for i in range(16)), tuple(i % 256 for i in range(16)), tuple(i % 256 for i in range(16))
        ),
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
    Call("get_supply_voltage", FunctionID.GET_SUPPLY_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_clock_frequency", FunctionID.SET_CLOCK_FREQUENCY, (Decimal("10000"),), sent=("I", (10000,))),
    Call(
        "set_clock_frequency",
        FunctionID.SET_CLOCK_FREQUENCY,
        (Decimal("10000"), False),
        sent=("I", (10000,)),
        response_expected=False,
    ),
    Call("get_clock_frequency", FunctionID.GET_CLOCK_FREQUENCY, (), reply=("I", (10000,)), result=Decimal("10000")),
    Call("set_chip_type", FunctionID.SET_CHIP_TYPE, (DEVICE.ChipType.APA102,), sent=("H", (102,))),
    Call(
        "set_chip_type",
        FunctionID.SET_CHIP_TYPE,
        (DEVICE.ChipType.APA102, False),
        sent=("H", (102,)),
        response_expected=False,
    ),
    Call("get_chip_type", FunctionID.GET_CHIP_TYPE, (), reply=("H", (102,)), result=DEVICE.ChipType.APA102),
    Call(
        "set_rgbw_values",
        FunctionID.SET_RGBW_VALUES,
        (
            3,
            3,
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
        ),
        sent=(
            "H B 12B 12B 12B 12B",
            (
                3,
                3,
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
            ),
        ),
    ),
    Call(
        "set_rgbw_values",
        FunctionID.SET_RGBW_VALUES,
        (
            3,
            3,
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            False,
        ),
        sent=(
            "H B 12B 12B 12B 12B",
            (
                3,
                3,
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
            ),
        ),
        response_expected=False,
    ),
    Call(
        "get_rgbw_values",
        FunctionID.GET_RGBW_VALUES,
        (3, 3),
        sent=("H B", (3, 3)),
        reply=(
            "12B 12B 12B 12B",
            (
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
                [i % 256 for i in range(12)],
            ),
        ),
        result=GetRGBWValues(
            tuple(i % 256 for i in range(12)),
            tuple(i % 256 for i in range(12)),
            tuple(i % 256 for i in range(12)),
            tuple(i % 256 for i in range(12)),
        ),
    ),
    Call("set_channel_mapping", FunctionID.SET_CHANNEL_MAPPING, (DEVICE.ChannelMapping.WBRG,), sent=("B", (225,))),
    Call(
        "set_channel_mapping",
        FunctionID.SET_CHANNEL_MAPPING,
        (DEVICE.ChannelMapping.WBRG, False),
        sent=("B", (225,)),
        response_expected=False,
    ),
    Call(
        "get_channel_mapping",
        FunctionID.GET_CHANNEL_MAPPING,
        (),
        reply=("B", (225,)),
        result=DEVICE.ChannelMapping.WBRG,
    ),
    Call("enable_frame_rendered_callback", FunctionID.ENABLE_FRAME_RENDERED_CALLBACK, ()),
    Call(
        "enable_frame_rendered_callback", FunctionID.ENABLE_FRAME_RENDERED_CALLBACK, (False,), response_expected=False
    ),
    Call("disable_frame_rendered_callback", FunctionID.DISABLE_FRAME_RENDERED_CALLBACK, ()),
    Call(
        "disable_frame_rendered_callback", FunctionID.DISABLE_FRAME_RENDERED_CALLBACK, (False,), response_expected=False
    ),
    Call(
        "is_frame_rendered_callback_enabled",
        FunctionID.IS_FRAME_RENDERED_CALLBACK_ENABLED,
        (),
        reply=("!", (True,)),
        result=True,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    (
        "set_rgb_values",
        (320, 3, [i % 256 for i in range(16)], [i % 256 for i in range(16)], [i % 256 for i in range(16)]),
    ),
    (
        "set_rgb_values",
        (3, 17, [i % 256 for i in range(16)], [i % 256 for i in range(16)], [i % 256 for i in range(16)]),
    ),
    (
        "set_rgb_values",
        (3, 3, ([i % 256 for i in range(16)])[:-1], [i % 256 for i in range(16)], [i % 256 for i in range(16)]),
    ),
    (
        "set_rgb_values",
        (3, 3, [i % 256 for i in range(16)], ([i % 256 for i in range(16)])[:-1], [i % 256 for i in range(16)]),
    ),
    (
        "set_rgb_values",
        (3, 3, [i % 256 for i in range(16)], [i % 256 for i in range(16)], ([i % 256 for i in range(16)])[:-1]),
    ),
    ("get_rgb_values", (320, 3)),
    ("get_rgb_values", (3, 17)),
    ("set_frame_duration", (Decimal("65.536"),)),
    ("set_clock_frequency", (Decimal("2000001"),)),
    ("set_chip_type", (12345,)),
    (
        "set_rgbw_values",
        (
            240,
            3,
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
        ),
    ),
    (
        "set_rgbw_values",
        (
            3,
            13,
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
        ),
    ),
    (
        "set_rgbw_values",
        (
            3,
            3,
            ([i % 256 for i in range(12)])[:-1],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
        ),
    ),
    (
        "set_rgbw_values",
        (
            3,
            3,
            [i % 256 for i in range(12)],
            ([i % 256 for i in range(12)])[:-1],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
        ),
    ),
    (
        "set_rgbw_values",
        (
            3,
            3,
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            ([i % 256 for i in range(12)])[:-1],
            [i % 256 for i in range(12)],
        ),
    ),
    (
        "set_rgbw_values",
        (
            3,
            3,
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            [i % 256 for i in range(12)],
            ([i % 256 for i in range(12)])[:-1],
        ),
    ),
    ("get_rgbw_values", (240, 3)),
    ("get_rgbw_values", (3, 13)),
    ("set_channel_mapping", (12345,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 231
    assert device.get_api_version() == (2, 0, 3)
    assert str(device).startswith("LED Strip Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_frame_rendered(device, connection):
    """The callback FRAME_RENDERED is converted to an event."""
    connection.callback(CallbackID.FRAME_RENDERED, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.FRAME_RENDERED, 3)]
