"""Tests for the Performance DC Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_performance_dc import (
    BrickletPerformanceDC,
    GetGPIOConfiguration,
    GetMotion,
    GetPowerStatistics,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletPerformanceDC
FunctionID = BrickletPerformanceDC.FunctionID
CallbackID = BrickletPerformanceDC.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_ENABLED": 1,
    "GET_ENABLED": 2,
    "SET_VELOCITY": 3,
    "GET_VELOCITY": 4,
    "GET_CURRENT_VELOCITY": 5,
    "SET_MOTION": 6,
    "GET_MOTION": 7,
    "FULL_BRAKE": 8,
    "SET_DRIVE_MODE": 9,
    "GET_DRIVE_MODE": 10,
    "SET_PWM_FREQUENCY": 11,
    "GET_PWM_FREQUENCY": 12,
    "GET_POWER_STATISTICS": 13,
    "SET_THERMAL_SHUTDOWN": 14,
    "GET_THERMAL_SHUTDOWN": 15,
    "SET_GPIO_CONFIGURATION": 16,
    "GET_GPIO_CONFIGURATION": 17,
    "SET_GPIO_ACTION": 18,
    "GET_GPIO_ACTION": 19,
    "GET_GPIO_STATE": 20,
    "SET_ERROR_LED_CONFIG": 21,
    "GET_ERROR_LED_CONFIG": 22,
    "SET_CW_LED_CONFIG": 23,
    "GET_CW_LED_CONFIG": 24,
    "SET_CCW_LED_CONFIG": 25,
    "GET_CCW_LED_CONFIG": 26,
    "SET_GPIO_LED_CONFIG": 27,
    "GET_GPIO_LED_CONFIG": 28,
    "SET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION": 29,
    "GET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION": 30,
    "SET_VELOCITY_REACHED_CALLBACK_CONFIGURATION": 31,
    "GET_VELOCITY_REACHED_CALLBACK_CONFIGURATION": 32,
    "SET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION": 33,
    "GET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION": 34,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "EMERGENCY_SHUTDOWN": 35,
    "VELOCITY_REACHED": 36,
    "CURRENT_VELOCITY": 37,
    "GPIO_STATE": 38,
}

CALLS: list[Call] = [
    Call("set_enabled", FunctionID.SET_ENABLED, (True,), sent=("!", (True,))),
    Call("set_enabled", FunctionID.SET_ENABLED, (True, False), sent=("!", (True,)), response_expected=False),
    Call("get_enabled", FunctionID.GET_ENABLED, (), reply=("!", (True,)), result=True),
    Call("set_velocity", FunctionID.SET_VELOCITY, (Decimal("0.009155552842799157689138462477"),), sent=("h", (3,))),
    Call(
        "set_velocity",
        FunctionID.SET_VELOCITY,
        (Decimal("0.009155552842799157689138462477"), False),
        sent=("h", (3,)),
        response_expected=False,
    ),
    Call(
        "get_velocity",
        FunctionID.GET_VELOCITY,
        (),
        reply=("h", (3,)),
        result=Decimal("0.009155552842799157689138462477"),
    ),
    Call(
        "get_current_velocity",
        FunctionID.GET_CURRENT_VELOCITY,
        (),
        reply=("h", (3,)),
        result=Decimal("0.009155552842799157689138462477"),
    ),
    Call(
        "set_motion",
        FunctionID.SET_MOTION,
        (Decimal("0.009155552842799157689138462477"), Decimal("0.009155552842799157689138462477")),
        sent=("H H", (3, 3)),
    ),
    Call(
        "set_motion",
        FunctionID.SET_MOTION,
        (Decimal("0.009155552842799157689138462477"), Decimal("0.009155552842799157689138462477"), False),
        sent=("H H", (3, 3)),
        response_expected=False,
    ),
    Call(
        "get_motion",
        FunctionID.GET_MOTION,
        (),
        reply=("H H", (3, 4)),
        result=GetMotion(Decimal("0.009155552842799157689138462477"), Decimal("0.01220740379039887691885128330")),
    ),
    Call("full_brake", FunctionID.FULL_BRAKE, ()),
    Call("full_brake", FunctionID.FULL_BRAKE, (False,), response_expected=False),
    Call("set_drive_mode", FunctionID.SET_DRIVE_MODE, (DEVICE.DriveMode.DRIVE_COAST,), sent=("B", (1,))),
    Call(
        "set_drive_mode",
        FunctionID.SET_DRIVE_MODE,
        (DEVICE.DriveMode.DRIVE_COAST, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call("get_drive_mode", FunctionID.GET_DRIVE_MODE, (), reply=("B", (1,)), result=DEVICE.DriveMode.DRIVE_COAST),
    Call("set_pwm_frequency", FunctionID.SET_PWM_FREQUENCY, (Decimal("3"),), sent=("H", (3,))),
    Call(
        "set_pwm_frequency",
        FunctionID.SET_PWM_FREQUENCY,
        (Decimal("3"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_pwm_frequency", FunctionID.GET_PWM_FREQUENCY, (), reply=("H", (3,)), result=Decimal("3")),
    Call(
        "get_power_statistics",
        FunctionID.GET_POWER_STATISTICS,
        (),
        reply=("H H h", (3, 4, 5)),
        result=GetPowerStatistics(Decimal("0.003"), Decimal("0.004"), Decimal("0.5")),
    ),
    Call("set_thermal_shutdown", FunctionID.SET_THERMAL_SHUTDOWN, (Decimal("3"),), sent=("B", (3,))),
    Call(
        "set_thermal_shutdown",
        FunctionID.SET_THERMAL_SHUTDOWN,
        (Decimal("3"), False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call("get_thermal_shutdown", FunctionID.GET_THERMAL_SHUTDOWN, (), reply=("B", (3,)), result=Decimal("3")),
    Call(
        "set_gpio_configuration",
        FunctionID.SET_GPIO_CONFIGURATION,
        (1, Decimal("0.003"), Decimal("0.009155552842799157689138462477")),
        sent=("B H H", (1, 3, 3)),
    ),
    Call(
        "set_gpio_configuration",
        FunctionID.SET_GPIO_CONFIGURATION,
        (1, Decimal("0.003"), Decimal("0.009155552842799157689138462477"), False),
        sent=("B H H", (1, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_gpio_configuration",
        FunctionID.GET_GPIO_CONFIGURATION,
        (1,),
        sent=("B", (1,)),
        reply=("H H", (3, 4)),
        result=GetGPIOConfiguration(Decimal("0.003"), Decimal("0.01220740379039887691885128330")),
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
        "set_cw_led_config", FunctionID.SET_CW_LED_CONFIG, (DEVICE.CWLEDConfig.SHOW_CW_AS_BACKWARD,), sent=("B", (4,))
    ),
    Call(
        "set_cw_led_config",
        FunctionID.SET_CW_LED_CONFIG,
        (DEVICE.CWLEDConfig.SHOW_CW_AS_BACKWARD, False),
        sent=("B", (4,)),
        response_expected=False,
    ),
    Call(
        "get_cw_led_config",
        FunctionID.GET_CW_LED_CONFIG,
        (),
        reply=("B", (4,)),
        result=DEVICE.CWLEDConfig.SHOW_CW_AS_BACKWARD,
    ),
    Call(
        "set_ccw_led_config",
        FunctionID.SET_CCW_LED_CONFIG,
        (DEVICE.CCWLEDConfig.SHOW_CCW_AS_BACKWARD,),
        sent=("B", (4,)),
    ),
    Call(
        "set_ccw_led_config",
        FunctionID.SET_CCW_LED_CONFIG,
        (DEVICE.CCWLEDConfig.SHOW_CCW_AS_BACKWARD, False),
        sent=("B", (4,)),
        response_expected=False,
    ),
    Call(
        "get_ccw_led_config",
        FunctionID.GET_CCW_LED_CONFIG,
        (),
        reply=("B", (4,)),
        result=DEVICE.CCWLEDConfig.SHOW_CCW_AS_BACKWARD,
    ),
    Call(
        "set_gpio_led_config",
        FunctionID.SET_GPIO_LED_CONFIG,
        (1, DEVICE.GPIOLEDConfig.SHOW_GPIO_ACTIVE_LOW),
        sent=("B B", (1, 4)),
    ),
    Call(
        "set_gpio_led_config",
        FunctionID.SET_GPIO_LED_CONFIG,
        (1, DEVICE.GPIOLEDConfig.SHOW_GPIO_ACTIVE_LOW, False),
        sent=("B B", (1, 4)),
        response_expected=False,
    ),
    Call(
        "get_gpio_led_config",
        FunctionID.GET_GPIO_LED_CONFIG,
        (1,),
        sent=("B", (1,)),
        reply=("B", (4,)),
        result=DEVICE.GPIOLEDConfig.SHOW_GPIO_ACTIVE_LOW,
    ),
    Call(
        "set_emergency_shutdown_callback_configuration",
        FunctionID.SET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_emergency_shutdown_callback_configuration",
        FunctionID.SET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_emergency_shutdown_callback_configuration",
        FunctionID.GET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "set_velocity_reached_callback_configuration",
        FunctionID.SET_VELOCITY_REACHED_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_velocity_reached_callback_configuration",
        FunctionID.SET_VELOCITY_REACHED_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_velocity_reached_callback_configuration",
        FunctionID.GET_VELOCITY_REACHED_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "set_current_velocity_callback_configuration",
        FunctionID.SET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_current_velocity_callback_configuration",
        FunctionID.SET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_current_velocity_callback_configuration",
        FunctionID.GET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "get_value",
        FunctionID.GET_CURRENT_VELOCITY,
        (2,),
        reply=("h", (3,)),
        result=Decimal("0.009155552842799157689138462477"),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION,
        (2, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "get_value",
        FunctionID.GET_GPIO_STATE,
        (3,),
        reply=("2!", ([i % 2 == 0 for i in range(2)],)),
        result=tuple(i % 2 == 0 for i in range(2)),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_velocity", (Decimal("100.0030518509475997192297128"),)),
    ("set_motion", (Decimal("200.0061037018951994384594256"), Decimal("0.009155552842799157689138462477"))),
    ("set_motion", (Decimal("0.009155552842799157689138462477"), Decimal("200.0061037018951994384594256"))),
    ("set_drive_mode", (12345,)),
    ("set_pwm_frequency", (Decimal("20001"),)),
    ("set_thermal_shutdown", (Decimal("256"),)),
    ("set_gpio_configuration", (2, Decimal("0.003"), Decimal("0.009155552842799157689138462477"))),
    ("set_gpio_configuration", (1, Decimal("65.536"), Decimal("0.009155552842799157689138462477"))),
    ("set_gpio_configuration", (1, Decimal("0.003"), Decimal("200.0061037018951994384594256"))),
    ("get_gpio_configuration", (2,)),
    ("set_gpio_action", (2, DEVICE.GPIOAction.CALLBACK_FALLING_EDGE)),
    ("set_gpio_action", (1, 12345)),
    ("get_gpio_action", (2,)),
    ("set_error_led_config", (12345,)),
    ("set_cw_led_config", (12345,)),
    ("set_ccw_led_config", (12345,)),
    ("set_gpio_led_config", (2, DEVICE.GPIOLEDConfig.SHOW_GPIO_ACTIVE_LOW)),
    ("set_gpio_led_config", (1, 12345)),
    ("get_gpio_led_config", (2,)),
    ("set_current_velocity_callback_configuration", (Decimal("4294967.296"), True)),
    ("get_value", (4,)),
    ("set_callback_configuration", (4,)),
    ("get_callback_configuration", (4,)),
]


def test_identity(device: BrickletPerformanceDC) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2156
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Performance DC Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_emergency_shutdown(device: BrickletPerformanceDC, connection: FakeConnection) -> None:
    """The callback EMERGENCY_SHUTDOWN is converted to an event."""
    connection.callback(CallbackID.EMERGENCY_SHUTDOWN)
    assert summary(read_events(device)) == [(0, CallbackID.EMERGENCY_SHUTDOWN, None)]


def test_callback_velocity_reached(device: BrickletPerformanceDC, connection: FakeConnection) -> None:
    """The callback VELOCITY_REACHED is converted to an event."""
    connection.callback(CallbackID.VELOCITY_REACHED, "h", *(3,))
    assert summary(read_events(device)) == [
        (1, CallbackID.VELOCITY_REACHED, Decimal("0.009155552842799157689138462477"))
    ]


def test_callback_current_velocity(device: BrickletPerformanceDC, connection: FakeConnection) -> None:
    """The callback CURRENT_VELOCITY is converted to an event."""
    connection.callback(CallbackID.CURRENT_VELOCITY, "h", *(3,))
    assert summary(read_events(device)) == [
        (2, CallbackID.CURRENT_VELOCITY, Decimal("0.009155552842799157689138462477"))
    ]


def test_callback_gpio_state(device: BrickletPerformanceDC, connection: FakeConnection) -> None:
    """The callback GPIO_STATE is converted to an event."""
    connection.callback(CallbackID.GPIO_STATE, "2!", *([i % 2 == 0 for i in range(2)],))
    assert summary(read_events(device)) == [(3, CallbackID.GPIO_STATE, tuple(i % 2 == 0 for i in range(2)))]
