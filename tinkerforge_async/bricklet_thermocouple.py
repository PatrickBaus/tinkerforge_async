"""
Module for the Tinkerforge Thermocouple Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/Thermocouple_Bricklet_Python.html) implemented using
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

from .devices import (
    AdvancedCallbackConfiguration,
    BasicCallbackConfiguration,
    Channel,
    ChannelConfiguration,
    Device,
    DeviceIdentifier,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, TEMPERATURE

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    TEMPERATURE = 8
    TEMPERATURE_REACHED = 9
    ERROR_STATE = 13


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_TEMPERATURE = 1
    SET_TEMPERATURE_CALLBACK_PERIOD = 2
    GET_TEMPERATURE_CALLBACK_PERIOD = 3
    SET_TEMPERATURE_CALLBACK_THRESHOLD = 4
    GET_TEMPERATURE_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_CONFIGURATION = 10
    GET_CONFIGURATION = 11
    GET_ERROR_STATE = 12


@unique
class Averaging(Enum):
    """
    The averaging options
    """

    AVERAGING_1 = 1
    AVERAGING_2 = 2
    AVERAGING_4 = 4
    AVERAGING_8 = 8
    AVERAGING_16 = 16


@unique
class SensorType(Enum):
    """
    The type options
    """

    TYPE_B = 0
    TYPE_E = 1
    TYPE_J = 2
    TYPE_K = 3
    TYPE_N = 4
    TYPE_R = 5
    TYPE_S = 6
    TYPE_T = 7
    TYPE_G8 = 8
    TYPE_G32 = 9


@unique
class FilterOption(Enum):
    """
    The filter option options
    """

    FILTER_OPTION_50HZ = 0
    FILTER_OPTION_60HZ = 1


class GetConfiguration(NamedTuple):
    averaging: Averaging
    thermocouple_type: SensorType
    filter_: FilterOption


class GetErrorState(NamedTuple):
    over_under: bool
    open_circuit: bool


# The raw value of the types G8 and G32 is gain * 1.6 * 2^17 * Vin
G8_GAIN = 8 * Decimal("1.6") * 2**17
G32_GAIN = 32 * Decimal("1.6") * 2**17


class BrickletThermocouple(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures temperature with thermocouples
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_THERMOCOUPLE
    DEVICE_DISPLAY_NAME = "Thermocouple Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Averaging: TypeAlias = Averaging
    SensorType: TypeAlias = SensorType
    FilterOption: TypeAlias = FilterOption

    CALLBACK_FORMATS = {
        CallbackID.TEMPERATURE: "i",
        CallbackID.TEMPERATURE_REACHED: "i",
        CallbackID.ERROR_STATE: "! !",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_temperature",
            callbacks=(
                CallbackID.TEMPERATURE,
                CallbackID.TEMPERATURE_REACHED,
            ),
            configuration=ChannelConfiguration("temperature", split=True, default=CELSIUS_ZERO),
        ),
        Channel(1, callbacks=(CallbackID.ERROR_STATE,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync, sensor_type: SensorType = SensorType.TYPE_K) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        self.__sensor_type = SensorType(sensor_type)

    @property
    def sensor_type(self) -> SensorType:
        """
        Returns the thermocouple type, that is used to convert the values. It is set by :func:`set_configuration` and
        updated by :func:`get_configuration`.
        """
        return self.__sensor_type

    @sensor_type.setter
    def sensor_type(self, value: SensorType | int) -> None:
        self.__sensor_type = SensorType(value)

    def __value_to_si(self, value: int) -> Decimal:
        """
        Convert a raw value to K, or to the input voltage in V for the thermocouple types G8 and G32.
        """
        if self.__sensor_type is SensorType.TYPE_G8:
            return Decimal(value) / G8_GAIN
        if self.__sensor_type is SensorType.TYPE_G32:
            return Decimal(value) / G32_GAIN
        return TEMPERATURE.to_si(value)

    def __si_to_value(self, value: float | Decimal) -> int:
        if self.__sensor_type is SensorType.TYPE_G8:
            return round(Decimal(str(value)) * G8_GAIN)
        if self.__sensor_type is SensorType.TYPE_G32:
            return round(Decimal(str(value)) * G32_GAIN)
        return TEMPERATURE.from_si(value)

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

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return await self._get_callback_configuration(sid)

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the thermocouple.

        If you want to get the temperature periodically, it is recommended
        to use the :attr:`CallbackID.TEMPERATURE` callback and set the period with
        :func:`set_temperature_callback_period`.

        Units: temperature in K (V for the types G8 and G32) (63.15 to 2073.15 K).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return self.__value_to_si(unpack_payload(payload, "i"))

    async def set_temperature_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.TEMPERATURE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.TEMPERATURE` callback is only triggered if the temperature has changed
        since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_temperature_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_temperature_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_temperature_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = Decimal("273.15"),
        maximum: float | Decimal = Decimal("273.15"),
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.TEMPERATURE_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

        Units: minimum in K, maximum in K (V for the types G8 and G32).
        """
        minimum_raw = self.__si_to_value(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = self.__si_to_value(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c i i"),
            response_expected=response_expected,
        )

    async def get_temperature_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_temperature_callback_threshold`.

        Units: minimum in K, maximum in K (V for the types G8 and G32).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        return BasicCallbackConfiguration(Threshold(option), self.__value_to_si(minimum), self.__value_to_si(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callback

        * :attr:`CallbackID.TEMPERATURE_REACHED`

        is triggered, if the threshold

        * :func:`set_temperature_callback_threshold`

        keeps being reached.

        Units: debounce in s.
        """
        debounce_raw = seconds_to_ms(debounce)
        check_range("debounce", debounce_raw, 0, 4294967295, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((debounce_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> Decimal:
        """
        Returns the debounce period as set by :func:`set_debounce_period`.

        Units: debounce in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_configuration(
        self,
        averaging: Averaging | int = Averaging.AVERAGING_16,
        thermocouple_type: SensorType | int = SensorType.TYPE_K,
        filter_: FilterOption | int = FilterOption.FILTER_OPTION_50HZ,
        response_expected: bool = True,
    ) -> None:
        """
        You can configure averaging size, thermocouple type and frequency
        filtering.

        Available averaging sizes are 1, 2, 4, 8 and 16 samples.

        As thermocouple type you can use B, E, J, K, N, R, S and T. If you have a
        different thermocouple or a custom thermocouple you can also use
        G8 and G32. With these types the returned value will not be in K, but the thermocouple input voltage in V.
        The Bricklet calculates the raw value by the following formulas, the library converts it back to Vin:

        * G8: ``value = 8 * 1.6 * 2^17 * Vin``
        * G32: ``value = 32 * 1.6 * 2^17 * Vin``

        where Vin is the thermocouple input voltage.

        The frequency filter can be either configured to 50Hz or to 60Hz. You should
        configure it according to your utility frequency.

        The conversion time depends on the averaging and filter configuration, it can
        be calculated as follows:

        * 60Hz: ``time = 82 + (samples - 1) * 16.67``
        * 50Hz: ``time = 98 + (samples - 1) * 20``
        """
        self.__sensor_type = SensorType(thermocouple_type)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload(
                (Averaging(averaging).value, SensorType(thermocouple_type).value, FilterOption(filter_).value), "B B B"
            ),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        averaging, thermocouple_type, filter_ = unpack_payload(payload, "B B B")
        self.__sensor_type = SensorType(thermocouple_type)
        return GetConfiguration(Averaging(averaging), self.__sensor_type, FilterOption(filter_))

    async def get_error_state(self) -> GetErrorState:
        """
        Returns the current error state. There are two possible errors:

        * Over/Under Voltage and
        * Open Circuit.

        Over/Under Voltage happens for voltages below 0V or above 3.3V. In this case
        it is very likely that your thermocouple is defective. An Open Circuit error
        indicates that there is no thermocouple connected.

        You can use the :attr:`CallbackID.ERROR_STATE` callback to automatically get triggered
        when the error state changes.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_STATE, response_expected=True
        )
        over_under, open_circuit = unpack_payload(payload, "! !")
        return GetErrorState(over_under, open_circuit)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.TEMPERATURE:
            return 0, self.__value_to_si(value)
        if callback_id is CallbackID.TEMPERATURE_REACHED:
            return 0, self.__value_to_si(value)
        over_under, open_circuit = value
        return 1, GetErrorState(over_under, open_circuit)
