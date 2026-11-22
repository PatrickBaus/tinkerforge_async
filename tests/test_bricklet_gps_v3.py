"""Tests for the GPS Bricklet 3.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_gps_v3 import (
    BrickletGPSV3,
    GetAltitude,
    GetCoordinates,
    GetDateTime,
    GetMotion,
    GetSatelliteStatus,
    GetSatelliteSystemStatus,
    GetStatus,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletGPSV3
FunctionID = BrickletGPSV3.FunctionID
CallbackID = BrickletGPSV3.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_COORDINATES": 1,
    "GET_STATUS": 2,
    "GET_ALTITUDE": 3,
    "GET_MOTION": 4,
    "GET_DATE_TIME": 5,
    "RESTART": 6,
    "GET_SATELLITE_SYSTEM_STATUS_LOW_LEVEL": 7,
    "GET_SATELLITE_STATUS": 8,
    "SET_FIX_LED_CONFIG": 9,
    "GET_FIX_LED_CONFIG": 10,
    "SET_COORDINATES_CALLBACK_PERIOD": 11,
    "GET_COORDINATES_CALLBACK_PERIOD": 12,
    "SET_STATUS_CALLBACK_PERIOD": 13,
    "GET_STATUS_CALLBACK_PERIOD": 14,
    "SET_ALTITUDE_CALLBACK_PERIOD": 15,
    "GET_ALTITUDE_CALLBACK_PERIOD": 16,
    "SET_MOTION_CALLBACK_PERIOD": 17,
    "GET_MOTION_CALLBACK_PERIOD": 18,
    "SET_DATE_TIME_CALLBACK_PERIOD": 19,
    "GET_DATE_TIME_CALLBACK_PERIOD": 20,
    "SET_SBAS_CONFIG": 27,
    "GET_SBAS_CONFIG": 28,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "PULSE_PER_SECOND": 21,
    "COORDINATES": 22,
    "STATUS": 23,
    "ALTITUDE": 24,
    "MOTION": 25,
    "DATE_TIME": 26,
}

CALLS: list[Call] = [
    Call(
        "get_coordinates",
        FunctionID.GET_COORDINATES,
        (),
        reply=("I c I c", (3, "a", 5, "a")),
        result=GetCoordinates(Decimal("0.000003"), "a", Decimal("0.000005"), "a"),
    ),
    Call("get_status", FunctionID.GET_STATUS, (), reply=("! B", (True, 4)), result=GetStatus(True, 4)),
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
        "get_satellite_system_status_low_level",
        FunctionID.GET_SATELLITE_SYSTEM_STATUS_LOW_LEVEL,
        (DEVICE.SatelliteSystem.GALILEO,),
        sent=("B", (2,)),
        reply=("B 12B B H H H", (3, [i % 256 for i in range(12)], 3, 6, 7, 8)),
        result=GetSatelliteSystemStatus(
            3,
            tuple(i % 256 for i in range(12)),
            DEVICE.Fix.FIX_3D_FIX,
            Decimal("0.06"),
            Decimal("0.07"),
            Decimal("0.08"),
        ),
    ),
    Call(
        "get_satellite_status",
        FunctionID.GET_SATELLITE_STATUS,
        (DEVICE.SatelliteSystem.GALILEO, 3),
        sent=("B B", (2, 3)),
        reply=("h h h", (3, 4, 5)),
        result=GetSatelliteStatus(Decimal("3"), Decimal("4"), Decimal("5")),
    ),
    Call("set_fix_led_config", FunctionID.SET_FIX_LED_CONFIG, (DEVICE.FixLEDConfig.SHOW_PPS,), sent=("B", (4,))),
    Call(
        "set_fix_led_config",
        FunctionID.SET_FIX_LED_CONFIG,
        (DEVICE.FixLEDConfig.SHOW_PPS, False),
        sent=("B", (4,)),
        response_expected=False,
    ),
    Call(
        "get_fix_led_config", FunctionID.GET_FIX_LED_CONFIG, (), reply=("B", (4,)), result=DEVICE.FixLEDConfig.SHOW_PPS
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
    Call("set_sbas_config", FunctionID.SET_SBAS_CONFIG, (DEVICE.SBAS.DISABLED,), sent=("B", (1,))),
    Call(
        "set_sbas_config",
        FunctionID.SET_SBAS_CONFIG,
        (DEVICE.SBAS.DISABLED, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call("get_sbas_config", FunctionID.GET_SBAS_CONFIG, (), reply=("B", (1,)), result=DEVICE.SBAS.DISABLED),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("restart", (12345,)),
    ("get_satellite_system_status_low_level", (12345,)),
    ("get_satellite_status", (12345, 3)),
    ("get_satellite_status", (DEVICE.SatelliteSystem.GALILEO, 33)),
    ("set_fix_led_config", (12345,)),
    ("set_coordinates_callback_period", (Decimal("4294967.296"),)),
    ("set_status_callback_period", (Decimal("4294967.296"),)),
    ("set_altitude_callback_period", (Decimal("4294967.296"),)),
    ("set_motion_callback_period", (Decimal("4294967.296"),)),
    ("set_date_time_callback_period", (Decimal("4294967.296"),)),
    ("set_sbas_config", (12345,)),
]


def test_identity(device: BrickletGPSV3) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2171
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("GPS Bricklet 3.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_get_satellite_system_status_transfers_the_stream(device: BrickletGPSV3, connection: FakeConnection) -> None:
    """The high-level function get_satellite_system_status() uses get_satellite_system_status_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 12):
        connection.reply(
            FunctionID.GET_SATELLITE_SYSTEM_STATUS_LOW_LEVEL,
            "B 12B B H H H",
            *(3, chunk(data, offset, 12, 0), 3, 6, 7, 8),
        )
    result = run(device.get_satellite_system_status(*(DEVICE.SatelliteSystem.GALILEO,)))
    assert connection.requests == [request(FunctionID.GET_SATELLITE_SYSTEM_STATUS_LOW_LEVEL, "B", *(2,))] * 1
    assert result.satellite_numbers == bytes([i % 256 for i in range(3)])


def test_callback_pulse_per_second(device: BrickletGPSV3, connection: FakeConnection) -> None:
    """The callback PULSE_PER_SECOND is converted to an event."""
    connection.callback(CallbackID.PULSE_PER_SECOND)
    assert summary(read_events(device)) == [(0, CallbackID.PULSE_PER_SECOND, None)]


def test_callback_coordinates(device: BrickletGPSV3, connection: FakeConnection) -> None:
    """The callback COORDINATES is converted to an event."""
    connection.callback(CallbackID.COORDINATES, "I c I c", *(3, "a", 5, "a"))
    assert summary(read_events(device)) == [
        (1, CallbackID.COORDINATES, GetCoordinates(Decimal("0.000003"), "a", Decimal("0.000005"), "a"))
    ]


def test_callback_status(device: BrickletGPSV3, connection: FakeConnection) -> None:
    """The callback STATUS is converted to an event."""
    connection.callback(CallbackID.STATUS, "! B", *(True, 4))
    assert summary(read_events(device)) == [(2, CallbackID.STATUS, GetStatus(True, 4))]


def test_callback_altitude(device: BrickletGPSV3, connection: FakeConnection) -> None:
    """The callback ALTITUDE is converted to an event."""
    connection.callback(CallbackID.ALTITUDE, "i i", *(3, 4))
    assert summary(read_events(device)) == [(3, CallbackID.ALTITUDE, GetAltitude(Decimal("0.03"), Decimal("0.04")))]


def test_callback_motion(device: BrickletGPSV3, connection: FakeConnection) -> None:
    """The callback MOTION is converted to an event."""
    connection.callback(CallbackID.MOTION, "I I", *(3, 4))
    assert summary(read_events(device)) == [
        (4, CallbackID.MOTION, GetMotion(Decimal("0.03"), Decimal("0.01111111111111111111111111111")))
    ]


def test_callback_date_time(device: BrickletGPSV3, connection: FakeConnection) -> None:
    """The callback DATE_TIME is converted to an event."""
    connection.callback(CallbackID.DATE_TIME, "I I", *(10100, 4))
    assert summary(read_events(device)) == [(5, CallbackID.DATE_TIME, GetDateTime(10100, 4))]
