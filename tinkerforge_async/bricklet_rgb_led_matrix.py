"""
Module for the Tinkerforge RGB LED Matrix Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDMatrix_Bricklet_Python.html) implemented using
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
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    FRAME_STARTED = 11


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_RED = 1
    GET_RED = 2
    SET_GREEN = 3
    GET_GREEN = 4
    SET_BLUE = 5
    GET_BLUE = 6
    SET_FRAME_DURATION = 7
    GET_FRAME_DURATION = 8
    DRAW_FRAME = 9
    GET_SUPPLY_VOLTAGE = 10


VOLTAGE = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletRGBLEDMatrix(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    RGB LED Matrix with 8x8 pixel
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_RGB_LED_MATRIX
    DEVICE_DISPLAY_NAME = "RGB LED Matrix Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.FRAME_STARTED: "I",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.FRAME_STARTED,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_red(self, red: bytes | Sequence[int], response_expected: bool = True) -> None:
        """
        Sets the 64 red LED values of the matrix.
        """
        check_length("red", red, 64)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RED,
            data=pack_payload((list(map(int, red)),), "64B"),
            response_expected=response_expected,
        )

    async def get_red(self) -> tuple[int, ...]:
        """
        Returns the red LED values as set by :func:`set_red`.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_RED, response_expected=True)
        return tuple(unpack_payload(payload, "64B"))

    async def set_green(self, green: bytes | Sequence[int], response_expected: bool = True) -> None:
        """
        Sets the 64 green LED values of the matrix.
        """
        check_length("green", green, 64)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GREEN,
            data=pack_payload((list(map(int, green)),), "64B"),
            response_expected=response_expected,
        )

    async def get_green(self) -> tuple[int, ...]:
        """
        Returns the green LED values as set by :func:`set_green`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GREEN, response_expected=True
        )
        return tuple(unpack_payload(payload, "64B"))

    async def set_blue(self, blue: bytes | Sequence[int], response_expected: bool = True) -> None:
        """
        Sets the 64 blue LED values of the matrix.
        """
        check_length("blue", blue, 64)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BLUE,
            data=pack_payload((list(map(int, blue)),), "64B"),
            response_expected=response_expected,
        )

    async def get_blue(self) -> tuple[int, ...]:
        """
        Returns the blue LED values as set by :func:`set_blue`.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_BLUE, response_expected=True)
        return tuple(unpack_payload(payload, "64B"))

    async def set_frame_duration(self, frame_duration: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the frame duration.

        Example: If you want to achieve 20 frames per second, you should
        set the frame duration to 50ms (50ms * 20 = 1 second).

        Set this value to 0 to turn the automatic frame write mechanism off.

        Approach:

        * Call :func:`set_frame_duration` with value > 0.
        * Set LED values for first frame with :func:`set_red`, :func:`set_green`, :func:`set_blue`.
        * Wait for :attr:`CallbackID.FRAME_STARTED` callback.
        * Set LED values for second frame with :func:`set_red`, :func:`set_green`, :func:`set_blue`.
        * Wait for :attr:`CallbackID.FRAME_STARTED` callback.
        * and so on.

        For frame duration of 0 see :func:`draw_frame`.

        Units: frame_duration in s.
        """
        frame_duration_raw = seconds_to_ms(frame_duration)
        check_range("frame_duration", frame_duration_raw, 0, 65535, frame_duration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_DURATION,
            data=pack_payload((frame_duration_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_frame_duration(self) -> Decimal:
        """
        Returns the frame duration as set by :func:`set_frame_duration`.

        Units: frame_duration in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_DURATION, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "H"))

    async def draw_frame(self, response_expected: bool = True) -> None:
        """
        If you set the frame duration to 0 (see :func:`set_frame_duration`), you can use this
        function to transfer the frame to the matrix.

        Approach:

        * Call :func:`set_frame_duration` with 0.
        * Set LED values for first frame with :func:`set_red`, :func:`set_green`, :func:`set_blue`.
        * Call :func:`draw_frame`.
        * Wait for :attr:`CallbackID.FRAME_STARTED` callback.
        * Set LED values for second frame with :func:`set_red`, :func:`set_green`, :func:`set_blue`.
        * Call :func:`draw_frame`.
        * Wait for :attr:`CallbackID.FRAME_STARTED` callback.
        * and so on.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DRAW_FRAME, response_expected=response_expected
        )

    async def get_supply_voltage(self) -> Decimal:
        """
        Returns the current supply voltage of the Bricklet.

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SUPPLY_VOLTAGE, response_expected=True
        )
        return VOLTAGE.to_si(unpack_payload(payload, "H"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, value
