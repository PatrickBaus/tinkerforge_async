"""
Module for the Tinkerforge Industrial Analog Out Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialAnalogOutV2_Bricklet_Python.html) implemented using
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

from .devices import BrickletWithMCU, DeviceIdentifier, _FunctionID
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

    SET_ENABLED = 1
    GET_ENABLED = 2
    SET_VOLTAGE = 3
    GET_VOLTAGE = 4
    SET_CURRENT = 5
    GET_CURRENT = 6
    SET_CONFIGURATION = 7
    GET_CONFIGURATION = 8
    SET_OUT_LED_CONFIG = 9
    GET_OUT_LED_CONFIG = 10
    SET_OUT_LED_STATUS_CONFIG = 11
    GET_OUT_LED_STATUS_CONFIG = 12


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


@unique
class OutLEDConfig(Enum):
    """
    The out led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_OUT_STATUS = 3


@unique
class OutLEDStatusConfig(Enum):
    """
    The out led status config options
    """

    THRESHOLD = 0
    INTENSITY = 1


class GetConfiguration(NamedTuple):
    voltage_range: VoltageRange
    current_range: CurrentRange


class GetOutLEDStatusConfig(NamedTuple):
    minimum: int
    maximum: int
    config: OutLEDStatusConfig


CURRENT = LinearQuantity(1, 1000000)  # raw: 1/1000000 Ampere, returned in A
VOLTAGE = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletIndustrialAnalogOutV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Generates configurable DC voltage and current, 0V to 10V and 4mA to 20mA
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_ANALOG_OUT_V2
    DEVICE_DISPLAY_NAME = "Industrial Analog Out Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    VoltageRange: TypeAlias = VoltageRange
    CurrentRange: TypeAlias = CurrentRange
    OutLEDConfig: TypeAlias = OutLEDConfig
    OutLEDStatusConfig: TypeAlias = OutLEDStatusConfig

    CALLBACK_FORMATS = {}

    SID_TO_CALLBACK = {}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_enabled(self, enabled: bool = False, response_expected: bool = True) -> None:
        """
        Enables/disables the output of voltage and current.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ENABLED,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_enabled(self) -> bool:
        """
        Returns *true* if output of voltage and current is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_voltage(self, voltage: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets the output voltage.

        The output voltage and output current are linked. Changing the output voltage
        also changes the output current.

        Units: voltage in V (0 to 10 V).
        """
        voltage_raw = VOLTAGE.from_si(voltage)
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
        return VOLTAGE.to_si(unpack_payload(payload, "H"))

    async def set_current(self, current: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets the output current.

        The output current and output voltage are linked. Changing the output current
        also changes the output voltage.

        Units: current in A (0 to 0.024 A).
        """
        current_raw = CURRENT.from_si(current)
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
        return CURRENT.to_si(unpack_payload(payload, "H"))

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

    async def set_out_led_config(
        self, config: OutLEDConfig | int = OutLEDConfig.SHOW_OUT_STATUS, response_expected: bool = True
    ) -> None:
        """
        You can turn the Out LED off, on or show a
        heartbeat. You can also set the LED to "Out Status". In this mode the
        LED can either be turned on with a pre-defined threshold or the intensity
        of the LED can change with the output value (voltage or current).

        You can configure the channel status behavior with :func:`set_out_led_status_config`.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_OUT_LED_CONFIG,
            data=pack_payload((OutLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_out_led_config(self) -> OutLEDConfig:
        """
        Returns the Out LED configuration as set by :func:`set_out_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OUT_LED_CONFIG, response_expected=True
        )
        return OutLEDConfig(unpack_payload(payload, "B"))

    async def set_out_led_status_config(
        self,
        minimum: int = 0,
        maximum: int = 10000,
        config: OutLEDStatusConfig | int = OutLEDStatusConfig.INTENSITY,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the Out LED status config. This config is used if the Out LED is
        configured as "Out Status", see :func:`set_out_led_config`.

        For each channel you can choose between threshold and intensity mode.

        In threshold mode you can define a positive or a negative threshold.
        For a positive threshold set the "min" parameter to the threshold value in V or
        µA above which the LED should turn on and set the "max" parameter to 0. Example:
        If you set a positive threshold of 5V, the LED will turn on as soon as the
        output value exceeds 5V and turn off again if it goes below 5V.
        For a negative threshold set the "max" parameter to the threshold value in V or
        µA below which the LED should turn on and set the "min" parameter to 0. Example:
        If you set a negative threshold of 5V, the LED will turn on as soon as the
        output value goes below 5V and the LED will turn off when the output value
        exceeds 5V.

        In intensity mode you can define a range mV or µA that is used to scale the brightness
        of the LED. Example with min=2V, max=8V: The LED is off at 2V and below, on at
        8V and above and the brightness is linearly scaled between the values 2V and 8V.
        If the min value is greater than the max value, the LED brightness is scaled the
        other way around.
        """
        minimum = int(minimum)
        check_range("minimum", minimum, 0, 24000)
        maximum = int(maximum)
        check_range("maximum", maximum, 0, 24000)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_OUT_LED_STATUS_CONFIG,
            data=pack_payload((minimum, maximum, OutLEDStatusConfig(config).value), "H H B"),
            response_expected=response_expected,
        )

    async def get_out_led_status_config(self) -> GetOutLEDStatusConfig:
        """
        Returns the Out LED status configuration as set by :func:`set_out_led_status_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OUT_LED_STATUS_CONFIG, response_expected=True
        )
        minimum, maximum, config = unpack_payload(payload, "H H B")
        return GetOutLEDStatusConfig(minimum, maximum, OutLEDStatusConfig(config))
