"""Tests for the Analog Out Bricklet 3.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_analog_out_v3 import BrickletAnalogOutV3
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletAnalogOutV3
FunctionID = BrickletAnalogOutV3.FunctionID
CallbackID = BrickletAnalogOutV3.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {"SET_OUTPUT_VOLTAGE": 1, "GET_OUTPUT_VOLTAGE": 2, "GET_INPUT_VOLTAGE": 3}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = [
    Call("set_output_voltage", FunctionID.SET_OUTPUT_VOLTAGE, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_output_voltage",
        FunctionID.SET_OUTPUT_VOLTAGE,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_output_voltage", FunctionID.GET_OUTPUT_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("get_input_voltage", FunctionID.GET_INPUT_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_output_voltage", (Decimal("12.001"),)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2115
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Analog Out Bricklet 3.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""
