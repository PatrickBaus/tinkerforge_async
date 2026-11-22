"""Tests for the IMU Brick. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_imu import (
    BrickIMU,
    GetAcceleration,
    GetAllData,
    GetAngularVelocity,
    GetMagneticField,
    GetOrientation,
    GetProtocol1BrickletName,
    GetQuaternion,
)
from tinkerforge_async.devices import GetSPITFPBaudrateConfig, GetSPITFPErrorCount
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickIMU
FunctionID = BrickIMU.FunctionID
CallbackID = BrickIMU.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_ACCELERATION": 1,
    "GET_MAGNETIC_FIELD": 2,
    "GET_ANGULAR_VELOCITY": 3,
    "GET_ALL_DATA": 4,
    "GET_ORIENTATION": 5,
    "GET_QUATERNION": 6,
    "GET_IMU_TEMPERATURE": 7,
    "LEDS_ON": 8,
    "LEDS_OFF": 9,
    "ARE_LEDS_ON": 10,
    "SET_ACCELERATION_RANGE": 11,
    "GET_ACCELERATION_RANGE": 12,
    "SET_MAGNETOMETER_RANGE": 13,
    "GET_MAGNETOMETER_RANGE": 14,
    "SET_CONVERGENCE_SPEED": 15,
    "GET_CONVERGENCE_SPEED": 16,
    "SET_CALIBRATION": 17,
    "GET_CALIBRATION": 18,
    "SET_ACCELERATION_PERIOD": 19,
    "GET_ACCELERATION_PERIOD": 20,
    "SET_MAGNETIC_FIELD_PERIOD": 21,
    "GET_MAGNETIC_FIELD_PERIOD": 22,
    "SET_ANGULAR_VELOCITY_PERIOD": 23,
    "GET_ANGULAR_VELOCITY_PERIOD": 24,
    "SET_ALL_DATA_PERIOD": 25,
    "GET_ALL_DATA_PERIOD": 26,
    "SET_ORIENTATION_PERIOD": 27,
    "GET_ORIENTATION_PERIOD": 28,
    "SET_QUATERNION_PERIOD": 29,
    "GET_QUATERNION_PERIOD": 30,
    "ORIENTATION_CALCULATION_ON": 37,
    "ORIENTATION_CALCULATION_OFF": 38,
    "IS_ORIENTATION_CALCULATION_ON": 39,
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
    "ACCELERATION": 31,
    "MAGNETIC_FIELD": 32,
    "ANGULAR_VELOCITY": 33,
    "ALL_DATA": 34,
    "ORIENTATION": 35,
    "QUATERNION": 36,
}

CALLS: list[Call] = [
    Call(
        "get_acceleration",
        FunctionID.GET_ACCELERATION,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetAcceleration(Decimal("0.02941995"), Decimal("0.0392266"), Decimal("0.04903325")),
    ),
    Call(
        "get_magnetic_field",
        FunctionID.GET_MAGNETIC_FIELD,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetMagneticField(Decimal("3E-7"), Decimal("4E-7"), Decimal("5E-7")),
    ),
    Call(
        "get_angular_velocity",
        FunctionID.GET_ANGULAR_VELOCITY,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetAngularVelocity(
            Decimal("0.2086956521739130434782608696"),
            Decimal("0.2782608695652173913043478261"),
            Decimal("0.3478260869565217391304347826"),
        ),
    ),
    Call(
        "get_all_data",
        FunctionID.GET_ALL_DATA,
        (),
        reply=("h h h h h h h h h h", (3, 4, 5, 6, 7, 8, 9, 10, 11, 12)),
        result=GetAllData(
            Decimal("0.02941995"),
            Decimal("0.0392266"),
            Decimal("0.04903325"),
            Decimal("6E-7"),
            Decimal("7E-7"),
            Decimal("8E-7"),
            Decimal("0.6260869565217391304347826087"),
            Decimal("0.6956521739130434782608695652"),
            Decimal("0.7652173913043478260869565217"),
            Decimal("273.27"),
        ),
    ),
    Call(
        "get_orientation",
        FunctionID.GET_ORIENTATION,
        (),
        reply=("h h h", (3, 4, 5)),
        result=GetOrientation(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")),
    ),
    Call(
        "get_quaternion",
        FunctionID.GET_QUATERNION,
        (),
        reply=("f f f f", (1.5, 1.5, 1.5, 1.5)),
        result=GetQuaternion(1.5, 1.5, 1.5, 1.5),
    ),
    Call("get_imu_temperature", FunctionID.GET_IMU_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("273.18")),
    Call("leds_on", FunctionID.LEDS_ON, ()),
    Call("leds_on", FunctionID.LEDS_ON, (False,), response_expected=False),
    Call("leds_off", FunctionID.LEDS_OFF, ()),
    Call("leds_off", FunctionID.LEDS_OFF, (False,), response_expected=False),
    Call("are_leds_on", FunctionID.ARE_LEDS_ON, (), reply=("!", (True,)), result=True),
    Call("set_acceleration_range", FunctionID.SET_ACCELERATION_RANGE, (3,), sent=("B", (3,))),
    Call(
        "set_acceleration_range",
        FunctionID.SET_ACCELERATION_RANGE,
        (3, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call("get_acceleration_range", FunctionID.GET_ACCELERATION_RANGE, (), reply=("B", (3,)), result=3),
    Call("set_magnetometer_range", FunctionID.SET_MAGNETOMETER_RANGE, (3,), sent=("B", (3,))),
    Call(
        "set_magnetometer_range",
        FunctionID.SET_MAGNETOMETER_RANGE,
        (3, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call("get_magnetometer_range", FunctionID.GET_MAGNETOMETER_RANGE, (), reply=("B", (3,)), result=3),
    Call("set_convergence_speed", FunctionID.SET_CONVERGENCE_SPEED, (Decimal("3"),), sent=("H", (3,))),
    Call(
        "set_convergence_speed",
        FunctionID.SET_CONVERGENCE_SPEED,
        (Decimal("3"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_convergence_speed", FunctionID.GET_CONVERGENCE_SPEED, (), reply=("H", (3,)), result=Decimal("3")),
    Call(
        "set_calibration",
        FunctionID.SET_CALIBRATION,
        (DEVICE.CalibrationType.GYROSCOPE_BIAS, [3] * 10),
        sent=("B 10h", (5, [3] * 10)),
    ),
    Call(
        "set_calibration",
        FunctionID.SET_CALIBRATION,
        (DEVICE.CalibrationType.GYROSCOPE_BIAS, [3] * 10, False),
        sent=("B 10h", (5, [3] * 10)),
        response_expected=False,
    ),
    Call(
        "get_calibration",
        FunctionID.GET_CALIBRATION,
        (DEVICE.CalibrationType.GYROSCOPE_BIAS,),
        sent=("B", (5,)),
        reply=("10h", ([3] * 10,)),
        result=(3,) * 10,
    ),
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
    Call("set_all_data_period", FunctionID.SET_ALL_DATA_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_all_data_period",
        FunctionID.SET_ALL_DATA_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_all_data_period", FunctionID.GET_ALL_DATA_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("set_orientation_period", FunctionID.SET_ORIENTATION_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_orientation_period",
        FunctionID.SET_ORIENTATION_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_orientation_period", FunctionID.GET_ORIENTATION_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("set_quaternion_period", FunctionID.SET_QUATERNION_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_quaternion_period",
        FunctionID.SET_QUATERNION_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_quaternion_period", FunctionID.GET_QUATERNION_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("orientation_calculation_on", FunctionID.ORIENTATION_CALCULATION_ON, ()),
    Call("orientation_calculation_on", FunctionID.ORIENTATION_CALCULATION_ON, (False,), response_expected=False),
    Call("orientation_calculation_off", FunctionID.ORIENTATION_CALCULATION_OFF, ()),
    Call("orientation_calculation_off", FunctionID.ORIENTATION_CALCULATION_OFF, (False,), response_expected=False),
    Call(
        "is_orientation_calculation_on", FunctionID.IS_ORIENTATION_CALCULATION_ON, (), reply=("!", (True,)), result=True
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
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_acceleration_range", (256,)),
    ("set_magnetometer_range", (256,)),
    ("set_convergence_speed", (Decimal("65536"),)),
    ("set_calibration", (12345, [3] * 10)),
    ("set_calibration", (DEVICE.CalibrationType.GYROSCOPE_BIAS, ([3] * 10)[:-1])),
    ("get_calibration", (12345,)),
    ("set_acceleration_period", (Decimal("4294967.296"),)),
    ("set_magnetic_field_period", (Decimal("4294967.296"),)),
    ("set_angular_velocity_period", (Decimal("4294967.296"),)),
    ("set_all_data_period", (Decimal("4294967.296"),)),
    ("set_orientation_period", (Decimal("4294967.296"),)),
    ("set_quaternion_period", (Decimal("4294967.296"),)),
    ("set_spitfp_baudrate_config", (True, 2000001)),
    ("get_send_timeout_count", (12345,)),
    ("set_spitfp_baudrate", ("b", 2000001)),
    ("write_bricklet_plugin", ("b", 256, [i % 256 for i in range(32)])),
    ("write_bricklet_plugin", ("b", 3, ([i % 256 for i in range(32)])[:-1])),
    ("read_bricklet_plugin", ("b", 256)),
]


def test_identity(device: BrickIMU) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 16
    assert device.get_api_version() == (2, 0, 4)
    assert str(device).startswith("IMU Brick with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_acceleration(device: BrickIMU, connection: FakeConnection) -> None:
    """The callback ACCELERATION is converted to an event."""
    connection.callback(CallbackID.ACCELERATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.ACCELERATION,
            GetAcceleration(Decimal("0.02941995"), Decimal("0.0392266"), Decimal("0.04903325")),
        )
    ]


def test_callback_magnetic_field(device: BrickIMU, connection: FakeConnection) -> None:
    """The callback MAGNETIC_FIELD is converted to an event."""
    connection.callback(CallbackID.MAGNETIC_FIELD, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (1, CallbackID.MAGNETIC_FIELD, GetMagneticField(Decimal("3E-7"), Decimal("4E-7"), Decimal("5E-7")))
    ]


def test_callback_angular_velocity(device: BrickIMU, connection: FakeConnection) -> None:
    """The callback ANGULAR_VELOCITY is converted to an event."""
    connection.callback(CallbackID.ANGULAR_VELOCITY, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (
            2,
            CallbackID.ANGULAR_VELOCITY,
            GetAngularVelocity(
                Decimal("0.2086956521739130434782608696"),
                Decimal("0.2782608695652173913043478261"),
                Decimal("0.3478260869565217391304347826"),
            ),
        )
    ]


def test_callback_all_data(device: BrickIMU, connection: FakeConnection) -> None:
    """The callback ALL_DATA is converted to an event."""
    connection.callback(CallbackID.ALL_DATA, "h h h h h h h h h h", *(3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
    assert summary(read_events(device)) == [
        (
            3,
            CallbackID.ALL_DATA,
            GetAllData(
                Decimal("0.02941995"),
                Decimal("0.0392266"),
                Decimal("0.04903325"),
                Decimal("6E-7"),
                Decimal("7E-7"),
                Decimal("8E-7"),
                Decimal("0.6260869565217391304347826087"),
                Decimal("0.6956521739130434782608695652"),
                Decimal("0.7652173913043478260869565217"),
                Decimal("273.27"),
            ),
        )
    ]


def test_callback_orientation(device: BrickIMU, connection: FakeConnection) -> None:
    """The callback ORIENTATION is converted to an event."""
    connection.callback(CallbackID.ORIENTATION, "h h h", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (4, CallbackID.ORIENTATION, GetOrientation(Decimal("0.03"), Decimal("0.04"), Decimal("0.05")))
    ]


def test_callback_quaternion(device: BrickIMU, connection: FakeConnection) -> None:
    """The callback QUATERNION is converted to an event."""
    connection.callback(CallbackID.QUATERNION, "f f f f", *(1.5, 1.5, 1.5, 1.5))
    assert summary(read_events(device)) == [(5, CallbackID.QUATERNION, GetQuaternion(1.5, 1.5, 1.5, 1.5))]
