"""Tests for the Temperature IR Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_temperature_ir_v2 import BrickletTemperatureIRV2
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletTemperatureIRV2
FunctionID = BrickletTemperatureIRV2.FunctionID
CallbackID = BrickletTemperatureIRV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_AMBIENT_TEMPERATURE": 1,
    "SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION": 2,
    "GET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION": 3,
    "GET_OBJECT_TEMPERATURE": 5,
    "SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION": 6,
    "GET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION": 7,
    "SET_EMISSIVITY": 9,
    "GET_EMISSIVITY": 10,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"AMBIENT_TEMPERATURE": 4, "OBJECT_TEMPERATURE": 8}

CALLS: list[Call] = [
    Call(
        "get_ambient_temperature", FunctionID.GET_AMBIENT_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("273.45")
    ),
    Call(
        "set_ambient_temperature_callback_configuration",
        FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("273.45"), Decimal("273.45")),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_ambient_temperature_callback_configuration",
        FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("273.45"), Decimal("273.45"), False),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_ambient_temperature_callback_configuration",
        FunctionID.GET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c h h", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("273.75"), Decimal("273.85")
        ),
    ),
    Call("get_object_temperature", FunctionID.GET_OBJECT_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("273.45")),
    Call(
        "set_object_temperature_callback_configuration",
        FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("273.45"), Decimal("273.45")),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_object_temperature_callback_configuration",
        FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("273.45"), Decimal("273.45"), False),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_object_temperature_callback_configuration",
        FunctionID.GET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c h h", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("273.75"), Decimal("273.85")
        ),
    ),
    Call(
        "set_emissivity", FunctionID.SET_EMISSIVITY, (Decimal("0.00004577706569008926527809567407"),), sent=("H", (3,))
    ),
    Call(
        "set_emissivity",
        FunctionID.SET_EMISSIVITY,
        (Decimal("0.00004577706569008926527809567407"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call(
        "get_emissivity",
        FunctionID.GET_EMISSIVITY,
        (),
        reply=("H", (3,)),
        result=Decimal("0.00004577706569008926527809567407"),
    ),
    Call("get_value", FunctionID.GET_AMBIENT_TEMPERATURE, (0,), reply=("h", (3,)), result=Decimal("273.45")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("273.45"), Decimal("273.55")),
        sent=("I ! c h h", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c h h", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("273.45"), Decimal("273.55")),
    ),
    Call("get_value", FunctionID.GET_OBJECT_TEMPERATURE, (1,), reply=("h", (3,)), result=Decimal("273.45")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (1, 1, True, Threshold.OUTSIDE, Decimal("273.45"), Decimal("273.55")),
        sent=("I ! c h h", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c h h", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("273.45"), Decimal("273.55")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    (
        "set_ambient_temperature_callback_configuration",
        (Decimal("4294967.296"), True, "o", Decimal("273.45"), Decimal("273.45")),
    ),
    (
        "set_ambient_temperature_callback_configuration",
        (Decimal("0.003"), True, "?", Decimal("273.45"), Decimal("273.45")),
    ),
    (
        "set_ambient_temperature_callback_configuration",
        (Decimal("0.003"), True, "o", Decimal("3549.95"), Decimal("273.45")),
    ),
    (
        "set_ambient_temperature_callback_configuration",
        (Decimal("0.003"), True, "o", Decimal("273.45"), Decimal("3549.95")),
    ),
    (
        "set_object_temperature_callback_configuration",
        (Decimal("4294967.296"), True, "o", Decimal("273.45"), Decimal("273.45")),
    ),
    (
        "set_object_temperature_callback_configuration",
        (Decimal("0.003"), True, "?", Decimal("273.45"), Decimal("273.45")),
    ),
    (
        "set_object_temperature_callback_configuration",
        (Decimal("0.003"), True, "o", Decimal("3549.95"), Decimal("273.45")),
    ),
    (
        "set_object_temperature_callback_configuration",
        (Decimal("0.003"), True, "o", Decimal("273.45"), Decimal("3549.95")),
    ),
    ("set_emissivity", (Decimal("1.000015259021896696421759365"),)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device: BrickletTemperatureIRV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 291
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Temperature IR Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_ambient_temperature(device: BrickletTemperatureIRV2, connection: FakeConnection) -> None:
    """The callback AMBIENT_TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.AMBIENT_TEMPERATURE, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.AMBIENT_TEMPERATURE, Decimal("273.45"))]


def test_callback_object_temperature(device: BrickletTemperatureIRV2, connection: FakeConnection) -> None:
    """The callback OBJECT_TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.OBJECT_TEMPERATURE, "h", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.OBJECT_TEMPERATURE, Decimal("273.45"))]
