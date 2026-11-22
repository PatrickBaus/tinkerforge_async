"""Tests for the UV Light Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_uv_light_v2 import BrickletUVLightV2
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletUVLightV2
FunctionID = BrickletUVLightV2.FunctionID
CallbackID = BrickletUVLightV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_UVA": 1,
    "SET_UVA_CALLBACK_CONFIGURATION": 2,
    "GET_UVA_CALLBACK_CONFIGURATION": 3,
    "GET_UVB": 5,
    "SET_UVB_CALLBACK_CONFIGURATION": 6,
    "GET_UVB_CALLBACK_CONFIGURATION": 7,
    "GET_UVI": 9,
    "SET_UVI_CALLBACK_CONFIGURATION": 10,
    "GET_UVI_CALLBACK_CONFIGURATION": 11,
    "SET_CONFIGURATION": 13,
    "GET_CONFIGURATION": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"UVA": 4, "UVB": 8, "UVI": 12}

CALLS: list[Call] = [
    Call("get_uva", FunctionID.GET_UVA, (), reply=("i", (3,)), result=Decimal("0.0003")),
    Call(
        "set_uva_callback_configuration",
        FunctionID.SET_UVA_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.0003"), Decimal("0.0003")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_uva_callback_configuration",
        FunctionID.SET_UVA_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.0003"), Decimal("0.0003"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_uva_callback_configuration",
        FunctionID.GET_UVA_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.0006"), Decimal("0.0007")
        ),
    ),
    Call("get_uvb", FunctionID.GET_UVB, (), reply=("i", (3,)), result=Decimal("0.0003")),
    Call(
        "set_uvb_callback_configuration",
        FunctionID.SET_UVB_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.0003"), Decimal("0.0003")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_uvb_callback_configuration",
        FunctionID.SET_UVB_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.0003"), Decimal("0.0003"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_uvb_callback_configuration",
        FunctionID.GET_UVB_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.0006"), Decimal("0.0007")
        ),
    ),
    Call("get_uvi", FunctionID.GET_UVI, (), reply=("i", (3,)), result=Decimal("0.3")),
    Call(
        "set_uvi_callback_configuration",
        FunctionID.SET_UVI_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("0.3")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_uvi_callback_configuration",
        FunctionID.SET_UVI_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("0.3"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_uvi_callback_configuration",
        FunctionID.GET_UVI_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.6"), Decimal("0.7")),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.IntegrationTime.INTEGRATION_TIME_800MS,),
        sent=("B", (4,)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.IntegrationTime.INTEGRATION_TIME_800MS, False),
        sent=("B", (4,)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B", (4,)),
        result=DEVICE.IntegrationTime.INTEGRATION_TIME_800MS,
    ),
    Call("get_value", FunctionID.GET_UVA, (0,), reply=("i", (3,)), result=Decimal("0.0003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_UVA_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.0003"), Decimal("0.0004")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_UVA_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.0003"), Decimal("0.0004")),
    ),
    Call("get_value", FunctionID.GET_UVB, (1,), reply=("i", (3,)), result=Decimal("0.0003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_UVB_CALLBACK_CONFIGURATION,
        (1, 1, True, Threshold.OUTSIDE, Decimal("0.0003"), Decimal("0.0004")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_UVB_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.0003"), Decimal("0.0004")),
    ),
    Call("get_value", FunctionID.GET_UVI, (2,), reply=("i", (3,)), result=Decimal("0.3")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_UVI_CALLBACK_CONFIGURATION,
        (2, 1, True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.4")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_UVI_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_uva_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.0003"), Decimal("0.0003"))),
    ("set_uva_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.0003"), Decimal("0.0003"))),
    ("set_uva_callback_configuration", (Decimal("0.003"), True, "o", Decimal("214748.3648"), Decimal("0.0003"))),
    ("set_uva_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.0003"), Decimal("214748.3648"))),
    ("set_uvb_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.0003"), Decimal("0.0003"))),
    ("set_uvb_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.0003"), Decimal("0.0003"))),
    ("set_uvb_callback_configuration", (Decimal("0.003"), True, "o", Decimal("214748.3648"), Decimal("0.0003"))),
    ("set_uvb_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.0003"), Decimal("214748.3648"))),
    ("set_uvi_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.3"), Decimal("0.3"))),
    ("set_uvi_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.3"), Decimal("0.3"))),
    ("set_uvi_callback_configuration", (Decimal("0.003"), True, "o", Decimal("214748364.8"), Decimal("0.3"))),
    ("set_uvi_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("214748364.8"))),
    ("set_configuration", (12345,)),
    ("get_value", (3,)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device: BrickletUVLightV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2118
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("UV Light Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_uva(device: BrickletUVLightV2, connection: FakeConnection) -> None:
    """The callback UVA is converted to an event."""
    connection.callback(CallbackID.UVA, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.UVA, Decimal("0.0003"))]


def test_callback_uvb(device: BrickletUVLightV2, connection: FakeConnection) -> None:
    """The callback UVB is converted to an event."""
    connection.callback(CallbackID.UVB, "i", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.UVB, Decimal("0.0003"))]


def test_callback_uvi(device: BrickletUVLightV2, connection: FakeConnection) -> None:
    """The callback UVI is converted to an event."""
    connection.callback(CallbackID.UVI, "i", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.UVI, Decimal("0.3"))]
