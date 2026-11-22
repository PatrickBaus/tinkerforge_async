"""
Module for the Tinkerforge Industrial Quad Relay Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialQuadRelay_Bricklet_Python.html) implemented using
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

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
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
    SET_GROUP = 5
    GET_GROUP = 6
    GET_AVAILABLE_FOR_GROUP = 7
    SET_SELECTED_VALUES = 9


class GetMonoflop(NamedTuple):
    value: int
    time: Decimal
    time_remaining: Decimal


class MonoflopDoneEvent(NamedTuple):
    selection_mask: int
    value_mask: int


class BrickletIndustrialQuadRelay(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    4 galvanically isolated solid state relays
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_QUAD_RELAY
    DEVICE_DISPLAY_NAME = "Industrial Quad Relay Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.MONOFLOP_DONE: "H H",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.MONOFLOP_DONE,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_value(self, value_mask: int, response_expected: bool = True) -> None:
        """
        Sets the output value with a bitmask (16bit). A 1 in the bitmask means relay
        closed and a 0 means relay open.

        For example: The value 3 or 0b0011 will close the relay of pins 0-1 and open
        the other pins.

        If no groups are used (see :func:`set_group`), the pins correspond to the
        markings on the Industrial Quad Relay Bricklet.

        If groups are used, the pins correspond to the element in the group.
        Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
        pins 8-11 and element 4 pins 12-15.

        All running monoflop timers will be aborted if this function is called.
        """
        value_mask = int(value_mask)
        check_range("value_mask", value_mask, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VALUE,
            data=pack_payload((value_mask,), "H"),
            response_expected=response_expected,
        )

    async def get_value(self) -> int:
        """
        Returns the bitmask as set by :func:`set_value`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_monoflop(
        self, selection_mask: int, value_mask: int, time: Duration, response_expected: bool = True
    ) -> None:
        """
        Configures a monoflop of the pins specified by the first parameter
        bitmask.

        The second parameter is a bitmask with the desired value of the specified
        pins. A 1 in the bitmask means relay closed and a 0 means relay open.

        The third parameter indicates the time that the pins should hold
        the value.

        If this function is called with the parameters (9, 1, 1500) or
        (0b1001, 0b0001, 1500): Pin 0 will close and pin 3 will open. In 1.5s pin 0
        will open and pin 3 will close again.

        A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
        have a RS485 bus and a Quad Relay Bricklet connected to one of the slave
        stacks. You can now call this function every second, with a time parameter
        of two seconds and pin 0 closed. Pin 0 will be closed all the time. If now
        the RS485 connection is lost, then pin 0 will be opened in at most two seconds.

        Units: time in s.
        """
        selection_mask = int(selection_mask)
        check_range("selection_mask", selection_mask, 0, 65535)
        value_mask = int(value_mask)
        check_range("value_mask", value_mask, 0, 65535)
        time_raw = seconds_to_ms(time)
        check_range("time", time_raw, 0, 4294967295, time)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MONOFLOP,
            data=pack_payload((selection_mask, value_mask, time_raw), "H H I"),
            response_expected=response_expected,
        )

    async def get_monoflop(self, pin: int) -> GetMonoflop:
        """
        Returns (for the given pin) the current value and the time as set by
        :func:`set_monoflop` as well as the remaining time until the value flips.

        If the timer is not running currently, the remaining time will be returned
        as 0.

        Units: time in s, time_remaining in s.
        """
        pin = int(pin)
        check_range("pin", pin, 0, 15)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MONOFLOP, data=pack_payload((pin,), "B"), response_expected=True
        )
        value, time, time_remaining = unpack_payload(payload, "H I I")
        return GetMonoflop(value, ms_to_seconds(time), ms_to_seconds(time_remaining))

    async def set_group(self, group: str | Sequence[str], response_expected: bool = True) -> None:
        """
        Sets a group of Quad Relay Bricklets that should work together. You can
        find Bricklets that can be grouped together with :func:`get_available_for_group`.

        The group consists of 4 elements. Element 1 in the group will get pins 0-3,
        element 2 pins 4-7, element 3 pins 8-11 and element 4 pins 12-15.

        Each element can either be one of the ports ('a' to 'd') or 'n' if it should
        not be used.

        For example: If you have two Quad Relay Bricklets connected to port A and
        port B respectively, you could call with |abnn|.

        Now the pins on the Quad Relay on port A are assigned to 0-3 and the
        pins on the Quad Relay on port B are assigned to 4-7. It is now possible
        to call :func:`set_value` and control two Bricklets at the same time.
        """
        check_length("group", group, 4)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GROUP,
            data=pack_payload((list(group),), "4c"),
            response_expected=response_expected,
        )

    async def get_group(self) -> tuple[str, ...]:
        """
        Returns the group as set by :func:`set_group`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GROUP, response_expected=True
        )
        return tuple(unpack_payload(payload, "4c"))

    async def get_available_for_group(self) -> int:
        """
        Returns a bitmask of ports that are available for grouping. For example the
        value 5 or 0b0101 means: Port A and port C are connected to Bricklets that
        can be grouped together.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AVAILABLE_FOR_GROUP, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_selected_values(self, selection_mask: int, value_mask: int, response_expected: bool = True) -> None:
        """
        Sets the output value with a bitmask, according to the selection mask.
        The bitmask is 16 bit long, *true* refers to a closed relay and
        *false* refers to an open relay.

        For example: The values (3, 1) or (0b0011, 0b0001) will close the relay of
        pin 0, open the relay of pin 1 and leave the others untouched.

        If no groups are used (see :func:`set_group`), the pins correspond to the
        markings on the Industrial Quad Relay Bricklet.

        If groups are used, the pins correspond to the element in the group.
        Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
        pins 8-11 and element 4 pins 12-15.

        Running monoflop timers for the selected relays will be aborted if this function
        is called.
        """
        selection_mask = int(selection_mask)
        check_range("selection_mask", selection_mask, 0, 65535)
        value_mask = int(value_mask)
        check_range("value_mask", value_mask, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_VALUES,
            data=pack_payload((selection_mask, value_mask), "H H"),
            response_expected=response_expected,
        )

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        selection_mask, value_mask = value
        return 0, MonoflopDoneEvent(selection_mask, value_mask)
