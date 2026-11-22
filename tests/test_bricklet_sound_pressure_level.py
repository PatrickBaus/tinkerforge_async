"""Tests for the Sound Pressure Level Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_sound_pressure_level import BrickletSoundPressureLevel, GetConfiguration, GetSpectrum
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletSoundPressureLevel
FunctionID = BrickletSoundPressureLevel.FunctionID
CallbackID = BrickletSoundPressureLevel.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_DECIBEL": 1,
    "SET_DECIBEL_CALLBACK_CONFIGURATION": 2,
    "GET_DECIBEL_CALLBACK_CONFIGURATION": 3,
    "GET_SPECTRUM_LOW_LEVEL": 5,
    "SET_SPECTRUM_CALLBACK_CONFIGURATION": 6,
    "GET_SPECTRUM_CALLBACK_CONFIGURATION": 7,
    "SET_CONFIGURATION": 9,
    "GET_CONFIGURATION": 10,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"DECIBEL": 4, "SPECTRUM_LOW_LEVEL": 8}

CALLS: list[Call] = [
    Call("get_decibel", FunctionID.GET_DECIBEL, (), reply=("H", (3,)), result=Decimal("0.3")),
    Call(
        "set_decibel_callback_configuration",
        FunctionID.SET_DECIBEL_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("0.3")),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_decibel_callback_configuration",
        FunctionID.SET_DECIBEL_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("0.3"), False),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_decibel_callback_configuration",
        FunctionID.GET_DECIBEL_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c H H", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.6"), Decimal("0.7")),
    ),
    Call(
        "get_spectrum_low_level",
        FunctionID.GET_SPECTRUM_LOW_LEVEL,
        (),
        reply=("H H 30H", (64, 4, [5] * 30)),
        result=GetSpectrum(64, 4, (5,) * 30),
    ),
    Call(
        "set_spectrum_callback_configuration",
        FunctionID.SET_SPECTRUM_CALLBACK_CONFIGURATION,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_spectrum_callback_configuration",
        FunctionID.SET_SPECTRUM_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_spectrum_callback_configuration",
        FunctionID.GET_SPECTRUM_CALLBACK_CONFIGURATION,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.FFTSize.FFT_SIZE_1024, DEVICE.Weighting.ITU_R_468),
        sent=("B B", (3, 5)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.FFTSize.FFT_SIZE_1024, DEVICE.Weighting.ITU_R_468, False),
        sent=("B B", (3, 5)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B B", (3, 5)),
        result=GetConfiguration(DEVICE.FFTSize.FFT_SIZE_1024, DEVICE.Weighting.ITU_R_468),
    ),
    Call("get_value", FunctionID.GET_DECIBEL, (0,), reply=("H", (3,)), result=Decimal("0.3")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_DECIBEL_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.4")),
        sent=("I ! c H H", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_DECIBEL_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c H H", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_decibel_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.3"), Decimal("0.3"))),
    ("set_decibel_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.3"), Decimal("0.3"))),
    ("set_decibel_callback_configuration", (Decimal("0.003"), True, "o", Decimal("6553.6"), Decimal("0.3"))),
    ("set_decibel_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("6553.6"))),
    ("set_spectrum_callback_configuration", (Decimal("4294967.296"),)),
    ("set_configuration", (12345, DEVICE.Weighting.ITU_R_468)),
    ("set_configuration", (DEVICE.FFTSize.FFT_SIZE_1024, 12345)),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 290
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Sound Pressure Level Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_get_spectrum_transfers_the_stream(device, connection):
    """The high-level function get_spectrum() uses get_spectrum_low_level()."""
    data = [3] * 3
    for offset in range(0, 1, 30):
        connection.reply(FunctionID.GET_SPECTRUM_LOW_LEVEL, "H H 30H", *(3, offset, chunk(data, offset, 30, 0)))
    result = run(device.get_spectrum())
    assert connection.requests == [request(FunctionID.GET_SPECTRUM_LOW_LEVEL)] * 1
    assert result == (3,) * 3


def test_callback_decibel(device, connection):
    """The callback DECIBEL is converted to an event."""
    connection.callback(CallbackID.DECIBEL, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.DECIBEL, Decimal("0.3"))]


def test_callback_spectrum(device, connection):
    """The callback SPECTRUM is converted to an event."""
    data = [3] * 3
    for offset in range(0, 1, 30):
        connection.callback(CallbackID.SPECTRUM, "H H 30H", *(3, offset, chunk(data, offset, 30, 0)))
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [(1, CallbackID.SPECTRUM)]
    assert events[0].payload == (3,) * 3
    connection_2 = FakeConnection()
    connection_2.callback(CallbackID.SPECTRUM, "H H 30H", *(33, 30, chunk(data, 0, 30, 0)))
    assert not read_events(DEVICE(UID, connection_2))
