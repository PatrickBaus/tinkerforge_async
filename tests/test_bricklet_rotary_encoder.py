"""Tests for the Rotary Encoder Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_rotary_encoder import BrickletRotaryEncoder
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletRotaryEncoder
FunctionID = BrickletRotaryEncoder.FunctionID
CallbackID = BrickletRotaryEncoder.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_COUNT": 1,
    "SET_COUNT_CALLBACK_PERIOD": 2,
    "GET_COUNT_CALLBACK_PERIOD": 3,
    "SET_COUNT_CALLBACK_THRESHOLD": 4,
    "GET_COUNT_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "IS_PRESSED": 10,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"COUNT": 8, "COUNT_REACHED": 9, "PRESSED": 11, "RELEASED": 12}

CALLS: list[Call] = [
    Call("get_count", FunctionID.GET_COUNT, (True,), sent=("!", (True,)), reply=("i", (3,)), result=3),
    Call("set_count_callback_period", FunctionID.SET_COUNT_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_count_callback_period",
        FunctionID.SET_COUNT_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_count_callback_period",
        FunctionID.GET_COUNT_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_count_callback_threshold",
        FunctionID.SET_COUNT_CALLBACK_THRESHOLD,
        ("o", 3, 3),
        sent=("c i i", ("o", 3, 3)),
    ),
    Call(
        "set_count_callback_threshold",
        FunctionID.SET_COUNT_CALLBACK_THRESHOLD,
        ("o", 3, 3, False),
        sent=("c i i", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_count_callback_threshold",
        FunctionID.GET_COUNT_CALLBACK_THRESHOLD,
        (),
        reply=("c i i", ("o", 4, 5)),
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
    Call("is_pressed", FunctionID.IS_PRESSED, (), reply=("!", (True,)), result=True),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_count_callback_period", (Decimal("4294967.296"),)),
    ("set_count_callback_threshold", ("?", 3, 3)),
    ("set_count_callback_threshold", ("o", 2147483648, 3)),
    ("set_count_callback_threshold", ("o", 3, 2147483648)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device: BrickletRotaryEncoder) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 236
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Rotary Encoder Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device: BrickletRotaryEncoder, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, 3, 4))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_COUNT_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_COUNT_CALLBACK_THRESHOLD, "c i i", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_COUNT_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_COUNT_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")
    )


def test_callback_count(device: BrickletRotaryEncoder, connection: FakeConnection) -> None:
    """The callback COUNT is converted to an event."""
    connection.callback(CallbackID.COUNT, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.COUNT, 3)]


def test_callback_count_reached(device: BrickletRotaryEncoder, connection: FakeConnection) -> None:
    """The callback COUNT_REACHED is converted to an event."""
    connection.callback(CallbackID.COUNT_REACHED, "i", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.COUNT_REACHED, 3)]


def test_callback_pressed(device: BrickletRotaryEncoder, connection: FakeConnection) -> None:
    """The callback PRESSED is converted to an event."""
    connection.callback(CallbackID.PRESSED)
    assert summary(read_events(device)) == [(1, CallbackID.PRESSED, None)]


def test_callback_released(device: BrickletRotaryEncoder, connection: FakeConnection) -> None:
    """The callback RELEASED is converted to an event."""
    connection.callback(CallbackID.RELEASED)
    assert summary(read_events(device)) == [(2, CallbackID.RELEASED, None)]
