"""
Module for the Tinkerforge XMC1400 Breakout Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/XMC1400Breakout_Bricklet_Python.html) implemented using
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

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    SimpleCallbackConfiguration,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ADC_VALUES = 9
    COUNT = 13


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_GPIO_CONFIG = 1
    GET_GPIO_INPUT = 2
    SET_ADC_CHANNEL_CONFIG = 3
    GET_ADC_CHANNEL_CONFIG = 4
    GET_ADC_CHANNEL_VALUE = 5
    GET_ADC_VALUES = 6
    SET_ADC_VALUES_CALLBACK_CONFIGURATION = 7
    GET_ADC_VALUES_CALLBACK_CONFIGURATION = 8
    GET_COUNT = 10
    SET_COUNT_CALLBACK_CONFIGURATION = 11
    GET_COUNT_CALLBACK_CONFIGURATION = 12


@unique
class GPIOMode(Enum):
    """
    The gpio mode options
    """

    INPUT_TRISTATE = 0
    INPUT_PULL_DOWN = 1
    INPUT_PULL_UP = 2
    INPUT_SAMPLING = 3
    INPUT_INVERTED_TRISTATE = 4
    INPUT_INVERTED_PULL_DOWN = 5
    INPUT_INVERTED_PULL_UP = 6
    INPUT_INVERTED_SAMPLING = 7
    OUTPUT_PUSH_PULL = 8
    OUTPUT_OPEN_DRAIN = 9


@unique
class GPIOInputHysteresis(Enum):
    """
    The gpio input hysteresis options
    """

    STANDARD = 0
    LARGE = 4


class BrickletXMC1400Breakout(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Breakout for Infineon XMC1400 microcontroller
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_XMC1400_BREAKOUT
    DEVICE_DISPLAY_NAME = "XMC1400 Breakout Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    GPIOMode: TypeAlias = GPIOMode
    GPIOInputHysteresis: TypeAlias = GPIOInputHysteresis

    CALLBACK_FORMATS = {
        CallbackID.ADC_VALUES: "8H",
        CallbackID.COUNT: "I",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_adc_values",
            callbacks=(CallbackID.ADC_VALUES,),
            configuration=ChannelConfiguration("adc_values", thresholds=False, wrap_advanced=True),
        ),
        Channel(1, getter="get_count", callbacks=(CallbackID.COUNT,), configuration=ChannelConfiguration("count")),
    )

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

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def set_gpio_config(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        port: int,
        pin: int,
        mode: GPIOMode | int,
        input_hysteresis: GPIOInputHysteresis | int,
        output_level: bool,
        response_expected: bool = True,
    ) -> None:
        """
        Example for a setter function. The values are the values that can be given to
        the XMC_GPIO_Init function. See communication.c in the firmware.
        """
        port = int(port)
        check_range("port", port, 0, 4)
        pin = int(pin)
        check_range("pin", pin, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GPIO_CONFIG,
            data=pack_payload(
                (port, pin, GPIOMode(mode).value, GPIOInputHysteresis(input_hysteresis).value, bool(output_level)),
                "B B B B !",
            ),
            response_expected=response_expected,
        )

    async def get_gpio_input(self, port: int, pin: int) -> bool:
        """
        Example for a getter function. Returns the result of a
        XMC_GPIO_GetInput call for the given port/pin.
        """
        port = int(port)
        check_range("port", port, 0, 4)
        pin = int(pin)
        check_range("pin", pin, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_GPIO_INPUT,
            data=pack_payload((port, pin), "B B"),
            response_expected=True,
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def set_adc_channel_config(self, channel: int, enable: bool, response_expected: bool = True) -> None:
        """
        Enables a ADC channel for the ADC driver example (adc.c/adc.h).

        There are 8 ADC channels and they correspond to the following pins:

        * Channel 0: P2_6
        * Channel 1: P2_8
        * Channel 2: P2_9
        * Channel 3: P2_10
        * Channel 4: P2_11
        * Channel 5: P2_0
        * Channel 6: P2_1
        * Channel 7: P2_2
        """
        channel = int(channel)
        check_range("channel", channel, 0, 7)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ADC_CHANNEL_CONFIG,
            data=pack_payload((channel, bool(enable)), "B !"),
            response_expected=response_expected,
        )

    async def get_adc_channel_config(self, channel: int) -> bool:
        """
        Returns the config for the given channel as set by :func:`set_adc_channel_config`.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 7)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ADC_CHANNEL_CONFIG,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def get_adc_channel_value(self, channel: int) -> int:
        """
        Returns the 12-bit value of the given ADC channel of the ADC driver example.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 7)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ADC_CHANNEL_VALUE,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        return cast(int, unpack_payload(payload, "H"))

    async def get_adc_values(self) -> tuple[int, ...]:
        """
        Returns the values for all 8 ADC channels of the adc driver example.

        This example function also has a corresponding callback.

        See :func:`set_adc_values_callback_configuration` and :attr:`CallbackID.ADC_VALUES` callback.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ADC_VALUES, response_expected=True
        )
        return tuple(unpack_payload(payload, "8H"))

    async def set_adc_values_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ADC_VALUES`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ADC_VALUES_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_adc_values_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_adc_values_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ADC_VALUES_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def get_count(self) -> int:
        """
        Returns the value of the example count (see example.c).

        This example function uses the "add_callback_value_function"-helper in the
        generator. The getter as well as the callback and callback configuration
        functions are auto-generated for the API as well as the firmware.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COUNT, response_expected=True
        )
        return cast(int, unpack_payload(payload, "I"))

    async def set_count_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: int = 0,
        maximum: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.COUNT` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.COUNT` callback.

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
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum = int(minimum)
        check_range("minimum", minimum, 0, 4294967295)
        maximum = int(maximum)
        check_range("maximum", maximum, 0, 4294967295)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COUNT_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum, maximum), "I ! c I I"
            ),
            response_expected=response_expected,
        )

    async def get_count_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_count_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COUNT_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c I I")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), Decimal(minimum), Decimal(maximum)
        )

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.ADC_VALUES:
            return 0, tuple(value)
        return 1, value
