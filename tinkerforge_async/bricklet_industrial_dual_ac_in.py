"""
Module for the Tinkerforge Industrial Dual AC In Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDualACIn_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
)
from .devices import Channel as ChannelDefinition
from .devices import ChannelConfiguration, DeviceIdentifier, SimpleCallbackConfiguration
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

    VALUE = 8
    ALL_VALUE = 9


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_VALUE = 1
    SET_VALUE_CALLBACK_CONFIGURATION = 2
    GET_VALUE_CALLBACK_CONFIGURATION = 3
    SET_ALL_VALUE_CALLBACK_CONFIGURATION = 4
    GET_ALL_VALUE_CALLBACK_CONFIGURATION = 5
    SET_CHANNEL_LED_CONFIG = 6
    GET_CHANNEL_LED_CONFIG = 7


@unique
class Channel(Enum):
    """
    The channel options
    """

    CHANNEL_0 = 0
    CHANNEL_1 = 1


@unique
class ChannelLEDConfig(Enum):
    """
    The channel led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_CHANNEL_STATUS = 3


class ValueEvent(NamedTuple):
    channel: Channel
    changed: bool
    value: bool


class AllValueEvent(NamedTuple):
    changed: tuple[bool, ...]
    value: tuple[bool, ...]


class BrickletIndustrialDualACIn(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    2 inputs that can detect AC voltages of up to 230V
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_DUAL_AC_IN
    DEVICE_DISPLAY_NAME = "Industrial Dual AC In Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Channel: TypeAlias = Channel
    ChannelLEDConfig: TypeAlias = ChannelLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.VALUE: "B ! !",
        CallbackID.ALL_VALUE: "2! 2!",
    }

    CHANNELS = (
        ChannelDefinition(0, callbacks=(CallbackID.VALUE,)),
        ChannelDefinition(
            1,
            callbacks=(CallbackID.ALL_VALUE,),
            configuration=ChannelConfiguration("all_value", thresholds=False, wrap_advanced=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

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
        return await self._get_callback_configuration(sid)

    async def get_value(self) -> tuple[bool, ...]:
        """
        Returns the input values as bools, *true* refers to "AC voltage detected" and *false* refers to no "AC voltage
        detected".
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VALUE, response_expected=True
        )
        return tuple(unpack_payload(payload, "2!"))

    async def set_value_callback_configuration(
        self,
        channel: Channel | int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        response_expected: bool = True,
    ) -> None:
        """
        This callback can be configured per channel.

        The period is the period with which the :attr:`CallbackID.VALUE`
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
            function_id=FunctionID.SET_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload((Channel(channel).value, period_raw, bool(value_has_to_change)), "B I !"),
            response_expected=response_expected,
        )

    async def get_value_callback_configuration(self, channel: Channel | int) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration for the given channel as set by
        :func:`set_value_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload((Channel(channel).value,), "B"),
            response_expected=True,
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_all_value_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ALL_VALUE`
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
            function_id=FunctionID.SET_ALL_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_all_value_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_all_value_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_VALUE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_channel_led_config(
        self,
        channel: Channel | int,
        config: ChannelLEDConfig | int = ChannelLEDConfig.SHOW_CHANNEL_STATUS,
        response_expected: bool = True,
    ) -> None:
        """
        Each channel has a corresponding LED. You can turn the LED off, on or show a
        heartbeat. You can also set the LED to "Channel Status". In this mode the
        LED is on if the channel is high and off otherwise.

        By default all channel LEDs are configured as "Channel Status".
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_CONFIG,
            data=pack_payload((Channel(channel).value, ChannelLEDConfig(config).value), "B B"),
            response_expected=response_expected,
        )

    async def get_channel_led_config(self, channel: Channel | int) -> ChannelLEDConfig:
        """
        Returns the channel LED configuration as set by :func:`set_channel_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_CONFIG,
            data=pack_payload((Channel(channel).value,), "B"),
            response_expected=True,
        )
        return ChannelLEDConfig(unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.VALUE:
            channel, changed, value = value
            return 0, ValueEvent(Channel(channel), changed, value)
        changed, value = value
        return 1, AllValueEvent(tuple(changed), tuple(value))
