"""
Module for the Tinkerforge Analog Out Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/AnalogOutV2_Bricklet_Python.html) implemented using
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

    SET_OUTPUT_VOLTAGE = 1
    GET_OUTPUT_VOLTAGE = 2
    GET_INPUT_VOLTAGE = 3


MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletAnalogOutV2(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Generates configurable DC voltage between 0V and 12V
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ANALOG_OUT_V2
    DEVICE_DISPLAY_NAME = "Analog Out Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {}

    SID_TO_CALLBACK = {}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_output_voltage(self, voltage: float | Decimal = 0, response_expected: bool = True) -> None:
        """
        Sets the voltage.

        Units: voltage in V (0 to 12 V).
        """
        voltage_raw = MILLI_VOLT.from_si(voltage)
        check_range("voltage", voltage_raw, 0, 12000, voltage)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_OUTPUT_VOLTAGE,
            data=pack_payload((voltage_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_output_voltage(self) -> Decimal:
        """
        Returns the voltage as set by :func:`set_output_voltage`.

        Units: voltage in V (0 to 12 V).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OUTPUT_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def get_input_voltage(self) -> Decimal:
        """
        Returns the input voltage.

        Units: voltage in V (0 to 15 V).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_INPUT_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))
