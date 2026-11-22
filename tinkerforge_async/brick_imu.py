"""
Module for the Tinkerforge IMU Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/IMU_Brick_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import BrickletPort as Port
from .devices import Channel, DeviceIdentifier, DeviceWithMCU, GetSPITFPBaudrateConfig, GetSPITFPErrorCount, _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, TEMPERATURE, LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this brick
    """

    ACCELERATION = 31
    MAGNETIC_FIELD = 32
    ANGULAR_VELOCITY = 33
    ALL_DATA = 34
    ORIENTATION = 35
    QUATERNION = 36


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """

    GET_ACCELERATION = 1
    GET_MAGNETIC_FIELD = 2
    GET_ANGULAR_VELOCITY = 3
    GET_ALL_DATA = 4
    GET_ORIENTATION = 5
    GET_QUATERNION = 6
    GET_IMU_TEMPERATURE = 7
    LEDS_ON = 8
    LEDS_OFF = 9
    ARE_LEDS_ON = 10
    SET_ACCELERATION_RANGE = 11
    GET_ACCELERATION_RANGE = 12
    SET_MAGNETOMETER_RANGE = 13
    GET_MAGNETOMETER_RANGE = 14
    SET_CONVERGENCE_SPEED = 15
    GET_CONVERGENCE_SPEED = 16
    SET_CALIBRATION = 17
    GET_CALIBRATION = 18
    SET_ACCELERATION_PERIOD = 19
    GET_ACCELERATION_PERIOD = 20
    SET_MAGNETIC_FIELD_PERIOD = 21
    GET_MAGNETIC_FIELD_PERIOD = 22
    SET_ANGULAR_VELOCITY_PERIOD = 23
    GET_ANGULAR_VELOCITY_PERIOD = 24
    SET_ALL_DATA_PERIOD = 25
    GET_ALL_DATA_PERIOD = 26
    SET_ORIENTATION_PERIOD = 27
    GET_ORIENTATION_PERIOD = 28
    SET_QUATERNION_PERIOD = 29
    GET_QUATERNION_PERIOD = 30
    ORIENTATION_CALCULATION_ON = 37
    ORIENTATION_CALCULATION_OFF = 38
    IS_ORIENTATION_CALCULATION_ON = 39
    SET_SPITFP_BAUDRATE_CONFIG = 231
    GET_SPITFP_BAUDRATE_CONFIG = 232
    GET_SEND_TIMEOUT_COUNT = 233
    SET_SPITFP_BAUDRATE = 234
    GET_SPITFP_BAUDRATE = 235
    GET_SPITFP_ERROR_COUNT = 237
    ENABLE_STATUS_LED = 238
    DISABLE_STATUS_LED = 239
    IS_STATUS_LED_ENABLED = 240
    GET_PROTOCOL1_BRICKLET_NAME = 241
    GET_CHIP_TEMPERATURE = 242
    WRITE_BRICKLET_PLUGIN = 246
    READ_BRICKLET_PLUGIN = 247


@unique
class CalibrationType(Enum):
    """
    The calibration type options
    """

    ACCELEROMETER_GAIN = 0
    ACCELEROMETER_BIAS = 1
    MAGNETOMETER_GAIN = 2
    MAGNETOMETER_BIAS = 3
    GYROSCOPE_GAIN = 4
    GYROSCOPE_BIAS = 5


@unique
class CommunicationMethod(Enum):
    """
    The communication method options
    """

    NONE = 0
    USB = 1
    SPI_STACK = 2
    CHIBI = 3
    RS485 = 4
    WIFI = 5
    ETHERNET = 6
    WIFI_V2 = 7


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


class GetAllData(NamedTuple):
    acc_x: Decimal
    acc_y: Decimal
    acc_z: Decimal
    mag_x: Decimal
    mag_y: Decimal
    mag_z: Decimal
    ang_x: Decimal
    ang_y: Decimal
    ang_z: Decimal
    temperature: Decimal


class GetOrientation(NamedTuple):
    roll: Decimal
    pitch: Decimal
    yaw: Decimal


class GetQuaternion(NamedTuple):
    x: float
    y: float
    z: float
    w: float


class GetProtocol1BrickletName(NamedTuple):
    protocol_version: int
    firmware_version: tuple[int, ...]
    name: str


CENTI_DEGREE = LinearQuantity(1, 100)  # raw: 1/100 Degree, returned in °
DECI_DEGREE_CELSIUS = LinearQuantity(1, 10, CELSIUS_ZERO)  # raw: 1/10 Degree Celsius, returned in K
DEGREE_PER_SECOND = LinearQuantity(1)  # raw: 1/1 Degree Per Second, returned in °/s
DEGREE_PER_SECOND_8_115 = LinearQuantity(8, 115)  # raw: 8/115 Degree Per Second, returned in °/s
MILLI_STANDARD_GRAVITY = LinearQuantity(196133, 20000000)  # raw: 1/1000 Standard Gravity, returned in m/s²
TESLA_1_10000000 = LinearQuantity(1, 10000000)  # raw: 1/10000000 Tesla, returned in T


class BrickIMU(DeviceWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Full fledged AHRS with 9 degrees of freedom
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_IMU
    DEVICE_DISPLAY_NAME = "IMU Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    BrickletPort = Port
    CalibrationType: TypeAlias = CalibrationType
    CommunicationMethod: TypeAlias = CommunicationMethod

    CALLBACK_FORMATS = {
        CallbackID.ACCELERATION: "h h h",
        CallbackID.MAGNETIC_FIELD: "h h h",
        CallbackID.ANGULAR_VELOCITY: "h h h",
        CallbackID.ALL_DATA: "h h h h h h h h h h",
        CallbackID.ORIENTATION: "h h h",
        CallbackID.QUATERNION: "f f f f",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.ACCELERATION,)),
        Channel(1, callbacks=(CallbackID.MAGNETIC_FIELD,)),
        Channel(2, callbacks=(CallbackID.ANGULAR_VELOCITY,)),
        Channel(3, callbacks=(CallbackID.ALL_DATA,)),
        Channel(4, callbacks=(CallbackID.ORIENTATION,)),
        Channel(5, callbacks=(CallbackID.QUATERNION,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 4)

    async def get_acceleration(self) -> GetAcceleration:
        """
        Returns the calibrated acceleration from the accelerometer for the
        x, y and z axis.

        If you want to get the acceleration periodically, it is recommended
        to use the :attr:`CallbackID.ACCELERATION` callback and set the period with
        :func:`set_acceleration_period`.

        Units: x in m/s², y in m/s², z in m/s².
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetAcceleration(
            MILLI_STANDARD_GRAVITY.to_si(x), MILLI_STANDARD_GRAVITY.to_si(y), MILLI_STANDARD_GRAVITY.to_si(z)
        )

    async def get_magnetic_field(self) -> GetMagneticField:
        """
        Returns the calibrated magnetic field from the magnetometer for the
        x, y and z axis.

        If you want to get the magnetic field periodically, it is recommended
        to use the :attr:`CallbackID.MAGNETIC_FIELD` callback and set the period with
        :func:`set_magnetic_field_period`.

        Units: x in T, y in T, z in T.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETIC_FIELD, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetMagneticField(TESLA_1_10000000.to_si(x), TESLA_1_10000000.to_si(y), TESLA_1_10000000.to_si(z))

    async def get_angular_velocity(self) -> GetAngularVelocity:
        """
        Returns the calibrated angular velocity from the gyroscope for the
        x, y and z axis in °/14.375s (you have to divide by 14.375 to
        get the value in °/s).

        If you want to get the angular velocity periodically, it is recommended
        to use the :attr:`CallbackID.ANGULAR_VELOCITY` callback and set the period with
        :func:`set_angular_velocity_period`.

        Units: x in °/s (-2000 to 2000 °/s), y in °/s (-2000 to 2000 °/s), z in °/s (-2000 to 2000 °/s).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANGULAR_VELOCITY, response_expected=True
        )
        x, y, z = unpack_payload(payload, "h h h")
        return GetAngularVelocity(
            DEGREE_PER_SECOND_8_115.to_si(x), DEGREE_PER_SECOND_8_115.to_si(y), DEGREE_PER_SECOND_8_115.to_si(z)
        )

    async def get_all_data(self) -> GetAllData:
        """
        Returns the data from :func:`get_acceleration`, :func:`get_magnetic_field`
        and :func:`get_angular_velocity` as well as the temperature of the IMU Brick.

        If you want to get the data periodically, it is recommended
        to use the :attr:`CallbackID.ALL_DATA` callback and set the period with
        :func:`set_all_data_period`.

        Units: acc_x in m/s², acc_y in m/s², acc_z in m/s², mag_x in T, mag_y in T, mag_z in T, ang_x in °/s (-2000 to
        2000 °/s), ang_y in °/s (-2000 to 2000 °/s), ang_z in °/s (-2000 to 2000 °/s), temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_DATA, response_expected=True
        )
        acc_x, acc_y, acc_z, mag_x, mag_y, mag_z, ang_x, ang_y, ang_z, temperature = unpack_payload(
            payload, "h h h h h h h h h h"
        )
        return GetAllData(
            MILLI_STANDARD_GRAVITY.to_si(acc_x),
            MILLI_STANDARD_GRAVITY.to_si(acc_y),
            MILLI_STANDARD_GRAVITY.to_si(acc_z),
            TESLA_1_10000000.to_si(mag_x),
            TESLA_1_10000000.to_si(mag_y),
            TESLA_1_10000000.to_si(mag_z),
            DEGREE_PER_SECOND_8_115.to_si(ang_x),
            DEGREE_PER_SECOND_8_115.to_si(ang_y),
            DEGREE_PER_SECOND_8_115.to_si(ang_z),
            TEMPERATURE.to_si(temperature),
        )

    async def get_orientation(self) -> GetOrientation:
        """
        Returns the current orientation (roll, pitch, yaw) of the IMU Brick as Euler
        angles. Note that Euler angles always experience a
        `gimbal lock <https://en.wikipedia.org/wiki/Gimbal_lock>`__.

        We recommend that you use quaternions instead.

        The order to sequence in which the orientation values should be applied is
        roll, yaw, pitch.

        If you want to get the orientation periodically, it is recommended
        to use the :attr:`CallbackID.ORIENTATION` callback and set the period with
        :func:`set_orientation_period`.

        Units: roll in ° (-180 to 180 °), pitch in ° (-180 to 180 °), yaw in ° (-180 to 180 °).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ORIENTATION, response_expected=True
        )
        roll, pitch, yaw = unpack_payload(payload, "h h h")
        return GetOrientation(CENTI_DEGREE.to_si(roll), CENTI_DEGREE.to_si(pitch), CENTI_DEGREE.to_si(yaw))

    async def get_quaternion(self) -> GetQuaternion:
        """
        Returns the current orientation (x, y, z, w) of the IMU as
        `quaternions <https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation>`__.

        You can go from quaternions to Euler angles with the following formula::

         xAngle = atan2(2*y*w - 2*x*z, 1 - 2*y*y - 2*z*z)
         yAngle = atan2(2*x*w - 2*y*z, 1 - 2*x*x - 2*z*z)
         zAngle =  asin(2*x*y + 2*z*w)

        This process is not reversible, because of the
        `gimbal lock <https://en.wikipedia.org/wiki/Gimbal_lock>`__.

        It is also possible to calculate independent angles. You can calculate
        yaw, pitch and roll in a right-handed vehicle coordinate system according to
        DIN70000 with::

         yaw   =  atan2(2*x*y + 2*w*z, w*w + x*x - y*y - z*z)
         pitch = -asin(2*w*y - 2*x*z)
         roll  = -atan2(2*y*z + 2*w*x, -w*w + x*x + y*y - z*z))

        Converting the quaternions to an OpenGL transformation matrix is
        possible with the following formula::

         matrix = [[1 - 2*(y*y + z*z),     2*(x*y - w*z),     2*(x*z + w*y), 0],
                   [    2*(x*y + w*z), 1 - 2*(x*x + z*z),     2*(y*z - w*x), 0],
                   [    2*(x*z - w*y),     2*(y*z + w*x), 1 - 2*(x*x + y*y), 0],
                   [                0,                 0,                 0, 1]]

        If you want to get the quaternions periodically, it is recommended
        to use the :attr:`CallbackID.QUATERNION` callback and set the period with
        :func:`set_quaternion_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_QUATERNION, response_expected=True
        )
        x, y, z, w = unpack_payload(payload, "f f f f")
        return GetQuaternion(x, y, z, w)

    async def get_imu_temperature(self) -> Decimal:
        """
        Returns the temperature of the IMU Brick.

        Units: temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_IMU_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "h"))

    async def leds_on(self, response_expected: bool = True) -> None:
        """
        Turns the orientation and direction LEDs of the IMU Brick on.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.LEDS_ON, response_expected=response_expected)

    async def leds_off(self, response_expected: bool = True) -> None:
        """
        Turns the orientation and direction LEDs of the IMU Brick off.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.LEDS_OFF, response_expected=response_expected)

    async def are_leds_on(self) -> bool:
        """
        Returns *true* if the orientation and direction LEDs of the IMU Brick
        are on, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.ARE_LEDS_ON, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_acceleration_range(self, range_: int, response_expected: bool = True) -> None:
        """
        Not implemented yet.
        """
        range_ = int(range_)
        check_range("range_", range_, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ACCELERATION_RANGE,
            data=pack_payload((range_,), "B"),
            response_expected=response_expected,
        )

    async def get_acceleration_range(self) -> int:
        """
        Not implemented yet.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION_RANGE, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_magnetometer_range(self, range_: int, response_expected: bool = True) -> None:
        """
        Not implemented yet.
        """
        range_ = int(range_)
        check_range("range_", range_, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MAGNETOMETER_RANGE,
            data=pack_payload((range_,), "B"),
            response_expected=response_expected,
        )

    async def get_magnetometer_range(self) -> int:
        """
        Not implemented yet.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETOMETER_RANGE, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_convergence_speed(self, speed: float | Decimal = 30, response_expected: bool = True) -> None:
        """
        Sets the convergence speed of the IMU Brick. The convergence speed
        determines how the different sensor measurements are fused.

        If the orientation of the IMU Brick is off by 10° and the convergence speed is
        set to 20°/s, it will take 0.5s until the orientation is corrected. However,
        if the correct orientation is reached and the convergence speed is too high,
        the orientation will fluctuate with the fluctuations of the accelerometer and
        the magnetometer.

        If you set the convergence speed to 0, practically only the gyroscope is used
        to calculate the orientation. This gives very smooth movements, but errors of the
        gyroscope will not be corrected. If you set the convergence speed to something
        above 500, practically only the magnetometer and the accelerometer are used to
        calculate the orientation. In this case the movements are abrupt and the values
        will fluctuate, but there won't be any errors that accumulate over time.

        In an application with high angular velocities, we recommend a high convergence
        speed, so the errors of the gyroscope can be corrected fast. In applications with
        only slow movements we recommend a low convergence speed. You can change the
        convergence speed on the fly. So it is possible (and recommended) to increase
        the convergence speed before an abrupt movement and decrease it afterwards
        again.

        You might want to play around with the convergence speed in the Brick Viewer to
        get a feeling for a good value for your application.

        Units: speed in °/s.
        """
        speed_raw = DEGREE_PER_SECOND.from_si(speed)
        check_range("speed", speed_raw, 0, 65535, speed)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONVERGENCE_SPEED,
            data=pack_payload((speed_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_convergence_speed(self) -> Decimal:
        """
        Returns the convergence speed as set by :func:`set_convergence_speed`.

        Units: speed in °/s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONVERGENCE_SPEED, response_expected=True
        )
        return DEGREE_PER_SECOND.to_si(unpack_payload(payload, "H"))

    async def set_calibration(
        self, typ: CalibrationType | int, data: Sequence[int], response_expected: bool = True
    ) -> None:
        """
        There are several different types that can be calibrated:

        .. csv-table::
         :header: "Type", "Description", "Values"
         :widths: 10, 30, 110

         "0",    "Accelerometer Gain", "``[mul x, mul y, mul z, div x, div y, div z, 0, 0, 0, 0]``"
         "1",    "Accelerometer Bias", "``[bias x, bias y, bias z, 0, 0, 0, 0, 0, 0, 0]``"
         "2",    "Magnetometer Gain",  "``[mul x, mul y, mul z, div x, div y, div z, 0, 0, 0, 0]``"
         "3",    "Magnetometer Bias",  "``[bias x, bias y, bias z, 0, 0, 0, 0, 0, 0, 0]``"
         "4",    "Gyroscope Gain",     "``[mul x, mul y, mul z, div x, div y, div z, 0, 0, 0, 0]``"
         "5",    "Gyroscope Bias",     "``[bias xl, bias yl, bias zl, temp l, bias xh, bias yh, bias zh, temp h, 0,
         0]``"

        The calibration via gain and bias is done with the following formula::

         new_value = (bias + orig_value) * gain_mul / gain_div

        If you really want to write your own calibration software, please keep
        in mind that you first have to undo the old calibration (set bias to 0 and
        gain to 1/1) and that you have to average over several thousand values
        to obtain a usable result in the end.

        The gyroscope bias is highly dependent on the temperature, so you have to
        calibrate the bias two times with different temperatures. The values ``xl``,
        ``yl``, ``zl`` and ``temp l`` are the bias for ``x``, ``y``, ``z`` and the
        corresponding temperature for a low temperature. The values ``xh``, ``yh``,
        ``zh`` and ``temp h`` are the same for a high temperatures. The temperature
        difference should be at least 278.15 K. If you have a temperature where the
        IMU Brick is mostly used, you should use this temperature for one of the
        sampling points.

        .. note::
         We highly recommend that you use the Brick Viewer to calibrate your
         IMU Brick.
        """
        check_length("data", data, 10)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload((CalibrationType(typ).value, list(map(int, data))), "B 10h"),
            response_expected=response_expected,
        )

    async def get_calibration(self, typ: CalibrationType | int) -> tuple[int, ...]:
        """
        Returns the calibration for a given type as set by :func:`set_calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CALIBRATION,
            data=pack_payload((CalibrationType(typ).value,), "B"),
            response_expected=True,
        )
        return tuple(unpack_payload(payload, "10h"))

    async def set_acceleration_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ACCELERATION` callback is triggered
        periodically. A value of 0 turns the callback off.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ACCELERATION_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_acceleration_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_acceleration_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_magnetic_field_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.MAGNETIC_FIELD` callback is
        triggered periodically. A value of 0 turns the callback off.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MAGNETIC_FIELD_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_magnetic_field_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_magnetic_field_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETIC_FIELD_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_angular_velocity_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ANGULAR_VELOCITY` callback is
        triggered periodically. A value of 0 turns the callback off.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ANGULAR_VELOCITY_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_angular_velocity_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_angular_velocity_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANGULAR_VELOCITY_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_all_data_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ALL_DATA` callback is triggered
        periodically. A value of 0 turns the callback off.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALL_DATA_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_all_data_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_all_data_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_DATA_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_orientation_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ORIENTATION` callback is triggered
        periodically. A value of 0 turns the callback off.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ORIENTATION_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_orientation_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_orientation_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ORIENTATION_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_quaternion_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.QUATERNION` callback is triggered
        periodically. A value of 0 turns the callback off.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_QUATERNION_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_quaternion_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_quaternion_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_QUATERNION_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def orientation_calculation_on(self, response_expected: bool = True) -> None:
        """
        Turns the orientation calculation of the IMU Brick on.

        As default the calculation is on.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ORIENTATION_CALCULATION_ON, response_expected=response_expected
        )

    async def orientation_calculation_off(self, response_expected: bool = True) -> None:
        """
        Turns the orientation calculation of the IMU Brick off.

        If the calculation is off, :func:`get_orientation` will return
        the last calculated value until the calculation is turned on again.

        The trigonometric functions that are needed to calculate the orientation
        are very expensive. We recommend to turn the orientation calculation
        off if the orientation is not needed, to free calculation time for the
        sensor fusion algorithm.

        As default the calculation is on.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ORIENTATION_CALCULATION_OFF, response_expected=response_expected
        )

    async def is_orientation_calculation_on(self) -> bool:
        """
        Returns *true* if the orientation calculation of the IMU Brick
        is on, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_ORIENTATION_CALCULATION_ON, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_spitfp_baudrate_config(
        self,
        enable_dynamic_baudrate: bool = True,
        minimum_dynamic_baudrate: int = 400000,
        response_expected: bool = True,
    ) -> None:
        """
        The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is enabled, the Brick will try
        to adapt the baudrate for the communication between Bricks and Bricklets according to the amount of data that is
        transferred.

        The maximum value of the baudrate can be set per port with the function :func:`set_spitfp_baudrate`. If the
        dynamic baudrate is disabled, the baudrate as set by :func:`set_spitfp_baudrate` will be used statically.
        """
        minimum_dynamic_baudrate = int(minimum_dynamic_baudrate)
        check_range("minimum_dynamic_baudrate", minimum_dynamic_baudrate, 400000, 2000000)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
            data=pack_payload((bool(enable_dynamic_baudrate), minimum_dynamic_baudrate), "! I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate_config(self) -> GetSPITFPBaudrateConfig:
        """
        Returns the baudrate config, see :func:`set_spitfp_baudrate_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPITFP_BAUDRATE_CONFIG, response_expected=True
        )
        enable_dynamic_baudrate, minimum_dynamic_baudrate = unpack_payload(payload, "! I")
        return GetSPITFPBaudrateConfig(enable_dynamic_baudrate, minimum_dynamic_baudrate)

    async def get_send_timeout_count(self, communication_method: CommunicationMethod | int) -> int:
        """
        Returns the timeout count for the different communication methods.

        This function is mostly used for debugging during development, in normal operation the counters should nearly
        always stay at 0.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SEND_TIMEOUT_COUNT,
            data=pack_payload((CommunicationMethod(communication_method).value,), "B"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def set_spitfp_baudrate(
        self, bricklet_port: Port | str, baudrate: int = 1400000, response_expected: bool = True
    ) -> None:
        """
        Sets the baudrate for a specific Bricklet port. If you want to increase the throughput of Bricklets you can
        increase the baudrate. If you get a high error count because of high interference (see
        :func:`get_spitfp_error_count`) you can decrease the baudrate.
        """
        baudrate = int(baudrate)
        check_range("baudrate", baudrate, 400000, 2000000)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE,
            data=pack_payload((Port(bricklet_port).value, baudrate), "c I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate(self, bricklet_port: Port | str) -> int:
        """
        Returns the baudrate for a given Bricklet port, see :func:`set_spitfp_baudrate`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_BAUDRATE,
            data=pack_payload((Port(bricklet_port).value,), "c"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def get_spitfp_error_count(self, bricklet_port: Port | str) -> GetSPITFPErrorCount:
        """
        Returns the error count for the communication between Brick and Bricklet. The errors counts are for errors that
        occur on the Brick side.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_ERROR_COUNT,
            data=pack_payload((Port(bricklet_port).value,), "c"),
            response_expected=True,
        )
        error_count_ack_checksum, error_count_message_checksum, error_count_frame, error_count_overflow = (
            unpack_payload(payload, "I I I I")
        )
        return GetSPITFPErrorCount(
            error_count_ack_checksum, error_count_message_checksum, error_count_frame, error_count_overflow
        )

    async def enable_status_led(self, response_expected: bool = True) -> None:
        """
        Enables the status LED. The default state is enabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_STATUS_LED, response_expected=response_expected
        )

    async def disable_status_led(self, response_expected: bool = True) -> None:
        """
        Disables the status LED. The default state is enabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_STATUS_LED, response_expected=response_expected
        )

    async def is_status_led_enabled(self) -> bool:
        """
        Returns *true* if the status LED is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_STATUS_LED_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def get_protocol1_bricklet_name(self, port: Port | str) -> GetProtocol1BrickletName:
        """
        Returns the firmware and protocol version and the name of the Bricklet for a given port.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROTOCOL1_BRICKLET_NAME,
            data=pack_payload((Port(port).value,), "c"),
            response_expected=True,
        )
        protocol_version, firmware_version, name = unpack_payload(payload, "B 3B 40s")
        return GetProtocol1BrickletName(protocol_version, tuple(firmware_version), name)

    @override
    async def get_chip_temperature(self) -> Decimal:
        """
        Returns the temperature as measured inside the microcontroller. The value returned is not the ambient
        temperature!

        The temperature is only proportional to the real temperature and it has an accuracy of ±15%. Practically it is
        only useful as an indicator for temperature changes.

        Units: temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIP_TEMPERATURE, response_expected=True
        )
        return DECI_DEGREE_CELSIUS.to_si(unpack_payload(payload, "h"))

    async def write_bricklet_plugin(
        self, port: Port | str, offset: int, chunk: bytes | Sequence[int], response_expected: bool = True
    ) -> None:
        """
        Writes 32 bytes of firmware to the bricklet attached at the given port. The bytes are written to the position
        offset * 32.

        This function is used by Brick Viewer during flashing. It should not be necessary to call it in a normal user
        program.
        """
        offset = int(offset)
        check_range("offset", offset, 0, 255)
        check_length("chunk", chunk, 32)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_BRICKLET_PLUGIN,
            data=pack_payload((Port(port).value, offset, list(map(int, chunk))), "c B 32B"),
            response_expected=response_expected,
        )

    async def read_bricklet_plugin(self, port: Port | str, offset: int) -> tuple[int, ...]:
        """
        Reads 32 bytes of firmware from the bricklet attached at the given port. The bytes are read starting at the
        position offset * 32.

        This function is used by Brick Viewer during flashing. It should not be necessary to call it in a normal user
        program.
        """
        offset = int(offset)
        check_range("offset", offset, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_BRICKLET_PLUGIN,
            data=pack_payload((Port(port).value, offset), "c B"),
            response_expected=True,
        )
        return tuple(unpack_payload(payload, "32B"))

    @override
    def _convert_callback(  # pylint: disable=too-many-return-statements,too-many-branches,too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.ACCELERATION:
            x, y, z = value
            return 0, GetAcceleration(
                MILLI_STANDARD_GRAVITY.to_si(x), MILLI_STANDARD_GRAVITY.to_si(y), MILLI_STANDARD_GRAVITY.to_si(z)
            )
        if callback_id is CallbackID.MAGNETIC_FIELD:
            x, y, z = value
            return 1, GetMagneticField(TESLA_1_10000000.to_si(x), TESLA_1_10000000.to_si(y), TESLA_1_10000000.to_si(z))
        if callback_id is CallbackID.ANGULAR_VELOCITY:
            x, y, z = value
            return 2, GetAngularVelocity(
                DEGREE_PER_SECOND_8_115.to_si(x), DEGREE_PER_SECOND_8_115.to_si(y), DEGREE_PER_SECOND_8_115.to_si(z)
            )
        if callback_id is CallbackID.ALL_DATA:
            acc_x, acc_y, acc_z, mag_x, mag_y, mag_z, ang_x, ang_y, ang_z, temperature = value
            return 3, GetAllData(
                MILLI_STANDARD_GRAVITY.to_si(acc_x),
                MILLI_STANDARD_GRAVITY.to_si(acc_y),
                MILLI_STANDARD_GRAVITY.to_si(acc_z),
                TESLA_1_10000000.to_si(mag_x),
                TESLA_1_10000000.to_si(mag_y),
                TESLA_1_10000000.to_si(mag_z),
                DEGREE_PER_SECOND_8_115.to_si(ang_x),
                DEGREE_PER_SECOND_8_115.to_si(ang_y),
                DEGREE_PER_SECOND_8_115.to_si(ang_z),
                TEMPERATURE.to_si(temperature),
            )
        if callback_id is CallbackID.ORIENTATION:
            roll, pitch, yaw = value
            return 4, GetOrientation(CENTI_DEGREE.to_si(roll), CENTI_DEGREE.to_si(pitch), CENTI_DEGREE.to_si(yaw))
        x, y, z, w = value
        return 5, GetQuaternion(x, y, z, w)
