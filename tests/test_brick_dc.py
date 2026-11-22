"""Tests for the DC Brick. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_dc import BrickDC, GetProtocol1BrickletName
from tinkerforge_async.devices import GetSPITFPBaudrateConfig, GetSPITFPErrorCount
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickDC
FunctionID = BrickDC.FunctionID
CallbackID = BrickDC.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_VELOCITY": 1,
    "GET_VELOCITY": 2,
    "GET_CURRENT_VELOCITY": 3,
    "SET_ACCELERATION": 4,
    "GET_ACCELERATION": 5,
    "SET_PWM_FREQUENCY": 6,
    "GET_PWM_FREQUENCY": 7,
    "FULL_BRAKE": 8,
    "GET_STACK_INPUT_VOLTAGE": 9,
    "GET_EXTERNAL_INPUT_VOLTAGE": 10,
    "GET_CURRENT_CONSUMPTION": 11,
    "ENABLE": 12,
    "DISABLE": 13,
    "IS_ENABLED": 14,
    "SET_MINIMUM_VOLTAGE": 15,
    "GET_MINIMUM_VOLTAGE": 16,
    "SET_DRIVE_MODE": 17,
    "GET_DRIVE_MODE": 18,
    "SET_CURRENT_VELOCITY_PERIOD": 19,
    "GET_CURRENT_VELOCITY_PERIOD": 20,
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
    "UNDER_VOLTAGE": 21,
    "EMERGENCY_SHUTDOWN": 22,
    "VELOCITY_REACHED": 23,
    "CURRENT_VELOCITY": 24,
}

CALLS: list[Call] = [
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
        "set_acceleration",
        FunctionID.SET_ACCELERATION,
        (Decimal("0.009155552842799157689138462477"),),
        sent=("H", (3,)),
    ),
    Call(
        "set_acceleration",
        FunctionID.SET_ACCELERATION,
        (Decimal("0.009155552842799157689138462477"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call(
        "get_acceleration",
        FunctionID.GET_ACCELERATION,
        (),
        reply=("H", (3,)),
        result=Decimal("0.009155552842799157689138462477"),
    ),
    Call("set_pwm_frequency", FunctionID.SET_PWM_FREQUENCY, (Decimal("3"),), sent=("H", (3,))),
    Call(
        "set_pwm_frequency",
        FunctionID.SET_PWM_FREQUENCY,
        (Decimal("3"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_pwm_frequency", FunctionID.GET_PWM_FREQUENCY, (), reply=("H", (3,)), result=Decimal("3")),
    Call("full_brake", FunctionID.FULL_BRAKE, ()),
    Call("full_brake", FunctionID.FULL_BRAKE, (False,), response_expected=False),
    Call("get_stack_input_voltage", FunctionID.GET_STACK_INPUT_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "get_external_input_voltage",
        FunctionID.GET_EXTERNAL_INPUT_VOLTAGE,
        (),
        reply=("H", (3,)),
        result=Decimal("0.003"),
    ),
    Call("get_current_consumption", FunctionID.GET_CURRENT_CONSUMPTION, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("enable", FunctionID.ENABLE, ()),
    Call("enable", FunctionID.ENABLE, (False,), response_expected=False),
    Call("disable", FunctionID.DISABLE, ()),
    Call("disable", FunctionID.DISABLE, (False,), response_expected=False),
    Call("is_enabled", FunctionID.IS_ENABLED, (), reply=("!", (True,)), result=True),
    Call("set_minimum_voltage", FunctionID.SET_MINIMUM_VOLTAGE, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_minimum_voltage",
        FunctionID.SET_MINIMUM_VOLTAGE,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_minimum_voltage", FunctionID.GET_MINIMUM_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_drive_mode", FunctionID.SET_DRIVE_MODE, (DEVICE.DriveMode.DRIVE_COAST,), sent=("B", (1,))),
    Call(
        "set_drive_mode",
        FunctionID.SET_DRIVE_MODE,
        (DEVICE.DriveMode.DRIVE_COAST, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call("get_drive_mode", FunctionID.GET_DRIVE_MODE, (), reply=("B", (1,)), result=DEVICE.DriveMode.DRIVE_COAST),
    Call("set_current_velocity_period", FunctionID.SET_CURRENT_VELOCITY_PERIOD, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_current_velocity_period",
        FunctionID.SET_CURRENT_VELOCITY_PERIOD,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call(
        "get_current_velocity_period",
        FunctionID.GET_CURRENT_VELOCITY_PERIOD,
        (),
        reply=("H", (3,)),
        result=Decimal("0.003"),
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
    Call(
        "get_value",
        FunctionID.GET_CURRENT_VELOCITY,
        (3,),
        reply=("h", (3,)),
        result=Decimal("0.009155552842799157689138462477"),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_velocity", (Decimal("100.0030518509475997192297128"),)),
    ("set_acceleration", (Decimal("200.0061037018951994384594256"),)),
    ("set_pwm_frequency", (Decimal("20001"),)),
    ("set_minimum_voltage", (Decimal("65.536"),)),
    ("set_drive_mode", (12345,)),
    ("set_current_velocity_period", (Decimal("65.536"),)),
    ("set_spitfp_baudrate_config", (True, 2000001)),
    ("get_send_timeout_count", (12345,)),
    ("set_spitfp_baudrate", ("b", 2000001)),
    ("write_bricklet_plugin", ("b", 256, [i % 256 for i in range(32)])),
    ("write_bricklet_plugin", ("b", 3, ([i % 256 for i in range(32)])[:-1])),
    ("read_bricklet_plugin", ("b", 256)),
    ("get_value", (4,)),
]


def test_identity(device: BrickDC) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 11
    assert device.get_api_version() == (2, 0, 3)
    assert str(device).startswith("DC Brick with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_under_voltage(device: BrickDC, connection: FakeConnection) -> None:
    """The callback UNDER_VOLTAGE is converted to an event."""
    connection.callback(CallbackID.UNDER_VOLTAGE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.UNDER_VOLTAGE, Decimal("0.003"))]


def test_callback_emergency_shutdown(device: BrickDC, connection: FakeConnection) -> None:
    """The callback EMERGENCY_SHUTDOWN is converted to an event."""
    connection.callback(CallbackID.EMERGENCY_SHUTDOWN)
    assert summary(read_events(device)) == [(1, CallbackID.EMERGENCY_SHUTDOWN, None)]


def test_callback_velocity_reached(device: BrickDC, connection: FakeConnection) -> None:
    """The callback VELOCITY_REACHED is converted to an event."""
    connection.callback(CallbackID.VELOCITY_REACHED, "h", *(3,))
    assert summary(read_events(device)) == [
        (2, CallbackID.VELOCITY_REACHED, Decimal("0.009155552842799157689138462477"))
    ]


def test_callback_current_velocity(device: BrickDC, connection: FakeConnection) -> None:
    """The callback CURRENT_VELOCITY is converted to an event."""
    connection.callback(CallbackID.CURRENT_VELOCITY, "h", *(3,))
    assert summary(read_events(device)) == [
        (3, CallbackID.CURRENT_VELOCITY, Decimal("0.009155552842799157689138462477"))
    ]
