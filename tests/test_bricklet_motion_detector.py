"""Tests for the Motion Detector Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_motion_detector import BrickletMotionDetector
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletMotionDetector
FunctionID = BrickletMotionDetector.FunctionID
CallbackID = BrickletMotionDetector.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_MOTION_DETECTED": 1,
    "SET_STATUS_LED_CONFIG": 4,
    "GET_STATUS_LED_CONFIG": 5,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"MOTION_DETECTED": 2, "DETECTION_CYCLE_ENDED": 3}

CALLS: list[Call] = [
    Call("get_motion_detected", FunctionID.GET_MOTION_DETECTED, (), reply=("B", (1,)), result=DEVICE.Motion.DETECTED),
    Call(
        "set_status_led_config",
        FunctionID.SET_STATUS_LED_CONFIG,
        (DEVICE.StatusLEDConfig.SHOW_STATUS,),
        sent=("B", (2,)),
    ),
    Call(
        "set_status_led_config",
        FunctionID.SET_STATUS_LED_CONFIG,
        (DEVICE.StatusLEDConfig.SHOW_STATUS, False),
        sent=("B", (2,)),
        response_expected=False,
    ),
    Call(
        "get_status_led_config",
        FunctionID.GET_STATUS_LED_CONFIG,
        (),
        reply=("B", (2,)),
        result=DEVICE.StatusLEDConfig.SHOW_STATUS,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_status_led_config", (12345,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 233
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Motion Detector Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_motion_detected(device, connection):
    """The callback MOTION_DETECTED is converted to an event."""
    connection.callback(CallbackID.MOTION_DETECTED)
    assert summary(read_events(device)) == [(0, CallbackID.MOTION_DETECTED, None)]


def test_callback_detection_cycle_ended(device, connection):
    """The callback DETECTION_CYCLE_ENDED is converted to an event."""
    connection.callback(CallbackID.DETECTION_CYCLE_ENDED)
    assert summary(read_events(device)) == [(1, CallbackID.DETECTION_CYCLE_ENDED, None)]
