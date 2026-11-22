"""
Module for the Tinkerforge Dust Detector Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DustDetector_Bricklet_Python.html) implemented using
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

    DUST_DENSITY = 8
    DUST_DENSITY_REACHED = 9


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_DUST_DENSITY = 1
    SET_DUST_DENSITY_CALLBACK_PERIOD = 2
    GET_DUST_DENSITY_CALLBACK_PERIOD = 3
    SET_DUST_DENSITY_CALLBACK_THRESHOLD = 4
    GET_DUST_DENSITY_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_MOVING_AVERAGE = 10
    GET_MOVING_AVERAGE = 11


MICRO_GRAM_PER_CUBIC_METER = LinearQuantity(1, 1000000000)  # raw: 1/1000000 Gram Per Cubic Meter, returned in kg/m³


class BrickletDustDetector(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures dust density
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DUST_DETECTOR
    DEVICE_DISPLAY_NAME = "Dust Detector Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.DUST_DENSITY: "H",
        CallbackID.DUST_DENSITY_REACHED: "H",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_dust_density",
            callbacks=(
                CallbackID.DUST_DENSITY,
                CallbackID.DUST_DENSITY_REACHED,
            ),
            configuration=ChannelConfiguration("dust_density", split=True),
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

    async def get_dust_density(self) -> Decimal:
        """
        Returns the dust density.

        If you want to get the dust density periodically, it is recommended
        to use the :attr:`CallbackID.DUST_DENSITY` callback and set the period with
        :func:`set_dust_density_callback_period`.

        Units: dust_density in kg/m³ (0 to 0.0000005 kg/m³).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DUST_DENSITY, response_expected=True
        )
        return MICRO_GRAM_PER_CUBIC_METER.to_si(unpack_payload(payload, "H"))

    async def set_dust_density_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.DUST_DENSITY` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.DUST_DENSITY` callback is only triggered if the dust density has
        changed since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DUST_DENSITY_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_dust_density_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_dust_density_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DUST_DENSITY_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_dust_density_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.DUST_DENSITY_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the dust density value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the dust density value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the dust density value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the dust density value is greater than the min value (max is ignored)"

        Units: minimum in kg/m³, maximum in kg/m³.
        """
        minimum_raw = MICRO_GRAM_PER_CUBIC_METER.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = MICRO_GRAM_PER_CUBIC_METER.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DUST_DENSITY_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c H H"),
            response_expected=response_expected,
        )

    async def get_dust_density_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_dust_density_callback_threshold`.

        Units: minimum in kg/m³, maximum in kg/m³.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DUST_DENSITY_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(
            Threshold(option), MICRO_GRAM_PER_CUBIC_METER.to_si(minimum), MICRO_GRAM_PER_CUBIC_METER.to_si(maximum)
        )

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callback

        * :attr:`CallbackID.DUST_DENSITY_REACHED`

        is triggered, if the threshold

        * :func:`set_dust_density_callback_threshold`

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

    async def set_moving_average(self, average: int = 100, response_expected: bool = True) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the dust density.

        Setting the length to 0 will turn the averaging completely off. With less
        averaging, there is more noise on the data.
        """
        average = int(average)
        check_range("average", average, 0, 100)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE,
            data=pack_payload((average,), "B"),
            response_expected=response_expected,
        )

    async def get_moving_average(self) -> int:
        """
        Returns the length moving average as set by :func:`set_moving_average`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOVING_AVERAGE, response_expected=True
        )
        return cast(int, unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.DUST_DENSITY:
            return 0, MICRO_GRAM_PER_CUBIC_METER.to_si(value)
        return 0, MICRO_GRAM_PER_CUBIC_METER.to_si(value)
