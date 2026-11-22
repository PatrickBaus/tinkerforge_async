"""
Module for the Tinkerforge Particulate Matter Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/ParticulateMatter_Bricklet_Python.html) implemented using
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

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    SimpleCallbackConfiguration,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
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

    PM_CONCENTRATION = 10
    PM_COUNT = 11


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_PM_CONCENTRATION = 1
    GET_PM_COUNT = 2
    SET_ENABLE = 3
    GET_ENABLE = 4
    GET_SENSOR_INFO = 5
    SET_PM_CONCENTRATION_CALLBACK_CONFIGURATION = 6
    GET_PM_CONCENTRATION_CALLBACK_CONFIGURATION = 7
    SET_PM_COUNT_CALLBACK_CONFIGURATION = 8
    GET_PM_COUNT_CALLBACK_CONFIGURATION = 9


class GetPMConcentration(NamedTuple):
    pm10: Decimal
    pm25: Decimal
    pm100: Decimal


class GetPMCount(NamedTuple):
    greater03um: Decimal
    greater05um: Decimal
    greater10um: Decimal
    greater25um: Decimal
    greater50um: Decimal
    greater100um: Decimal


class GetSensorInfo(NamedTuple):
    sensor_version: int
    last_error_code: int
    framing_error_count: int
    checksum_error_count: int


GREATER03UM = LinearQuantity(10000)  # raw: 10000/1 Particles Per Cubic Meter, returned in 1/m³
GREATER05UM = LinearQuantity(10000)  # raw: 10000/1 Particles Per Cubic Meter, returned in 1/m³
GREATER100UM = LinearQuantity(10000)  # raw: 10000/1 Particles Per Cubic Meter, returned in 1/m³
GREATER10UM = LinearQuantity(10000)  # raw: 10000/1 Particles Per Cubic Meter, returned in 1/m³
GREATER25UM = LinearQuantity(10000)  # raw: 10000/1 Particles Per Cubic Meter, returned in 1/m³
GREATER50UM = LinearQuantity(10000)  # raw: 10000/1 Particles Per Cubic Meter, returned in 1/m³
PM10 = LinearQuantity(1, 1000000000)  # raw: 1/1000000 Gram Per Cubic Meter, returned in kg/m³
PM100 = LinearQuantity(1, 1000000000)  # raw: 1/1000000 Gram Per Cubic Meter, returned in kg/m³
PM25 = LinearQuantity(1, 1000000000)  # raw: 1/1000000 Gram Per Cubic Meter, returned in kg/m³


class BrickletParticulateMatter(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures Particulate Matter concentration (PM1.0, PM2.5 and PM10)
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_PARTICULATE_MATTER
    DEVICE_DISPLAY_NAME = "Particulate Matter Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.PM_CONCENTRATION: "H H H",
        CallbackID.PM_COUNT: "H H H H H H",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.PM_CONCENTRATION,),
            configuration=ChannelConfiguration("pm_concentration", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            1,
            callbacks=(CallbackID.PM_COUNT,),
            configuration=ChannelConfiguration("pm_count", thresholds=False, wrap_advanced=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the callbacks of the channel with the secondary id `sid`. The thresholds are ignored by
        channels without thresholds.
        """
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return await self._get_callback_configuration(sid)

    async def get_pm_concentration(self) -> GetPMConcentration:
        r"""
        Returns the particulate matter concentration, broken down as:

        * PM\ ``1.0``\ ,
        * PM\ ``2.5``\  and
        * PM\ ``10.0``\ .

        If the sensor is disabled (see :func:`set_enable`) then the last known good
        values from the sensor are returned.

        If you want to get the values periodically, it is recommended to use the
        :attr:`CallbackID.PM_CONCENTRATION` callback. You can set the callback configuration
        with :func:`set_pm_concentration_callback_configuration`.

        Units: pm10 in kg/m³, pm25 in kg/m³, pm100 in kg/m³.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_PM_CONCENTRATION, response_expected=True
        )
        pm10, pm25, pm100 = unpack_payload(payload, "H H H")
        return GetPMConcentration(PM10.to_si(pm10), PM25.to_si(pm25), PM100.to_si(pm100))

    async def get_pm_count(self) -> GetPMCount:
        """
        Returns the number of particulates in 100 ml of air, broken down by their
        diameter:

        * greater 0.3µm,
        * greater 0.5µm,
        * greater 1.0µm,
        * greater 2.5µm,
        * greater 5.0µm and
        * greater 10.0µm.

        If the sensor is disabled (see :func:`set_enable`) then the last known good
        value from the sensor is returned.

        If you want to get the values periodically, it is recommended to use the
        :attr:`CallbackID.PM_COUNT` callback. You can set the callback configuration
        with :func:`set_pm_count_callback_configuration`.

        Units: greater03um in 1/m³, greater05um in 1/m³, greater10um in 1/m³, greater25um in 1/m³, greater50um in 1/m³,
        greater100um in 1/m³.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_PM_COUNT, response_expected=True
        )
        greater03um, greater05um, greater10um, greater25um, greater50um, greater100um = unpack_payload(
            payload, "H H H H H H"
        )
        return GetPMCount(
            GREATER03UM.to_si(greater03um),
            GREATER05UM.to_si(greater05um),
            GREATER10UM.to_si(greater10um),
            GREATER25UM.to_si(greater25um),
            GREATER50UM.to_si(greater50um),
            GREATER100UM.to_si(greater100um),
        )

    async def set_enable(self, enable: bool = True, response_expected: bool = True) -> None:
        """
        Enables/Disables the fan and the laser diode of the sensors.

        The sensor takes about 30 seconds after it is enabled to settle and produce stable
        values.

        The laser diode has a lifetime of about 8000 hours. If you want to measure in
        an interval with a long idle time (e.g. hourly) you should turn the
        laser diode off between the measurements.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ENABLE,
            data=pack_payload((bool(enable),), "!"),
            response_expected=response_expected,
        )

    async def get_enable(self) -> bool:
        """
        Returns the state of the sensor as set by :func:`set_enable`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ENABLE, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def get_sensor_info(self) -> GetSensorInfo:
        """
        Returns information about the sensor:

        * the sensor version number,
        * the last error code reported by the sensor (0 means no error) and
        * the number of framing and checksum errors that occurred in the communication
          with the sensor.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_INFO, response_expected=True
        )
        sensor_version, last_error_code, framing_error_count, checksum_error_count = unpack_payload(payload, "B B B B")
        return GetSensorInfo(sensor_version, last_error_code, framing_error_count, checksum_error_count)

    async def set_pm_concentration_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.PM_CONCENTRATION`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PM_CONCENTRATION_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_pm_concentration_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_pm_concentration_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_PM_CONCENTRATION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_pm_count_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.PM_COUNT` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PM_COUNT_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_pm_count_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_pm_count_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_PM_COUNT_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.PM_CONCENTRATION:
            pm10, pm25, pm100 = value
            return 0, GetPMConcentration(PM10.to_si(pm10), PM25.to_si(pm25), PM100.to_si(pm100))
        greater03um, greater05um, greater10um, greater25um, greater50um, greater100um = value
        return 1, GetPMCount(
            GREATER03UM.to_si(greater03um),
            GREATER05UM.to_si(greater05um),
            GREATER10UM.to_si(greater10um),
            GREATER25UM.to_si(greater25um),
            GREATER50UM.to_si(greater50um),
            GREATER100UM.to_si(greater100um),
        )
