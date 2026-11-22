"""
Module for the Tinkerforge Industrial Digital Out 4 Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDigitalOut4V2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
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

    MONOFLOP_DONE = 6


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_VALUE = 1
    GET_VALUE = 2
    SET_SELECTED_VALUE = 3
    SET_MONOFLOP = 4
    GET_MONOFLOP = 5
    SET_CHANNEL_LED_CONFIG = 7
    GET_CHANNEL_LED_CONFIG = 8
    SET_PWM_CONFIGURATION = 9
    GET_PWM_CONFIGURATION = 10


@unique
class ChannelLEDConfig(Enum):
    """
    The channel led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_CHANNEL_STATUS = 3


class GetMonoflop(NamedTuple):
    value: bool
    time: Decimal
    time_remaining: Decimal


class GetPWMConfiguration(NamedTuple):
    frequency: Decimal
    duty_cycle: Decimal


CENTI_PERCENT = LinearQuantity(1, 100)  # raw: 1/100 Percent, returned in %
DECI_HERTZ = LinearQuantity(1, 10)  # raw: 1/10 Hertz, returned in Hz


class BrickletIndustrialDigitalOut4V2(
    BrickletWithMCU
):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    4 galvanically isolated digital outputs
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_DIGITAL_OUT_4_V2
    DEVICE_DISPLAY_NAME = "Industrial Digital Out 4 Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ChannelLEDConfig: TypeAlias = ChannelLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.MONOFLOP_DONE: "B !",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.MONOFLOP_DONE,), index=0),
        Channel(1, callbacks=(CallbackID.MONOFLOP_DONE,), index=1),
        Channel(2, callbacks=(CallbackID.MONOFLOP_DONE,), index=2),
        Channel(3, callbacks=(CallbackID.MONOFLOP_DONE,), index=3),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_value(self, value: Sequence[bool], response_expected: bool = True) -> None:
        """
        Sets the output value of all four channels. A value of *true* or *false* outputs
        logic 1 or logic 0 respectively on the corresponding channel.

        Use :func:`set_selected_value` to change only one output channel state.

        All running monoflop timers and PWMs will be aborted if this function is called.

        For example: (True, True, False, False) will turn the channels 0-1 high and the
        channels 2-3 low.
        """
        check_length("value", value, 4)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VALUE,
            data=pack_payload(([bool(item) for item in value],), "4!"),
            response_expected=response_expected,
        )

    async def get_value(self) -> tuple[bool, ...]:
        """
        Returns the logic levels that are currently output on the channels.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return tuple(unpack_payload(payload, "4!"))

    async def set_selected_value(self, channel: int, value: bool, response_expected: bool = True) -> None:
        """
        Sets the output value of a specific channel without affecting the other channels.

        A running monoflop timer or PWM for the specified channel will be aborted if this
        function is called.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 3)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_VALUE,
            data=pack_payload((channel, bool(value)), "B !"),
            response_expected=response_expected,
        )

    async def set_monoflop(self, channel: int, value: bool, time: Duration, response_expected: bool = True) -> None:
        """
        The first parameter is the desired state of the channel (*true* means output *high*
        and *false* means output *low*). The second parameter indicates the time that
        the channel should hold the state.

        If this function is called with the parameters (true, 1500):
        The channel will turn on and in 1.5s it will turn off again.

        A PWM for the selected channel will be aborted if this function is called.

        A monoflop can be used as a failsafe mechanism. For example: Lets assume you
        have a RS485 bus and a IO-4 Bricklet is connected to one of the slave
        stacks. You can now call this function every second, with a time parameter
        of two seconds. The channel will be *high* all the time. If now the RS485
        connection is lost, the channel will turn *low* in at most two seconds.

        Units: time in s.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 3)
        time_raw = seconds_to_ms(time)
        check_range("time", time_raw, 0, 4294967295, time)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MONOFLOP,
            data=pack_payload((channel, bool(value), time_raw), "B ! I"),
            response_expected=response_expected,
        )

    async def get_monoflop(self, channel: int) -> GetMonoflop:
        """
        Returns (for the given channel) the current value and the time as set by
        :func:`set_monoflop` as well as the remaining time until the value flips.

        If the timer is not running currently, the remaining time will be returned
        as 0.

        Units: time in s, time_remaining in s.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MONOFLOP, data=pack_payload((channel,), "B"), response_expected=True
        )
        value, time, time_remaining = unpack_payload(payload, "! I I")
        return GetMonoflop(value, ms_to_seconds(time), ms_to_seconds(time_remaining))

    async def set_channel_led_config(
        self,
        channel: int,
        config: ChannelLEDConfig | int = ChannelLEDConfig.SHOW_CHANNEL_STATUS,
        response_expected: bool = True,
    ) -> None:
        """
        Each channel has a corresponding LED. You can turn the LED off, on or show a
        heartbeat. You can also set the LED to "Channel Status". In this mode the
        LED is on if the channel is high and off otherwise.

        By default all channel LEDs are configured as "Channel Status".
        """
        channel = int(channel)
        check_range("channel", channel, 0, 3)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_CONFIG,
            data=pack_payload((channel, ChannelLEDConfig(config).value), "B B"),
            response_expected=response_expected,
        )

    async def get_channel_led_config(self, channel: int) -> ChannelLEDConfig:
        """
        Returns the channel LED configuration as set by :func:`set_channel_led_config`
        """
        channel = int(channel)
        check_range("channel", channel, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_CONFIG,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        return ChannelLEDConfig(unpack_payload(payload, "B"))

    async def set_pwm_configuration(
        self,
        channel: int,
        frequency: float | Decimal = 0,
        duty_cycle: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Activates a PWM for the given channel.

        To turn the PWM off again, you can set the frequency to 0 or any other
        function that changes a value of the channel (e.g. :func:`set_selected_value`).

        The optocoupler of the Industrial Digital
        Out 4 Bricklet 2.0 has a rise time and fall time of 11.5us (each) at 24V. So the maximum
        useful frequency value is about 400000 (40kHz).

        A running monoflop timer for the given channel will be aborted if this function
        is called.

        Units: frequency in Hz, duty_cycle in % (0 to 100 %).
        """
        channel = int(channel)
        check_range("channel", channel, 0, 3)
        frequency_raw = DECI_HERTZ.from_si(frequency)
        check_range("frequency", frequency_raw, 0, 4294967295, frequency)
        duty_cycle_raw = CENTI_PERCENT.from_si(duty_cycle)
        check_range("duty_cycle", duty_cycle_raw, 0, 10000, duty_cycle)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PWM_CONFIGURATION,
            data=pack_payload((channel, frequency_raw, duty_cycle_raw), "B I H"),
            response_expected=response_expected,
        )

    async def get_pwm_configuration(self, channel: int) -> GetPWMConfiguration:
        """
        Returns the PWM configuration as set by :func:`set_pwm_configuration`.

        Units: frequency in Hz, duty_cycle in % (0 to 100 %).
        """
        channel = int(channel)
        check_range("channel", channel, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PWM_CONFIGURATION,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        frequency, duty_cycle = unpack_payload(payload, "I H")
        return GetPWMConfiguration(DECI_HERTZ.to_si(frequency), CENTI_PERCENT.to_si(duty_cycle))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        channel, value = value
        return channel, value
