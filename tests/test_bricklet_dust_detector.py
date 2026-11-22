"""Tests for the Dust Detector Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_dust_detector import BrickletDustDetector
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletDustDetector
FunctionID = BrickletDustDetector.FunctionID
CallbackID = BrickletDustDetector.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_DUST_DENSITY": 1,
    "SET_DUST_DENSITY_CALLBACK_PERIOD": 2,
    "GET_DUST_DENSITY_CALLBACK_PERIOD": 3,
    "SET_DUST_DENSITY_CALLBACK_THRESHOLD": 4,
    "GET_DUST_DENSITY_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "SET_MOVING_AVERAGE": 10,
    "GET_MOVING_AVERAGE": 11,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DUST_DENSITY": 8, "DUST_DENSITY_REACHED": 9}

CALLS: list[Call] = [
    Call("get_dust_density", FunctionID.GET_DUST_DENSITY, (), reply=("H", (3,)), result=Decimal("3E-9")),
    Call(
        "set_dust_density_callback_period",
        FunctionID.SET_DUST_DENSITY_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_dust_density_callback_period",
        FunctionID.SET_DUST_DENSITY_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_dust_density_callback_period",
        FunctionID.GET_DUST_DENSITY_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_dust_density_callback_threshold",
        FunctionID.SET_DUST_DENSITY_CALLBACK_THRESHOLD,
        ("o", Decimal("3E-9"), Decimal("3E-9")),
        sent=("c H H", ("o", 3, 3)),
    ),
    Call(
        "set_dust_density_callback_threshold",
        FunctionID.SET_DUST_DENSITY_CALLBACK_THRESHOLD,
        ("o", Decimal("3E-9"), Decimal("3E-9"), False),
        sent=("c H H", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_dust_density_callback_threshold",
        FunctionID.GET_DUST_DENSITY_CALLBACK_THRESHOLD,
        (),
        reply=("c H H", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("4E-9"), Decimal("5E-9")),
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
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3,), sent=("B", (3,))),
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3, False), sent=("B", (3,)), response_expected=False),
    Call("get_moving_average", FunctionID.GET_MOVING_AVERAGE, (), reply=("B", (3,)), result=3),
    Call("get_value", FunctionID.GET_DUST_DENSITY, (0,), reply=("H", (3,)), result=Decimal("3E-9")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_dust_density_callback_period", (Decimal("4294967.296"),)),
    ("set_dust_density_callback_threshold", ("?", Decimal("3E-9"), Decimal("3E-9"))),
    ("set_dust_density_callback_threshold", ("o", Decimal("0.000065536"), Decimal("3E-9"))),
    ("set_dust_density_callback_threshold", ("o", Decimal("3E-9"), Decimal("0.000065536"))),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_moving_average", (101,)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device: BrickletDustDetector) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 260
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Dust Detector Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device: BrickletDustDetector, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("3E-9"), Decimal("4E-9")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_DUST_DENSITY_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_DUST_DENSITY_CALLBACK_THRESHOLD, "c H H", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_DUST_DENSITY_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_DUST_DENSITY_CALLBACK_THRESHOLD, "c H H", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("3E-9"), Decimal("4E-9")
    )


def test_callback_dust_density(device: BrickletDustDetector, connection: FakeConnection) -> None:
    """The callback DUST_DENSITY is converted to an event."""
    connection.callback(CallbackID.DUST_DENSITY, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.DUST_DENSITY, Decimal("3E-9"))]


def test_callback_dust_density_reached(device: BrickletDustDetector, connection: FakeConnection) -> None:
    """The callback DUST_DENSITY_REACHED is converted to an event."""
    connection.callback(CallbackID.DUST_DENSITY_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.DUST_DENSITY_REACHED, Decimal("3E-9"))]
