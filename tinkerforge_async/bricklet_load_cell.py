"""
Module for the Tinkerforge Load Cell Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/LoadCell_Bricklet_Python.html) implemented using
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

    WEIGHT = 17
    WEIGHT_REACHED = 18


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_WEIGHT = 1
    SET_WEIGHT_CALLBACK_PERIOD = 2
    GET_WEIGHT_CALLBACK_PERIOD = 3
    SET_WEIGHT_CALLBACK_THRESHOLD = 4
    GET_WEIGHT_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_MOVING_AVERAGE = 8
    GET_MOVING_AVERAGE = 9
    LED_ON = 10
    LED_OFF = 11
    IS_LED_ON = 12
    CALIBRATE = 13
    TARE = 14
    SET_CONFIGURATION = 15
    GET_CONFIGURATION = 16


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


GRAM = LinearQuantity(1, 1000)  # raw: 1/1 Gram, returned in kg


class BrickletLoadCell(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures weight with a load cell
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_LOAD_CELL
    DEVICE_DISPLAY_NAME = "Load Cell Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Rate: TypeAlias = Rate
    Gain: TypeAlias = Gain

    CALLBACK_FORMATS = {
        CallbackID.WEIGHT: "i",
        CallbackID.WEIGHT_REACHED: "i",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_weight",
            callbacks=(
                CallbackID.WEIGHT,
                CallbackID.WEIGHT_REACHED,
            ),
            configuration=ChannelConfiguration("weight", split=True),
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

    async def get_weight(self) -> Decimal:
        """
        Returns the currently measured weight.

        If you want to get the weight periodically, it is recommended
        to use the :attr:`CallbackID.WEIGHT` callback and set the period with
        :func:`set_weight_callback_period`.

        Units: weight in kg.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WEIGHT, response_expected=True
        )
        return GRAM.to_si(unpack_payload(payload, "i"))

    async def set_weight_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.WEIGHT` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.WEIGHT` callback is only triggered if the weight has changed since the
        last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WEIGHT_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_weight_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_weight_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WEIGHT_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_weight_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.WEIGHT_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the weight is *outside* the min and max values"
         "'i'",    "Callback is triggered when the weight is *inside* the min and max values"
         "'<'",    "Callback is triggered when the weight is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the weight is greater than the min value (max is ignored)"

        Units: minimum in kg, maximum in kg.
        """
        minimum_raw = GRAM.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = GRAM.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WEIGHT_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c i i"),
            response_expected=response_expected,
        )

    async def get_weight_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_weight_callback_threshold`.

        Units: minimum in kg, maximum in kg.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WEIGHT_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        return BasicCallbackConfiguration(Threshold(option), GRAM.to_si(minimum), GRAM.to_si(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callback

        * :attr:`CallbackID.WEIGHT_REACHED`

        is triggered, if the threshold

        * :func:`set_weight_callback_threshold`

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

    async def set_moving_average(self, average: int = 4, response_expected: bool = True) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the weight value.

        Setting the length to 1 will turn the averaging off. With less
        averaging, there is more noise on the data.
        """
        average = int(average)
        check_range("average", average, 1, 40)
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

    async def led_on(self, response_expected: bool = True) -> None:
        """
        Turns the LED on.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.LED_ON, response_expected=response_expected)

    async def led_off(self, response_expected: bool = True) -> None:
        """
        Turns the LED off.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.LED_OFF, response_expected=response_expected)

    async def is_led_on(self) -> bool:
        """
        Returns *true* if the led is on, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_LED_ON, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def calibrate(self, weight: float | Decimal, response_expected: bool = True) -> None:
        """
        To calibrate your Load Cell Bricklet you have to

        * empty the scale and call this function with 0 and
        * add a known weight to the scale and call this function with the weight.

        The calibration is saved in the EEPROM of the Bricklet and only
        needs to be done once.

        We recommend to use the Brick Viewer for calibration, you don't need
        to call this function in your source code.

        Units: weight in kg.
        """
        weight_raw = GRAM.from_si(weight)
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

        The configuration is saved in the EEPROM of the Bricklet and only
        needs to be done once.

        We recommend to use the Brick Viewer for configuration, you don't need
        to call this function in your source code.
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

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.WEIGHT:
            return 0, GRAM.to_si(value)
        return 0, GRAM.to_si(value)
