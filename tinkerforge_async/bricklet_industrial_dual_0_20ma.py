"""
Module for the Tinkerforge Industrial Dual 0-20mA Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDual020mA_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias, override

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

    CURRENT = 10
    CURRENT_REACHED = 11


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_CURRENT = 1
    SET_CURRENT_CALLBACK_PERIOD = 2
    GET_CURRENT_CALLBACK_PERIOD = 3
    SET_CURRENT_CALLBACK_THRESHOLD = 4
    GET_CURRENT_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_SAMPLE_RATE = 8
    GET_SAMPLE_RATE = 9


@unique
class SampleRate(Enum):
    """
    The sample rate options
    """

    SAMPLE_RATE_240_SPS = 0
    SAMPLE_RATE_60_SPS = 1
    SAMPLE_RATE_15_SPS = 2
    SAMPLE_RATE_4_SPS = 3


NANO_AMPERE = LinearQuantity(1, 1000000000)  # raw: 1/1000000000 Ampere, returned in A


class BrickletIndustrialDual020mA(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures two DC currents between 0mA and 20mA (IEC 60381-1)
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_DUAL_0_20MA
    DEVICE_DISPLAY_NAME = "Industrial Dual 0-20mA Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    SampleRate: TypeAlias = SampleRate

    CALLBACK_FORMATS = {
        CallbackID.CURRENT: "B i",
        CallbackID.CURRENT_REACHED: "B i",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_current",
            callbacks=(
                CallbackID.CURRENT,
                CallbackID.CURRENT_REACHED,
            ),
            configuration=ChannelConfiguration("current", split=True),
            index=0,
        ),
        Channel(
            1,
            getter="get_current",
            callbacks=(
                CallbackID.CURRENT,
                CallbackID.CURRENT_REACHED,
            ),
            configuration=ChannelConfiguration("current", split=True),
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

    async def get_current(self, sensor: int) -> Decimal:
        """
        Returns the current of the specified sensor.

        It is possible to detect if an IEC 60381-1 compatible sensor is connected
        and if it works properly.

        If the returned current is below 4mA, there is likely no sensor connected
        or the sensor may be defect. If the returned current is over 20mA, there might
        be a short circuit or the sensor may be defect.

        If you want to get the current periodically, it is recommended to use the
        :attr:`CallbackID.CURRENT` callback and set the period with
        :func:`set_current_callback_period`.

        Units: current in A (0 to 0.022505322 A).
        """
        sensor = int(sensor)
        check_range("sensor", sensor, 0, 1)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT, data=pack_payload((sensor,), "B"), response_expected=True
        )
        return NANO_AMPERE.to_si(unpack_payload(payload, "i"))

    async def set_current_callback_period(
        self, sensor: int, period: Duration = 0, response_expected: bool = True
    ) -> None:
        """
        Sets the period with which the :attr:`CallbackID.CURRENT` callback is triggered
        periodically for the given sensor. A value of 0 turns the callback off.

        The :attr:`CallbackID.CURRENT` callback is only triggered if the current has changed since the
        last triggering.
        """
        sensor = int(sensor)
        check_range("sensor", sensor, 0, 1)
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_CALLBACK_PERIOD,
            data=pack_payload((sensor, period_raw), "B I"),
            response_expected=response_expected,
        )

    async def get_current_callback_period(self, sensor: int) -> Decimal:
        """
        Returns the period as set by :func:`set_current_callback_period`.
        """
        sensor = int(sensor)
        check_range("sensor", sensor, 0, 1)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CURRENT_CALLBACK_PERIOD,
            data=pack_payload((sensor,), "B"),
            response_expected=True,
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_current_callback_threshold(
        self,
        sensor: int,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.CURRENT_REACHED` callback for the given
        sensor.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the current is *outside* the min and max values"
         "'i'",    "Callback is triggered when the current is *inside* the min and max values"
         "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"

        Units: minimum in A, maximum in A.
        """
        sensor = int(sensor)
        check_range("sensor", sensor, 0, 1)
        minimum_raw = NANO_AMPERE.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = NANO_AMPERE.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_CALLBACK_THRESHOLD,
            data=pack_payload((sensor, Threshold(option).value, minimum_raw, maximum_raw), "B c i i"),
            response_expected=response_expected,
        )

    async def get_current_callback_threshold(self, sensor: int) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_current_callback_threshold`.

        Units: minimum in A, maximum in A.
        """
        sensor = int(sensor)
        check_range("sensor", sensor, 0, 1)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CURRENT_CALLBACK_THRESHOLD,
            data=pack_payload((sensor,), "B"),
            response_expected=True,
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        return BasicCallbackConfiguration(Threshold(option), NANO_AMPERE.to_si(minimum), NANO_AMPERE.to_si(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callback

        * :attr:`CallbackID.CURRENT_REACHED`

        is triggered, if the threshold

        * :func:`set_current_callback_threshold`

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
        self, rate: SampleRate | int = SampleRate.SAMPLE_RATE_4_SPS, response_expected: bool = True
    ) -> None:
        """
        Sets the sample rate to either 240, 60, 15 or 4 samples per second.
        The resolution for the rates is 12, 14, 16 and 18 bit respectively.

        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 100

         "0",    "240 samples per second, 12 bit resolution"
         "1",    "60 samples per second, 14 bit resolution"
         "2",    "15 samples per second, 16 bit resolution"
         "3",    "4 samples per second, 18 bit resolution"
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

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.CURRENT:
            channel, current = value
            return channel, NANO_AMPERE.to_si(current)
        channel, current = value
        return channel, NANO_AMPERE.to_si(current)
