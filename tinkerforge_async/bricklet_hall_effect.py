"""
Module for the Tinkerforge Hall Effect Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/HallEffect_Bricklet_Python.html) implemented using
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

    EDGE_COUNT = 10


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_VALUE = 1
    GET_EDGE_COUNT = 2
    SET_EDGE_COUNT_CONFIG = 3
    GET_EDGE_COUNT_CONFIG = 4
    SET_EDGE_INTERRUPT = 5
    GET_EDGE_INTERRUPT = 6
    SET_EDGE_COUNT_CALLBACK_PERIOD = 7
    GET_EDGE_COUNT_CALLBACK_PERIOD = 8
    EDGE_INTERRUPT = 9


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


class EdgeInterrupt(NamedTuple):
    count_: int
    value: bool


class BrickletHallEffect(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Detects presence of magnetic field
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_HALL_EFFECT
    DEVICE_DISPLAY_NAME = "Hall Effect Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    EdgeType: TypeAlias = EdgeType

    CALLBACK_FORMATS = {
        CallbackID.EDGE_COUNT: "I !",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.EDGE_COUNT,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self) -> bool:
        """
        Returns *true* if a magnetic field of 3.5 millitesla or greater is detected.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def get_edge_count(self, reset_counter: bool) -> int:
        """
        Returns the current value of the edge counter. You can configure
        edge type (rising, falling, both) that is counted with
        :func:`set_edge_count_config`.

        If you set the reset counter to *true*, the count is set back to 0
        directly after it is read.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT,
            data=pack_payload((bool(reset_counter),), "!"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def set_edge_count_config(
        self,
        edge_type: EdgeType | int = EdgeType.RISING,
        debounce: Duration = Decimal("0.1"),
        response_expected: bool = True,
    ) -> None:
        """
        The edge type parameter configures if rising edges, falling edges or
        both are counted. Possible edge types are:

        * 0 = rising
        * 1 = falling
        * 2 = both

        A magnetic field of 3.5 millitesla or greater causes a falling edge and a
        magnetic field of 2.5 millitesla or smaller causes a rising edge.

        If a magnet comes near the Bricklet the signal goes low (falling edge), if
        a magnet is removed from the vicinity the signal goes high (rising edge).

        Configuring an edge counter resets its value to 0.

        If you don't know what any of this means, just leave it at default. The
        default configuration is very likely OK for you.

        Units: debounce in s.
        """
        debounce_raw = seconds_to_ms(debounce)
        check_range("debounce", debounce_raw, 0, 255, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_COUNT_CONFIG,
            data=pack_payload((EdgeType(edge_type).value, debounce_raw), "B B"),
            response_expected=response_expected,
        )

    async def get_edge_count_config(self) -> GetEdgeCountConfig:
        """
        Returns the edge type and debounce time as set by :func:`set_edge_count_config`.

        Units: debounce in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_EDGE_COUNT_CONFIG, response_expected=True
        )
        edge_type, debounce = unpack_payload(payload, "B B")
        return GetEdgeCountConfig(EdgeType(edge_type), ms_to_seconds(debounce))

    async def set_edge_interrupt(self, edges: int = 0, response_expected: bool = True) -> None:
        """
        Sets the number of edges until an interrupt is invoked.

        If *edges* is set to n, an interrupt is invoked for every n-th detected edge.

        If *edges* is set to 0, the interrupt is disabled.
        """
        edges = int(edges)
        check_range("edges", edges, 0, 4294967295)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_INTERRUPT,
            data=pack_payload((edges,), "I"),
            response_expected=response_expected,
        )

    async def get_edge_interrupt(self) -> int:
        """
        Returns the edges as set by :func:`set_edge_interrupt`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_EDGE_INTERRUPT, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_edge_count_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.EDGE_COUNT` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.EDGE_COUNT` callback is only triggered if the edge count has changed
        since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_COUNT_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_edge_count_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_edge_count_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_EDGE_COUNT_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def edge_interrupt(self) -> EdgeInterrupt:
        """
        This callback is triggered every n-th count, as configured with
        :func:`set_edge_interrupt`. The parameters are the
        current count and the current value (see :func:`get_value` and
        :func:`get_edge_count`).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.EDGE_INTERRUPT, response_expected=True
        )
        count, value = unpack_payload(payload, "I !")
        return EdgeInterrupt(count, value)

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        count, value = value
        return 0, EdgeInterrupt(count, value)
