"""Tests for the Remote Switch Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_remote_switch import BrickletRemoteSwitch
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletRemoteSwitch
FunctionID = BrickletRemoteSwitch.FunctionID
CallbackID = BrickletRemoteSwitch.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SWITCH_SOCKET": 1,
    "GET_SWITCHING_STATE": 2,
    "SET_REPEATS": 4,
    "GET_REPEATS": 5,
    "SWITCH_SOCKET_A": 6,
    "SWITCH_SOCKET_B": 7,
    "DIM_SOCKET_B": 8,
    "SWITCH_SOCKET_C": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"SWITCHING_DONE": 3}

CALLS: list[Call] = [
    Call("switch_socket", FunctionID.SWITCH_SOCKET, (3, 3, DEVICE.SwitchTo.ON), sent=("B B B", (3, 3, 1))),
    Call(
        "switch_socket",
        FunctionID.SWITCH_SOCKET,
        (3, 3, DEVICE.SwitchTo.ON, False),
        sent=("B B B", (3, 3, 1)),
        response_expected=False,
    ),
    Call(
        "get_switching_state", FunctionID.GET_SWITCHING_STATE, (), reply=("B", (1,)), result=DEVICE.SwitchingState.BUSY
    ),
    Call("set_repeats", FunctionID.SET_REPEATS, (3,), sent=("B", (3,))),
    Call("set_repeats", FunctionID.SET_REPEATS, (3, False), sent=("B", (3,)), response_expected=False),
    Call("get_repeats", FunctionID.GET_REPEATS, (), reply=("B", (3,)), result=3),
    Call("switch_socket_a", FunctionID.SWITCH_SOCKET_A, (3, 3, DEVICE.SwitchTo.ON), sent=("B B B", (3, 3, 1))),
    Call(
        "switch_socket_a",
        FunctionID.SWITCH_SOCKET_A,
        (3, 3, DEVICE.SwitchTo.ON, False),
        sent=("B B B", (3, 3, 1)),
        response_expected=False,
    ),
    Call("switch_socket_b", FunctionID.SWITCH_SOCKET_B, (3, 3, DEVICE.SwitchTo.ON), sent=("I B B", (3, 3, 1))),
    Call(
        "switch_socket_b",
        FunctionID.SWITCH_SOCKET_B,
        (3, 3, DEVICE.SwitchTo.ON, False),
        sent=("I B B", (3, 3, 1)),
        response_expected=False,
    ),
    Call("dim_socket_b", FunctionID.DIM_SOCKET_B, (3, 3, 3), sent=("I B B", (3, 3, 3))),
    Call("dim_socket_b", FunctionID.DIM_SOCKET_B, (3, 3, 3, False), sent=("I B B", (3, 3, 3)), response_expected=False),
    Call("switch_socket_c", FunctionID.SWITCH_SOCKET_C, ("a", 3, DEVICE.SwitchTo.ON), sent=("c B B", ("a", 3, 1))),
    Call(
        "switch_socket_c",
        FunctionID.SWITCH_SOCKET_C,
        ("a", 3, DEVICE.SwitchTo.ON, False),
        sent=("c B B", ("a", 3, 1)),
        response_expected=False,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("switch_socket", (32, 3, DEVICE.SwitchTo.ON)),
    ("switch_socket", (3, 32, DEVICE.SwitchTo.ON)),
    ("switch_socket", (3, 3, 12345)),
    ("set_repeats", (256,)),
    ("switch_socket_a", (32, 3, DEVICE.SwitchTo.ON)),
    ("switch_socket_a", (3, 32, DEVICE.SwitchTo.ON)),
    ("switch_socket_a", (3, 3, 12345)),
    ("switch_socket_b", (67108864, 3, DEVICE.SwitchTo.ON)),
    ("switch_socket_b", (3, 256, DEVICE.SwitchTo.ON)),
    ("switch_socket_b", (3, 3, 12345)),
    ("dim_socket_b", (67108864, 3, 3)),
    ("dim_socket_b", (3, 256, 3)),
    ("dim_socket_b", (3, 3, 256)),
    ("switch_socket_c", ("a", 17, DEVICE.SwitchTo.ON)),
    ("switch_socket_c", ("a", 3, 12345)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 235
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Remote Switch Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_switching_done(device, connection):
    """The callback SWITCHING_DONE is converted to an event."""
    connection.callback(CallbackID.SWITCHING_DONE)
    assert summary(read_events(device)) == [(0, CallbackID.SWITCHING_DONE, None)]
