"""
Module for the Tinkerforge Humidity Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Humidity_V2.html) implemented using Python asyncIO. It does the
low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, DeviceIdentifier
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, TEMPERATURE, Quantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    HUMIDITY = 4
    TEMPERATURE = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_HUMIDITY = 1
    SET_HUMIDITY_CALLBACK_CONFIGURATION = 2
    GET_HUMIDITY_CALLBACK_CONFIGURATION = 3
    GET_TEMPERATURE = 5
    SET_TEMPERATURE_CALLBACK_CONFIGURATION = 6
    GET_TEMPERATURE_CALLBACK_CONFIGURATION = 7
    SET_HEATER_CONFIGURATION = 9
    GET_HEATER_CONFIGURATION = 10
    SET_MOVING_AVERAGE_CONFIGURATION = 11
    GET_MOVING_AVERAGE_CONFIGURATION = 12
    SET_SAMPLES_PER_SECOND = 13
    GET_SAMPLES_PER_SECOND = 14


@unique
class HeaterConfig(Enum):
    """
    The builtin heater can be used for testing purposes
    """

    DISABLED = 0
    ENABLED = 1


@unique
class SamplesPerSecond(Enum):
    """
    The sampling rate of the humidity sensor
    """

    SPS_20 = 0
    SPS_10 = 1
    SPS_5 = 2
    SPS_1 = 3
    SPS_02 = 4
    SPS_01 = 5


class GetMovingAverageConfiguration(NamedTuple):
    moving_average_length_humidity: int
    moving_average_length_temperature: int


HUMIDITY = Quantity(100)  # raw: 1/100 %RH


class BrickletHumidityV2(BrickletWithMCU):
    """
    Measures relative humidity
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_HUMIDITY_V2
    DEVICE_DISPLAY_NAME = "Humidity Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    HeaterConfig: TypeAlias = HeaterConfig
    SamplesPerSecond: TypeAlias = SamplesPerSecond

    CALLBACK_FORMATS = {
        CallbackID.HUMIDITY: "H",
        CallbackID.TEMPERATURE: "h",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.HUMIDITY,),
        1: (CallbackID.TEMPERATURE,),
    }

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 2)

    async def get_value(self, sid: int) -> Decimal:
        self._validate_sid(sid, (0, 1))

        if sid == 0:
            return await self.get_humidity()
        return await self.get_temperature()

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: Decimal | float | None = None,
        maximum: Decimal | float | None = None,
        response_expected: bool = True,
    ) -> None:
        self._validate_sid(sid, (0, 1))

        if sid == 0:
            minimum = 0 if minimum is None else minimum
            maximum = 0 if maximum is None else maximum
            await self.set_humidity_callback_configuration(
                period, value_has_to_change, option, minimum, maximum, response_expected
            )
        else:
            minimum = CELSIUS_ZERO if minimum is None else minimum
            maximum = CELSIUS_ZERO if maximum is None else maximum
            await self.set_temperature_callback_configuration(
                period, value_has_to_change, option, minimum, maximum, response_expected
            )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        self._validate_sid(sid, (0, 1))

        if sid == 0:
            return await self.get_humidity_callback_configuration()
        return await self.get_temperature_callback_configuration()

    async def get_humidity(self) -> Decimal:
        """
        Returns the humidity of the sensor. The value
        has a range of 0 to 100 and is given in %RH (relative humidity),
        i.e. a value of 42.1 means that a relative humidity of 42.1 %RH is measured.

        If you want to get the humidity periodically, it is recommended to use the
        :cb:`Humidity` callback and set the period with
        :func:`Set Humidity Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HUMIDITY, response_expected=True
        )
        return HUMIDITY.to_si(unpack_payload(payload, "H"))

    async def set_humidity_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: Decimal | float = 0,
        maximum: Decimal | float = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period in s is the period with which the :cb:`Humidity` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Humidity` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"


        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        option = Threshold(option)

        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")
        if minimum < 0:
            raise ValueError(f"Invalid argument: expected minimum >= 0, got minimum={minimum!r}")
        if maximum < 0:
            raise ValueError(f"Invalid argument: expected maximum >= 0, got maximum={maximum!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    seconds_to_ms(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    HUMIDITY.from_si(minimum),
                    HUMIDITY.from_si(maximum),
                ),
                "I ! c H H",
            ),
            response_expected=response_expected,
        )

    async def get_humidity_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Humidity Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HUMIDITY_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        option = Threshold(option)
        minimum, maximum = HUMIDITY.to_si(minimum), HUMIDITY.to_si(maximum)
        return AdvancedCallbackConfiguration(ms_to_seconds(period), value_has_to_change, option, minimum, maximum)

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature measured by the sensor in K. The value has a range of 233.15 to 438.15 K,
        i.e. a value of 305.15 K means that a temperature of 305.15 K is measured.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Temperature` callback. You can set the callback configuration
        with :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "h"))

    async def set_temperature_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: Decimal | float = CELSIUS_ZERO,
        maximum: Decimal | float = CELSIUS_ZERO,
        response_expected: bool = True,
    ) -> None:
        """
        The period in s is the period with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Temperature` callback. The
        thresholds are given in K.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"


        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 273.15, 273.15).
        """
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
                    TEMPERATURE.from_si(minimum),
                    TEMPERATURE.from_si(maximum),
                ),
                "I ! c h h",
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
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        option = Threshold(option)
        minimum, maximum = TEMPERATURE.to_si(minimum), TEMPERATURE.to_si(maximum)
        return AdvancedCallbackConfiguration(ms_to_seconds(period), value_has_to_change, option, minimum, maximum)

    async def set_heater_configuration(
        self, heater_config: HeaterConfig | int = HeaterConfig.DISABLED, response_expected: bool = True
    ) -> None:
        """
        Enables/disables the heater. The heater can be used to dry the sensor in
        extremely wet conditions.

        By default, the heater is disabled.
        """
        if not isinstance(heater_config, HeaterConfig):
            heater_config = HeaterConfig(heater_config)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HEATER_CONFIGURATION,
            data=pack_payload((heater_config.value,), "B"),
            response_expected=response_expected,
        )

    async def get_heater_configuration(self) -> HeaterConfig:
        """
        Returns the heater configuration as set by :func:`Set Heater Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HEATER_CONFIGURATION, response_expected=True
        )

        return HeaterConfig(unpack_payload(payload, "B"))

    async def set_moving_average_configuration(
        self,
        moving_average_length_humidity: int = 5,
        moving_average_length_temperature: int = 5,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the humidity and temperature.

        Setting the length to 1 will turn the averaging off. With less
        averaging, there is more noise on the data.

        The range for the averaging is 1-1000.

        New data is gathered every 50ms. With a moving average of length 1000 the resulting
        averaging window has a length of 50s. If you want to do long term measurements the longest
        moving average will give the cleanest results.

        * In firmware version 2.0.3 we added the set_samples_per_second() function. It configures
        the measurement frequency. Since high frequencies can result in self-heating of th IC,
        changed the default value from 20 samples per second to 1. With 1 sample per second a
         moving average length of 1000 would result in an averaging window of 1000 seconds!

        The default value is 5.
        """
        if moving_average_length_humidity < 1:
            raise ValueError(
                "Invalid argument: expected moving_average_length_humidity >= 1, "
                f"got moving_average_length_humidity={moving_average_length_humidity!r}"
            )
        if moving_average_length_temperature < 1:
            raise ValueError(
                "Invalid argument: expected moving_average_length_temperature >= 1, "
                f"got moving_average_length_temperature={moving_average_length_temperature!r}"
            )

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE_CONFIGURATION,
            data=pack_payload(
                (
                    int(moving_average_length_humidity),
                    int(moving_average_length_temperature),
                ),
                "H H",
            ),
            response_expected=response_expected,
        )

    async def get_moving_average_configuration(self) -> GetMovingAverageConfiguration:
        """
        Returns the moving average configuration as set by :func:`Set Moving Average Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOVING_AVERAGE_CONFIGURATION, response_expected=True
        )

        return GetMovingAverageConfiguration(*unpack_payload(payload, "H H"))

    async def set_samples_per_second(
        self, sps: SamplesPerSecond | int = SamplesPerSecond.SPS_1, response_expected: bool = True
    ) -> None:
        """
        Sets the samples per second that are gathered by the humidity/temperature sensor HDC1080.
        We added this function since we found out that a high measurement frequency can lead to
        self-heating of the sensor. Which can distort the temperature measurement.
        If you don't need a lot of measurements, you can use the lowest available measurement
        frequency of 0.1 samples per second for the least amount of self-heating.

        Before version 2.0.3 the default was 20 samples per second. The new default is 1 sample per second.
        """
        if not isinstance(sps, SamplesPerSecond):
            sps = SamplesPerSecond(sps)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SAMPLES_PER_SECOND,
            data=pack_payload((sps,), "B"),
            response_expected=response_expected,
        )

    async def get_samples_per_second(self) -> SamplesPerSecond:
        """
        Sets the samples per second that are gathered by the humidity/temperature sensor HDC1080.
        We added this function since we found out that a high measurement frequency can lead to
        self-heating of the sensor. Which can distort the temperature measurement.
        If you don't need a lot of measurements, you can use the lowest available measurement
        frequency of 0.1 samples per second for the least amount of self-heating.

        Before version 2.0.3 the default was 20 samples per second. The new default is 1 sample per second.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SAMPLES_PER_SECOND, response_expected=True
        )

        return SamplesPerSecond(unpack_payload(payload, "B"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.HUMIDITY:
            return 0, HUMIDITY.to_si(value)
        return 1, TEMPERATURE.to_si(value)
