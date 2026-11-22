"""
Module for the Tinkerforge CO2 Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/CO2V2_Bricklet_Python.html) implemented using
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
from .quantities import CELSIUS_ZERO, TEMPERATURE, LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ALL_VALUES = 8
    CO2_CONCENTRATION = 12
    TEMPERATURE = 16
    HUMIDITY = 20


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ALL_VALUES = 1
    SET_AIR_PRESSURE = 2
    GET_AIR_PRESSURE = 3
    SET_TEMPERATURE_OFFSET = 4
    GET_TEMPERATURE_OFFSET = 5
    SET_ALL_VALUES_CALLBACK_CONFIGURATION = 6
    GET_ALL_VALUES_CALLBACK_CONFIGURATION = 7
    GET_CO2_CONCENTRATION = 9
    SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION = 10
    GET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION = 11
    GET_TEMPERATURE = 13
    SET_TEMPERATURE_CALLBACK_CONFIGURATION = 14
    GET_TEMPERATURE_CALLBACK_CONFIGURATION = 15
    GET_HUMIDITY = 17
    SET_HUMIDITY_CALLBACK_CONFIGURATION = 18
    GET_HUMIDITY_CALLBACK_CONFIGURATION = 19
    SET_AUTOMATIC_SELF_CALIBRATION = 21
    GET_AUTOMATIC_SELF_CALIBRATION = 22
    SET_FORCED_RECALIBRATION = 23
    GET_FORCED_RECALIBRATION = 24


class GetAllValues(NamedTuple):
    co2_concentration: Decimal
    temperature: Decimal
    humidity: Decimal


AIR_PRESSURE = LinearQuantity(100)  # raw: 1/1 Hectopascal, returned in Pa
CO2_CONCENTRATION = LinearQuantity(1)  # raw: 1/1 Parts Per Million, returned in ppm
HUMIDITY = LinearQuantity(1, 100)  # raw: 1/100 Percent Relative Humidity, returned in %RH
VALUE = LinearQuantity(1)  # raw: 1/1 Parts Per Million, returned in ppm


class BrickletCO2V2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures CO2 concentration, temperature and humidity
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_CO2_V2
    DEVICE_DISPLAY_NAME = "CO2 Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.ALL_VALUES: "H h H",
        CallbackID.CO2_CONCENTRATION: "H",
        CallbackID.TEMPERATURE: "h",
        CallbackID.HUMIDITY: "H",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.ALL_VALUES,),
            configuration=ChannelConfiguration("all_values", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            1,
            getter="get_co2_concentration",
            callbacks=(CallbackID.CO2_CONCENTRATION,),
            configuration=ChannelConfiguration("co2_concentration"),
        ),
        Channel(
            2,
            getter="get_temperature",
            callbacks=(CallbackID.TEMPERATURE,),
            configuration=ChannelConfiguration("temperature", default=CELSIUS_ZERO),
        ),
        Channel(
            3, getter="get_humidity", callbacks=(CallbackID.HUMIDITY,), configuration=ChannelConfiguration("humidity")
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> Any:
        """
        Returns the value of the channel with the secondary id `sid`. See `CHANNELS` for the channels.
        """
        return await self._get_value(sid)

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

    async def get_all_values(self) -> GetAllValues:
        """
        Returns all values measured by the CO2 Bricklet 2.0.

        If you want to get the values periodically, it is recommended to use the
        :attr:`CallbackID.ALL_VALUES` callback. You can set the callback configuration
        with :func:`set_all_values_callback_configuration`.

        .. note::
         The sensor is able to messure up to 393.15 K. However it is only specified up to 343.15 K.
         Exposing the Bricklet to higher temperatures might result in permanent damage.

        Units: co2_concentration in ppm (0 to 40000 ppm), temperature in K (233.15 to 393.15 K), humidity in %RH (0 to
        100 %RH).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_VALUES, response_expected=True
        )
        co2_concentration, temperature, humidity = unpack_payload(payload, "H h H")
        return GetAllValues(
            CO2_CONCENTRATION.to_si(co2_concentration), TEMPERATURE.to_si(temperature), HUMIDITY.to_si(humidity)
        )

    async def set_air_pressure(self, air_pressure: float | Decimal = 0, response_expected: bool = True) -> None:
        """
        The CO2 concentration depends (among other things) on the ambient air pressure.

        To increase the accuracy of the CO2 Bricklet 2.0 you can set the current air pressure.
        You use the ``Barometer Bricklet 2.0 <barometer_v2_bricklet>`` or the
        ``Air Quality Bricklet <air_quality_bricklet>`` to get the current air pressure.

        By default air pressure compensation is disabled. Once you set a value it
        will be used for compensation. You can turn the compensation off again by
        setting the value to 0.

        It is sufficient to update the value every few minutes.

        Units: air_pressure in Pa.
        """
        air_pressure_raw = AIR_PRESSURE.from_si(air_pressure)
        check_range("air_pressure", air_pressure_raw, 0, 65535, air_pressure)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AIR_PRESSURE,
            data=pack_payload((air_pressure_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_air_pressure(self) -> Decimal:
        """
        Returns the ambient air pressure as set by :func:`set_air_pressure`.

        Units: air_pressure in Pa.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AIR_PRESSURE, response_expected=True
        )
        return AIR_PRESSURE.to_si(unpack_payload(payload, "H"))

    async def set_temperature_offset(self, offset: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets a temperature offset. A offset of 10 will decrease
        the measured temperature by 0.1 K.

        If you install this Bricklet into an enclosure and you want to measure the ambient
        temperature, you may have to decrease the measured temperature by some value to
        compensate for the error because of the heating inside of the enclosure.

        We recommend that you leave the parts in the enclosure running for at least
        24 hours such that a temperature equilibrium can be reached. After that you can measure
        the temperature directly outside of enclosure and set the difference as offset.

        This temperature offset is used to calculate the relative humidity and
        CO2 concentration. In case the Bricklet is installed in an enclosure, we
        recommend to measure and set the temperature offset to improve the accuracy of
        the measurements.

        It is sufficient to set the temperature offset once. The offset is saved in
        non-volatile memory and is applied again after a power loss.

        Units: offset in K.
        """
        offset_raw = TEMPERATURE.from_si(offset)
        check_range("offset", offset_raw, 0, 65535, offset)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_OFFSET,
            data=pack_payload((offset_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_temperature_offset(self) -> Decimal:
        """
        Returns the temperature offset as set by
        :func:`set_temperature_offset`.

        Units: offset in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_OFFSET, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "H"))

    async def set_all_values_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ALL_VALUES`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after at least one of the values has changed. If the values didn't
        change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALL_VALUES_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_all_values_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_all_values_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_VALUES_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def get_co2_concentration(self) -> Decimal:
        """
        Returns CO2 concentration.

        Units: co2_concentration in ppm (0 to 40000 ppm).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CO2_CONCENTRATION, response_expected=True
        )
        return CO2_CONCENTRATION.to_si(unpack_payload(payload, "H"))

    async def set_co2_concentration_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.CO2_CONCENTRATION` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.CO2_CONCENTRATION`
        callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in ppm, maximum in ppm.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = VALUE.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = VALUE.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c H H"
            ),
            response_expected=response_expected,
        )

    async def get_co2_concentration_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_co2_concentration_callback_configuration`.

        Units: minimum in ppm, maximum in ppm.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), VALUE.to_si(minimum), VALUE.to_si(maximum)
        )

    async def get_temperature(self) -> Decimal:
        """
        Returns temperature.

        .. note::
         The sensor is able to messure up to 393.15 K. However it is only specified up to 343.15 K.
         Exposing the Bricklet to higher temperatures might result in permanent damage.

        Units: temperature in K (233.15 to 393.15 K).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "h"))

    async def set_temperature_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = Decimal("273.15"),
        maximum: float | Decimal = Decimal("273.15"),
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.TEMPERATURE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.TEMPERATURE` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in K, maximum in K.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = TEMPERATURE.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = TEMPERATURE.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c h h"
            ),
            response_expected=response_expected,
        )

    async def get_temperature_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_temperature_callback_configuration`.

        Units: minimum in K, maximum in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            TEMPERATURE.to_si(minimum),
            TEMPERATURE.to_si(maximum),
        )

    async def get_humidity(self) -> Decimal:
        """
        Returns relative humidity.

        Units: humidity in %RH (0 to 100 %RH).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HUMIDITY, response_expected=True
        )
        return HUMIDITY.to_si(unpack_payload(payload, "H"))

    async def set_humidity_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.HUMIDITY` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.HUMIDITY` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in %RH, maximum in %RH.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = HUMIDITY.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = HUMIDITY.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c H H"
            ),
            response_expected=response_expected,
        )

    async def get_humidity_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_humidity_callback_configuration`.

        Units: minimum in %RH, maximum in %RH.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HUMIDITY_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            HUMIDITY.to_si(minimum),
            HUMIDITY.to_si(maximum),
        )

    async def set_automatic_self_calibration(self, enabled: bool = True, response_expected: bool = True) -> None:
        """
        Enables/disables the automatic self-calibration (ASC) of the CO2 sensor.

        If ASC is enabled the sensor continuously recalibrates itself. For this to work
        the sensor has to be exposed to fresh air for at least one hour every day. The first
        time ASC is enabled, the sensor needs at least 7 days of uninterrupted operation to
        find its initial calibration parameters.

        If the Bricklet is used in an environment where it does not regularly see fresh
        air (for example in a living room or bedroom), ASC can result in wrong
        CO2 concentration measurements over time. In this case we recommend to disable ASC
        and to recalibrate the sensor with :func:`set_forced_recalibration` instead.

        Disabling ASC does not discard the calibration that was found so far. It stays in
        use until it is replaced by :func:`set_forced_recalibration` or by a new
        calibration found by ASC.

        The setting is saved in flash and applied again after a power loss.

        By default ASC is enabled. Before firmware version 2.0.4 ASC was always enabled
        and could not be disabled.

        .. versionadded:: 2.0.4 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AUTOMATIC_SELF_CALIBRATION,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_automatic_self_calibration(self) -> bool:
        """
        Returns the automatic self-calibration configuration as set by
        :func:`set_automatic_self_calibration`.

        .. versionadded:: 2.0.4 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AUTOMATIC_SELF_CALIBRATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_forced_recalibration(
        self, co2_concentration: float | Decimal, response_expected: bool = True
    ) -> None:
        """
        Recalibrates the CO2 sensor with a known reference CO2 concentration
        (forced recalibration, FRC).

        For best results, operate the Bricklet in a stable environment with a known
        CO2 concentration close to the sensor, for example next to a calibrated
        reference instrument.

        The sensor has to measure continuously for at least two minutes before the
        recalibration is applied. If this function is called within the first two
        minutes after the Bricklet was started, the recalibration is applied automatically
        as soon as the two minutes have passed.

        The recalibration is saved permanently in the sensor and stays in use after a
        power loss.

        A forced recalibration replaces the calibration found by the automatic
        self-calibration (ASC) and vice versa. If you want to use forced recalibration,
        we recommend to disable ASC with :func:`set_automatic_self_calibration` first.
        Otherwise the recalibration may later be overwritten by ASC.

        The reference CO2 concentration of the most recent recalibration can be read
        back with :func:`get_forced_recalibration`.

        Units: co2_concentration in ppm (400 to 2000 ppm).

        .. versionadded:: 2.0.4 (Firmware)
        """
        co2_concentration_raw = CO2_CONCENTRATION.from_si(co2_concentration)
        check_range("co2_concentration", co2_concentration_raw, 400, 2000, co2_concentration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FORCED_RECALIBRATION,
            data=pack_payload((co2_concentration_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_forced_recalibration(self) -> Decimal:
        """
        Returns the reference CO2 concentration of the most recent forced recalibration
        as reported by the CO2 sensor.

        The value is updated as soon as the recalibration set by
        :func:`set_forced_recalibration` has been applied (see the two minute
        waiting period described there).

        The sensor only keeps this value in volatile memory. After a power loss
        400 ppm (the default reference value of the sensor) is returned, even though
        the recalibration itself is saved permanently in the sensor and stays in use.

        Units: co2_concentration in ppm (400 to 2000 ppm).

        .. versionadded:: 2.0.4 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FORCED_RECALIBRATION, response_expected=True
        )
        return CO2_CONCENTRATION.to_si(unpack_payload(payload, "H"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.ALL_VALUES:
            co2_concentration, temperature, humidity = value
            return 0, GetAllValues(
                CO2_CONCENTRATION.to_si(co2_concentration), TEMPERATURE.to_si(temperature), HUMIDITY.to_si(humidity)
            )
        if callback_id is CallbackID.CO2_CONCENTRATION:
            return 1, CO2_CONCENTRATION.to_si(value)
        if callback_id is CallbackID.TEMPERATURE:
            return 2, TEMPERATURE.to_si(value)
        return 3, HUMIDITY.to_si(value)
