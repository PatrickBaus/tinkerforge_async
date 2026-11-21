"""
RS485 Extension of the Master Brick.
"""

# pylint: disable=too-many-lines,duplicate-code
from __future__ import annotations

import asyncio
from collections.abc import Iterable
from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple

from ..devices import Device
from ..ip_connection_helper import pack_payload, unpack_payload
from .common import FunctionID

if TYPE_CHECKING:
    from ..ip_connection import IPConnectionAsync


class GetRS485Configuration(NamedTuple):
    speed: int
    parity: Rs485Parity
    stopbits: int


@unique
class Rs485Parity(Enum):
    """
    The parity bit used for error correction. NONE disables parity
    """

    NONE = "n"
    EVEN = "e"
    ODD = "o"


class Rs485Extension(Device):
    """
    The functions of the RS485 Extension.
    """

    async def is_rs485_present(self) -> bool:
        """
        Returns *true* if a RS485 Extension is available to be used by the Master Brick.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_RS485_PRESENT, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_rs485_address(self, address: int, response_expected: bool = True) -> None:
        """
        Sets the address (0-255) belonging to the RS485 Extension.

        Set to 0 if the RS485 Extension should be the RS485 Master (i.e. connected to a PC via USB).

        It is possible to set the address with the Brick Viewer, and it will be saved in the EEPROM of the RS485
        Extension, it does not have to be set on every startup.
        """
        if not 0 <= address <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= address <= 255, got address={address!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RS485_ADDRESS,
            data=pack_payload((int(address),), "B"),
            response_expected=response_expected,
        )

    async def get_rs485_address(self) -> int:
        """
        Returns the address as set by :func:`Set RS485 Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RS485_ADDRESS, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def __set_rs485_slave_address(self, num: int, address: int, response_expected: bool = True) -> None:
        """
        Sets up to 255 slave addresses. Valid addresses are in range 1-255. 0 has a special meaning, it is used as list
        terminator and not allowed as normal slave address. The address numeration (via ``num`` parameter) has to be
        used ascending from 0. For example: If you use the RS485 Extension in Master mode (i.e. the stack has a USB
        connection) and you want to talk to three other RS485 stacks with the addresses 17, 23, and 42, you should call
         with ``(0, 17)``, ``(1, 23)``, ``(2, 42)`` and ``(3, 0)``. The last call with ``(3, 0)`` is a list terminator
         and indicates that the RS485 slave address list contains 3 addresses in this case.

        It is possible to set the addresses with the Brick Viewer, that will take care of correct address numeration and
        list termination.

        The slave addresses will be saved in the EEPROM of the Chibi Extension, they don't have to be set on every
        startup.
        """
        if not 0 <= num <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= num <= 255, got num={num!r}")
        if not 0 <= address <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= address <= 255, got address={address!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RS485_SLAVE_ADDRESS,
            data=pack_payload((int(num), int(address)), "B B"),
            response_expected=response_expected,
        )

    async def set_rs485_slave_addresses(self, addresses: Iterable[int], response_expected: bool = True) -> None:
        """
        Sets up to 255 slave addresses. Valid addresses are in range 1-255. For example: If you use the RS485 Extension
        in Master mode (i.e. the stack has a USB connection) and you want to talk to three other RS485 stacks with the
        addresses 17, 23, and 42, you should call the function with ``(17, 23, 42)``

        The slave addresses will be saved in the EEPROM of the Chibi Extension, they don't have to be set on every
        startup.
        """
        if not isinstance(addresses, (tuple, list)):
            raise ValueError(
                f"Invalid argument: expected isinstance(addresses, (tuple, list)), got addresses={addresses!r}"
            )
        addresses = list(addresses)
        if addresses[-1] != 0:
            addresses += [
                0,
            ]  # add a trailing [0], because it is the delimiter
        if len(addresses) >= 255:
            raise ValueError(f"Invalid argument: expected len(addresses) < 255, got addresses={addresses!r}")

        coros = [
            self.__set_rs485_slave_address(index, address, response_expected) for index, address in enumerate(addresses)
        ]
        await asyncio.gather(*coros)

    async def __get_rs485_slave_address(self, num: int) -> int:
        """
        Returns the slave address for a given ``num`` as set by
        :func:`Set RS485 Slave Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RS485_SLAVE_ADDRESS,
            data=pack_payload((int(num),), "B"),
            response_expected=True,
        )

        return unpack_payload(payload, "B")

    async def get_rs485_slave_addresses(self) -> tuple[int, ...]:
        """
        Returns the slave addresses as a tuple.
        """
        addresses = [await self.__get_rs485_slave_address(0)]
        index = 1
        while addresses[-1] != 0:
            addresses.append(await self.__get_rs485_slave_address(index))
            index += 1
        return tuple(addresses[:-1])  # strip the trailing [0], because it is the delimiter

    async def get_rs485_error_log(self) -> int:
        """
        Returns CRC error counts of the RS485 communication.
        If this counter starts rising, it is likely that the distance
        between the RS485 nodes is too big or there is some kind of
        interference.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RS485_ERROR_LOG, response_expected=True
        )

        return unpack_payload(payload, "H")

    async def set_rs485_configuration(
        self, speed: int, parity: Rs485Parity, stopbits: int, response_expected: bool = True
    ) -> None:
        """
        Sets the configuration of the RS485 Extension. Speed is given in baud. The
        Master Brick will try to match the given baud rate as exactly as possible.
        The maximum recommended baud rate is 2000000 (2Mbit/s).
        Possible values for parity are 'n' (none), 'e' (even) and 'o' (odd).
        Possible values for stop bits are 1 and 2.

        If your RS485 is unstable (lost messages etc.), the first thing you should
        try is to decrease the speed. On very large bus (e.g. 1km), you probably
        should use a value in the range of 100000 (100kbit/s).

        The values are stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after configuration.
        """
        if stopbits not in (1, 2):
            raise ValueError(f"Invalid argument: expected stopbits in (1, 2), got stopbits={stopbits!r}")
        if not isinstance(parity, Rs485Parity):
            parity = Rs485Parity(parity)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RS485_CONFIGURATION,
            data=pack_payload((int(speed), parity.value, int(stopbits)), "I c B"),
            response_expected=response_expected,
        )

    async def get_rs485_configuration(self) -> GetRS485Configuration:
        """
        Returns the configuration as set by :func:`Set RS485 Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RS485_CONFIGURATION, response_expected=True
        )
        speed, parity, stopbits = unpack_payload(payload, "I c B")

        return GetRS485Configuration(speed, Rs485Parity(parity), stopbits)
