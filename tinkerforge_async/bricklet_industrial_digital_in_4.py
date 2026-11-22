"""
Module for the Tinkerforge Industrial Digital In 4 Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDigitalIn4_Bricklet_Python.html) implemented using
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

    INTERRUPT = 9


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_VALUE = 1
    SET_GROUP = 2
    GET_GROUP = 3
    GET_AVAILABLE_FOR_GROUP = 4
    SET_DEBOUNCE_PERIOD = 5
    GET_DEBOUNCE_PERIOD = 6
    SET_INTERRUPT = 7
    GET_INTERRUPT = 8
    GET_EDGE_COUNT = 10
    SET_EDGE_COUNT_CONFIG = 11
    GET_EDGE_COUNT_CONFIG = 12


@unique
class EdgeType(Enum):
    """
    The edge type options
    """

    RISING = 0
    FALLING = 1
    BOTH = 2


class GetEdgeCountConfig(NamedTuple):
    edge_type: EdgeType
    debounce: Decimal


class InterruptEvent(NamedTuple):
    interrupt_mask: int
    value_mask: int


class BrickletIndustrialDigitalIn4(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    4 galvanically isolated digital inputs
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_DIGITAL_IN_4
    DEVICE_DISPLAY_NAME = "Industrial Digital In 4 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    EdgeType: TypeAlias = EdgeType

    CALLBACK_FORMATS = {
        CallbackID.INTERRUPT: "H H",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.INTERRUPT,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self) -> int:
        """
        Returns the input value with a bitmask. The bitmask is 16bit long, *true*
        refers to high and *false* refers to low.

        For example: The value 3 or 0b0011 means that pins 0-1 are high and the other
        pins are low.

        If no groups are used (see :func:`set_group`), the pins correspond to the
        markings on the IndustrialDigital In 4 Bricklet.

        If groups are used, the pins correspond to the element in the group.
        Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
        pins 8-11 and element 4 pins 12-15.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_group(self, group: str | Sequence[str], response_expected: bool = True) -> None:
        """
        Sets a group of Digital In 4 Bricklets that should work together. You can
        find Bricklets that can be grouped together with :func:`get_available_for_group`.

        The group consists of 4 elements. Element 1 in the group will get pins 0-3,
        element 2 pins 4-7, element 3 pins 8-11 and element 4 pins 12-15.

        Each element can either be one of the ports ('a' to 'd') or 'n' if it should
        not be used.

        For example: If you have two Digital In 4 Bricklets connected to port A and
        port B respectively, you could call with |abnn|.

        Now the pins on the Digital In 4 on port A are assigned to 0-3 and the
        pins on the Digital In 4 on port B are assigned to 4-7. It is now possible
        to call :func:`get_value` and read out two Bricklets at the same time.

        Changing the group configuration resets all edge counter configurations
        and values.
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

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the debounce period of the :attr:`CallbackID.INTERRUPT` callback.

        For example: If you set this value to 100, you will get the interrupt
        maximal every 100ms. This is necessary if something that bounces is
        connected to the Digital In 4 Bricklet, such as a button.

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

        For example: An interrupt bitmask of 9 or 0b1001 will enable the interrupt for
        pins 0 and 3.

        The interrupts use the grouping as set by :func:`set_group`.

        The interrupt is delivered with the :attr:`CallbackID.INTERRUPT` callback.
        """
        interrupt_mask = int(interrupt_mask)
        check_range("interrupt_mask", interrupt_mask, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_INTERRUPT,
            data=pack_payload((interrupt_mask,), "H"),
            response_expected=response_expected,
        )

    async def get_interrupt(self) -> int:
        """
        Returns the interrupt bitmask as set by :func:`set_interrupt`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_INTERRUPT, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def get_edge_count(self, pin: int, reset_counter: bool) -> int:
        """
        Returns the current value of the edge counter for the selected pin. You can
        configure the edges that are counted with :func:`set_edge_count_config`.

        If you set the reset counter to *true*, the count is set back to 0
        directly after it is read.

        The edge counters use the grouping as set by :func:`set_group`.

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
        Configures the edge counter for the selected pins. A bitmask of 9 or 0b1001 will
        enable the edge counter for pins 0 and 3.

        The edge type parameter configures if rising edges, falling edges or
        both are counted if the pin is configured for input. Possible edge types are:

        * 0 = rising
        * 1 = falling
        * 2 = both

        Configuring an edge counter resets its value to 0.

        If you don't know what any of this means, just leave it at default. The
        default configuration is very likely OK for you.

        The edge counters use the grouping as set by :func:`set_group`.

        Units: debounce in s.

        .. versionadded:: 2.0.1 (Firmware)
        """
        selection_mask = int(selection_mask)
        check_range("selection_mask", selection_mask, 0, 65535)
        debounce_raw = seconds_to_ms(debounce)
        check_range("debounce", debounce_raw, 0, 255, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_COUNT_CONFIG,
            data=pack_payload((selection_mask, EdgeType(edge_type).value, debounce_raw), "H B B"),
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
        check_range("pin", pin, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT_CONFIG,
            data=pack_payload((pin,), "B"),
            response_expected=True,
        )
        edge_type, debounce = unpack_payload(payload, "B B")
        return GetEdgeCountConfig(EdgeType(edge_type), ms_to_seconds(debounce))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        interrupt_mask, value_mask = value
        return 0, InterruptEvent(interrupt_mask, value_mask)
