"""Tests for the Industrial Dual 0-20mA Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_dual_0_20ma import BrickletIndustrialDual020mA
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialDual020mA
FunctionID = BrickletIndustrialDual020mA.FunctionID
CallbackID = BrickletIndustrialDual020mA.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_CURRENT": 1,
    "SET_CURRENT_CALLBACK_PERIOD": 2,
    "GET_CURRENT_CALLBACK_PERIOD": 3,
    "SET_CURRENT_CALLBACK_THRESHOLD": 4,
    "GET_CURRENT_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "SET_SAMPLE_RATE": 8,
    "GET_SAMPLE_RATE": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"CURRENT": 10, "CURRENT_REACHED": 11}

CALLS: list[Call] = [
    Call("get_current", FunctionID.GET_CURRENT, (1,), sent=("B", (1,)), reply=("i", (3,)), result=Decimal("3E-9")),
    Call(
        "set_current_callback_period",
        FunctionID.SET_CURRENT_CALLBACK_PERIOD,
        (1, Decimal("0.003")),
        sent=("B I", (1, 3)),
    ),
    Call(
        "set_current_callback_period",
        FunctionID.SET_CURRENT_CALLBACK_PERIOD,
        (1, Decimal("0.003"), False),
        sent=("B I", (1, 3)),
        response_expected=False,
    ),
    Call(
        "get_current_callback_period",
        FunctionID.GET_CURRENT_CALLBACK_PERIOD,
        (1,),
        sent=("B", (1,)),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_current_callback_threshold",
        FunctionID.SET_CURRENT_CALLBACK_THRESHOLD,
        (1, "o", Decimal("3E-9"), Decimal("3E-9")),
        sent=("B c i i", (1, "o", 3, 3)),
    ),
    Call(
        "set_current_callback_threshold",
        FunctionID.SET_CURRENT_CALLBACK_THRESHOLD,
        (1, "o", Decimal("3E-9"), Decimal("3E-9"), False),
        sent=("B c i i", (1, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_current_callback_threshold",
        FunctionID.GET_CURRENT_CALLBACK_THRESHOLD,
        (1,),
        sent=("B", (1,)),
        reply=("c i i", ("o", 4, 5)),
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
    Call("set_sample_rate", FunctionID.SET_SAMPLE_RATE, (DEVICE.SampleRate.SAMPLE_RATE_4_SPS,), sent=("B", (3,))),
    Call(
        "set_sample_rate",
        FunctionID.SET_SAMPLE_RATE,
        (DEVICE.SampleRate.SAMPLE_RATE_4_SPS, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_sample_rate", FunctionID.GET_SAMPLE_RATE, (), reply=("B", (3,)), result=DEVICE.SampleRate.SAMPLE_RATE_4_SPS
    ),
    Call("get_value", FunctionID.GET_CURRENT, (0,), sent=("B", (0,)), reply=("i", (3,)), result=Decimal("3E-9")),
    Call("get_value", FunctionID.GET_CURRENT, (1,), sent=("B", (1,)), reply=("i", (3,)), result=Decimal("3E-9")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("get_current", (2,)),
    ("set_current_callback_period", (2, Decimal("0.003"))),
    ("set_current_callback_period", (1, Decimal("4294967.296"))),
    ("get_current_callback_period", (2,)),
    ("set_current_callback_threshold", (2, "o", Decimal("3E-9"), Decimal("3E-9"))),
    ("set_current_callback_threshold", (1, "?", Decimal("3E-9"), Decimal("3E-9"))),
    ("set_current_callback_threshold", (1, "o", Decimal("2.147483648"), Decimal("3E-9"))),
    ("set_current_callback_threshold", (1, "o", Decimal("3E-9"), Decimal("2.147483648"))),
    ("get_current_callback_threshold", (2,)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_sample_rate", (12345,)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device: BrickletIndustrialDual020mA) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 228
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Dual 0-20mA Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device: BrickletIndustrialDual020mA, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("3E-9"), Decimal("4E-9")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_CURRENT_CALLBACK_PERIOD, "B I", *(0, 1000)),
            request(FunctionID.SET_CURRENT_CALLBACK_THRESHOLD, "B c i i", *(0, "o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_CURRENT_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_CURRENT_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("3E-9"), Decimal("4E-9")
    )


def test_callback_configuration_of_sid_1(device: BrickletIndustrialDual020mA, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(1, 1, True, Threshold.OUTSIDE, Decimal("3E-9"), Decimal("4E-9")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_CURRENT_CALLBACK_PERIOD, "B I", *(1, 1000)),
            request(FunctionID.SET_CURRENT_CALLBACK_THRESHOLD, "B c i i", *(1, "o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_CURRENT_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_CURRENT_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("3E-9"), Decimal("4E-9")
    )


def test_callback_current(device: BrickletIndustrialDual020mA, connection: FakeConnection) -> None:
    """The callback CURRENT is converted to an event."""
    connection.callback(CallbackID.CURRENT, "B i", *(1, 4))
    assert summary(read_events(device)) == [(1, CallbackID.CURRENT, Decimal("4E-9"))]


def test_callback_current_reached(device: BrickletIndustrialDual020mA, connection: FakeConnection) -> None:
    """The callback CURRENT_REACHED is converted to an event."""
    connection.callback(CallbackID.CURRENT_REACHED, "B i", *(1, 4))
    assert summary(read_events(device)) == [(1, CallbackID.CURRENT_REACHED, Decimal("4E-9"))]
