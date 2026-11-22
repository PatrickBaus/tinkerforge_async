"""Tests for the Remote Switch Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_remote_switch_v2 import (
    BrickletRemoteSwitchV2,
    GetRemoteConfiguration,
    GetRemoteStatusA,
    GetRemoteStatusB,
    GetRemoteStatusC,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletRemoteSwitchV2
FunctionID = BrickletRemoteSwitchV2.FunctionID
CallbackID = BrickletRemoteSwitchV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_SWITCHING_STATE": 1,
    "SET_REPEATS": 3,
    "GET_REPEATS": 4,
    "SWITCH_SOCKET_A": 5,
    "SWITCH_SOCKET_B": 6,
    "DIM_SOCKET_B": 7,
    "SWITCH_SOCKET_C": 8,
    "SET_REMOTE_CONFIGURATION": 9,
    "GET_REMOTE_CONFIGURATION": 10,
    "GET_REMOTE_STATUS_A": 11,
    "GET_REMOTE_STATUS_B": 12,
    "GET_REMOTE_STATUS_C": 13,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "SWITCHING_DONE": 2,
    "REMOTE_STATUS_A": 14,
    "REMOTE_STATUS_B": 15,
    "REMOTE_STATUS_C": 16,
}

CALLS: list[Call] = [
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
    Call(
        "set_remote_configuration",
        FunctionID.SET_REMOTE_CONFIGURATION,
        (DEVICE.RemoteType.C, 3, True),
        sent=("B H !", (2, 3, True)),
    ),
    Call(
        "set_remote_configuration",
        FunctionID.SET_REMOTE_CONFIGURATION,
        (DEVICE.RemoteType.C, 3, True, False),
        sent=("B H !", (2, 3, True)),
        response_expected=False,
    ),
    Call(
        "get_remote_configuration",
        FunctionID.GET_REMOTE_CONFIGURATION,
        (),
        reply=("B H !", (2, 4, True)),
        result=GetRemoteConfiguration(DEVICE.RemoteType.C, 4, True),
    ),
    Call(
        "get_remote_status_a",
        FunctionID.GET_REMOTE_STATUS_A,
        (),
        reply=("B B B H", (3, 4, 1, 6)),
        result=GetRemoteStatusA(3, 4, DEVICE.SwitchTo.ON, 6),
    ),
    Call(
        "get_remote_status_b",
        FunctionID.GET_REMOTE_STATUS_B,
        (),
        reply=("I B B B H", (3, 4, 1, 6, 7)),
        result=GetRemoteStatusB(3, 4, DEVICE.SwitchTo.ON, 6, 7),
    ),
    Call(
        "get_remote_status_c",
        FunctionID.GET_REMOTE_STATUS_C,
        (),
        reply=("c B B H", ("a", 4, 1, 6)),
        result=GetRemoteStatusC("a", 4, DEVICE.SwitchTo.ON, 6),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
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
    ("set_remote_configuration", (12345, 3, True)),
    ("set_remote_configuration", (DEVICE.RemoteType.C, 65536, True)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 289
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Remote Switch Bricklet 2.0 with uid 12345")


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


def test_callback_remote_status_a(device, connection):
    """The callback REMOTE_STATUS_A is converted to an event."""
    connection.callback(CallbackID.REMOTE_STATUS_A, "B B B H", *(3, 4, 1, 6))
    assert summary(read_events(device)) == [
        (1, CallbackID.REMOTE_STATUS_A, GetRemoteStatusA(3, 4, DEVICE.SwitchTo.ON, 6))
    ]


def test_callback_remote_status_b(device, connection):
    """The callback REMOTE_STATUS_B is converted to an event."""
    connection.callback(CallbackID.REMOTE_STATUS_B, "I B B B H", *(3, 4, 1, 6, 7))
    assert summary(read_events(device)) == [
        (2, CallbackID.REMOTE_STATUS_B, GetRemoteStatusB(3, 4, DEVICE.SwitchTo.ON, 6, 7))
    ]


def test_callback_remote_status_c(device, connection):
    """The callback REMOTE_STATUS_C is converted to an event."""
    connection.callback(CallbackID.REMOTE_STATUS_C, "c B B H", *("a", 4, 1, 6))
    assert summary(read_events(device)) == [
        (3, CallbackID.REMOTE_STATUS_C, GetRemoteStatusC("a", 4, DEVICE.SwitchTo.ON, 6))
    ]
