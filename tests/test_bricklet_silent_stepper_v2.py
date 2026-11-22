"""Tests for the Silent Stepper Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_silent_stepper_v2 import (
    BrickletSilentStepperV2,
    GetAllData,
    GetBasicConfiguration,
    GetCoolstepConfiguration,
    GetDriverStatus,
    GetGPIOConfiguration,
    GetMiscConfiguration,
    GetSpeedRamping,
    GetSpreadcycleConfiguration,
    GetStealthConfiguration,
    GetStepConfiguration,
    NewStateEvent,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletSilentStepperV2
FunctionID = BrickletSilentStepperV2.FunctionID
CallbackID = BrickletSilentStepperV2.CallbackID

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
    "GET_INPUT_VOLTAGE": 19,
    "SET_MOTOR_CURRENT": 22,
    "GET_MOTOR_CURRENT": 23,
    "SET_ENABLED": 24,
    "GET_ENABLED": 25,
    "SET_BASIC_CONFIGURATION": 26,
    "GET_BASIC_CONFIGURATION": 27,
    "SET_SPREADCYCLE_CONFIGURATION": 28,
    "GET_SPREADCYCLE_CONFIGURATION": 29,
    "SET_STEALTH_CONFIGURATION": 30,
    "GET_STEALTH_CONFIGURATION": 31,
    "SET_COOLSTEP_CONFIGURATION": 32,
    "GET_COOLSTEP_CONFIGURATION": 33,
    "SET_MISC_CONFIGURATION": 34,
    "GET_MISC_CONFIGURATION": 35,
    "SET_ERROR_LED_CONFIG": 36,
    "GET_ERROR_LED_CONFIG": 37,
    "GET_DRIVER_STATUS": 38,
    "SET_MINIMUM_VOLTAGE": 39,
    "GET_MINIMUM_VOLTAGE": 40,
    "SET_TIME_BASE": 43,
    "GET_TIME_BASE": 44,
    "GET_ALL_DATA": 45,
    "SET_ALL_CALLBACK_CONFIGURATION": 46,
    "GET_ALL_DATA_CALLBACK_CONFIGURATON": 47,
    "SET_GPIO_CONFIGURATION": 48,
    "GET_GPIO_CONFIGURATION": 49,
    "SET_GPIO_ACTION": 50,
    "GET_GPIO_ACTION": 51,
    "GET_GPIO_STATE": 52,
    "SET_MOTOR_STALLED_CALLBACK_CONFIGURATION": 56,
    "GET_MOTOR_STALLED_CALLBACK_CONFIGURATON": 57,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "UNDER_VOLTAGE": 41,
    "POSITION_REACHED": 42,
    "ALL_DATA": 53,
    "NEW_STATE": 54,
    "GPIO_STATE": 55,
    "MOTOR_STALLED": 58,
}

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
    Call("get_input_voltage", FunctionID.GET_INPUT_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_motor_current", FunctionID.SET_MOTOR_CURRENT, (Decimal("0.36"),), sent=("H", (360,))),
    Call(
        "set_motor_current",
        FunctionID.SET_MOTOR_CURRENT,
        (Decimal("0.36"), False),
        sent=("H", (360,)),
        response_expected=False,
    ),
    Call("get_motor_current", FunctionID.GET_MOTOR_CURRENT, (), reply=("H", (360,)), result=Decimal("0.36")),
    Call("set_enabled", FunctionID.SET_ENABLED, (True,), sent=("!", (True,))),
    Call("set_enabled", FunctionID.SET_ENABLED, (True, False), sent=("!", (True,)), response_expected=False),
    Call("get_enabled", FunctionID.GET_ENABLED, (), reply=("!", (True,)), result=True),
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
        "set_error_led_config", FunctionID.SET_ERROR_LED_CONFIG, (DEVICE.ErrorLEDConfig.SHOW_ERROR,), sent=("B", (3,))
    ),
    Call(
        "set_error_led_config",
        FunctionID.SET_ERROR_LED_CONFIG,
        (DEVICE.ErrorLEDConfig.SHOW_ERROR, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_error_led_config",
        FunctionID.GET_ERROR_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.ErrorLEDConfig.SHOW_ERROR,
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
        reply=("H i i H H", (3, 4, 5, 6, 7)),
        result=GetAllData(3, 4, 5, Decimal("0.006"), Decimal("0.007")),
    ),
    Call(
        "set_all_callback_configuration",
        FunctionID.SET_ALL_CALLBACK_CONFIGURATION,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_all_callback_configuration",
        FunctionID.SET_ALL_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_all_data_callback_configuraton",
        FunctionID.GET_ALL_DATA_CALLBACK_CONFIGURATON,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_gpio_configuration", FunctionID.SET_GPIO_CONFIGURATION, (1, Decimal("0.003"), 3), sent=("B H H", (1, 3, 3))
    ),
    Call(
        "set_gpio_configuration",
        FunctionID.SET_GPIO_CONFIGURATION,
        (1, Decimal("0.003"), 3, False),
        sent=("B H H", (1, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_gpio_configuration",
        FunctionID.GET_GPIO_CONFIGURATION,
        (1,),
        sent=("B", (1,)),
        reply=("H H", (3, 4)),
        result=GetGPIOConfiguration(Decimal("0.003"), 4),
    ),
    Call(
        "set_gpio_action",
        FunctionID.SET_GPIO_ACTION,
        (1, DEVICE.GPIOAction.CALLBACK_FALLING_EDGE),
        sent=("B I", (1, 32)),
    ),
    Call(
        "set_gpio_action",
        FunctionID.SET_GPIO_ACTION,
        (1, DEVICE.GPIOAction.CALLBACK_FALLING_EDGE, False),
        sent=("B I", (1, 32)),
        response_expected=False,
    ),
    Call(
        "get_gpio_action",
        FunctionID.GET_GPIO_ACTION,
        (1,),
        sent=("B", (1,)),
        reply=("I", (32,)),
        result=DEVICE.GPIOAction.CALLBACK_FALLING_EDGE,
    ),
    Call(
        "get_gpio_state",
        FunctionID.GET_GPIO_STATE,
        (),
        reply=("2!", ([i % 2 == 0 for i in range(2)],)),
        result=tuple(i % 2 == 0 for i in range(2)),
    ),
    Call(
        "set_motor_stalled_callback_configuration",
        FunctionID.SET_MOTOR_STALLED_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_motor_stalled_callback_configuration",
        FunctionID.SET_MOTOR_STALLED_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_motor_stalled_callback_configuraton",
        FunctionID.GET_MOTOR_STALLED_CALLBACK_CONFIGURATON,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "get_value",
        FunctionID.GET_GPIO_STATE,
        (4,),
        reply=("2!", ([i % 2 == 0 for i in range(2)],)),
        result=tuple(i % 2 == 0 for i in range(2)),
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
    ("set_error_led_config", (12345,)),
    ("set_minimum_voltage", (Decimal("65.536"),)),
    ("set_time_base", (Decimal("4294967296"),)),
    ("set_all_callback_configuration", (Decimal("4294967.296"),)),
    ("set_gpio_configuration", (2, Decimal("0.003"), 3)),
    ("set_gpio_configuration", (1, Decimal("65.536"), 3)),
    ("set_gpio_configuration", (1, Decimal("0.003"), 65536)),
    ("get_gpio_configuration", (2,)),
    ("set_gpio_action", (2, DEVICE.GPIOAction.CALLBACK_FALLING_EDGE)),
    ("set_gpio_action", (1, 12345)),
    ("get_gpio_action", (2,)),
    ("get_value", (6,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2166
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Silent Stepper Bricklet 2.0 with uid 12345")


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
    connection.callback(CallbackID.ALL_DATA, "H i i H H", *(3, 4, 5, 6, 7))
    assert summary(read_events(device)) == [
        (2, CallbackID.ALL_DATA, GetAllData(3, 4, 5, Decimal("0.006"), Decimal("0.007")))
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


def test_callback_gpio_state(device, connection):
    """The callback GPIO_STATE is converted to an event."""
    connection.callback(CallbackID.GPIO_STATE, "2!", *([i % 2 == 0 for i in range(2)],))
    assert summary(read_events(device)) == [(4, CallbackID.GPIO_STATE, tuple(i % 2 == 0 for i in range(2)))]


def test_callback_motor_stalled(device, connection):
    """The callback MOTOR_STALLED is converted to an event."""
    connection.callback(CallbackID.MOTOR_STALLED, "i", *(3,))
    assert summary(read_events(device)) == [(5, CallbackID.MOTOR_STALLED, 3)]
