"""Tests for the Hall Effect Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_hall_effect_v2 import BrickletHallEffectV2, GetCounterConfig
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletHallEffectV2
FunctionID = BrickletHallEffectV2.FunctionID
CallbackID = BrickletHallEffectV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_MAGNETIC_FLUX_DENSITY": 1,
    "SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION": 2,
    "GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION": 3,
    "GET_COUNTER": 5,
    "SET_COUNTER_CONFIG": 6,
    "GET_COUNTER_CONFIG": 7,
    "SET_COUNTER_CALLBACK_CONFIGURATION": 8,
    "GET_COUNTER_CALLBACK_CONFIGURATION": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"MAGNETIC_FLUX_DENSITY": 4, "COUNTER": 10}

CALLS: list[Call] = [
    Call(
        "get_magnetic_flux_density",
        FunctionID.GET_MAGNETIC_FLUX_DENSITY,
        (),
        reply=("h", (3,)),
        result=Decimal("0.000003"),
    ),
    Call(
        "set_magnetic_flux_density_callback_configuration",
        FunctionID.SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.000003"), Decimal("0.000003")),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_magnetic_flux_density_callback_configuration",
        FunctionID.SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.000003"), Decimal("0.000003"), False),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_magnetic_flux_density_callback_configuration",
        FunctionID.GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c h h", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.000006"), Decimal("0.000007")
        ),
    ),
    Call("get_counter", FunctionID.GET_COUNTER, (True,), sent=("!", (True,)), reply=("I", (3,)), result=3),
    Call(
        "set_counter_config",
        FunctionID.SET_COUNTER_CONFIG,
        (Decimal("0.000003"), Decimal("0.000003"), Decimal("0.000003")),
        sent=("h h I", (3, 3, 3)),
    ),
    Call(
        "set_counter_config",
        FunctionID.SET_COUNTER_CONFIG,
        (Decimal("0.000003"), Decimal("0.000003"), Decimal("0.000003"), False),
        sent=("h h I", (3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_counter_config",
        FunctionID.GET_COUNTER_CONFIG,
        (),
        reply=("h h I", (3, 4, 5)),
        result=GetCounterConfig(Decimal("0.000003"), Decimal("0.000004"), Decimal("0.000005")),
    ),
    Call(
        "set_counter_callback_configuration",
        FunctionID.SET_COUNTER_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_counter_callback_configuration",
        FunctionID.SET_COUNTER_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_counter_callback_configuration",
        FunctionID.GET_COUNTER_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("get_value", FunctionID.GET_MAGNETIC_FLUX_DENSITY, (0,), reply=("h", (3,)), result=Decimal("0.000003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.000003"), Decimal("0.000004")),
        sent=("I ! c h h", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c h h", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(
            Decimal(1), True, Threshold.OUTSIDE, Decimal("0.000003"), Decimal("0.000004")
        ),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_COUNTER_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_COUNTER_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    (
        "set_magnetic_flux_density_callback_configuration",
        (Decimal("4294967.296"), True, "o", Decimal("0.000003"), Decimal("0.000003")),
    ),
    (
        "set_magnetic_flux_density_callback_configuration",
        (Decimal("0.003"), True, "?", Decimal("0.000003"), Decimal("0.000003")),
    ),
    (
        "set_magnetic_flux_density_callback_configuration",
        (Decimal("0.003"), True, "o", Decimal("0.032768"), Decimal("0.000003")),
    ),
    (
        "set_magnetic_flux_density_callback_configuration",
        (Decimal("0.003"), True, "o", Decimal("0.000003"), Decimal("0.032768")),
    ),
    ("set_counter_config", (Decimal("0.032768"), Decimal("0.000003"), Decimal("0.000003"))),
    ("set_counter_config", (Decimal("0.000003"), Decimal("0.032768"), Decimal("0.000003"))),
    ("set_counter_config", (Decimal("0.000003"), Decimal("0.000003"), Decimal("1.000001"))),
    ("set_counter_callback_configuration", (Decimal("4294967.296"), True)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device: BrickletHallEffectV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2132
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Hall Effect Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_magnetic_flux_density(device: BrickletHallEffectV2, connection: FakeConnection) -> None:
    """The callback MAGNETIC_FLUX_DENSITY is converted to an event."""
    connection.callback(CallbackID.MAGNETIC_FLUX_DENSITY, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.MAGNETIC_FLUX_DENSITY, Decimal("0.000003"))]


def test_callback_counter(device: BrickletHallEffectV2, connection: FakeConnection) -> None:
    """The callback COUNTER is converted to an event."""
    connection.callback(CallbackID.COUNTER, "I", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.COUNTER, 3)]
