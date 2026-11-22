"""Tests for the Multi Touch Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_multi_touch import BrickletMultiTouch
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletMultiTouch
FunctionID = BrickletMultiTouch.FunctionID
CallbackID = BrickletMultiTouch.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_TOUCH_STATE": 1,
    "RECALIBRATE": 2,
    "SET_ELECTRODE_CONFIG": 3,
    "GET_ELECTRODE_CONFIG": 4,
    "SET_ELECTRODE_SENSITIVITY": 6,
    "GET_ELECTRODE_SENSITIVITY": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"TOUCH_STATE": 5}

CALLS: list[Call] = [
    Call("get_touch_state", FunctionID.GET_TOUCH_STATE, (), reply=("H", (3,)), result=3),
    Call("recalibrate", FunctionID.RECALIBRATE, ()),
    Call("recalibrate", FunctionID.RECALIBRATE, (False,), response_expected=False),
    Call("set_electrode_config", FunctionID.SET_ELECTRODE_CONFIG, (3,), sent=("H", (3,))),
    Call(
        "set_electrode_config", FunctionID.SET_ELECTRODE_CONFIG, (3, False), sent=("H", (3,)), response_expected=False
    ),
    Call("get_electrode_config", FunctionID.GET_ELECTRODE_CONFIG, (), reply=("H", (3,)), result=3),
    Call("set_electrode_sensitivity", FunctionID.SET_ELECTRODE_SENSITIVITY, (5,), sent=("B", (5,))),
    Call(
        "set_electrode_sensitivity",
        FunctionID.SET_ELECTRODE_SENSITIVITY,
        (5, False),
        sent=("B", (5,)),
        response_expected=False,
    ),
    Call("get_electrode_sensitivity", FunctionID.GET_ELECTRODE_SENSITIVITY, (), reply=("B", (5,)), result=5),
    Call("get_value", FunctionID.GET_TOUCH_STATE, (0,), reply=("H", (3,)), result=3),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_electrode_config", (8192,)),
    ("set_electrode_sensitivity", (202,)),
    ("get_value", (1,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 234
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Multi Touch Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_touch_state(device, connection):
    """The callback TOUCH_STATE is converted to an event."""
    connection.callback(CallbackID.TOUCH_STATE, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.TOUCH_STATE, 3)]
