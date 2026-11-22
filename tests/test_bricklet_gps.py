"""Tests for the GPS Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_gps import BrickletGPS, GetAltitude, GetCoordinates, GetDateTime, GetMotion, GetStatus
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletGPS
FunctionID = BrickletGPS.FunctionID
CallbackID = BrickletGPS.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_COORDINATES": 1,
    "GET_STATUS": 2,
    "GET_ALTITUDE": 3,
    "GET_MOTION": 4,
    "GET_DATE_TIME": 5,
    "RESTART": 6,
    "SET_COORDINATES_CALLBACK_PERIOD": 7,
    "GET_COORDINATES_CALLBACK_PERIOD": 8,
    "SET_STATUS_CALLBACK_PERIOD": 9,
    "GET_STATUS_CALLBACK_PERIOD": 10,
    "SET_ALTITUDE_CALLBACK_PERIOD": 11,
    "GET_ALTITUDE_CALLBACK_PERIOD": 12,
    "SET_MOTION_CALLBACK_PERIOD": 13,
    "GET_MOTION_CALLBACK_PERIOD": 14,
    "SET_DATE_TIME_CALLBACK_PERIOD": 15,
    "GET_DATE_TIME_CALLBACK_PERIOD": 16,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"COORDINATES": 17, "STATUS": 18, "ALTITUDE": 19, "MOTION": 20, "DATE_TIME": 21}

CALLS: list[Call] = [
    Call(
        "get_coordinates",
        FunctionID.GET_COORDINATES,
        (),
        reply=("I c I c H H H H", (3, "a", 5, "a", 7, 8, 9, 10)),
        result=GetCoordinates(
            Decimal("0.000003"),
            "a",
            Decimal("0.000005"),
            "a",
            Decimal("0.07"),
            Decimal("0.08"),
            Decimal("0.09"),
            Decimal("0.1"),
        ),
    ),
    Call(
        "get_status",
        FunctionID.GET_STATUS,
        (),
        reply=("B B B", (3, 4, 5)),
        result=GetStatus(DEVICE.Fix.FIX_3D_FIX, 4, 5),
    ),
    Call(
        "get_altitude",
        FunctionID.GET_ALTITUDE,
        (),
        reply=("i i", (3, 4)),
        result=GetAltitude(Decimal("0.03"), Decimal("0.04")),
    ),
    Call(
        "get_motion",
        FunctionID.GET_MOTION,
        (),
        reply=("I I", (3, 4)),
        result=GetMotion(Decimal("0.03"), Decimal("0.01111111111111111111111111111")),
    ),
    Call("get_date_time", FunctionID.GET_DATE_TIME, (), reply=("I I", (10100, 4)), result=GetDateTime(10100, 4)),
    Call("restart", FunctionID.RESTART, (DEVICE.RestartType.FACTORY_RESET,), sent=("B", (3,))),
    Call(
        "restart",
        FunctionID.RESTART,
        (DEVICE.RestartType.FACTORY_RESET, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "set_coordinates_callback_period",
        FunctionID.SET_COORDINATES_CALLBACK_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_coordinates_callback_period",
        FunctionID.SET_COORDINATES_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_coordinates_callback_period",
        FunctionID.GET_COORDINATES_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("set_status_callback_period", FunctionID.SET_STATUS_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_status_callback_period",
        FunctionID.SET_STATUS_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_status_callback_period",
        FunctionID.GET_STATUS_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_altitude_callback_period", FunctionID.SET_ALTITUDE_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))
    ),
    Call(
        "set_altitude_callback_period",
        FunctionID.SET_ALTITUDE_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_altitude_callback_period",
        FunctionID.GET_ALTITUDE_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("set_motion_callback_period", FunctionID.SET_MOTION_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_motion_callback_period",
        FunctionID.SET_MOTION_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_motion_callback_period",
        FunctionID.GET_MOTION_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_date_time_callback_period", FunctionID.SET_DATE_TIME_CALLBACK_PERIOD, (Decimal("0.003"),), sent=("I", (3,))
    ),
    Call(
        "set_date_time_callback_period",
        FunctionID.SET_DATE_TIME_CALLBACK_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_date_time_callback_period",
        FunctionID.GET_DATE_TIME_CALLBACK_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("restart", (12345,)),
    ("set_coordinates_callback_period", (Decimal("4294967.296"),)),
    ("set_status_callback_period", (Decimal("4294967.296"),)),
    ("set_altitude_callback_period", (Decimal("4294967.296"),)),
    ("set_motion_callback_period", (Decimal("4294967.296"),)),
    ("set_date_time_callback_period", (Decimal("4294967.296"),)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 222
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("GPS Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_coordinates(device, connection):
    """The callback COORDINATES is converted to an event."""
    connection.callback(CallbackID.COORDINATES, "I c I c H H H H", *(3, "a", 5, "a", 7, 8, 9, 10))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.COORDINATES,
            GetCoordinates(
                Decimal("0.000003"),
                "a",
                Decimal("0.000005"),
                "a",
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.09"),
                Decimal("0.1"),
            ),
        )
    ]


def test_callback_status(device, connection):
    """The callback STATUS is converted to an event."""
    connection.callback(CallbackID.STATUS, "B B B", *(3, 4, 5))
    assert summary(read_events(device)) == [(1, CallbackID.STATUS, GetStatus(DEVICE.Fix.FIX_3D_FIX, 4, 5))]


def test_callback_altitude(device, connection):
    """The callback ALTITUDE is converted to an event."""
    connection.callback(CallbackID.ALTITUDE, "i i", *(3, 4))
    assert summary(read_events(device)) == [(2, CallbackID.ALTITUDE, GetAltitude(Decimal("0.03"), Decimal("0.04")))]


def test_callback_motion(device, connection):
    """The callback MOTION is converted to an event."""
    connection.callback(CallbackID.MOTION, "I I", *(3, 4))
    assert summary(read_events(device)) == [
        (3, CallbackID.MOTION, GetMotion(Decimal("0.03"), Decimal("0.01111111111111111111111111111")))
    ]


def test_callback_date_time(device, connection):
    """The callback DATE_TIME is converted to an event."""
    connection.callback(CallbackID.DATE_TIME, "I I", *(10100, 4))
    assert summary(read_events(device)) == [(4, CallbackID.DATE_TIME, GetDateTime(10100, 4))]
