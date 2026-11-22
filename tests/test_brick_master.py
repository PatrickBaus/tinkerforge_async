"""Tests for the functions of the Master Brick, that do not belong to an extension."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.brick_master import BrickMaster, GetProtocol1BrickletName, SetBrickletXMCFlashConfig
from tinkerforge_async.devices import BasicCallbackConfiguration
from tinkerforge_async.devices import FunctionID as DeviceFunctionID
from tinkerforge_async.devices import GetSPITFPBaudrateConfig, GetSPITFPErrorCount
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, read_events, summary

DEVICE = BrickMaster
FunctionID = BrickMaster.FunctionID
CallbackID = BrickMaster.CallbackID
ExtensionPosition = BrickMaster.ExtensionPosition
ExtensionType = BrickMaster.ExtensionType
ConnectionType = BrickMaster.ConnectionType
Port = BrickMaster.BrickletPort

CALLS = [
    # The voltages are transferred in mV, the current in mA
    Call("get_stack_voltage", FunctionID.GET_STACK_VOLTAGE, reply=("H", (12345,)), result=Decimal("12.345")),
    Call("get_stack_current", FunctionID.GET_STACK_CURRENT, reply=("H", (1500,)), result=Decimal("1.5")),
    Call("get_usb_voltage", FunctionID.GET_USB_VOLTAGE, reply=("H", (5010,)), result=Decimal("5.01")),
    # The temperature is transferred in 1/10 °C
    Call("get_chip_temperature", FunctionID.GET_CHIP_TEMPERATURE, reply=("h", (305,)), result=Decimal("303.65")),
    Call("get_chip_temperature", FunctionID.GET_CHIP_TEMPERATURE, reply=("h", (-100,)), result=Decimal("263.15")),
    Call(
        "set_extension_type",
        FunctionID.SET_EXTENSION_TYPE,
        (ExtensionPosition.TOP, ExtensionType.ETHERNET),
        sent=("B I", (1, 4)),
    ),
    Call(
        "set_extension_type",
        FunctionID.SET_EXTENSION_TYPE,
        (0, 2, False),
        sent=("B I", (0, 2)),
        response_expected=False,
    ),
    Call(
        "get_extension_type",
        FunctionID.GET_EXTENSION_TYPE,
        (1,),
        sent=("B", (1,)),
        reply=("I", (5,)),
        result=ExtensionType.WIFI2,
    ),
    Call(
        "set_stack_current_callback_period",
        FunctionID.SET_STACK_CURRENT_CALLBACK_PERIOD,
        (Decimal("0.5"),),
        sent=("I", (500,)),
    ),
    Call(
        "get_stack_current_callback_period",
        FunctionID.GET_STACK_CURRENT_CALLBACK_PERIOD,
        reply=("I", (500,)),
        result=Decimal("0.5"),
    ),
    Call("set_stack_voltage_callback_period", FunctionID.SET_STACK_VOLTAGE_CALLBACK_PERIOD, (1,), sent=("I", (1000,))),
    Call(
        "get_stack_voltage_callback_period",
        FunctionID.GET_STACK_VOLTAGE_CALLBACK_PERIOD,
        reply=("I", (1000,)),
        result=Decimal(1),
    ),
    Call("set_usb_voltage_callback_period", FunctionID.SET_USB_VOLTAGE_CALLBACK_PERIOD, (0,), sent=("I", (0,))),
    Call(
        "get_usb_voltage_callback_period",
        FunctionID.GET_USB_VOLTAGE_CALLBACK_PERIOD,
        reply=("I", (0,)),
        result=Decimal(0),
    ),
    Call(
        "set_stack_current_callback_threshold",
        FunctionID.SET_STACK_CURRENT_CALLBACK_THRESHOLD,
        (Threshold.GREATER_THAN, Decimal("1.5"), 0),
        sent=("c H H", (b">", 1500, 0)),
    ),
    Call(
        "set_stack_current_callback_threshold",
        FunctionID.SET_STACK_CURRENT_CALLBACK_THRESHOLD,
        ("i", 0.5, 2),
        sent=("c H H", (b"i", 500, 2000)),
    ),
    Call(
        "get_stack_current_callback_threshold",
        FunctionID.GET_STACK_CURRENT_CALLBACK_THRESHOLD,
        reply=("c H H", ("i", 500, 2000)),
        result=BasicCallbackConfiguration(Threshold.INSIDE, Decimal("0.5"), Decimal(2)),
    ),
    Call(
        "set_stack_voltage_callback_threshold",
        FunctionID.SET_STACK_VOLTAGE_CALLBACK_THRESHOLD,
        (Threshold.LESS_THAN, Decimal("11.5"), 0),
        sent=("c H H", (b"<", 11500, 0)),
    ),
    Call(
        "set_stack_voltage_callback_threshold",
        FunctionID.SET_STACK_VOLTAGE_CALLBACK_THRESHOLD,
        ("o", 11, 13),
        sent=("c H H", (b"o", 11000, 13000)),
    ),
    Call(
        "get_stack_voltage_callback_threshold",
        FunctionID.GET_STACK_VOLTAGE_CALLBACK_THRESHOLD,
        reply=("c H H", ("o", 11000, 13000)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal(11), Decimal(13)),
    ),
    Call(
        "set_usb_voltage_callback_threshold",
        FunctionID.SET_USB_VOLTAGE_CALLBACK_THRESHOLD,
        (Threshold.LESS_THAN, Decimal("4.75"), 0),
        sent=("c H H", (b"<", 4750, 0)),
    ),
    Call(
        "set_usb_voltage_callback_threshold",
        FunctionID.SET_USB_VOLTAGE_CALLBACK_THRESHOLD,
        ("x", 0, 0),
        sent=("c H H", (b"x", 0, 0)),
    ),
    Call(
        "get_usb_voltage_callback_threshold",
        FunctionID.GET_USB_VOLTAGE_CALLBACK_THRESHOLD,
        reply=("c H H", ("<", 4750, 0)),
        result=BasicCallbackConfiguration(Threshold.LESS_THAN, Decimal("4.75"), Decimal(0)),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (2,), sent=("I", (2000,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
    Call("set_spitfp_baudrate_config", FunctionID.SET_SPITFP_BAUDRATE_CONFIG, sent=("! I", (True, 400000))),
    Call(
        "set_spitfp_baudrate_config",
        FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
        (False, 2000000),
        sent=("! I", (False, 2000000)),
    ),
    Call(
        "get_spitfp_baudrate_config",
        FunctionID.GET_SPITFP_BAUDRATE_CONFIG,
        reply=("! I", (True, 400000)),
        result=GetSPITFPBaudrateConfig(True, 400000),
    ),
    Call(
        "get_send_timeout_count",
        FunctionID.GET_SEND_TIMEOUT_COUNT,
        (ConnectionType.RS485,),
        sent=("B", (4,)),
        reply=("I", (7,)),
        result=7,
    ),
    Call(
        "get_send_timeout_count", FunctionID.GET_SEND_TIMEOUT_COUNT, (1,), sent=("B", (1,)), reply=("I", (0,)), result=0
    ),
    Call("set_spitfp_baudrate", FunctionID.SET_SPITFP_BAUDRATE, (Port.A,), sent=("c I", (b"a", 1400000))),
    Call("set_spitfp_baudrate", FunctionID.SET_SPITFP_BAUDRATE, ("d", 400000), sent=("c I", (b"d", 400000))),
    Call(
        "get_spitfp_baudrate",
        FunctionID.GET_SPITFP_BAUDRATE,
        (Port.B,),
        sent=("c", (b"b",)),
        reply=("I", (1400000,)),
        result=1400000,
    ),
    Call(
        "get_spitfp_baudrate", FunctionID.GET_SPITFP_BAUDRATE, ("c",), sent=("c", (b"c",)), reply=("I", (1,)), result=1
    ),
    Call(
        "get_spitfp_error_count",
        FunctionID.GET_SPITFP_ERROR_COUNT,
        (Port.A,),
        sent=("c", (b"a",)),
        reply=("I I I I", (1, 2, 3, 4)),
        result=GetSPITFPErrorCount(1, 2, 3, 4),
    ),
    Call(
        "get_spitfp_error_count",
        FunctionID.GET_SPITFP_ERROR_COUNT,
        ("b",),
        sent=("c", (b"b",)),
        reply=("I I I I", (0, 0, 0, 0)),
        result=GetSPITFPErrorCount(0, 0, 0, 0),
    ),
    Call("enable_status_led", FunctionID.ENABLE_STATUS_LED),
    Call("disable_status_led", FunctionID.DISABLE_STATUS_LED, (False,), response_expected=False),
    Call("is_status_led_enabled", FunctionID.IS_STATUS_LED_ENABLED, reply=("!", (True,)), result=True),
    Call(
        "get_protocol1_bricklet_name",
        FunctionID.GET_PROTOCOL1_BRICKLET_NAME,
        (Port.A,),
        sent=("c", (b"a",)),
        reply=("B 3B 40s", (1, (2, 0, 1), b"Temperature Bricklet")),
        result=GetProtocol1BrickletName(1, (2, 0, 1), "Temperature Bricklet"),
    ),
    Call(
        "get_protocol1_bricklet_name",
        FunctionID.GET_PROTOCOL1_BRICKLET_NAME,
        ("b",),
        sent=("c", (b"b",)),
        reply=("B 3B 40s", (0, (0, 0, 0), b"")),
        result=GetProtocol1BrickletName(0, (0, 0, 0), ""),
    ),
    Call("get_connection_type", FunctionID.GET_CONNECTION_TYPE, reply=("B", (6,)), result=ConnectionType.ETHERNET),
    # Master Brick 3.0
    Call(
        "set_bricklet_xmc_flash_config",
        FunctionID.SET_BRICKLET_XMC_FLASH_CONFIG,
        (1, 2, 3, bytes(range(52))),
        sent=("I I I 52B", (1, 2, 3, list(range(52)))),
        reply=("I 60B", (7, list(range(60)))),
        result=SetBrickletXMCFlashConfig(7, tuple(range(60))),
    ),
    Call(
        "set_bricklet_xmc_flash_data",
        FunctionID.SET_BRICKLET_XMC_FLASH_DATA,
        (list(range(64)),),
        sent=("64B", (list(range(64)),)),
        reply=("I", (7,)),
        result=7,
    ),
    Call("set_bricklets_enabled", FunctionID.SET_BRICKLETS_ENABLED, (True,), sent=("!", (True,))),
    Call(
        "set_bricklets_enabled",
        FunctionID.SET_BRICKLETS_ENABLED,
        (0, False),
        sent=("!", (False,)),
        response_expected=False,
    ),
    Call("get_bricklets_enabled", FunctionID.GET_BRICKLETS_ENABLED, reply=("!", (True,)), result=True),
    # Inherited from the bricks with a microcontroller
    Call("reset", DeviceFunctionID.RESET, response_expected=False),
]

REJECTED = [
    ("set_extension_type", (2, 1)),
    ("set_extension_type", (0, 6)),
    ("set_stack_current_callback_threshold", ("?", 0, 0)),
    ("set_stack_voltage_callback_threshold", ("?", 0, 0)),
    ("set_usb_voltage_callback_threshold", ("?", 0, 0)),
    ("get_send_timeout_count", (8,)),
    ("set_spitfp_baudrate", ("y",)),
    ("get_spitfp_baudrate", ("y",)),
    ("get_spitfp_error_count", ("y",)),
    ("get_protocol1_bricklet_name", ("y",)),
    ("set_bricklet_xmc_flash_config", (1, 2, 3, bytes(51))),
    ("set_bricklet_xmc_flash_data", (bytes(65),)),
]


def test_identity(brick: BrickMaster) -> None:
    """The Brick knows who it is."""
    assert brick.DEVICE_IDENTIFIER.value == 13
    assert brick.get_api_version() == (2, 0, 4)
    assert str(brick).startswith("Master Brick with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(brick: BrickMaster, connection: FakeConnection) -> None:
    """The USB voltage is sid 0, the stack voltage sid 1 and the stack current sid 2. They are converted to V and A."""
    connection.callback(CallbackID.USB_VOLTAGE, "H", 5010)
    connection.callback(CallbackID.USB_VOLTAGE_REACHED, "H", 4750)
    connection.callback(CallbackID.STACK_VOLTAGE, "H", 12345)
    connection.callback(CallbackID.STACK_VOLTAGE_REACHED, "H", 11000)
    connection.callback(CallbackID.STACK_CURRENT, "H", 1500)
    connection.callback(CallbackID.STACK_CURRENT_REACHED, "H", 2000)
    assert summary(read_events(brick)) == [
        (0, CallbackID.USB_VOLTAGE, Decimal("5.01")),
        (0, CallbackID.USB_VOLTAGE_REACHED, Decimal("4.75")),
        (1, CallbackID.STACK_VOLTAGE, Decimal("12.345")),
        (1, CallbackID.STACK_VOLTAGE_REACHED, Decimal(11)),
        (2, CallbackID.STACK_CURRENT, Decimal("1.5")),
        (2, CallbackID.STACK_CURRENT_REACHED, Decimal(2)),
    ]
    assert summary(read_events(brick, sids=(2,))) == [
        (2, CallbackID.STACK_CURRENT, Decimal("1.5")),
        (2, CallbackID.STACK_CURRENT_REACHED, Decimal(2)),
    ]
