"""Tests for the RGB LED Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_rgb_led import BrickletRGBLED, GetRGBValue
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletRGBLED
FunctionID = BrickletRGBLED.FunctionID
CallbackID = BrickletRGBLED.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {"SET_RGB_VALUE": 1, "GET_RGB_VALUE": 2}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = [
    Call("set_rgb_value", FunctionID.SET_RGB_VALUE, (3, 3, 3), sent=("B B B", (3, 3, 3))),
    Call(
        "set_rgb_value", FunctionID.SET_RGB_VALUE, (3, 3, 3, False), sent=("B B B", (3, 3, 3)), response_expected=False
    ),
    Call("get_rgb_value", FunctionID.GET_RGB_VALUE, (), reply=("B B B", (3, 4, 5)), result=GetRGBValue(3, 4, 5)),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_rgb_value", (256, 3, 3)),
    ("set_rgb_value", (3, 256, 3)),
    ("set_rgb_value", (3, 3, 256)),
]


def test_identity(device: BrickletRGBLED) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 271
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("RGB LED Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""
