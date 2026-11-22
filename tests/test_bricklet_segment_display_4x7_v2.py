"""Tests for the Segment Display 4x7 Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2, GetSegments

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, read_events, summary

DEVICE = BrickletSegmentDisplay4x7V2
FunctionID = BrickletSegmentDisplay4x7V2.FunctionID
CallbackID = BrickletSegmentDisplay4x7V2.CallbackID

CALLS = [
    Call("set_segments", FunctionID.SET_SEGMENTS, sent=("4B 2! !", ((0, 0, 0, 0), (False, False), False))),
    Call(
        "set_segments",
        FunctionID.SET_SEGMENTS,
        ((1, 2, 3, 255), (True, False), True, False),
        sent=("4B 2! !", ((1, 2, 3, 255), (True, False), True)),
        response_expected=False,
    ),
    Call(
        "get_segments",
        FunctionID.GET_SEGMENTS,
        reply=("4B 2! !", ((1, 2, 3, 255), (False, True), True)),
        result=GetSegments((1, 2, 3, 255), (False, True), True),
    ),
    Call("set_brightness", FunctionID.SET_BRIGHTNESS, sent=("B", (7,))),
    Call("set_brightness", FunctionID.SET_BRIGHTNESS, (0,), sent=("B", (0,))),
    Call("get_brightness", FunctionID.GET_BRIGHTNESS, reply=("B", (3,)), result=3),
    Call("set_numeric_value", FunctionID.SET_NUMERIC_VALUE, ((-2, -1, 4, 2),), sent=("4b", ((-2, -1, 4, 2),))),
    Call("set_selected_segment", FunctionID.SET_SELECTED_SEGMENT, (34, True), sent=("B !", (34, True))),
    Call("set_selected_segment", FunctionID.SET_SELECTED_SEGMENT, (0, False), sent=("B !", (0, False))),
    Call(
        "get_selected_segment",
        FunctionID.GET_SELECTED_SEGMENT,
        (34,),
        sent=("B", (34,)),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "start_counter",
        FunctionID.START_COUNTER,
        (-999, 9999, 1, Decimal("0.1")),
        sent=("h h h I", (-999, 9999, 1, 100)),
    ),
    Call("start_counter", FunctionID.START_COUNTER, (10, 0, -1, 1), sent=("h h h I", (10, 0, -1, 1000))),
    Call("get_counter_value", FunctionID.GET_COUNTER_VALUE, reply=("H", (42,)), result=42),
]

REJECTED = [
    ("set_segments", ((0, 0, 0),)),
    ("set_segments", ((0, 0, 0, 256),)),
    ("set_segments", ((-1, 0, 0, 0),)),
    ("set_segments", ((0, 0, 0, 0), (True,))),
    ("set_brightness", (8,)),
    ("set_brightness", (-1,)),
    ("set_selected_segment", (35, True)),
    ("set_selected_segment", (-1, True)),
    ("get_selected_segment", (35,)),
    ("get_selected_segment", (-1,)),
    ("start_counter", (-1000, 0, 1, 1)),
    ("start_counter", (10000, 0, 1, 1)),
    ("start_counter", (0, -1000, 1, 1)),
    ("start_counter", (0, 10000, 1, 1)),
    ("start_counter", (0, 1, -1000, 1)),
    ("start_counter", (0, 1, 10000, 1)),
]


def test_identity(bricklet: BrickletSegmentDisplay4x7V2) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2137
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Segment Display 4x7 Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet: BrickletSegmentDisplay4x7V2, connection: FakeConnection) -> None:
    """The callback has no payload."""
    connection.callback(CallbackID.COUNTER_FINISHED)
    assert summary(read_events(bricklet)) == [(0, CallbackID.COUNTER_FINISHED, None)]
