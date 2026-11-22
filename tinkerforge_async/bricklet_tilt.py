"""
Module for the Tinkerforge Tilt Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/Tilt_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias, override

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .ip_connection_helper import unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    TILT_STATE = 5


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_TILT_STATE = 1
    ENABLE_TILT_STATE_CALLBACK = 2
    DISABLE_TILT_STATE_CALLBACK = 3
    IS_TILT_STATE_CALLBACK_ENABLED = 4


@unique
class TiltState(Enum):
    """
    The tilt state options
    """

    CLOSED = 0
    OPEN = 1
    CLOSED_VIBRATING = 2


class BrickletTilt(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Detects inclination of Bricklet (tilt switch open/closed)
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_TILT
    DEVICE_DISPLAY_NAME = "Tilt Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    TiltState: TypeAlias = TiltState

    CALLBACK_FORMATS = {
        CallbackID.TILT_STATE: "B",
    }

    CHANNELS = (Channel(0, getter="get_tilt_state", callbacks=(CallbackID.TILT_STATE,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> Any:
        """
        Returns the value of the channel with the secondary id `sid`. See `CHANNELS` for the channels.
        """
        return await self._get_value(sid)

    async def get_tilt_state(self) -> TiltState:
        """
        Returns the current tilt state. The state can either be

        * 0 = Closed: The ball in the tilt switch closes the circuit.
        * 1 = Open: The ball in the tilt switch does not close the circuit.
        * 2 = Closed Vibrating: The tilt switch is in motion (rapid change between open and close).

        .. image:: /Images/Bricklets/bricklet_tilt_mechanics.jpg
           :scale: 100 %
           :alt: Tilt states
           :align: center
           :target: ../../_images/Bricklets/bricklet_tilt_mechanics.jpg
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TILT_STATE, response_expected=True
        )
        return TiltState(unpack_payload(payload, "B"))

    async def enable_tilt_state_callback(self, response_expected: bool = True) -> None:
        """
        Enables the :attr:`CallbackID.TILT_STATE` callback.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_TILT_STATE_CALLBACK, response_expected=response_expected
        )

    async def disable_tilt_state_callback(self, response_expected: bool = True) -> None:
        """
        Disables the :attr:`CallbackID.TILT_STATE` callback.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_TILT_STATE_CALLBACK, response_expected=response_expected
        )

    async def is_tilt_state_callback_enabled(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.TILT_STATE` callback is enabled.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_TILT_STATE_CALLBACK_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, TiltState(value)
