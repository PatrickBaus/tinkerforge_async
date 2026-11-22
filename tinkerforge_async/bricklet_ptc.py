"""
Module for the Tinkerforge PTC Bricklet (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/PTC.html)implemented
using Python asyncIO. It does the low-level communication with the Tinkerforge ip connection and also handles conversion
of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, TypeAlias, cast, override

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

    TEMPERATURE = 13
    TEMPERATURE_REACHED = 14
    RESISTANCE = 15
    RESISTANCE_REACHED = 16
    SENSOR_CONNECTED = 24


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_TEMPERATURE = 1
    GET_RESISTANCE = 2
    SET_TEMPERATURE_CALLBACK_PERIOD = 3
    GET_TEMPERATURE_CALLBACK_PERIOD = 4
    SET_RESISTANCE_CALLBACK_PERIOD = 5
    GET_RESISTANCE_CALLBACK_PERIOD = 6
    SET_TEMPERATURE_CALLBACK_THRESHOLD = 7
    GET_TEMPERATURE_CALLBACK_THRESHOLD = 8
    SET_RESISTANCE_CALLBACK_THRESHOLD = 9
    GET_RESISTANCE_CALLBACK_THRESHOLD = 10
    SET_DEBOUNCE_PERIOD = 11
    GET_DEBOUNCE_PERIOD = 12
    SET_NOISE_REJECTION_FILTER = 17
    GET_NOISE_REJECTION_FILTER = 18
    IS_SENSOR_CONNECTED = 19
    SET_WIRE_MODE = 20
    GET_WIRE_MODE = 21
    SET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION = 22
    GET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION = 23


@unique
class LineFilter(Enum):
    """
    Selects the notch filter to filter out the mains frequency hum
    """

    FREQUENCY_50HZ = 0
    FREQUENCY_60HZ = 1


@unique
class WireMode(Enum):
    """
    Select the measurement setup. Use 3 or 4 wires to eliminate most/all the
    resistance of the wire. Use 3 or 4 wire setups when using PT100 and long
    cables.
    """

    WIRE_2 = 2
    WIRE_3 = 3
    WIRE_4 = 4


@unique
class SensorType(Enum):
    """
    The type of sensor used
    """

    PT_100 = 0
    PT_1000 = 1


class BrickletPtc(Device):  # pylint: disable=too-many-public-methods
    """
    Reads temperatures from Pt100 und Pt1000 sensors
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_PTC
    DEVICE_DISPLAY_NAME = "PTC Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    LineFilter: TypeAlias = LineFilter
    WireMode: TypeAlias = WireMode
    SensorType: TypeAlias = SensorType

    CALLBACK_FORMATS = {
        CallbackID.TEMPERATURE: "i",
        CallbackID.TEMPERATURE_REACHED: "i",
        CallbackID.RESISTANCE: "i",
        CallbackID.RESISTANCE_REACHED: "i",
        CallbackID.SENSOR_CONNECTED: "!",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_temperature",
            callbacks=(CallbackID.TEMPERATURE, CallbackID.TEMPERATURE_REACHED),
            configuration=ChannelConfiguration("temperature", split=True, default=CELSIUS_ZERO),
        ),
        Channel(
            1,
            getter="get_resistance",
            callbacks=(CallbackID.RESISTANCE, CallbackID.RESISTANCE_REACHED),
            configuration=ChannelConfiguration("resistance", split=True),
        ),
        Channel(2, getter="is_sensor_connected", callbacks=(CallbackID.SENSOR_CONNECTED,)),
    )

    @property
    def sensor_type(self) -> SensorType:
        """
        Return the type of sensor. Either PT100 oder PT1000 as a SensorType
        enum.
        """
        return self.__sensor_type

    @sensor_type.setter
    def sensor_type(self, value: SensorType | int) -> None:
        self.__sensor_type = SensorType(value)

    def __init__(self, uid: int, ipcon: IPConnectionAsync, sensor_type: SensorType | int = SensorType.PT_100) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)
        self.sensor_type = sensor_type  # Use the setter to automatically convert to enum

    @override
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            f"(uid={self.uid}, ipcon={self.ipcon!r}, sensor_type={self.sensor_type})"
        )

    async def get_value(self, sid: int) -> Decimal | bool:
        return cast(Decimal | bool, await self._get_value(sid))

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
        # The sensor connected callback (sid 2) cannot be configured.
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    @override
    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        # The sensor connected callback (sid 2) cannot be configured.
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the sensor in K. The value has a range of 27.15 to 1122.15 K,
        e.g. a value of 315.38 K means that a temperature of 315.38 K is measured.

        If you want to get the temperature periodically, it is recommended
        to use the :cb:`Temperature` callback and set the period with
        :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "i"))

    async def get_resistance(self) -> Decimal:
        """
        Returns the value as measured by the MAX31865 precision delta-sigma ADC.

        The value can be converted with the following formulas:

        * Pt100:  resistance = (value * 390) / 32768
        * Pt1000: resistance = (value * 3900) / 32768

        If you want to get the resistance periodically, it is recommended
        to use the :cb:`Resistance` callback and set the period with
        :func:`Set Resistance Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RESISTANCE, response_expected=True
        )
        return self.__value_to_si_resistance(unpack_payload(payload, "i"))

    async def set_temperature_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period in s with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Temperature` callback is only triggered if the temperature has changed
        since the last triggering.

        The default value is 0.
        """
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_temperature_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_resistance_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :cb:`Resistance` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Resistance` callback is only triggered if the resistance has changed
        since the last triggering.
        """
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RESISTANCE_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_resistance_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set Resistance Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RESISTANCE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_temperature_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = CELSIUS_ZERO,
        maximum: float | Decimal = CELSIUS_ZERO,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Temperature Reached` callback. The thresholds are given in K.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

        The default value is ('x', 273.15, 273.15).
        """
        option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value.encode("ascii"),
                    TEMPERATURE.from_si(minimum),
                    TEMPERATURE.from_si(maximum),
                ),
                "c i i",
            ),
            response_expected=response_expected,
        )

    async def get_temperature_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        option = Threshold(option)
        minimum, maximum = TEMPERATURE.to_si(minimum), TEMPERATURE.to_si(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_resistance_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Resistance Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the resistance is *outside* the min and max values"
         "'i'",    "Callback is triggered when the resistance is *inside* the min and max values"
         "'<'",    "Callback is triggered when the resistance is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the resistance is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RESISTANCE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value.encode("ascii"),
                    self.__si_resistance_to_value(minimum),
                    self.__si_resistance_to_value(maximum),
                ),
                "c i i",
            ),
            response_expected=response_expected,
        )

    async def get_resistance_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RESISTANCE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        option = Threshold(option)
        minimum, maximum = self.__value_to_si_resistance(minimum), self.__value_to_si_resistance(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_debounce_period(
        self, debounce_period: Duration = Decimal("0.1"), response_expected: bool = True
    ) -> None:
        """
        Sets the period in s with which the threshold callback

        * :cb:`Temperature Reached`

        is triggered, if the threshold

        * :func:`Set Temperature Callback Threshold`

        keeps being reached.

        The default value is 0.1.
        """
        if debounce_period < 0:
            raise ValueError(
                f"Invalid argument: expected debounce_period >= 0, got debounce_period={debounce_period!r}"
            )

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((seconds_to_ms(debounce_period),), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> Decimal:
        """
        Returns the debounce-period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_noise_rejection_filter(
        self, line_filter: LineFilter | int = LineFilter.FREQUENCY_50HZ, response_expected: bool = True
    ) -> None:
        """
        Sets the noise rejection filter to either 50Hz (0) or 60Hz (1).
        Noise from 50Hz or 60Hz power sources (including
        harmonics of the AC power's fundamental frequency) is
        attenuated by 82dB.

        Default value is 0 = 50Hz.
        """
        line_filter = LineFilter(line_filter)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_NOISE_REJECTION_FILTER,
            data=pack_payload((line_filter.value,), "B"),
            response_expected=response_expected,
        )

    async def get_noise_rejection_filter(self) -> LineFilter:
        """
        Returns the noise rejection filter option as set by
        :func:`Set Noise Rejection Filter`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_NOISE_REJECTION_FILTER, response_expected=True
        )
        return LineFilter(unpack_payload(payload, "B"))

    async def is_sensor_connected(self) -> bool:
        """
        Returns *true* if the sensor is connected correctly.

        If this function
        returns *false*, there is either no Pt100 or Pt1000 sensor connected,
        the sensor is connected incorrectly or the sensor itself is faulty.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_SENSOR_CONNECTED, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def set_wire_mode(self, mode: WireMode | int = WireMode.WIRE_2, response_expected: bool = True) -> None:
        """
        Sets the wire mode of the sensor. Possible values are 2, 3 and 4 which
        correspond to 2-, 3- and 4-wire sensors. The value has to match the jumper
        configuration on the Bricklet.

        The default value is 2 = 2-wire.
        """
        mode = WireMode(mode)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIRE_MODE,
            data=pack_payload((mode.value,), "B"),
            response_expected=response_expected,
        )

    async def get_wire_mode(self) -> WireMode:
        """
        Returns the wire mode as set by :func:`Set Wire Mode`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIRE_MODE, response_expected=True
        )
        return WireMode(unpack_payload(payload, "B"))

    async def set_sensor_connected_callback_configuration(self, enabled: bool, response_expected: bool = True) -> None:
        """
        If you enable this callback, the :cb:`Sensor Connected` callback is triggered
        every time a Pt sensor is connected/disconnected.

        By default this callback is disabled.

        .. versionadded:: 2.0.2$nbsp;(Plugin)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_sensor_connected_callback_configuration(self) -> bool:
        """
                Returns the configuration as set by :func:`Set Sensor Connected Callback Configuration`.
        set_sensor_connected_callback_configuration
                .. versionadded:: 2.0.2$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    def __value_to_si_resistance(self, value: int) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        result = Decimal(value) * 390 / 32768
        if self.__sensor_type is SensorType.PT_1000:
            result *= 10
        return result

    def __si_resistance_to_value(self, value: float | Decimal) -> int:
        if self.__sensor_type is SensorType.PT_1000:
            value /= 10
        return round(value * 32768 / 390)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id in (CallbackID.TEMPERATURE, CallbackID.TEMPERATURE_REACHED):
            return 0, TEMPERATURE.to_si(value)
        if callback_id in (CallbackID.RESISTANCE, CallbackID.RESISTANCE_REACHED):
            return 1, self.__value_to_si_resistance(value)
        return 2, value
