"""
Module for the Tinkerforge IO-16 Bricklet (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/IO16.html)
implemented using Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, Generator, NamedTuple

from .devices import AdvancedCallbackConfiguration, Device, DeviceIdentifier, Event
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
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


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_PORT = 1
    GET_PORT = 2
    SET_PORT_CONFIGURATION = 3
    GET_PORT_CONFIGURATION = 4
    SET_DEBOUNCE_PERIOD = 5
    GET_DEBOUNCE_PERIOD = 6
    SET_PORT_INTERRUPT = 7
    GET_PORT_INTERRUPT = 8
    SET_PORT_MONOFLOP = 10
    GET_PORT_MONOFLOP = 11
    SET_SELECTED_VALUES = 13
    GET_EDGE_COUNT = 14
    SET_EDGE_COUNT_CONFIG = 15
    GET_EDGE_COUNT_CONFIG = 16


@unique
class Port(Enum):
    """
    There are two ports of 8 pins each
    """

    A = "a"
    B = "b"


_Port = Port  # We need the alias for MyPy type hinting


@unique
class Direction(Enum):
    """
    Configures a pin as input or output
    """

    IN = "i"
    OUT = "o"


_Direction = Direction  # We need the alias for MyPy type hinting


@unique
class InputConfiguration(Enum):
    """
    Enable a pull-up resistor or let the input floating
    """

    PULL_UP = True
    FLOATING = False


_InputConfiguration = InputConfiguration


@unique
class OutputConfiguration(Enum):
    """
    Set the output to low or high
    """

    HIGH = True
    LOW = False


_OutputConfiguration = OutputConfiguration


@unique
class EdgeType(Enum):
    """
    Trigger at a rising or falling edge or both
    """

    RISING = 0
    FALLING = 1
    BOTH = 2


_EdgeType = EdgeType  # We need the alias for MyPy type hinting


class GetPortConfiguration(NamedTuple):
    direction_mask: int
    value_mask: bool


class GetPortMonoflop(NamedTuple):
    value: bool
    time: int
    time_remaining: int


class GetEdgeCountConfiguration(NamedTuple):
    edge_type: EdgeType
    debounce: int


class BrickletIO16(Device):
    """
    16-channel digital input/output
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_IO_16
    DEVICE_DISPLAY_NAME = "IO-16 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    Port = Port
    Direction = Direction
    InputConfiguration = InputConfiguration
    OutputConfiguration = OutputConfiguration
    EdgeType = EdgeType

    CALLBACK_FORMATS = {
        CallbackID.INTERRUPT: "c B B",
        CallbackID.MONOFLOP_DONE: "c B B",
    }

    # Callbacks are by pin
    SID_TO_CALLBACK = {i: (CallbackID.INTERRUPT, CallbackID.MONOFLOP_DONE) for i in range(16)}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def set_port(self, port: _Port | str, value_mask: int, response_expected: bool = True) -> None:
        """
        Sets the output value (high or low) for a port ("a" or "b") with a bitmask (8bit). A 1 in the bitmask means high
         and a 0 in the bitmask means low.

        For example: The value 15 or 0b00001111 will turn the pins 0-3 high and the pins 4-7 low for the specified port.

        All running monoflop timers of the given port will be aborted if this function is called.

        .. note::
         This function does nothing for pins that are configured as input.
         Pull-up resistors can be switched on with :func:`Set Port Configuration`.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())
        assert isinstance(value_mask, int) and (0 <= value_mask <= 255)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PORT,
            data=pack_payload((port.value.encode("ascii"), value_mask), "c B"),
            response_expected=response_expected,
        )

    async def get_port(self, port: _Port | str) -> int:
        """
        Returns a bitmask of the values that are currently measured on the specified port. This function works if the
        pin is configured to input as well as if it is configured to output.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PORT,
            data=pack_payload((port.value.encode("ascii"),), "c"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def set_port_configuration(  # pylint: disable=too-many-arguments
        self,
        port: _Port | str,
        selection_mask: int,
        direction: _Direction | str,
        value: _InputConfiguration | _OutputConfiguration | bool = False,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the value and direction of a specified port. Possible directions are 'i' and 'o' for input and
        output.

        If the direction is configured as output, the value is either high or low (set as *true* or *false*).

        If the direction is configured as input, the value is either pull-up or default (set as *true* or *false*).

        For example:

        * ('a', 255, 'i', true) or ('a', 0b11111111, 'i', true) will set all pins of port A as input pull-up.
        * ('a', 128, 'i', false) or ('a', 0b10000000, 'i', false) will set pin 7 of port A as input default (floating if
         nothing is connected).
        * ('b', 3, 'o', false) or ('b', 0b00000011, 'o', false) will set pins 0 and 1 of port B as output low.
        * ('b', 4, 'o', true) or ('b', 0b00000100, 'o', true) will set pin 2 of port B as output high.

        Running monoflop timers for the selected pins will be aborted if this function is called.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())
        assert isinstance(selection_mask, int) and (0 <= selection_mask <= 255)
        if not isinstance(direction, Direction):
            direction = Direction(direction)

        val = value
        if isinstance(val, (InputConfiguration, OutputConfiguration)):
            val = val.value

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PORT_CONFIGURATION,
            data=pack_payload(
                (port.value.encode("ascii"), selection_mask, direction.value.encode("ascii"), bool(val)), "c B c !"
            ),
            response_expected=response_expected,
        )

    async def get_port_configuration(self, port: _Port | str) -> GetPortConfiguration:
        """
        Returns a direction bitmask and a value bitmask for the specified port. A 1 in the direction bitmask means
        input and a 0 in the bitmask means output.

        For example: A return value of (15, 51) or (0b00001111, 0b00110011) for direction and value means that:

        * pins 0 and 1 are configured as input pull-up,
        * pins 2 and 3 are configured as input default,
        * pins 4 and 5 are configured as output high
        * and pins 6 and 7 are configured as output low.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PORT_CONFIGURATION,
            data=pack_payload((port.value.encode("ascii"),), "c"),
            response_expected=True,
        )
        return GetPortConfiguration(*unpack_payload(payload, "B B"))

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,unused-argument
        self,
        sid: int,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        port = Port.A if sid < 16 else Port.B
        interrupt_mask = await self.get_port_interrupt(port)
        interrupt_mask &= ~(1 << (sid % 16))  # Reset the bit a position sid
        interrupt_mask |= int(bool(period)) << (sid % 16)  # if period is non-zero, enable the interrupt
        await self.set_port_interrupt(port, interrupt_mask)

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        port = Port.A if sid < 16 else Port.B
        interrupt_mask = await self.get_port_interrupt(port)
        value = interrupt_mask & (1 << (sid % 16))
        return AdvancedCallbackConfiguration(int(bool(value)), False, None, None, None)

    async def set_debounce_period(self, debounce_period: int = 100, response_expected: bool = True) -> None:
        """
        Sets the debounce-period of the :cb:`Interrupt` callback.

        For example: If you set this value to 100, you will get the interrupt maximal every 100ms. This is necessary
        if something that bounces is connected to the IO-16 Bricklet such as a button.
        """
        assert debounce_period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((int(debounce_period),), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> int:
        """
        Returns the debounce-period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_port_interrupt(self, port: _Port | str, interrupt_mask: int, response_expected: bool = True) -> None:
        """
        Sets the pins on which an interrupt is activated with a bitmask. Interrupts are triggered on changes of the
        voltage level of the pin, i.e. changes from high to low and low to high.

        For example: ('a', 129) or ('a', 0b10000001) will enable the interrupt for pins 0 and 7 of port A.

        The interrupt is delivered with the :cb:`Interrupt` callback.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())
        assert isinstance(interrupt_mask, int) and (0 <= interrupt_mask <= 255)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PORT_INTERRUPT,
            data=pack_payload((port.value.encode("ascii"), interrupt_mask), "c B"),
            response_expected=response_expected,
        )

    async def get_port_interrupt(self, port: _Port | str) -> int:
        """
        Returns the interrupt bitmask for the specified port as set by :func:`Set Port Interrupt`.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PORT_INTERRUPT,
            data=pack_payload((port.value.encode("ascii"),), "c"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def set_port_monoflop(  # pylint: disable=too-many-arguments
        self, port: _Port | str, selection_mask: int, value_mask: int, time: int, response_expected: bool = True
    ) -> None:
        """
        Configures a monoflop of the pins specified by the second parameter as an 8 bit long bitmask. The specified pins
        must be configured for output. Non-output pins will be ignored.

        The third parameter is a bitmask with the desired value of the specified output pins. A 1 in the bitmask means
        high and a 0 in the bitmask means low.

        The forth parameter indicates the time that the pins should hold the value.

        If this function is called with the parameters ('a', 9, 1, 1500) or ('a', 0b00001001, 0b00000001, 1500): Pin 0
        will get high and pin 3 will get low on port 'a'. In 1.5s pin 0 will get low and pin 3 will get high again.

        A monoflop can be used as a fail-safe mechanism. For example: Lets assume you have a RS485 bus and an IO-16
        Bricklet connected to one of the slave stacks. You can now call this function every second, with a time
        parameter of two seconds and pin 0 set to high. Pin 0 will be high all the time. If now the RS485 connection is
        lost, then pin 0 will get low in at most two seconds.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())
        assert isinstance(selection_mask, int) and (0 <= selection_mask <= 255)
        assert isinstance(value_mask, int) and (0 <= value_mask <= 255)
        assert time >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PORT_MONOFLOP,
            data=pack_payload((port.value.encode("ascii"), selection_mask, value_mask, int(time)), "c B B I"),
            response_expected=response_expected,
        )

    async def get_port_monoflop(self, port: _Port | str, pin: int) -> GetPortMonoflop:
        """
        Returns the interrupt bitmask for the specified port as set by :func:`Set Port Interrupt`.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())
        assert isinstance(pin, int) and (0 <= pin <= 7)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PORT_MONOFLOP,
            data=pack_payload((port.value.encode("ascii"), pin), "c B"),
            response_expected=True,
        )
        return GetPortMonoflop(*unpack_payload(payload, "B I I"))

    async def set_selected_values(
        self, port: _Port | str, selection_mask: int, value_mask: int, response_expected: bool = True
    ) -> None:
        """
        Sets the output value (high or low) for a port ("a" or "b" with a bitmask, according to the selection mask. The
        bitmask is 8 bit long and a 1 in the bitmask means high and a 0 in the bitmask means low.

        For example: The parameters ('a', 192, 128) or ('a', 0b11000000, 0b10000000) will turn pin 7 high and pin 6 low
        on port A, pins 0-6 will remain untouched.

        Running monoflop timers for the selected pins will be aborted if this function is called.

        .. note::
         This function does nothing for pins that are configured as input.
         Pull-up resistors can be switched on with :func:`Set Port Configuration`.
        """
        if not isinstance(port, Port):
            port = Port(port.lower())
        assert isinstance(selection_mask, int) and (0 <= selection_mask <= 255)
        assert isinstance(value_mask, int) and (0 <= value_mask <= 255)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_VALUES,
            data=pack_payload((port.value.encode("ascii"), selection_mask, value_mask), "c B B"),
            response_expected=response_expected,
        )

    async def get_edge_count(self, pin: int, reset_counter: bool = False) -> int:
        """
        Returns the current value of the edge counter for the selected pin on port A. You can configure the edges that
        are counted with :func:`Set Edge Count Config`.

        If you set the reset counter to *true*, the count is set back to 0 directly after it is read.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        assert isinstance(pin, int) and (0 <= pin <= 7)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT,
            data=pack_payload((pin, bool(reset_counter)), "B !"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def set_edge_count_config(
        self,
        pin: int,
        edge_type: _EdgeType | int = EdgeType.RISING,
        debounce: int = 100,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the edge counter for the selected pin of port A. Pins 0 and 1 are available for edge counting.

        The edge type parameter configures if rising edges, falling edges or both are counted if the pin is configured
        for input. Possible edge types are:

        * 0 = rising
        * 1 = falling
        * 2 = both

        Configuring an edge counter resets its value to 0.

        If you don't know what any of this means, just leave it at default. The default configuration is very likely OK
        for you.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        assert isinstance(pin, int) and (0 <= pin <= 1)
        edge_type = EdgeType(edge_type)
        assert 0 <= debounce <= 255

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_COUNT_CONFIG,
            data=pack_payload((pin, edge_type.value, int(debounce)), "B B B"),
            response_expected=response_expected,
        )

    async def get_edge_count_config(self, pin: int) -> GetEdgeCountConfiguration:
        """
        Returns the edge type and debounce time for the selected pin of port A as set by :func:`Set Edge Count Config`.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        assert isinstance(pin, int) and (0 <= pin <= 7)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT_CONFIG,
            data=pack_payload((pin,), "B"),
            response_expected=True,
        )
        edge_type, debounce_time = unpack_payload(payload, "B B")
        edge_type = EdgeType(edge_type)
        return GetEdgeCountConfiguration(edge_type, debounce_time)

    @staticmethod
    def __bits_set(number: int) -> Generator[int, None, None]:
        """
        See https://lemire.me/blog/2018/02/21/iterating-over-set-bits-quickly/ for an explanation how this code
        works.
        """
        while number:
            bit = number & (~number + 1)
            yield bit.bit_length() - 1
            number ^= bit

    async def read_events(  # pylint: disable=too-many-branches
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        assert events is None or sids is None

        registered_events = set()
        if events is not None:
            for event in events:
                registered_events.add(self.CallbackID(event))
        if sids is not None:
            for sid in sids:
                if sid > 15 or sid < 0:
                    raise ValueError("Invalid secondary id. All sids must be in range(16).")
                for callback in self.SID_TO_CALLBACK.get(sid, []):
                    registered_events.add(callback)

        if events is None and sids is None:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue

            if function_id in registered_events:
                port, interrupt_mask, value_mask = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                port = Port(port)
                if port is Port.B:
                    interrupt_mask, value_mask = interrupt_mask << 8, value_mask << 8

                if sids is not None:
                    for sid in self.__bits_set(interrupt_mask):
                        if sid in sids:
                            yield Event(self, sid, function_id, bool(value_mask & (1 << sid)))
                else:
                    # Use a special sid if all channels are returned, because it returns a tuple
                    yield Event(self, 16, function_id, value_mask, interrupt_mask)
