"""
Module for the Tinkerforge Industrial Counter Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialCounter_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
)
from .devices import Channel as ChannelDefinition
from .devices import ChannelConfiguration, DeviceIdentifier, SimpleCallbackConfiguration
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ALL_COUNTER = 19
    ALL_SIGNAL_DATA = 20


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_COUNTER = 1
    GET_ALL_COUNTER = 2
    SET_COUNTER = 3
    SET_ALL_COUNTER = 4
    GET_SIGNAL_DATA = 5
    GET_ALL_SIGNAL_DATA = 6
    SET_COUNTER_ACTIVE = 7
    SET_ALL_COUNTER_ACTIVE = 8
    GET_COUNTER_ACTIVE = 9
    GET_ALL_COUNTER_ACTIVE = 10
    SET_COUNTER_CONFIGURATION = 11
    GET_COUNTER_CONFIGURATION = 12
    SET_ALL_COUNTER_CALLBACK_CONFIGURATION = 13
    GET_ALL_COUNTER_CALLBACK_CONFIGURATION = 14
    SET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION = 15
    GET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION = 16
    SET_CHANNEL_LED_CONFIG = 17
    GET_CHANNEL_LED_CONFIG = 18


@unique
class Channel(Enum):
    """
    The channel options
    """

    CHANNEL_0 = 0
    CHANNEL_1 = 1
    CHANNEL_2 = 2
    CHANNEL_3 = 3


@unique
class CountEdge(Enum):
    """
    The count edge options
    """

    RISING = 0
    FALLING = 1
    BOTH = 2


@unique
class CountDirection(Enum):
    """
    The count direction options
    """

    UP = 0
    DOWN = 1
    EXTERNAL_UP = 2
    EXTERNAL_DOWN = 3


@unique
class DutyCyclePrescaler(Enum):
    """
    The duty cycle prescaler options
    """

    DUTY_CYCLE_PRESCALER_1 = 0
    DUTY_CYCLE_PRESCALER_2 = 1
    DUTY_CYCLE_PRESCALER_4 = 2
    DUTY_CYCLE_PRESCALER_8 = 3
    DUTY_CYCLE_PRESCALER_16 = 4
    DUTY_CYCLE_PRESCALER_32 = 5
    DUTY_CYCLE_PRESCALER_64 = 6
    DUTY_CYCLE_PRESCALER_128 = 7
    DUTY_CYCLE_PRESCALER_256 = 8
    DUTY_CYCLE_PRESCALER_512 = 9
    DUTY_CYCLE_PRESCALER_1024 = 10
    DUTY_CYCLE_PRESCALER_2048 = 11
    DUTY_CYCLE_PRESCALER_4096 = 12
    DUTY_CYCLE_PRESCALER_8192 = 13
    DUTY_CYCLE_PRESCALER_16384 = 14
    DUTY_CYCLE_PRESCALER_32768 = 15


@unique
class FrequencyIntegrationTime(Enum):
    """
    The frequency integration time options
    """

    FREQUENCY_INTEGRATION_TIME_128_MS = 0
    FREQUENCY_INTEGRATION_TIME_256_MS = 1
    FREQUENCY_INTEGRATION_TIME_512_MS = 2
    FREQUENCY_INTEGRATION_TIME_1024_MS = 3
    FREQUENCY_INTEGRATION_TIME_2048_MS = 4
    FREQUENCY_INTEGRATION_TIME_4096_MS = 5
    FREQUENCY_INTEGRATION_TIME_8192_MS = 6
    FREQUENCY_INTEGRATION_TIME_16384_MS = 7
    FREQUENCY_INTEGRATION_TIME_32768_MS = 8


@unique
class ChannelLEDConfig(Enum):
    """
    The channel led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_CHANNEL_STATUS = 3


class GetSignalData(NamedTuple):
    duty_cycle: Decimal
    period: Decimal
    frequency: Decimal
    value: bool


class GetAllSignalData(NamedTuple):
    duty_cycle: tuple[Decimal, ...]
    period: tuple[Decimal, ...]
    frequency: tuple[Decimal, ...]
    value: tuple[bool, ...]


class GetCounterConfiguration(NamedTuple):
    count_edge: CountEdge
    count_direction: CountDirection
    duty_cycle_prescaler: DutyCyclePrescaler
    frequency_integration_time: FrequencyIntegrationTime


CENTI_PERCENT = LinearQuantity(1, 100)  # raw: 1/100 Percent, returned in %
MILLI_HERTZ = LinearQuantity(1, 1000)  # raw: 1/1000 Hertz, returned in Hz
NANO_SECOND = LinearQuantity(1, 1000000000)  # raw: 1/1000000000 Second, returned in s


class BrickletIndustrialCounter(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    4 channel counter up to 4MHz
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_COUNTER
    DEVICE_DISPLAY_NAME = "Industrial Counter Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Channel: TypeAlias = Channel
    CountEdge: TypeAlias = CountEdge
    CountDirection: TypeAlias = CountDirection
    DutyCyclePrescaler: TypeAlias = DutyCyclePrescaler
    FrequencyIntegrationTime: TypeAlias = FrequencyIntegrationTime
    ChannelLEDConfig: TypeAlias = ChannelLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.ALL_COUNTER: "4q",
        CallbackID.ALL_SIGNAL_DATA: "4H 4Q 4I 4!",
    }

    CHANNELS = (
        ChannelDefinition(
            0,
            getter="get_all_counter",
            callbacks=(CallbackID.ALL_COUNTER,),
            configuration=ChannelConfiguration("all_counter", thresholds=False, wrap_advanced=True),
        ),
        ChannelDefinition(
            1,
            callbacks=(CallbackID.ALL_SIGNAL_DATA,),
            configuration=ChannelConfiguration("all_signal_data", thresholds=False, wrap_advanced=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

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
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_counter(self, channel: Channel | int) -> int:
        """
        Returns the current counter value for the given channel.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_COUNTER,
            data=pack_payload((Channel(channel).value,), "B"),
            response_expected=True,
        )
        return cast(int, unpack_payload(payload, "q"))

    async def get_all_counter(self) -> tuple[int, ...]:
        """
        Returns the current counter values for all four channels.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_COUNTER, response_expected=True
        )
        return tuple(unpack_payload(payload, "4q"))

    async def set_counter(self, channel: Channel | int, counter: int, response_expected: bool = True) -> None:
        """
        Sets the counter value for the given channel.

        The default value for the counters on startup is 0.
        """
        counter = int(counter)
        check_range("counter", counter, -140737488355328, 140737488355327)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COUNTER,
            data=pack_payload((Channel(channel).value, counter), "B q"),
            response_expected=response_expected,
        )

    async def set_all_counter(self, counter: Sequence[int], response_expected: bool = True) -> None:
        """
        Sets the counter values for all four channels.

        The default value for the counters on startup is 0.
        """
        check_length("counter", counter, 4)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALL_COUNTER,
            data=pack_payload((list(map(int, counter)),), "4q"),
            response_expected=response_expected,
        )

    async def get_signal_data(self, channel: Channel | int) -> GetSignalData:
        """
        Returns the signal data (duty cycle, period, frequency and value) for the
        given channel.

        Units: duty_cycle in % (0 to 100 %), frequency in Hz.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SIGNAL_DATA,
            data=pack_payload((Channel(channel).value,), "B"),
            response_expected=True,
        )
        duty_cycle, period, frequency, value = unpack_payload(payload, "H Q I !")
        return GetSignalData(
            CENTI_PERCENT.to_si(duty_cycle), NANO_SECOND.to_si(period), MILLI_HERTZ.to_si(frequency), value
        )

    async def get_all_signal_data(self) -> GetAllSignalData:
        """
        Returns the signal data (duty cycle, period, frequency and value) for all four
        channels.

        Units: duty_cycle in % (0 to 100 %), frequency in Hz.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_SIGNAL_DATA, response_expected=True
        )
        duty_cycle, period, frequency, value = unpack_payload(payload, "4H 4Q 4I 4!")
        return GetAllSignalData(
            tuple(CENTI_PERCENT.to_si(item) for item in duty_cycle),
            tuple(NANO_SECOND.to_si(item) for item in period),
            tuple(MILLI_HERTZ.to_si(item) for item in frequency),
            tuple(value),
        )

    async def set_counter_active(
        self, channel: Channel | int, active: bool = True, response_expected: bool = True
    ) -> None:
        """
        Activates/deactivates the counter of the given channel.

        true = activate, false = deactivate.

        By default all channels are activated.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COUNTER_ACTIVE,
            data=pack_payload((Channel(channel).value, bool(active)), "B !"),
            response_expected=response_expected,
        )

    async def set_all_counter_active(self, active: Sequence[bool], response_expected: bool = True) -> None:
        """
        Activates/deactivates the counter of all four channels.

        true = activate, false = deactivate.

        By default all channels are activated.
        """
        check_length("active", active, 4)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALL_COUNTER_ACTIVE,
            data=pack_payload(([bool(item) for item in active],), "4!"),
            response_expected=response_expected,
        )

    async def get_counter_active(self, channel: Channel | int) -> bool:
        """
        Returns the activation state of the given channel.

        true = activated, false = deactivated.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_COUNTER_ACTIVE,
            data=pack_payload((Channel(channel).value,), "B"),
            response_expected=True,
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def get_all_counter_active(self) -> tuple[bool, ...]:
        """
        Returns the activation state of all four channels.

        true = activated, false = deactivated.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_COUNTER_ACTIVE, response_expected=True
        )
        return tuple(unpack_payload(payload, "4!"))

    async def set_counter_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        channel: Channel | int,
        count_edge: CountEdge | int = CountEdge.RISING,
        count_direction: CountDirection | int = CountDirection.UP,
        duty_cycle_prescaler: DutyCyclePrescaler | int = DutyCyclePrescaler.DUTY_CYCLE_PRESCALER_1,
        frequency_integration_time: (
            FrequencyIntegrationTime | int
        ) = FrequencyIntegrationTime.FREQUENCY_INTEGRATION_TIME_1024_MS,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the counter configuration for the given channel.

        * Count Edge: Counter can count on rising, falling or both edges.
        * Count Direction: Counter can count up or down. You can also use
          another channel as direction input, see
          `here
          <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Counter.html#external-count-direction>`__
          for details.
        * Duty Cycle Prescaler: Sets a divider for the internal clock. See
          `here
          <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Counter.html#duty-cycle-prescaler-and-frequency-integration-time>`__
          for details.
        * Frequency Integration Time: Sets the integration time for the
          frequency measurement. See
          `here
          <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Counter.html#duty-cycle-prescaler-and-frequency-integration-time>`__
          for details.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COUNTER_CONFIGURATION,
            data=pack_payload(
                (
                    Channel(channel).value,
                    CountEdge(count_edge).value,
                    CountDirection(count_direction).value,
                    DutyCyclePrescaler(duty_cycle_prescaler).value,
                    FrequencyIntegrationTime(frequency_integration_time).value,
                ),
                "B B B B B",
            ),
            response_expected=response_expected,
        )

    async def get_counter_configuration(self, channel: Channel | int) -> GetCounterConfiguration:
        """
        Returns the counter configuration as set by :func:`set_counter_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_COUNTER_CONFIGURATION,
            data=pack_payload((Channel(channel).value,), "B"),
            response_expected=True,
        )
        count_edge, count_direction, duty_cycle_prescaler, frequency_integration_time = unpack_payload(
            payload, "B B B B"
        )
        return GetCounterConfiguration(
            CountEdge(count_edge),
            CountDirection(count_direction),
            DutyCyclePrescaler(duty_cycle_prescaler),
            FrequencyIntegrationTime(frequency_integration_time),
        )

    async def set_all_counter_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ALL_COUNTER`
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
            function_id=FunctionID.SET_ALL_COUNTER_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_all_counter_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_all_counter_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_COUNTER_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_all_signal_data_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ALL_SIGNAL_DATA`
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
            function_id=FunctionID.SET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_all_signal_data_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_all_signal_data_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_SIGNAL_DATA_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_channel_led_config(
        self,
        channel: Channel | int,
        config: ChannelLEDConfig | int = ChannelLEDConfig.SHOW_CHANNEL_STATUS,
        response_expected: bool = True,
    ) -> None:
        """
        Each channel has a corresponding LED. You can turn the LED off, on or show a
        heartbeat. You can also set the LED to "Channel Status". In this mode the
        LED is on if the channel is high and off otherwise.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_CONFIG,
            data=pack_payload((Channel(channel).value, ChannelLEDConfig(config).value), "B B"),
            response_expected=response_expected,
        )

    async def get_channel_led_config(self, channel: Channel | int) -> ChannelLEDConfig:
        """
        Returns the channel LED configuration as set by :func:`set_channel_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_CONFIG,
            data=pack_payload((Channel(channel).value,), "B"),
            response_expected=True,
        )
        return ChannelLEDConfig(unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.ALL_COUNTER:
            return 0, tuple(value)
        duty_cycle, period, frequency, value = value
        return 1, GetAllSignalData(
            tuple(CENTI_PERCENT.to_si(item) for item in duty_cycle),
            tuple(NANO_SECOND.to_si(item) for item in period),
            tuple(MILLI_HERTZ.to_si(item) for item in frequency),
            tuple(value),
        )
