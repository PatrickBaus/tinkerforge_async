"""Tests for the IMU Brick 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_imu_v2 import (
    BrickIMUV2,
    GetAcceleration,
    GetAllData,
    GetAngularVelocity,
    GetGravityVector,
    GetLinearAcceleration,
    GetMagneticField,
    GetOrientation,
    GetProtocol1BrickletName,
    GetQuaternion,
    GetSensorConfiguration,
)
from tinkerforge_async.devices import GetSPITFPBaudrateConfig, GetSPITFPErrorCount
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickIMUV2
FunctionID = BrickIMUV2.FunctionID
CallbackID = BrickIMUV2.CallbackID

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
    "LEDS_ON": 10,
    "LEDS_OFF": 11,
    "ARE_LEDS_ON": 12,
    "SAVE_CALIBRATION": 13,
    "SET_ACCELERATION_PERIOD": 14,
    "GET_ACCELERATION_PERIOD": 15,
    "SET_MAGNETIC_FIELD_PERIOD": 16,
    "GET_MAGNETIC_FIELD_PERIOD": 17,
    "SET_ANGULAR_VELOCITY_PERIOD": 18,
    "GET_ANGULAR_VELOCITY_PERIOD": 19,
    "SET_TEMPERATURE_PERIOD": 20,
    "GET_TEMPERATURE_PERIOD": 21,
    "SET_ORIENTATION_PERIOD": 22,
    "GET_ORIENTATION_PERIOD": 23,
    "SET_LINEAR_ACCELERATION_PERIOD": 24,
    "GET_LINEAR_ACCELERATION_PERIOD": 25,
    "SET_GRAVITY_VECTOR_PERIOD": 26,
    "GET_GRAVITY_VECTOR_PERIOD": 27,
    "SET_QUATERNION_PERIOD": 28,
    "GET_QUATERNION_PERIOD": 29,
    "SET_ALL_DATA_PERIOD": 30,
    "GET_ALL_DATA_PERIOD": 31,
    "SET_SENSOR_CONFIGURATION": 41,
    "GET_SENSOR_CONFIGURATION": 42,
    "SET_SENSOR_FUSION_MODE": 43,
    "GET_SENSOR_FUSION_MODE": 44,
    "SET_SPITFP_BAUDRATE_CONFIG": 231,
    "GET_SPITFP_BAUDRATE_CONFIG": 232,
    "GET_SEND_TIMEOUT_COUNT": 233,
    "SET_SPITFP_BAUDRATE": 234,
    "GET_SPITFP_BAUDRATE": 235,
    "GET_SPITFP_ERROR_COUNT": 237,
    "ENABLE_STATUS_LED": 238,
    "DISABLE_STATUS_LED": 239,
    "IS_STATUS_LED_ENABLED": 240,
    "GET_PROTOCOL1_BRICKLET_NAME": 241,
    "GET_CHIP_TEMPERATURE": 242,
    "WRITE_BRICKLET_PLUGIN": 246,
    "READ_BRICKLET_PLUGIN": 247,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "ACCELERATION": 32,
    "MAGNETIC_FIELD": 33,
    "ANGULAR_VELOCITY": 34,
    "TEMPERATURE": 35,
    "LINEAR_ACCELERATION": 36,
    "GRAVITY_VECTOR": 37,
    "ORIENTATION": 38,
    "QUATERNION": 39,
    "ALL_DATA": 40,
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
    Call("leds_on", FunctionID.LEDS_ON, ()),
    Call("leds_on", FunctionID.LEDS_ON, (False,), response_expected=False),
    Call("leds_off", FunctionID.LEDS_OFF, ()),
    Call("leds_off", FunctionID.LEDS_OFF, (False,), response_expected=False),
    Call("are_leds_on", FunctionID.ARE_LEDS_ON, (), reply=("!", (True,)), result=True),
    Call("save_calibration", FunctionID.SAVE_CALIBRATION, (), reply=("!", (True,)), result=True),
    Call("set_acceleration_period", FunctionID.SET_ACCELERATION_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_acceleration_period",
        FunctionID.SET_ACCELERATION_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_acceleration_period", FunctionID.GET_ACCELERATION_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("set_magnetic_field_period", FunctionID.SET_MAGNETIC_FIELD_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_magnetic_field_period",
        FunctionID.SET_MAGNETIC_FIELD_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_magnetic_field_period",
        FunctionID.GET_MAGNETIC_FIELD_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("set_angular_velocity_period", FunctionID.SET_ANGULAR_VELOCITY_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_angular_velocity_period",
        FunctionID.SET_ANGULAR_VELOCITY_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_angular_velocity_period",
        FunctionID.GET_ANGULAR_VELOCITY_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("set_temperature_period", FunctionID.SET_TEMPERATURE_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_temperature_period",
        FunctionID.SET_TEMPERATURE_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_temperature_period", FunctionID.GET_TEMPERATURE_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("set_orientation_period", FunctionID.SET_ORIENTATION_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_orientation_period",
        FunctionID.SET_ORIENTATION_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_orientation_period", FunctionID.GET_ORIENTATION_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call(
        "set_linear_acceleration_period",
        FunctionID.SET_LINEAR_ACCELERATION_PERIOD,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_linear_acceleration_period",
        FunctionID.SET_LINEAR_ACCELERATION_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_linear_acceleration_period",
        FunctionID.GET_LINEAR_ACCELERATION_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("set_gravity_vector_period", FunctionID.SET_GRAVITY_VECTOR_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_gravity_vector_period",
        FunctionID.SET_GRAVITY_VECTOR_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_gravity_vector_period",
        FunctionID.GET_GRAVITY_VECTOR_PERIOD,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call("set_quaternion_period", FunctionID.SET_QUATERNION_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_quaternion_period",
        FunctionID.SET_QUATERNION_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_quaternion_period", FunctionID.GET_QUATERNION_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("set_all_data_period", FunctionID.SET_ALL_DATA_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_all_data_period",
        FunctionID.SET_ALL_DATA_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_all_data_period", FunctionID.GET_ALL_DATA_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
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
        "set_spitfp_baudrate_config",
        FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
        (True, 400000),
        sent=("! I", (True, 400000)),
    ),
    Call(
        "set_spitfp_baudrate_config",
        FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
        (True, 400000, False),
        sent=("! I", (True, 400000)),
        response_expected=False,
    ),
    Call(
        "get_spitfp_baudrate_config",
        FunctionID.GET_SPITFP_BAUDRATE_CONFIG,
        (),
        reply=("! I", (True, 4)),
        result=GetSPITFPBaudrateConfig(True, 4),
    ),
    Call(
        "get_send_timeout_count",
        FunctionID.GET_SEND_TIMEOUT_COUNT,
        (DEVICE.CommunicationMethod.WIFI_V2,),
        sent=("B", (7,)),
        reply=("I", (3,)),
        result=3,
    ),
    Call("set_spitfp_baudrate", FunctionID.SET_SPITFP_BAUDRATE, ("b", 400000), sent=("c I", ("b", 400000))),
    Call(
        "set_spitfp_baudrate",
        FunctionID.SET_SPITFP_BAUDRATE,
        ("b", 400000, False),
        sent=("c I", ("b", 400000)),
        response_expected=False,
    ),
    Call(
        "get_spitfp_baudrate", FunctionID.GET_SPITFP_BAUDRATE, ("b",), sent=("c", ("b",)), reply=("I", (3,)), result=3
    ),
    Call(
        "get_spitfp_error_count",
        FunctionID.GET_SPITFP_ERROR_COUNT,
        ("b",),
        sent=("c", ("b",)),
        reply=("I I I I", (3, 4, 5, 6)),
        result=GetSPITFPErrorCount(3, 4, 5, 6),
    ),
    Call("enable_status_led", FunctionID.ENABLE_STATUS_LED, ()),
    Call("enable_status_led", FunctionID.ENABLE_STATUS_LED, (False,), response_expected=False),
    Call("disable_status_led", FunctionID.DISABLE_STATUS_LED, ()),
    Call("disable_status_led", FunctionID.DISABLE_STATUS_LED, (False,), response_expected=False),
    Call("is_status_led_enabled", FunctionID.IS_STATUS_LED_ENABLED, (), reply=("!", (True,)), result=True),
    Call(
        "get_protocol1_bricklet_name",
        FunctionID.GET_PROTOCOL1_BRICKLET_NAME,
        ("b",),
        sent=("c", ("b",)),
        reply=("B 3B 40s", (3, [i % 256 for i in range(3)], b"abc")),
        result=GetProtocol1BrickletName(3, tuple(i % 256 for i in range(3)), "abc"),
    ),
    Call("get_chip_temperature", FunctionID.GET_CHIP_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("273.45")),
    Call(
        "write_bricklet_plugin",
        FunctionID.WRITE_BRICKLET_PLUGIN,
        ("b", 3, [i % 256 for i in range(32)]),
        sent=("c B 32B", ("b", 3, [i % 256 for i in range(32)])),
    ),
    Call(
        "write_bricklet_plugin",
        FunctionID.WRITE_BRICKLET_PLUGIN,
        ("b", 3, [i % 256 for i in range(32)], False),
        sent=("c B 32B", ("b", 3, [i % 256 for i in range(32)])),
        response_expected=False,
    ),
    Call(
        "read_bricklet_plugin",
        FunctionID.READ_BRICKLET_PLUGIN,
        ("b", 3),
        sent=("c B", ("b", 3)),
        reply=("32B", ([i % 256 for i in range(32)],)),
        result=tuple(i % 256 for i in range(32)),
    ),
    Call("get_value", FunctionID.GET_TEMPERATURE, (3,), reply=("b", (3,)), result=Decimal("276.15")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_acceleration_period", (Decimal("4294967.296"),)),
    ("set_magnetic_field_period", (Decimal("4294967.296"),)),
    ("set_angular_velocity_period", (Decimal("4294967.296"),)),
    ("set_temperature_period", (Decimal("4294967.296"),)),
    ("set_orientation_period", (Decimal("4294967.296"),)),
    ("set_linear_acceleration_period", (Decimal("4294967.296"),)),
    ("set_gravity_vector_period", (Decimal("4294967.296"),)),
    ("set_quaternion_period", (Decimal("4294967.296"),)),
    ("set_all_data_period", (Decimal("4294967.296"),)),
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
    ("set_spitfp_baudrate_config", (True, 2000001)),
    ("get_send_timeout_count", (12345,)),
    ("set_spitfp_baudrate", ("b", 2000001)),
    ("write_bricklet_plugin", ("b", 256, [i % 256 for i in range(32)])),
    ("write_bricklet_plugin", ("b", 3, ([i % 256 for i in range(32)])[:-1])),
    ("read_bricklet_plugin", ("b", 256)),
    ("get_value", (9,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 18
    assert device.get_api_version() == (2, 0, 3)
    assert str(device).startswith("IMU Brick 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_acceleration(device, connection):
    """The callback ACCELERATION is converted to an event."""
    connection.callback(CallbackID.ACCELERATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (0, CallbackID.ACCELERATION, GetAcceleration(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")))
    ]


def test_callback_magnetic_field(device, connection):
    """The callback MAGNETIC_FIELD is converted to an event."""
    connection.callback(CallbackID.MAGNETIC_FIELD, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (1, CallbackID.MAGNETIC_FIELD, GetMagneticField(Decimal("1.875E-7"), Decimal("2.5E-7"), Decimal("3.125E-7")))
    ]


def test_callback_angular_velocity(device, connection):
    """The callback ANGULAR_VELOCITY is converted to an event."""
    connection.callback(CallbackID.ANGULAR_VELOCITY, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (2, CallbackID.ANGULAR_VELOCITY, GetAngularVelocity(Decimal("0.1875"), Decimal("0.25"), Decimal("0.3125")))
    ]


def test_callback_temperature(device, connection):
    """The callback TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.TEMPERATURE, "b", *(3,))
    assert summary(read_events(device)) == [(3, CallbackID.TEMPERATURE, Decimal("276.15"))]


def test_callback_linear_acceleration(device, connection):
    """The callback LINEAR_ACCELERATION is converted to an event."""
    connection.callback(CallbackID.LINEAR_ACCELERATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (4, CallbackID.LINEAR_ACCELERATION, GetLinearAcceleration(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")))
    ]


def test_callback_gravity_vector(device, connection):
    """The callback GRAVITY_VECTOR is converted to an event."""
    connection.callback(CallbackID.GRAVITY_VECTOR, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (5, CallbackID.GRAVITY_VECTOR, GetGravityVector(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")))
    ]


def test_callback_orientation(device, connection):
    """The callback ORIENTATION is converted to an event."""
    connection.callback(CallbackID.ORIENTATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (6, CallbackID.ORIENTATION, GetOrientation(Decimal("0.1875"), Decimal("0.25"), Decimal("0.3125")))
    ]


def test_callback_quaternion(device, connection):
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


def test_callback_all_data(device, connection):
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
