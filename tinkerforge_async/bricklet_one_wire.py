"""
Module for the Tinkerforge One Wire Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/OneWire_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

import asyncio
from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, DeviceIdentifier, _FunctionID
from .helper import check_range
from .ip_connection_helper import pack_payload, unpack_payload
from .streams import Chunk, read_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SEARCH_BUS_LOW_LEVEL = 1
    RESET_BUS = 2
    WRITE = 3
    READ = 4
    WRITE_COMMAND = 5
    SET_COMMUNICATION_LED_CONFIG = 6
    GET_COMMUNICATION_LED_CONFIG = 7


@unique
class Status(Enum):
    """
    The status options
    """

    OK = 0
    BUSY = 1
    NO_PRESENCE = 2
    TIMEOUT = 3
    ERROR = 4


@unique
class CommunicationLEDConfig(Enum):
    """
    The communication led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_COMMUNICATION = 3


class SearchBus(NamedTuple):
    identifier_length: int
    identifier_chunk_offset: int
    identifier_chunk_data: tuple[int, ...]
    status: Status


class SearchBusResult(NamedTuple):
    status: Status
    identifier: tuple[int, ...]


class Read(NamedTuple):
    data: int
    status: Status


class BrickletOneWire(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Communicates with up 64 1-Wire devices
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ONE_WIRE
    DEVICE_DISPLAY_NAME = "One Wire Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Status: TypeAlias = Status
    CommunicationLEDConfig: TypeAlias = CommunicationLEDConfig

    CALLBACK_FORMATS = {}

    SID_TO_CALLBACK = {}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()

    async def search_bus_low_level(self) -> SearchBus:
        """
        Returns a list of up to 64 identifiers of the connected 1-Wire devices.
        Each identifier is 64-bit and consists of 8-bit family code, 48-bit ID and
        8-bit CRC.

        To get these identifiers the Bricklet runs the
        `SEARCH ROM algorithm <https://www.maximintegrated.com/en/app-notes/index.mvp/id/187>`__,
        as defined by Maxim.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.SEARCH_BUS_LOW_LEVEL, response_expected=True
        )
        identifier_length, identifier_chunk_offset, identifier_chunk_data, status = unpack_payload(payload, "H H 7Q B")
        return SearchBus(identifier_length, identifier_chunk_offset, tuple(identifier_chunk_data), Status(status))

    async def search_bus(self) -> SearchBusResult:
        """
        Returns a list of up to 64 identifiers of the connected 1-Wire devices.
        Each identifier is 64-bit and consists of 8-bit family code, 48-bit ID and
        8-bit CRC.

        To get these identifiers the Bricklet runs the
        `SEARCH ROM algorithm <https://www.maximintegrated.com/en/app-notes/index.mvp/id/187>`__,
        as defined by Maxim.

        This function transfers the complete identifier stream and calls :func:`search_bus_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.search_bus_low_level()
            return Chunk(result.identifier_length, result.identifier_chunk_offset, result.identifier_chunk_data, result)

        async with self._stream_lock:
            data, result = await read_stream(read_chunk, name="identifier", chunk_size=7)
        return SearchBusResult(result.status, tuple(data))

    async def reset_bus(self) -> Status:
        """
        Resets the bus with the 1-Wire reset operation.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.RESET_BUS, response_expected=True
        )
        return Status(unpack_payload(payload, "B"))

    async def write(self, data: int) -> Status:
        """
        Writes a byte of data to the 1-Wire bus.
        """
        data = int(data)
        check_range("data", data, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.WRITE, data=pack_payload((data,), "B"), response_expected=True
        )
        return Status(unpack_payload(payload, "B"))

    async def read(self) -> Read:
        """
        Reads a byte of data from the 1-Wire bus.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.READ, response_expected=True)
        data, status = unpack_payload(payload, "B B")
        return Read(data, Status(status))

    async def write_command(self, identifier: int, command: int) -> Status:
        """
        Writes a command to the 1-Wire device with the given identifier. You can obtain
        the identifier by calling :func:`search_bus`. The MATCH ROM operation is used to
        write the command.

        If you only have one device connected or want to broadcast to all devices
        you can set the identifier to 0. In this case the SKIP ROM operation is used to
        write the command.
        """
        identifier = int(identifier)
        check_range("identifier", identifier, 0, 18446744073709551615)
        command = int(command)
        check_range("command", command, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_COMMAND,
            data=pack_payload((identifier, command), "Q B"),
            response_expected=True,
        )
        return Status(unpack_payload(payload, "B"))

    async def set_communication_led_config(
        self,
        config: CommunicationLEDConfig | int = CommunicationLEDConfig.SHOW_COMMUNICATION,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the communication LED configuration. By default the LED shows 1-wire
        communication traffic by flickering.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COMMUNICATION_LED_CONFIG,
            data=pack_payload((CommunicationLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_communication_led_config(self) -> CommunicationLEDConfig:
        """
        Returns the configuration as set by :func:`set_communication_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COMMUNICATION_LED_CONFIG, response_expected=True
        )
        return CommunicationLEDConfig(unpack_payload(payload, "B"))
