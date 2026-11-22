"""
Module for the Tinkerforge GPS Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/GPS_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    COORDINATES = 17
    STATUS = 18
    ALTITUDE = 19
    MOTION = 20
    DATE_TIME = 21


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_COORDINATES = 1
    GET_STATUS = 2
    GET_ALTITUDE = 3
    GET_MOTION = 4
    GET_DATE_TIME = 5
    RESTART = 6
    SET_COORDINATES_CALLBACK_PERIOD = 7
    GET_COORDINATES_CALLBACK_PERIOD = 8
    SET_STATUS_CALLBACK_PERIOD = 9
    GET_STATUS_CALLBACK_PERIOD = 10
    SET_ALTITUDE_CALLBACK_PERIOD = 11
    GET_ALTITUDE_CALLBACK_PERIOD = 12
    SET_MOTION_CALLBACK_PERIOD = 13
    GET_MOTION_CALLBACK_PERIOD = 14
    SET_DATE_TIME_CALLBACK_PERIOD = 15
    GET_DATE_TIME_CALLBACK_PERIOD = 16


@unique
class Fix(Enum):
    """
    The fix options
    """

    NO_FIX = 1
    FIX_2D_FIX = 2
    FIX_3D_FIX = 3


@unique
class RestartType(Enum):
    """
    The restart type options
    """

    HOT_START = 0
    WARM_START = 1
    COLD_START = 2
    FACTORY_RESET = 3


class GetCoordinates(NamedTuple):
    latitude: Decimal
    ns: str
    longitude: Decimal
    ew: str
    pdop: Decimal
    hdop: Decimal
    vdop: Decimal
    epe: Decimal


class GetStatus(NamedTuple):
    fix: Fix
    satellites_view: int
    satellites_used: int


class GetAltitude(NamedTuple):
    altitude: Decimal
    geoidal_separation: Decimal


class GetMotion(NamedTuple):
    course: Decimal
    speed: Decimal


class GetDateTime(NamedTuple):
    date: int
    time: int


CENTI_DEGREE = LinearQuantity(1, 100)  # raw: 1/100 Degree, returned in °
CENTI_KILOMETER_PER_HOUR = LinearQuantity(1, 360)  # raw: 1/100 Kilometer Per Hour, returned in m/s
CENTI_METER = LinearQuantity(1, 100)  # raw: 1/100 Meter, returned in m
MICRO_DEGREE = LinearQuantity(1, 1000000)  # raw: 1/1000000 Degree, returned in °
RATIO_1_100 = LinearQuantity(1, 100)  # raw: 1/100, dimensionless


class BrickletGPS(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Determine position, velocity and altitude using GPS
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_GPS
    DEVICE_DISPLAY_NAME = "GPS Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Fix: TypeAlias = Fix
    RestartType: TypeAlias = RestartType

    CALLBACK_FORMATS = {
        CallbackID.COORDINATES: "I c I c H H H H",
        CallbackID.STATUS: "B B B",
        CallbackID.ALTITUDE: "i i",
        CallbackID.MOTION: "I I",
        CallbackID.DATE_TIME: "I I",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.COORDINATES,)),
        Channel(1, callbacks=(CallbackID.STATUS,)),
        Channel(2, callbacks=(CallbackID.ALTITUDE,)),
        Channel(3, callbacks=(CallbackID.MOTION,)),
        Channel(4, callbacks=(CallbackID.DATE_TIME,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_coordinates(self) -> GetCoordinates:
        """
        Returns the GPS coordinates. Latitude and longitude are given in the
        ``DD.dddddd°`` format, the value 57123468 means 57.123468°.
        The parameter ``ns`` and ``ew`` are the cardinal directions for
        latitude and longitude. Possible values for ``ns`` and ``ew`` are 'N', 'S', 'E'
        and 'W' (north, south, east and west).

        PDOP, HDOP and VDOP are the dilution of precision (DOP) values. They specify
        the additional multiplicative effect of GPS satellite geometry on GPS
        precision. See
        `here <https://en.wikipedia.org/wiki/Dilution_of_precision_(GPS)>`__
        for more information.

        EPE is the "Estimated Position Error". This is not the
        absolute maximum error, it is the error with a specific confidence. See
        `here <https://www.nps.gov/gis/gps/WhatisEPE.html>`__ for more information.

        This data is only valid if there is currently a fix as indicated by
        :func:`get_status`.

        Units: latitude in ° (0 to 90 °), longitude in ° (0 to 180 °), epe in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COORDINATES, response_expected=True
        )
        latitude, ns, longitude, ew, pdop, hdop, vdop, epe = unpack_payload(payload, "I c I c H H H H")
        return GetCoordinates(
            MICRO_DEGREE.to_si(latitude),
            ns,
            MICRO_DEGREE.to_si(longitude),
            ew,
            RATIO_1_100.to_si(pdop),
            RATIO_1_100.to_si(hdop),
            RATIO_1_100.to_si(vdop),
            CENTI_METER.to_si(epe),
        )

    async def get_status(self) -> GetStatus:
        """
        Returns the current fix status, the number of satellites that are in view and
        the number of satellites that are currently used.

        Possible fix status values can be:

        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 100

         "1", "No Fix, :func:`get_coordinates`, :func:`get_altitude` and :func:`get_motion` return invalid data"
         "2", "2D Fix, only :func:`get_coordinates` and :func:`get_motion` return valid data"
         "3", "3D Fix, :func:`get_coordinates`, :func:`get_altitude` and :func:`get_motion` return valid data"

        There is also a ``blue LED <gps_bricklet_fix_led>`` on the Bricklet that
        indicates the fix status.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATUS, response_expected=True
        )
        fix, satellites_view, satellites_used = unpack_payload(payload, "B B B")
        return GetStatus(Fix(fix), satellites_view, satellites_used)

    async def get_altitude(self) -> GetAltitude:
        """
        Returns the current altitude and corresponding geoidal separation.

        This data is only valid if there is currently a fix as indicated by
        :func:`get_status`.

        Units: altitude in m, geoidal_separation in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALTITUDE, response_expected=True
        )
        altitude, geoidal_separation = unpack_payload(payload, "i i")
        return GetAltitude(CENTI_METER.to_si(altitude), CENTI_METER.to_si(geoidal_separation))

    async def get_motion(self) -> GetMotion:
        """
        Returns the current course and speed. A course of 0° means the Bricklet is
        traveling north bound and 90° means it is traveling east bound.

        Please note that this only returns useful values if an actual movement
        is present.

        This data is only valid if there is currently a fix as indicated by
        :func:`get_status`.

        Units: course in ° (0 to 360 °), speed in m/s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOTION, response_expected=True
        )
        course, speed = unpack_payload(payload, "I I")
        return GetMotion(CENTI_DEGREE.to_si(course), CENTI_KILOMETER_PER_HOUR.to_si(speed))

    async def get_date_time(self) -> GetDateTime:
        """
        Returns the current date and time. The date is
        given in the format ``ddmmyy`` and the time is given
        in the format ``hhmmss.sss``. For example, 140713 means
        14.07.13 as date and 195923568 means 19:59:23.568 as time.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DATE_TIME, response_expected=True
        )
        date, time = unpack_payload(payload, "I I")
        return GetDateTime(date, time)

    async def restart(self, restart_type: RestartType | int, response_expected: bool = True) -> None:
        """
        Restarts the GPS Bricklet, the following restart types are available:

        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 100

         "0", "Hot start (use all available data in the NV store)"
         "1", "Warm start (don't use ephemeris at restart)"
         "2", "Cold start (don't use time, position, almanacs and ephemeris at restart)"
         "3", "Factory reset (clear all system/user configurations at restart)"
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.RESTART,
            data=pack_payload((RestartType(restart_type).value,), "B"),
            response_expected=response_expected,
        )

    async def set_coordinates_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.COORDINATES` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.COORDINATES` callback is only triggered if the coordinates changed
        since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COORDINATES_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_coordinates_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_coordinates_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COORDINATES_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_status_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.STATUS` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.STATUS` callback is only triggered if the status changed since the
        last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STATUS_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_status_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_status_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATUS_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_altitude_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ALTITUDE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.ALTITUDE` callback is only triggered if the altitude changed since
        the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALTITUDE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_altitude_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_altitude_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALTITUDE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_motion_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.MOTION` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.MOTION` callback is only triggered if the motion changed since the
        last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOTION_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_motion_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_motion_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOTION_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_date_time_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.DATE_TIME` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.DATE_TIME` callback is only triggered if the date or time changed
        since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DATE_TIME_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_date_time_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_date_time_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DATE_TIME_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    @override
    def _convert_callback(  # pylint: disable=too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.COORDINATES:
            latitude, ns, longitude, ew, pdop, hdop, vdop, epe = value
            return 0, GetCoordinates(
                MICRO_DEGREE.to_si(latitude),
                ns,
                MICRO_DEGREE.to_si(longitude),
                ew,
                RATIO_1_100.to_si(pdop),
                RATIO_1_100.to_si(hdop),
                RATIO_1_100.to_si(vdop),
                CENTI_METER.to_si(epe),
            )
        if callback_id is CallbackID.STATUS:
            fix, satellites_view, satellites_used = value
            return 1, GetStatus(Fix(fix), satellites_view, satellites_used)
        if callback_id is CallbackID.ALTITUDE:
            altitude, geoidal_separation = value
            return 2, GetAltitude(CENTI_METER.to_si(altitude), CENTI_METER.to_si(geoidal_separation))
        if callback_id is CallbackID.MOTION:
            course, speed = value
            return 3, GetMotion(CENTI_DEGREE.to_si(course), CENTI_KILOMETER_PER_HOUR.to_si(speed))
        date, time = value
        return 4, GetDateTime(date, time)
