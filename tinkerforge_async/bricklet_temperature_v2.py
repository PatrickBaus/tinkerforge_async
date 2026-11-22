"""
Module for the Tinkerforge Temperature Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature_V2.html) implemented using Python asyncio. It does
the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, TypeAlias, override

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, Channel, ChannelConfiguration, DeviceIdentifier
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, TEMPERATURE

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    TEMPERATURE = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_TEMPERATURE = 1
    SET_TEMPERATURE_CALLBACK_CONFIGURATION = 2
    GET_TEMPERATURE_CALLBACK_CONFIGURATION = 3
    SET_HEATER_CONFIGURATION = 5
    GET_HEATER_CONFIGURATION = 6


@unique
class HeaterConfig(Enum):
    """
    The builtin heater can be used for testing purposes
    """

    DISABLED = 0
    ENABLED = 1


class BrickletTemperatureV2(BrickletWithMCU):
    """
    Measures ambient temperature with 0.2 K accuracy
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_TEMPERATURE_V2
    DEVICE_DISPLAY_NAME = "Temperature Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    HeaterConfig: TypeAlias = HeaterConfig

    CALLBACK_FORMATS = {
        CallbackID.TEMPERATURE: "h",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_temperature",
            callbacks=(CallbackID.TEMPERATURE,),
            configuration=ChannelConfiguration("temperature", default=CELSIUS_ZERO),
        ),
    )

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> Decimal:
        return await self._get_value(sid)

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
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        return await self._get_callback_configuration(sid)

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the sensor in K. The value has a range of 248.15 to 358.15 K,
        e.g. a value of 315.38 K means that a temperature of 315.38 K is measured.

        If you want to get the temperature periodically, it is recommended
        to use the :cb:`Temperature` callback and set the period with
        :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "h"))

    async def set_temperature_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: Decimal | int | float = CELSIUS_ZERO,
        maximum: Decimal | int | float = CELSIUS_ZERO,
        response_expected=True,
    ) -> None:
        """
        The period in s is the period with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Temperature` callback. The
        thresholds are given in K.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"


        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 273.15, 273.15).
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    seconds_to_ms(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    TEMPERATURE.from_si(minimum),
                    TEMPERATURE.from_si(maximum),
                ),
                "I ! c h h",
            ),
            response_expected=response_expected,
        )

    async def get_temperature_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        option = Threshold(option)
        minimum, maximum = TEMPERATURE.to_si(minimum), TEMPERATURE.to_si(maximum)
        return AdvancedCallbackConfiguration(ms_to_seconds(period), value_has_to_change, option, minimum, maximum)

    async def set_heater_configuration(
        self, heater_config: HeaterConfig | int = HeaterConfig.DISABLED, response_expected: bool = True
    ) -> None:
        """
        Enables/disables the heater. The heater can be used to test the sensor.
        """
        if not isinstance(heater_config, HeaterConfig):
            heater_config = HeaterConfig(int(heater_config))

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HEATER_CONFIGURATION,
            data=pack_payload((heater_config.value,), "B"),
            response_expected=response_expected,
        )

    async def get_heater_configuration(self) -> HeaterConfig:
        """
        Returns the heater configuration as set by :func:`Set Heater Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HEATER_CONFIGURATION, response_expected=True
        )

        return HeaterConfig(unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, TEMPERATURE.to_si(value)
