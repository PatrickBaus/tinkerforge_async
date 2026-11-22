"""Tests for the HAT Zero Brick. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.brick_hat_zero import BrickHATZero
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickHATZero
FunctionID = BrickHATZero.FunctionID
CallbackID = BrickHATZero.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_USB_VOLTAGE": 1,
    "SET_USB_VOLTAGE_CALLBACK_CONFIGURATION": 2,
    "GET_USB_VOLTAGE_CALLBACK_CONFIGURATION": 3,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"USB_VOLTAGE": 4}

CALLS: list[Call] = [
    Call("get_usb_voltage", FunctionID.GET_USB_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "set_usb_voltage_callback_configuration",
        FunctionID.SET_USB_VOLTAGE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003")),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_usb_voltage_callback_configuration",
        FunctionID.SET_USB_VOLTAGE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_usb_voltage_callback_configuration",
        FunctionID.GET_USB_VOLTAGE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c H H", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.006"), Decimal("0.007")
        ),
    ),
    Call("get_value", FunctionID.GET_USB_VOLTAGE, (0,), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_USB_VOLTAGE_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
        sent=("I ! c H H", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_USB_VOLTAGE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c H H", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_usb_voltage_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_usb_voltage_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_usb_voltage_callback_configuration", (Decimal("0.003"), True, "o", Decimal("65.536"), Decimal("0.003"))),
    ("set_usb_voltage_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.003"), Decimal("65.536"))),
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device: BrickHATZero) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 112
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("HAT Zero Brick with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_usb_voltage(device: BrickHATZero, connection: FakeConnection) -> None:
    """The callback USB_VOLTAGE is converted to an event."""
    connection.callback(CallbackID.USB_VOLTAGE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.USB_VOLTAGE, Decimal("0.003"))]
