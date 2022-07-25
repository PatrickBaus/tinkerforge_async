"""
Module for the Tinkerforge Temperature Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature_V2.html) implemented using Python asyncio. It does
the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, DeviceIdentifier, Event
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    TEMPERATURE = 4


_CallbackID = CallbackID


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


_HeaterConfig = HeaterConfig  # We need the alias for MyPy type hinting


class BrickletTemperatureV2(BrickletWithMCU):
    """
    Measures ambient temperature with 0.2 K accuracy
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_TEMPERATURE_V2
    DEVICE_DISPLAY_NAME = "Temperature Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    HeaterConfig = HeaterConfig

    CALLBACK_FORMATS = {
        CallbackID.TEMPERATURE: "h",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.TEMPERATURE,),
    }

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> Decimal:
        assert sid == 0

        return await self.get_temperature()

    async def set_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        sid: int,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        minimum = Decimal("273.15") if minimum is None else minimum
        maximum = Decimal("273.15") if maximum is None else maximum

        assert sid == 0

        await self.set_temperature_callback_configuration(
            period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        assert sid == 0

        return await self.get_temperature_callback_configuration()

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the sensor. The value
        has a range of -2500 to 8500 and is given in °C/100,
        e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

        If you want to get the temperature periodically, it is recommended
        to use the :cb:`Temperature` callback and set the period with
        :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return self.__value_to_si(unpack_payload(payload, "h"))

    async def set_temperature_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: Decimal | int | float = Decimal("273.15"),
        maximum: Decimal | int | float = Decimal("273.15"),
        response_expected=True,
    ) -> None:
        """
        The period in ms is the period with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Temperature` callback.

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

        The default value is (0, false, 'x', 0, 0).
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    self.__si_to_value(minimum),
                    self.__si_to_value(maximum),
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
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return AdvancedCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def set_heater_configuration(
        self, heater_config: _HeaterConfig | int = HeaterConfig.DISABLED, response_expected: bool = True
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

    async def get_heater_configuration(self) -> _HeaterConfig:
        """
        Returns the heater configuration as set by :func:`Set Heater Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HEATER_CONFIGURATION, response_expected=True
        )

        return HeaterConfig(unpack_payload(payload, "B"))

    @staticmethod
    def __value_to_si(value: int) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value + 27315) / 100

    @staticmethod
    def __si_to_value(value: float | Decimal) -> int:
        return int(value * 100) - 27315

    async def read_events(
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        registered_events = set()
        if events:
            for event in events:
                registered_events.add(self.CallbackID(event))
        if sids is not None:
            for sid in sids:
                for callback in self.SID_TO_CALLBACK.get(sid, []):
                    registered_events.add(callback)

        if events is None and sids is None:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                yield Event(self, 0, function_id, self.__value_to_si(value))
