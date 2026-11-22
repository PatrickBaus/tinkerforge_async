"""
Module for the Tinkerforge Distance US Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DistanceUSV2_Bricklet_Python.html) implemented using
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

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, Channel, ChannelConfiguration, DeviceIdentifier
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

    DISTANCE = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_DISTANCE = 1
    SET_DISTANCE_CALLBACK_CONFIGURATION = 2
    GET_DISTANCE_CALLBACK_CONFIGURATION = 3
    SET_UPDATE_RATE = 5
    GET_UPDATE_RATE = 6
    SET_DISTANCE_LED_CONFIG = 7
    GET_DISTANCE_LED_CONFIG = 8


@unique
class UpdateRate(Enum):
    """
    The update rate options
    """

    UPDATE_RATE_2_HZ = 0
    UPDATE_RATE_10_HZ = 1


@unique
class DistanceLEDConfig(Enum):
    """
    The distance led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_DISTANCE = 3


MILLI_METER = LinearQuantity(1, 1000)  # raw: 1/1000 Meter, returned in m


class BrickletDistanceUSV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures distance between 0.3 m and 5 m with ultrasound
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DISTANCE_US_V2
    DEVICE_DISPLAY_NAME = "Distance US Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    UpdateRate: TypeAlias = UpdateRate
    DistanceLEDConfig: TypeAlias = DistanceLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.DISTANCE: "H",
    }

    CHANNELS = (
        Channel(
            0, getter="get_distance", callbacks=(CallbackID.DISTANCE,), configuration=ChannelConfiguration("distance")
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

    async def get_distance(self) -> Decimal:
        """
        Returns the distance.

        Units: distance in m (0.3 to 5 m).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE, response_expected=True
        )
        return MILLI_METER.to_si(unpack_payload(payload, "H"))

    async def set_distance_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.DISTANCE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.DISTANCE` callback.

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

        Units: minimum in m, maximum in m.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = MILLI_METER.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = MILLI_METER.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c H H"
            ),
            response_expected=response_expected,
        )

    async def get_distance_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_distance_callback_configuration`.

        Units: minimum in m, maximum in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            MILLI_METER.to_si(minimum),
            MILLI_METER.to_si(maximum),
        )

    async def set_update_rate(
        self, update_rate: UpdateRate | int = UpdateRate.UPDATE_RATE_2_HZ, response_expected: bool = True
    ) -> None:
        """
        Sets the update rate to 2 Hz or 10 Hz.

        With 2 Hz update rate the noise is about ±0.001 m, while with 10 Hz update rate the noise
        increases to about ±0.005 m.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_UPDATE_RATE,
            data=pack_payload((UpdateRate(update_rate).value,), "B"),
            response_expected=response_expected,
        )

    async def get_update_rate(self) -> UpdateRate:
        """
        Returns the update rate as set by :func:`set_update_rate`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_UPDATE_RATE, response_expected=True
        )
        return UpdateRate(unpack_payload(payload, "B"))

    async def set_distance_led_config(
        self, config: DistanceLEDConfig | int = DistanceLEDConfig.SHOW_DISTANCE, response_expected: bool = True
    ) -> None:
        """
        Configures the distance LED to be either turned off, turned on, blink in
        heartbeat mode or show the distance (brighter = object is nearer).
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_LED_CONFIG,
            data=pack_payload((DistanceLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_distance_led_config(self) -> DistanceLEDConfig:
        """
        Returns the LED configuration as set by :func:`set_distance_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_LED_CONFIG, response_expected=True
        )
        return DistanceLEDConfig(unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, MILLI_METER.to_si(value)
