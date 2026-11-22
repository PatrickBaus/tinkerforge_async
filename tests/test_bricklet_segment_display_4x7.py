"""Tests for the Segment Display 4x7 Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7, GetSegments

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, read_events, summary

DEVICE = BrickletSegmentDisplay4x7
FunctionID = BrickletSegmentDisplay4x7.FunctionID
CallbackID = BrickletSegmentDisplay4x7.CallbackID

CALLS = [
    Call("set_segments", FunctionID.SET_SEGMENTS, sent=("4B B !", ((0, 0, 0, 0), 7, False))),
    Call(
        "set_segments",
        FunctionID.SET_SEGMENTS,
        ((1, 2, 3, 127), 0, True, False),
        sent=("4B B !", ((1, 2, 3, 127), 0, True)),
        response_expected=False,
    ),
    Call(
        "get_segments",
        FunctionID.GET_SEGMENTS,
        reply=("4B B !", ((1, 2, 3, 127), 7, True)),
        result=GetSegments((1, 2, 3, 127), 7, True),
    ),
    Call("start_counter", FunctionID.START_COUNTER, (-999, 9999), sent=("h h h I", (-999, 9999, 1, 1000))),
    Call(
        "start_counter",
        FunctionID.START_COUNTER,
        (10, 0, -1, Decimal("0.1")),
        sent=("h h h I", (10, 0, -1, 100)),
    ),
    Call("get_counter_value", FunctionID.GET_COUNTER_VALUE, reply=("H", (42,)), result=42),
]

REJECTED = [
    ("set_segments", ((0, 0, 0, 128),)),
    ("set_segments", ((-1, 0, 0, 0),)),
    ("set_segments", ((0, 0, 0, 0), 8)),
    ("set_segments", ((0, 0, 0, 0), -1)),
    ("start_counter", (-1000, 0)),
    ("start_counter", (10000, 0)),
    ("start_counter", (0, -1000)),
    ("start_counter", (0, 10000)),
    ("start_counter", (0, 1, -1000)),
    ("start_counter", (0, 1, 10000)),
    ("start_counter", (0, 1, 1, -1)),
    ("start_counter", (0, 1, 1, 2**32 / 1000)),
]


def test_identity(bricklet: BrickletSegmentDisplay4x7) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 237
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Segment Display 4x7 Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet: BrickletSegmentDisplay4x7, connection: FakeConnection) -> None:
    """The callback has no payload."""
    connection.callback(CallbackID.COUNTER_FINISHED)
    assert summary(read_events(bricklet)) == [(0, CallbackID.COUNTER_FINISHED, None)]
    assert summary(read_events(bricklet, sids=(0,))) == [(0, CallbackID.COUNTER_FINISHED, None)]
    assert not read_events(bricklet, sids=(1,))
