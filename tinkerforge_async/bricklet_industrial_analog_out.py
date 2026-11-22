"""
Module for the Tinkerforge Industrial Analog Out Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialAnalogOut_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, NamedTuple, TypeAlias

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

    ENABLE = 1
    DISABLE = 2
    IS_ENABLED = 3
    SET_VOLTAGE = 4
    GET_VOLTAGE = 5
    SET_CURRENT = 6
    GET_CURRENT = 7
    SET_CONFIGURATION = 8
    GET_CONFIGURATION = 9


@unique
class VoltageRange(Enum):
    """
    The voltage range options
    """

    VOLTAGE_RANGE_0_TO_5V = 0
    VOLTAGE_RANGE_0_TO_10V = 1


@unique
class CurrentRange(Enum):
    """
    The current range options
    """

    CURRENT_RANGE_4_TO_20MA = 0
    CURRENT_RANGE_0_TO_20MA = 1
    CURRENT_RANGE_0_TO_24MA = 2


class GetConfiguration(NamedTuple):
    voltage_range: VoltageRange
    current_range: CurrentRange


MICRO_AMPERE = LinearQuantity(1, 1000000)  # raw: 1/1000000 Ampere, returned in A
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletIndustrialAnalogOut(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Generates configurable DC voltage and current, 0V to 10V and 4mA to 20mA
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_ANALOG_OUT
    DEVICE_DISPLAY_NAME = "Industrial Analog Out Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    VoltageRange: TypeAlias = VoltageRange
    CurrentRange: TypeAlias = CurrentRange

    CALLBACK_FORMATS = {}

    SID_TO_CALLBACK = {}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def enable(self, response_expected: bool = True) -> None:
        """
        Enables the output of voltage and current.

        The default is disabled.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.ENABLE, response_expected=response_expected)

    async def disable(self, response_expected: bool = True) -> None:
        """
        Disables the output of voltage and current.

        The default is disabled.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.DISABLE, response_expected=response_expected)

    async def is_enabled(self) -> bool:
        """
        Returns *true* if output of voltage and current is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_voltage(self, voltage: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets the output voltage.

        The output voltage and output current are linked. Changing the output voltage
        also changes the output current.

        Units: voltage in V (0 to 10 V).
        """
        voltage_raw = MILLI_VOLT.from_si(voltage)
        check_range("voltage", voltage_raw, 0, 10000, voltage)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE,
            data=pack_payload((voltage_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_voltage(self) -> Decimal:
        """
        Returns the voltage as set by :func:`set_voltage`.

        Units: voltage in V (0 to 10 V).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def set_current(self, current: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets the output current.

        The output current and output voltage are linked. Changing the output current
        also changes the output voltage.

        Units: current in A (0 to 0.024 A).
        """
        current_raw = MICRO_AMPERE.from_si(current)
        check_range("current", current_raw, 0, 24000, current)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT,
            data=pack_payload((current_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_current(self) -> Decimal:
        """
        Returns the current as set by :func:`set_current`.

        Units: current in A (0 to 0.024 A).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT, response_expected=True
        )
        return MICRO_AMPERE.to_si(unpack_payload(payload, "H"))

    async def set_configuration(
        self,
        voltage_range: VoltageRange | int = VoltageRange.VOLTAGE_RANGE_0_TO_10V,
        current_range: CurrentRange | int = CurrentRange.CURRENT_RANGE_4_TO_20MA,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the voltage and current range.

        Possible voltage ranges are:

        * 0V to 5V
        * 0V to 10V

        Possible current ranges are:

        * 4mA to 20mA
        * 0mA to 20mA
        * 0mA to 24mA

        The resolution will always be 12 bit. This means, that the
        precision is higher with a smaller range.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((VoltageRange(voltage_range).value, CurrentRange(current_range).value), "B B"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        voltage_range, current_range = unpack_payload(payload, "B B")
        return GetConfiguration(VoltageRange(voltage_range), CurrentRange(current_range))
