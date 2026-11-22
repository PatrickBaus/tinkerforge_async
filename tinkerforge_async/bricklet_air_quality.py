"""
Module for the Tinkerforge Air Quality Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/AirQuality_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

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

    ALL_VALUES = 6
    IAQ_INDEX = 10
    TEMPERATURE = 14
    HUMIDITY = 18
    AIR_PRESSURE = 22


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ALL_VALUES = 1
    SET_TEMPERATURE_OFFSET = 2
    GET_TEMPERATURE_OFFSET = 3
    SET_ALL_VALUES_CALLBACK_CONFIGURATION = 4
    GET_ALL_VALUES_CALLBACK_CONFIGURATION = 5
    GET_IAQ_INDEX = 7
    SET_IAQ_INDEX_CALLBACK_CONFIGURATION = 8
    GET_IAQ_INDEX_CALLBACK_CONFIGURATION = 9
    GET_TEMPERATURE = 11
    SET_TEMPERATURE_CALLBACK_CONFIGURATION = 12
    GET_TEMPERATURE_CALLBACK_CONFIGURATION = 13
    GET_HUMIDITY = 15
    SET_HUMIDITY_CALLBACK_CONFIGURATION = 16
    GET_HUMIDITY_CALLBACK_CONFIGURATION = 17
    GET_AIR_PRESSURE = 19
    SET_AIR_PRESSURE_CALLBACK_CONFIGURATION = 20
    GET_AIR_PRESSURE_CALLBACK_CONFIGURATION = 21
    REMOVE_CALIBRATION = 23
    SET_BACKGROUND_CALIBRATION_DURATION = 24
    GET_BACKGROUND_CALIBRATION_DURATION = 25


@unique
class Accuracy(Enum):
    """
    The accuracy options
    """

    UNRELIABLE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@unique
class BackgroundCalibrationDuration(Enum):
    """
    The duration options
    """

    DURATION_4_DAYS = 0
    DURATION_28_DAYS = 1


class GetAllValues(NamedTuple):
    iaq_index: int
    iaq_index_accuracy: Accuracy
    temperature: Decimal
    humidity: Decimal
    air_pressure: Decimal


class GetIAQIndex(NamedTuple):
    iaq_index: int
    iaq_index_accuracy: Accuracy


CENTI_DEGREE_CELSIUS_DIFFERENCE = LinearQuantity(1, 100)  # raw: 1/100 Degree Celsius, returned in K
CENTI_HECTOPASCAL = LinearQuantity(1)  # raw: 1/100 Hectopascal, returned in Pa
CENTI_PERCENT_RELATIVE_HUMIDITY = LinearQuantity(1, 100)  # raw: 1/100 Percent Relative Humidity, returned in %RH


class BrickletAirQuality(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures IAQ index, temperature, humidity and air pressure
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_AIR_QUALITY
    DEVICE_DISPLAY_NAME = "Air Quality Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Accuracy: TypeAlias = Accuracy
    BackgroundCalibrationDuration: TypeAlias = BackgroundCalibrationDuration

    CALLBACK_FORMATS = {
        CallbackID.ALL_VALUES: "i B i i i",
        CallbackID.IAQ_INDEX: "i B",
        CallbackID.TEMPERATURE: "i",
        CallbackID.HUMIDITY: "i",
        CallbackID.AIR_PRESSURE: "i",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.ALL_VALUES,),
            configuration=ChannelConfiguration("all_values", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            1,
            callbacks=(CallbackID.IAQ_INDEX,),
            configuration=ChannelConfiguration("iaq_index", thresholds=False, wrap_advanced=True),
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
        Channel(
            4,
            getter="get_air_pressure",
            callbacks=(CallbackID.AIR_PRESSURE,),
            configuration=ChannelConfiguration("air_pressure"),
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

    @override
    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
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

    @override
    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_all_values(self) -> GetAllValues:
        """
        Returns all values measured by the Air Quality Bricklet. The values are
        IAQ (Indoor Air Quality) Index (higher value means greater level of air pollution), IAQ Index Accuracy,
        Temperature, Humidity and
        Air Pressure.

        .. image:: /Images/Misc/bricklet_air_quality_iaq_index.png
           :scale: 100 %
           :alt: Air Quality Index description
           :align: center
           :target: ../../_images/Misc/bricklet_air_quality_iaq_index.png

        Units: temperature in K, humidity in %RH, air_pressure in Pa.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_VALUES, response_expected=True
        )
        iaq_index, iaq_index_accuracy, temperature, humidity, air_pressure = unpack_payload(payload, "i B i i i")
        return GetAllValues(
            iaq_index,
            Accuracy(iaq_index_accuracy),
            TEMPERATURE.to_si(temperature),
            CENTI_PERCENT_RELATIVE_HUMIDITY.to_si(humidity),
            CENTI_HECTOPASCAL.to_si(air_pressure),
        )

    async def set_temperature_offset(self, offset: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets a temperature offset. A offset of 10 will decrease the measured temperature by 0.1 K.

        If you install this Bricklet into an enclosure and you want to measure the ambient
        temperature, you may have to decrease the measured temperature by some value to
        compensate for the error because of the heating inside of the enclosure.

        We recommend that you leave the parts in the enclosure running for at least
        24 hours such that a temperature equilibrium can be reached. After that you can measure
        the temperature directly outside of enclosure and set the difference as offset.

        This temperature offset is used to calculate the relative humidity and
        IAQ index measurements. In case the Bricklet is installed in an enclosure, we
        recommend to measure and set the temperature offset to improve the accuracy of
        the measurements.

        Units: offset in K.
        """
        offset_raw = CENTI_DEGREE_CELSIUS_DIFFERENCE.from_si(offset)
        check_range("offset", offset_raw, -2147483648, 2147483647, offset)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_OFFSET,
            data=pack_payload((offset_raw,), "i"),
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
        return CENTI_DEGREE_CELSIUS_DIFFERENCE.to_si(unpack_payload(payload, "i"))

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

    async def get_iaq_index(self) -> GetIAQIndex:
        """
        Returns the IAQ index and accuracy. The higher the IAQ index, the greater the level of air pollution.

        .. image:: /Images/Misc/bricklet_air_quality_iaq_index.png
           :scale: 100 %
           :alt: IAQ index description
           :align: center
           :target: ../../_images/Misc/bricklet_air_quality_iaq_index.png

        If you want to get the value periodically, it is recommended to use the
        :attr:`CallbackID.IAQ_INDEX` callback. You can set the callback configuration
        with :func:`set_iaq_index_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_IAQ_INDEX, response_expected=True
        )
        iaq_index, iaq_index_accuracy = unpack_payload(payload, "i B")
        return GetIAQIndex(iaq_index, Accuracy(iaq_index_accuracy))

    async def set_iaq_index_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.IAQ_INDEX`
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
            function_id=FunctionID.SET_IAQ_INDEX_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_iaq_index_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_iaq_index_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_IAQ_INDEX_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def get_temperature(self) -> Decimal:
        """
        Returns temperature.

        Units: temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "i"))

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
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = TEMPERATURE.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
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
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
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

        Units: humidity in %RH.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HUMIDITY, response_expected=True
        )
        return CENTI_PERCENT_RELATIVE_HUMIDITY.to_si(unpack_payload(payload, "i"))

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
        minimum_raw = CENTI_PERCENT_RELATIVE_HUMIDITY.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = CENTI_PERCENT_RELATIVE_HUMIDITY.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
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
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            CENTI_PERCENT_RELATIVE_HUMIDITY.to_si(minimum),
            CENTI_PERCENT_RELATIVE_HUMIDITY.to_si(maximum),
        )

    async def get_air_pressure(self) -> Decimal:
        """
        Returns air pressure.

        Units: air_pressure in Pa.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AIR_PRESSURE, response_expected=True
        )
        return CENTI_HECTOPASCAL.to_si(unpack_payload(payload, "i"))

    async def set_air_pressure_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.AIR_PRESSURE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.AIR_PRESSURE` callback.

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

        Units: minimum in Pa, maximum in Pa.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = CENTI_HECTOPASCAL.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = CENTI_HECTOPASCAL.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
            ),
            response_expected=response_expected,
        )

    async def get_air_pressure_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_air_pressure_callback_configuration`.

        Units: minimum in Pa, maximum in Pa.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AIR_PRESSURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            CENTI_HECTOPASCAL.to_si(minimum),
            CENTI_HECTOPASCAL.to_si(maximum),
        )

    async def remove_calibration(self, response_expected: bool = True) -> None:
        """
        Deletes the calibration from flash. After you call this function,
        you need to power cycle the Air Quality Bricklet.

        On the next power up the Bricklet will start a new calibration, as
        if it was started for the very first time.

        The calibration is based on the data of the last four days, so it takes
        four days until a full calibration is re-established.

        .. versionadded:: 2.0.3 (Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.REMOVE_CALIBRATION, response_expected=response_expected
        )

    async def set_background_calibration_duration(
        self,
        duration: BackgroundCalibrationDuration | int = BackgroundCalibrationDuration.DURATION_28_DAYS,
        response_expected: bool = True,
    ) -> None:
        """
        The Air Quality Bricklet uses an automatic background calibration mechanism to
        calculate the IAQ Index. This calibration mechanism considers a history of
        measured data. The duration of this history can be configured to either be
        4 days or 28 days.

        If you keep the Bricklet mostly at one place and it does not get moved around
        to different environments, we recommend that you use a duration of 28 days.

        If you change the duration, the current calibration will be discarded and
        the calibration will start from beginning again. The configuration of the
        duration is saved in flash, so you should only have to call this function
        once in the lifetime of the Bricklet.

        The Bricklet has to be power cycled after this function is called
        for a duration change to take effect.

        Before firmware version 2.0.3 this was not configurable and the duration was
        4 days.

        The default value (since firmware version 2.0.3) is 28 days.

        .. versionadded:: 2.0.3 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BACKGROUND_CALIBRATION_DURATION,
            data=pack_payload((BackgroundCalibrationDuration(duration).value,), "B"),
            response_expected=response_expected,
        )

    async def get_background_calibration_duration(self) -> BackgroundCalibrationDuration:
        """
        Returns the background calibration duration as set by
        :func:`set_background_calibration_duration`.

        .. versionadded:: 2.0.3 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BACKGROUND_CALIBRATION_DURATION, response_expected=True
        )
        return BackgroundCalibrationDuration(unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.ALL_VALUES:
            iaq_index, iaq_index_accuracy, temperature, humidity, air_pressure = value
            return 0, GetAllValues(
                iaq_index,
                Accuracy(iaq_index_accuracy),
                TEMPERATURE.to_si(temperature),
                CENTI_PERCENT_RELATIVE_HUMIDITY.to_si(humidity),
                CENTI_HECTOPASCAL.to_si(air_pressure),
            )
        if callback_id is CallbackID.IAQ_INDEX:
            iaq_index, iaq_index_accuracy = value
            return 1, GetIAQIndex(iaq_index, Accuracy(iaq_index_accuracy))
        if callback_id is CallbackID.TEMPERATURE:
            return 2, TEMPERATURE.to_si(value)
        if callback_id is CallbackID.HUMIDITY:
            return 3, CENTI_PERCENT_RELATIVE_HUMIDITY.to_si(value)
        return 4, CENTI_HECTOPASCAL.to_si(value)
