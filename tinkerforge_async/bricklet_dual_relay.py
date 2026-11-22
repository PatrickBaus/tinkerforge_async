"""
Module for the Tinkerforge Dual Relay Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DualRelay_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

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

    MONOFLOP_DONE = 5


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_STATE = 1
    GET_STATE = 2
    SET_MONOFLOP = 3
    GET_MONOFLOP = 4
    SET_SELECTED_STATE = 6


class GetState(NamedTuple):
    relay1: bool
    relay2: bool


class GetMonoflop(NamedTuple):
    state: bool
    time: Decimal
    time_remaining: Decimal


class MonoflopDoneEvent(NamedTuple):
    relay: int
    state: bool


class BrickletDualRelay(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Two relays to switch AC/DC devices
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DUAL_RELAY
    DEVICE_DISPLAY_NAME = "Dual Relay Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.MONOFLOP_DONE: "B !",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.MONOFLOP_DONE,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_state(self, relay1: bool = False, relay2: bool = False, response_expected: bool = True) -> None:
        """
        Sets the state of the relays, *true* means on and *false* means off.
        For example: (true, false) turns relay 1 on and relay 2 off.

        If you just want to set one of the relays and don't know the current state
        of the other relay, you can get the state with :func:`get_state` or you
        can use :func:`set_selected_state`.

        All running monoflop timers will be aborted if this function is called.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STATE,
            data=pack_payload((bool(relay1), bool(relay2)), "! !"),
            response_expected=response_expected,
        )

    async def get_state(self) -> GetState:
        """
        Returns the state of the relays, *true* means on and *false* means off.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATE, response_expected=True
        )
        relay1, relay2 = unpack_payload(payload, "! !")
        return GetState(relay1, relay2)

    async def set_monoflop(self, relay: int, state: bool, time: Duration, response_expected: bool = True) -> None:
        """
        The first parameter can be 1 or 2 (relay 1 or relay 2). The second parameter
        is the desired state of the relay (*true* means on and *false* means off).
        The third parameter indicates the time that the relay should hold
        the state.

        If this function is called with the parameters (1, true, 1500):
        Relay 1 will turn on and in 1.5s it will turn off again.

        A monoflop can be used as a failsafe mechanism. For example: Lets assume you
        have a RS485 bus and a Dual Relay Bricklet connected to one of the slave
        stacks. You can now call this function every second, with a time parameter
        of two seconds. The relay will be on all the time. If now the RS485
        connection is lost, the relay will turn off in at most two seconds.

        Units: time in s.

        .. versionadded:: 1.1.1 (Firmware)
        """
        relay = int(relay)
        check_range("relay", relay, 1, 2)
        time_raw = seconds_to_ms(time)
        check_range("time", time_raw, 0, 4294967295, time)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MONOFLOP,
            data=pack_payload((relay, bool(state), time_raw), "B ! I"),
            response_expected=response_expected,
        )

    async def get_monoflop(self, relay: int) -> GetMonoflop:
        """
        Returns (for the given relay) the current state and the time as set by
        :func:`set_monoflop` as well as the remaining time until the state flips.

        If the timer is not running currently, the remaining time will be returned
        as 0.

        Units: time in s, time_remaining in s.

        .. versionadded:: 1.1.1 (Firmware)
        """
        relay = int(relay)
        check_range("relay", relay, 1, 2)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MONOFLOP, data=pack_payload((relay,), "B"), response_expected=True
        )
        state, time, time_remaining = unpack_payload(payload, "! I I")
        return GetMonoflop(state, ms_to_seconds(time), ms_to_seconds(time_remaining))

    async def set_selected_state(self, relay: int, state: bool, response_expected: bool = True) -> None:
        """
        Sets the state of the selected relay (1 or 2), *true* means on and *false* means off.

        A running monoflop timer for the selected relay will be aborted if this function is called.

        The other relay remains untouched.
        """
        relay = int(relay)
        check_range("relay", relay, 1, 2)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_STATE,
            data=pack_payload((relay, bool(state)), "B !"),
            response_expected=response_expected,
        )

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        relay, state = value
        return 0, MonoflopDoneEvent(relay, state)
