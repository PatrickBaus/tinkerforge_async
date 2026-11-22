"""
Module for the Tinkerforge RS232 Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RS232_Bricklet_Python.html) implemented using
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
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import Duration, check_length, check_range, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    READ = 8
    ERROR = 9
    FRAME_READABLE = 13


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    WRITE = 1
    READ = 2
    ENABLE_READ_CALLBACK = 3
    DISABLE_READ_CALLBACK = 4
    IS_READ_CALLBACK_ENABLED = 5
    SET_CONFIGURATION = 6
    GET_CONFIGURATION = 7
    SET_BREAK_CONDITION = 10
    SET_FRAME_READABLE_CALLBACK_CONFIGURATION = 11
    GET_FRAME_READABLE_CALLBACK_CONFIGURATION = 12
    READ_FRAME = 14


@unique
class Baudrate(Enum):
    """
    The baudrate options
    """

    BAUDRATE_300 = 0
    BAUDRATE_600 = 1
    BAUDRATE_1200 = 2
    BAUDRATE_2400 = 3
    BAUDRATE_4800 = 4
    BAUDRATE_9600 = 5
    BAUDRATE_14400 = 6
    BAUDRATE_19200 = 7
    BAUDRATE_28800 = 8
    BAUDRATE_38400 = 9
    BAUDRATE_57600 = 10
    BAUDRATE_115200 = 11
    BAUDRATE_230400 = 12


@unique
class Parity(Enum):
    """
    The parity options
    """

    NONE = 0
    ODD = 1
    EVEN = 2
    FORCED_PARITY_1 = 3
    FORCED_PARITY_0 = 4


@unique
class Stopbits(Enum):
    """
    The stopbits options
    """

    STOPBITS_1 = 1
    STOPBITS_2 = 2


@unique
class Wordlength(Enum):
    """
    The wordlength options
    """

    WORDLENGTH_5 = 5
    WORDLENGTH_6 = 6
    WORDLENGTH_7 = 7
    WORDLENGTH_8 = 8


@unique
class HardwareFlowcontrol(Enum):
    """
    The hardware flowcontrol options
    """

    OFF = 0
    ON = 1


@unique
class SoftwareFlowcontrol(Enum):
    """
    The software flowcontrol options
    """

    OFF = 0
    ON = 1


@unique
class Error(Enum):
    """
    The error options
    """

    OVERRUN = 1
    PARITY = 2
    FRAMING = 4


class Read(NamedTuple):
    message: tuple[str, ...]
    length: int


class GetConfiguration(NamedTuple):
    baudrate: Baudrate
    parity: Parity
    stopbits: Stopbits
    wordlength: Wordlength
    hardware_flowcontrol: HardwareFlowcontrol
    software_flowcontrol: SoftwareFlowcontrol


class ReadFrame(NamedTuple):
    message: tuple[str, ...]
    length: int


class ReadEvent(NamedTuple):
    message: tuple[str, ...]
    length: int


class BrickletRS232(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Communicates with RS232 devices
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_RS232
    DEVICE_DISPLAY_NAME = "RS232 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Baudrate: TypeAlias = Baudrate
    Parity: TypeAlias = Parity
    Stopbits: TypeAlias = Stopbits
    Wordlength: TypeAlias = Wordlength
    HardwareFlowcontrol: TypeAlias = HardwareFlowcontrol
    SoftwareFlowcontrol: TypeAlias = SoftwareFlowcontrol
    Error: TypeAlias = Error

    CALLBACK_FORMATS = {
        CallbackID.READ: "60c B",
        CallbackID.ERROR: "B",
        CallbackID.FRAME_READABLE: "B",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.READ,)),
        Channel(1, callbacks=(CallbackID.ERROR,)),
        Channel(2, callbacks=(CallbackID.FRAME_READABLE,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 3)

    async def write(self, message: str | Sequence[str], length: int) -> int:
        """
        Writes a string of up to 60 characters to the RS232 interface. The string
        can be binary data, ASCII or similar is not necessary.

        The length of the string has to be given as an additional parameter.

        The return value is the number of bytes that could be written.

        See :func:`set_configuration` for configuration possibilities
        regarding baudrate, parity and so on.
        """
        check_length("message", message, 60)
        length = int(length)
        check_range("length", length, 0, 60)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE,
            data=pack_payload((list(message), length), "60c B"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def read(self) -> Read:
        """
        Returns the currently buffered message. The maximum length
        of message is 60. If the returned length is 0, no new data was available.

        Instead of polling with this function, you can also use
        callbacks. See :func:`enable_read_callback` and :attr:`CallbackID.READ` callback.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.READ, response_expected=True)
        message, length = unpack_payload(payload, "60c B")
        return Read(tuple(message), length)

    async def enable_read_callback(self, response_expected: bool = True) -> None:
        """
        Enables the :attr:`CallbackID.READ` callback. This will disable the :attr:`CallbackID.FRAME_READABLE` callback.

        By default the callback is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_READ_CALLBACK, response_expected=response_expected
        )

    async def disable_read_callback(self, response_expected: bool = True) -> None:
        """
        Disables the :attr:`CallbackID.READ` callback.

        By default the callback is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_READ_CALLBACK, response_expected=response_expected
        )

    async def is_read_callback_enabled(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.READ` callback is enabled,
        *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_READ_CALLBACK_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        baudrate: Baudrate | int = Baudrate.BAUDRATE_115200,
        parity: Parity | int = Parity.NONE,
        stopbits: Stopbits | int = Stopbits.STOPBITS_1,
        wordlength: Wordlength | int = Wordlength.WORDLENGTH_8,
        hardware_flowcontrol: HardwareFlowcontrol | int = HardwareFlowcontrol.OFF,
        software_flowcontrol: SoftwareFlowcontrol | int = SoftwareFlowcontrol.OFF,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration for the RS232 communication.

        Hard-/Software flow control can either be on or off but not both simultaneously on.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload(
                (
                    Baudrate(baudrate).value,
                    Parity(parity).value,
                    Stopbits(stopbits).value,
                    Wordlength(wordlength).value,
                    HardwareFlowcontrol(hardware_flowcontrol).value,
                    SoftwareFlowcontrol(software_flowcontrol).value,
                ),
                "B B B B B B",
            ),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        baudrate, parity, stopbits, wordlength, hardware_flowcontrol, software_flowcontrol = unpack_payload(
            payload, "B B B B B B"
        )
        return GetConfiguration(
            Baudrate(baudrate),
            Parity(parity),
            Stopbits(stopbits),
            Wordlength(wordlength),
            HardwareFlowcontrol(hardware_flowcontrol),
            SoftwareFlowcontrol(software_flowcontrol),
        )

    async def set_break_condition(self, break_time: Duration, response_expected: bool = True) -> None:
        """
        Sets a break condition (the TX output is forced to a logic 0 state).
        The parameter sets the hold-time of the break condition.

        Units: break_time in s.

        .. versionadded:: 2.0.2 (Firmware)
        """
        break_time_raw = seconds_to_ms(break_time)
        check_range("break_time", break_time_raw, 0, 65535, break_time)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BREAK_CONDITION,
            data=pack_payload((break_time_raw,), "H"),
            response_expected=response_expected,
        )

    async def set_frame_readable_callback_configuration(
        self, frame_size: int = 0, response_expected: bool = True
    ) -> None:
        """
        Configures the :attr:`CallbackID.FRAME_READABLE` callback. The frame size is the number of bytes, that have to
        be readable to trigger the callback.
        A frame size of 0 disables the callback. A frame size greater than 0 enables the callback and disables the
        :attr:`CallbackID.READ` callback.

        By default the callback is disabled.

        .. versionadded:: 2.0.4 (Firmware)
        """
        frame_size = int(frame_size)
        check_range("frame_size", frame_size, 0, 100)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
            data=pack_payload((frame_size,), "B"),
            response_expected=response_expected,
        )

    async def get_frame_readable_callback_configuration(self) -> int:
        """
        Returns the callback configuration as set by :func:`set_frame_readable_callback_configuration`.

        .. versionadded:: 2.0.4 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def read_frame(self) -> ReadFrame:
        """
        Returns up to one frame of bytes from the read buffer.
        The frame size is configured with :func:`set_frame_readable_callback_configuration`.
        If the returned length is 0, no new data was available.

        .. versionadded:: 2.0.4 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READ_FRAME, response_expected=True
        )
        message, length = unpack_payload(payload, "60c B")
        return ReadFrame(tuple(message), length)

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.READ:
            message, length = value
            return 0, ReadEvent(tuple(message), length)
        if callback_id is CallbackID.ERROR:
            return 1, Error(value)
        return 2, value
