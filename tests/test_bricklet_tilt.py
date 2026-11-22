"""Tests for the Tilt Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_tilt import BrickletTilt
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletTilt
FunctionID = BrickletTilt.FunctionID
CallbackID = BrickletTilt.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_TILT_STATE": 1,
    "ENABLE_TILT_STATE_CALLBACK": 2,
    "DISABLE_TILT_STATE_CALLBACK": 3,
    "IS_TILT_STATE_CALLBACK_ENABLED": 4,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"TILT_STATE": 5}

CALLS: list[Call] = [
    Call("get_tilt_state", FunctionID.GET_TILT_STATE, (), reply=("B", (2,)), result=DEVICE.TiltState.CLOSED_VIBRATING),
    Call("enable_tilt_state_callback", FunctionID.ENABLE_TILT_STATE_CALLBACK, ()),
    Call("enable_tilt_state_callback", FunctionID.ENABLE_TILT_STATE_CALLBACK, (False,), response_expected=False),
    Call("disable_tilt_state_callback", FunctionID.DISABLE_TILT_STATE_CALLBACK, ()),
    Call("disable_tilt_state_callback", FunctionID.DISABLE_TILT_STATE_CALLBACK, (False,), response_expected=False),
    Call(
        "is_tilt_state_callback_enabled",
        FunctionID.IS_TILT_STATE_CALLBACK_ENABLED,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call("get_value", FunctionID.GET_TILT_STATE, (0,), reply=("B", (2,)), result=DEVICE.TiltState.CLOSED_VIBRATING),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("get_value", (1,)),
]


def test_identity(device: BrickletTilt) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 239
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Tilt Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_tilt_state(device: BrickletTilt, connection: FakeConnection) -> None:
    """The callback TILT_STATE is converted to an event."""
    connection.callback(CallbackID.TILT_STATE, "B", *(2,))
    assert summary(read_events(device)) == [(0, CallbackID.TILT_STATE, DEVICE.TiltState.CLOSED_VIBRATING)]
