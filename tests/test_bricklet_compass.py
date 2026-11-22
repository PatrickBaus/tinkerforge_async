"""Tests for the Compass Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_compass import BrickletCompass, GetCalibration, GetConfiguration, GetMagneticFluxDensity
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletCompass
FunctionID = BrickletCompass.FunctionID
CallbackID = BrickletCompass.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_HEADING": 1,
    "SET_HEADING_CALLBACK_CONFIGURATION": 2,
    "GET_HEADING_CALLBACK_CONFIGURATION": 3,
    "GET_MAGNETIC_FLUX_DENSITY": 5,
    "SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION": 6,
    "GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION": 7,
    "SET_CONFIGURATION": 9,
    "GET_CONFIGURATION": 10,
    "SET_CALIBRATION": 11,
    "GET_CALIBRATION": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"HEADING": 4, "MAGNETIC_FLUX_DENSITY": 8}

CALLS: list[Call] = [
    Call("get_heading", FunctionID.GET_HEADING, (), reply=("h", (3,)), result=Decimal("0.3")),
    Call(
        "set_heading_callback_configuration",
        FunctionID.SET_HEADING_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("0.3")),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_heading_callback_configuration",
        FunctionID.SET_HEADING_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("0.3"), False),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_heading_callback_configuration",
        FunctionID.GET_HEADING_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c h h", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.6"), Decimal("0.7")),
    ),
    Call(
        "get_magnetic_flux_density",
        FunctionID.GET_MAGNETIC_FLUX_DENSITY,
        (),
        reply=("i i i", (3, 4, 5)),
        result=GetMagneticFluxDensity(Decimal("3E-8"), Decimal("4E-8"), Decimal("5E-8")),
    ),
    Call(
        "set_magnetic_flux_density_callback_configuration",
        FunctionID.SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_magnetic_flux_density_callback_configuration",
        FunctionID.SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_magnetic_flux_density_callback_configuration",
        FunctionID.GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.DataRate.DATA_RATE_600HZ, True),
        sent=("B !", (3, True)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (DEVICE.DataRate.DATA_RATE_600HZ, True, False),
        sent=("B !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (),
        reply=("B !", (3, True)),
        result=GetConfiguration(DEVICE.DataRate.DATA_RATE_600HZ, True),
    ),
    Call("set_calibration", FunctionID.SET_CALIBRATION, ([3] * 3, [3] * 3), sent=("3h 3h", ([3] * 3, [3] * 3))),
    Call(
        "set_calibration",
        FunctionID.SET_CALIBRATION,
        ([3] * 3, [3] * 3, False),
        sent=("3h 3h", ([3] * 3, [3] * 3)),
        response_expected=False,
    ),
    Call(
        "get_calibration",
        FunctionID.GET_CALIBRATION,
        (),
        reply=("3h 3h", ([3] * 3, [4] * 3)),
        result=GetCalibration((3,) * 3, (4,) * 3),
    ),
    Call("get_value", FunctionID.GET_HEADING, (0,), reply=("h", (3,)), result=Decimal("0.3")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_HEADING_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.4")),
        sent=("I ! c h h", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_HEADING_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c h h", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.3"), Decimal("0.4")),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_heading_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.3"), Decimal("0.3"))),
    ("set_heading_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.3"), Decimal("0.3"))),
    ("set_heading_callback_configuration", (Decimal("0.003"), True, "o", Decimal("3276.8"), Decimal("0.3"))),
    ("set_heading_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.3"), Decimal("3276.8"))),
    ("set_magnetic_flux_density_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_configuration", (12345, True)),
    ("set_calibration", (([3] * 3)[:-1], [3] * 3)),
    ("set_calibration", ([3] * 3, ([3] * 3)[:-1])),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2153
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Compass Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_heading(device, connection):
    """The callback HEADING is converted to an event."""
    connection.callback(CallbackID.HEADING, "h", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.HEADING, Decimal("0.3"))]


def test_callback_magnetic_flux_density(device, connection):
    """The callback MAGNETIC_FLUX_DENSITY is converted to an event."""
    connection.callback(CallbackID.MAGNETIC_FLUX_DENSITY, "i i i", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (1, CallbackID.MAGNETIC_FLUX_DENSITY, GetMagneticFluxDensity(Decimal("3E-8"), Decimal("4E-8"), Decimal("5E-8")))
    ]
