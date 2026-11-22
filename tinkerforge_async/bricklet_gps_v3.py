"""
Module for the Tinkerforge GPS Bricklet 3.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/GPSV3_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
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

    PULSE_PER_SECOND = 21
    COORDINATES = 22
    STATUS = 23
    ALTITUDE = 24
    MOTION = 25
    DATE_TIME = 26


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
    GET_SATELLITE_SYSTEM_STATUS_LOW_LEVEL = 7
    GET_SATELLITE_STATUS = 8
    SET_FIX_LED_CONFIG = 9
    GET_FIX_LED_CONFIG = 10
    SET_COORDINATES_CALLBACK_PERIOD = 11
    GET_COORDINATES_CALLBACK_PERIOD = 12
    SET_STATUS_CALLBACK_PERIOD = 13
    GET_STATUS_CALLBACK_PERIOD = 14
    SET_ALTITUDE_CALLBACK_PERIOD = 15
    GET_ALTITUDE_CALLBACK_PERIOD = 16
    SET_MOTION_CALLBACK_PERIOD = 17
    GET_MOTION_CALLBACK_PERIOD = 18
    SET_DATE_TIME_CALLBACK_PERIOD = 19
    GET_DATE_TIME_CALLBACK_PERIOD = 20
    SET_SBAS_CONFIG = 27
    GET_SBAS_CONFIG = 28


@unique
class RestartType(Enum):
    """
    The restart type options
    """

    HOT_START = 0
    WARM_START = 1
    COLD_START = 2
    FACTORY_RESET = 3


@unique
class SatelliteSystem(Enum):
    """
    The satellite system options
    """

    GPS = 0
    GLONASS = 1
    GALILEO = 2


@unique
class Fix(Enum):
    """
    The fix options
    """

    NO_FIX = 1
    FIX_2D_FIX = 2
    FIX_3D_FIX = 3


@unique
class FixLEDConfig(Enum):
    """
    The fix led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_FIX = 3
    SHOW_PPS = 4


@unique
class SBAS(Enum):
    """
    The sbas options
    """

    ENABLED = 0
    DISABLED = 1


class GetCoordinates(NamedTuple):
    latitude: Decimal
    ns: str
    longitude: Decimal
    ew: str


class GetStatus(NamedTuple):
    has_fix: bool
    satellites_view: int


class GetAltitude(NamedTuple):
    altitude: Decimal
    geoidal_separation: Decimal


class GetMotion(NamedTuple):
    course: Decimal
    speed: Decimal


class GetDateTime(NamedTuple):
    date: int
    time: int


class GetSatelliteSystemStatus(NamedTuple):
    satellite_numbers_length: int
    satellite_numbers_data: tuple[int, ...]
    fix: Fix
    pdop: Decimal
    hdop: Decimal
    vdop: Decimal


class GetSatelliteSystemStatusResult(NamedTuple):
    fix: Fix
    pdop: Decimal
    hdop: Decimal
    vdop: Decimal
    satellite_numbers: bytes


class GetSatelliteStatus(NamedTuple):
    elevation: Decimal
    azimuth: Decimal
    snr: Decimal


CENTI_DEGREE = LinearQuantity(1, 100)  # raw: 1/100 Degree, returned in °
CENTI_KILOMETER_PER_HOUR = LinearQuantity(1, 360)  # raw: 1/100 Kilometer Per Hour, returned in m/s
CENTI_METER = LinearQuantity(1, 100)  # raw: 1/100 Meter, returned in m
DECIBEL = LinearQuantity(1)  # raw: 1/1 Decibel, returned in dB
DEGREE = LinearQuantity(1)  # raw: 1/1 Degree, returned in °
MICRO_DEGREE = LinearQuantity(1, 1000000)  # raw: 1/1000000 Degree, returned in °
RATIO_1_100 = LinearQuantity(1, 100)  # raw: 1/100, dimensionless


class BrickletGPSV3(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Determine position, velocity and altitude using GPS
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_GPS_V3
    DEVICE_DISPLAY_NAME = "GPS Bricklet 3.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    RestartType: TypeAlias = RestartType
    SatelliteSystem: TypeAlias = SatelliteSystem
    Fix: TypeAlias = Fix
    FixLEDConfig: TypeAlias = FixLEDConfig
    SBAS: TypeAlias = SBAS

    CALLBACK_FORMATS = {
        CallbackID.PULSE_PER_SECOND: "",
        CallbackID.COORDINATES: "I c I c",
        CallbackID.STATUS: "! B",
        CallbackID.ALTITUDE: "i i",
        CallbackID.MOTION: "I I",
        CallbackID.DATE_TIME: "I I",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.PULSE_PER_SECOND,)),
        Channel(1, callbacks=(CallbackID.COORDINATES,)),
        Channel(2, callbacks=(CallbackID.STATUS,)),
        Channel(3, callbacks=(CallbackID.ALTITUDE,)),
        Channel(4, callbacks=(CallbackID.MOTION,)),
        Channel(5, callbacks=(CallbackID.DATE_TIME,)),
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

    async def get_coordinates(self) -> GetCoordinates:
        """
        Returns the GPS coordinates. Latitude and longitude are given in the
        ``DD.dddddd°`` format, the value 57123468 means 57.123468°.
        The parameter ``ns`` and ``ew`` are the cardinal directions for
        latitude and longitude. Possible values for ``ns`` and ``ew`` are 'N', 'S', 'E'
        and 'W' (north, south, east and west).

        This data is only valid if there is currently a fix as indicated by
        :func:`get_status`.

        Units: latitude in ° (0 to 90 °), longitude in ° (0 to 180 °).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COORDINATES, response_expected=True
        )
        latitude, ns, longitude, ew = unpack_payload(payload, "I c I c")
        return GetCoordinates(MICRO_DEGREE.to_si(latitude), ns, MICRO_DEGREE.to_si(longitude), ew)

    async def get_status(self) -> GetStatus:
        """
        Returns if a fix is currently available as well as the number of
        satellites that are in view.

        There is also a ``green LED <gps_v2_bricklet_fix_led>`` on the Bricklet that
        indicates the fix status.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATUS, response_expected=True
        )
        has_fix, satellites_view = unpack_payload(payload, "! B")
        return GetStatus(has_fix, satellites_view)

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

    async def get_satellite_system_status_low_level(
        self, satellite_system: SatelliteSystem | int
    ) -> GetSatelliteSystemStatus:
        """
        Returns the

        * satellite numbers list (up to 12 items)
        * fix value,
        * PDOP value,
        * HDOP value and
        * VDOP value

        for a given satellite system. Currently GPS, GLONASS and Galileo are supported.

        The GPS and GLONASS satellites have unique numbers and the satellite list gives
        the numbers of the satellites that are currently utilized. The number 0 is not
        a valid satellite number and can be ignored in the list.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SATELLITE_SYSTEM_STATUS_LOW_LEVEL,
            data=pack_payload((SatelliteSystem(satellite_system).value,), "B"),
            response_expected=True,
        )
        satellite_numbers_length, satellite_numbers_data, fix, pdop, hdop, vdop = unpack_payload(
            payload, "B 12B B H H H"
        )
        return GetSatelliteSystemStatus(
            satellite_numbers_length,
            tuple(satellite_numbers_data),
            Fix(fix),
            RATIO_1_100.to_si(pdop),
            RATIO_1_100.to_si(hdop),
            RATIO_1_100.to_si(vdop),
        )

    async def get_satellite_system_status(
        self, satellite_system: SatelliteSystem | int
    ) -> GetSatelliteSystemStatusResult:
        """
        Returns the

        * satellite numbers list (up to 12 items)
        * fix value,
        * PDOP value,
        * HDOP value and
        * VDOP value

        for a given satellite system. Currently GPS, GLONASS and Galileo are supported.

        The GPS and GLONASS satellites have unique numbers and the satellite list gives
        the numbers of the satellites that are currently utilized. The number 0 is not
        a valid satellite number and can be ignored in the list.

        This function transfers the complete satellite_numbers stream and calls
        :func:`get_satellite_system_status_low_level` as often as necessary. Concurrent transfers of the stream are
        serialized.
        """
        result = await self.get_satellite_system_status_low_level(satellite_system)
        return GetSatelliteSystemStatusResult(
            result.fix,
            result.pdop,
            result.hdop,
            result.vdop,
            bytes(result.satellite_numbers_data[: result.satellite_numbers_length]),
        )

    async def get_satellite_status(
        self, satellite_system: SatelliteSystem | int, satellite_number: int
    ) -> GetSatelliteStatus:
        """
        Returns the current elevation, azimuth and SNR for a given satellite and satellite system.

        The available satellite numbers are:

        * GPS: 1-32
        * GLONASS: 65-96
        * Galileo: 301-332

        Units: elevation in ° (0 to 90 °), azimuth in ° (0 to 359 °), snr in dB (0 to 99 dB).
        """
        satellite_number = int(satellite_number)
        check_range("satellite_number", satellite_number, 1, 32)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SATELLITE_STATUS,
            data=pack_payload((SatelliteSystem(satellite_system).value, satellite_number), "B B"),
            response_expected=True,
        )
        elevation, azimuth, snr = unpack_payload(payload, "h h h")
        return GetSatelliteStatus(DEGREE.to_si(elevation), DEGREE.to_si(azimuth), DECIBEL.to_si(snr))

    async def set_fix_led_config(
        self, config: FixLEDConfig | int = FixLEDConfig.SHOW_FIX, response_expected: bool = True
    ) -> None:
        """
        Sets the fix LED configuration. By default the LED shows if
        the Bricklet got a GPS fix yet. If a fix is established the LED turns on.
        If there is no fix then the LED is turned off.

        You can also turn the LED permanently on/off, show a heartbeat or let it blink
        in sync with the PPS (pulse per second) output of the GPS module.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FIX_LED_CONFIG,
            data=pack_payload((FixLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_fix_led_config(self) -> FixLEDConfig:
        """
        Returns the configuration as set by :func:`set_fix_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FIX_LED_CONFIG, response_expected=True
        )
        return FixLEDConfig(unpack_payload(payload, "B"))

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

        The :attr:`CallbackID.ALTITUDE` callback is only triggered if the altitude changed since the
        last triggering.
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

    async def set_sbas_config(self, sbas_config: SBAS | int = SBAS.ENABLED, response_expected: bool = True) -> None:
        """
        If `SBAS <https://en.wikipedia.org/wiki/GNSS_augmentation#Satellite-based_augmentation_system>`__ is enabled,
        the position accuracy increases (if SBAS satellites are in view),
        but the update rate is limited to 5Hz. With SBAS disabled the update rate is increased to 10Hz.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SBAS_CONFIG,
            data=pack_payload((SBAS(sbas_config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_sbas_config(self) -> SBAS:
        """
        Returns the SBAS configuration as set by :func:`set_sbas_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SBAS_CONFIG, response_expected=True
        )
        return SBAS(unpack_payload(payload, "B"))

    def _convert_callback(  # pylint: disable=too-many-return-statements,too-many-branches,too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.PULSE_PER_SECOND:
            return 0, None
        if callback_id is CallbackID.COORDINATES:
            latitude, ns, longitude, ew = value
            return 1, GetCoordinates(MICRO_DEGREE.to_si(latitude), ns, MICRO_DEGREE.to_si(longitude), ew)
        if callback_id is CallbackID.STATUS:
            has_fix, satellites_view = value
            return 2, GetStatus(has_fix, satellites_view)
        if callback_id is CallbackID.ALTITUDE:
            altitude, geoidal_separation = value
            return 3, GetAltitude(CENTI_METER.to_si(altitude), CENTI_METER.to_si(geoidal_separation))
        if callback_id is CallbackID.MOTION:
            course, speed = value
            return 4, GetMotion(CENTI_DEGREE.to_si(course), CENTI_KILOMETER_PER_HOUR.to_si(speed))
        date, time = value
        return 5, GetDateTime(date, time)
