"""Tests for the Motion Detector Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from tinkerforge_async.bricklet_motion_detector_v2 import BrickletMotionDetectorV2, GetIndicator

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, summary

DEVICE = BrickletMotionDetectorV2
FunctionID = BrickletMotionDetectorV2.FunctionID
CallbackID = BrickletMotionDetectorV2.CallbackID

CALLS = [
    Call("get_motion_detected", FunctionID.GET_MOTION_DETECTED, reply=("B", (1,)), result=True),
    Call("get_value", FunctionID.GET_MOTION_DETECTED, (0,), reply=("B", (0,)), result=False),
    Call("set_sensitivity", FunctionID.SET_SENSITIVITY, sent=("B", (50,))),
    Call("set_sensitivity", FunctionID.SET_SENSITIVITY, (100, False), sent=("B", (100,)), response_expected=False),
    Call("get_sensitivity", FunctionID.GET_SENSITIVITY, reply=("B", (50,)), result=50),
    Call("set_indicator", FunctionID.SET_INDICATOR, sent=("B B B", (0, 0, 0))),
    Call("set_indicator", FunctionID.SET_INDICATOR, (1, 2, 255), sent=("B B B", (1, 2, 255))),
    Call("get_indicator", FunctionID.GET_INDICATOR, reply=("B B B", (1, 2, 255)), result=GetIndicator(1, 2, 255)),
]

REJECTED = [
    ("set_sensitivity", (-1,)),
    ("set_sensitivity", (101,)),
    ("set_indicator", (-1, 0, 0)),
    ("set_indicator", (256, 0, 0)),
    ("set_indicator", (0, -1, 0)),
    ("set_indicator", (0, 256, 0)),
    ("set_indicator", (0, 0, -1)),
    ("set_indicator", (0, 0, 256)),
    # Only the sid 0 has a value. The sid 1 is the event, that the detection cycle ended.
    ("get_value", (1,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 292
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Motion Detector Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet, connection):
    """The callbacks have no payload. A detected motion is sid 0, the end of the detection cycle is sid 1."""
    connection.callback(CallbackID.MOTION_DETECTED)
    connection.callback(CallbackID.DETECTION_CYCLE_ENDED)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.MOTION_DETECTED, None),
        (1, CallbackID.DETECTION_CYCLE_ENDED, None),
    ]
    assert summary(read_events(bricklet, sids=(1,))) == [(1, CallbackID.DETECTION_CYCLE_ENDED, None)]
