"""Tests for the Piezo Speaker Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_piezo_speaker import BrickletPiezoSpeaker
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletPiezoSpeaker
FunctionID = BrickletPiezoSpeaker.FunctionID
CallbackID = BrickletPiezoSpeaker.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {"BEEP": 1, "MORSE_CODE": 2, "CALIBRATE": 3}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"BEEP_FINISHED": 4, "MORSE_CODE_FINISHED": 5}

CALLS: list[Call] = [
    Call("beep", FunctionID.BEEP, (DEVICE.BeepDuration.INFINITE, Decimal("585")), sent=("I H", (4294967295, 585))),
    Call(
        "beep",
        FunctionID.BEEP,
        (DEVICE.BeepDuration.INFINITE, Decimal("585"), False),
        sent=("I H", (4294967295, 585)),
        response_expected=False,
    ),
    Call("morse_code", FunctionID.MORSE_CODE, ("abc", Decimal("585")), sent=("60s H", (b"abc", 585))),
    Call(
        "morse_code",
        FunctionID.MORSE_CODE,
        ("abc", Decimal("585"), False),
        sent=("60s H", (b"abc", 585)),
        response_expected=False,
    ),
    Call("calibrate", FunctionID.CALIBRATE, (), reply=("!", (True,)), result=True),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("beep", (12345, Decimal("585"))),
    ("beep", (DEVICE.BeepDuration.INFINITE, Decimal("7101"))),
    ("morse_code", ("abc", Decimal("7101"))),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 242
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Piezo Speaker Bricklet with uid 12345")


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


def test_callback_morse_code_finished(device, connection):
    """The callback MORSE_CODE_FINISHED is converted to an event."""
    connection.callback(CallbackID.MORSE_CODE_FINISHED)
    assert summary(read_events(device)) == [(1, CallbackID.MORSE_CODE_FINISHED, None)]
