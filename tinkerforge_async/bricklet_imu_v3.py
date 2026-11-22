"""
Module for the Tinkerforge IMU Bricklet 3.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/IMUV3_Bricklet_Python.html) implemented using
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
from .quantities import CELSIUS_ZERO, LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ACCELERATION = 33
    MAGNETIC_FIELD = 34
    ANGULAR_VELOCITY = 35
    TEMPERATURE = 36
    LINEAR_ACCELERATION = 37
    GRAVITY_VECTOR = 38
    ORIENTATION = 39
    QUATERNION = 40
    ALL_DATA = 41


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ACCELERATION = 1
    GET_MAGNETIC_FIELD = 2
    GET_ANGULAR_VELOCITY = 3
    GET_TEMPERATURE = 4
    GET_ORIENTATION = 5
    GET_LINEAR_ACCELERATION = 6
    GET_GRAVITY_VECTOR = 7
    GET_QUATERNION = 8
    GET_ALL_DATA = 9
    SAVE_CALIBRATION = 10
    SET_SENSOR_CONFIGURATION = 11
    GET_SENSOR_CONFIGURATION = 12
    SET_SENSOR_FUSION_MODE = 13
    GET_SENSOR_FUSION_MODE = 14
    SET_ACCELERATION_CALLBACK_CONFIGURATION = 15
    GET_ACCELERATION_CALLBACK_CONFIGURATION = 16
    SET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION = 17
    GET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION = 18
    SET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION = 19
    GET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION = 20
    SET_TEMPERATURE_CALLBACK_CONFIGURATION = 21
    GET_TEMPERATURE_CALLBACK_CONFIGURATION = 22
    SET_ORIENTATION_CALLBACK_CONFIGURATION = 23
    GET_ORIENTATION_CALLBACK_CONFIGURATION = 24
    SET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION = 25
    GET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION = 26
    SET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION = 27
    GET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION = 28
    SET_QUATERNION_CALLBACK_CONFIGURATION = 29
    GET_QUATERNION_CALLBACK_CONFIGURATION = 30
    SET_ALL_DATA_CALLBACK_CONFIGURATION = 31
    GET_ALL_DATA_CALLBACK_CONFIGURATION = 32


@unique
class MagnetometerRate(Enum):
    """
    The magnetometer rate options
    """

    MAGNETOMETER_RATE_2HZ = 0
    MAGNETOMETER_RATE_6HZ = 1
    MAGNETOMETER_RATE_8HZ = 2
    MAGNETOMETER_RATE_10HZ = 3
    MAGNETOMETER_RATE_15HZ = 4
    MAGNETOMETER_RATE_20HZ = 5
    MAGNETOMETER_RATE_25HZ = 6
    MAGNETOMETER_RATE_30HZ = 7


@unique
class GyroscopeRange(Enum):
    """
    The gyroscope range options
    """

    GYROSCOPE_RANGE_2000DPS = 0
    GYROSCOPE_RANGE_1000DPS = 1
    GYROSCOPE_RANGE_500DPS = 2
    GYROSCOPE_RANGE_250DPS = 3
    GYROSCOPE_RANGE_125DPS = 4


@unique
class GyroscopeBandwidth(Enum):
    """
    The gyroscope bandwidth options
    """

    GYROSCOPE_BANDWIDTH_523HZ = 0
    GYROSCOPE_BANDWIDTH_230HZ = 1
    GYROSCOPE_BANDWIDTH_116HZ = 2
    GYROSCOPE_BANDWIDTH_47HZ = 3
    GYROSCOPE_BANDWIDTH_23HZ = 4
    GYROSCOPE_BANDWIDTH_12HZ = 5
    GYROSCOPE_BANDWIDTH_64HZ = 6
    GYROSCOPE_BANDWIDTH_32HZ = 7


@unique
class AccelerometerRange(Enum):
    """
    The accelerometer range options
    """

    ACCELEROMETER_RANGE_2G = 0
    ACCELEROMETER_RANGE_4G = 1
    ACCELEROMETER_RANGE_8G = 2
    ACCELEROMETER_RANGE_16G = 3


@unique
class AccelerometerBandwidth(Enum):
    """
    The accelerometer bandwidth options
    """

    ACCELEROMETER_BANDWIDTH_7_81HZ = 0
    ACCELEROMETER_BANDWIDTH_15_63HZ = 1
    ACCELEROMETER_BANDWIDTH_31_25HZ = 2
    ACCELEROMETER_BANDWIDTH_62_5HZ = 3
    ACCELEROMETER_BANDWIDTH_125HZ = 4
    ACCELEROMETER_BANDWIDTH_250HZ = 5
    ACCELEROMETER_BANDWIDTH_500HZ = 6
    ACCELEROMETER_BANDWIDTH_1000HZ = 7


@unique
class SensorFusion(Enum):
    """
    The sensor fusion options
    """

    OFF = 0
    ON = 1
    ON_WITHOUT_MAGNETOMETER = 2
    ON_WITHOUT_FAST_MAGNETOMETER_CALIBRATION = 3


class GetAcceleration(NamedTuple):
    x: Decimal
    y: Decimal
    z: Decimal


class GetMagneticField(NamedTuple):
    x: Decimal
    y: Decimal
    z: Decimal


class GetAngularVelocity(NamedTuple):
    x: Decimal
    y: Decimal
    z: Decimal


class GetOrientation(NamedTuple):
    heading: Decimal
    roll: Decimal
    pitch: Decimal


class GetLinearAcceleration(NamedTuple):
    x: Decimal
    y: Decimal
    z: Decimal


class GetGravityVector(NamedTuple):
    x: Decimal
    y: Decimal
    z: Decimal


class GetQuaternion(NamedTuple):
    w: Decimal
    x: Decimal
    y: Decimal
    z: Decimal


class GetAllData(NamedTuple):
    acceleration: tuple[int, ...]
    magnetic_field: tuple[int, ...]
    angular_velocity: tuple[int, ...]
    euler_angle: tuple[int, ...]
    quaternion: tuple[int, ...]
    linear_acceleration: tuple[int, ...]
    gravity_vector: tuple[int, ...]
    temperature: Decimal
    calibration_status: int


class GetSensorConfiguration(NamedTuple):
    magnetometer_rate: MagnetometerRate
    gyroscope_range: GyroscopeRange
    gyroscope_bandwidth: GyroscopeBandwidth
    accelerometer_range: AccelerometerRange
    accelerometer_bandwidth: AccelerometerBandwidth


CENTI_METER_PER_SECOND_SQUARED = LinearQuantity(1, 100)  # raw: 1/100 Meter Per Second Squared, returned in m/s²
DEGREE_1_16 = LinearQuantity(1, 16)  # raw: 1/16 Degree, returned in °
DEGREE_CELSIUS = LinearQuantity(1, 1, CELSIUS_ZERO)  # raw: 1/1 Degree Celsius, returned in K
DEGREE_PER_SECOND_1_16 = LinearQuantity(1, 16)  # raw: 1/16 Degree Per Second, returned in °/s
RATIO_1_16383 = LinearQuantity(1, 16383)  # raw: 1/16383, dimensionless
TESLA_1_16000000 = LinearQuantity(1, 16000000)  # raw: 1/16000000 Tesla, returned in T


class BrickletIMUV3(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Full fledged AHRS with 9 degrees of freedom
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_IMU_V3
    DEVICE_DISPLAY_NAME = "IMU Bricklet 3.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    MagnetometerRate: TypeAlias = MagnetometerRate
    GyroscopeRange: TypeAlias = GyroscopeRange
    GyroscopeBandwidth: TypeAlias = GyroscopeBandwidth
    AccelerometerRange: TypeAlias = AccelerometerRange
    AccelerometerBandwidth: TypeAlias = AccelerometerBandwidth
    SensorFusion: TypeAlias = SensorFusion

    CALLBACK_FORMATS = {
        CallbackID.ACCELERATION: "h h h",
        CallbackID.MAGNETIC_FIELD: "h h h",
        CallbackID.ANGULAR_VELOCITY: "h h h",
        CallbackID.TEMPERATURE: "b",
        CallbackID.LINEAR_ACCELERATION: "h h h",
        CallbackID.GRAVITY_VECTOR: "h h h",
        CallbackID.ORIENTATION: "h h h",
        CallbackID.QUATERNION: "h h h h",
        CallbackID.ALL_DATA: "3h 3h 3h 3h 4h 3h 3h b B",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.ACCELERATION,),
            configuration=ChannelConfiguration("acceleration", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            1,
            callbacks=(CallbackID.MAGNETIC_FIELD,),
            configuration=ChannelConfiguration("magnetic_field", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            2,
            callbacks=(CallbackID.ANGULAR_VELOCITY,),
            configuration=ChannelConfiguration("angular_velocity", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            3,
            getter="get_temperature",
            callbacks=(CallbackID.TEMPERATURE,),
            configuration=ChannelConfiguration("temperature", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            4,
            callbacks=(CallbackID.LINEAR_ACCELERATION,),
            configuration=ChannelConfiguration("linear_acceleration", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            5,
            callbacks=(CallbackID.GRAVITY_VECTOR,),
            configuration=ChannelConfiguration("gravity_vector", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            6,
            callbacks=(CallbackID.ORIENTATION,),
            configuration=ChannelConfiguration("orientation", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            7,
            callbacks=(CallbackID.QUATERNION,),
            configuration=ChannelConfiguration("quaternion", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            8,
            callbacks=(CallbackID.ALL_DATA,),
            configuration=ChannelConfiguration("all_data", thresholds=False, wrap_advanced=True),
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

    async def get_acceleration(self) -> GetAcceleration:
        """
        Returns the calibrated acceleration from the accelerometer for the
        x, y and z axis. The acceleration is in the range configured with
        :func:`set_sensor_configuration`.

        If you want to get the acceleration periodically, it is recommended
        to use the :attr:`CallbackID.ACCELERATION` callback and set the period with
        :func:`set_acceleration_callback_configuration`.

        Units: x in m/s², y in m/s², z in m/s².
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetAcceleration(
            CENTI_METER_PER_SECOND_SQUARED.to_si(x),
            CENTI_METER_PER_SECOND_SQUARED.to_si(y),
            CENTI_METER_PER_SECOND_SQUARED.to_si(z),
        )

    async def get_magnetic_field(self) -> GetMagneticField:
        """
        Returns the calibrated magnetic field from the magnetometer for the
        x, y and z axis.

        If you want to get the magnetic field periodically, it is recommended
        to use the :attr:`CallbackID.MAGNETIC_FIELD` callback and set the period with
        :func:`set_magnetic_field_callback_configuration`.

        Units: x in T (-0.0013 to 0.0013 T), y in T (-0.0013 to 0.0013 T), z in T (-0.0025 to 0.0025 T).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETIC_FIELD, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetMagneticField(TESLA_1_16000000.to_si(x), TESLA_1_16000000.to_si(y), TESLA_1_16000000.to_si(z))

    async def get_angular_velocity(self) -> GetAngularVelocity:
        """
        Returns the calibrated angular velocity from the gyroscope for the
        x, y and z axis. The angular velocity is in the range configured with
        :func:`set_sensor_configuration`.

        If you want to get the angular velocity periodically, it is recommended
        to use the :attr:`CallbackID.ANGULAR_VELOCITY` acallback nd set the period with
        :func:`set_angular_velocity_callback_configuration`.

        Units: x in °/s, y in °/s, z in °/s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANGULAR_VELOCITY, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetAngularVelocity(
            DEGREE_PER_SECOND_1_16.to_si(x), DEGREE_PER_SECOND_1_16.to_si(y), DEGREE_PER_SECOND_1_16.to_si(z)
        )

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the IMU Brick.
        The temperature is measured in the core of the BNO055 IC, it is not the
        ambient temperature

        Units: temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return DEGREE_CELSIUS.to_si(unpack_payload(payload, "b"))

    async def get_orientation(self) -> GetOrientation:
        """
        Returns the current orientation (heading, roll, pitch) of the IMU Brick as
        independent Euler angles. Note that Euler angles always
        experience a `gimbal lock <https://en.wikipedia.org/wiki/Gimbal_lock>`__.
        We recommend that you use quaternions instead, if you need the absolute
        orientation.

        If you want to get the orientation periodically, it is recommended
        to use the :attr:`CallbackID.ORIENTATION` callback and set the period with
        :func:`set_orientation_callback_configuration`.

        Units: heading in ° (0 to 360 °), roll in ° (-90 to 90 °), pitch in ° (-180 to 180 °).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ORIENTATION, response_expected=True
        )
        heading, roll, pitch = unpack_payload(payload, "h h h")
        return GetOrientation(DEGREE_1_16.to_si(heading), DEGREE_1_16.to_si(roll), DEGREE_1_16.to_si(pitch))

    async def get_linear_acceleration(self) -> GetLinearAcceleration:
        """
        Returns the linear acceleration of the IMU Brick for the
        x, y and z axis. The acceleration is in the range configured with
        :func:`set_sensor_configuration`.

        The linear acceleration is the acceleration in each of the three
        axis of the IMU Brick with the influences of gravity removed.

        It is also possible to get the gravity vector with the influence of linear
        acceleration removed, see :func:`get_gravity_vector`.

        If you want to get the linear acceleration periodically, it is recommended
        to use the :attr:`CallbackID.LINEAR_ACCELERATION` callback and set the period with
        :func:`set_linear_acceleration_callback_configuration`.

        Units: x in m/s², y in m/s², z in m/s².
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_LINEAR_ACCELERATION, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetLinearAcceleration(
            CENTI_METER_PER_SECOND_SQUARED.to_si(x),
            CENTI_METER_PER_SECOND_SQUARED.to_si(y),
            CENTI_METER_PER_SECOND_SQUARED.to_si(z),
        )

    async def get_gravity_vector(self) -> GetGravityVector:
        """
        Returns the current gravity vector of the IMU Brick for the
        x, y and z axis.

        The gravity vector is the acceleration that occurs due to gravity.
        Influences of additional linear acceleration are removed.

        It is also possible to get the linear acceleration with the influence
        of gravity removed, see :func:`get_linear_acceleration`.

        If you want to get the gravity vector periodically, it is recommended
        to use the :attr:`CallbackID.GRAVITY_VECTOR` callback and set the period with
        :func:`set_gravity_vector_callback_configuration`.

        Units: x in m/s² (-9.81 to 9.81 m/s²), y in m/s² (-9.81 to 9.81 m/s²), z in m/s² (-9.81 to 9.81 m/s²).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GRAVITY_VECTOR, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetGravityVector(
            CENTI_METER_PER_SECOND_SQUARED.to_si(x),
            CENTI_METER_PER_SECOND_SQUARED.to_si(y),
            CENTI_METER_PER_SECOND_SQUARED.to_si(z),
        )

    async def get_quaternion(self) -> GetQuaternion:
        """
        Returns the current orientation (w, x, y, z) of the IMU Brick as
        `quaternions <https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation>`__.

        You have to divide the return values by 16383 (14 bit) to get
        the usual range of -1.0 to +1.0 for quaternions.

        If you want to get the quaternions periodically, it is recommended
        to use the :attr:`CallbackID.QUATERNION` callback and set the period with
        :func:`set_quaternion_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_QUATERNION, response_expected=True
        )
        w, x, y, z = unpack_payload(payload, "h h h h")
        return GetQuaternion(
            RATIO_1_16383.to_si(w), RATIO_1_16383.to_si(x), RATIO_1_16383.to_si(y), RATIO_1_16383.to_si(z)
        )

    async def get_all_data(self) -> GetAllData:
        """
        Return all of the available data of the IMU Brick.

        * acceleration (see :func:`get_acceleration`)
        * magnetic field (see :func:`get_magnetic_field`)
        * angular velocity (see :func:`get_angular_velocity`)
        * Euler angles (see :func:`get_orientation`)
        * quaternion (see :func:`get_quaternion`)
        * linear acceleration (see :func:`get_linear_acceleration`)
        * gravity vector (see :func:`get_gravity_vector`)
        * temperature (see :func:`get_temperature`)
        * calibration status (see below)

        The calibration status consists of four pairs of two bits. Each pair
        of bits represents the status of the current calibration.

        * bit 0-1: Magnetometer
        * bit 2-3: Accelerometer
        * bit 4-5: Gyroscope
        * bit 6-7: System

        A value of 0 means for "not calibrated" and a value of 3 means
        "fully calibrated". In your program you should always be able to
        ignore the calibration status, it is used by the calibration
        window of the Brick Viewer and it can be ignored after the first
        calibration. See the documentation in the calibration window for
        more information regarding the calibration of the IMU Brick.

        If you want to get the data periodically, it is recommended
        to use the :attr:`CallbackID.ALL_DATA` callback and set the period with
        :func:`set_all_data_callback_configuration`.

        Units: temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_DATA, response_expected=True
        )
        (
            acceleration,
            magnetic_field,
            angular_velocity,
            euler_angle,
            quaternion,
            linear_acceleration,
            gravity_vector,
            temperature,
            calibration_status,
        ) = unpack_payload(payload, "3h 3h 3h 3h 4h 3h 3h b B")
        return GetAllData(
            tuple(acceleration),
            tuple(magnetic_field),
            tuple(angular_velocity),
            tuple(euler_angle),
            tuple(quaternion),
            tuple(linear_acceleration),
            tuple(gravity_vector),
            DEGREE_CELSIUS.to_si(temperature),
            calibration_status,
        )

    async def save_calibration(self) -> bool:
        """
        A call of this function saves the current calibration to be used
        as a starting point for the next restart of continuous calibration
        of the IMU Brick.

        A return value of *true* means that the calibration could be used and
        *false* means that it could not be used (this happens if the calibration
        status is not "fully calibrated").

        This function is used by the calibration window of the Brick Viewer, you
        should not need to call it in your program.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.SAVE_CALIBRATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_sensor_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        magnetometer_rate: MagnetometerRate | int = MagnetometerRate.MAGNETOMETER_RATE_20HZ,
        gyroscope_range: GyroscopeRange | int = GyroscopeRange.GYROSCOPE_RANGE_2000DPS,
        gyroscope_bandwidth: GyroscopeBandwidth | int = GyroscopeBandwidth.GYROSCOPE_BANDWIDTH_32HZ,
        accelerometer_range: AccelerometerRange | int = AccelerometerRange.ACCELEROMETER_RANGE_4G,
        accelerometer_bandwidth: AccelerometerBandwidth | int = AccelerometerBandwidth.ACCELEROMETER_BANDWIDTH_62_5HZ,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the available sensor configuration for the Magnetometer, Gyroscope and
        Accelerometer. The Accelerometer Range is user selectable in all fusion modes,
        all other configurations are auto-controlled in fusion mode.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSOR_CONFIGURATION,
            data=pack_payload(
                (
                    MagnetometerRate(magnetometer_rate).value,
                    GyroscopeRange(gyroscope_range).value,
                    GyroscopeBandwidth(gyroscope_bandwidth).value,
                    AccelerometerRange(accelerometer_range).value,
                    AccelerometerBandwidth(accelerometer_bandwidth).value,
                ),
                "B B B B B",
            ),
            response_expected=response_expected,
        )

    async def get_sensor_configuration(self) -> GetSensorConfiguration:
        """
        Returns the sensor configuration as set by :func:`set_sensor_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_CONFIGURATION, response_expected=True
        )
        magnetometer_rate, gyroscope_range, gyroscope_bandwidth, accelerometer_range, accelerometer_bandwidth = (
            unpack_payload(payload, "B B B B B")
        )
        return GetSensorConfiguration(
            MagnetometerRate(magnetometer_rate),
            GyroscopeRange(gyroscope_range),
            GyroscopeBandwidth(gyroscope_bandwidth),
            AccelerometerRange(accelerometer_range),
            AccelerometerBandwidth(accelerometer_bandwidth),
        )

    async def set_sensor_fusion_mode(
        self, mode: SensorFusion | int = SensorFusion.ON, response_expected: bool = True
    ) -> None:
        """
        If the fusion mode is turned off, the functions :func:`get_acceleration`,
        :func:`get_magnetic_field` and :func:`get_angular_velocity` return uncalibrated
        and uncompensated sensor data. All other sensor data getters return no data.

        Since firmware version 2.0.6 you can also use a fusion mode without magnetometer.
        In this mode the calculated orientation is relative (with magnetometer it is
        absolute with respect to the earth). However, the calculation can't be influenced
        by spurious magnetic fields.

        Since firmware version 2.0.13 you can also use a fusion mode without fast
        magnetometer calibration. This mode is the same as the normal fusion mode,
        but the fast magnetometer calibration is turned off. So to find the orientation
        the first time will likely take longer, but small magnetic influences might
        not affect the automatic calibration as much.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSOR_FUSION_MODE,
            data=pack_payload((SensorFusion(mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_sensor_fusion_mode(self) -> SensorFusion:
        """
        Returns the sensor fusion mode as set by :func:`set_sensor_fusion_mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_FUSION_MODE, response_expected=True
        )
        return SensorFusion(unpack_payload(payload, "B"))

    async def set_acceleration_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ACCELERATION` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ACCELERATION_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_acceleration_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_acceleration_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_magnetic_field_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.MAGNETIC_FIELD` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_magnetic_field_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_magnetic_field_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_angular_velocity_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ANGULAR_VELOCITY` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_angular_velocity_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_angular_velocity_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_temperature_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.TEMPERATURE` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_temperature_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_temperature_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_orientation_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ORIENTATION` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ORIENTATION_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_orientation_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_orientation_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ORIENTATION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_linear_acceleration_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.LINEAR_ACCELERATION` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_linear_acceleration_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_linear_acceleration_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_gravity_vector_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.GRAVITY_VECTOR` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_gravity_vector_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_gravity_vector_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_quaternion_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.QUATERNION` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_QUATERNION_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_quaternion_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_quaternion_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_QUATERNION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_all_data_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ALL_DATA` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALL_DATA_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_all_data_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_all_data_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_DATA_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    def _convert_callback(  # pylint: disable=too-many-return-statements,too-many-branches,too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.ACCELERATION:
            x, y, z = value
            return 0, GetAcceleration(
                CENTI_METER_PER_SECOND_SQUARED.to_si(x),
                CENTI_METER_PER_SECOND_SQUARED.to_si(y),
                CENTI_METER_PER_SECOND_SQUARED.to_si(z),
            )
        if callback_id is CallbackID.MAGNETIC_FIELD:
            x, y, z = value
            return 1, GetMagneticField(TESLA_1_16000000.to_si(x), TESLA_1_16000000.to_si(y), TESLA_1_16000000.to_si(z))
        if callback_id is CallbackID.ANGULAR_VELOCITY:
            x, y, z = value
            return 2, GetAngularVelocity(
                DEGREE_PER_SECOND_1_16.to_si(x), DEGREE_PER_SECOND_1_16.to_si(y), DEGREE_PER_SECOND_1_16.to_si(z)
            )
        if callback_id is CallbackID.TEMPERATURE:
            return 3, DEGREE_CELSIUS.to_si(value)
        if callback_id is CallbackID.LINEAR_ACCELERATION:
            x, y, z = value
            return 4, GetLinearAcceleration(
                CENTI_METER_PER_SECOND_SQUARED.to_si(x),
                CENTI_METER_PER_SECOND_SQUARED.to_si(y),
                CENTI_METER_PER_SECOND_SQUARED.to_si(z),
            )
        if callback_id is CallbackID.GRAVITY_VECTOR:
            x, y, z = value
            return 5, GetGravityVector(
                CENTI_METER_PER_SECOND_SQUARED.to_si(x),
                CENTI_METER_PER_SECOND_SQUARED.to_si(y),
                CENTI_METER_PER_SECOND_SQUARED.to_si(z),
            )
        if callback_id is CallbackID.ORIENTATION:
            heading, roll, pitch = value
            return 6, GetOrientation(DEGREE_1_16.to_si(heading), DEGREE_1_16.to_si(roll), DEGREE_1_16.to_si(pitch))
        if callback_id is CallbackID.QUATERNION:
            w, x, y, z = value
            return 7, GetQuaternion(
                RATIO_1_16383.to_si(w), RATIO_1_16383.to_si(x), RATIO_1_16383.to_si(y), RATIO_1_16383.to_si(z)
            )
        (
            acceleration,
            magnetic_field,
            angular_velocity,
            euler_angle,
            quaternion,
            linear_acceleration,
            gravity_vector,
            temperature,
            calibration_status,
        ) = value
        return 8, GetAllData(
            tuple(acceleration),
            tuple(magnetic_field),
            tuple(angular_velocity),
            tuple(euler_angle),
            tuple(quaternion),
            tuple(linear_acceleration),
            tuple(gravity_vector),
            DEGREE_CELSIUS.to_si(temperature),
            calibration_status,
        )
