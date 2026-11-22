"""Tests for the Solid State Relay Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_solid_state_relay import BrickletSolidStateRelay, GetMonoflop
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletSolidStateRelay
FunctionID = BrickletSolidStateRelay.FunctionID
CallbackID = BrickletSolidStateRelay.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {"SET_STATE": 1, "GET_STATE": 2, "SET_MONOFLOP": 3, "GET_MONOFLOP": 4}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"MONOFLOP_DONE": 5}

CALLS: list[Call] = [
    Call("set_state", FunctionID.SET_STATE, (True,), sent=("!", (True,))),
    Call("set_state", FunctionID.SET_STATE, (True, False), sent=("!", (True,)), response_expected=False),
    Call("get_state", FunctionID.GET_STATE, (), reply=("!", (True,)), result=True),
    Call("set_monoflop", FunctionID.SET_MONOFLOP, (True, Decimal("0.003")), sent=("! I", (True, 3))),
    Call(
        "set_monoflop",
        FunctionID.SET_MONOFLOP,
        (True, Decimal("0.003"), False),
        sent=("! I", (True, 3)),
        response_expected=False,
    ),
    Call(
        "get_monoflop",
        FunctionID.GET_MONOFLOP,
        (),
        reply=("! I I", (True, 4, 5)),
        result=GetMonoflop(True, Decimal("0.004"), Decimal("0.005")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_monoflop", (True, Decimal("4294967.296"))),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 244
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Solid State Relay Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_monoflop_done(device, connection):
    """The callback MONOFLOP_DONE is converted to an event."""
    connection.callback(CallbackID.MONOFLOP_DONE, "!", *(True,))
    assert summary(read_events(device)) == [(0, CallbackID.MONOFLOP_DONE, True)]
