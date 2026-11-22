"""
Module for the Tinkerforge Temperature IR Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/TemperatureIRV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias, cast, override

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, Channel, ChannelConfiguration, DeviceIdentifier
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    AMBIENT_TEMPERATURE = 4
    OBJECT_TEMPERATURE = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_AMBIENT_TEMPERATURE = 1
    SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION = 2
    GET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION = 3
    GET_OBJECT_TEMPERATURE = 5
    SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION = 6
    GET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION = 7
    SET_EMISSIVITY = 9
    GET_EMISSIVITY = 10


DECI_DEGREE_CELSIUS = LinearQuantity(1, 10, CELSIUS_ZERO)  # raw: 1/10 Degree Celsius, returned in K
RATIO_1_65535 = LinearQuantity(1, 65535)  # raw: 1/65535, dimensionless


class BrickletTemperatureIRV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures contactless object temperature between 203.15 K and 653.15 K
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_TEMPERATURE_IR_V2
    DEVICE_DISPLAY_NAME = "Temperature IR Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.AMBIENT_TEMPERATURE: "h",
        CallbackID.OBJECT_TEMPERATURE: "h",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_ambient_temperature",
            callbacks=(CallbackID.AMBIENT_TEMPERATURE,),
            configuration=ChannelConfiguration("ambient_temperature", default=CELSIUS_ZERO),
        ),
        Channel(
            1,
            getter="get_object_temperature",
            callbacks=(CallbackID.OBJECT_TEMPERATURE,),
            configuration=ChannelConfiguration("object_temperature", default=CELSIUS_ZERO),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> Any:
        """
        Returns the value of the channel with the secondary id `sid`. See `CHANNELS` for the channels.
        """
        return await self._get_value(sid)

    @override
    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the callbacks of the channel with the secondary id `sid`. The thresholds are ignored by
        channels without thresholds.
        """
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    @override
    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_ambient_temperature(self) -> Decimal:
        """
        Returns the ambient temperature of the sensor.

        Units: temperature in K (233.15 to 398.15 K).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AMBIENT_TEMPERATURE, response_expected=True
        )
        return DECI_DEGREE_CELSIUS.to_si(unpack_payload(payload, "h"))

    async def set_ambient_temperature_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = Decimal("273.15"),
        maximum: float | Decimal = Decimal("273.15"),
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.AMBIENT_TEMPERATURE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.AMBIENT_TEMPERATURE`
        callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in K, maximum in K.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = DECI_DEGREE_CELSIUS.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = DECI_DEGREE_CELSIUS.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c h h"
            ),
            response_expected=response_expected,
        )

    async def get_ambient_temperature_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_ambient_temperature_callback_configuration`.

        Units: minimum in K, maximum in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AMBIENT_TEMPERATURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            DECI_DEGREE_CELSIUS.to_si(minimum),
            DECI_DEGREE_CELSIUS.to_si(maximum),
        )

    async def get_object_temperature(self) -> Decimal:
        """
        Returns the object temperature of the sensor, i.e. the temperature
        of the surface of the object the sensor is aimed at.

        The temperature of different materials is dependent on their `emissivity
        <https://en.wikipedia.org/wiki/Emissivity>`__. The emissivity of the material
        can be set with :func:`set_emissivity`.

        Units: temperature in K (203.15 to 653.15 K).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OBJECT_TEMPERATURE, response_expected=True
        )
        return DECI_DEGREE_CELSIUS.to_si(unpack_payload(payload, "h"))

    async def set_object_temperature_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = Decimal("273.15"),
        maximum: float | Decimal = Decimal("273.15"),
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.OBJECT_TEMPERATURE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.OBJECT_TEMPERATURE`
        callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in K, maximum in K.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = DECI_DEGREE_CELSIUS.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = DECI_DEGREE_CELSIUS.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c h h"
            ),
            response_expected=response_expected,
        )

    async def get_object_temperature_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_object_temperature_callback_configuration`.

        Units: minimum in K, maximum in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            DECI_DEGREE_CELSIUS.to_si(minimum),
            DECI_DEGREE_CELSIUS.to_si(maximum),
        )

    async def set_emissivity(self, emissivity: float | Decimal = 1, response_expected: bool = True) -> None:
        """
        Sets the `emissivity <https://en.wikipedia.org/wiki/Emissivity>`__ that is
        used to calculate the surface temperature as returned by
        :func:`get_object_temperature`.

        The emissivity is usually given as a value between 0.0 and 1.0. A list of
        emissivities of different materials can be found
        `here <https://www.infrared-thermography.com/material.htm>`__.

        The parameter of :func:`set_emissivity` has to be given with a factor of
        65535 (16-bit). For example: An emissivity of 0.1 can be set with the
        value 6553, an emissivity of 0.5 with the value 32767 and so on.

        .. note::
         If you need a precise measurement for the object temperature, it is
         absolutely crucial that you also provide a precise emissivity.

        The emissivity is stored in non-volatile memory and will still be
        used after a restart or power cycle of the Bricklet.
        """
        emissivity_raw = RATIO_1_65535.from_si(emissivity)
        check_range("emissivity", emissivity_raw, 0, 65535, emissivity)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EMISSIVITY,
            data=pack_payload((emissivity_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_emissivity(self) -> Decimal:
        """
        Returns the emissivity as set by :func:`set_emissivity`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_EMISSIVITY, response_expected=True
        )
        return RATIO_1_65535.to_si(unpack_payload(payload, "H"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.AMBIENT_TEMPERATURE:
            return 0, DECI_DEGREE_CELSIUS.to_si(value)
        return 1, DECI_DEGREE_CELSIUS.to_si(value)
