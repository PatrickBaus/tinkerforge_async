"""
Module for the Tinkerforge Hall Effect Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/HallEffectV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

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

    MAGNETIC_FLUX_DENSITY = 4
    COUNTER = 10


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_MAGNETIC_FLUX_DENSITY = 1
    SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION = 2
    GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION = 3
    GET_COUNTER = 5
    SET_COUNTER_CONFIG = 6
    GET_COUNTER_CONFIG = 7
    SET_COUNTER_CALLBACK_CONFIGURATION = 8
    GET_COUNTER_CALLBACK_CONFIGURATION = 9


class GetCounterConfig(NamedTuple):
    high_threshold: Decimal
    low_threshold: Decimal
    debounce: Decimal


MICRO_SECOND = LinearQuantity(1, 1000000)  # raw: 1/1000000 Second, returned in s
MICRO_TESLA = LinearQuantity(1, 1000000)  # raw: 1/1000000 Tesla, returned in T


class BrickletHallEffectV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures magnetic flux density between -7mT and +7mT
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_HALL_EFFECT_V2
    DEVICE_DISPLAY_NAME = "Hall Effect Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.MAGNETIC_FLUX_DENSITY: "h",
        CallbackID.COUNTER: "I",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_magnetic_flux_density",
            callbacks=(CallbackID.MAGNETIC_FLUX_DENSITY,),
            configuration=ChannelConfiguration("magnetic_flux_density"),
        ),
        Channel(
            1,
            callbacks=(CallbackID.COUNTER,),
            configuration=ChannelConfiguration("counter", thresholds=False, wrap_advanced=True),
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
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_magnetic_flux_density(self) -> Decimal:
        """
        Returns the `magnetic flux density (magnetic induction) <https://en.wikipedia.org/wiki/Magnetic_flux>`__.

        Units: magnetic_flux_density in T (-0.007 to 0.007 T).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETIC_FLUX_DENSITY, response_expected=True
        )
        return MICRO_TESLA.to_si(unpack_payload(payload, "h"))

    async def set_magnetic_flux_density_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.MAGNETIC_FLUX_DENSITY` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.MAGNETIC_FLUX_DENSITY`
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

        Units: minimum in T, maximum in T.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = MICRO_TESLA.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = MICRO_TESLA.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c h h"
            ),
            response_expected=response_expected,
        )

    async def get_magnetic_flux_density_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_magnetic_flux_density_callback_configuration`.

        Units: minimum in T, maximum in T.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            MICRO_TESLA.to_si(minimum),
            MICRO_TESLA.to_si(maximum),
        )

    async def get_counter(self, reset_counter: bool) -> int:
        """
        Returns the current value of the counter.

        You can configure the low/high thresholds and the debounce time
        with :func:`set_counter_config`.

        If you set reset counter to *true*, the count is set back to 0
        directly after it is read.

        If you want to get the count periodically, it is recommended to use the
        :attr:`CallbackID.COUNTER` callback. You can set the callback configuration
        with :func:`set_counter_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_COUNTER,
            data=pack_payload((bool(reset_counter),), "!"),
            response_expected=True,
        )
        return cast(int, unpack_payload(payload, "I"))

    async def set_counter_config(
        self,
        high_threshold: float | Decimal = Decimal("0.002"),
        low_threshold: float | Decimal = Decimal("-0.002"),
        debounce: float | Decimal = Decimal("0.1"),
        response_expected: bool = True,
    ) -> None:
        """
        Sets a high and a low threshold as well as a debounce time.

        If the measured magnetic flux density goes above the high threshold or
        below the low threshold, the count of the counter is increased by 1.

        The debounce time is the minimum time between two count increments.

        Units: high_threshold in T, low_threshold in T, debounce in s (0 to 1 s).
        """
        high_threshold_raw = MICRO_TESLA.from_si(high_threshold)
        check_range("high_threshold", high_threshold_raw, -32768, 32767, high_threshold)
        low_threshold_raw = MICRO_TESLA.from_si(low_threshold)
        check_range("low_threshold", low_threshold_raw, -32768, 32767, low_threshold)
        debounce_raw = MICRO_SECOND.from_si(debounce)
        check_range("debounce", debounce_raw, 0, 1000000, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COUNTER_CONFIG,
            data=pack_payload((high_threshold_raw, low_threshold_raw, debounce_raw), "h h I"),
            response_expected=response_expected,
        )

    async def get_counter_config(self) -> GetCounterConfig:
        """
        Returns the counter config as set by :func:`set_counter_config`.

        Units: high_threshold in T, low_threshold in T, debounce in s (0 to 1 s).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COUNTER_CONFIG, response_expected=True
        )
        high_threshold, low_threshold, debounce = unpack_payload(payload, "h h I")
        return GetCounterConfig(
            MICRO_TESLA.to_si(high_threshold), MICRO_TESLA.to_si(low_threshold), MICRO_SECOND.to_si(debounce)
        )

    async def set_counter_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.COUNTER`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after at least one of the values has changed. If the values didn't
        change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COUNTER_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_counter_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_counter_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COUNTER_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.MAGNETIC_FLUX_DENSITY:
            return 0, MICRO_TESLA.to_si(value)
        return 1, value
