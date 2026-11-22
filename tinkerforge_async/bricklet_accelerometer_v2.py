"""
Module for the Tinkerforge Accelerometer Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/AccelerometerV2_Bricklet_Python.html) implemented using
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
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    SimpleCallbackConfiguration,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ACCELERATION = 8
    CONTINUOUS_ACCELERATION_16_BIT = 11
    CONTINUOUS_ACCELERATION_8_BIT = 12


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ACCELERATION = 1
    SET_CONFIGURATION = 2
    GET_CONFIGURATION = 3
    SET_ACCELERATION_CALLBACK_CONFIGURATION = 4
    GET_ACCELERATION_CALLBACK_CONFIGURATION = 5
    SET_INFO_LED_CONFIG = 6
    GET_INFO_LED_CONFIG = 7
    SET_CONTINUOUS_ACCELERATION_CONFIGURATION = 9
    GET_CONTINUOUS_ACCELERATION_CONFIGURATION = 10
    SET_FILTER_CONFIGURATION = 13
    GET_FILTER_CONFIGURATION = 14


@unique
class DataRate(Enum):
    """
    The data rate options
    """

    DATA_RATE_0_781HZ = 0
    DATA_RATE_1_563HZ = 1
    DATA_RATE_3_125HZ = 2
    DATA_RATE_6_2512HZ = 3
    DATA_RATE_12_5HZ = 4
    DATA_RATE_25HZ = 5
    DATA_RATE_50HZ = 6
    DATA_RATE_100HZ = 7
    DATA_RATE_200HZ = 8
    DATA_RATE_400HZ = 9
    DATA_RATE_800HZ = 10
    DATA_RATE_1600HZ = 11
    DATA_RATE_3200HZ = 12
    DATA_RATE_6400HZ = 13
    DATA_RATE_12800HZ = 14
    DATA_RATE_25600HZ = 15


@unique
class FullScale(Enum):
    """
    The full scale options
    """

    FULL_SCALE_2G = 0
    FULL_SCALE_4G = 1
    FULL_SCALE_8G = 2


@unique
class InfoLEDConfig(Enum):
    """
    The info led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2


@unique
class Resolution(Enum):
    """
    The resolution options
    """

    RESOLUTION_8BIT = 0
    RESOLUTION_16BIT = 1


@unique
class IIRBypass(Enum):
    """
    The iir bypass options
    """

    APPLIED = 0
    BYPASSED = 1


@unique
class LowPassFilter(Enum):
    """
    The low pass filter options
    """

    NINTH = 0
    HALF = 1


class GetAcceleration(NamedTuple):
    x: Decimal
    y: Decimal
    z: Decimal


class GetConfiguration(NamedTuple):
    data_rate: DataRate
    full_scale: FullScale


class GetContinuousAccelerationConfiguration(NamedTuple):
    enable_x: bool
    enable_y: bool
    enable_z: bool
    resolution: Resolution


class GetFilterConfiguration(NamedTuple):
    iir_bypass: IIRBypass
    low_pass_filter: LowPassFilter


STANDARD_GRAVITY_1_10000 = LinearQuantity(196133, 200000000)  # raw: 1/10000 Standard Gravity, returned in m/s²


class BrickletAccelerometerV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures acceleration in three axis
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ACCELEROMETER_V2
    DEVICE_DISPLAY_NAME = "Accelerometer Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    DataRate: TypeAlias = DataRate
    FullScale: TypeAlias = FullScale
    InfoLEDConfig: TypeAlias = InfoLEDConfig
    Resolution: TypeAlias = Resolution
    IIRBypass: TypeAlias = IIRBypass
    LowPassFilter: TypeAlias = LowPassFilter

    CALLBACK_FORMATS = {
        CallbackID.ACCELERATION: "i i i",
        CallbackID.CONTINUOUS_ACCELERATION_16_BIT: "30h",
        CallbackID.CONTINUOUS_ACCELERATION_8_BIT: "60b",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.ACCELERATION,),
            configuration=ChannelConfiguration("acceleration", thresholds=False, wrap_advanced=True),
        ),
        Channel(1, callbacks=(CallbackID.CONTINUOUS_ACCELERATION_16_BIT,)),
        Channel(2, callbacks=(CallbackID.CONTINUOUS_ACCELERATION_8_BIT,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

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

    async def get_acceleration(self) -> GetAcceleration:
        """
        Returns the acceleration in x, y and z direction. The values
        are given in gₙ/10000 (1gₙ = 9.80665m/s²). The range is
        configured with :func:`set_configuration`.

        If you want to get the acceleration periodically, it is recommended
        to use the :attr:`CallbackID.ACCELERATION` callback and set the period with
        :func:`set_acceleration_callback_configuration`.

        Units: x in m/s², y in m/s², z in m/s².
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION, response_expected=True
        )
        x, y, z = unpack_payload(payload, "i i i")
        return GetAcceleration(
            STANDARD_GRAVITY_1_10000.to_si(x), STANDARD_GRAVITY_1_10000.to_si(y), STANDARD_GRAVITY_1_10000.to_si(z)
        )

    async def set_configuration(
        self,
        data_rate: DataRate | int = DataRate.DATA_RATE_100HZ,
        full_scale: FullScale | int = FullScale.FULL_SCALE_2G,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the data rate and full scale range.
        Possible values are:

        * Data rate of 0.781Hz to 25600Hz.
        * Full scale range of ±2g up to ±8g.

        Decreasing data rate or full scale range will also decrease the noise on
        the data.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((DataRate(data_rate).value, FullScale(full_scale).value), "B B"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        data_rate, full_scale = unpack_payload(payload, "B B")
        return GetConfiguration(DataRate(data_rate), FullScale(full_scale))

    async def set_acceleration_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ACCELERATION`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        If this callback is enabled, the :attr:`CallbackID.CONTINUOUS_ACCELERATION_16_BIT` callback
        and :attr:`CallbackID.CONTINUOUS_ACCELERATION_8_BIT` callback will automatically be disabled.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ACCELERATION_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_acceleration_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_acceleration_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_info_led_config(
        self, config: InfoLEDConfig | int = InfoLEDConfig.OFF, response_expected: bool = True
    ) -> None:
        """
        Configures the info LED (marked as "Force" on the Bricklet) to be either turned off,
        turned on, or blink in heartbeat mode.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_INFO_LED_CONFIG,
            data=pack_payload((InfoLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_info_led_config(self) -> InfoLEDConfig:
        """
        Returns the LED configuration as set by :func:`set_info_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_INFO_LED_CONFIG, response_expected=True
        )
        return InfoLEDConfig(unpack_payload(payload, "B"))

    async def set_continuous_acceleration_configuration(
        self,
        enable_x: bool = False,
        enable_y: bool = False,
        enable_z: bool = False,
        resolution: Resolution | int = Resolution.RESOLUTION_8BIT,
        response_expected: bool = True,
    ) -> None:
        """
        For high throughput of acceleration data (> 1000Hz) you have to use the
        :attr:`CallbackID.CONTINUOUS_ACCELERATION_16_BIT` or :attr:`CallbackID.CONTINUOUS_ACCELERATION_8_BIT`
        callbacks.

        You can enable the callback for each axis (x, y, z) individually and choose a
        resolution of 8 bit or 16 bit.

        If at least one of the axis is enabled and the resolution is set to 8 bit,
        the :attr:`CallbackID.CONTINUOUS_ACCELERATION_8_BIT` callback is activated. If at least
        one of the axis is enabled and the resolution is set to 16 bit,
        the :attr:`CallbackID.CONTINUOUS_ACCELERATION_16_BIT` callback is activated.

        The returned values are raw ADC data. If you want to put this data into
        a FFT to determine the occurrences of specific frequencies we recommend
        that you use the data as is. It has all of the ADC noise in it. This noise
        looks like pure noise at first glance, but it might still have some frequnecy
        information in it that can be utilized by the FFT.

        Otherwise you have to use the following formulas that depend on the configured
        resolution (8/16 bit) and the full scale range (see :func:`set_configuration`) to calculate
        the data in gₙ/10000 (same unit that is returned by :func:`get_acceleration`):

        * 16 bit, full scale 2g: acceleration = value * 625 / 1024
        * 16 bit, full scale 4g: acceleration = value * 1250 / 1024
        * 16 bit, full scale 8g: acceleration = value * 2500 / 1024

        If a resolution of 8 bit is used, only the 8 most significant bits will be
        transferred, so you can use the following formulas:

        * 8 bit, full scale 2g: acceleration = value * 256 * 625 / 1024
        * 8 bit, full scale 4g: acceleration = value * 256 * 1250 / 1024
        * 8 bit, full scale 8g: acceleration = value * 256 * 2500 / 1024

        If no axis is enabled, both callbacks are disabled. If one of the continuous
        callbacks is enabled, the :attr:`CallbackID.ACCELERATION` callback is disabled.

        The maximum throughput depends on the exact configuration:

        .. csv-table::
         :header: "Number of axis enabled", "Throughput 8 bit", "Throughout 16 bit"
         :widths: 20, 20, 20

         "1", "25600Hz", "25600Hz"
         "2", "25600Hz", "15000Hz"
         "3", "20000Hz", "10000Hz"
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONTINUOUS_ACCELERATION_CONFIGURATION,
            data=pack_payload(
                (bool(enable_x), bool(enable_y), bool(enable_z), Resolution(resolution).value), "! ! ! B"
            ),
            response_expected=response_expected,
        )

    async def get_continuous_acceleration_configuration(self) -> GetContinuousAccelerationConfiguration:
        """
        Returns the continuous acceleration configuration as set by
        :func:`set_continuous_acceleration_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONTINUOUS_ACCELERATION_CONFIGURATION, response_expected=True
        )
        enable_x, enable_y, enable_z, resolution = unpack_payload(payload, "! ! ! B")
        return GetContinuousAccelerationConfiguration(enable_x, enable_y, enable_z, Resolution(resolution))

    async def set_filter_configuration(
        self,
        iir_bypass: IIRBypass | int = IIRBypass.APPLIED,
        low_pass_filter: LowPassFilter | int = LowPassFilter.NINTH,
        response_expected: bool = True,
    ) -> None:
        """
        Configures IIR Bypass filter mode and low pass filter roll off corner frequency.

        The filter can be applied or bypassed and the corner frequency can be
        half or a ninth of the output data rate.

        .. image:: /Images/Bricklets/bricklet_accelerometer_v2_filter.png
           :scale: 100 %
           :alt: Accelerometer filter
           :align: center
           :target: ../../_images/Bricklets/bricklet_accelerometer_v2_filter.png

        .. versionadded:: 2.0.2 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FILTER_CONFIGURATION,
            data=pack_payload((IIRBypass(iir_bypass).value, LowPassFilter(low_pass_filter).value), "B B"),
            response_expected=response_expected,
        )

    async def get_filter_configuration(self) -> GetFilterConfiguration:
        """
        Returns the configuration as set by :func:`set_filter_configuration`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FILTER_CONFIGURATION, response_expected=True
        )
        iir_bypass, low_pass_filter = unpack_payload(payload, "B B")
        return GetFilterConfiguration(IIRBypass(iir_bypass), LowPassFilter(low_pass_filter))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.ACCELERATION:
            x, y, z = value
            return 0, GetAcceleration(
                STANDARD_GRAVITY_1_10000.to_si(x), STANDARD_GRAVITY_1_10000.to_si(y), STANDARD_GRAVITY_1_10000.to_si(z)
            )
        if callback_id is CallbackID.CONTINUOUS_ACCELERATION_16_BIT:
            return 1, tuple(value)
        return 2, tuple(value)
