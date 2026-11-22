"""Tests for the CO2 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_co2 import BrickletCO2
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletCO2
FunctionID = BrickletCO2.FunctionID
CallbackID = BrickletCO2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_CO2_CONCENTRATION": 1,
    "SET_CO2_CONCENTRATION_CALLBACK_PERIOD": 2,
    "GET_CO2_CONCENTRATION_CALLBACK_PERIOD": 3,
    "SET_CO2_CONCENTRATION_CALLBACK_THRESHOLD": 4,
    "GET_CO2_CONCENTRATION_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"CO2_CONCENTRATION": 8, "CO2_CONCENTRATION_REACHED": 9}

CALLS: list[Call] = [
    Call("get_co2_concentration", FunctionID.GET_CO2_CONCENTRATION, (), reply=("H", (3,)), result=Decimal("3")),
    Call(
        "set_co2_concentration_callback_period",
        FunctionID.SET_CO2_CONCENTRATION_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_co2_concentration_callback_period",
        FunctionID.SET_CO2_CONCENTRATION_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_co2_concentration_callback_period",
        FunctionID.GET_CO2_CONCENTRATION_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_co2_concentration_callback_threshold",
        FunctionID.SET_CO2_CONCENTRATION_CALLBACK_THRESHOLD,
        ("o", Decimal("3"), Decimal("3")),
        sent=("c H H", ("o", 3, 3)),
    ),
    Call(
        "set_co2_concentration_callback_threshold",
        FunctionID.SET_CO2_CONCENTRATION_CALLBACK_THRESHOLD,
        ("o", Decimal("3"), Decimal("3"), False),
        sent=("c H H", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_co2_concentration_callback_threshold",
        FunctionID.GET_CO2_CONCENTRATION_CALLBACK_THRESHOLD,
        (),
        reply=("c H H", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("4"), Decimal("5")),
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
    Call("get_value", FunctionID.GET_CO2_CONCENTRATION, (0,), reply=("H", (3,)), result=Decimal("3")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_co2_concentration_callback_period", (Decimal("4294967.296"),)),
    ("set_co2_concentration_callback_threshold", ("?", Decimal("3"), Decimal("3"))),
    ("set_co2_concentration_callback_threshold", ("o", Decimal("65536"), Decimal("3"))),
    ("set_co2_concentration_callback_threshold", ("o", Decimal("3"), Decimal("65536"))),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device: BrickletCO2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 262
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("CO2 Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device: BrickletCO2, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_CO2_CONCENTRATION_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_CO2_CONCENTRATION_CALLBACK_THRESHOLD, "c H H", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_CO2_CONCENTRATION_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_CO2_CONCENTRATION_CALLBACK_THRESHOLD, "c H H", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")
    )


def test_callback_co2_concentration(device: BrickletCO2, connection: FakeConnection) -> None:
    """The callback CO2_CONCENTRATION is converted to an event."""
    connection.callback(CallbackID.CO2_CONCENTRATION, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.CO2_CONCENTRATION, Decimal("3"))]


def test_callback_co2_concentration_reached(device: BrickletCO2, connection: FakeConnection) -> None:
    """The callback CO2_CONCENTRATION_REACHED is converted to an event."""
    connection.callback(CallbackID.CO2_CONCENTRATION_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.CO2_CONCENTRATION_REACHED, Decimal("3"))]
