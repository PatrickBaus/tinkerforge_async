"""
Module for the Tinkerforge Industrial Dual Analog In Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Dual_Analog_In_V2.html) implemented using Python
asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units
to SI units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, DeviceIdentifier, Event, LedConfig
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    VOLTAGE = 4
    ALL_VOLTAGES = 17


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_VOLTAGE = 1
    SET_VOLTAGE_CALLBACK_CONFIGURATION = 2
    GET_VOLTAGE_CALLBACK_CONFIGURATION = 3
    SET_SAMPLE_RATE = 5
    GET_SAMPLE_RATE = 6
    SET_CALIBRATION = 7
    GET_CALIBRATION = 8
    GET_ADC_VALUES = 9
    SET_CHANNEL_LED_CONFIG = 10
    GET_CHANNEL_LED_CONFIG = 11
    SET_CHANNEL_LED_STATUS_CONFIG = 12
    GET_CHANNEL_LED_STATUS_CONFIG = 13
    GET_ALL_VOLTAGES = 14
    SET_ALL_VOLTAGES_CALLBACK_CONFIGURATION = 15
    GET_ALL_VOLTAGES_CALLBACK_CONFIGURATION = 16


@unique
class ChannelLedStatusConfig(Enum):
    """
    Defines the LED brightness when LedConfig.SHOW_STATUS
    """

    THRESHOLD = 0
    INTENSITY = 1


_ChannelLedStatusConfig = ChannelLedStatusConfig  # We need the alias for MyPy type hinting


@unique
class SamplingRate(Enum):
    """
    Defines the sampling rate of the ADC
    """

    RATE_976_SPS = 0
    RATE_488_SPS = 1
    RATE_244_SPS = 2
    RATE_122_SPS = 3
    RATE_61_SPS = 4
    RATE_4_SPS = 5
    RATE_2_SPS = 6
    RATE_1_SPS = 7


_SamplingRate = SamplingRate  # We need the alias for MyPy type hinting


class GetCalibration(NamedTuple):
    offset: int
    gain: int


class GetChannelLEDStatusConfig(NamedTuple):
    minimum: Decimal
    maximum: Decimal
    config: ChannelLedStatusConfig


class GetAllVoltagesCallbackConfiguration(NamedTuple):
    period: int
    value_has_to_change: bool


class BrickletIndustrialDualAnalogInV2(BrickletWithMCU):
    """
    Measures two DC voltages between -35V and +35V with 24bit resolution each
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_DUAL_ANALOG_IN_V2
    DEVICE_DISPLAY_NAME = "Industrial Dual Analog In Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    ChannelLedConfig = LedConfig
    ChannelLedStatusConfig = ChannelLedStatusConfig
    SamplingRate = SamplingRate

    CALLBACK_FORMATS = {
        CallbackID.VOLTAGE: "B i",
        CallbackID.ALL_VOLTAGES: "2i",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.VOLTAGE,),
        1: (CallbackID.VOLTAGE,),
        2: (CallbackID.ALL_VOLTAGES,),
    }

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> Decimal | tuple[Decimal, Decimal]:
        assert sid in (0, 1, 2)

        if sid in (0, 1):
            return await self.get_voltage(sid)
        return await self.get_all_voltages()

    async def set_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        sid: int,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        minimum = 0 if minimum is None else minimum
        maximum = 0 if maximum is None else maximum

        assert sid in (0, 1, 2)

        if sid in (0, 1):
            await self.set_voltage_callback_configuration(
                sid, period, value_has_to_change, option, minimum, maximum, response_expected
            )
        else:
            await self.set_all_voltages_callback_configuration(period, value_has_to_change, response_expected)

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        assert sid in (0, 1, 2)
        if sid in (0, 1):
            return await self.get_voltage_callback_configuration(sid)
        return AdvancedCallbackConfiguration(
            *(await self.get_all_voltages_callback_configuration()), option=None, minimum=None, maximum=None
        )

    async def get_voltage(self, channel: int) -> Decimal:
        """
        Returns the voltage for the given channel.


        If you want to get the value periodically, it is recommended to use the :cb:`Voltage` callback. You can set the
        callback configuration with :func:`Set Voltage Callback Configuration`.
        """
        assert channel in (0, 1)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_VOLTAGE,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )
        return self.__value_to_si(unpack_payload(payload, "i"))

    async def set_voltage_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        channel: int,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :cb:`Voltage` callback is triggered periodically. A value of 0 turns the
        callback off.

        If the `value has to change`-parameter is set to true, the callback is only triggered after the value has
        changed. If the value didn't change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period, independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Voltage` callback.

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
        assert channel in (0, 1)
        option = Threshold(option)
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(channel),
                    int(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    self.__si_to_value(minimum),
                    self.__si_to_value(maximum),
                ),
                "B I ! c i i",
            ),
            response_expected=response_expected,
        )

    async def get_voltage_callback_configuration(self, channel: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Voltage Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        option = Threshold(option)
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return AdvancedCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def get_all_voltages(self) -> tuple[Decimal, Decimal]:
        """
        Returns the voltages for all channels.


        If you want to get the value periodically, it is recommended to use the cb:`All Voltages` callback. You can set
        the callback configuration with :func:`Set All Voltages Callback Configuration`.

        .. versionadded:: 2.0.6$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_VOLTAGES, response_expected=True
        )
        value1, value2 = unpack_payload(payload, "2i")
        return self.__value_to_si(value1), self.__value_to_si(value2)

    async def set_all_voltages_callback_configuration(
        self, period: int = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :cb:`All Voltages` callback is triggered periodically. A value of 0
        turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only triggered after at least one of the
        values has changed. If the values didn't change within the period, the callback is triggered immediately on
        change.

        If it is set to false, the callback is continuously triggered with the period, independent of the value.

        .. versionadded:: 2.0.6$nbsp;(Plugin)
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALL_VOLTAGES_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(period),
                    bool(value_has_to_change),
                ),
                "I !",
            ),
            response_expected=response_expected,
        )

    async def get_all_voltages_callback_configuration(self) -> GetAllVoltagesCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set All Voltages Callback Configuration`.

        .. versionadded:: 2.0.6$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION, response_expected=True
        )
        return GetAllVoltagesCallbackConfiguration(*unpack_payload(payload, "I !"))

    async def set_sample_rate(self, rate: _SamplingRate | int, response_expected: bool = True) -> None:
        """
        Sets the sample rate. The sample rate can be between 1 sample per second and 976 samples per second. Decreasing
        the sample rate will also decrease the noise on the data.
        """
        rate = SamplingRate(rate)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SAMPLE_RATE,
            data=pack_payload((rate.value,), "B"),
            response_expected=response_expected,
        )

    async def get_sample_rate(self) -> _SamplingRate:
        """
        Returns the sample rate as set by :func:`Set Sample Rate`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SAMPLE_RATE, response_expected=True
        )

        return SamplingRate(unpack_payload(payload, "B"))

    async def set_calibration(
        self, offset: tuple[int, int] | list[int], gain: tuple[int, int] | list[int], response_expected: bool = True
    ) -> None:
        """
        Sets offset and gain of MCP3911 internal calibration registers.

        See MCP3911 datasheet 7.7 and 7.8. The Industrial Dual Analog In Bricklet 2.0 is already factory calibrated by
        Tinkerforge. It should not be necessary for you to use this function
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload((list(map(int, offset)), list(map(int, gain))), "2i 2i"),
            response_expected=response_expected,
        )

    async def get_calibration(self) -> GetCalibration:
        """
        Returns the calibration as set by :func:`Set Calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CALIBRATION, response_expected=True
        )

        return GetCalibration(*unpack_payload(payload, "2i 2i"))

    async def get_adc_values(self) -> tuple[int, int]:
        """
        Returns the ADC values as given by the MCP3911 IC. This function is needed for proper calibration, see
        :func:`Set Calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ADC_VALUES, response_expected=True
        )

        return unpack_payload(payload, "2i")

    async def set_channel_led_config(self, channel: int, config: LedConfig, response_expected: bool = True) -> None:
        """
        Each channel has a corresponding LED. You can turn the LED off, on or show a heartbeat. You can also set the LED
        to "Channel Status". In this mode the LED can either be turned on with a pre-defined threshold or the intensity
        of the LED can change with the measured value.

        You can configure the channel status behavior with :func:`Set Channel LED Status Config`.

        By default, all channel LEDs are configured as "Channel Status".
        """
        assert channel in (0, 1)
        config = LedConfig(config)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_CONFIG,
            data=pack_payload(
                (
                    int(channel),
                    config.value,
                ),
                "B B",
            ),
            response_expected=response_expected,
        )

    async def get_channel_led_config(self, channel: int) -> LedConfig:
        """
        Returns the ADC values as given by the MCP3911 IC. This function is needed for proper calibration, see
        :func:`Set Calibration`.
        """
        assert channel in (0, 1)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_CONFIG,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )

        return LedConfig(unpack_payload(payload, "B"))

    async def set_channel_led_status_config(  # pylint: disable=too-many-arguments
        self,
        channel: int,
        minimum: float | Decimal,
        maximum: float | Decimal,
        config: _ChannelLedStatusConfig | int,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the channel LED status config. This config is used if the channel LED is configured as "Channel Status",
        see :func:`Set Channel LED Config`.

        For each channel you can choose between threshold and intensity mode.

        In threshold mode you can define a positive or a negative threshold. For a positive threshold set the "min"
        parameter to the threshold value in mV above which the LED should turn on and set the "max" parameter to 0.
        Example: If you set a positive threshold of 10V, the LED will turn on as soon as the voltage exceeds 10V and
        turn off again if it goes below 10V. For a negative threshold set the "max" parameter to the threshold value in
        mV below which the LED should turn on and set the "min" parameter to 0. Example: If you set a negative threshold
        of 10V, the LED will turn on as soon as the voltage goes below 10V and the LED will turn off when the voltage
        exceeds 10V.

        In intensity mode you can define a range in mV that is used to scale the brightness of the LED. Example with
        min=4V, max=20V: The LED is off at 4V, on at 20V and the brightness is linearly scaled between the values
        4V and 20V. If the min value is greater than the max value, the LED brightness is scaled the other way around.
        """
        assert channel in (0, 1)
        config = ChannelLedStatusConfig(config)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_STATUS_CONFIG,
            data=pack_payload(
                (
                    int(channel),
                    self.__si_to_value(minimum),
                    self.__si_to_value(maximum),
                    config.value,
                ),
                "B i i B",
            ),
            response_expected=response_expected,
        )

    async def get_channel_led_status_config(self, channel: int) -> GetChannelLEDStatusConfig:
        """
        Returns the channel LED status configuration as set by :func:`Set Channel LED Status Config`.
        """
        assert channel in (0, 1)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_STATUS_CONFIG,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )

        minimum, maximum, config = unpack_payload(payload, "i i B")
        config = ChannelLedStatusConfig(config)
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return GetChannelLEDStatusConfig(minimum, maximum, config)

    @staticmethod
    def __value_to_si(value: int) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 1000

    @staticmethod
    def __si_to_value(value: float | Decimal) -> int:
        return int(value * 1000)

    async def read_events(
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        registered_events = set()
        if events:
            for event in events:
                registered_events.add(self.CallbackID(event))
        if sids is not None:
            for sid in sids:
                for callback in self.SID_TO_CALLBACK.get(sid, []):
                    registered_events.add(callback)

        if not events and not sids:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                if function_id is CallbackID.VOLTAGE:
                    channel, value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                    if sids is not None and channel not in sids:
                        # We got a reply from the wrong channel, maybe there is
                        # another callback running on that other channel, so we
                        # ignore the value
                        continue
                    yield Event(self, channel, function_id, self.__value_to_si(value))

                elif function_id is CallbackID.ALL_VOLTAGES:
                    values = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                    yield Event(self, 2, function_id, (self.__value_to_si(value) for value in values))
