"""
Module for the Tinkerforge Remote Switch Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RemoteSwitch_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, Any, TypeAlias, cast, override

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import check_range
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    SWITCHING_DONE = 3


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SWITCH_SOCKET = 1
    GET_SWITCHING_STATE = 2
    SET_REPEATS = 4
    GET_REPEATS = 5
    SWITCH_SOCKET_A = 6
    SWITCH_SOCKET_B = 7
    DIM_SOCKET_B = 8
    SWITCH_SOCKET_C = 9


@unique
class SwitchTo(Enum):
    """
    The switch to options
    """

    OFF = 0
    ON = 1


@unique
class SwitchingState(Enum):
    """
    The switching state options
    """

    READY = 0
    BUSY = 1


class BrickletRemoteSwitch(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Controls remote mains switches
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_REMOTE_SWITCH
    DEVICE_DISPLAY_NAME = "Remote Switch Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    SwitchTo: TypeAlias = SwitchTo
    SwitchingState: TypeAlias = SwitchingState

    CALLBACK_FORMATS = {
        CallbackID.SWITCHING_DONE: "",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.SWITCHING_DONE,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def switch_socket(
        self, house_code: int, receiver_code: int, switch_to: SwitchTo | int, response_expected: bool = True
    ) -> None:
        """
        This function is deprecated, use :func:`switch_socket_a` instead.
        """
        house_code = int(house_code)
        check_range("house_code", house_code, 0, 31)
        receiver_code = int(receiver_code)
        check_range("receiver_code", receiver_code, 0, 31)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SWITCH_SOCKET,
            data=pack_payload((house_code, receiver_code, SwitchTo(switch_to).value), "B B B"),
            response_expected=response_expected,
        )

    async def get_switching_state(self) -> SwitchingState:
        """
        Returns the current switching state. If the current state is busy, the
        Bricklet is currently sending a code to switch a socket. It will not
        accept any requests to switch sockets until the state changes to ready.

        How long the switching takes is dependent on the number of repeats, see
        :func:`set_repeats`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SWITCHING_STATE, response_expected=True
        )
        return SwitchingState(unpack_payload(payload, "B"))

    async def set_repeats(self, repeats: int = 5, response_expected: bool = True) -> None:
        """
        Sets the number of times the code is sent when one of the switch socket
        functions is called. The repeats basically correspond to the amount of time
        that a button of the remote is pressed.

        Some dimmers are controlled by the length of a button pressed,
        this can be simulated by increasing the repeats.
        """
        repeats = int(repeats)
        check_range("repeats", repeats, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_REPEATS,
            data=pack_payload((repeats,), "B"),
            response_expected=response_expected,
        )

    async def get_repeats(self) -> int:
        """
        Returns the number of repeats as set by :func:`set_repeats`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_REPEATS, response_expected=True
        )
        return cast(int, unpack_payload(payload, "B"))

    async def switch_socket_a(
        self, house_code: int, receiver_code: int, switch_to: SwitchTo | int, response_expected: bool = True
    ) -> None:
        """
        To switch a type A socket you have to give the house code, receiver code and the
        state (on or off) you want to switch to.

        A detailed description on how you can figure out the house and receiver code
        can be found ``here <remote_switch_bricklet_type_a_house_and_receiver_code>``.

        .. versionadded:: 2.0.1 (Firmware)
        """
        house_code = int(house_code)
        check_range("house_code", house_code, 0, 31)
        receiver_code = int(receiver_code)
        check_range("receiver_code", receiver_code, 0, 31)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SWITCH_SOCKET_A,
            data=pack_payload((house_code, receiver_code, SwitchTo(switch_to).value), "B B B"),
            response_expected=response_expected,
        )

    async def switch_socket_b(
        self, address: int, unit: int, switch_to: SwitchTo | int, response_expected: bool = True
    ) -> None:
        """
        To switch a type B socket you have to give the address, unit and the state
        (on or off) you want to switch to.

        To switch all devices with the same address use 255 for the unit.

        A detailed description on how you can teach a socket the address and unit can
        be found ``here <remote_switch_bricklet_type_b_address_and_unit>``.

        .. versionadded:: 2.0.1 (Firmware)
        """
        address = int(address)
        check_range("address", address, 0, 67108863)
        unit = int(unit)
        check_range("unit", unit, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SWITCH_SOCKET_B,
            data=pack_payload((address, unit, SwitchTo(switch_to).value), "I B B"),
            response_expected=response_expected,
        )

    async def dim_socket_b(self, address: int, unit: int, dim_value: int, response_expected: bool = True) -> None:
        """
        To control a type B dimmer you have to give the address, unit and the
        dim value you want to set the dimmer to.

        A detailed description on how you can teach a dimmer the address and unit can
        be found ``here <remote_switch_bricklet_type_b_address_and_unit>``.

        .. versionadded:: 2.0.1 (Firmware)
        """
        address = int(address)
        check_range("address", address, 0, 67108863)
        unit = int(unit)
        check_range("unit", unit, 0, 255)
        dim_value = int(dim_value)
        check_range("dim_value", dim_value, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DIM_SOCKET_B,
            data=pack_payload((address, unit, dim_value), "I B B"),
            response_expected=response_expected,
        )

    async def switch_socket_c(
        self, system_code: str, device_code: int, switch_to: SwitchTo | int, response_expected: bool = True
    ) -> None:
        """
        To switch a type C socket you have to give the system code, device code and the
        state (on or off) you want to switch to.

        A detailed description on how you can figure out the system and device code
        can be found ``here <remote_switch_bricklet_type_c_system_and_device_code>``.

        .. versionadded:: 2.0.1 (Firmware)
        """
        device_code = int(device_code)
        check_range("device_code", device_code, 1, 16)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SWITCH_SOCKET_C,
            data=pack_payload((system_code, device_code, SwitchTo(switch_to).value), "c B B"),
            response_expected=response_expected,
        )

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, None
