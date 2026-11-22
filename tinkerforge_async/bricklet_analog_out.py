"""
Module for the Tinkerforge Analog Out Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/AnalogOut_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, TypeAlias

from .devices import Device, DeviceIdentifier, _FunctionID
from .helper import check_range
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

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

    SET_VOLTAGE = 1
    GET_VOLTAGE = 2
    SET_MODE = 3
    GET_MODE = 4


@unique
class Mode(Enum):
    """
    The mode options
    """

    ANALOG_VALUE = 0
    MODE_1K_TO_GROUND = 1
    MODE_100K_TO_GROUND = 2
    MODE_500K_TO_GROUND = 3


VOLTAGE = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletAnalogOut(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Generates configurable DC voltage between 0V and 5V
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ANALOG_OUT
    DEVICE_DISPLAY_NAME = "Analog Out Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Mode: TypeAlias = Mode

    CALLBACK_FORMATS = {}

    SID_TO_CALLBACK = {}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_voltage(self, voltage: float | Decimal = 0, response_expected: bool = True) -> None:
        """
        Sets the voltage. Calling this function will set
        the mode to 0 (see :func:`set_mode`).

        Units: voltage in V (0 to 5 V).
        """
        voltage_raw = VOLTAGE.from_si(voltage)
        check_range("voltage", voltage_raw, 0, 5000, voltage)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE,
            data=pack_payload((voltage_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_voltage(self) -> Decimal:
        """
        Returns the voltage as set by :func:`set_voltage`.

        Units: voltage in V (0 to 5 V).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE, response_expected=True
        )
        return VOLTAGE.to_si(unpack_payload(payload, "H"))

    async def set_mode(self, mode: Mode | int = Mode.MODE_1K_TO_GROUND, response_expected: bool = True) -> None:
        """
        Sets the mode of the analog value. Possible modes:

        * 0: Normal Mode (Analog value as set by :func:`set_voltage` is applied)
        * 1: 1k Ohm resistor to ground
        * 2: 100k Ohm resistor to ground
        * 3: 500k Ohm resistor to ground

        Setting the mode to 0 will result in an output voltage of 0 V. You can jump
        to a higher output voltage directly by calling :func:`set_voltage`.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MODE,
            data=pack_payload((Mode(mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_mode(self) -> Mode:
        """
        Returns the mode as set by :func:`set_mode`.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_MODE, response_expected=True)
        return Mode(unpack_payload(payload, "B"))
