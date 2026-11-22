"""
Module for the Tinkerforge Outdoor Weather Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/OutdoorWeather_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

import asyncio
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .helper import check_range
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, LinearQuantity
from .streams import Chunk, read_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    STATION_DATA = 9
    SENSOR_DATA = 10


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_STATION_IDENTIFIERS_LOW_LEVEL = 1
    GET_SENSOR_IDENTIFIERS_LOW_LEVEL = 2
    GET_STATION_DATA = 3
    GET_SENSOR_DATA = 4
    SET_STATION_CALLBACK_CONFIGURATION = 5
    GET_STATION_CALLBACK_CONFIGURATION = 6
    SET_SENSOR_CALLBACK_CONFIGURATION = 7
    GET_SENSOR_CALLBACK_CONFIGURATION = 8


@unique
class WindDirection(Enum):
    """
    The wind direction options
    """

    N = 0
    NNE = 1
    NE = 2
    ENE = 3
    E = 4
    ESE = 5
    SE = 6
    SSE = 7
    S = 8
    SSW = 9
    SW = 10
    WSW = 11
    W = 12
    WNW = 13
    NW = 14
    NNW = 15
    ERROR = 255


class GetStationIdentifiers(NamedTuple):
    identifiers_length: int
    identifiers_chunk_offset: int
    identifiers_chunk_data: tuple[int, ...]


class GetSensorIdentifiers(NamedTuple):
    identifiers_length: int
    identifiers_chunk_offset: int
    identifiers_chunk_data: tuple[int, ...]


class GetStationData(NamedTuple):
    temperature: Decimal
    humidity: Decimal
    wind_speed: Decimal
    gust_speed: Decimal
    rain: Decimal
    wind_direction: WindDirection
    battery_low: bool
    last_change: Decimal


class GetSensorData(NamedTuple):
    temperature: Decimal
    humidity: Decimal
    last_change: Decimal


class StationDataEvent(NamedTuple):
    identifier: int
    temperature: Decimal
    humidity: Decimal
    wind_speed: Decimal
    gust_speed: Decimal
    rain: Decimal
    wind_direction: WindDirection
    battery_low: bool


class SensorDataEvent(NamedTuple):
    identifier: int
    temperature: Decimal
    humidity: Decimal


DECI_DEGREE_CELSIUS = LinearQuantity(1, 10, CELSIUS_ZERO)  # raw: 1/10 Degree Celsius, returned in K
DECI_METER_PER_SECOND = LinearQuantity(1, 10)  # raw: 1/10 Meter Per Second, returned in m/s
DECI_MILLIMETER = LinearQuantity(1, 10000)  # raw: 1/10 Millimeter, returned in m
PERCENT_RELATIVE_HUMIDITY = LinearQuantity(1)  # raw: 1/1 Percent Relative Humidity, returned in %RH
SECOND = LinearQuantity(1)  # raw: 1/1 Second, returned in s


class BrickletOutdoorWeather(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    433MHz receiver for outdoor weather station
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_OUTDOOR_WEATHER
    DEVICE_DISPLAY_NAME = "Outdoor Weather Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    WindDirection: TypeAlias = WindDirection

    CALLBACK_FORMATS = {
        CallbackID.STATION_DATA: "B h B I I I B !",
        CallbackID.SENSOR_DATA: "B h B",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.STATION_DATA,)),
        Channel(1, callbacks=(CallbackID.SENSOR_DATA,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()

    async def get_station_identifiers_low_level(self) -> GetStationIdentifiers:
        """
        Returns the identifiers (number between 0 and 255) of all `stations
        <https://www.tinkerforge.com/en/shop/accessories/sensors/outdoor-weather-station-ws-6147.html>`__
        that have been seen since the startup of the Bricklet.

        Each station gives itself a random identifier on first startup.

        Since firmware version 2.0.2 a station is removed from the list if no data was received for
        12 hours.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATION_IDENTIFIERS_LOW_LEVEL, response_expected=True
        )
        identifiers_length, identifiers_chunk_offset, identifiers_chunk_data = unpack_payload(payload, "H H 60B")
        return GetStationIdentifiers(identifiers_length, identifiers_chunk_offset, tuple(identifiers_chunk_data))

    async def get_station_identifiers(self) -> bytes:
        """
        Returns the identifiers (number between 0 and 255) of all `stations
        <https://www.tinkerforge.com/en/shop/accessories/sensors/outdoor-weather-station-ws-6147.html>`__
        that have been seen since the startup of the Bricklet.

        Each station gives itself a random identifier on first startup.

        Since firmware version 2.0.2 a station is removed from the list if no data was received for
        12 hours.

        This function transfers the complete identifiers stream and calls :func:`get_station_identifiers_low_level` as
        often as necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.get_station_identifiers_low_level()
            return Chunk(
                result.identifiers_length, result.identifiers_chunk_offset, result.identifiers_chunk_data, result
            )

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="identifiers", chunk_size=60)
        return bytes(data)

    async def get_sensor_identifiers_low_level(self) -> GetSensorIdentifiers:
        """
        Returns the identifiers (number between 0 and 255) of all `sensors
        <https://www.tinkerforge.com/en/shop/accessories/sensors/temperature-humidity-sensor-th-6148.html>`__
        that have been seen since the startup of the Bricklet.

        Each sensor gives itself a random identifier on first startup.

        Since firmware version 2.0.2 a sensor is removed from the list if no data was received for
        12 hours.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_IDENTIFIERS_LOW_LEVEL, response_expected=True
        )
        identifiers_length, identifiers_chunk_offset, identifiers_chunk_data = unpack_payload(payload, "H H 60B")
        return GetSensorIdentifiers(identifiers_length, identifiers_chunk_offset, tuple(identifiers_chunk_data))

    async def get_sensor_identifiers(self) -> bytes:
        """
        Returns the identifiers (number between 0 and 255) of all `sensors
        <https://www.tinkerforge.com/en/shop/accessories/sensors/temperature-humidity-sensor-th-6148.html>`__
        that have been seen since the startup of the Bricklet.

        Each sensor gives itself a random identifier on first startup.

        Since firmware version 2.0.2 a sensor is removed from the list if no data was received for
        12 hours.

        This function transfers the complete identifiers stream and calls :func:`get_sensor_identifiers_low_level` as
        often as necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.get_sensor_identifiers_low_level()
            return Chunk(
                result.identifiers_length, result.identifiers_chunk_offset, result.identifiers_chunk_data, result
            )

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="identifiers", chunk_size=60)
        return bytes(data)

    async def get_station_data(self, identifier: int) -> GetStationData:
        """
        Returns the last received data for a station with the given identifier.
        Call :func:`get_station_identifiers` for a list of all available identifiers.

        The return values are:

        * Temperature,
        * Humidity,
        * Wind Speed,
        * Gust Speed,
        * Rain Fall (accumulated since station power-up),
        * Wind Direction,
        * Battery Low (true if battery is low) and
        * Last Change (seconds since the reception of this data).

        Units: temperature in K (233.15 to 338.15 K), humidity in %RH (10 to 99 %RH), wind_speed in m/s, gust_speed in
        m/s, rain in m, last_change in s.
        """
        identifier = int(identifier)
        check_range("identifier", identifier, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_STATION_DATA,
            data=pack_payload((identifier,), "B"),
            response_expected=True,
        )
        temperature, humidity, wind_speed, gust_speed, rain, wind_direction, battery_low, last_change = unpack_payload(
            payload, "h B I I I B ! H"
        )
        return GetStationData(
            DECI_DEGREE_CELSIUS.to_si(temperature),
            PERCENT_RELATIVE_HUMIDITY.to_si(humidity),
            DECI_METER_PER_SECOND.to_si(wind_speed),
            DECI_METER_PER_SECOND.to_si(gust_speed),
            DECI_MILLIMETER.to_si(rain),
            WindDirection(wind_direction),
            battery_low,
            SECOND.to_si(last_change),
        )

    async def get_sensor_data(self, identifier: int) -> GetSensorData:
        """
        Returns the last measured data for a sensor with the given identifier.
        Call :func:`get_sensor_identifiers` for a list of all available identifiers.

        The return values are:

        * Temperature,
        * Humidity and
        * Last Change (seconds since the last reception of data).

        Units: temperature in K, humidity in %RH, last_change in s.
        """
        identifier = int(identifier)
        check_range("identifier", identifier, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SENSOR_DATA,
            data=pack_payload((identifier,), "B"),
            response_expected=True,
        )
        temperature, humidity, last_change = unpack_payload(payload, "h B H")
        return GetSensorData(
            DECI_DEGREE_CELSIUS.to_si(temperature), PERCENT_RELATIVE_HUMIDITY.to_si(humidity), SECOND.to_si(last_change)
        )

    async def set_station_callback_configuration(
        self, enable_callback: bool = False, response_expected: bool = True
    ) -> None:
        """
        Turns callback for station data on or off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STATION_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enable_callback),), "!"),
            response_expected=response_expected,
        )

    async def get_station_callback_configuration(self) -> bool:
        """
        Returns the configuration as set by :func:`set_station_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATION_CALLBACK_CONFIGURATION, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def set_sensor_callback_configuration(
        self, enable_callback: bool = False, response_expected: bool = True
    ) -> None:
        """
        Turns callback for sensor data on or off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSOR_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enable_callback),), "!"),
            response_expected=response_expected,
        )

    async def get_sensor_callback_configuration(self) -> bool:
        """
        Returns the configuration as set by :func:`set_sensor_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_CALLBACK_CONFIGURATION, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.STATION_DATA:
            identifier, temperature, humidity, wind_speed, gust_speed, rain, wind_direction, battery_low = value
            return 0, StationDataEvent(
                identifier,
                DECI_DEGREE_CELSIUS.to_si(temperature),
                PERCENT_RELATIVE_HUMIDITY.to_si(humidity),
                DECI_METER_PER_SECOND.to_si(wind_speed),
                DECI_METER_PER_SECOND.to_si(gust_speed),
                DECI_MILLIMETER.to_si(rain),
                WindDirection(wind_direction),
                battery_low,
            )
        identifier, temperature, humidity = value
        return 1, SensorDataEvent(
            identifier, DECI_DEGREE_CELSIUS.to_si(temperature), PERCENT_RELATIVE_HUMIDITY.to_si(humidity)
        )
