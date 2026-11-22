"""Tests for the Accelerometer Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_accelerometer import (
    BrickletAccelerometer,
    GetAcceleration,
    GetAccelerationCallbackThreshold,
    GetConfiguration,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletAccelerometer
FunctionID = BrickletAccelerometer.FunctionID
CallbackID = BrickletAccelerometer.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_ACCELERATION": 1,
    "SET_ACCELERATION_CALLBACK_PERIOD": 2,
    "GET_ACCELERATION_CALLBACK_PERIOD": 3,
    "SET_ACCELERATION_CALLBACK_THRESHOLD": 4,
    "GET_ACCELERATION_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "GET_TEMPERATURE": 8,
    "SET_CONFIGURATION": 9,
    "GET_CONFIGURATION": 10,
    "LED_ON": 11,
    "LED_OFF": 12,
    "IS_LED_ON": 13,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"ACCELERATION": 14, "ACCELERATION_REACHED": 15}

CALLS: list[Call] = [
    Call(
        "get_acceleration",
        FunctionID.GET_ACCELERATION,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetAcceleration(Decimal("0.02941995"), Decimal("0.0392266"), Decimal("0.04903325")),
    ),
    Call(
        "set_acceleration_callback_period",
        FunctionID.SET_ACCELERATION_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_acceleration_callback_period",
        FunctionID.SET_ACCELERATION_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_acceleration_callback_period",
        FunctionID.GET_ACCELERATION_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_acceleration_callback_threshold",
        FunctionID.SET_ACCELERATION_CALLBACK_THRESHOLD,
        (
            "o",
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
        ),
        sent=("c h h h h h h", ("o", 3, 3, 3, 3, 3, 3)),
    ),
    Call(
        "set_acceleration_callback_threshold",
        FunctionID.SET_ACCELERATION_CALLBACK_THRESHOLD,
        (
            "o",
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            False,
        ),
        sent=("c h h h h h h", ("o", 3, 3, 3, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_acceleration_callback_threshold",
        FunctionID.GET_ACCELERATION_CALLBACK_THRESHOLD,
        (),
        reply=("c h h h h h h", ("o", 4, 5, 6, 7, 8, 9)),
        result=GetAccelerationCallbackThreshold(
            Threshold.OUTSIDE,
            Decimal("0.0392266"),
            Decimal("0.04903325"),
            Decimal("0.0588399"),
            Decimal("0.06864655"),
            Decimal("0.0784532"),
            Decimal("0.08825985"),
        ),
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
    Call("get_temperature", FunctionID.GET_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("276.15")),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (
            DEVICE.DataRate.DATA_RATE_1600HZ,
            DEVICE.FullScale.FULL_SCALE_16G,
            DEVICE.FilterBandwidth.FILTER_BANDWIDTH_50HZ,
        ),
        sent=("B B B", (9, 4, 3)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (
            DEVICE.DataRate.DATA_RATE_1600HZ,
            DEVICE.FullScale.FULL_SCALE_16G,
            DEVICE.FilterBandwidth.FILTER_BANDWIDTH_50HZ,
            False,
        ),
        sent=("B B B", (9, 4, 3)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B B", (9, 4, 3)),
        result=GetConfiguration(
            DEVICE.DataRate.DATA_RATE_1600HZ,
            DEVICE.FullScale.FULL_SCALE_16G,
            DEVICE.FilterBandwidth.FILTER_BANDWIDTH_50HZ,
        ),
    ),
    Call("led_on", FunctionID.LED_ON, ()),
    Call("led_on", FunctionID.LED_ON, (False,), response_expected=False),
    Call("led_off", FunctionID.LED_OFF, ()),
    Call("led_off", FunctionID.LED_OFF, (False,), response_expected=False),
    Call("is_led_on", FunctionID.IS_LED_ON, (), reply=("!", (True,)), result=True),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_acceleration_callback_period", (Decimal("4294967.296"),)),
    (
        "set_acceleration_callback_threshold",
        (
            "?",
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
        ),
    ),
    (
        "set_acceleration_callback_threshold",
        (
            "o",
            Decimal("321.3443072"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
        ),
    ),
    (
        "set_acceleration_callback_threshold",
        (
            "o",
            Decimal("0.02941995"),
            Decimal("321.3443072"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
        ),
    ),
    (
        "set_acceleration_callback_threshold",
        (
            "o",
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("321.3443072"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
        ),
    ),
    (
        "set_acceleration_callback_threshold",
        (
            "o",
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("321.3443072"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
        ),
    ),
    (
        "set_acceleration_callback_threshold",
        (
            "o",
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("321.3443072"),
            Decimal("0.02941995"),
        ),
    ),
    (
        "set_acceleration_callback_threshold",
        (
            "o",
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("0.02941995"),
            Decimal("321.3443072"),
        ),
    ),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_configuration", (12345, DEVICE.FullScale.FULL_SCALE_16G, DEVICE.FilterBandwidth.FILTER_BANDWIDTH_50HZ)),
    ("set_configuration", (DEVICE.DataRate.DATA_RATE_1600HZ, 12345, DEVICE.FilterBandwidth.FILTER_BANDWIDTH_50HZ)),
    ("set_configuration", (DEVICE.DataRate.DATA_RATE_1600HZ, DEVICE.FullScale.FULL_SCALE_16G, 12345)),
]


def test_identity(device: BrickletAccelerometer) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 250
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Accelerometer Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_acceleration(device: BrickletAccelerometer, connection: FakeConnection) -> None:
    """The callback ACCELERATION is converted to an event."""
    connection.callback(CallbackID.ACCELERATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.ACCELERATION,
            GetAcceleration(Decimal("0.02941995"), Decimal("0.0392266"), Decimal("0.04903325")),
        )
    ]


def test_callback_acceleration_reached(device: BrickletAccelerometer, connection: FakeConnection) -> None:
    """The callback ACCELERATION_REACHED is converted to an event."""
    connection.callback(CallbackID.ACCELERATION_REACHED, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (
            1,
            CallbackID.ACCELERATION_REACHED,
            GetAcceleration(Decimal("0.02941995"), Decimal("0.0392266"), Decimal("0.04903325")),
        )
    ]
