"""Tests for the DC Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_dc_v2 import BrickletDCV2, GetMotion, GetPowerStatistics
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletDCV2
FunctionID = BrickletDCV2.FunctionID
CallbackID = BrickletDCV2.CallbackID

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
    "SET_ERROR_LED_CONFIG": 14,
    "GET_ERROR_LED_CONFIG": 15,
    "SET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION": 16,
    "GET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION": 17,
    "SET_VELOCITY_REACHED_CALLBACK_CONFIGURATION": 18,
    "GET_VELOCITY_REACHED_CALLBACK_CONFIGURATION": 19,
    "SET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION": 20,
    "GET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION": 21,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"EMERGENCY_SHUTDOWN": 22, "VELOCITY_REACHED": 23, "CURRENT_VELOCITY": 24}

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
        reply=("H H", (3, 4)),
        result=GetPowerStatistics(Decimal("0.003"), Decimal("0.004")),
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
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_velocity", (Decimal("100.0030518509475997192297128"),)),
    ("set_motion", (Decimal("200.0061037018951994384594256"), Decimal("0.009155552842799157689138462477"))),
    ("set_motion", (Decimal("0.009155552842799157689138462477"), Decimal("200.0061037018951994384594256"))),
    ("set_drive_mode", (12345,)),
    ("set_pwm_frequency", (Decimal("20001"),)),
    ("set_error_led_config", (12345,)),
    ("set_current_velocity_callback_configuration", (Decimal("4294967.296"), True)),
    ("get_value", (3,)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(device: BrickletDCV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2165
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("DC Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_emergency_shutdown(device: BrickletDCV2, connection: FakeConnection) -> None:
    """The callback EMERGENCY_SHUTDOWN is converted to an event."""
    connection.callback(CallbackID.EMERGENCY_SHUTDOWN)
    assert summary(read_events(device)) == [(0, CallbackID.EMERGENCY_SHUTDOWN, None)]


def test_callback_velocity_reached(device: BrickletDCV2, connection: FakeConnection) -> None:
    """The callback VELOCITY_REACHED is converted to an event."""
    connection.callback(CallbackID.VELOCITY_REACHED, "h", *(3,))
    assert summary(read_events(device)) == [
        (1, CallbackID.VELOCITY_REACHED, Decimal("0.009155552842799157689138462477"))
    ]


def test_callback_current_velocity(device: BrickletDCV2, connection: FakeConnection) -> None:
    """The callback CURRENT_VELOCITY is converted to an event."""
    connection.callback(CallbackID.CURRENT_VELOCITY, "h", *(3,))
    assert summary(read_events(device)) == [
        (2, CallbackID.CURRENT_VELOCITY, Decimal("0.009155552842799157689138462477"))
    ]
