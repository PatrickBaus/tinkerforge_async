"""Tests for the Color Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_color import BrickletColor, GetColor, GetColorCallbackThreshold, GetConfig
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletColor
FunctionID = BrickletColor.FunctionID
CallbackID = BrickletColor.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_COLOR": 1,
    "SET_COLOR_CALLBACK_PERIOD": 2,
    "GET_COLOR_CALLBACK_PERIOD": 3,
    "SET_COLOR_CALLBACK_THRESHOLD": 4,
    "GET_COLOR_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "LIGHT_ON": 10,
    "LIGHT_OFF": 11,
    "IS_LIGHT_ON": 12,
    "SET_CONFIG": 13,
    "GET_CONFIG": 14,
    "GET_ILLUMINANCE": 15,
    "GET_COLOR_TEMPERATURE": 16,
    "SET_ILLUMINANCE_CALLBACK_PERIOD": 17,
    "GET_ILLUMINANCE_CALLBACK_PERIOD": 18,
    "SET_COLOR_TEMPERATURE_CALLBACK_PERIOD": 19,
    "GET_COLOR_TEMPERATURE_CALLBACK_PERIOD": 20,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"COLOR": 8, "COLOR_REACHED": 9, "ILLUMINANCE": 21, "COLOR_TEMPERATURE": 22}

CALLS: list[Call] = [
    Call("get_color", FunctionID.GET_COLOR, (), reply=("H H H H", (3, 4, 5, 6)), result=GetColor(3, 4, 5, 6)),
    Call("set_color_callback_period", FunctionID.SET_COLOR_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_color_callback_period",
        FunctionID.SET_COLOR_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_color_callback_period",
        FunctionID.GET_COLOR_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_color_callback_threshold",
        FunctionID.SET_COLOR_CALLBACK_THRESHOLD,
        ("o", 3, 3, 3, 3, 3, 3, 3, 3),
        sent=("c H H H H H H H H", ("o", 3, 3, 3, 3, 3, 3, 3, 3)),
    ),
    Call(
        "set_color_callback_threshold",
        FunctionID.SET_COLOR_CALLBACK_THRESHOLD,
        ("o", 3, 3, 3, 3, 3, 3, 3, 3, False),
        sent=("c H H H H H H H H", ("o", 3, 3, 3, 3, 3, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_color_callback_threshold",
        FunctionID.GET_COLOR_CALLBACK_THRESHOLD,
        (),
        reply=("c H H H H H H H H", ("o", 4, 5, 6, 7, 8, 9, 10, 11)),
        result=GetColorCallbackThreshold(Threshold.OUTSIDE, 4, 5, 6, 7, 8, 9, 10, 11),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_debounce_period",
        FunctionID.SET_DEBOUNCE_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("light_on", FunctionID.LIGHT_ON, ()),
    Call("light_on", FunctionID.LIGHT_ON, (False,), response_expected=False),
    Call("light_off", FunctionID.LIGHT_OFF, ()),
    Call("light_off", FunctionID.LIGHT_OFF, (False,), response_expected=False),
    Call("is_light_on", FunctionID.IS_LIGHT_ON, (), reply=("B", (1,)), result=DEVICE.Light.OFF),
    Call(
        "set_config",
        FunctionID.SET_CONFIG,
        (DEVICE.Gain.GAIN_60X, DEVICE.IntegrationTime.INTEGRATION_TIME_700MS),
        sent=("B B", (3, 4)),
    ),
    Call(
        "set_config",
        FunctionID.SET_CONFIG,
        (DEVICE.Gain.GAIN_60X, DEVICE.IntegrationTime.INTEGRATION_TIME_700MS, False),
        sent=("B B", (3, 4)),
        response_expected=False,
    ),
    Call(
        "get_config",
        FunctionID.GET_CONFIG,
        (),
        reply=("B B", (3, 4)),
        result=GetConfig(DEVICE.Gain.GAIN_60X, DEVICE.IntegrationTime.INTEGRATION_TIME_700MS),
    ),
    Call("get_illuminance", FunctionID.GET_ILLUMINANCE, (), reply=("I", (3,)), result=3),
    Call("get_color_temperature", FunctionID.GET_COLOR_TEMPERATURE, (), reply=("H", (3,)), result=Decimal("3")),
    Call(
        "set_illuminance_callback_period",
        FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_illuminance_callback_period",
        FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_illuminance_callback_period",
        FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_color_temperature_callback_period",
        FunctionID.SET_COLOR_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_color_temperature_callback_period",
        FunctionID.SET_COLOR_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_color_temperature_callback_period",
        FunctionID.GET_COLOR_TEMPERATURE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("get_value", FunctionID.GET_ILLUMINANCE, (2,), reply=("I", (3,)), result=3),
    Call("get_value", FunctionID.GET_COLOR_TEMPERATURE, (3,), reply=("H", (3,)), result=Decimal("3")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_color_callback_period", (Decimal("4294967.296"),)),
    ("set_color_callback_threshold", ("?", 3, 3, 3, 3, 3, 3, 3, 3)),
    ("set_color_callback_threshold", ("o", 65536, 3, 3, 3, 3, 3, 3, 3)),
    ("set_color_callback_threshold", ("o", 3, 65536, 3, 3, 3, 3, 3, 3)),
    ("set_color_callback_threshold", ("o", 3, 3, 65536, 3, 3, 3, 3, 3)),
    ("set_color_callback_threshold", ("o", 3, 3, 3, 65536, 3, 3, 3, 3)),
    ("set_color_callback_threshold", ("o", 3, 3, 3, 3, 65536, 3, 3, 3)),
    ("set_color_callback_threshold", ("o", 3, 3, 3, 3, 3, 65536, 3, 3)),
    ("set_color_callback_threshold", ("o", 3, 3, 3, 3, 3, 3, 65536, 3)),
    ("set_color_callback_threshold", ("o", 3, 3, 3, 3, 3, 3, 3, 65536)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_config", (12345, DEVICE.IntegrationTime.INTEGRATION_TIME_700MS)),
    ("set_config", (DEVICE.Gain.GAIN_60X, 12345)),
    ("set_illuminance_callback_period", (Decimal("4294967.296"),)),
    ("set_color_temperature_callback_period", (Decimal("4294967.296"),)),
    ("get_value", (4,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 243
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Color Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_color(device, connection):
    """The callback COLOR is converted to an event."""
    connection.callback(CallbackID.COLOR, "H H H H", *(3, 4, 5, 6))
    assert summary(read_events(device)) == [(0, CallbackID.COLOR, GetColor(3, 4, 5, 6))]


def test_callback_color_reached(device, connection):
    """The callback COLOR_REACHED is converted to an event."""
    connection.callback(CallbackID.COLOR_REACHED, "H H H H", *(3, 4, 5, 6))
    assert summary(read_events(device)) == [(1, CallbackID.COLOR_REACHED, GetColor(3, 4, 5, 6))]


def test_callback_illuminance(device, connection):
    """The callback ILLUMINANCE is converted to an event."""
    connection.callback(CallbackID.ILLUMINANCE, "I", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.ILLUMINANCE, 3)]


def test_callback_color_temperature(device, connection):
    """The callback COLOR_TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.COLOR_TEMPERATURE, "H", *(3,))
    assert summary(read_events(device)) == [(3, CallbackID.COLOR_TEMPERATURE, Decimal("3"))]
