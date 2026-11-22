"""Tests for the Industrial Analog Out Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_analog_out import BrickletIndustrialAnalogOut, GetConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialAnalogOut
FunctionID = BrickletIndustrialAnalogOut.FunctionID
CallbackID = BrickletIndustrialAnalogOut.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "ENABLE": 1,
    "DISABLE": 2,
    "IS_ENABLED": 3,
    "SET_VOLTAGE": 4,
    "GET_VOLTAGE": 5,
    "SET_CURRENT": 6,
    "GET_CURRENT": 7,
    "SET_CONFIGURATION": 8,
    "GET_CONFIGURATION": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {}

CALLS: list[Call] = [
    Call("enable", FunctionID.ENABLE, ()),
    Call("enable", FunctionID.ENABLE, (False,), response_expected=False),
    Call("disable", FunctionID.DISABLE, ()),
    Call("disable", FunctionID.DISABLE, (False,), response_expected=False),
    Call("is_enabled", FunctionID.IS_ENABLED, (), reply=("!", (True,)), result=True),
    Call("set_voltage", FunctionID.SET_VOLTAGE, (Decimal("0.003"),), sent=("H", (3,))),
    Call("set_voltage", FunctionID.SET_VOLTAGE, (Decimal("0.003"), False), sent=("H", (3,)), response_expected=False),
    Call("get_voltage", FunctionID.GET_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_current", FunctionID.SET_CURRENT, (Decimal("0.000003"),), sent=("H", (3,))),
    Call(
        "set_current", FunctionID.SET_CURRENT, (Decimal("0.000003"), False), sent=("H", (3,)), response_expected=False
    ),
    Call("get_current", FunctionID.GET_CURRENT, (), reply=("H", (3,)), result=Decimal("0.000003")),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.VoltageRange.VOLTAGE_RANGE_0_TO_10V, DEVICE.CurrentRange.CURRENT_RANGE_0_TO_24MA),
        sent=("B B", (1, 2)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.VoltageRange.VOLTAGE_RANGE_0_TO_10V, DEVICE.CurrentRange.CURRENT_RANGE_0_TO_24MA, False),
        sent=("B B", (1, 2)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B", (1, 2)),
        result=GetConfiguration(
            DEVICE.VoltageRange.VOLTAGE_RANGE_0_TO_10V, DEVICE.CurrentRange.CURRENT_RANGE_0_TO_24MA
        ),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_voltage", (Decimal("10.001"),)),
    ("set_current", (Decimal("0.024001"),)),
    ("set_configuration", (12345, DEVICE.CurrentRange.CURRENT_RANGE_0_TO_24MA)),
    ("set_configuration", (DEVICE.VoltageRange.VOLTAGE_RANGE_0_TO_10V, 12345)),
]


def test_identity(device: BrickletIndustrialAnalogOut) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 258
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Analog Out Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""
