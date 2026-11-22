"""Tests for the Sound Intensity Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_sound_intensity import BrickletSoundIntensity
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletSoundIntensity
FunctionID = BrickletSoundIntensity.FunctionID
CallbackID = BrickletSoundIntensity.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_INTENSITY": 1,
    "SET_INTENSITY_CALLBACK_PERIOD": 2,
    "GET_INTENSITY_CALLBACK_PERIOD": 3,
    "SET_INTENSITY_CALLBACK_THRESHOLD": 4,
    "GET_INTENSITY_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"INTENSITY": 8, "INTENSITY_REACHED": 9}

CALLS: list[Call] = [
    Call("get_intensity", FunctionID.GET_INTENSITY, (), reply=("H", (3,)), result=3),
    Call(
        "set_intensity_callback_period", FunctionID.SET_INTENSITY_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))
    ),
    Call(
        "set_intensity_callback_period",
        FunctionID.SET_INTENSITY_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_intensity_callback_period",
        FunctionID.GET_INTENSITY_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_intensity_callback_threshold",
        FunctionID.SET_INTENSITY_CALLBACK_THRESHOLD,
        ("o", 3, 3),
        sent=("c H H", ("o", 3, 3)),
    ),
    Call(
        "set_intensity_callback_threshold",
        FunctionID.SET_INTENSITY_CALLBACK_THRESHOLD,
        ("o", 3, 3, False),
        sent=("c H H", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_intensity_callback_threshold",
        FunctionID.GET_INTENSITY_CALLBACK_THRESHOLD,
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
    Call("get_value", FunctionID.GET_INTENSITY, (0,), reply=("H", (3,)), result=3),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_intensity_callback_period", (Decimal("4294967.296"),)),
    ("set_intensity_callback_threshold", ("?", 3, 3)),
    ("set_intensity_callback_threshold", ("o", 65536, 3)),
    ("set_intensity_callback_threshold", ("o", 3, 65536)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device: BrickletSoundIntensity) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 238
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Sound Intensity Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device: BrickletSoundIntensity, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, 3, 4))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_INTENSITY_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_INTENSITY_CALLBACK_THRESHOLD, "c H H", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_INTENSITY_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_INTENSITY_CALLBACK_THRESHOLD, "c H H", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")
    )


def test_callback_intensity(device: BrickletSoundIntensity, connection: FakeConnection) -> None:
    """The callback INTENSITY is converted to an event."""
    connection.callback(CallbackID.INTENSITY, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.INTENSITY, 3)]


def test_callback_intensity_reached(device: BrickletSoundIntensity, connection: FakeConnection) -> None:
    """The callback INTENSITY_REACHED is converted to an event."""
    connection.callback(CallbackID.INTENSITY_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.INTENSITY_REACHED, 3)]
