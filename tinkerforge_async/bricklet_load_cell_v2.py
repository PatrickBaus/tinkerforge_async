"""
Module for the Tinkerforge Load Cell Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/LoadCellV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

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

    WEIGHT = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_WEIGHT = 1
    SET_WEIGHT_CALLBACK_CONFIGURATION = 2
    GET_WEIGHT_CALLBACK_CONFIGURATION = 3
    SET_MOVING_AVERAGE = 5
    GET_MOVING_AVERAGE = 6
    SET_INFO_LED_CONFIG = 7
    GET_INFO_LED_CONFIG = 8
    CALIBRATE = 9
    TARE = 10
    SET_CONFIGURATION = 11
    GET_CONFIGURATION = 12


@unique
class InfoLEDConfig(Enum):
    """
    The info led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2


@unique
class Rate(Enum):
    """
    The rate options
    """

    RATE_10HZ = 0
    RATE_80HZ = 1


@unique
class Gain(Enum):
    """
    The gain options
    """

    GAIN_128X = 0
    GAIN_64X = 1
    GAIN_32X = 2


class GetConfiguration(NamedTuple):
    rate: Rate
    gain: Gain


VALUE = LinearQuantity(1, 1000)  # raw: 1/1 Gram, returned in kg
WEIGHT = LinearQuantity(1, 1000)  # raw: 1/1 Gram, returned in kg


class BrickletLoadCellV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures weight with a load cell
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_LOAD_CELL_V2
    DEVICE_DISPLAY_NAME = "Load Cell Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    InfoLEDConfig: TypeAlias = InfoLEDConfig
    Rate: TypeAlias = Rate
    Gain: TypeAlias = Gain

    CALLBACK_FORMATS = {
        CallbackID.WEIGHT: "i",
    }

    CHANNELS = (
        Channel(0, getter="get_weight", callbacks=(CallbackID.WEIGHT,), configuration=ChannelConfiguration("weight")),
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
        option: Threshold | int = Threshold.OFF,
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

    async def get_weight(self) -> Decimal:
        """
        Returns the currently measured weight.

        Units: weight in kg.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WEIGHT, response_expected=True
        )
        return WEIGHT.to_si(unpack_payload(payload, "i"))

    async def set_weight_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.WEIGHT` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.WEIGHT` callback.

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

        Units: minimum in kg, maximum in kg.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = VALUE.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = VALUE.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WEIGHT_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
            ),
            response_expected=response_expected,
        )

    async def get_weight_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_weight_callback_configuration`.

        Units: minimum in kg, maximum in kg.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WEIGHT_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), VALUE.to_si(minimum), VALUE.to_si(maximum)
        )

    async def set_moving_average(self, average: int = 4, response_expected: bool = True) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the weight value.

        Setting the length to 1 will turn the averaging off. With less
        averaging, there is more noise on the data.
        """
        average = int(average)
        check_range("average", average, 1, 100)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE,
            data=pack_payload((average,), "H"),
            response_expected=response_expected,
        )

    async def get_moving_average(self) -> int:
        """
        Returns the length moving average as set by :func:`set_moving_average`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOVING_AVERAGE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_info_led_config(
        self, config: InfoLEDConfig | int = InfoLEDConfig.OFF, response_expected: bool = True
    ) -> None:
        """
        Configures the info LED to be either turned off, turned on, or blink in
        heartbeat mode.
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

    async def calibrate(self, weight: float | Decimal, response_expected: bool = True) -> None:
        """
        To calibrate your Load Cell Bricklet 2.0 you have to

        * empty the scale and call this function with 0 and
        * add a known weight to the scale and call this function with the weight.

        The calibration is saved in the flash of the Bricklet and only
        needs to be done once.

        We recommend to use the Brick Viewer for calibration, you don't need
        to call this function in your source code.

        Units: weight in kg.
        """
        weight_raw = WEIGHT.from_si(weight)
        check_range("weight", weight_raw, 0, 4294967295, weight)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.CALIBRATE,
            data=pack_payload((weight_raw,), "I"),
            response_expected=response_expected,
        )

    async def tare(self, response_expected: bool = True) -> None:
        """
        Sets the currently measured weight as tare weight.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.TARE, response_expected=response_expected)

    async def set_configuration(
        self, rate: Rate | int = Rate.RATE_10HZ, gain: Gain | int = Gain.GAIN_128X, response_expected: bool = True
    ) -> None:
        """
        The measurement rate and gain are configurable.

        The rate can be either 10Hz or 80Hz. A faster rate will produce more noise.
        It is additionally possible to add a moving average
        (see :func:`set_moving_average`) to the measurements.

        The gain can be 128x, 64x or 32x. It represents a measurement range of
        ±20mV, ±40mV and ±80mV respectively. The Load Cell Bricklet uses an
        excitation voltage of 5V and most load cells use an output of 2mV/V. That
        means the voltage range is ±15mV for most load cells (i.e. gain of 128x
        is best). If you don't know what all of this means you should keep it at
        128x, it will most likely be correct.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((Rate(rate).value, Gain(gain).value), "B B"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        rate, gain = unpack_payload(payload, "B B")
        return GetConfiguration(Rate(rate), Gain(gain))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, WEIGHT.to_si(value)
