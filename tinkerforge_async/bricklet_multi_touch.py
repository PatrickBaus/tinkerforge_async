"""
Module for the Tinkerforge Multi Touch Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/MultiTouch_Bricklet_Python.html) implemented using
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

    TOUCH_STATE = 5


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_TOUCH_STATE = 1
    RECALIBRATE = 2
    SET_ELECTRODE_CONFIG = 3
    GET_ELECTRODE_CONFIG = 4
    SET_ELECTRODE_SENSITIVITY = 6
    GET_ELECTRODE_SENSITIVITY = 7


class BrickletMultiTouch(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Capacitive touch sensor for 12 electrodes
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_MULTI_TOUCH
    DEVICE_DISPLAY_NAME = "Multi Touch Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.TOUCH_STATE: "H",
    }

    CHANNELS = (Channel(0, getter="get_touch_state", callbacks=(CallbackID.TOUCH_STATE,)),)

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

    async def get_touch_state(self) -> int:
        """
        Returns the current touch state. The state is given as a bitfield.

        Bits 0 to 11 represent the 12 electrodes and bit 12 represents
        the proximity.

        If an electrode is touched, the corresponding bit is *true*. If
        a hand or similar is in proximity to the electrodes, bit 12 is
        *true*.

        Example: The state 4103 = 0x1007 = 0b1000000000111 means that
        electrodes 0, 1 and 2 are touched and that something is in the
        proximity of the electrodes.

        The proximity is activated with a distance of 1-0.02 m. An electrode
        is already counted as touched if a finger is nearly touching the
        electrode. This means that you can put a piece of paper or foil
        or similar on top of a electrode to build a touch panel with
        a professional look.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_STATE, response_expected=True
        )
        return cast(int, unpack_payload(payload, "H"))

    async def recalibrate(self, response_expected: bool = True) -> None:
        """
        Recalibrates the electrodes. Call this function whenever you changed
        or moved you electrodes.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.RECALIBRATE, response_expected=response_expected
        )

    async def set_electrode_config(self, enabled_electrodes: int = 8191, response_expected: bool = True) -> None:
        """
        Enables/disables electrodes with a bitfield (see :func:`get_touch_state`).

        *True* enables the electrode, *false* disables the electrode. A
        disabled electrode will always return *false* as its state. If you
        don't need all electrodes you can disable the electrodes that are
        not needed.

        It is recommended that you disable the proximity bit (bit 12) if
        the proximity feature is not needed. This will reduce the amount of
        traffic that is produced by the :attr:`CallbackID.TOUCH_STATE` callback.

        Disabling electrodes will also reduce power consumption.

        Default: 8191 = 0x1FFF = 0b1111111111111 (all electrodes and proximity feature enabled)
        """
        enabled_electrodes = int(enabled_electrodes)
        check_range("enabled_electrodes", enabled_electrodes, 0, 8191)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ELECTRODE_CONFIG,
            data=pack_payload((enabled_electrodes,), "H"),
            response_expected=response_expected,
        )

    async def get_electrode_config(self) -> int:
        """
        Returns the electrode configuration, as set by :func:`set_electrode_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ELECTRODE_CONFIG, response_expected=True
        )
        return cast(int, unpack_payload(payload, "H"))

    async def set_electrode_sensitivity(self, sensitivity: int = 181, response_expected: bool = True) -> None:
        """
        Sets the sensitivity of the electrodes. An electrode with a high sensitivity
        will register a touch earlier then an electrode with a low sensitivity.

        If you build a big electrode you might need to decrease the sensitivity, since
        the area that can be charged will get bigger. If you want to be able to
        activate an electrode from further away you need to increase the sensitivity.

        After a new sensitivity is set, you likely want to call :func:`recalibrate`
        to calibrate the electrodes with the newly defined sensitivity.
        """
        sensitivity = int(sensitivity)
        check_range("sensitivity", sensitivity, 5, 201)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ELECTRODE_SENSITIVITY,
            data=pack_payload((sensitivity,), "B"),
            response_expected=response_expected,
        )

    async def get_electrode_sensitivity(self) -> int:
        """
        Returns the current sensitivity, as set by :func:`set_electrode_sensitivity`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ELECTRODE_SENSITIVITY, response_expected=True
        )
        return cast(int, unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, value
