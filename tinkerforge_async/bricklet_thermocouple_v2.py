"""
Module for the Tinkerforge Thermocouple Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermocouple_V2.html) implemented using Python asyncio. It does
the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, Channel, ChannelConfiguration, DeviceIdentifier
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, TEMPERATURE

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    TEMPERATURE = 4
    ERROR_STATE = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_TEMPERATURE = 1
    SET_TEMPERATURE_CALLBACK_CONFIGURATION = 2
    GET_TEMPERATURE_CALLBACK_CONFIGURATION = 3
    SET_CONFIGURATION = 5
    GET_CONFIGURATION = 6
    GET_ERROR_STATE = 7


@unique
class Averaging(Enum):
    """
    The number of values averaged before returning the measurement result.
    """

    AVERAGING_1 = 1
    AVERAGING_2 = 2
    AVERAGING_4 = 4
    AVERAGING_8 = 8
    AVERAGING_16 = 16


@unique
class SensorType(Enum):
    """
    The type of thermocouple connected to the bricklet.
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


class LineFilter(Enum):
    """
    Selects the notch filter to filter out the mains frequency hum
    """

    FREQUENCY_50HZ = 0
    FREQUENCY_60HZ = 1


class GetConfiguration(NamedTuple):
    averaging: Averaging
    sensor_type: SensorType
    filter: LineFilter


class GetErrorState(NamedTuple):
    """
    Tuple that contains the error states of the system. Over-/undervoltage indicates either a voltage above 3.3 V or
    below 0 V and likely a defective thermocouple. An open circuit indicates a missing or defective thermocouple.
    """

    over_under: bool
    open_circuit: bool


# The raw value of the types G8 and G32 is gain * 1.6 * 2^17 * Vin. Decimals keep the conversion exact.
G8_GAIN = 8 * Decimal("1.6") * 2**17
G32_GAIN = 32 * Decimal("1.6") * 2**17


class BrickletThermocoupleV2(BrickletWithMCU):
    """
    Measures temperature with a thermocouple.
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_THERMOCOUPLE_V2
    DEVICE_DISPLAY_NAME = "Thermocouple Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Averaging: TypeAlias = Averaging
    SensorType: TypeAlias = SensorType
    LineFilter: TypeAlias = LineFilter

    CALLBACK_FORMATS = {CallbackID.TEMPERATURE: "i", CallbackID.ERROR_STATE: "! !"}

    CHANNELS = (
        Channel(
            0,
            getter="get_temperature",
            callbacks=(CallbackID.TEMPERATURE,),
            configuration=ChannelConfiguration("temperature", default=CELSIUS_ZERO),
        ),
        Channel(1, getter="get_error_state", callbacks=(CallbackID.ERROR_STATE,)),
    )

    @property
    def sensor_type(self) -> SensorType:
        """
        Return the type of sensor. Either PT100 oder PT1000 as a SensorType enum.
        """
        return self.__sensor_type

    @sensor_type.setter
    def sensor_type(self, value: SensorType | int) -> None:
        if not isinstance(value, SensorType):
            self.__sensor_type: SensorType = SensorType(value)
        else:
            self.__sensor_type = value

    def __init__(self, uid: int, ipcon: IPConnectionAsync, sensor_type: SensorType | int = SensorType.TYPE_K) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        self.sensor_type = sensor_type  # Use the setter to automatically convert to enum

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            f"(uid={self.uid}, ipcon={self.ipcon!r}, sensor_type={self.sensor_type})"
        )

    async def get_value(self, sid: int) -> Decimal | GetErrorState:
        return cast(Decimal | GetErrorState, await self._get_value(sid))

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
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    @override
    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        # Only the temperature (sid 0) has a callback configuration. The error state is always reported.
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the thermocouple in K, e.g. a value of 315.38 K means that a temperature of
        315.38 K is measured. If the thermocouple type is G8 or G32, the value is not a temperature, but the
        thermocouple input voltage in V, see :func:`Set Configuration`.

        If you want to get the temperature periodically, it is recommended
        to use the :cb:`Temperature` callback and set the period with
        :func:`Set Temperature Callback Configuration`.

        If you want to get the value periodically, it is recommended to use the
        :cb:`Temperature` callback. You can set the callback configuration
        with :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return self.__value_to_si(unpack_payload(payload, "i"))

    async def set_temperature_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: Decimal | int | float = CELSIUS_ZERO,
        maximum: Decimal | int | float = CELSIUS_ZERO,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Temperature` callback. The
        thresholds are given in K (or in V for the types G8 and G32).

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
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    seconds_to_ms(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    self.__si_to_value(minimum),
                    self.__si_to_value(maximum),
                ),
                "I ! c i i",
            ),
            response_expected=response_expected,
        )

    async def get_temperature_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        option = Threshold(option)
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return AdvancedCallbackConfiguration(ms_to_seconds(period), value_has_to_change, option, minimum, maximum)

    async def set_configuration(
        self,
        averaging: Averaging = Averaging.AVERAGING_16,
        sensor_type: SensorType = SensorType.TYPE_K,
        line_filter: LineFilter = LineFilter.FREQUENCY_50HZ,
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
        if not isinstance(averaging, Averaging):
            averaging = Averaging(averaging)
        if not isinstance(sensor_type, SensorType):
            sensor_type = SensorType(sensor_type)
        if not isinstance(line_filter, LineFilter):
            line_filter = LineFilter(line_filter)

        self.__sensor_type = sensor_type
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((averaging.value, sensor_type.value, line_filter.value), "B B B"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )

        averaging, sensor_type, line_filter = unpack_payload(payload, "B B B")
        return GetConfiguration(Averaging(averaging), SensorType(sensor_type), LineFilter(line_filter))

    async def get_error_state(self) -> GetErrorState:
        """
        Returns the current error state. There are two possible errors:

        * Over/Under Voltage and
        * Open Circuit.

        Over/Under Voltage happens for voltages below 0V or above 3.3V. In this case
        it is very likely that your thermocouple is defective. An Open Circuit error
        indicates that there is no thermocouple connected.

        You can use the :cb:`Error State` callback to automatically get triggered
        when the error state changes.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_STATE, response_expected=True
        )

        over_under, open_circuit = unpack_payload(payload, "! !")
        return GetErrorState(over_under, open_circuit)

    def __value_to_si(self, value: int) -> Decimal:
        """
        Convert to the sensor value to SI units
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

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.TEMPERATURE:
            return 0, self.__value_to_si(value)
        return 1, value
