"""Tests for the Stepper Brick. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_stepper import (
    BrickStepper,
    GetAllData,
    GetProtocol1BrickletName,
    GetSpeedRamping,
    NewStateEvent,
)
from tinkerforge_async.devices import GetSPITFPBaudrateConfig, GetSPITFPErrorCount
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickStepper
FunctionID = BrickStepper.FunctionID
CallbackID = BrickStepper.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_MAX_VELOCITY": 1,
    "GET_MAX_VELOCITY": 2,
    "GET_CURRENT_VELOCITY": 3,
    "SET_SPEED_RAMPING": 4,
    "GET_SPEED_RAMPING": 5,
    "FULL_BRAKE": 6,
    "SET_CURRENT_POSITION": 7,
    "GET_CURRENT_POSITION": 8,
    "SET_TARGET_POSITION": 9,
    "GET_TARGET_POSITION": 10,
    "SET_STEPS": 11,
    "GET_STEPS": 12,
    "GET_REMAINING_STEPS": 13,
    "SET_STEP_MODE": 14,
    "GET_STEP_MODE": 15,
    "DRIVE_FORWARD": 16,
    "DRIVE_BACKWARD": 17,
    "STOP": 18,
    "GET_STACK_INPUT_VOLTAGE": 19,
    "GET_EXTERNAL_INPUT_VOLTAGE": 20,
    "GET_CURRENT_CONSUMPTION": 21,
    "SET_MOTOR_CURRENT": 22,
    "GET_MOTOR_CURRENT": 23,
    "ENABLE": 24,
    "DISABLE": 25,
    "IS_ENABLED": 26,
    "SET_DECAY": 27,
    "GET_DECAY": 28,
    "SET_MINIMUM_VOLTAGE": 29,
    "GET_MINIMUM_VOLTAGE": 30,
    "SET_SYNC_RECT": 33,
    "IS_SYNC_RECT": 34,
    "SET_TIME_BASE": 35,
    "GET_TIME_BASE": 36,
    "GET_ALL_DATA": 37,
    "SET_ALL_DATA_PERIOD": 38,
    "GET_ALL_DATA_PERIOD": 39,
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
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"UNDER_VOLTAGE": 31, "POSITION_REACHED": 32, "ALL_DATA": 40, "NEW_STATE": 41}

CALLS: list[Call] = [
    Call("set_max_velocity", FunctionID.SET_MAX_VELOCITY, (3,), sent=("H", (3,))),
    Call("set_max_velocity", FunctionID.SET_MAX_VELOCITY, (3, False), sent=("H", (3,)), response_expected=False),
    Call("get_max_velocity", FunctionID.GET_MAX_VELOCITY, (), reply=("H", (3,)), result=3),
    Call("get_current_velocity", FunctionID.GET_CURRENT_VELOCITY, (), reply=("H", (3,)), result=3),
    Call("set_speed_ramping", FunctionID.SET_SPEED_RAMPING, (3, 3), sent=("H H", (3, 3))),
    Call(
        "set_speed_ramping", FunctionID.SET_SPEED_RAMPING, (3, 3, False), sent=("H H", (3, 3)), response_expected=False
    ),
    Call("get_speed_ramping", FunctionID.GET_SPEED_RAMPING, (), reply=("H H", (3, 4)), result=GetSpeedRamping(3, 4)),
    Call("full_brake", FunctionID.FULL_BRAKE, ()),
    Call("full_brake", FunctionID.FULL_BRAKE, (False,), response_expected=False),
    Call("set_current_position", FunctionID.SET_CURRENT_POSITION, (3,), sent=("i", (3,))),
    Call(
        "set_current_position", FunctionID.SET_CURRENT_POSITION, (3, False), sent=("i", (3,)), response_expected=False
    ),
    Call("get_current_position", FunctionID.GET_CURRENT_POSITION, (), reply=("i", (3,)), result=3),
    Call("set_target_position", FunctionID.SET_TARGET_POSITION, (3,), sent=("i", (3,))),
    Call("set_target_position", FunctionID.SET_TARGET_POSITION, (3, False), sent=("i", (3,)), response_expected=False),
    Call("get_target_position", FunctionID.GET_TARGET_POSITION, (), reply=("i", (3,)), result=3),
    Call("set_steps", FunctionID.SET_STEPS, (3,), sent=("i", (3,))),
    Call("set_steps", FunctionID.SET_STEPS, (3, False), sent=("i", (3,)), response_expected=False),
    Call("get_steps", FunctionID.GET_STEPS, (), reply=("i", (3,)), result=3),
    Call("get_remaining_steps", FunctionID.GET_REMAINING_STEPS, (), reply=("i", (3,)), result=3),
    Call("set_step_mode", FunctionID.SET_STEP_MODE, (DEVICE.StepMode.EIGHTH_STEP,), sent=("B", (8,))),
    Call(
        "set_step_mode",
        FunctionID.SET_STEP_MODE,
        (DEVICE.StepMode.EIGHTH_STEP, False),
        sent=("B", (8,)),
        response_expected=False,
    ),
    Call("get_step_mode", FunctionID.GET_STEP_MODE, (), reply=("B", (8,)), result=DEVICE.StepMode.EIGHTH_STEP),
    Call("drive_forward", FunctionID.DRIVE_FORWARD, ()),
    Call("drive_forward", FunctionID.DRIVE_FORWARD, (False,), response_expected=False),
    Call("drive_backward", FunctionID.DRIVE_BACKWARD, ()),
    Call("drive_backward", FunctionID.DRIVE_BACKWARD, (False,), response_expected=False),
    Call("stop", FunctionID.STOP, ()),
    Call("stop", FunctionID.STOP, (False,), response_expected=False),
    Call("get_stack_input_voltage", FunctionID.GET_STACK_INPUT_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "get_external_input_voltage",
        FunctionID.GET_EXTERNAL_INPUT_VOLTAGE,
        (),
        reply=("H", (3,)),
        result=Decimal("0.003"),
    ),
    Call("get_current_consumption", FunctionID.GET_CURRENT_CONSUMPTION, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_motor_current", FunctionID.SET_MOTOR_CURRENT, (Decimal("0.1"),), sent=("H", (100,))),
    Call(
        "set_motor_current",
        FunctionID.SET_MOTOR_CURRENT,
        (Decimal("0.1"), False),
        sent=("H", (100,)),
        response_expected=False,
    ),
    Call("get_motor_current", FunctionID.GET_MOTOR_CURRENT, (), reply=("H", (100,)), result=Decimal("0.1")),
    Call("enable", FunctionID.ENABLE, ()),
    Call("enable", FunctionID.ENABLE, (False,), response_expected=False),
    Call("disable", FunctionID.DISABLE, ()),
    Call("disable", FunctionID.DISABLE, (False,), response_expected=False),
    Call("is_enabled", FunctionID.IS_ENABLED, (), reply=("!", (True,)), result=True),
    Call("set_decay", FunctionID.SET_DECAY, (3,), sent=("H", (3,))),
    Call("set_decay", FunctionID.SET_DECAY, (3, False), sent=("H", (3,)), response_expected=False),
    Call("get_decay", FunctionID.GET_DECAY, (), reply=("H", (3,)), result=3),
    Call("set_minimum_voltage", FunctionID.SET_MINIMUM_VOLTAGE, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_minimum_voltage",
        FunctionID.SET_MINIMUM_VOLTAGE,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_minimum_voltage", FunctionID.GET_MINIMUM_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_sync_rect", FunctionID.SET_SYNC_RECT, (True,), sent=("!", (True,))),
    Call("set_sync_rect", FunctionID.SET_SYNC_RECT, (True, False), sent=("!", (True,)), response_expected=False),
    Call("is_sync_rect", FunctionID.IS_SYNC_RECT, (), reply=("!", (True,)), result=True),
    Call("set_time_base", FunctionID.SET_TIME_BASE, (Decimal("3"),), sent=("I", (3,))),
    Call("set_time_base", FunctionID.SET_TIME_BASE, (Decimal("3"), False), sent=("I", (3,)), response_expected=False),
    Call("get_time_base", FunctionID.GET_TIME_BASE, (), reply=("I", (3,)), result=Decimal("3")),
    Call(
        "get_all_data",
        FunctionID.GET_ALL_DATA,
        (),
        reply=("H i i H H H", (3, 4, 5, 6, 7, 8)),
        result=GetAllData(3, 4, 5, Decimal("0.006"), Decimal("0.007"), Decimal("0.008")),
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
    ("set_max_velocity", (65536,)),
    ("set_speed_ramping", (65536, 3)),
    ("set_speed_ramping", (3, 65536)),
    ("set_current_position", (2147483648,)),
    ("set_target_position", (2147483648,)),
    ("set_steps", (2147483648,)),
    ("set_step_mode", (12345,)),
    ("set_motor_current", (Decimal("2.292"),)),
    ("set_decay", (65536,)),
    ("set_minimum_voltage", (Decimal("65.536"),)),
    ("set_time_base", (Decimal("4294967296"),)),
    ("set_all_data_period", (Decimal("4294967.296"),)),
    ("set_spitfp_baudrate_config", (True, 2000001)),
    ("get_send_timeout_count", (12345,)),
    ("set_spitfp_baudrate", ("b", 2000001)),
    ("write_bricklet_plugin", ("b", 256, [i % 256 for i in range(32)])),
    ("write_bricklet_plugin", ("b", 3, ([i % 256 for i in range(32)])[:-1])),
    ("read_bricklet_plugin", ("b", 256)),
]


def test_identity(device: BrickStepper) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 15
    assert device.get_api_version() == (2, 0, 4)
    assert str(device).startswith("Stepper Brick with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_under_voltage(device: BrickStepper, connection: FakeConnection) -> None:
    """The callback UNDER_VOLTAGE is converted to an event."""
    connection.callback(CallbackID.UNDER_VOLTAGE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.UNDER_VOLTAGE, Decimal("0.003"))]


def test_callback_position_reached(device: BrickStepper, connection: FakeConnection) -> None:
    """The callback POSITION_REACHED is converted to an event."""
    connection.callback(CallbackID.POSITION_REACHED, "i", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.POSITION_REACHED, 3)]


def test_callback_all_data(device: BrickStepper, connection: FakeConnection) -> None:
    """The callback ALL_DATA is converted to an event."""
    connection.callback(CallbackID.ALL_DATA, "H i i H H H", *(3, 4, 5, 6, 7, 8))
    assert summary(read_events(device)) == [
        (2, CallbackID.ALL_DATA, GetAllData(3, 4, 5, Decimal("0.006"), Decimal("0.007"), Decimal("0.008")))
    ]


def test_callback_new_state(device: BrickStepper, connection: FakeConnection) -> None:
    """The callback NEW_STATE is converted to an event."""
    connection.callback(CallbackID.NEW_STATE, "B B", *(6, 6))
    assert summary(read_events(device)) == [
        (
            3,
            CallbackID.NEW_STATE,
            NewStateEvent(DEVICE.State.DIRECTION_CHANGE_TO_BACKWARD, DEVICE.State.DIRECTION_CHANGE_TO_BACKWARD),
        )
    ]
