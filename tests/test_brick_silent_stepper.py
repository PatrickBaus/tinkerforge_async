"""Tests for the Silent Stepper Brick. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_silent_stepper import (
    BrickSilentStepper,
    GetAllData,
    GetBasicConfiguration,
    GetCoolstepConfiguration,
    GetDriverStatus,
    GetMiscConfiguration,
    GetProtocol1BrickletName,
    GetSpeedRamping,
    GetSpreadcycleConfiguration,
    GetStealthConfiguration,
    GetStepConfiguration,
    NewStateEvent,
)
from tinkerforge_async.devices import GetSPITFPBaudrateConfig, GetSPITFPErrorCount
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickSilentStepper
FunctionID = BrickSilentStepper.FunctionID
CallbackID = BrickSilentStepper.CallbackID

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
    "SET_STEP_CONFIGURATION": 14,
    "GET_STEP_CONFIGURATION": 15,
    "DRIVE_FORWARD": 16,
    "DRIVE_BACKWARD": 17,
    "STOP": 18,
    "GET_STACK_INPUT_VOLTAGE": 19,
    "GET_EXTERNAL_INPUT_VOLTAGE": 20,
    "SET_MOTOR_CURRENT": 22,
    "GET_MOTOR_CURRENT": 23,
    "ENABLE": 24,
    "DISABLE": 25,
    "IS_ENABLED": 26,
    "SET_BASIC_CONFIGURATION": 27,
    "GET_BASIC_CONFIGURATION": 28,
    "SET_SPREADCYCLE_CONFIGURATION": 29,
    "GET_SPREADCYCLE_CONFIGURATION": 30,
    "SET_STEALTH_CONFIGURATION": 31,
    "GET_STEALTH_CONFIGURATION": 32,
    "SET_COOLSTEP_CONFIGURATION": 33,
    "GET_COOLSTEP_CONFIGURATION": 34,
    "SET_MISC_CONFIGURATION": 35,
    "GET_MISC_CONFIGURATION": 36,
    "GET_DRIVER_STATUS": 37,
    "SET_MINIMUM_VOLTAGE": 38,
    "GET_MINIMUM_VOLTAGE": 39,
    "SET_TIME_BASE": 42,
    "GET_TIME_BASE": 43,
    "GET_ALL_DATA": 44,
    "SET_ALL_DATA_PERIOD": 45,
    "GET_ALL_DATA_PERIOD": 46,
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
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"UNDER_VOLTAGE": 40, "POSITION_REACHED": 41, "ALL_DATA": 47, "NEW_STATE": 48}

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
    Call(
        "set_step_configuration",
        FunctionID.SET_STEP_CONFIGURATION,
        (DEVICE.StepResolution.STEP_RESOLUTION_256, True),
        sent=("B !", (0, True)),
    ),
    Call(
        "set_step_configuration",
        FunctionID.SET_STEP_CONFIGURATION,
        (DEVICE.StepResolution.STEP_RESOLUTION_256, True, False),
        sent=("B !", (0, True)),
        response_expected=False,
    ),
    Call(
        "get_step_configuration",
        FunctionID.GET_STEP_CONFIGURATION,
        (),
        reply=("B !", (0, True)),
        result=GetStepConfiguration(DEVICE.StepResolution.STEP_RESOLUTION_256, True),
    ),
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
    Call("set_motor_current", FunctionID.SET_MOTOR_CURRENT, (Decimal("0.36"),), sent=("H", (360,))),
    Call(
        "set_motor_current",
        FunctionID.SET_MOTOR_CURRENT,
        (Decimal("0.36"), False),
        sent=("H", (360,)),
        response_expected=False,
    ),
    Call("get_motor_current", FunctionID.GET_MOTOR_CURRENT, (), reply=("H", (360,)), result=Decimal("0.36")),
    Call("enable", FunctionID.ENABLE, ()),
    Call("enable", FunctionID.ENABLE, (False,), response_expected=False),
    Call("disable", FunctionID.DISABLE, ()),
    Call("disable", FunctionID.DISABLE, (False,), response_expected=False),
    Call("is_enabled", FunctionID.IS_ENABLED, (), reply=("!", (True,)), result=True),
    Call(
        "set_basic_configuration",
        FunctionID.SET_BASIC_CONFIGURATION,
        (Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), 3, 3, 3, True),
        sent=("H H H H H H H !", (3, 3, 3, 3, 3, 3, 3, True)),
    ),
    Call(
        "set_basic_configuration",
        FunctionID.SET_BASIC_CONFIGURATION,
        (Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), 3, 3, 3, True, False),
        sent=("H H H H H H H !", (3, 3, 3, 3, 3, 3, 3, True)),
        response_expected=False,
    ),
    Call(
        "get_basic_configuration",
        FunctionID.GET_BASIC_CONFIGURATION,
        (),
        reply=("H H H H H H H !", (3, 4, 5, 6, 7, 8, 9, True)),
        result=GetBasicConfiguration(
            Decimal("0.003"), Decimal("0.004"), Decimal("0.005"), Decimal("0.006"), 7, 8, 9, True
        ),
    ),
    Call(
        "set_spreadcycle_configuration",
        FunctionID.SET_SPREADCYCLE_CONFIGURATION,
        (3, True, 3, 3, 3, 3, DEVICE.ChopperMode.FAST_DECAY, 3, True),
        sent=("B ! B B b b B B !", (3, True, 3, 3, 3, 3, 1, 3, True)),
    ),
    Call(
        "set_spreadcycle_configuration",
        FunctionID.SET_SPREADCYCLE_CONFIGURATION,
        (3, True, 3, 3, 3, 3, DEVICE.ChopperMode.FAST_DECAY, 3, True, False),
        sent=("B ! B B b b B B !", (3, True, 3, 3, 3, 3, 1, 3, True)),
        response_expected=False,
    ),
    Call(
        "get_spreadcycle_configuration",
        FunctionID.GET_SPREADCYCLE_CONFIGURATION,
        (),
        reply=("B ! B B b b B B !", (3, True, 5, 6, 7, 8, 1, 3, True)),
        result=GetSpreadcycleConfiguration(3, True, 5, 6, 7, 8, DEVICE.ChopperMode.FAST_DECAY, 3, True),
    ),
    Call(
        "set_stealth_configuration",
        FunctionID.SET_STEALTH_CONFIGURATION,
        (True, 3, 3, True, True, DEVICE.FreewheelMode.COIL_SHORT_HS),
        sent=("! B B ! ! B", (True, 3, 3, True, True, 3)),
    ),
    Call(
        "set_stealth_configuration",
        FunctionID.SET_STEALTH_CONFIGURATION,
        (True, 3, 3, True, True, DEVICE.FreewheelMode.COIL_SHORT_HS, False),
        sent=("! B B ! ! B", (True, 3, 3, True, True, 3)),
        response_expected=False,
    ),
    Call(
        "get_stealth_configuration",
        FunctionID.GET_STEALTH_CONFIGURATION,
        (),
        reply=("! B B ! ! B", (True, 4, 5, True, True, 3)),
        result=GetStealthConfiguration(True, 4, 5, True, True, DEVICE.FreewheelMode.COIL_SHORT_HS),
    ),
    Call(
        "set_coolstep_configuration",
        FunctionID.SET_COOLSTEP_CONFIGURATION,
        (
            3,
            3,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            DEVICE.MinimumCurrent.QUARTER,
            3,
            DEVICE.StallguardMode.FILTERED,
        ),
        sent=("B B B B B b B", (3, 3, 3, 3, 1, 3, 1)),
    ),
    Call(
        "set_coolstep_configuration",
        FunctionID.SET_COOLSTEP_CONFIGURATION,
        (
            3,
            3,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            DEVICE.MinimumCurrent.QUARTER,
            3,
            DEVICE.StallguardMode.FILTERED,
            False,
        ),
        sent=("B B B B B b B", (3, 3, 3, 3, 1, 3, 1)),
        response_expected=False,
    ),
    Call(
        "get_coolstep_configuration",
        FunctionID.GET_COOLSTEP_CONFIGURATION,
        (),
        reply=("B B B B B b B", (3, 4, 3, 3, 1, 8, 1)),
        result=GetCoolstepConfiguration(
            3,
            4,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            DEVICE.MinimumCurrent.QUARTER,
            8,
            DEVICE.StallguardMode.FILTERED,
        ),
    ),
    Call("set_misc_configuration", FunctionID.SET_MISC_CONFIGURATION, (True, 3), sent=("! B", (True, 3))),
    Call(
        "set_misc_configuration",
        FunctionID.SET_MISC_CONFIGURATION,
        (True, 3, False),
        sent=("! B", (True, 3)),
        response_expected=False,
    ),
    Call(
        "get_misc_configuration",
        FunctionID.GET_MISC_CONFIGURATION,
        (),
        reply=("! B", (True, 4)),
        result=GetMiscConfiguration(True, 4),
    ),
    Call(
        "get_driver_status",
        FunctionID.GET_DRIVER_STATUS,
        (),
        reply=("B B B ! B ! B B", (3, 3, 2, True, 7, True, 9, 10)),
        result=GetDriverStatus(
            DEVICE.OpenLoad.PHASE_AB, DEVICE.ShortToGround.PHASE_AB, DEVICE.OverTemperature.LIMIT, True, 7, True, 9, 10
        ),
    ),
    Call("set_minimum_voltage", FunctionID.SET_MINIMUM_VOLTAGE, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_minimum_voltage",
        FunctionID.SET_MINIMUM_VOLTAGE,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_minimum_voltage", FunctionID.GET_MINIMUM_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
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
    ("set_step_configuration", (12345, True)),
    ("set_motor_current", (Decimal("1.641"),)),
    (
        "set_basic_configuration",
        (Decimal("65.536"), Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), 3, 3, 3, True),
    ),
    (
        "set_basic_configuration",
        (Decimal("0.003"), Decimal("65.536"), Decimal("0.003"), Decimal("0.003"), 3, 3, 3, True),
    ),
    (
        "set_basic_configuration",
        (Decimal("0.003"), Decimal("0.003"), Decimal("0.308"), Decimal("0.003"), 3, 3, 3, True),
    ),
    (
        "set_basic_configuration",
        (Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), Decimal("5.223"), 3, 3, 3, True),
    ),
    (
        "set_basic_configuration",
        (Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), 65536, 3, 3, True),
    ),
    (
        "set_basic_configuration",
        (Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), 3, 65536, 3, True),
    ),
    (
        "set_basic_configuration",
        (Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), Decimal("0.003"), 3, 3, 65536, True),
    ),
    ("set_spreadcycle_configuration", (16, True, 3, 3, 3, 3, DEVICE.ChopperMode.FAST_DECAY, 3, True)),
    ("set_spreadcycle_configuration", (3, True, 16, 3, 3, 3, DEVICE.ChopperMode.FAST_DECAY, 3, True)),
    ("set_spreadcycle_configuration", (3, True, 3, 8, 3, 3, DEVICE.ChopperMode.FAST_DECAY, 3, True)),
    ("set_spreadcycle_configuration", (3, True, 3, 3, 13, 3, DEVICE.ChopperMode.FAST_DECAY, 3, True)),
    ("set_spreadcycle_configuration", (3, True, 3, 3, 3, 13, DEVICE.ChopperMode.FAST_DECAY, 3, True)),
    ("set_spreadcycle_configuration", (3, True, 3, 3, 3, 3, 12345, 3, True)),
    ("set_spreadcycle_configuration", (3, True, 3, 3, 3, 3, DEVICE.ChopperMode.FAST_DECAY, 4, True)),
    ("set_stealth_configuration", (True, 256, 3, True, True, DEVICE.FreewheelMode.COIL_SHORT_HS)),
    ("set_stealth_configuration", (True, 3, 256, True, True, DEVICE.FreewheelMode.COIL_SHORT_HS)),
    ("set_stealth_configuration", (True, 3, 3, True, True, 12345)),
    (
        "set_coolstep_configuration",
        (
            16,
            3,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            DEVICE.MinimumCurrent.QUARTER,
            3,
            DEVICE.StallguardMode.FILTERED,
        ),
    ),
    (
        "set_coolstep_configuration",
        (
            3,
            16,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            DEVICE.MinimumCurrent.QUARTER,
            3,
            DEVICE.StallguardMode.FILTERED,
        ),
    ),
    (
        "set_coolstep_configuration",
        (
            3,
            3,
            12345,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            DEVICE.MinimumCurrent.QUARTER,
            3,
            DEVICE.StallguardMode.FILTERED,
        ),
    ),
    (
        "set_coolstep_configuration",
        (
            3,
            3,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            12345,
            DEVICE.MinimumCurrent.QUARTER,
            3,
            DEVICE.StallguardMode.FILTERED,
        ),
    ),
    (
        "set_coolstep_configuration",
        (
            3,
            3,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            12345,
            3,
            DEVICE.StallguardMode.FILTERED,
        ),
    ),
    (
        "set_coolstep_configuration",
        (
            3,
            3,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            DEVICE.MinimumCurrent.QUARTER,
            64,
            DEVICE.StallguardMode.FILTERED,
        ),
    ),
    (
        "set_coolstep_configuration",
        (
            3,
            3,
            DEVICE.CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_8,
            DEVICE.CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_32,
            DEVICE.MinimumCurrent.QUARTER,
            3,
            12345,
        ),
    ),
    ("set_misc_configuration", (True, 16)),
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


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 19
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Silent Stepper Brick with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_under_voltage(device, connection):
    """The callback UNDER_VOLTAGE is converted to an event."""
    connection.callback(CallbackID.UNDER_VOLTAGE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.UNDER_VOLTAGE, Decimal("0.003"))]


def test_callback_position_reached(device, connection):
    """The callback POSITION_REACHED is converted to an event."""
    connection.callback(CallbackID.POSITION_REACHED, "i", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.POSITION_REACHED, 3)]


def test_callback_all_data(device, connection):
    """The callback ALL_DATA is converted to an event."""
    connection.callback(CallbackID.ALL_DATA, "H i i H H H", *(3, 4, 5, 6, 7, 8))
    assert summary(read_events(device)) == [
        (2, CallbackID.ALL_DATA, GetAllData(3, 4, 5, Decimal("0.006"), Decimal("0.007"), Decimal("0.008")))
    ]


def test_callback_new_state(device, connection):
    """The callback NEW_STATE is converted to an event."""
    connection.callback(CallbackID.NEW_STATE, "B B", *(6, 6))
    assert summary(read_events(device)) == [
        (
            3,
            CallbackID.NEW_STATE,
            NewStateEvent(DEVICE.State.DIRECTION_CHANGE_TO_BACKWARD, DEVICE.State.DIRECTION_CHANGE_TO_BACKWARD),
        )
    ]
