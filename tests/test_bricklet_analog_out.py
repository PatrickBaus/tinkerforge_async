"""Tests for the Analog Out Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_analog_out import BrickletAnalogOut
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletAnalogOut
FunctionID = BrickletAnalogOut.FunctionID
CallbackID = BrickletAnalogOut.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {"SET_VOLTAGE": 1, "GET_VOLTAGE": 2, "SET_MODE": 3, "GET_MODE": 4}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = [
    Call("set_voltage", FunctionID.SET_VOLTAGE, (Decimal("0.003"),), sent=("H", (3,))),
    Call("set_voltage", FunctionID.SET_VOLTAGE, (Decimal("0.003"), False), sent=("H", (3,)), response_expected=False),
    Call("get_voltage", FunctionID.GET_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_mode", FunctionID.SET_MODE, (DEVICE.Mode.MODE_500K_TO_GROUND,), sent=("B", (3,))),
    Call(
        "set_mode",
        FunctionID.SET_MODE,
        (DEVICE.Mode.MODE_500K_TO_GROUND, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call("get_mode", FunctionID.GET_MODE, (), reply=("B", (3,)), result=DEVICE.Mode.MODE_500K_TO_GROUND),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_voltage", (Decimal("5.001"),)),
    ("set_mode", (12345,)),
]


def test_identity(device: BrickletAnalogOut) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 220
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Analog Out Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""
