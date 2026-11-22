"""
Module for the Tinkerforge Laser Range Finder Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/LaserRangeFinder_Bricklet_Python.html) implemented using
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

    DISTANCE = 20
    VELOCITY = 21
    DISTANCE_REACHED = 22
    VELOCITY_REACHED = 23


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_DISTANCE = 1
    GET_VELOCITY = 2
    SET_DISTANCE_CALLBACK_PERIOD = 3
    GET_DISTANCE_CALLBACK_PERIOD = 4
    SET_VELOCITY_CALLBACK_PERIOD = 5
    GET_VELOCITY_CALLBACK_PERIOD = 6
    SET_DISTANCE_CALLBACK_THRESHOLD = 7
    GET_DISTANCE_CALLBACK_THRESHOLD = 8
    SET_VELOCITY_CALLBACK_THRESHOLD = 9
    GET_VELOCITY_CALLBACK_THRESHOLD = 10
    SET_DEBOUNCE_PERIOD = 11
    GET_DEBOUNCE_PERIOD = 12
    SET_MOVING_AVERAGE = 13
    GET_MOVING_AVERAGE = 14
    SET_MODE = 15
    GET_MODE = 16
    ENABLE_LASER = 17
    DISABLE_LASER = 18
    IS_LASER_ENABLED = 19
    GET_SENSOR_HARDWARE_VERSION = 24
    SET_CONFIGURATION = 25
    GET_CONFIGURATION = 26


@unique
class Mode(Enum):
    """
    The mode options
    """

    DISTANCE = 0
    VELOCITY_MAX_13MS = 1
    VELOCITY_MAX_32MS = 2
    VELOCITY_MAX_64MS = 3
    VELOCITY_MAX_127MS = 4


@unique
class Version(Enum):
    """
    The version options
    """

    VERSION_1 = 1
    VERSION_3 = 3


class GetMovingAverage(NamedTuple):
    distance_average_length: int
    velocity_average_length: int


class GetConfiguration(NamedTuple):
    acquisition_count: int
    enable_quick_termination: bool
    threshold_value: int
    measurement_frequency: Decimal


DISTANCE = LinearQuantity(1, 100)  # raw: 1/100 Meter, returned in m
MEASUREMENT_FREQUENCY = LinearQuantity(1)  # raw: 1/1 Hertz, returned in Hz
VALUE = LinearQuantity(1, 100)  # raw: 1/100 Meter Per Second, returned in m/s
VELOCITY = LinearQuantity(1, 100)  # raw: 1/100 Meter Per Second, returned in m/s


class BrickletLaserRangeFinder(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures distance up to 40m with laser light
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_LASER_RANGE_FINDER
    DEVICE_DISPLAY_NAME = "Laser Range Finder Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Mode: TypeAlias = Mode
    Version: TypeAlias = Version

    CALLBACK_FORMATS = {
        CallbackID.DISTANCE: "H",
        CallbackID.VELOCITY: "h",
        CallbackID.DISTANCE_REACHED: "H",
        CallbackID.VELOCITY_REACHED: "h",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_distance",
            callbacks=(
                CallbackID.DISTANCE,
                CallbackID.DISTANCE_REACHED,
            ),
            configuration=ChannelConfiguration("distance", split=True),
        ),
        Channel(
            1,
            getter="get_velocity",
            callbacks=(
                CallbackID.VELOCITY,
                CallbackID.VELOCITY_REACHED,
            ),
            configuration=ChannelConfiguration("velocity", split=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

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

    async def get_distance(self) -> Decimal:
        """
        Returns the measured distance.

        Sensor hardware version 1 (see :func:`get_sensor_hardware_version`) cannot
        measure distance and velocity at the same time. Therefore, the distance mode
        has to be enabled using :func:`set_mode`.
        Sensor hardware version 3 can measure distance and velocity at the same
        time. Also the laser has to be enabled, see :func:`enable_laser`.

        If you want to get the distance periodically, it is recommended to
        use the :attr:`CallbackID.DISTANCE` callback and set the period with
        :func:`set_distance_callback_period`.

        Units: distance in m (0 to 40 m).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE, response_expected=True
        )
        return DISTANCE.to_si(unpack_payload(payload, "H"))

    async def get_velocity(self) -> Decimal:
        """
        Returns the measured velocity.

        Sensor hardware version 1 (see :func:`get_sensor_hardware_version`) cannot
        measure distance and velocity at the same time. Therefore, the velocity mode
        has to be enabled using :func:`set_mode`.
        Sensor hardware version 3 can measure distance and velocity at the same
        time, but the velocity measurement only produces stables results if a fixed
        measurement rate (see :func:`set_configuration`) is configured. Also the laser
        has to be enabled, see :func:`enable_laser`.

        If you want to get the velocity periodically, it is recommended to
        use the :attr:`CallbackID.VELOCITY` callback and set the period with
        :func:`set_velocity_callback_period`.

        Units: velocity in m/s (-128 to 127 m/s).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VELOCITY, response_expected=True
        )
        return VELOCITY.to_si(unpack_payload(payload, "h"))

    async def set_distance_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.DISTANCE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.DISTANCE` callback is only triggered if the distance value has
        changed since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_distance_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_distance_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_velocity_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.VELOCITY` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.VELOCITY` callback is only triggered if the velocity value has
        changed since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VELOCITY_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_velocity_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_velocity_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VELOCITY_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_distance_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.DISTANCE_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the distance value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the distance value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the distance value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the distance value is greater than the min value (max is ignored)"

        Units: minimum in m, maximum in m.
        """
        minimum_raw = DISTANCE.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = DISTANCE.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c H H"),
            response_expected=response_expected,
        )

    async def get_distance_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_distance_callback_threshold`.

        Units: minimum in m, maximum in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(Threshold(option), DISTANCE.to_si(minimum), DISTANCE.to_si(maximum))

    async def set_velocity_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.VELOCITY_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the velocity is *outside* the min and max values"
         "'i'",    "Callback is triggered when the velocity is *inside* the min and max values"
         "'<'",    "Callback is triggered when the velocity is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the velocity is greater than the min value (max is ignored)"

        Units: minimum in m/s, maximum in m/s.
        """
        minimum_raw = VALUE.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = VALUE.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VELOCITY_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c h h"),
            response_expected=response_expected,
        )

    async def get_velocity_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_velocity_callback_threshold`.

        Units: minimum in m/s, maximum in m/s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VELOCITY_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c h h")
        return BasicCallbackConfiguration(Threshold(option), VALUE.to_si(minimum), VALUE.to_si(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callbacks

        * :attr:`CallbackID.DISTANCE_REACHED`,
        * :attr:`CallbackID.VELOCITY_REACHED`,

        are triggered, if the thresholds

        * :func:`set_distance_callback_threshold`,
        * :func:`set_velocity_callback_threshold`,

        keep being reached.

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
        check_range("distance_average_length", distance_average_length, 0, 30)
        velocity_average_length = int(velocity_average_length)
        check_range("velocity_average_length", velocity_average_length, 0, 30)
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

    async def set_mode(self, mode: Mode | int = Mode.DISTANCE, response_expected: bool = True) -> None:
        """
        .. note::
         This function is only available if you have a LIDAR-Lite sensor with hardware
         version 1. Use :func:`set_configuration` for hardware version 3. You can check
         the sensor hardware version using :func:`get_sensor_hardware_version`.

        The LIDAR-Lite sensor (hardware version 1) has five different modes. One mode is
        for distance measurements and four modes are for velocity measurements with
        different ranges.

        The following modes are available:

        * 0: Distance is measured with resolution 0.01 m and range 0-40 m
        * 1: Velocity is measured with resolution 0.1 m/s and range is 0-12.7 m/s
        * 2: Velocity is measured with resolution 0.25 m/s and range is 0-31.75 m/s
        * 3: Velocity is measured with resolution 0.5 m/s and range is 0-63.5 m/s
        * 4: Velocity is measured with resolution 1.0 m/s and range is 0-127 m/s
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MODE,
            data=pack_payload((Mode(mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_mode(self) -> Mode:
        """
        Returns the mode as set by :func:`set_mode`.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_MODE, response_expected=True)
        return Mode(unpack_payload(payload, "B"))

    async def enable_laser(self, response_expected: bool = True) -> None:
        """
        Activates the laser of the LIDAR.

        We recommend that you wait 250ms after enabling the laser before
        the first call of :func:`get_distance` to ensure stable measurements.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_LASER, response_expected=response_expected
        )

    async def disable_laser(self, response_expected: bool = True) -> None:
        """
        Deactivates the laser of the LIDAR.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_LASER, response_expected=response_expected
        )

    async def is_laser_enabled(self) -> bool:
        """
        Returns *true* if the laser is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_LASER_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def get_sensor_hardware_version(self) -> Version:
        """
        Returns the LIDAR-Lite hardware version.

        .. versionadded:: 2.0.3 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_HARDWARE_VERSION, response_expected=True
        )
        return Version(unpack_payload(payload, "B"))

    async def set_configuration(
        self,
        acquisition_count: int = 128,
        enable_quick_termination: bool = False,
        threshold_value: int = 0,
        measurement_frequency: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        .. note::
         This function is only available if you have a LIDAR-Lite sensor with hardware
         version 3. Use :func:`set_mode` for hardware version 1. You can check
         the sensor hardware version using :func:`get_sensor_hardware_version`.

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

        Units: measurement_frequency in Hz.

        .. versionadded:: 2.0.3 (Firmware)
        """
        acquisition_count = int(acquisition_count)
        check_range("acquisition_count", acquisition_count, 1, 255)
        threshold_value = int(threshold_value)
        check_range("threshold_value", threshold_value, 0, 255)
        measurement_frequency_raw = MEASUREMENT_FREQUENCY.from_si(measurement_frequency)
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

        .. versionadded:: 2.0.3 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        acquisition_count, enable_quick_termination, threshold_value, measurement_frequency = unpack_payload(
            payload, "B ! B H"
        )
        return GetConfiguration(
            acquisition_count,
            enable_quick_termination,
            threshold_value,
            MEASUREMENT_FREQUENCY.to_si(measurement_frequency),
        )

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.DISTANCE:
            return 0, DISTANCE.to_si(value)
        if callback_id is CallbackID.VELOCITY:
            return 1, VELOCITY.to_si(value)
        if callback_id is CallbackID.DISTANCE_REACHED:
            return 0, DISTANCE.to_si(value)
        return 1, VELOCITY.to_si(value)
