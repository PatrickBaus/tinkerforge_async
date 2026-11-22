"""Tests for the Piezo Speaker Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2, GetAlarm, GetBeep
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletPiezoSpeakerV2
FunctionID = BrickletPiezoSpeakerV2.FunctionID
CallbackID = BrickletPiezoSpeakerV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_BEEP": 1,
    "GET_BEEP": 2,
    "SET_ALARM": 3,
    "GET_ALARM": 4,
    "UPDATE_VOLUME": 5,
    "UPDATE_FREQUENCY": 6,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"BEEP_FINISHED": 7, "ALARM_FINISHED": 8}

CALLS: list[Call] = [
    Call(
        "set_beep",
        FunctionID.SET_BEEP,
        (Decimal("50"), 3, DEVICE.BeepDuration.INFINITE),
        sent=("H B I", (50, 3, 4294967295)),
    ),
    Call(
        "set_beep",
        FunctionID.SET_BEEP,
        (Decimal("50"), 3, DEVICE.BeepDuration.INFINITE, False),
        sent=("H B I", (50, 3, 4294967295)),
        response_expected=False,
    ),
    Call(
        "get_beep",
        FunctionID.GET_BEEP,
        (),
        reply=("H B I I", (50, 4, 4294967295, 6)),
        result=GetBeep(Decimal("50"), 4, DEVICE.BeepDuration.INFINITE, Decimal("0.006")),
    ),
    Call(
        "set_alarm",
        FunctionID.SET_ALARM,
        (Decimal("50"), Decimal("51"), Decimal("3"), Decimal("0.003"), 3, DEVICE.AlarmDuration.INFINITE),
        sent=("H H H H B I", (50, 51, 3, 3, 3, 4294967295)),
    ),
    Call(
        "set_alarm",
        FunctionID.SET_ALARM,
        (Decimal("50"), Decimal("51"), Decimal("3"), Decimal("0.003"), 3, DEVICE.AlarmDuration.INFINITE, False),
        sent=("H H H H B I", (50, 51, 3, 3, 3, 4294967295)),
        response_expected=False,
    ),
    Call(
        "get_alarm",
        FunctionID.GET_ALARM,
        (),
        reply=("H H H H B I I H", (50, 51, 50, 6, 7, 4294967295, 4294967295, 50)),
        result=GetAlarm(
            Decimal("50"),
            Decimal("51"),
            Decimal("50"),
            Decimal("0.006"),
            7,
            DEVICE.AlarmDuration.INFINITE,
            DEVICE.AlarmDuration.INFINITE,
            Decimal("50"),
        ),
    ),
    Call("update_volume", FunctionID.UPDATE_VOLUME, (3,), sent=("B", (3,))),
    Call("update_volume", FunctionID.UPDATE_VOLUME, (3, False), sent=("B", (3,)), response_expected=False),
    Call("update_frequency", FunctionID.UPDATE_FREQUENCY, (Decimal("50"),), sent=("H", (50,))),
    Call(
        "update_frequency",
        FunctionID.UPDATE_FREQUENCY,
        (Decimal("50"), False),
        sent=("H", (50,)),
        response_expected=False,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_beep", (Decimal("15001"), 3, DEVICE.BeepDuration.INFINITE)),
    ("set_beep", (Decimal("50"), 11, DEVICE.BeepDuration.INFINITE)),
    ("set_beep", (Decimal("50"), 3, 12345)),
    ("set_alarm", (Decimal("15000"), Decimal("51"), Decimal("3"), Decimal("0.003"), 3, DEVICE.AlarmDuration.INFINITE)),
    ("set_alarm", (Decimal("50"), Decimal("15001"), Decimal("3"), Decimal("0.003"), 3, DEVICE.AlarmDuration.INFINITE)),
    ("set_alarm", (Decimal("50"), Decimal("51"), Decimal("14951"), Decimal("0.003"), 3, DEVICE.AlarmDuration.INFINITE)),
    ("set_alarm", (Decimal("50"), Decimal("51"), Decimal("3"), Decimal("65.536"), 3, DEVICE.AlarmDuration.INFINITE)),
    ("set_alarm", (Decimal("50"), Decimal("51"), Decimal("3"), Decimal("0.003"), 11, DEVICE.AlarmDuration.INFINITE)),
    ("set_alarm", (Decimal("50"), Decimal("51"), Decimal("3"), Decimal("0.003"), 3, 12345)),
    ("update_volume", (11,)),
    ("update_frequency", (Decimal("15001"),)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2145
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Piezo Speaker Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_beep_finished(device, connection):
    """The callback BEEP_FINISHED is converted to an event."""
    connection.callback(CallbackID.BEEP_FINISHED)
    assert summary(read_events(device)) == [(0, CallbackID.BEEP_FINISHED, None)]


def test_callback_alarm_finished(device, connection):
    """The callback ALARM_FINISHED is converted to an event."""
    connection.callback(CallbackID.ALARM_FINISHED)
    assert summary(read_events(device)) == [(1, CallbackID.ALARM_FINISHED, None)]
