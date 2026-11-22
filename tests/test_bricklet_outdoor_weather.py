"""Tests for the Outdoor Weather Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_outdoor_weather import (
    BrickletOutdoorWeather,
    GetSensorData,
    GetSensorIdentifiers,
    GetStationData,
    GetStationIdentifiers,
    SensorDataEvent,
    StationDataEvent,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletOutdoorWeather
FunctionID = BrickletOutdoorWeather.FunctionID
CallbackID = BrickletOutdoorWeather.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_STATION_IDENTIFIERS_LOW_LEVEL": 1,
    "GET_SENSOR_IDENTIFIERS_LOW_LEVEL": 2,
    "GET_STATION_DATA": 3,
    "GET_SENSOR_DATA": 4,
    "SET_STATION_CALLBACK_CONFIGURATION": 5,
    "GET_STATION_CALLBACK_CONFIGURATION": 6,
    "SET_SENSOR_CALLBACK_CONFIGURATION": 7,
    "GET_SENSOR_CALLBACK_CONFIGURATION": 8,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"STATION_DATA": 9, "SENSOR_DATA": 10}

CALLS: list[Call] = [
    Call(
        "get_station_identifiers_low_level",
        FunctionID.GET_STATION_IDENTIFIERS_LOW_LEVEL,
        (),
        reply=("H H 60B", (3, 4, [i % 256 for i in range(60)])),
        result=GetStationIdentifiers(3, 4, tuple(i % 256 for i in range(60))),
    ),
    Call(
        "get_sensor_identifiers_low_level",
        FunctionID.GET_SENSOR_IDENTIFIERS_LOW_LEVEL,
        (),
        reply=("H H 60B", (3, 4, [i % 256 for i in range(60)])),
        result=GetSensorIdentifiers(3, 4, tuple(i % 256 for i in range(60))),
    ),
    Call(
        "get_station_data",
        FunctionID.GET_STATION_DATA,
        (3,),
        sent=("B", (3,)),
        reply=("h B I I I B ! H", (3, 10, 5, 6, 7, 255, True, 10)),
        result=GetStationData(
            Decimal("273.45"),
            Decimal("10"),
            Decimal("0.5"),
            Decimal("0.6"),
            Decimal("0.0007"),
            DEVICE.WindDirection.ERROR,
            True,
            Decimal("10"),
        ),
    ),
    Call(
        "get_sensor_data",
        FunctionID.GET_SENSOR_DATA,
        (3,),
        sent=("B", (3,)),
        reply=("h B H", (3, 4, 5)),
        result=GetSensorData(Decimal("273.45"), Decimal("4"), Decimal("5")),
    ),
    Call(
        "set_station_callback_configuration",
        FunctionID.SET_STATION_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_station_callback_configuration",
        FunctionID.SET_STATION_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_station_callback_configuration",
        FunctionID.GET_STATION_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "set_sensor_callback_configuration", FunctionID.SET_SENSOR_CALLBACK_CONFIGURATION, (True,), sent=("!", (True,))
    ),
    Call(
        "set_sensor_callback_configuration",
        FunctionID.SET_SENSOR_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_sensor_callback_configuration",
        FunctionID.GET_SENSOR_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("get_station_data", (256,)),
    ("get_sensor_data", (256,)),
]


def test_identity(device: BrickletOutdoorWeather) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 288
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Outdoor Weather Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_get_station_identifiers_transfers_the_stream(
    device: BrickletOutdoorWeather, connection: FakeConnection
) -> None:
    """The high-level function get_station_identifiers() uses get_station_identifiers_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 60):
        connection.reply(
            FunctionID.GET_STATION_IDENTIFIERS_LOW_LEVEL, "H H 60B", *(3, offset, chunk(data, offset, 60, 0))
        )
    result = run(device.get_station_identifiers())
    assert connection.requests == [request(FunctionID.GET_STATION_IDENTIFIERS_LOW_LEVEL)] * 1
    assert result == bytes([i % 256 for i in range(3)])


def test_get_sensor_identifiers_transfers_the_stream(
    device: BrickletOutdoorWeather, connection: FakeConnection
) -> None:
    """The high-level function get_sensor_identifiers() uses get_sensor_identifiers_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 60):
        connection.reply(
            FunctionID.GET_SENSOR_IDENTIFIERS_LOW_LEVEL, "H H 60B", *(3, offset, chunk(data, offset, 60, 0))
        )
    result = run(device.get_sensor_identifiers())
    assert connection.requests == [request(FunctionID.GET_SENSOR_IDENTIFIERS_LOW_LEVEL)] * 1
    assert result == bytes([i % 256 for i in range(3)])


def test_callback_station_data(device: BrickletOutdoorWeather, connection: FakeConnection) -> None:
    """The callback STATION_DATA is converted to an event."""
    connection.callback(CallbackID.STATION_DATA, "B h B I I I B !", *(3, 4, 10, 6, 7, 8, 255, True))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.STATION_DATA,
            StationDataEvent(
                3,
                Decimal("273.55"),
                Decimal("10"),
                Decimal("0.6"),
                Decimal("0.7"),
                Decimal("0.0008"),
                DEVICE.WindDirection.ERROR,
                True,
            ),
        )
    ]


def test_callback_sensor_data(device: BrickletOutdoorWeather, connection: FakeConnection) -> None:
    """The callback SENSOR_DATA is converted to an event."""
    connection.callback(CallbackID.SENSOR_DATA, "B h B", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (1, CallbackID.SENSOR_DATA, SensorDataEvent(3, Decimal("273.55"), Decimal("5")))
    ]
