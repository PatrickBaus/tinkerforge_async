"""Tests for the Real-Time Clock Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_real_time_clock_v2 import AlarmEvent, BrickletRealTimeClockV2, GetAlarm, GetDateTime
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletRealTimeClockV2
FunctionID = BrickletRealTimeClockV2.FunctionID
CallbackID = BrickletRealTimeClockV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_DATE_TIME": 1,
    "GET_DATE_TIME": 2,
    "GET_TIMESTAMP": 3,
    "SET_OFFSET": 4,
    "GET_OFFSET": 5,
    "SET_DATE_TIME_CALLBACK_CONFIGURATION": 6,
    "GET_DATE_TIME_CALLBACK_CONFIGURATION": 7,
    "SET_ALARM": 8,
    "GET_ALARM": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DATE_TIME": 10, "ALARM": 11}

CALLS: list[Call] = [
    Call(
        "set_date_time",
        FunctionID.SET_DATE_TIME,
        (2000, 3, 3, 3, 3, 3, 3, DEVICE.Weekday.SUNDAY),
        sent=("H B B B B B B B", (2000, 3, 3, 3, 3, 3, 3, 7)),
    ),
    Call(
        "set_date_time",
        FunctionID.SET_DATE_TIME,
        (2000, 3, 3, 3, 3, 3, 3, DEVICE.Weekday.SUNDAY, False),
        sent=("H B B B B B B B", (2000, 3, 3, 3, 3, 3, 3, 7)),
        response_expected=False,
    ),
    Call(
        "get_date_time",
        FunctionID.GET_DATE_TIME,
        (),
        reply=("H B B B B B B B q", (2000, 4, 5, 6, 7, 8, 9, 7, 11)),
        result=GetDateTime(2000, 4, 5, 6, 7, 8, 9, DEVICE.Weekday.SUNDAY, Decimal("0.011")),
    ),
    Call("get_timestamp", FunctionID.GET_TIMESTAMP, (), reply=("q", (3,)), result=Decimal("0.003")),
    Call("set_offset", FunctionID.SET_OFFSET, (Decimal("6.51"),), sent=("b", (3,))),
    Call("set_offset", FunctionID.SET_OFFSET, (Decimal("6.51"), False), sent=("b", (3,)), response_expected=False),
    Call("get_offset", FunctionID.GET_OFFSET, (), reply=("b", (3,)), result=Decimal("6.51")),
    Call(
        "set_date_time_callback_configuration",
        FunctionID.SET_DATE_TIME_CALLBACK_CONFIGURATION,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_date_time_callback_configuration",
        FunctionID.SET_DATE_TIME_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_date_time_callback_configuration",
        FunctionID.GET_DATE_TIME_CALLBACK_CONFIGURATION,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_alarm",
        FunctionID.SET_ALARM,
        (
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmInterval.DISABLED,
        ),
        sent=("b b b b b b i", (-1, -1, -1, -1, -1, -1, -1)),
    ),
    Call(
        "set_alarm",
        FunctionID.SET_ALARM,
        (
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmInterval.DISABLED,
            False,
        ),
        sent=("b b b b b b i", (-1, -1, -1, -1, -1, -1, -1)),
        response_expected=False,
    ),
    Call(
        "get_alarm",
        FunctionID.GET_ALARM,
        (),
        reply=("b b b b b b i", (-1, -1, -1, -1, -1, -1, -1)),
        result=GetAlarm(
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmInterval.DISABLED,
        ),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_date_time", (2100, 3, 3, 3, 3, 3, 3, DEVICE.Weekday.SUNDAY)),
    ("set_date_time", (2000, 13, 3, 3, 3, 3, 3, DEVICE.Weekday.SUNDAY)),
    ("set_date_time", (2000, 3, 32, 3, 3, 3, 3, DEVICE.Weekday.SUNDAY)),
    ("set_date_time", (2000, 3, 3, 24, 3, 3, 3, DEVICE.Weekday.SUNDAY)),
    ("set_date_time", (2000, 3, 3, 3, 60, 3, 3, DEVICE.Weekday.SUNDAY)),
    ("set_date_time", (2000, 3, 3, 3, 3, 60, 3, DEVICE.Weekday.SUNDAY)),
    ("set_date_time", (2000, 3, 3, 3, 3, 3, 100, DEVICE.Weekday.SUNDAY)),
    ("set_date_time", (2000, 3, 3, 3, 3, 3, 3, 12345)),
    ("set_offset", (Decimal("277.76"),)),
    ("set_date_time_callback_configuration", (Decimal("4294967.296"),)),
    (
        "set_alarm",
        (
            12345,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmInterval.DISABLED,
        ),
    ),
    (
        "set_alarm",
        (
            DEVICE.AlarmMatch.DISABLED,
            12345,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmInterval.DISABLED,
        ),
    ),
    (
        "set_alarm",
        (
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            12345,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmInterval.DISABLED,
        ),
    ),
    (
        "set_alarm",
        (
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            12345,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmInterval.DISABLED,
        ),
    ),
    (
        "set_alarm",
        (
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            12345,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmInterval.DISABLED,
        ),
    ),
    (
        "set_alarm",
        (
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            12345,
            DEVICE.AlarmInterval.DISABLED,
        ),
    ),
    (
        "set_alarm",
        (
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            DEVICE.AlarmMatch.DISABLED,
            12345,
        ),
    ),
]


def test_identity(device: BrickletRealTimeClockV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2106
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Real-Time Clock Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_date_time(device: BrickletRealTimeClockV2, connection: FakeConnection) -> None:
    """The callback DATE_TIME is converted to an event."""
    connection.callback(CallbackID.DATE_TIME, "H B B B B B B B q", *(2000, 4, 5, 6, 7, 8, 9, 7, 11))
    assert summary(read_events(device)) == [
        (0, CallbackID.DATE_TIME, GetDateTime(2000, 4, 5, 6, 7, 8, 9, DEVICE.Weekday.SUNDAY, Decimal("0.011")))
    ]


def test_callback_alarm(device: BrickletRealTimeClockV2, connection: FakeConnection) -> None:
    """The callback ALARM is converted to an event."""
    connection.callback(CallbackID.ALARM, "H B B B B B B B q", *(2000, 4, 5, 6, 7, 8, 9, 7, 11))
    assert summary(read_events(device)) == [
        (1, CallbackID.ALARM, AlarmEvent(2000, 4, 5, 6, 7, 8, 9, DEVICE.Weekday.SUNDAY, Decimal("0.011")))
    ]
