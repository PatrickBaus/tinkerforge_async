"""Tests for the ESP32 Ethernet Brick. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_esp32_ethernet import BrickESP32Ethernet
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickESP32Ethernet
FunctionID = BrickESP32Ethernet.FunctionID
CallbackID = BrickESP32Ethernet.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = []

REJECTED: list[tuple[str, tuple[Any, ...]]] = []


def test_identity(device: BrickESP32Ethernet) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 115
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("ESP32 Ethernet Brick with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""
