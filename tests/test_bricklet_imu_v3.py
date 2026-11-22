"""Tests for the IMU Bricklet 3.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_imu_v3 import (
    BrickletIMUV3,
    GetAcceleration,
    GetAllData,
    GetAngularVelocity,
    GetGravityVector,
    GetLinearAcceleration,
    GetMagneticField,
    GetOrientation,
    GetQuaternion,
    GetSensorConfiguration,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletIMUV3
FunctionID = BrickletIMUV3.FunctionID
CallbackID = BrickletIMUV3.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_ACCELERATION": 1,
    "GET_MAGNETIC_FIELD": 2,
    "GET_ANGULAR_VELOCITY": 3,
    "GET_TEMPERATURE": 4,
    "GET_ORIENTATION": 5,
    "GET_LINEAR_ACCELERATION": 6,
    "GET_GRAVITY_VECTOR": 7,
    "GET_QUATERNION": 8,
    "GET_ALL_DATA": 9,
    "SAVE_CALIBRATION": 10,
    "SET_SENSOR_CONFIGURATION": 11,
    "GET_SENSOR_CONFIGURATION": 12,
    "SET_SENSOR_FUSION_MODE": 13,
    "GET_SENSOR_FUSION_MODE": 14,
    "SET_ACCELERATION_CALLBACK_CONFIGURATION": 15,
    "GET_ACCELERATION_CALLBACK_CONFIGURATION": 16,
    "SET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION": 17,
    "GET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION": 18,
    "SET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION": 19,
    "GET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION": 20,
    "SET_TEMPERATURE_CALLBACK_CONFIGURATION": 21,
    "GET_TEMPERATURE_CALLBACK_CONFIGURATION": 22,
    "SET_ORIENTATION_CALLBACK_CONFIGURATION": 23,
    "GET_ORIENTATION_CALLBACK_CONFIGURATION": 24,
    "SET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION": 25,
    "GET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION": 26,
    "SET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION": 27,
    "GET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION": 28,
    "SET_QUATERNION_CALLBACK_CONFIGURATION": 29,
    "GET_QUATERNION_CALLBACK_CONFIGURATION": 30,
    "SET_ALL_DATA_CALLBACK_CONFIGURATION": 31,
    "GET_ALL_DATA_CALLBACK_CONFIGURATION": 32,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "ACCELERATION": 33,
    "MAGNETIC_FIELD": 34,
    "ANGULAR_VELOCITY": 35,
    "TEMPERATURE": 36,
    "LINEAR_ACCELERATION": 37,
    "GRAVITY_VECTOR": 38,
    "ORIENTATION": 39,
    "QUATERNION": 40,
    "ALL_DATA": 41,
}

CALLS: list[Call] = [
    Call(
        "get_acceleration",
        FunctionID.GET_ACCELERATION,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetAcceleration(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")),
    ),
    Call(
        "get_magnetic_field",
        FunctionID.GET_MAGNETIC_FIELD,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetMagneticField(Decimal("1.875E-7"), Decimal("2.5E-7"), Decimal("3.125E-7")),
    ),
    Call(
        "get_angular_velocity",
        FunctionID.GET_ANGULAR_VELOCITY,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetAngularVelocity(Decimal("0.1875"), Decimal("0.25"), Decimal("0.3125")),
    ),
    Call("get_temperature", FunctionID.GET_TEMPERATURE, (), reply=("b", (3,)), result=Decimal("276.15")),
    Call(
        "get_orientation",
        FunctionID.GET_ORIENTATION,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetOrientation(Decimal("0.1875"), Decimal("0.25"), Decimal("0.3125")),
    ),
    Call(
        "get_linear_acceleration",
        FunctionID.GET_LINEAR_ACCELERATION,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetLinearAcceleration(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")),
    ),
    Call(
        "get_gravity_vector",
        FunctionID.GET_GRAVITY_VECTOR,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetGravityVector(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")),
    ),
    Call(
        "get_quaternion",
        FunctionID.GET_QUATERNION,
        (),
        reply=("h h h h", (3, 4, 5, 6)),
        result=GetQuaternion(
            Decimal("0.0001831166453030580479765610694"),
            Decimal("0.0002441555270707440639687480925"),
            Decimal("0.0003051944088384300799609351157"),
            Decimal("0.0003662332906061160959531221388"),
        ),
    ),
    Call(
        "get_all_data",
        FunctionID.GET_ALL_DATA,
        (),
        reply=("3h 3h 3h 3h 4h 3h 3h b B", ([3] * 3, [4] * 3, [5] * 3, [6] * 3, [7] * 4, [8] * 3, [9] * 3, 10, 11)),
        result=GetAllData((3,) * 3, (4,) * 3, (5,) * 3, (6,) * 3, (7,) * 4, (8,) * 3, (9,) * 3, Decimal("283.15"), 11),
    ),
    Call("save_calibration", FunctionID.SAVE_CALIBRATION, (), reply=("!", (True,)), result=True),
    Call(
        "set_sensor_configuration",
        FunctionID.SET_SENSOR_CONFIGURATION,
        (
            DEVICE.MagnetometerRate.MAGNETOMETER_RATE_30HZ,
            DEVICE.GyroscopeRange.GYROSCOPE_RANGE_125DPS,
            DEVICE.GyroscopeBandwidth.GYROSCOPE_BANDWIDTH_32HZ,
            DEVICE.AccelerometerRange.ACCELEROMETER_RANGE_16G,
            DEVICE.AccelerometerBandwidth.ACCELEROMETER_BANDWIDTH_1000HZ,
        ),
        sent=("B B B B B", (7, 4, 7, 3, 7)),
    ),
    Call(
        "set_sensor_configuration",
        FunctionID.SET_SENSOR_CONFIGURATION,
        (
            DEVICE.MagnetometerRate.MAGNETOMETER_RATE_30HZ,
            DEVICE.GyroscopeRange.GYROSCOPE_RANGE_125DPS,
            DEVICE.GyroscopeBandwidth.GYROSCOPE_BANDWIDTH_32HZ,
            DEVICE.AccelerometerRange.ACCELEROMETER_RANGE_16G,
            DEVICE.AccelerometerBandwidth.ACCELEROMETER_BANDWIDTH_1000HZ,
            False,
        ),
        sent=("B B B B B", (7, 4, 7, 3, 7)),
        response_expected=False,
    ),
    Call(
        "get_sensor_configuration",
        FunctionID.GET_SENSOR_CONFIGURATION,
        (),
        reply=("B B B B B", (7, 4, 7, 3, 7)),
        result=GetSensorConfiguration(
            DEVICE.MagnetometerRate.MAGNETOMETER_RATE_30HZ,
            DEVICE.GyroscopeRange.GYROSCOPE_RANGE_125DPS,
            DEVICE.GyroscopeBandwidth.GYROSCOPE_BANDWIDTH_32HZ,
            DEVICE.AccelerometerRange.ACCELEROMETER_RANGE_16G,
            DEVICE.AccelerometerBandwidth.ACCELEROMETER_BANDWIDTH_1000HZ,
        ),
    ),
    Call(
        "set_sensor_fusion_mode",
        FunctionID.SET_SENSOR_FUSION_MODE,
        (DEVICE.SensorFusion.ON_WITHOUT_FAST_MAGNETOMETER_CALIBRATION,),
        sent=("B", (3,)),
    ),
    Call(
        "set_sensor_fusion_mode",
        FunctionID.SET_SENSOR_FUSION_MODE,
        (DEVICE.SensorFusion.ON_WITHOUT_FAST_MAGNETOMETER_CALIBRATION, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_sensor_fusion_mode",
        FunctionID.GET_SENSOR_FUSION_MODE,
        (),
        reply=("B", (3,)),
        result=DEVICE.SensorFusion.ON_WITHOUT_FAST_MAGNETOMETER_CALIBRATION,
    ),
    Call(
        "set_acceleration_callback_configuration",
        FunctionID.SET_ACCELERATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_acceleration_callback_configuration",
        FunctionID.SET_ACCELERATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_acceleration_callback_configuration",
        FunctionID.GET_ACCELERATION_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_magnetic_field_callback_configuration",
        FunctionID.SET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_magnetic_field_callback_configuration",
        FunctionID.SET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_magnetic_field_callback_configuration",
        FunctionID.GET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_angular_velocity_callback_configuration",
        FunctionID.SET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_angular_velocity_callback_configuration",
        FunctionID.SET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_angular_velocity_callback_configuration",
        FunctionID.GET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_temperature_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_orientation_callback_configuration",
        FunctionID.SET_ORIENTATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_orientation_callback_configuration",
        FunctionID.SET_ORIENTATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_orientation_callback_configuration",
        FunctionID.GET_ORIENTATION_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_linear_acceleration_callback_configuration",
        FunctionID.SET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_linear_acceleration_callback_configuration",
        FunctionID.SET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_linear_acceleration_callback_configuration",
        FunctionID.GET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_gravity_vector_callback_configuration",
        FunctionID.SET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_gravity_vector_callback_configuration",
        FunctionID.SET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_gravity_vector_callback_configuration",
        FunctionID.GET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_quaternion_callback_configuration",
        FunctionID.SET_QUATERNION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_quaternion_callback_configuration",
        FunctionID.SET_QUATERNION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_quaternion_callback_configuration",
        FunctionID.GET_QUATERNION_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_all_data_callback_configuration",
        FunctionID.SET_ALL_DATA_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_all_data_callback_configuration",
        FunctionID.SET_ALL_DATA_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_all_data_callback_configuration",
        FunctionID.GET_ALL_DATA_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ACCELERATION_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ACCELERATION_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_MAGNETIC_FIELD_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION,
        (2, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ANGULAR_VELOCITY_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call("get_value", FunctionID.GET_TEMPERATURE, (3,), reply=("b", (3,)), result=Decimal("276.15")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (3, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (3,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION,
        (4, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_LINEAR_ACCELERATION_CALLBACK_CONFIGURATION,
        (4,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION,
        (5, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_GRAVITY_VECTOR_CALLBACK_CONFIGURATION,
        (5,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ORIENTATION_CALLBACK_CONFIGURATION,
        (6, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ORIENTATION_CALLBACK_CONFIGURATION,
        (6,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_QUATERNION_CALLBACK_CONFIGURATION,
        (7, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_QUATERNION_CALLBACK_CONFIGURATION,
        (7,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALL_DATA_CALLBACK_CONFIGURATION,
        (8, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALL_DATA_CALLBACK_CONFIGURATION,
        (8,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    (
        "set_sensor_configuration",
        (
            12345,
            DEVICE.GyroscopeRange.GYROSCOPE_RANGE_125DPS,
            DEVICE.GyroscopeBandwidth.GYROSCOPE_BANDWIDTH_32HZ,
            DEVICE.AccelerometerRange.ACCELEROMETER_RANGE_16G,
            DEVICE.AccelerometerBandwidth.ACCELEROMETER_BANDWIDTH_1000HZ,
        ),
    ),
    (
        "set_sensor_configuration",
        (
            DEVICE.MagnetometerRate.MAGNETOMETER_RATE_30HZ,
            12345,
            DEVICE.GyroscopeBandwidth.GYROSCOPE_BANDWIDTH_32HZ,
            DEVICE.AccelerometerRange.ACCELEROMETER_RANGE_16G,
            DEVICE.AccelerometerBandwidth.ACCELEROMETER_BANDWIDTH_1000HZ,
        ),
    ),
    (
        "set_sensor_configuration",
        (
            DEVICE.MagnetometerRate.MAGNETOMETER_RATE_30HZ,
            DEVICE.GyroscopeRange.GYROSCOPE_RANGE_125DPS,
            12345,
            DEVICE.AccelerometerRange.ACCELEROMETER_RANGE_16G,
            DEVICE.AccelerometerBandwidth.ACCELEROMETER_BANDWIDTH_1000HZ,
        ),
    ),
    (
        "set_sensor_configuration",
        (
            DEVICE.MagnetometerRate.MAGNETOMETER_RATE_30HZ,
            DEVICE.GyroscopeRange.GYROSCOPE_RANGE_125DPS,
            DEVICE.GyroscopeBandwidth.GYROSCOPE_BANDWIDTH_32HZ,
            12345,
            DEVICE.AccelerometerBandwidth.ACCELEROMETER_BANDWIDTH_1000HZ,
        ),
    ),
    (
        "set_sensor_configuration",
        (
            DEVICE.MagnetometerRate.MAGNETOMETER_RATE_30HZ,
            DEVICE.GyroscopeRange.GYROSCOPE_RANGE_125DPS,
            DEVICE.GyroscopeBandwidth.GYROSCOPE_BANDWIDTH_32HZ,
            DEVICE.AccelerometerRange.ACCELEROMETER_RANGE_16G,
            12345,
        ),
    ),
    ("set_sensor_fusion_mode", (12345,)),
    ("set_acceleration_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_magnetic_field_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_angular_velocity_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_temperature_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_orientation_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_linear_acceleration_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_gravity_vector_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_quaternion_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_all_data_callback_configuration", (Decimal("4294967.296"), True)),
    ("get_value", (9,)),
    ("set_callback_configuration", (9,)),
    ("get_callback_configuration", (9,)),
]


def test_identity(device: BrickletIMUV3) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2161
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("IMU Bricklet 3.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_acceleration(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback ACCELERATION is converted to an event."""
    connection.callback(CallbackID.ACCELERATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (0, CallbackID.ACCELERATION, GetAcceleration(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")))
    ]


def test_callback_magnetic_field(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback MAGNETIC_FIELD is converted to an event."""
    connection.callback(CallbackID.MAGNETIC_FIELD, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (1, CallbackID.MAGNETIC_FIELD, GetMagneticField(Decimal("1.875E-7"), Decimal("2.5E-7"), Decimal("3.125E-7")))
    ]


def test_callback_angular_velocity(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback ANGULAR_VELOCITY is converted to an event."""
    connection.callback(CallbackID.ANGULAR_VELOCITY, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (2, CallbackID.ANGULAR_VELOCITY, GetAngularVelocity(Decimal("0.1875"), Decimal("0.25"), Decimal("0.3125")))
    ]


def test_callback_temperature(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.TEMPERATURE, "b", *(3,))
    assert summary(read_events(device)) == [(3, CallbackID.TEMPERATURE, Decimal("276.15"))]


def test_callback_linear_acceleration(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback LINEAR_ACCELERATION is converted to an event."""
    connection.callback(CallbackID.LINEAR_ACCELERATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (4, CallbackID.LINEAR_ACCELERATION, GetLinearAcceleration(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")))
    ]


def test_callback_gravity_vector(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback GRAVITY_VECTOR is converted to an event."""
    connection.callback(CallbackID.GRAVITY_VECTOR, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (5, CallbackID.GRAVITY_VECTOR, GetGravityVector(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")))
    ]


def test_callback_orientation(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback ORIENTATION is converted to an event."""
    connection.callback(CallbackID.ORIENTATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (6, CallbackID.ORIENTATION, GetOrientation(Decimal("0.1875"), Decimal("0.25"), Decimal("0.3125")))
    ]


def test_callback_quaternion(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback QUATERNION is converted to an event."""
    connection.callback(CallbackID.QUATERNION, "h h h h", *(3, 4, 5, 6))
    assert summary(read_events(device)) == [
        (
            7,
            CallbackID.QUATERNION,
            GetQuaternion(
                Decimal("0.0001831166453030580479765610694"),
                Decimal("0.0002441555270707440639687480925"),
                Decimal("0.0003051944088384300799609351157"),
                Decimal("0.0003662332906061160959531221388"),
            ),
        )
    ]


def test_callback_all_data(device: BrickletIMUV3, connection: FakeConnection) -> None:
    """The callback ALL_DATA is converted to an event."""
    connection.callback(
        CallbackID.ALL_DATA,
        "3h 3h 3h 3h 4h 3h 3h b B",
        *([3] * 3, [4] * 3, [5] * 3, [6] * 3, [7] * 4, [8] * 3, [9] * 3, 10, 11),
    )
    assert summary(read_events(device)) == [
        (
            8,
            CallbackID.ALL_DATA,
            GetAllData((3,) * 3, (4,) * 3, (5,) * 3, (6,) * 3, (7,) * 4, (8,) * 3, (9,) * 3, Decimal("283.15"), 11),
        )
    ]
