"""
Module for the Tinkerforge Industrial Quad Relay Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialQuadRelayV2_Bricklet_Python.html) implemented using
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

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    MONOFLOP_DONE = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_VALUE = 1
    GET_VALUE = 2
    SET_MONOFLOP = 3
    GET_MONOFLOP = 4
    SET_SELECTED_VALUE = 5
    SET_CHANNEL_LED_CONFIG = 6
    GET_CHANNEL_LED_CONFIG = 7


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


class BrickletIndustrialQuadRelayV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    4 galvanically isolated solid state relays
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_QUAD_RELAY_V2
    DEVICE_DISPLAY_NAME = "Industrial Quad Relay Bricklet 2.0"

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
        Sets the value of all four relays. A value of *true* closes the
        relay and a value of *false* opens the relay.

        Use :func:`set_selected_value` to only change one relay.

        All running monoflop timers will be aborted if this function is called.
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
        Returns the values as set by :func:`set_value`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return tuple(unpack_payload(payload, "4!"))

    async def set_monoflop(self, channel: int, value: bool, time: Duration, response_expected: bool = True) -> None:
        """
        Configures a monoflop of the specified channel.

        The second parameter is the desired value of the specified
        channel. A *true* means relay closed and a *false* means relay open.

        The third parameter indicates the time that the channels should hold
        the value.

        If this function is called with the parameters (0, 1, 1500) channel 0 will
        close and in 1.5s channel 0 will open again

        A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
        have a RS485 bus and a Industrial Quad Relay Bricklet 2.0 connected to one of
        the slave stacks. You can now call this function every second, with a time
        parameter of two seconds and channel 0 closed. Channel 0 will be closed all the
        time. If now the RS485 connection is lost, then channel 0 will be opened in at
        most two seconds.

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

    async def set_selected_value(self, channel: int, value: bool, response_expected: bool = True) -> None:
        """
        Sets the output value of the specified channel without affecting the other
        channels.

        A running monoflop timer for the specified channel will be aborted if this
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

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        channel, value = value
        return channel, value
