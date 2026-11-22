"""
Module for the Tinkerforge Laser Range Finder Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/LaserRangeFinderV2_Bricklet_Python.html) implemented using
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
    VELOCITY = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_DISTANCE = 1
    SET_DISTANCE_CALLBACK_CONFIGURATION = 2
    GET_DISTANCE_CALLBACK_CONFIGURATION = 3
    GET_VELOCITY = 5
    SET_VELOCITY_CALLBACK_CONFIGURATION = 6
    GET_VELOCITY_CALLBACK_CONFIGURATION = 7
    SET_ENABLE = 9
    GET_ENABLE = 10
    SET_CONFIGURATION = 11
    GET_CONFIGURATION = 12
    SET_MOVING_AVERAGE = 13
    GET_MOVING_AVERAGE = 14
    SET_OFFSET_CALIBRATION = 15
    GET_OFFSET_CALIBRATION = 16
    SET_DISTANCE_LED_CONFIG = 17
    GET_DISTANCE_LED_CONFIG = 18


@unique
class DistanceLEDConfig(Enum):
    """
    The distance led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_DISTANCE = 3


class GetConfiguration(NamedTuple):
    acquisition_count: int
    enable_quick_termination: bool
    threshold_value: int
    measurement_frequency: Decimal


class GetMovingAverage(NamedTuple):
    distance_average_length: int
    velocity_average_length: int


CENTI_METER = LinearQuantity(1, 100)  # raw: 1/100 Meter, returned in m
CENTI_METER_PER_SECOND = LinearQuantity(1, 100)  # raw: 1/100 Meter Per Second, returned in m/s
HERTZ = LinearQuantity(1)  # raw: 1/1 Hertz, returned in Hz


class BrickletLaserRangeFinderV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures distance up to 40m with laser light
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_LASER_RANGE_FINDER_V2
    DEVICE_DISPLAY_NAME = "Laser Range Finder Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    DistanceLEDConfig: TypeAlias = DistanceLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.DISTANCE: "h",
        CallbackID.VELOCITY: "h",
    }

    CHANNELS = (
        Channel(
            0, getter="get_distance", callbacks=(CallbackID.DISTANCE,), configuration=ChannelConfiguration("distance")
        ),
        Channel(
            1, getter="get_velocity", callbacks=(CallbackID.VELOCITY,), configuration=ChannelConfiguration("velocity")
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

    async def get_distance(self) -> Decimal:
        """
        Returns the measured distance.

        The laser has to be enabled, see :func:`set_enable`.

        Units: distance in m (0 to 40 m).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE, response_expected=True
        )
        return CENTI_METER.to_si(unpack_payload(payload, "h"))

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
        minimum_raw = CENTI_METER.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = CENTI_METER.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c h h"
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
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            CENTI_METER.to_si(minimum),
            CENTI_METER.to_si(maximum),
        )

    async def get_velocity(self) -> Decimal:
        """
        Returns the measured velocity. The value has a range of -12800 to 12700
        and is given in 1/100 m/s.

        The velocity measurement only produces stables results if a fixed
        measurement rate (see :func:`set_configuration`) is configured. Also the laser
        has to be enabled, see :func:`set_enable`.

        Units: velocity in m/s (-128 to 127 m/s).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VELOCITY, response_expected=True
        )
        return CENTI_METER_PER_SECOND.to_si(unpack_payload(payload, "h"))

    async def set_velocity_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.VELOCITY` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.VELOCITY` callback.

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

        Units: minimum in m/s, maximum in m/s.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = CENTI_METER_PER_SECOND.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = CENTI_METER_PER_SECOND.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VELOCITY_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c h h"
            ),
            response_expected=response_expected,
        )

    async def get_velocity_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_velocity_callback_configuration`.

        Units: minimum in m/s, maximum in m/s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VELOCITY_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            CENTI_METER_PER_SECOND.to_si(minimum),
            CENTI_METER_PER_SECOND.to_si(maximum),
        )

    async def set_enable(self, enable: bool = False, response_expected: bool = True) -> None:
        """
        Enables the laser of the LIDAR if set to *true*.

        We recommend that you wait 250ms after enabling the laser before
        the first call of :func:`get_distance` to ensure stable measurements.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ENABLE,
            data=pack_payload((bool(enable),), "!"),
            response_expected=response_expected,
        )

    async def get_enable(self) -> bool:
        """
        Returns the value as set by :func:`set_enable`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ENABLE, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def set_configuration(
        self,
        acquisition_count: int = 128,
        enable_quick_termination: bool = False,
        threshold_value: int = 0,
        measurement_frequency: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The **Acquisition Count** defines the number of times the Laser Range Finder Bricklet
        will integrate acquisitions to find a correlation record peak. With a higher count,
        the Bricklet can measure longer distances. With a lower count, the rate increases. The
        allowed values are 1-255.

        If you set **Enable Quick Termination** to true, the distance measurement will be terminated
        early if a high peak was already detected. This means that a higher measurement rate can be achieved
        and long distances can be measured at the same time. However, the chance of false-positive
        distance measurements increases.

        Normally the distance is calculated with a detection algorithm that uses peak value,
        signal strength and noise. You can however also define a fixed **Threshold Value**.
        Set this to a low value if you want to measure the distance to something that has
        very little reflection (e.g. glass) and set it to a high value if you want to measure
        the distance to something with a very high reflection (e.g. mirror). Set this to 0 to
        use the default algorithm. The other allowed values are 1-255.

        Set the **Measurement Frequency** to force a fixed measurement rate. If set to 0,
        the Laser Range Finder Bricklet will use the optimal frequency according to the other
        configurations and the actual measured distance. Since the rate is not fixed in this case,
        the velocity measurement is not stable. For a stable velocity measurement you should
        set a fixed measurement frequency. The lower the frequency, the higher is the resolution
        of the calculated velocity. The allowed values are 10Hz-500Hz (and 0 to turn the fixed
        frequency off).

        The default values for Acquisition Count, Enable Quick Termination, Threshold Value and
        Measurement Frequency are 128, false, 0 and 0.

        Units: measurement_frequency in Hz.
        """
        acquisition_count = int(acquisition_count)
        check_range("acquisition_count", acquisition_count, 1, 255)
        threshold_value = int(threshold_value)
        check_range("threshold_value", threshold_value, 0, 255)
        measurement_frequency_raw = HERTZ.from_si(measurement_frequency)
        check_range("measurement_frequency", measurement_frequency_raw, 0, 65535, measurement_frequency)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload(
                (acquisition_count, bool(enable_quick_termination), threshold_value, measurement_frequency_raw),
                "B ! B H",
            ),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.

        Units: measurement_frequency in Hz.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        acquisition_count, enable_quick_termination, threshold_value, measurement_frequency = unpack_payload(
            payload, "B ! B H"
        )
        return GetConfiguration(
            acquisition_count, enable_quick_termination, threshold_value, HERTZ.to_si(measurement_frequency)
        )

    async def set_moving_average(
        self, distance_average_length: int = 10, velocity_average_length: int = 10, response_expected: bool = True
    ) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the distance and velocity.

        Setting the length to 0 will turn the averaging completely off. With less
        averaging, there is more noise on the data.
        """
        distance_average_length = int(distance_average_length)
        check_range("distance_average_length", distance_average_length, 0, 255)
        velocity_average_length = int(velocity_average_length)
        check_range("velocity_average_length", velocity_average_length, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE,
            data=pack_payload((distance_average_length, velocity_average_length), "B B"),
            response_expected=response_expected,
        )

    async def get_moving_average(self) -> GetMovingAverage:
        """
        Returns the length moving average as set by :func:`set_moving_average`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOVING_AVERAGE, response_expected=True
        )
        distance_average_length, velocity_average_length = unpack_payload(payload, "B B")
        return GetMovingAverage(distance_average_length, velocity_average_length)

    async def set_offset_calibration(self, offset: float | Decimal, response_expected: bool = True) -> None:
        """
        The offset is added to the measured distance.
        It is saved in non-volatile memory, you only have to set it once.

        The Bricklet comes with a per-sensor factory-calibrated offset value,
        you should not have to call this function.

        If you want to re-calibrate the offset you first have to set it to 0.
        Calculate the offset by measuring the distance to a known distance
        and set it again.

        Units: offset in m.
        """
        offset_raw = CENTI_METER.from_si(offset)
        check_range("offset", offset_raw, -32768, 32767, offset)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_OFFSET_CALIBRATION,
            data=pack_payload((offset_raw,), "h"),
            response_expected=response_expected,
        )

    async def get_offset_calibration(self) -> Decimal:
        """
        Returns the offset value as set by :func:`set_offset_calibration`.

        Units: offset in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OFFSET_CALIBRATION, response_expected=True
        )
        return CENTI_METER.to_si(unpack_payload(payload, "h"))

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
        if callback_id is CallbackID.DISTANCE:
            return 0, CENTI_METER.to_si(value)
        return 1, CENTI_METER_PER_SECOND.to_si(value)
