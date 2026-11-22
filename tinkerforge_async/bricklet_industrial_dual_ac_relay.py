"""
Module for the Tinkerforge Industrial Dual AC Relay Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDualACRelay_Bricklet_Python.html) implemented using
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

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    MONOFLOP_DONE = 7


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_VALUE = 1
    GET_VALUE = 2
    SET_CHANNEL_LED_CONFIG = 3
    GET_CHANNEL_LED_CONFIG = 4
    SET_MONOFLOP = 5
    GET_MONOFLOP = 6
    SET_SELECTED_VALUE = 8


@unique
class ChannelLEDConfig(Enum):
    """
    The channel led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_CHANNEL_STATUS = 3


class GetValue(NamedTuple):
    channel0: bool
    channel1: bool


class GetMonoflop(NamedTuple):
    value: bool
    time: Decimal
    time_remaining: Decimal


class BrickletIndustrialDualACRelay(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Two relays to switch AC devices
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_DUAL_AC_RELAY
    DEVICE_DISPLAY_NAME = "Industrial Dual AC Relay Bricklet"

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
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_value(self, channel0: bool = False, channel1: bool = False, response_expected: bool = True) -> None:
        """
        Sets the state of the relays, *true* means on and *false* means off.
        For example: (true, false) turns relay 0 on and relay 1 off.

        If you just want to set one of the relays and don't know the current state
        of the other relay, you can get the state with :func:`get_value` or you
        can use :func:`set_selected_value`.

        All running monoflop timers will be aborted if this function is called.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VALUE,
            data=pack_payload((bool(channel0), bool(channel1)), "! !"),
            response_expected=response_expected,
        )

    async def get_value(self) -> GetValue:
        """
        Returns the state of the relays, *true* means on and *false* means off.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        channel0, channel1 = unpack_payload(payload, "! !")
        return GetValue(channel0, channel1)

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
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
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
        check_range("channel", channel, 0, 1)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_CONFIG,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        return ChannelLEDConfig(unpack_payload(payload, "B"))

    async def set_monoflop(self, channel: int, value: bool, time: Duration, response_expected: bool = True) -> None:
        """
        The first parameter can be 0 or 1 (relay 0 or relay 1). The second parameter
        is the desired state of the relay (*true* means on and *false* means off).
        The third parameter indicates the time that the relay should hold
        the state.

        If this function is called with the parameters (1, true, 1500):
        Relay 1 will turn on and in 1.5s it will turn off again.

        A monoflop can be used as a failsafe mechanism. For example: Lets assume you
        have a RS485 bus and a Industrial Dual AC Relay Bricklet connected to one of the
        slave stacks. You can now call this function every second, with a time parameter
        of two seconds. The relay will be on all the time. If now the RS485
        connection is lost, the relay will turn off in at most two seconds.

        Units: time in s.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
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
        Returns (for the given relay) the current state and the time as set by
        :func:`set_monoflop` as well as the remaining time until the state flips.

        If the timer is not running currently, the remaining time will be returned
        as 0.

        Units: time in s, time_remaining in s.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MONOFLOP, data=pack_payload((channel,), "B"), response_expected=True
        )
        value, time, time_remaining = unpack_payload(payload, "! I I")
        return GetMonoflop(value, ms_to_seconds(time), ms_to_seconds(time_remaining))

    async def set_selected_value(self, channel: int, value: bool, response_expected: bool = True) -> None:
        """
        Sets the state of the selected relay, *true* means on and *false*
        means off.

        A running monoflop timer for the selected relay will be aborted if this function
        is called.

        The other relay remains untouched.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_VALUE,
            data=pack_payload((channel, bool(value)), "B !"),
            response_expected=response_expected,
        )

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        channel, value = value
        return channel, value
