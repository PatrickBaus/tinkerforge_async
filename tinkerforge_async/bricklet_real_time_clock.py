"""
Module for the Tinkerforge Real-Time Clock Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RealTimeClock_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

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

    DATE_TIME = 10
    ALARM = 11


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_DATE_TIME = 1
    GET_DATE_TIME = 2
    GET_TIMESTAMP = 3
    SET_OFFSET = 4
    GET_OFFSET = 5
    SET_DATE_TIME_CALLBACK_PERIOD = 6
    GET_DATE_TIME_CALLBACK_PERIOD = 7
    SET_ALARM = 8
    GET_ALARM = 9


@unique
class Weekday(Enum):
    """
    The weekday options
    """

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


@unique
class AlarmMatch(Enum):
    """
    The alarm match options
    """

    DISABLED = -1


@unique
class AlarmInterval(Enum):
    """
    The alarm interval options
    """

    DISABLED = -1


class GetDateTime(NamedTuple):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    centisecond: int
    weekday: Weekday


class GetAlarm(NamedTuple):
    month: AlarmMatch
    day: AlarmMatch
    hour: AlarmMatch
    minute: AlarmMatch
    second: AlarmMatch
    weekday: AlarmMatch
    interval: AlarmInterval


class DateTimeEvent(NamedTuple):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    centisecond: int
    weekday: Weekday
    timestamp: Decimal


class AlarmEvent(NamedTuple):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    centisecond: int
    weekday: Weekday
    timestamp: Decimal


PARTS_PER_MILLION_217_100 = LinearQuantity(217, 100)  # raw: 217/100 Parts Per Million, returned in ppm


class BrickletRealTimeClock(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Battery-backed real-time clock
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_REAL_TIME_CLOCK
    DEVICE_DISPLAY_NAME = "Real-Time Clock Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Weekday: TypeAlias = Weekday
    AlarmMatch: TypeAlias = AlarmMatch
    AlarmInterval: TypeAlias = AlarmInterval

    CALLBACK_FORMATS = {
        CallbackID.DATE_TIME: "H B B B B B B B q",
        CallbackID.ALARM: "H B B B B B B B q",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.DATE_TIME,)),
        Channel(1, callbacks=(CallbackID.ALARM,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def set_date_time(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        centisecond: int,
        weekday: Weekday | int,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the current date (including weekday) and the current time.

        If the backup battery is installed then the real-time clock keeps date and
        time even if the Bricklet is not powered by a Brick.

        The real-time clock handles leap year and inserts the 29th of February
        accordingly. But leap seconds, time zones and daylight saving time are not
        handled.
        """
        year = int(year)
        check_range("year", year, 2000, 2099)
        month = int(month)
        check_range("month", month, 1, 12)
        day = int(day)
        check_range("day", day, 1, 31)
        hour = int(hour)
        check_range("hour", hour, 0, 23)
        minute = int(minute)
        check_range("minute", minute, 0, 59)
        second = int(second)
        check_range("second", second, 0, 59)
        centisecond = int(centisecond)
        check_range("centisecond", centisecond, 0, 99)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DATE_TIME,
            data=pack_payload(
                (year, month, day, hour, minute, second, centisecond, Weekday(weekday).value), "H B B B B B B B"
            ),
            response_expected=response_expected,
        )

    async def get_date_time(self) -> GetDateTime:
        """
        Returns the current date (including weekday) and the current time of the
        real-time clock.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DATE_TIME, response_expected=True
        )
        year, month, day, hour, minute, second, centisecond, weekday = unpack_payload(payload, "H B B B B B B B")
        return GetDateTime(year, month, day, hour, minute, second, centisecond, Weekday(weekday))

    async def get_timestamp(self) -> Decimal:
        """
        Returns the current date and the time of the real-time clock.
        The timestamp has an effective resolution of hundredths of a
        second and is an offset to 2000-01-01 00:00:00.000.

        Units: timestamp in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TIMESTAMP, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "q"))

    async def set_offset(self, offset: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets the offset the real-time clock should compensate for in 2.17 ppm steps
        between -277.76 ppm (-128) and +275.59 ppm (127).

        The real-time clock time can deviate from the actual time due to the frequency
        deviation of its 32.768 kHz crystal. Even without compensation (factory
        default) the resulting time deviation should be at most ±20 ppm (±52.6
        seconds per month).

        This deviation can be calculated by comparing the same duration measured by the
        real-time clock (``rtc_duration``) an accurate reference clock
        (``ref_duration``).

        For best results the configured offset should be set to 0 ppm first and then a
        duration of at least 6 hours should be measured.

        The new offset (``new_offset``) can be calculated from the currently configured
        offset (``current_offset``) and the measured durations as follow::

          new_offset = current_offset - round(1000000 * (rtc_duration - ref_duration) / rtc_duration / 2.17)

        If you want to calculate the offset, then we recommend using the calibration
        dialog in Brick Viewer, instead of doing it manually.

        The offset is saved in the EEPROM of the Bricklet and only needs to be
        configured once.

        Units: offset in ppm.
        """
        offset_raw = PARTS_PER_MILLION_217_100.from_si(offset)
        check_range("offset", offset_raw, -128, 127, offset)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_OFFSET,
            data=pack_payload((offset_raw,), "b"),
            response_expected=response_expected,
        )

    async def get_offset(self) -> Decimal:
        """
        Returns the offset as set by :func:`set_offset`.

        Units: offset in ppm.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OFFSET, response_expected=True
        )
        return PARTS_PER_MILLION_217_100.to_si(unpack_payload(payload, "b"))

    async def set_date_time_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.DATE_TIME` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.DATE_TIME` Callback is only triggered if the date or time changed
        since the last triggering.

        .. versionadded:: 2.0.1 (Firmware)
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

        .. versionadded:: 2.0.1 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DATE_TIME_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_alarm(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        month: AlarmMatch | int,
        day: AlarmMatch | int,
        hour: AlarmMatch | int,
        minute: AlarmMatch | int,
        second: AlarmMatch | int,
        weekday: AlarmMatch | int,
        interval: AlarmInterval | int,
        response_expected: bool = True,
    ) -> None:
        """
        Configures a repeatable alarm. The :attr:`CallbackID.ALARM` callback is triggered if the
        current date and time matches the configured alarm.

        Setting a parameter to -1 means that it should be disabled and doesn't take part
        in the match. Setting all parameters to -1 disables the alarm completely.

        For example, to make the alarm trigger every day at 7:30 AM it can be
        configured as (-1, -1, 7, 30, -1, -1, -1). The hour is set to match 7 and the
        minute is set to match 30. The alarm is triggered if all enabled parameters
        match.

        The interval has a special role. It allows to make the alarm reconfigure itself.
        This is useful if you need a repeated alarm that cannot be expressed by matching
        the current date and time. For example, to make the alarm trigger every 23
        seconds it can be configured as (-1, -1, -1, -1, -1, -1, 23). Internally the
        Bricklet will take the current date and time, add 23 seconds to it and set the
        result as its alarm. The first alarm will be triggered 23 seconds after the
        call. Because the interval is not -1, the Bricklet will do the same again
        internally, take the current date and time, add 23 seconds to it and set that
        as its alarm. This results in a repeated alarm that triggers every 23 seconds.

        The interval can also be used in combination with the other parameters. For
        example, configuring the alarm as (-1, -1, 7, 30, -1, -1, 300) results in an
        alarm that triggers every day at 7:30 AM and is then repeated every 5 minutes.

        .. versionadded:: 2.0.1 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALARM,
            data=pack_payload(
                (
                    AlarmMatch(month).value,
                    AlarmMatch(day).value,
                    AlarmMatch(hour).value,
                    AlarmMatch(minute).value,
                    AlarmMatch(second).value,
                    AlarmMatch(weekday).value,
                    AlarmInterval(interval).value,
                ),
                "b b b b b b i",
            ),
            response_expected=response_expected,
        )

    async def get_alarm(self) -> GetAlarm:
        """
        Returns the alarm configuration as set by :func:`set_alarm`.

        .. versionadded:: 2.0.1 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALARM, response_expected=True
        )
        month, day, hour, minute, second, weekday, interval = unpack_payload(payload, "b b b b b b i")
        return GetAlarm(
            AlarmMatch(month),
            AlarmMatch(day),
            AlarmMatch(hour),
            AlarmMatch(minute),
            AlarmMatch(second),
            AlarmMatch(weekday),
            AlarmInterval(interval),
        )

    def _convert_callback(  # pylint: disable=too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.DATE_TIME:
            year, month, day, hour, minute, second, centisecond, weekday, timestamp = value
            return 0, DateTimeEvent(
                year, month, day, hour, minute, second, centisecond, Weekday(weekday), ms_to_seconds(timestamp)
            )
        year, month, day, hour, minute, second, centisecond, weekday, timestamp = value
        return 1, AlarmEvent(
            year, month, day, hour, minute, second, centisecond, Weekday(weekday), ms_to_seconds(timestamp)
        )
