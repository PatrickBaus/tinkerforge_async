"""
Module for the Tinkerforge Industrial Dual 0-20mA Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Dual_020mA_V2.html) implemented using Python
asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles conversion of raw
units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from collections.abc import Iterable, Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    Event,
    LedConfig,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import Quantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    CURRENT = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_CURRENT = 1
    SET_CURRENT_CALLBACK_CONFIGURATION = 2
    GET_CURRENT_CALLBACK_CONFIGURATION = 3
    SET_SAMPLE_RATE = 5
    GET_SAMPLE_RATE = 6
    SET_GAIN = 7
    GET_GAIN = 8
    SET_CHANNEL_LED_CONFIG = 9
    GET_CHANNEL_LED_CONFIG = 10
    SET_CHANNEL_LED_STATUS_CONFIG = 11
    GET_CHANNEL_LED_STATUS_CONFIG = 12


@unique
class ChannelLedStatusConfig(Enum):
    """
    Defines the LED brightness when LedConfig.SHOW_STATUS
    """

    THRESHOLD = 0
    INTENSITY = 1


@unique
class SamplingRate(Enum):
    """
    Defines the sampling rate of the ADC. The resolution of the ADC depends on the sampling rate: 12 bit at 240 SPS,
    14 bit at 60 SPS, 16 bit at 15 SPS and 18 bit at 4 SPS.
    """

    RATE_240_SPS = 0
    RATE_60_SPS = 1
    RATE_15_SPS = 2
    RATE_4_SPS = 3


@unique
class Gain(Enum):
    """
    Defines the gain of the ADC
    """

    GAIN_1X = 0
    GAIN_2X = 1
    GAIN_4X = 2
    GAIN_8X = 3


class GetChannelLEDStatusConfig(NamedTuple):
    minimum: Decimal
    maximum: Decimal
    config: ChannelLedStatusConfig


CURRENT = Quantity(1_000_000_000)  # raw: nA


class BrickletIndustrialDual020mAV2(BrickletWithMCU):
    """
    Measures two currents between 0mA and 22.5mA (IEC 60381-1 compatible, so 4-20mA sensors work as well) with up to
    18bit resolution each. All currents are returned in A.
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_DUAL_0_20MA_V2
    DEVICE_DISPLAY_NAME = "Industrial Dual 0-20mA Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    ChannelLedConfig = LedConfig
    ChannelLedStatusConfig: TypeAlias = ChannelLedStatusConfig
    SamplingRate: TypeAlias = SamplingRate
    Gain: TypeAlias = Gain

    CALLBACK_FORMATS = {
        CallbackID.CURRENT: "B i",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_current",
            callbacks=(CallbackID.CURRENT,),
            configuration=ChannelConfiguration("current"),
            index=0,
        ),
        Channel(
            1,
            getter="get_current",
            callbacks=(CallbackID.CURRENT,),
            configuration=ChannelConfiguration("current"),
            index=1,
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP connection *ipcon*.
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
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        return await self._get_callback_configuration(sid)

    async def get_current(self, channel: int) -> Decimal:
        """
        Returns the current of the specified channel in A.

        It is possible to detect if an IEC 60381-1 compatible sensor is connected and if it works probably.

        If the returned current is below 4mA, there is likely no sensor connected or the connected sensor is defective.
        If the returned current is over 20mA, there might be a short circuit or the sensor is defective.

        If you want to get the value periodically, it is recommended to use the :cb:`Current` callback. You can set the
        callback configuration with :func:`Set Current Callback Configuration`.
        """
        if channel not in (0, 1):
            raise ValueError(f"Invalid argument: expected channel in (0, 1), got channel={channel!r}")

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CURRENT,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )
        return CURRENT.to_si(unpack_payload(payload, "i"))

    async def set_current_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        channel: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :cb:`Current` callback is triggered periodically. A value of 0 turns
        the callback off.

        If the `value has to change`-parameter is set to true, the callback is only triggered after the value has
        changed. If the value didn't change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period, independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Current` callback. The thresholds
        are given in A.

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
        if channel not in (0, 1):
            raise ValueError(f"Invalid argument: expected channel in (0, 1), got channel={channel!r}")
        option = Threshold(option)
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(channel),
                    seconds_to_ms(period),
                    bool(value_has_to_change),
                    option.value,
                    CURRENT.from_si(minimum),
                    CURRENT.from_si(maximum),
                ),
                "B I ! c i i",
            ),
            response_expected=response_expected,
        )

    async def get_current_callback_configuration(self, channel: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Current Callback Configuration`.
        """
        if channel not in (0, 1):
            raise ValueError(f"Invalid argument: expected channel in (0, 1), got channel={channel!r}")

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CURRENT_CALLBACK_CONFIGURATION,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            CURRENT.to_si(minimum),
            CURRENT.to_si(maximum),
        )

    async def set_sample_rate(self, rate: SamplingRate | int, response_expected: bool = True) -> None:
        """
        Sets the sample rate to either 240, 60, 15 or 4 samples per second. The resolution for the rates is 12, 14, 16
        and 18 bit respectively.

        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 100

         "0",    "240 samples per second, 12 bit resolution"
         "1",    "60 samples per second, 14 bit resolution"
         "2",    "15 samples per second, 16 bit resolution"
         "3",    "4 samples per second, 18 bit resolution"
        """
        rate = SamplingRate(rate)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SAMPLE_RATE,
            data=pack_payload((rate.value,), "B"),
            response_expected=response_expected,
        )

    async def get_sample_rate(self) -> SamplingRate:
        """
        Returns the sample rate as set by :func:`Set Sample Rate`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SAMPLE_RATE, response_expected=True
        )

        return SamplingRate(unpack_payload(payload, "B"))

    async def set_gain(self, gain: Gain | int, response_expected: bool = True) -> None:
        """
        Sets a gain between 1x and 8x. If you want to measure a very small current, you can increase the gain to get
        some more resolution.

        Example: If you measure 0.5mA with a gain of 8x the return value will be 4mA.
        """
        gain = Gain(gain)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GAIN,
            data=pack_payload((gain.value,), "B"),
            response_expected=response_expected,
        )

    async def get_gain(self) -> Gain:
        """
        Returns the gain as set by :func:`Set Gain`.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_GAIN, response_expected=True)

        return Gain(unpack_payload(payload, "B"))

    async def set_channel_led_config(
        self, channel: int, config: LedConfig | int, response_expected: bool = True
    ) -> None:
        """
        Each channel has a corresponding LED. You can turn the LED off, on or show a heartbeat. You can also set the LED
        to "Channel Status". In this mode the LED can either be turned on with a pre-defined threshold or the intensity
        of the LED can change with the measured value.

        You can configure the channel status behavior with :func:`Set Channel LED Status Config`.

        By default, all channel LEDs are configured as "Channel Status".
        """
        if channel not in (0, 1):
            raise ValueError(f"Invalid argument: expected channel in (0, 1), got channel={channel!r}")
        config = LedConfig(config)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_CONFIG,
            data=pack_payload((int(channel), config.value), "B B"),
            response_expected=response_expected,
        )

    async def get_channel_led_config(self, channel: int) -> LedConfig:
        """
        Returns the channel LED configuration as set by :func:`Set Channel LED Config`.
        """
        if channel not in (0, 1):
            raise ValueError(f"Invalid argument: expected channel in (0, 1), got channel={channel!r}")

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_CONFIG,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )

        return LedConfig(unpack_payload(payload, "B"))

    async def set_channel_led_status_config(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        channel: int,
        minimum: float | Decimal,
        maximum: float | Decimal,
        config: ChannelLedStatusConfig | int,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the channel LED status config. This config is used if the channel LED is configured as "Channel Status",
        see :func:`Set Channel LED Config`. The `minimum` and `maximum` values are given in A.

        For each channel you can choose between threshold and intensity mode.

        In threshold mode you can define a positive or a negative threshold. For a positive threshold set the "min"
        parameter to the threshold value in A above which the LED should turn on and set the "max" parameter to 0.
        Example: If you set a positive threshold of 10mA, the LED will turn on as soon as the current exceeds 10mA and
        turn off again if it goes below 10mA. For a negative threshold set the "max" parameter to the threshold value in
        A below which the LED should turn on and set the "min" parameter to 0. Example: If you set a negative threshold
        of 10mA, the LED will turn on as soon as the current goes below 10mA and the LED will turn off when the current
        exceeds 10mA.

        In intensity mode you can define a range in A that is used to scale the brightness of the LED. Example with
        min=4mA and max=20mA: The LED is off at 4mA and below, on at 20mA and above and the brightness is linearly
        scaled between the values 4mA and 20mA. If the min value is greater than the max value, the LED brightness is
        scaled the other way around.
        """
        if channel not in (0, 1):
            raise ValueError(f"Invalid argument: expected channel in (0, 1), got channel={channel!r}")
        config = ChannelLedStatusConfig(config)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_STATUS_CONFIG,
            data=pack_payload(
                (
                    int(channel),
                    CURRENT.from_si(minimum),
                    CURRENT.from_si(maximum),
                    config.value,
                ),
                "B i i B",
            ),
            response_expected=response_expected,
        )

    async def get_channel_led_status_config(self, channel: int) -> GetChannelLEDStatusConfig:
        """
        Returns the channel LED status configuration as set by :func:`Set Channel LED Status Config`.
        """
        if channel not in (0, 1):
            raise ValueError(f"Invalid argument: expected channel in (0, 1), got channel={channel!r}")

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_STATUS_CONFIG,
            data=pack_payload((int(channel),), "B"),
            response_expected=True,
        )

        minimum, maximum, config = unpack_payload(payload, "i i B")
        return GetChannelLEDStatusConfig(CURRENT.to_si(minimum), CURRENT.to_si(maximum), ChannelLedStatusConfig(config))

    def _to_events(self, callback_id: CallbackID, value: Any, sids: Sequence[int] | None) -> Iterable[Event]:
        channel, current = value
        if sids is not None and channel not in sids:
            # We got a reply from the wrong channel, maybe there is another callback running on that other
            # channel, so we ignore the value
            return ()
        return (Event(self, channel, callback_id, CURRENT.to_si(current)),)
