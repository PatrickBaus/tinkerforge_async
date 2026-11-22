"""
Module for the Tinkerforge IO-4 Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IO4_Bricklet_Python.html) implemented using
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

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    INTERRUPT = 9
    MONOFLOP_DONE = 12


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_VALUE = 1
    GET_VALUE = 2
    SET_CONFIGURATION = 3
    GET_CONFIGURATION = 4
    SET_DEBOUNCE_PERIOD = 5
    GET_DEBOUNCE_PERIOD = 6
    SET_INTERRUPT = 7
    GET_INTERRUPT = 8
    SET_MONOFLOP = 10
    GET_MONOFLOP = 11
    SET_SELECTED_VALUES = 13
    GET_EDGE_COUNT = 14
    SET_EDGE_COUNT_CONFIG = 15
    GET_EDGE_COUNT_CONFIG = 16


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
    direction_mask: int
    value_mask: int


class GetMonoflop(NamedTuple):
    value: int
    time: Decimal
    time_remaining: Decimal


class GetEdgeCountConfig(NamedTuple):
    edge_type: EdgeType
    debounce: Decimal


class InterruptEvent(NamedTuple):
    interrupt_mask: int
    value_mask: int


class MonoflopDoneEvent(NamedTuple):
    selection_mask: int
    value_mask: int


class BrickletIO4(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    4-channel digital input/output
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_IO4
    DEVICE_DISPLAY_NAME = "IO-4 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Direction: TypeAlias = Direction
    EdgeType: TypeAlias = EdgeType

    CALLBACK_FORMATS = {
        CallbackID.INTERRUPT: "B B",
        CallbackID.MONOFLOP_DONE: "B B",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.INTERRUPT,)),
        Channel(1, callbacks=(CallbackID.MONOFLOP_DONE,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def set_value(self, value_mask: int, response_expected: bool = True) -> None:
        """
        Sets the output value (high or low) with a bitmask (4bit). A 1 in the bitmask
        means high and a 0 in the bitmask means low.

        For example: The value 3 or 0b0011 will turn the pins 0-1 high and the
        pins 2-3 low.

        All running monoflop timers will be aborted if this function is called.

        .. note::
         This function does nothing for pins that are configured as input.
         Pull-up resistors can be switched on with :func:`set_configuration`.
        """
        value_mask = int(value_mask)
        check_range("value_mask", value_mask, 0, 15)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VALUE,
            data=pack_payload((value_mask,), "B"),
            response_expected=response_expected,
        )

    async def get_value(self) -> int:
        """
        Returns a bitmask of the values that are currently measured.
        This function works if the pin is configured to input
        as well as if it is configured to output.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_configuration(
        self,
        selection_mask: int,
        direction: Direction | str = Direction.IN,
        value: bool = True,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the value and direction of the specified pins. Possible directions
        are 'i' and 'o' for input and output.

        If the direction is configured as output, the value is either high or low
        (set as *true* or *false*).

        If the direction is configured as input, the value is either pull-up or
        default (set as *true* or *false*).

        For example:

        * (15, 'i', true) or (0b1111, 'i', true) will set all pins of as input pull-up.
        * (8, 'i', false) or (0b1000, 'i', false) will set pin 3 of as input default (floating if nothing is connected).
        * (3, 'o', false) or (0b0011, 'o', false) will set pins 0 and 1 as output low.
        * (4, 'o', true) or (0b0100, 'o', true) will set pin 2 of as output high.

        Running monoflop timers for the specified pins will be aborted if this
        function is called.
        """
        selection_mask = int(selection_mask)
        check_range("selection_mask", selection_mask, 0, 15)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((selection_mask, Direction(direction).value, bool(value)), "B c !"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns a value bitmask and a direction bitmask. A 1 in the direction bitmask
        means input and a 0 in the bitmask means output.

        For example: A return value of (3, 5) or (0b0011, 0b0101) for direction and
        value means that:

        * pin 0 is configured as input pull-up,
        * pin 1 is configured as input default,
        * pin 2 is configured as output high and
        * pin 3 is are configured as output low.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        direction_mask, value_mask = unpack_payload(payload, "B B")
        return GetConfiguration(direction_mask, value_mask)

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the debounce period of the :attr:`CallbackID.INTERRUPT` callback.

        For example: If you set this value to 100, you will get the interrupt
        maximal every 100ms. This is necessary if something that bounces is
        connected to the IO-4 Bricklet, such as a button.

        Units: debounce in s.
        """
        debounce_raw = seconds_to_ms(debounce)
        check_range("debounce", debounce_raw, 0, 4294967295, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((debounce_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> Decimal:
        """
        Returns the debounce period as set by :func:`set_debounce_period`.

        Units: debounce in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_interrupt(self, interrupt_mask: int, response_expected: bool = True) -> None:
        """
        Sets the pins on which an interrupt is activated with a bitmask.
        Interrupts are triggered on changes of the voltage level of the pin,
        i.e. changes from high to low and low to high.

        For example: An interrupt bitmask of 10 or 0b1010 will enable the interrupt for
        pins 1 and 3.

        The interrupt is delivered with the :attr:`CallbackID.INTERRUPT` callback.
        """
        interrupt_mask = int(interrupt_mask)
        check_range("interrupt_mask", interrupt_mask, 0, 15)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_INTERRUPT,
            data=pack_payload((interrupt_mask,), "B"),
            response_expected=response_expected,
        )

    async def get_interrupt(self) -> int:
        """
        Returns the interrupt bitmask as set by :func:`set_interrupt`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_INTERRUPT, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_monoflop(
        self, selection_mask: int, value_mask: int, time: Duration, response_expected: bool = True
    ) -> None:
        """
        Configures a monoflop of the pins specified by the first parameter as 4 bit
        long bitmask. The specified pins must be configured for output. Non-output
        pins will be ignored.

        The second parameter is a bitmask with the desired value of the specified
        output pins. A 1 in the bitmask means high and a 0 in the bitmask means low.

        The third parameter indicates the time that the pins should hold
        the value.

        If this function is called with the parameters (9, 1, 1500) or
        (0b1001, 0b0001, 1500): Pin 0 will get high and pin 3 will get low. In 1.5s pin
        0 will get low and pin 3 will get high again.

        A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
        have a RS485 bus and an IO-4 Bricklet connected to one of the slave
        stacks. You can now call this function every second, with a time parameter
        of two seconds and pin 0 set to high. Pin 0 will be high all the time. If now
        the RS485 connection is lost, then pin 0 will get low in at most two seconds.

        Units: time in s.

        .. versionadded:: 1.1.1 (Firmware)
        """
        selection_mask = int(selection_mask)
        check_range("selection_mask", selection_mask, 0, 15)
        value_mask = int(value_mask)
        check_range("value_mask", value_mask, 0, 15)
        time_raw = seconds_to_ms(time)
        check_range("time", time_raw, 0, 4294967295, time)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MONOFLOP,
            data=pack_payload((selection_mask, value_mask, time_raw), "B B I"),
            response_expected=response_expected,
        )

    async def get_monoflop(self, pin: int) -> GetMonoflop:
        """
        Returns (for the given pin) the current value and the time as set by
        :func:`set_monoflop` as well as the remaining time until the value flips.

        If the timer is not running currently, the remaining time will be returned
        as 0.

        Units: time in s, time_remaining in s.

        .. versionadded:: 1.1.1 (Firmware)
        """
        pin = int(pin)
        check_range("pin", pin, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MONOFLOP, data=pack_payload((pin,), "B"), response_expected=True
        )
        value, time, time_remaining = unpack_payload(payload, "B I I")
        return GetMonoflop(value, ms_to_seconds(time), ms_to_seconds(time_remaining))

    async def set_selected_values(self, selection_mask: int, value_mask: int, response_expected: bool = True) -> None:
        """
        Sets the output value (high or low) with a bitmask, according to
        the selection mask. The bitmask is 4 bit long, *true* refers to high
        and *false* refers to low.

        For example: The parameters (9, 4) or (0b0110, 0b0100) will turn
        pin 1 low and pin 2 high, pin 0 and 3 will remain untouched.

        Running monoflop timers for the selected pins will be aborted if this
        function is called.

        .. note::
         This function does nothing for pins that are configured as input.
         Pull-up resistors can be switched on with :func:`set_configuration`.
        """
        selection_mask = int(selection_mask)
        check_range("selection_mask", selection_mask, 0, 15)
        value_mask = int(value_mask)
        check_range("value_mask", value_mask, 0, 15)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_VALUES,
            data=pack_payload((selection_mask, value_mask), "B B"),
            response_expected=response_expected,
        )

    async def get_edge_count(self, pin: int, reset_counter: bool) -> int:
        """
        Returns the current value of the edge counter for the selected pin. You can
        configure the edges that are counted with :func:`set_edge_count_config`.

        If you set the reset counter to *true*, the count is set back to 0
        directly after it is read.

        .. versionadded:: 2.0.1 (Firmware)
        """
        pin = int(pin)
        check_range("pin", pin, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT,
            data=pack_payload((pin, bool(reset_counter)), "B !"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def set_edge_count_config(
        self,
        selection_mask: int,
        edge_type: EdgeType | int = EdgeType.RISING,
        debounce: Duration = Decimal("0.1"),
        response_expected: bool = True,
    ) -> None:
        """
        Configures the edge counter for the selected pins.

        The edge type parameter configures if rising edges, falling edges or
        both are counted if the pin is configured for input. Possible edge types are:

        * 0 = rising (default)
        * 1 = falling
        * 2 = both

        Configuring an edge counter resets its value to 0.

        If you don't know what any of this means, just leave it at default. The
        default configuration is very likely OK for you.

        Units: debounce in s.

        .. versionadded:: 2.0.1 (Firmware)
        """
        selection_mask = int(selection_mask)
        check_range("selection_mask", selection_mask, 0, 15)
        debounce_raw = seconds_to_ms(debounce)
        check_range("debounce", debounce_raw, 0, 255, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_COUNT_CONFIG,
            data=pack_payload((selection_mask, EdgeType(edge_type).value, debounce_raw), "B B B"),
            response_expected=response_expected,
        )

    async def get_edge_count_config(self, pin: int) -> GetEdgeCountConfig:
        """
        Returns the edge type and debounce time for the selected pin as set by
        :func:`set_edge_count_config`.

        Units: debounce in s.

        .. versionadded:: 2.0.1 (Firmware)
        """
        pin = int(pin)
        check_range("pin", pin, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT_CONFIG,
            data=pack_payload((pin,), "B"),
            response_expected=True,
        )
        edge_type, debounce = unpack_payload(payload, "B B")
        return GetEdgeCountConfig(EdgeType(edge_type), ms_to_seconds(debounce))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.INTERRUPT:
            interrupt_mask, value_mask = value
            return 0, InterruptEvent(interrupt_mask, value_mask)
        selection_mask, value_mask = value
        return 1, MonoflopDoneEvent(selection_mask, value_mask)
