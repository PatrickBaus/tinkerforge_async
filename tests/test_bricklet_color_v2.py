"""Tests for the Color Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_color_v2 import BrickletColorV2, GetColor, GetConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletColorV2
FunctionID = BrickletColorV2.FunctionID
CallbackID = BrickletColorV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_COLOR": 1,
    "SET_COLOR_CALLBACK_CONFIGURATION": 2,
    "GET_COLOR_CALLBACK_CONFIGURATION": 3,
    "GET_ILLUMINANCE": 5,
    "SET_ILLUMINANCE_CALLBACK_CONFIGURATION": 6,
    "GET_ILLUMINANCE_CALLBACK_CONFIGURATION": 7,
    "GET_COLOR_TEMPERATURE": 9,
    "SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION": 10,
    "GET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION": 11,
    "SET_LIGHT": 13,
    "GET_LIGHT": 14,
    "SET_CONFIGURATION": 15,
    "GET_CONFIGURATION": 16,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"COLOR": 4, "ILLUMINANCE": 8, "COLOR_TEMPERATURE": 12}

CALLS: list[Call] = [
    Call("get_color", FunctionID.GET_COLOR, (), reply=("H H H H", (3, 4, 5, 6)), result=GetColor(3, 4, 5, 6)),
    Call(
        "set_color_callback_configuration",
        FunctionID.SET_COLOR_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_color_callback_configuration",
        FunctionID.SET_COLOR_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_color_callback_configuration",
        FunctionID.GET_COLOR_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("get_illuminance", FunctionID.GET_ILLUMINANCE, (), reply=("I", (3,)), result=3),
    Call(
        "set_illuminance_callback_configuration",
        FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3),
        sent=("I ! c I I", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_illuminance_callback_configuration",
        FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", 3, 3, False),
        sent=("I ! c I I", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_illuminance_callback_configuration",
        FunctionID.GET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c I I", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call("get_color_temperature", FunctionID.GET_COLOR_TEMPERATURE, (), reply=("H", (3,)), result=Decimal("3")),
    Call(
        "set_color_temperature_callback_configuration",
        FunctionID.SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("3"), Decimal("3")),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_color_temperature_callback_configuration",
        FunctionID.SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("3"), Decimal("3"), False),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_color_temperature_callback_configuration",
        FunctionID.GET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c H H", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call("set_light", FunctionID.SET_LIGHT, (True,), sent=("!", (True,))),
    Call("set_light", FunctionID.SET_LIGHT, (True, False), sent=("!", (True,)), response_expected=False),
    Call("get_light", FunctionID.GET_LIGHT, (), reply=("!", (True,)), result=True),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.Gain.GAIN_60X, DEVICE.IntegrationTime.INTEGRATION_TIME_700MS),
        sent=("B B", (3, 4)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.Gain.GAIN_60X, DEVICE.IntegrationTime.INTEGRATION_TIME_700MS, False),
        sent=("B B", (3, 4)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B", (3, 4)),
        result=GetConfiguration(DEVICE.Gain.GAIN_60X, DEVICE.IntegrationTime.INTEGRATION_TIME_700MS),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_COLOR_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_COLOR_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call("get_value", FunctionID.GET_ILLUMINANCE, (1,), reply=("I", (3,)), result=3),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        (1, 1, True, Threshold.OUTSIDE, 3, 4),
        sent=("I ! c I I", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c I I", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
    Call("get_value", FunctionID.GET_COLOR_TEMPERATURE, (2,), reply=("H", (3,)), result=Decimal("3")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION,
        (2, 1, True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
        sent=("I ! c H H", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I ! c H H", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_color_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_illuminance_callback_configuration", (Decimal("4294967.296"), True, "o", 3, 3)),
    ("set_illuminance_callback_configuration", (Decimal("0.003"), True, "?", 3, 3)),
    ("set_illuminance_callback_configuration", (Decimal("0.003"), True, "o", 4294967296, 3)),
    ("set_illuminance_callback_configuration", (Decimal("0.003"), True, "o", 3, 4294967296)),
    ("set_color_temperature_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("3"), Decimal("3"))),
    ("set_color_temperature_callback_configuration", (Decimal("0.003"), True, "?", Decimal("3"), Decimal("3"))),
    ("set_color_temperature_callback_configuration", (Decimal("0.003"), True, "o", Decimal("65536"), Decimal("3"))),
    ("set_color_temperature_callback_configuration", (Decimal("0.003"), True, "o", Decimal("3"), Decimal("65536"))),
    ("set_configuration", (12345, DEVICE.IntegrationTime.INTEGRATION_TIME_700MS)),
    ("set_configuration", (DEVICE.Gain.GAIN_60X, 12345)),
    ("get_value", (3,)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device: BrickletColorV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2128
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Color Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_color(device: BrickletColorV2, connection: FakeConnection) -> None:
    """The callback COLOR is converted to an event."""
    connection.callback(CallbackID.COLOR, "H H H H", *(3, 4, 5, 6))
    assert summary(read_events(device)) == [(0, CallbackID.COLOR, GetColor(3, 4, 5, 6))]


def test_callback_illuminance(device: BrickletColorV2, connection: FakeConnection) -> None:
    """The callback ILLUMINANCE is converted to an event."""
    connection.callback(CallbackID.ILLUMINANCE, "I", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.ILLUMINANCE, 3)]


def test_callback_color_temperature(device: BrickletColorV2, connection: FakeConnection) -> None:
    """The callback COLOR_TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.COLOR_TEMPERATURE, "H", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.COLOR_TEMPERATURE, Decimal("3"))]
