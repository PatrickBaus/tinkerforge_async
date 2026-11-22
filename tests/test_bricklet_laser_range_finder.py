"""Tests for the Laser Range Finder Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_laser_range_finder import BrickletLaserRangeFinder, GetConfiguration, GetMovingAverage
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletLaserRangeFinder
FunctionID = BrickletLaserRangeFinder.FunctionID
CallbackID = BrickletLaserRangeFinder.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_DISTANCE": 1,
    "GET_VELOCITY": 2,
    "SET_DISTANCE_CALLBACK_PERIOD": 3,
    "GET_DISTANCE_CALLBACK_PERIOD": 4,
    "SET_VELOCITY_CALLBACK_PERIOD": 5,
    "GET_VELOCITY_CALLBACK_PERIOD": 6,
    "SET_DISTANCE_CALLBACK_THRESHOLD": 7,
    "GET_DISTANCE_CALLBACK_THRESHOLD": 8,
    "SET_VELOCITY_CALLBACK_THRESHOLD": 9,
    "GET_VELOCITY_CALLBACK_THRESHOLD": 10,
    "SET_DEBOUNCE_PERIOD": 11,
    "GET_DEBOUNCE_PERIOD": 12,
    "SET_MOVING_AVERAGE": 13,
    "GET_MOVING_AVERAGE": 14,
    "SET_MODE": 15,
    "GET_MODE": 16,
    "ENABLE_LASER": 17,
    "DISABLE_LASER": 18,
    "IS_LASER_ENABLED": 19,
    "GET_SENSOR_HARDWARE_VERSION": 24,
    "SET_CONFIGURATION": 25,
    "GET_CONFIGURATION": 26,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DISTANCE": 20, "VELOCITY": 21, "DISTANCE_REACHED": 22, "VELOCITY_REACHED": 23}

CALLS: list[Call] = [
    Call("get_distance", FunctionID.GET_DISTANCE, (), reply=("H", (3,)), result=Decimal("0.03")),
    Call("get_velocity", FunctionID.GET_VELOCITY, (), reply=("h", (3,)), result=Decimal("0.03")),
    Call(
        "set_distance_callback_period", FunctionID.SET_DISTANCE_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))
    ),
    Call(
        "set_distance_callback_period",
        FunctionID.SET_DISTANCE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_distance_callback_period",
        FunctionID.GET_DISTANCE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_velocity_callback_period", FunctionID.SET_VELOCITY_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))
    ),
    Call(
        "set_velocity_callback_period",
        FunctionID.SET_VELOCITY_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_velocity_callback_period",
        FunctionID.GET_VELOCITY_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_distance_callback_threshold",
        FunctionID.SET_DISTANCE_CALLBACK_THRESHOLD,
        ("o", Decimal("0.03"), Decimal("0.03")),
        sent=("c H H", ("o", 3, 3)),
    ),
    Call(
        "set_distance_callback_threshold",
        FunctionID.SET_DISTANCE_CALLBACK_THRESHOLD,
        ("o", Decimal("0.03"), Decimal("0.03"), False),
        sent=("c H H", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_distance_callback_threshold",
        FunctionID.GET_DISTANCE_CALLBACK_THRESHOLD,
        (),
        reply=("c H H", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.04"), Decimal("0.05")),
    ),
    Call(
        "set_velocity_callback_threshold",
        FunctionID.SET_VELOCITY_CALLBACK_THRESHOLD,
        ("o", Decimal("0.03"), Decimal("0.03")),
        sent=("c h h", ("o", 3, 3)),
    ),
    Call(
        "set_velocity_callback_threshold",
        FunctionID.SET_VELOCITY_CALLBACK_THRESHOLD,
        ("o", Decimal("0.03"), Decimal("0.03"), False),
        sent=("c h h", ("o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_velocity_callback_threshold",
        FunctionID.GET_VELOCITY_CALLBACK_THRESHOLD,
        (),
        reply=("c h h", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.04"), Decimal("0.05")),
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
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (3, 3), sent=("B B", (3, 3))),
    Call(
        "set_moving_average",
        FunctionID.SET_MOVING_AVERAGE,
        (3, 3, False),
        sent=("B B", (3, 3)),
        response_expected=False,
    ),
    Call("get_moving_average", FunctionID.GET_MOVING_AVERAGE, (), reply=("B B", (3, 4)), result=GetMovingAverage(3, 4)),
    Call("set_mode", FunctionID.SET_MODE, (DEVICE.Mode.VELOCITY_MAX_127MS,), sent=("B", (4,))),
    Call(
        "set_mode",
        FunctionID.SET_MODE,
        (DEVICE.Mode.VELOCITY_MAX_127MS, False),
        sent=("B", (4,)),
        response_expected=False,
    ),
    Call("get_mode", FunctionID.GET_MODE, (), reply=("B", (4,)), result=DEVICE.Mode.VELOCITY_MAX_127MS),
    Call("enable_laser", FunctionID.ENABLE_LASER, ()),
    Call("enable_laser", FunctionID.ENABLE_LASER, (False,), response_expected=False),
    Call("disable_laser", FunctionID.DISABLE_LASER, ()),
    Call("disable_laser", FunctionID.DISABLE_LASER, (False,), response_expected=False),
    Call("is_laser_enabled", FunctionID.IS_LASER_ENABLED, (), reply=("!", (True,)), result=True),
    Call(
        "get_sensor_hardware_version",
        FunctionID.GET_SENSOR_HARDWARE_VERSION,
        (),
        reply=("B", (3,)),
        result=DEVICE.Version.VERSION_3,
    ),
    Call(
        "set_configuration", FunctionID.SET_CONFIGURATION, (3, True, 3, Decimal("0")), sent=("B ! B H", (3, True, 3, 0))
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (3, True, 3, Decimal("0"), False),
        sent=("B ! B H", (3, True, 3, 0)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B ! B H", (3, True, 5, 0)),
        result=GetConfiguration(3, True, 5, Decimal("0")),
    ),
    Call("get_value", FunctionID.GET_DISTANCE, (0,), reply=("H", (3,)), result=Decimal("0.03")),
    Call("get_value", FunctionID.GET_VELOCITY, (1,), reply=("h", (3,)), result=Decimal("0.03")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_distance_callback_period", (Decimal("4294967.296"),)),
    ("set_velocity_callback_period", (Decimal("4294967.296"),)),
    ("set_distance_callback_threshold", ("?", Decimal("0.03"), Decimal("0.03"))),
    ("set_distance_callback_threshold", ("o", Decimal("655.36"), Decimal("0.03"))),
    ("set_distance_callback_threshold", ("o", Decimal("0.03"), Decimal("655.36"))),
    ("set_velocity_callback_threshold", ("?", Decimal("0.03"), Decimal("0.03"))),
    ("set_velocity_callback_threshold", ("o", Decimal("327.68"), Decimal("0.03"))),
    ("set_velocity_callback_threshold", ("o", Decimal("0.03"), Decimal("327.68"))),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_moving_average", (31, 3)),
    ("set_moving_average", (3, 31)),
    ("set_mode", (12345,)),
    ("set_configuration", (256, True, 3, Decimal("0"))),
    ("set_configuration", (3, True, 256, Decimal("0"))),
    ("set_configuration", (3, True, 3, Decimal("65536"))),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device: BrickletLaserRangeFinder) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 255
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Laser Range Finder Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device: BrickletLaserRangeFinder, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_DISTANCE_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_DISTANCE_CALLBACK_THRESHOLD, "c H H", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_DISTANCE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_DISTANCE_CALLBACK_THRESHOLD, "c H H", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")
    )


def test_callback_configuration_of_sid_1(device: BrickletLaserRangeFinder, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(1, 1, True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_VELOCITY_CALLBACK_PERIOD, "I", *(1000,)),
            request(FunctionID.SET_VELOCITY_CALLBACK_THRESHOLD, "c h h", *("o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_VELOCITY_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_VELOCITY_CALLBACK_THRESHOLD, "c h h", "o", 3, 4)
    assert run(device.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")
    )


def test_callback_distance(device: BrickletLaserRangeFinder, connection: FakeConnection) -> None:
    """The callback DISTANCE is converted to an event."""
    connection.callback(CallbackID.DISTANCE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.DISTANCE, Decimal("0.03"))]


def test_callback_velocity(device: BrickletLaserRangeFinder, connection: FakeConnection) -> None:
    """The callback VELOCITY is converted to an event."""
    connection.callback(CallbackID.VELOCITY, "h", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.VELOCITY, Decimal("0.03"))]


def test_callback_distance_reached(device: BrickletLaserRangeFinder, connection: FakeConnection) -> None:
    """The callback DISTANCE_REACHED is converted to an event."""
    connection.callback(CallbackID.DISTANCE_REACHED, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.DISTANCE_REACHED, Decimal("0.03"))]


def test_callback_velocity_reached(device: BrickletLaserRangeFinder, connection: FakeConnection) -> None:
    """The callback VELOCITY_REACHED is converted to an event."""
    connection.callback(CallbackID.VELOCITY_REACHED, "h", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.VELOCITY_REACHED, Decimal("0.03"))]
