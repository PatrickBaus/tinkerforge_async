"""
Module for the Tinkerforge Accelerometer Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/Accelerometer_Bricklet_Python.html) implemented using
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

from .devices import Channel, Device, DeviceIdentifier
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ACCELERATION = 14
    ACCELERATION_REACHED = 15


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ACCELERATION = 1
    SET_ACCELERATION_CALLBACK_PERIOD = 2
    GET_ACCELERATION_CALLBACK_PERIOD = 3
    SET_ACCELERATION_CALLBACK_THRESHOLD = 4
    GET_ACCELERATION_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    GET_TEMPERATURE = 8
    SET_CONFIGURATION = 9
    GET_CONFIGURATION = 10
    LED_ON = 11
    LED_OFF = 12
    IS_LED_ON = 13


@unique
class DataRate(Enum):
    """
    The data rate options
    """

    OFF = 0
    DATA_RATE_3HZ = 1
    DATA_RATE_6HZ = 2
    DATA_RATE_12HZ = 3
    DATA_RATE_25HZ = 4
    DATA_RATE_50HZ = 5
    DATA_RATE_100HZ = 6
    DATA_RATE_400HZ = 7
    DATA_RATE_800HZ = 8
    DATA_RATE_1600HZ = 9


@unique
class FullScale(Enum):
    """
    The full scale options
    """

    FULL_SCALE_2G = 0
    FULL_SCALE_4G = 1
    FULL_SCALE_6G = 2
    FULL_SCALE_8G = 3
    FULL_SCALE_16G = 4


@unique
class FilterBandwidth(Enum):
    """
    The filter bandwidth options
    """

    FILTER_BANDWIDTH_800HZ = 0
    FILTER_BANDWIDTH_400HZ = 1
    FILTER_BANDWIDTH_200HZ = 2
    FILTER_BANDWIDTH_50HZ = 3


class GetAcceleration(NamedTuple):
    x: Decimal
    y: Decimal
    z: Decimal


class GetAccelerationCallbackThreshold(NamedTuple):
    option: Threshold
    min_x: Decimal
    max_x: Decimal
    min_y: Decimal
    max_y: Decimal
    min_z: Decimal
    max_z: Decimal


class GetConfiguration(NamedTuple):
    data_rate: DataRate
    full_scale: FullScale
    filter_bandwidth: FilterBandwidth


TEMPERATURE_2 = LinearQuantity(1, 1, CELSIUS_ZERO)  # raw: 1/1 Degree Celsius, returned in K
X = LinearQuantity(196133, 20000000)  # raw: 1/1000 Standard Gravity, returned in m/s²
Y = LinearQuantity(196133, 20000000)  # raw: 1/1000 Standard Gravity, returned in m/s²
Z = LinearQuantity(196133, 20000000)  # raw: 1/1000 Standard Gravity, returned in m/s²


class BrickletAccelerometer(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures acceleration in three axis
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ACCELEROMETER
    DEVICE_DISPLAY_NAME = "Accelerometer Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    DataRate: TypeAlias = DataRate
    FullScale: TypeAlias = FullScale
    FilterBandwidth: TypeAlias = FilterBandwidth

    CALLBACK_FORMATS = {
        CallbackID.ACCELERATION: "h h h",
        CallbackID.ACCELERATION_REACHED: "h h h",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.ACCELERATION,)),
        Channel(1, callbacks=(CallbackID.ACCELERATION_REACHED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_acceleration(self) -> GetAcceleration:
        """
        Returns the acceleration in x, y and z direction. The values
        are given in gₙ/1000 (1gₙ = 9.80665m/s²). The range is
        configured with :func:`set_configuration`.

        If you want to get the acceleration periodically, it is recommended
        to use the :attr:`CallbackID.ACCELERATION` callback and set the period with
        :func:`set_acceleration_callback_period`.

        Units: x in m/s², y in m/s², z in m/s².
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetAcceleration(X.to_si(x), Y.to_si(y), Z.to_si(z))

    async def set_acceleration_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ACCELERATION` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.ACCELERATION` callback is only triggered if the acceleration has
        changed since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ACCELERATION_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_acceleration_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_acceleration_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_acceleration_callback_threshold(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        option: Threshold | str = Threshold.OFF,
        min_x: float | Decimal = 0,
        max_x: float | Decimal = 0,
        min_y: float | Decimal = 0,
        max_y: float | Decimal = 0,
        min_z: float | Decimal = 0,
        max_z: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.ACCELERATION_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the acceleration is *outside* the min and max values"
         "'i'",    "Callback is triggered when the acceleration is *inside* the min and max values"
         "'<'",    "Callback is triggered when the acceleration is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the acceleration is greater than the min value (max is ignored)"

        Units: min_x in m/s², max_x in m/s², min_y in m/s², max_y in m/s², min_z in m/s², max_z in m/s².
        """
        min_x_raw = X.from_si(min_x)
        check_range("min_x", min_x_raw, -32768, 32767, min_x)
        max_x_raw = X.from_si(max_x)
        check_range("max_x", max_x_raw, -32768, 32767, max_x)
        min_y_raw = Y.from_si(min_y)
        check_range("min_y", min_y_raw, -32768, 32767, min_y)
        max_y_raw = Y.from_si(max_y)
        check_range("max_y", max_y_raw, -32768, 32767, max_y)
        min_z_raw = Z.from_si(min_z)
        check_range("min_z", min_z_raw, -32768, 32767, min_z)
        max_z_raw = Z.from_si(max_z)
        check_range("max_z", max_z_raw, -32768, 32767, max_z)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ACCELERATION_CALLBACK_THRESHOLD,
            data=pack_payload(
                (Threshold(option).value, min_x_raw, max_x_raw, min_y_raw, max_y_raw, min_z_raw, max_z_raw),
                "c h h h h h h",
            ),
            response_expected=response_expected,
        )

    async def get_acceleration_callback_threshold(self) -> GetAccelerationCallbackThreshold:
        """
        Returns the threshold as set by :func:`set_acceleration_callback_threshold`.

        Units: min_x in m/s², max_x in m/s², min_y in m/s², max_y in m/s², min_z in m/s², max_z in m/s².
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION_CALLBACK_THRESHOLD, response_expected=True
        )
        option, min_x, max_x, min_y, max_y, min_z, max_z = unpack_payload(payload, "c h h h h h h")
        return GetAccelerationCallbackThreshold(
            Threshold(option),
            X.to_si(min_x),
            X.to_si(max_x),
            Y.to_si(min_y),
            Y.to_si(max_y),
            Z.to_si(min_z),
            Z.to_si(max_z),
        )

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callback

        * :attr:`CallbackID.ACCELERATION_REACHED`

        is triggered, if the threshold

        * :func:`set_acceleration_callback_threshold`

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

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the accelerometer.

        Units: temperature in K (170.15 to 425.15 K).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE_2.to_si(unpack_payload(payload, "h"))

    async def set_configuration(
        self,
        data_rate: DataRate | int = DataRate.DATA_RATE_100HZ,
        full_scale: FullScale | int = FullScale.FULL_SCALE_4G,
        filter_bandwidth: FilterBandwidth | int = FilterBandwidth.FILTER_BANDWIDTH_200HZ,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the data rate, full scale range and filter bandwidth.
        Possible values are:

        * Data rate of 0Hz to 1600Hz.
        * Full scale range of ±2gₙ up to ±16gₙ.
        * Filter bandwidth between 50Hz and 800Hz.

        Decreasing data rate or full scale range will also decrease the noise on
        the data.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload(
                (DataRate(data_rate).value, FullScale(full_scale).value, FilterBandwidth(filter_bandwidth).value),
                "B B B",
            ),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        data_rate, full_scale, filter_bandwidth = unpack_payload(payload, "B B B")
        return GetConfiguration(DataRate(data_rate), FullScale(full_scale), FilterBandwidth(filter_bandwidth))

    async def led_on(self, response_expected: bool = True) -> None:
        """
        Enables the LED on the Bricklet.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.LED_ON, response_expected=response_expected)

    async def led_off(self, response_expected: bool = True) -> None:
        """
        Disables the LED on the Bricklet.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.LED_OFF, response_expected=response_expected)

    async def is_led_on(self) -> bool:
        """
        Returns *true* if the LED is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_LED_ON, response_expected=True
        )
        return unpack_payload(payload, "!")

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.ACCELERATION:
            x, y, z = value
            return 0, GetAcceleration(X.to_si(x), Y.to_si(y), Z.to_si(z))
        x, y, z = value
        return 1, GetAcceleration(X.to_si(x), Y.to_si(y), Z.to_si(z))
