# -*- coding: utf-8 -*-
from collections import namedtuple
from enum import Enum, unique

from .devices import DeviceIdentifier, Device
from .ip_connection_helper import pack_payload, unpack_payload

GetPortConfiguration = namedtuple('PortConfiguration', ['direction_mask', 'value_mask'])
GetPortMonoflop = namedtuple('PortMonoflop', ['value', 'time', 'time_remaining'])
GetEdgeCountConfig = namedtuple('EdgeCountConfig', ['edge_type', 'debounce'])


@unique
class CallbackID(Enum):
    INTERRUPT = 9
    MONOFLOP_DONE = 12


@unique
class FunctionID(Enum):
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
    A = 'a'
    B = 'b'


@unique
class Direction(Enum):
    IN = 'i'
    OUT = 'o'


@unique
class InputConfiguration(Enum):
    PULL_UP = True
    FLOATING = False


@unique
class OutputConfiguration(Enum):
    HIGH = True
    LOW = False


@unique
class EdgeType(Enum):
    RISING = 0
    FALLING = 1
    BOTH = 2


class BrickletIO16(Device):
    """
    16-channel digital input/output
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletIO16
    DEVICE_DISPLAY_NAME = 'IO-16 Bricklet'

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    Port = Port
    Direction = Direction
    InputConfiguration = InputConfiguration
    OutputConfiguration = OutputConfiguration
    EdgeType = EdgeType

    CALLBACK_FORMATS = {
        CallbackID.INTERRUPT: 'c B B',
        CallbackID.MONOFLOP_DONE: 'c B B',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(uid, ipcon)

        self.api_version = (2, 0, 1)

    async def set_port(self, port, value_mask, response_expected=True):
        """
        Sets the output value (high or low) for a port ("a" or "b") with a bitmask
        (8bit). A 1 in the bitmask means high and a 0 in the bitmask means low.

        For example: The value 15 or 0b00001111 will turn the pins 0-3 high and the
        pins 4-7 low for the specified port.

        All running monoflop timers of the given port will be aborted if this function
        is called.

        .. note::
         This function does nothing for pins that are configured as input.
         Pull-up resistors can be switched on with :func:`Set Port Configuration`.
        """
        if not type(port) is Port:
            port = Port(port.lower())
        assert (isinstance(value_mask, int) and (0 <= value_mask <= 255))

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PORT,
            data=pack_payload((port.value.encode('ascii'), value_mask), 'c B'),
            response_expected=response_expected,
        )

    async def get_port(self, port):
        """
        Returns a bitmask of the values that are currently measured on the
        specified port. This function works if the pin is configured to input
        as well as if it is configured to output.
        """
        if not type(port) is Port:
            port = Port(port.lower())

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PORT,
            data=pack_payload((port.value.encode('ascii'),), 'c'),
            response_expected=True
        )
        return unpack_payload(payload, 'B')

    async def set_port_configuration(self, port, selection_mask, direction, value=False, response_expected=True):
        """
        Configures the value and direction of a specified port. Possible directions
        are 'i' and 'o' for input and output.

        If the direction is configured as output, the value is either high or low
        (set as *true* or *false*).

        If the direction is configured as input, the value is either pull-up or
        default (set as *true* or *false*).

        For example:

        * ('a', 255, 'i', true) or ('a', 0b11111111, 'i', true) will set all pins of port A as input pull-up.
        * ('a', 128, 'i', false) or ('a', 0b10000000, 'i', false) will set pin 7 of port A as input default (floating if nothing is connected).
        * ('b', 3, 'o', false) or ('b', 0b00000011, 'o', false) will set pins 0 and 1 of port B as output low.
        * ('b', 4, 'o', true) or ('b', 0b00000100, 'o', true) will set pin 2 of port B as output high.

        Running monoflop timers for the selected pins will be aborted if this
        function is called.
        """
        if not type(port) is Port:
            port = Port(port.lower())
        assert (isinstance(selection_mask, int) and (0 <= selection_mask <= 255))
        if not type(direction) is Direction:
            direction = Direction(direction)

        val = value
        if (type(val) is InputConfiguration or type(val) is OutputConfiguration):
            val = val.value

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PORT_CONFIGURATION,
            data=pack_payload(
              (
                port.value.encode('ascii'),
                selection_mask,
                direction.value.encode('ascii'),
                bool(val)
              ), 'c B c !'),
            response_expected=response_expected,
        )

    async def get_port_configuration(self, port):
        """
        Returns a direction bitmask and a value bitmask for the specified port. A 1 in
        the direction bitmask means input and a 0 in the bitmask means output.

        For example: A return value of (15, 51) or (0b00001111, 0b00110011) for
        direction and value means that:

        * pins 0 and 1 are configured as input pull-up,
        * pins 2 and 3 are configured as input default,
        * pins 4 and 5 are configured as output high
        * and pins 6 and 7 are configured as output low.
        """
        if not type(port) is Port:
            port = Port(port.lower())

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PORT_CONFIGURATION,
            data=pack_payload((port.value.encode('ascii'),), 'c'),
            response_expected=True
        )
        return GetPortConfiguration(*unpack_payload(payload, 'B B'))

    async def set_debounce_period(self, debounce_period=100, response_expected=True):
        """
        Sets the debounce period of the :cb:`Interrupt` callback.

        For example: If you set this value to 100, you will get the interrupt
        maximal every 100ms. This is necessary if something that bounces is
        connected to the IO-16 Bricklet, such as a button.
        """
        assert debounce_period >= 0

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((int(debounce_period),), 'I'),
            response_expected=response_expected
        )

    async def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_DEBOUNCE_PERIOD,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_port_interrupt(self, port, interrupt_mask, response_expected=True):
        """
        Sets the pins on which an interrupt is activated with a bitmask.
        Interrupts are triggered on changes of the voltage level of the pin,
        i.e. changes from high to low and low to high.

        For example: ('a', 129) or ('a', 0b10000001) will enable the interrupt for
        pins 0 and 7 of port a.

        The interrupt is delivered with the :cb:`Interrupt` callback.
        """
        if not type(port) is Port:
            port = Port(port.lower())
        assert (isinstance(interrupt_mask, int) and (0 <= interrupt_mask <= 255))

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PORT_INTERRUPT,
            data=pack_payload((port.value.encode('ascii'), interrupt_mask), 'c B'),
            response_expected=response_expected
        )

    async def get_port_interrupt(self, port):
        """
        Returns the interrupt bitmask for the specified port as set by
        :func:`Set Port Interrupt`.
        """
        if not type(port) is Port:
            port = Port(port.lower())

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PORT_INTERRUPT,
            data=pack_payload((port.value.encode('ascii'),), 'c'),
            response_expected=True
        )
        return unpack_payload(payload, 'B')

    async def set_port_monoflop(self, port, selection_mask, value_mask, time, response_expected=True):
        """
        Configures a monoflop of the pins specified by the second parameter as 8 bit
        long bitmask. The specified pins must be configured for output. Non-output
        pins will be ignored.

        The third parameter is a bitmask with the desired value of the specified
        output pins. A 1 in the bitmask means high and a 0 in the bitmask means low.

        The forth parameter indicates the time that the pins should hold
        the value.

        If this function is called with the parameters ('a', 9, 1, 1500) or
        ('a', 0b00001001, 0b00000001, 1500): Pin 0 will get high and pin 3 will get
        low on port 'a'. In 1.5s pin 0 will get low and pin 3 will get high again.

        A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
        have a RS485 bus and an IO-16 Bricklet connected to one of the slave
        stacks. You can now call this function every second, with a time parameter
        of two seconds and pin 0 set to high. Pin 0 will be high all the time. If now
        the RS485 connection is lost, then pin 0 will get low in at most two seconds.
        """
        if not type(port) is Port:
            port = Port(port.lower())
        assert (isinstance(selection_mask, int) and (0 <= selection_mask <= 255))
        assert (isinstance(value_mask, int) and (0 <= value_mask <= 255))
        assert time >= 0

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PORT_MONOFLOP,
            data=pack_payload(
              (
                port.value.encode('ascii'),
                selection_mask,
                value_mask,
                int(time)
              ), 'c B B I'),
            response_expected=response_expected
        )

    async def get_port_monoflop(self, port, pin):
        """
        Returns the interrupt bitmask for the specified port as set by
        :func:`Set Port Interrupt`.
        """
        if not type(port) is Port:
            port = Port(port.lower())
        assert (isinstance(pin, int) and (0 <= pin <= 7))

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PORT_MONOFLOP,
            data=pack_payload((port.value.encode('ascii'), pin), 'c B'),
            response_expected=True
        )
        return GetPortMonoflop(*unpack_payload(payload, 'B I I'))

    async def set_selected_values(self, port, selection_mask, value_mask, response_expected=True):
        """
        Sets the output value (high or low) for a port ("a" or "b" with a bitmask,
        according to the selection mask. The bitmask is 8 bit long and a 1 in the
        bitmask means high and a 0 in the bitmask means low.

        For example: The parameters ('a', 192, 128) or ('a', 0b11000000, 0b10000000)
        will turn pin 7 high and pin 6 low on port A, pins 0-6 will remain untouched.

        Running monoflop timers for the selected pins will be aborted if this
        function is called.

        .. note::
         This function does nothing for pins that are configured as input.
         Pull-up resistors can be switched on with :func:`Set Port Configuration`.
        """
        if not type(port) is Port:
            port = Port(port.lower())
        assert (isinstance(selection_mask, int) and (0 <= selection_mask <= 255))
        assert (isinstance(value_mask, int) and (0 <= value_mask <= 255))

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_VALUES,
            data=pack_payload(
              (
                port.value.encode('ascii'),
                selection_mask,
                value_mask
              ), 'c B B'),
            response_expected=response_expected
        )

    async def get_edge_count(self, pin, reset_counter=False):
        """
        Returns the current value of the edge counter for the selected pin on port A.
        You can configure the edges that are counted with :func:`Set Edge Count Config`.

        If you set the reset counter to *true*, the count is set back to 0
        directly after it is read.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        assert (isinstance(pin, int) and (0 <= pin <= 7))

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT,
            data=pack_payload((pin, bool(reset_counter)), 'B !'),
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_edge_count_config(self, pin, edge_type=EdgeType.RISING, debounce=100, response_expected=True):
        """
        Configures the edge counter for the selected pin of port A. Pins 0 and 1
        are available for edge counting.

        The edge type parameter configures if rising edges, falling edges or
        both are counted if the pin is configured for input. Possible edge types are:

        * 0 = rising
        * 1 = falling
        * 2 = both

        Configuring an edge counter resets its value to 0.

        If you don't know what any of this means, just leave it at default. The
        default configuration is very likely OK for you.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        assert (isinstance(pin, int) and (0 <= pin <= 1))
        if not type(edge_type) is EdgeType:
            edge_type = EdgeType(edge_type)
        assert (0 <= debounce <= 255)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EDGE_COUNT_CONFIG,
            data=pack_payload(
              (
                pin,
                edge_type.value,
                int(debounce)
              ), 'B B B'),
            response_expected=response_expected
        )

    async def get_edge_count_config(self, pin):
        """
        Returns the edge type and debounce time for the selected pin of port A as set by
        :func:`Set Edge Count Config`.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        assert (isinstance(pin, int) and (0 <= pin <= 7))

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EDGE_COUNT_CONFIG,
            data=pack_payload((pin,), 'B'),
            response_expected=True
        )
        edge_type, debounce_time = unpack_payload(payload, 'B B')
        edge_type = EdgeType(edge_type)
        return GetEdgeCountConfig(edge_type, debounce_time)
