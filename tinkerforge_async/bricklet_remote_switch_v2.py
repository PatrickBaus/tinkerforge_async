"""
Module for the Tinkerforge Remote Switch Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RemoteSwitchV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .helper import check_range
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    SWITCHING_DONE = 2
    REMOTE_STATUS_A = 14
    REMOTE_STATUS_B = 15
    REMOTE_STATUS_C = 16


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_SWITCHING_STATE = 1
    SET_REPEATS = 3
    GET_REPEATS = 4
    SWITCH_SOCKET_A = 5
    SWITCH_SOCKET_B = 6
    DIM_SOCKET_B = 7
    SWITCH_SOCKET_C = 8
    SET_REMOTE_CONFIGURATION = 9
    GET_REMOTE_CONFIGURATION = 10
    GET_REMOTE_STATUS_A = 11
    GET_REMOTE_STATUS_B = 12
    GET_REMOTE_STATUS_C = 13


@unique
class SwitchingState(Enum):
    """
    The switching state options
    """

    READY = 0
    BUSY = 1


@unique
class SwitchTo(Enum):
    """
    The switch to options
    """

    OFF = 0
    ON = 1


@unique
class RemoteType(Enum):
    """
    The remote type options
    """

    A = 0
    B = 1
    C = 2


class GetRemoteConfiguration(NamedTuple):
    remote_type: RemoteType
    minimum_repeats: int
    callback_enabled: bool


class GetRemoteStatusA(NamedTuple):
    house_code: int
    receiver_code: int
    switch_to: SwitchTo
    repeats: int


class GetRemoteStatusB(NamedTuple):
    address: int
    unit: int
    switch_to: SwitchTo
    dim_value: int
    repeats: int


class GetRemoteStatusC(NamedTuple):
    system_code: str
    device_code: int
    switch_to: SwitchTo
    repeats: int


class BrickletRemoteSwitchV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Controls remote mains switches and receives signals from remotes
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_REMOTE_SWITCH_V2
    DEVICE_DISPLAY_NAME = "Remote Switch Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    SwitchingState: TypeAlias = SwitchingState
    SwitchTo: TypeAlias = SwitchTo
    RemoteType: TypeAlias = RemoteType

    CALLBACK_FORMATS = {
        CallbackID.SWITCHING_DONE: "",
        CallbackID.REMOTE_STATUS_A: "B B B H",
        CallbackID.REMOTE_STATUS_B: "I B B B H",
        CallbackID.REMOTE_STATUS_C: "c B B H",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.SWITCHING_DONE,)),
        Channel(1, callbacks=(CallbackID.REMOTE_STATUS_A,)),
        Channel(2, callbacks=(CallbackID.REMOTE_STATUS_B,)),
        Channel(3, callbacks=(CallbackID.REMOTE_STATUS_C,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_switching_state(self) -> SwitchingState:
        """
        Returns the current switching state. If the current state is busy, the
        Bricklet is currently sending a code to switch a socket. It will not
        accept any calls of switch socket functions until the state changes to ready.

        How long the switching takes is dependent on the number of repeats, see
        :func:`set_repeats`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SWITCHING_STATE, response_expected=True
        )
        return SwitchingState(unpack_payload(payload, "B"))

    async def set_repeats(self, repeats: int = 5, response_expected: bool = True) -> None:
        """
        Sets the number of times the code is sent when one of the Switch Socket
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
        return unpack_payload(payload, "B")

    async def switch_socket_a(
        self, house_code: int, receiver_code: int, switch_to: SwitchTo | int, response_expected: bool = True
    ) -> None:
        """
        To switch a type A socket you have to give the house code, receiver code and the
        state (on or off) you want to switch to.

        A detailed description on how you can figure out the house and receiver code
        can be found ``here <remote_switch_bricklet_type_a_house_and_receiver_code>``.
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
        """
        device_code = int(device_code)
        check_range("device_code", device_code, 1, 16)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SWITCH_SOCKET_C,
            data=pack_payload((system_code, device_code, SwitchTo(switch_to).value), "c B B"),
            response_expected=response_expected,
        )

    async def set_remote_configuration(
        self,
        remote_type: RemoteType | int = RemoteType.A,
        minimum_repeats: int = 2,
        callback_enabled: bool = False,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration for **receiving** data from a remote of type A, B or C.

        * Remote Type: A, B or C depending on the type of remote you want to receive.
        * Minimum Repeats: The minimum number of repeated data packets until the callback
          is triggered (if enabled).
        * Callback Enabled: Enable or disable callback (see :attr:`CallbackID.REMOTE_STATUS_A` callback,
          :attr:`CallbackID.REMOTE_STATUS_B` callback and :attr:`CallbackID.REMOTE_STATUS_C` callback).
        """
        minimum_repeats = int(minimum_repeats)
        check_range("minimum_repeats", minimum_repeats, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_REMOTE_CONFIGURATION,
            data=pack_payload((RemoteType(remote_type).value, minimum_repeats, bool(callback_enabled)), "B H !"),
            response_expected=response_expected,
        )

    async def get_remote_configuration(self) -> GetRemoteConfiguration:
        """
        Returns the remote configuration as set by :func:`set_remote_configuration`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_REMOTE_CONFIGURATION, response_expected=True
        )
        remote_type, minimum_repeats, callback_enabled = unpack_payload(payload, "B H !")
        return GetRemoteConfiguration(RemoteType(remote_type), minimum_repeats, callback_enabled)

    async def get_remote_status_a(self) -> GetRemoteStatusA:
        """
        Returns the house code, receiver code, switch state (on/off) and number of
        repeats for remote type A.

        Repeats == 0 means there was no button press. Repeats >= 1 means there
        was a button press with the specified house/receiver code. The repeats are the
        number of received identical data packets. The longer the button is pressed,
        the higher the repeat number.

        Use the callback to get this data automatically when a button is pressed,
        see :func:`set_remote_configuration` and :attr:`CallbackID.REMOTE_STATUS_A` callback.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_REMOTE_STATUS_A, response_expected=True
        )
        house_code, receiver_code, switch_to, repeats = unpack_payload(payload, "B B B H")
        return GetRemoteStatusA(house_code, receiver_code, SwitchTo(switch_to), repeats)

    async def get_remote_status_b(self) -> GetRemoteStatusB:
        """
        Returns the address (unique per remote), unit (button number), switch state
        (on/off) and number of repeats for remote type B.

        If the remote supports dimming the dim value is used instead of the switch state.

        If repeats=0 there was no button press. If repeats >= 1 there
        was a button press with the specified address/unit. The repeats are the number of received
        identical data packets. The longer the button is pressed, the higher the repeat number.

        Use the callback to get this data automatically when a button is pressed,
        see :func:`set_remote_configuration` and :attr:`CallbackID.REMOTE_STATUS_B` callback.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_REMOTE_STATUS_B, response_expected=True
        )
        address, unit, switch_to, dim_value, repeats = unpack_payload(payload, "I B B B H")
        return GetRemoteStatusB(address, unit, SwitchTo(switch_to), dim_value, repeats)

    async def get_remote_status_c(self) -> GetRemoteStatusC:
        """
        Returns the system code, device code, switch state (on/off) and number of repeats for
        remote type C.

        If repeats=0 there was no button press. If repeats >= 1 there
        was a button press with the specified system/device code. The repeats are the number of received
        identical data packets. The longer the button is pressed, the higher the repeat number.

        Use the callback to get this data automatically when a button is pressed,
        see :func:`set_remote_configuration` and :attr:`CallbackID.REMOTE_STATUS_C` callback.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_REMOTE_STATUS_C, response_expected=True
        )
        system_code, device_code, switch_to, repeats = unpack_payload(payload, "c B B H")
        return GetRemoteStatusC(system_code, device_code, SwitchTo(switch_to), repeats)

    def _convert_callback(  # pylint: disable=too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.SWITCHING_DONE:
            return 0, None
        if callback_id is CallbackID.REMOTE_STATUS_A:
            house_code, receiver_code, switch_to, repeats = value
            return 1, GetRemoteStatusA(house_code, receiver_code, SwitchTo(switch_to), repeats)
        if callback_id is CallbackID.REMOTE_STATUS_B:
            address, unit, switch_to, dim_value, repeats = value
            return 2, GetRemoteStatusB(address, unit, SwitchTo(switch_to), dim_value, repeats)
        system_code, device_code, switch_to, repeats = value
        return 3, GetRemoteStatusC(system_code, device_code, SwitchTo(switch_to), repeats)
