"""
Module for the Tinkerforge IO-4 Bricklet 2.0 (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/IO4_V2.html)
implemented using Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

import asyncio
from asyncio import CancelledError
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple, TypeAlias, TypedDict

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    DeviceIdentifier,
    Event,
    SimpleCallbackConfiguration,
)
from .devices import ThresholdOption as Threshold
from .devices import (
    _FunctionID,
)
from .helper import join
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import HeaderPayload, IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    INPUT_VALUE = 17
    ALL_INPUT_VALUE = 18
    MONOFLOP_DONE = 19
    EDGE_COUNT = 20


_CallbackID: TypeAlias = CallbackID  # pylint: disable=invalid-name


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
    SET_PWM_CONFIGURATION = 15
    GET_PWM_CONFIGURATION = 16


@unique
class Direction(Enum):
    """
    Configures a pin as input or output
    """

    IN = "i"
    OUT = "o"


_Direction = Direction


@unique
class EdgeType(Enum):
    """
    Trigger at a rising or falling edge or both
    """

    RISING = 0
    FALLING = 1
    BOTH = 2


_EdgeType = EdgeType


class _EdgeCountTaskConfig(TypedDict):
    queue: asyncio.Queue[Event]
    task: asyncio.Task | None
    lock: asyncio.Lock
    period: int
    value_has_to_change: bool


class GetConfiguration(NamedTuple):
    direction: Direction
    value: bool


class GetInputValueCallbackConfiguration(NamedTuple):
    period: int
    value_has_to_change: bool


class GetMonoflop(NamedTuple):
    value: bool
    time: int
    time_remaining: int


class GetEdgeCountConfiguration(NamedTuple):
    edge_type: EdgeType
    debounce: int


class GetPWMConfiguration(NamedTuple):
    frequency: Decimal
    duty_cycle: Decimal


class BrickletIO4V2(BrickletWithMCU):  # pylint: disable=too-many-public-methods
    """
    4-channel digital input/output
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_IO_4_V2
    DEVICE_DISPLAY_NAME = "IO-4 Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    Direction = Direction
    EdgeType = EdgeType

    CALLBACK_FORMATS = {
        CallbackID.INPUT_VALUE: "B ! !",
        CallbackID.ALL_INPUT_VALUE: "4! 4!",
        CallbackID.MONOFLOP_DONE: "B !",
    }

    SID_TO_CALLBACK = {i: (CallbackID.INPUT_VALUE, CallbackID.MONOFLOP_DONE) for i in range(4)}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        # The queues are used by the pulse counter
        self.__counter_queue: dict[int, _EdgeCountTaskConfig] = {
            channel: {
                "queue": asyncio.Queue(maxsize=1),
                "task": None,
                "lock": asyncio.Lock(),
                "period": 0,
                "value_has_to_change": False,
            }
            for channel in range(4)
        }

    async def set_value(
        self, value: tuple[bool, bool, bool, bool] | list[bool], response_expected: bool = True
    ) -> None:
        """
        Sets the output value of all four channels. A value of *true* or *false* outputs
        logic 1 or logic 0 respectively on the corresponding channel.

        Use :func:`Set Selected Value` to change only one output channel state.

        For example: (True, True, False, False) will turn the channels 0-1 high and the
        channels 2-3 low.

        All running monoflop timers and PWMs will be aborted if this function is called.

        .. note::
         This function does nothing for channels that are configured as input. Pull-up
         resistors can be switched on with :func:`Set Configuration`.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VALUE,
            data=pack_payload((list(map(bool, value)),), "4!"),
            response_expected=response_expected,
        )

    async def get_value(self) -> tuple[bool, bool, bool, bool]:
        """
        Returns the logic levels that are currently measured on the channels.
        This function works if the channel is configured as input as well as if it is
        configured as output.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return unpack_payload(payload, "4!")

    async def set_selected_value(self, channel: int, value: bool, response_expected: bool = True) -> None:
        """
        Sets the output value of a specific channel without affecting the other channels.

        A running monoflop timer or PWM for the specific channel will be aborted if this
        function is called.

        .. note::
         This function does nothing for channels that are configured as input. Pull-up
         resistors can be switched on with :func:`Set Configuration`.
        """
        assert channel in (0, 1, 2, 3)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_VALUE,
            data=pack_payload(
                (
                    channel,
                    bool(value),
                ),
                "B !",
            ),
            response_expected=response_expected,
        )

    async def set_configuration(
        self,
        channel: int,
        direction: _Direction | str = Direction.IN,
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

        * (0, 'i', true) will set channel 0 as input pull-up.
        * (1, 'i', false) will set channel 1 as input default (floating if nothing is connected).
        * (2, 'o', true) will set channel 2 as output high.
        * (3, 'o', false) will set channel 3 as output low.

        A running monoflop timer or PWM for the specific channel will be aborted if this
        function is called.
        """
        assert channel in (0, 1, 2, 3)
        if not isinstance(direction, Direction):
            direction = Direction(direction)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload(
                (
                    channel,
                    direction.value.encode("ascii"),
                    bool(value),
                ),
                "B c !",
            ),
            response_expected=response_expected,
        )

    async def get_configuration(self, channel: int) -> GetConfiguration:
        """
        Returns the channel configuration as set by :func:`Set Configuration`.
        """
        assert channel in (0, 1, 2, 3)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CONFIGURATION,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )
        direction, value = unpack_payload(payload, "c !")
        direction = Direction(direction)
        return GetConfiguration(direction, value)

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments,unused-argument
        self,
        sid: int,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        assert sid in range(4 + 1 + 4)

        if sid in range(4):
            await self.set_input_value_callback_configuration(sid, period, value_has_to_change, response_expected)
        elif sid == 4:
            await self.set_all_input_value_callback_configuration(period, value_has_to_change, response_expected)
        elif sid in range(5, 5 + 4):
            await self.set_edge_count_callback_configuration(sid - 5, period, value_has_to_change, response_expected)

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        assert sid in range(4 + 1 + 4)

        if sid in range(4):
            return AdvancedCallbackConfiguration(
                *(await self.get_input_value_callback_configuration(sid)), option=None, minimum=None, maximum=None
            )
        if sid == 4:
            return AdvancedCallbackConfiguration(
                *(await self.get_all_input_value_callback_configuration()), option=None, minimum=None, maximum=None
            )
        if sid in range(5, 5 + 4):
            return AdvancedCallbackConfiguration(
                *(await self.get_edge_count_callback_configuration(sid - 5)), option=None, minimum=None, maximum=None
            )

        raise ValueError(f"Invalid sid: {sid}")

    async def set_input_value_callback_configuration(
        self, channel: int, period: int = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        This callback can be configured per channel.

        The period is the period with which the :cb:`Input Value`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        assert channel in (0, 1, 2, 3)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    channel,
                    int(period),
                    bool(value_has_to_change),
                ),
                "B I !",
            ),
            response_expected=response_expected,
        )

    async def get_input_value_callback_configuration(self, channel: int) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration for the given channel as set by
        :func:`Set Input Value Callback Configuration`.
        """
        assert channel in (0, 1, 2, 3)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )
        return SimpleCallbackConfiguration(*unpack_payload(payload, "I !"))

    async def set_all_input_value_callback_configuration(
        self, period: int = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :cb:`All Input Value`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(period),
                    bool(value_has_to_change),
                ),
                "I !",
            ),
            response_expected=response_expected,
        )

    async def get_all_input_value_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`Set All Input Value Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION, response_expected=True
        )
        return SimpleCallbackConfiguration(*unpack_payload(payload, "I !"))

    async def set_edge_count_callback_configuration(  # pylint: disable=unused-argument
        self, channel: int, period: int = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        Enable an edge counter task. This task will feed a queue to be read by calling __read_edge_counter().
        Do note, that the edge counter needs to sync first, so the first value will be available after period * 2.

        Parameters
        ----------
        channel: int
            The input channel used for edge counting. Must in range(0,3).
        period: int
            Time in ms
        value_has_to_change: bool
            If True, the event will be suppressed if there was no change
        response_expected: bool
            No effect. Parameter is used for compatibility with other callback configuration functions only.
        """
        assert channel in (0, 1, 2, 3)

        async with self.__counter_queue[channel]["lock"]:
            task = self.__counter_queue[channel]["task"]
            # We either need to create a new task or just kill the existing one
            if task is not None:
                task.cancel()
                try:
                    await task
                except CancelledError:
                    pass

            if period > 0:
                self.__counter_queue[channel]["task"] = asyncio.create_task(
                    self.__edge_counter_task(channel, period, value_has_to_change)
                )
            else:
                queue = self.__counter_queue[channel]["queue"]
                if not queue.empty():  # The queue has a maximum of 1 element
                    queue.get_nowait()
                    queue.task_done()
            self.__counter_queue[channel]["period"] = period
            self.__counter_queue[channel]["value_has_to_change"] = value_has_to_change

    async def get_edge_count_callback_configuration(self, channel: int) -> SimpleCallbackConfiguration:
        period = self.__counter_queue[channel]["period"]
        value_has_to_change = self.__counter_queue[channel]["value_has_to_change"]
        return SimpleCallbackConfiguration(period=period, value_has_to_change=value_has_to_change)

    async def set_monoflop(self, channel: int, value: bool, time: int, response_expected: bool = True) -> None:
        """
        The first parameter is the desired state of the channel (*true* means output *high*
        and *false* means output *low*). The second parameter indicates the time that
        the channel should hold the state.

        If this function is called with the parameters (true, 1500):
        The channel will turn on and in 1.5s it will turn off again.

        A PWM for the selected channel will be aborted if this function is called.

        A monoflop can be used as a failsafe mechanism. For example: Lets assume you
        have a RS485 bus and a IO-4 Bricklet 2.0 is connected to one of the slave
        stacks. You can now call this function every second, with a time parameter
        of two seconds. The channel will be *high* all the time. If now the RS485
        connection is lost, the channel will turn *low* in at most two seconds.
        """
        assert channel in (0, 1, 2, 3)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MONOFLOP,
            data=pack_payload(
                (
                    int(channel),
                    bool(value),
                    int(time),
                ),
                "B ! I",
            ),
            response_expected=response_expected,
        )

    async def get_monoflop(self, channel: int) -> GetMonoflop:
        """
        Returns (for the given channel) the current value and the time as set by
        :func:`Set Monoflop` as well as the remaining time until the value flips.

        If the timer is not running currently, the remaining time will be returned
        as 0.
        """
        assert channel in (0, 1, 2, 3)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_MONOFLOP,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )
        return GetMonoflop(*unpack_payload(payload, "! I I"))

    async def get_edge_count(self, channel: int, reset_counter: bool = False) -> int:
        """
        Returns the current value of the edge counter for the selected channel. You can
        configure the edges that are counted with :func:`Set Edge Count Configuration`.

        If you set the reset counter to *true*, the count is set back to 0
        directly after it is read.

        .. note::
         Calling this function is only allowed for channels configured as input.
        """
        assert channel in (0, 1, 2, 3)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT,
            data=pack_payload(
                (
                    int(channel),
                    bool(reset_counter),
                ),
                "B !",
            ),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def set_edge_count_configuration(
        self,
        channel: int,
        edge_type: _EdgeType | int = EdgeType.RISING,
        debounce: int = 100,
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

        .. note::
         Calling this function is only allowed for channels configured as input.
        """
        assert channel in (0, 1, 2, 3)
        if not isinstance(edge_type, EdgeType):
            edge_type = EdgeType(edge_type)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_COUNT_CONFIGURATION,
            data=pack_payload(
                (
                    int(channel),
                    edge_type.value,
                    int(debounce),
                ),
                "B B B",
            ),
            response_expected=response_expected,
        )

    async def get_edge_count_configuration(self, channel: int) -> GetEdgeCountConfiguration:
        """
        Returns the edge type and debounce time for the selected channel as set by
        :func:`Set Edge Count Configuration`.

        .. note::
         Calling this function is only allowed for channels configured as input.
        """
        assert channel in (0, 1, 2, 3)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT_CONFIGURATION,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )
        edge_type, debounce = unpack_payload(payload, "B B")
        edge_type = EdgeType(edge_type)
        return GetEdgeCountConfiguration(edge_type, debounce)

    async def set_pwm_configuration(
        self,
        channel: int,
        frequency: float | Decimal = 0,
        duty_cycle: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Activates a PWM for the given channel.

        You need to set the channel to output before you call this function, otherwise it will
        report an invalid parameter error. To turn the PWM off again, you can set the frequency to 0 or any other
        function that changes a value of the channel (e.g. :func:`Set Selected Value`).

        A running monoflop timer for the given channel will be aborted if this function
        is called.
        """
        assert channel in (0, 1, 2, 3)
        frequency *= 10
        duty_cycle *= 10000

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PWM_CONFIGURATION,
            data=pack_payload(
                (
                    int(channel),
                    int(frequency),
                    int(duty_cycle),
                ),
                "B I H",
            ),
            response_expected=response_expected,
        )

    async def get_pwm_configuration(self, channel: int) -> GetPWMConfiguration:
        """
        Returns the PWM configuration as set by :func:`Set PWM Configuration`.
        """
        assert channel in (0, 1, 2, 3)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PWM_CONFIGURATION,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )
        frequency, duty_cycle = unpack_payload(payload, "I H")
        return GetPWMConfiguration(Decimal(frequency) / 10, Decimal(duty_cycle) / 10000)

    async def __edge_counter_task(self, channel: int, period: int, value_has_to_change: bool) -> None:
        previous_value: int | None = None
        # Throw away the first value, because we need to reset and sync the internal counter of the IO bricklet.
        try:
            await asyncio.gather(self.get_edge_count(channel, reset_counter=True), asyncio.sleep(period / 1000))
            while "not canceled":
                value, _ = await asyncio.gather(
                    self.get_edge_count(channel, reset_counter=True), asyncio.sleep(period / 1000)
                )
                queue = self.__counter_queue[channel]["queue"]
                if not value_has_to_change or previous_value != value:
                    previous_value = value
                    event = Event(self, sid=channel + 5, function_id=CallbackID.EDGE_COUNT, payload=value)
                    try:
                        queue.put_nowait(event)
                    except asyncio.QueueFull:
                        queue.get_nowait()
                        queue.put_nowait(event)
        except ValueError:
            # raised if the channel is set to output. We will then stop the edge counter callback without notice.
            pass

    async def __read_edge_counter(self, channel: int) -> AsyncGenerator[Event, None]:
        while "not cancelled":
            queue = self.__counter_queue[channel]["queue"]
            yield await queue.get()
            queue.task_done()

    async def __read_callback_events(
        self,
        events: set[_CallbackID],
        sids: tuple[int, ...] | list[int],
    ) -> AsyncGenerator[Event, None]:
        """
        This functions connects to the ip connection and retrieves callback events for a given list of events or sids.
        The callback must be enabled prior to registering to this generator.

        Parameters
        ----------
        events: set of CallbackID
            Any value of CallbackID.INPUT_VALUE, CallbackID.ALL_INPUT_VALUE or CallbackID.MONOFLOP_DONE. Other values
            in the set will be ignored.
        sids: tuple or list of int
            A tuple with ints in range of range(4). Other sids will be ignored.

        Yields
        -------
        Event
            Events matching the desired sid/event filters

        """
        if not events and not sids:
            return

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue

            if function_id is CallbackID.INPUT_VALUE:
                sid, value_has_changed, value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                if function_id in events or sid in sids:
                    yield Event(self, sid, function_id, value, value_has_changed)
                    continue
            elif function_id is CallbackID.MONOFLOP_DONE:
                sid, value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                if function_id in events or sid in sids:
                    yield Event(self, sid, function_id, value)
                    continue
            else:
                changed_sids, values = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                if function_id in events:
                    # Use a special sid for the CallbackID.ALL_INPUT_VALUE, because it returns a tuple
                    yield Event(self, 4, function_id, values, changed_sids)
                else:
                    for sid in sids:
                        yield Event(self, sid, function_id, values[sid], changed_sids[sid])

    async def read_events(
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        assert events is None or sids is None

        sids = tuple() if sids is None else sids

        registered_edge_count_sids = tuple(sid for sid in sids if sid in range(5, 5 + 4))
        registered_callback_events: set[_CallbackID] = set()

        if events:
            for event in events:
                event = self.CallbackID(event)
                # CallbackID.PULSE_COUNT is not a regular callback, so it must be treated special
                if event != CallbackID.EDGE_COUNT:
                    registered_callback_events.add(event)
                else:
                    registered_edge_count_sids = tuple(range(5, 5 + 4))
        registered_callback_sids = tuple(sid for sid in sids if sid in range(5))

        # register all callback events if no specific filter is given
        if not events and not sids:
            registered_callback_events = set(self.CALLBACK_FORMATS.keys())
            registered_edge_count_sids = tuple(range(5, 5 + 4))

        async for res in join(
            self.__read_callback_events(registered_callback_events, registered_callback_sids),
            *(self.__read_edge_counter(sid - 5) for sid in registered_edge_count_sids),
        ):
            yield res
