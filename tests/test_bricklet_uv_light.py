"""Tests for the UV Light Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_uv_light import BrickletUVLight
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletUVLight
FunctionID = BrickletUVLight.FunctionID
CallbackID = BrickletUVLight.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_UV_LIGHT": 1,
    "SET_UV_LIGHT_CALLBACK_PERIOD": 2,
    "GET_UV_LIGHT_CALLBACK_PERIOD": 3,
    "SET_UV_LIGHT_CALLBACK_THRESHOLD": 4,
    "GET_UV_LIGHT_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"UV_LIGHT": 8, "UV_LIGHT_REACHED": 9}

CALLS: list[Call] = [
    Call("get_uv_light", FunctionID.GET_UV_LIGHT, (), reply=("I", (3,)), result=Decimal("0.0003")),
    Call(
        "set_uv_light_callback_period", FunctionID.SET_UV_LIGHT_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))
    ),
    Call(
        "set_uv_light_callback_period",
        FunctionID.SET_UV_LIGHT_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_uv_light_callback_period",
        FunctionID.GET_UV_LIGHT_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_uv_light_callback_threshold",
        FunctionID.SET_UV_LIGHT_CALLBACK_THRESHOLD,
        ("o", Decimal("0.0003"), Decimal("0.0003")),
        sent=("c I I", ("o", 3, 3)),
    ),
    Call(
        "set_uv_light_callback_threshold",
        FunctionID.SET_UV_LIGHT_CALLBACK_THRESHOLD,
        ("o", Decimal("0.0003"), Decimal("0.0003"), False),
        sent=("c I I", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_uv_light_callback_threshold",
        FunctionID.GET_UV_LIGHT_CALLBACK_THRESHOLD,
        (),
        reply=("c I I", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.0004"), Decimal("0.0005")),
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
    Call("get_value", FunctionID.GET_UV_LIGHT, (0,), reply=("I", (3,)), result=Decimal("0.0003")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_uv_light_callback_period", (Decimal("4294967.296"),)),
    ("set_uv_light_callback_threshold", ("?", Decimal("0.0003"), Decimal("0.0003"))),
    ("set_uv_light_callback_threshold", ("o", Decimal("429496.7296"), Decimal("0.0003"))),
    ("set_uv_light_callback_threshold", ("o", Decimal("0.0003"), Decimal("429496.7296"))),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 265
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("UV Light Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device, connection):
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("0.0003"), Decimal("0.0004")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_UV_LIGHT_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_UV_LIGHT_CALLBACK_THRESHOLD, "c I I", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_UV_LIGHT_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_UV_LIGHT_CALLBACK_THRESHOLD, "c I I", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.0003"), Decimal("0.0004")
    )


def test_callback_uv_light(device, connection):
    """The callback UV_LIGHT is converted to an event."""
    connection.callback(CallbackID.UV_LIGHT, "I", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.UV_LIGHT, Decimal("0.0003"))]


def test_callback_uv_light_reached(device, connection):
    """The callback UV_LIGHT_REACHED is converted to an event."""
    connection.callback(CallbackID.UV_LIGHT_REACHED, "I", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.UV_LIGHT_REACHED, Decimal("0.0003"))]
