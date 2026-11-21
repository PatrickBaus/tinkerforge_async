"""
Chibi Extension of the Master Brick.
"""

# pylint: disable=too-many-lines,duplicate-code
from __future__ import annotations

import asyncio
from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple

from ..devices import Device
from ..ip_connection_helper import pack_payload, unpack_payload
from .common import FunctionID

if TYPE_CHECKING:
    from ..ip_connection import IPConnectionAsync


class GetChibiErrorLog(NamedTuple):
    underrun: int
    no_ack: int
    crc_error: int
    overflow: int


@unique
class ChibiFrequency(Enum):
    """
    The Chibi frequencies available.
    """

    OQPSK_868_MHZ = 0
    OQPSK_915_MHZ = 1
    OQPSK_750_MHZ = 2
    BPSK40_915_MHZ = 3


class ChibiExtension(Device):
    """
    The functions of the Chibi Extension.
    """

    async def is_chibi_present(self) -> bool:
        """
        Returns *true* if a Chibi Extension is available to be used by the Master Brick.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_CHIBI_PRESENT, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_chibi_address(self, address: int, response_expected: bool = True) -> None:
        """
        Sets the address (1-255) belonging to the Chibi Extension.

        It is possible to set the address with the Brick Viewer and it will be
        saved in the EEPROM of the Chibi Extension, it does not
        have to be set on every startup.
        """
        if not 1 <= address <= 255:
            raise ValueError(f"Invalid argument: expected 1 <= address <= 255, got address={address!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_ADDRESS,
            data=pack_payload((int(address),), "B"),
            response_expected=response_expected,
        )

    async def get_chibi_address(self) -> int:
        """
        Returns the address as set by :func:`Set Chibi Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_ADDRESS, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_chibi_master_address(self, address: int, response_expected: bool = True) -> None:
        """
        Sets the address (1-255) of the Chibi Master. This address is used if the
        Chibi Extension is used as slave (i.e. it does not have a USB connection).

        It is possible to set the address with the Brick Viewer and it will be
        saved in the EEPROM of the Chibi Extension, it does not
        have to be set on every startup.
        """
        if not 1 <= address <= 255:
            raise ValueError(f"Invalid argument: expected 1 <= address <= 255, got address={address!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_MASTER_ADDRESS,
            data=pack_payload((int(address),), "B"),
            response_expected=response_expected,
        )

    async def get_chibi_master_address(self) -> int:
        """
        Returns the address as set by :func:`Set Chibi Master Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_MASTER_ADDRESS, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def __set_chibi_slave_address(self, num: int, address: int, response_expected: bool = True) -> None:
        """
        Sets up to 254 slave addresses. Valid addresses are in range 1-255. 0 has a
        special meaning, it is used as list terminator and not allowed as normal slave
        address. The address numeration (via ``num`` parameter) has to be used
        ascending from 0. For example: If you use the Chibi Extension in Master mode
        (i.e. the stack has an USB connection) and you want to talk to three other
        Chibi stacks with the slave addresses 17, 23, and 42, you should call with
        ``(0, 17)``, ``(1, 23)``, ``(2, 42)`` and ``(3, 0)``. The last call with
        ``(3, 0)`` is a list terminator and indicates that the Chibi slave address
        list contains 3 addresses in this case.

        It is possible to set the addresses with the Brick Viewer, that will take care
        of correct address numeration and list termination.

        The slave addresses will be saved in the EEPROM of the Chibi Extension, they
        don't have to be set on every startup.
        """
        if not 0 <= address <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= address <= 255, got address={address!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_SLAVE_ADDRESS,
            data=pack_payload((int(num), int(address)), "B B"),
            response_expected=response_expected,
        )

    async def set_chibi_slave_addresses(
        self, addresses: tuple[int, ...] | list[int], response_expected: bool = True
    ) -> None:
        """
        Sets up to 254 slave addresses. Valid addresses are in range 1-255. For
        example: If you use the Chibi Extension in Master mode
        (i.e. the stack has an USB connection) and you want to talk to three other
        Chibi stacks with the slave addresses 17, 23, and 42, you should call this
        function with ``(17, 23, 42)``

        The slave addresses will be saved in the EEPROM of the Chibi Extension, they
        don't have to be set on every startup.
        """
        if not isinstance(addresses, (tuple, list)):
            raise ValueError(
                f"Invalid argument: expected isinstance(addresses, (tuple, list)), got addresses={addresses!r}"
            )
        addresses = list(addresses)
        if not addresses or addresses[-1] != 0:
            addresses += [
                0,
            ]  # add a trailing [0], because it is the delimiter
        if len(addresses) > 255:
            raise ValueError(f"Invalid argument: expected len(addresses) <= 255, got addresses={addresses!r}")

        coros = [
            self.__set_chibi_slave_address(index, address, response_expected) for index, address in enumerate(addresses)
        ]
        await asyncio.gather(*coros)

    async def __get_chibi_slave_address(self, num: int) -> int:
        """
        Returns the slave address for a given ``num`` as set by
        :func:`Set Chibi Slave Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHIBI_SLAVE_ADDRESS,
            data=pack_payload((int(num),), "B"),
            response_expected=True,
        )

        return unpack_payload(payload, "B")

    async def get_slave_addresses(self) -> tuple[int, ...]:
        """
        Returns the slave addresses as a tuple.
        """
        addresses = [await self.__get_chibi_slave_address(0)]
        index = 1
        while addresses[-1] != 0:
            addresses.append(await self.__get_chibi_slave_address(index))
            index += 1

        return tuple(addresses[:-1])

    async def get_chibi_signal_strength(self) -> int:
        """
        Returns the signal strength in dBm. The signal strength updates every time a
        packet is received.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_SIGNAL_STRENGTH, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def get_chibi_error_log(self) -> GetChibiErrorLog:
        """
        Returns underrun, CRC error, no ACK and overflow error counts of the Chibi
        communication. If these errors start rising, it is likely that either the
        distance between two Chibi stacks is becoming too big or there are
        interferences.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_ERROR_LOG, response_expected=True
        )
        return GetChibiErrorLog(*unpack_payload(payload, "H H H H"))

    async def set_chibi_frequency(self, frequency: ChibiFrequency | int, response_expected: bool = True) -> None:
        """
        Sets the Chibi frequency range for the Chibi Extension. Possible values are:

        .. csv-table::
         :header: "Type", "Description"
         :widths: 10, 100

         "0",    "OQPSK 868MHz (Europe)"
         "1",    "OQPSK 915MHz (US)"
         "2",    "OQPSK 780MHz (China)"
         "3",    "BPSK40 915MHz"

        It is possible to set the frequency with the Brick Viewer, and it will be saved in the EEPROM of the Chibi
        Extension, it does not have to be set on every startup.
        """
        if not isinstance(frequency, ChibiFrequency):
            frequency = ChibiFrequency(frequency)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_FREQUENCY,
            data=pack_payload((frequency.value,), "B"),
            response_expected=response_expected,
        )

    async def get_chibi_frequency(self) -> ChibiFrequency:
        """
        Returns the frequency value as set by :func:`Set Chibi Frequency`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_FREQUENCY, response_expected=True
        )
        return ChibiFrequency(unpack_payload(payload, "B"))

    async def set_chibi_channel(self, channel: int, response_expected: bool = True) -> None:
        """
        Sets the channel used by the Chibi Extension. Possible channels are
        different for different frequencies:

        .. csv-table::
         :header: "Frequency",             "Possible Channels"
         :widths: 40, 60

         "OQPSK 868MHz (Europe)", "0"
         "OQPSK 915MHz (US)",     "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
         "OQPSK 780MHz (China)",  "0, 1, 2, 3"
         "BPSK40 915MHz",         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

        It is possible to set the channel with the Brick Viewer, and it will be saved in the EEPROM of the Chibi
        Extension, it does not have to be set on every startup.
        """
        # TODO: Add sanity checking of the channel
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_CHANNEL,
            data=pack_payload((int(channel),), "B"),
            response_expected=response_expected,
        )

    async def get_chibi_channel(self) -> int:
        """
        Returns the channel as set by :func:`Set Chibi Channel`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_CHANNEL, response_expected=True
        )
        return unpack_payload(payload, "B")
