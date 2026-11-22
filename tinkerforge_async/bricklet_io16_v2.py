"""
Module for the Tinkerforge IO-16 Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IO16V2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

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
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    INPUT_VALUE = 15
    ALL_INPUT_VALUE = 16
    MONOFLOP_DONE = 17


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_VALUE = 1
    GET_VALUE = 2
    SET_SELECTED_VALUE = 3
    SET_CONFIGURATION = 4
    GET_CONFIGURATION = 5
    SET_INPUT_VALUE_CALLBACK_CONFIGURATION = 6
    GET_INPUT_VALUE_CALLBACK_CONFIGURATION = 7
    SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION = 8
    GET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION = 9
    SET_MONOFLOP = 10
    GET_MONOFLOP = 11
    GET_EDGE_COUNT = 12
    SET_EDGE_COUNT_CONFIGURATION = 13
    GET_EDGE_COUNT_CONFIGURATION = 14


@unique
class Direction(Enum):
    """
    The direction options
    """

    IN = "i"
    OUT = "o"


@unique
class EdgeType(Enum):
    """
    The edge type options
    """

    RISING = 0
    FALLING = 1
    BOTH = 2


class GetConfiguration(NamedTuple):
    direction: Direction
    value: bool


class GetMonoflop(NamedTuple):
    value: bool
    time: Decimal
    time_remaining: Decimal


class GetEdgeCountConfiguration(NamedTuple):
    edge_type: EdgeType
    debounce: Decimal


class InputValueEvent(NamedTuple):
    changed: bool
    value: bool


class AllInputValueEvent(NamedTuple):
    changed: tuple[bool, ...]
    value: tuple[bool, ...]


class BrickletIO16V2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    16-channel digital input/output
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_IO16_V2
    DEVICE_DISPLAY_NAME = "IO-16 Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Direction: TypeAlias = Direction
    EdgeType: TypeAlias = EdgeType

    CALLBACK_FORMATS = {
        CallbackID.INPUT_VALUE: "B ! !",
        CallbackID.ALL_INPUT_VALUE: "16! 16!",
        CallbackID.MONOFLOP_DONE: "B !",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=0,
        ),
        Channel(
            1,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=1,
        ),
        Channel(
            2,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=2,
        ),
        Channel(
            3,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=3,
        ),
        Channel(
            4,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=4,
        ),
        Channel(
            5,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=5,
        ),
        Channel(
            6,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=6,
        ),
        Channel(
            7,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=7,
        ),
        Channel(
            8,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=8,
        ),
        Channel(
            9,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=9,
        ),
        Channel(
            10,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=10,
        ),
        Channel(
            11,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=11,
        ),
        Channel(
            12,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=12,
        ),
        Channel(
            13,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=13,
        ),
        Channel(
            14,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=14,
        ),
        Channel(
            15,
            callbacks=(CallbackID.INPUT_VALUE,),
            configuration=ChannelConfiguration("input_value", thresholds=False, wrap_advanced=True),
            index=15,
        ),
        Channel(
            16,
            callbacks=(CallbackID.ALL_INPUT_VALUE,),
            configuration=ChannelConfiguration("all_input_value", thresholds=False, wrap_advanced=True),
        ),
        Channel(17, callbacks=(CallbackID.MONOFLOP_DONE,), index=0),
        Channel(18, callbacks=(CallbackID.MONOFLOP_DONE,), index=1),
        Channel(19, callbacks=(CallbackID.MONOFLOP_DONE,), index=2),
        Channel(20, callbacks=(CallbackID.MONOFLOP_DONE,), index=3),
        Channel(21, callbacks=(CallbackID.MONOFLOP_DONE,), index=4),
        Channel(22, callbacks=(CallbackID.MONOFLOP_DONE,), index=5),
        Channel(23, callbacks=(CallbackID.MONOFLOP_DONE,), index=6),
        Channel(24, callbacks=(CallbackID.MONOFLOP_DONE,), index=7),
        Channel(25, callbacks=(CallbackID.MONOFLOP_DONE,), index=8),
        Channel(26, callbacks=(CallbackID.MONOFLOP_DONE,), index=9),
        Channel(27, callbacks=(CallbackID.MONOFLOP_DONE,), index=10),
        Channel(28, callbacks=(CallbackID.MONOFLOP_DONE,), index=11),
        Channel(29, callbacks=(CallbackID.MONOFLOP_DONE,), index=12),
        Channel(30, callbacks=(CallbackID.MONOFLOP_DONE,), index=13),
        Channel(31, callbacks=(CallbackID.MONOFLOP_DONE,), index=14),
        Channel(32, callbacks=(CallbackID.MONOFLOP_DONE,), index=15),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

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

    async def set_value(self, value: Sequence[bool], response_expected: bool = True) -> None:
        """
        Sets the output value of all sixteen channels. A value of *true* or *false* outputs
        logic 1 or logic 0 respectively on the corresponding channel.

        Use :func:`set_selected_value` to change only one output channel state.

        For example: (True, True, False, False, ..., False) will turn the channels 0-1
        high and the channels 2-15 low.

        All running monoflop timers will be aborted if this function is called.

        .. note::
         This function does nothing for channels that are configured as input. Pull-up
         resistors can be switched on with :func:`set_configuration`.
        """
        check_length("value", value, 16)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VALUE,
            data=pack_payload(([bool(item) for item in value],), "16!"),
            response_expected=response_expected,
        )

    async def get_value(self) -> tuple[bool, ...]:
        """
        Returns the logic levels that are currently measured on the channels.
        This function works if the channel is configured as input as well as if it is
        configured as output.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return tuple(unpack_payload(payload, "16!"))

    async def set_selected_value(self, channel: int, value: bool, response_expected: bool = True) -> None:
        """
        Sets the output value of a specific channel without affecting the other channels.

        A running monoflop timer for the specific channel will be aborted if this
        function is called.

        .. note::
         This function does nothing for channels that are configured as input. Pull-up
         resistors can be switched on with :func:`set_configuration`.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_VALUE,
            data=pack_payload((channel, bool(value)), "B !"),
            response_expected=response_expected,
        )

    async def set_configuration(
        self,
        channel: int,
        direction: Direction | str = Direction.IN,
        value: bool = True,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the value and direction of a specific channel. Possible directions
        are 'i' and 'o' for input and output.

        If the direction is configured as output, the value is either high or low
        (set as *true* or *false*).

        If the direction is configured as input, the value is either pull-up or
        default (set as *true* or *false*).

        For example:

        * (0, 'i', true) will set channel-0 as input pull-up.
        * (1, 'i', false) will set channel-1 as input default (floating if nothing is connected).
        * (2, 'o', true) will set channel-2 as output high.
        * (3, 'o', false) will set channel-3 as output low.

        A running monoflop timer for the specific channel will be aborted if this
        function is called.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((channel, Direction(direction).value, bool(value)), "B c !"),
            response_expected=response_expected,
        )

    async def get_configuration(self, channel: int) -> GetConfiguration:
        """
        Returns the channel configuration as set by :func:`set_configuration`.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CONFIGURATION,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        direction, value = unpack_payload(payload, "c !")
        return GetConfiguration(Direction(direction), value)

    async def set_input_value_callback_configuration(
        self, channel: int, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        This callback can be configured per channel.

        The period is the period with which the :attr:`CallbackID.INPUT_VALUE`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload((channel, period_raw, bool(value_has_to_change)), "B I !"),
            response_expected=response_expected,
        )

    async def get_input_value_callback_configuration(self, channel: int) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_input_value_callback_configuration`.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_all_input_value_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ALL_INPUT_VALUE`
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
            function_id=FunctionID.SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_all_input_value_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_all_input_value_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

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
        have a RS485 bus and a IO-16 Bricklet 2.0 connected to one of
        the slave stacks. You can now call this function every second, with a time
        parameter of two seconds and channel 0 closed. Channel 0 will be closed all the
        time. If now the RS485 connection is lost, then channel 0 will be opened in at
        most two seconds.

        Units: time in s.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
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
        check_range("channel", channel, 0, 15)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MONOFLOP, data=pack_payload((channel,), "B"), response_expected=True
        )
        value, time, time_remaining = unpack_payload(payload, "! I I")
        return GetMonoflop(value, ms_to_seconds(time), ms_to_seconds(time_remaining))

    async def get_edge_count(self, channel: int, reset_counter: bool) -> int:
        """
        Returns the current value of the edge counter for the selected channel. You can
        configure the edges that are counted with :func:`set_edge_count_configuration`.

        If you set the reset counter to *true*, the count is set back to 0
        directly after it is read.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT,
            data=pack_payload((channel, bool(reset_counter)), "B !"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def set_edge_count_configuration(
        self,
        channel: int,
        edge_type: EdgeType | int = EdgeType.RISING,
        debounce: Duration = Decimal("0.1"),
        response_expected: bool = True,
    ) -> None:
        """
        Configures the edge counter for a specific channel.

        The edge type parameter configures if rising edges, falling edges or
        both are counted if the channel is configured for input. Possible edge types are:

        * 0 = rising
        * 1 = falling
        * 2 = both

        Configuring an edge counter resets its value to 0.

        If you don't know what any of this means, just leave it at default. The
        default configuration is very likely OK for you.

        Units: debounce in s.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
        debounce_raw = seconds_to_ms(debounce)
        check_range("debounce", debounce_raw, 0, 255, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_COUNT_CONFIGURATION,
            data=pack_payload((channel, EdgeType(edge_type).value, debounce_raw), "B B B"),
            response_expected=response_expected,
        )

    async def get_edge_count_configuration(self, channel: int) -> GetEdgeCountConfiguration:
        """
        Returns the edge type and debounce time for the selected channel as set by
        :func:`set_edge_count_configuration`.

        Units: debounce in s.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 15)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT_CONFIGURATION,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        edge_type, debounce = unpack_payload(payload, "B B")
        return GetEdgeCountConfiguration(EdgeType(edge_type), ms_to_seconds(debounce))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.INPUT_VALUE:
            channel, changed, value = value
            return channel, InputValueEvent(changed, value)
        if callback_id is CallbackID.ALL_INPUT_VALUE:
            changed, value = value
            return 16, AllInputValueEvent(tuple(changed), tuple(value))
        channel, value = value
        return 17 + channel, value
