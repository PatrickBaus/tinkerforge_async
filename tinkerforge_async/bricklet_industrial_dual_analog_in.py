"""
Module for the Tinkerforge Industrial Dual Analog In Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDualAnalogIn_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

from .devices import (
    AdvancedCallbackConfiguration,
    BasicCallbackConfiguration,
    Channel,
    ChannelConfiguration,
    Device,
    DeviceIdentifier,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    VOLTAGE = 13
    VOLTAGE_REACHED = 14


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_VOLTAGE = 1
    SET_VOLTAGE_CALLBACK_PERIOD = 2
    GET_VOLTAGE_CALLBACK_PERIOD = 3
    SET_VOLTAGE_CALLBACK_THRESHOLD = 4
    GET_VOLTAGE_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_SAMPLE_RATE = 8
    GET_SAMPLE_RATE = 9
    SET_CALIBRATION = 10
    GET_CALIBRATION = 11
    GET_ADC_VALUES = 12


@unique
class SampleRate(Enum):
    """
    The sample rate options
    """

    SAMPLE_RATE_976_SPS = 0
    SAMPLE_RATE_488_SPS = 1
    SAMPLE_RATE_244_SPS = 2
    SAMPLE_RATE_122_SPS = 3
    SAMPLE_RATE_61_SPS = 4
    SAMPLE_RATE_4_SPS = 5
    SAMPLE_RATE_2_SPS = 6
    SAMPLE_RATE_1_SPS = 7


class GetCalibration(NamedTuple):
    offset: tuple[int, ...]
    gain: tuple[int, ...]


MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletIndustrialDualAnalogIn(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures two DC voltages between -35V and +35V with 24bit resolution each
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_DUAL_ANALOG_IN
    DEVICE_DISPLAY_NAME = "Industrial Dual Analog In Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    SampleRate: TypeAlias = SampleRate

    CALLBACK_FORMATS = {
        CallbackID.VOLTAGE: "B i",
        CallbackID.VOLTAGE_REACHED: "B i",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_voltage",
            callbacks=(
                CallbackID.VOLTAGE,
                CallbackID.VOLTAGE_REACHED,
            ),
            configuration=ChannelConfiguration("voltage", split=True),
            index=0,
        ),
        Channel(
            1,
            getter="get_voltage",
            callbacks=(
                CallbackID.VOLTAGE,
                CallbackID.VOLTAGE_REACHED,
            ),
            configuration=ChannelConfiguration("voltage", split=True),
            index=1,
        ),
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

    async def get_voltage(self, channel: int) -> Decimal:
        """
        Returns the voltage for the given channel.

        If you want to get the voltage periodically, it is recommended to use the
        :attr:`CallbackID.VOLTAGE` callback and set the period with
        :func:`set_voltage_callback_period`.

        Units: voltage in V (-35 to 35 V).
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE, data=pack_payload((channel,), "B"), response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "i"))

    async def set_voltage_callback_period(
        self, channel: int, period: Duration = 0, response_expected: bool = True
    ) -> None:
        """
        Sets the period with which the :attr:`CallbackID.VOLTAGE` callback is triggered
        periodically for the given channel. A value of 0 turns the callback off.

        The :attr:`CallbackID.VOLTAGE` callback is only triggered if the voltage has changed since the
        last triggering.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_PERIOD,
            data=pack_payload((channel, period_raw), "B I"),
            response_expected=response_expected,
        )

    async def get_voltage_callback_period(self, channel: int) -> Decimal:
        """
        Returns the period as set by :func:`set_voltage_callback_period`.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_VOLTAGE_CALLBACK_PERIOD,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_voltage_callback_threshold(
        self,
        channel: int,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.VOLTAGE_REACHED` callback for the given
        channel.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
         "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
         "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

        Units: minimum in V, maximum in V.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
        minimum_raw = MILLI_VOLT.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = MILLI_VOLT.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
            data=pack_payload((channel, Threshold(option).value, minimum_raw, maximum_raw), "B c i i"),
            response_expected=response_expected,
        )

    async def get_voltage_callback_threshold(self, channel: int) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_voltage_callback_threshold`.

        Units: minimum in V, maximum in V.
        """
        channel = int(channel)
        check_range("channel", channel, 0, 1)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD,
            data=pack_payload((channel,), "B"),
            response_expected=True,
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        return BasicCallbackConfiguration(Threshold(option), MILLI_VOLT.to_si(minimum), MILLI_VOLT.to_si(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callback

        * :attr:`CallbackID.VOLTAGE_REACHED`

        is triggered, if the threshold

        * :func:`set_voltage_callback_threshold`

        keeps being reached.

        Units: debounce in s.
        """
        debounce_raw = seconds_to_ms(debounce)
        check_range("debounce", debounce_raw, 0, 4294967295, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((debounce_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> Decimal:
        """
        Returns the debounce period as set by :func:`set_debounce_period`.

        Units: debounce in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_sample_rate(
        self, rate: SampleRate | int = SampleRate.SAMPLE_RATE_2_SPS, response_expected: bool = True
    ) -> None:
        """
        Sets the sample rate. The sample rate can be between 1 sample per second
        and 976 samples per second. Decreasing the sample rate will also decrease the
        noise on the data.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SAMPLE_RATE,
            data=pack_payload((SampleRate(rate).value,), "B"),
            response_expected=response_expected,
        )

    async def get_sample_rate(self) -> SampleRate:
        """
        Returns the sample rate as set by :func:`set_sample_rate`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SAMPLE_RATE, response_expected=True
        )
        return SampleRate(unpack_payload(payload, "B"))

    async def set_calibration(self, offset: Sequence[int], gain: Sequence[int], response_expected: bool = True) -> None:
        """
        Sets offset and gain of MCP3911 internal calibration registers.

        See MCP3911 datasheet 7.7 and 7.8. The Industrial Dual Analog In Bricklet
        is already factory calibrated by Tinkerforge. It should not be necessary
        for you to use this function
        """
        check_length("offset", offset, 2)
        check_length("gain", gain, 2)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload((list(map(int, offset)), list(map(int, gain))), "2i 2i"),
            response_expected=response_expected,
        )

    async def get_calibration(self) -> GetCalibration:
        """
        Returns the calibration as set by :func:`set_calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CALIBRATION, response_expected=True
        )
        offset, gain = unpack_payload(payload, "2i 2i")
        return GetCalibration(tuple(offset), tuple(gain))

    async def get_adc_values(self) -> tuple[int, ...]:
        """
        Returns the ADC values as given by the MCP3911 IC. This function
        is needed for proper calibration, see :func:`set_calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ADC_VALUES, response_expected=True
        )
        return tuple(unpack_payload(payload, "2i"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.VOLTAGE:
            channel, voltage = value
            return channel, MILLI_VOLT.to_si(voltage)
        channel, voltage = value
        return channel, MILLI_VOLT.to_si(voltage)
