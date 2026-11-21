"""Tests for the Ambient Light Bricklet 3.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_ambient_light_v3 import BrickletAmbientLightV3, GetConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, run, summary

DEVICE = BrickletAmbientLightV3
FunctionID = BrickletAmbientLightV3.FunctionID
CallbackID = BrickletAmbientLightV3.CallbackID
IlluminanceRange = BrickletAmbientLightV3.IlluminanceRange
IntegrationTime = BrickletAmbientLightV3.IntegrationTime

CONFIGURATION = AdvancedCallbackConfiguration(Decimal("0.5"), True, Threshold.OUTSIDE, Decimal("0.5"), Decimal(64000))

CALLS = [
    Call("get_illuminance", FunctionID.GET_ILLUMINANCE, reply=("I", (123456,)), result=Decimal("1234.56")),
    Call("get_value", FunctionID.GET_ILLUMINANCE, (0,), reply=("I", (100,)), result=Decimal(1)),
    Call(
        "set_illuminance_callback_configuration",
        FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        sent=("I ! c I I", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_illuminance_callback_configuration",
        FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        (Decimal("0.5"), True, "o", Decimal("0.5"), 64000, False),
        sent=("I ! c I I", (500, True, b"o", 50, 6400000)),
        response_expected=False,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        (0, 1, False, Threshold.LESS_THAN, 10),
        sent=("I ! c I I", (1000, False, b"<", 1000, 0)),
    ),
    Call(
        "get_illuminance_callback_configuration",
        FunctionID.GET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        reply=("I ! c I I", (500, True, "o", 50, 6400000)),
        result=CONFIGURATION,
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ILLUMINANCE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c I I", (500, True, "o", 50, 6400000)),
        result=CONFIGURATION,
    ),
    Call("set_configuration", FunctionID.SET_CONFIGURATION, sent=("B B", (3, 2))),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (IlluminanceRange.UNLIMITED, IntegrationTime.T400MS),
        sent=("B B", (6, 7)),
    ),
    Call("set_configuration", FunctionID.SET_CONFIGURATION, (0, 0), sent=("B B", (0, 0))),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        reply=("B B", (3, 3)),
        result=GetConfiguration(IlluminanceRange.LUX8000, IntegrationTime.T200MS),
    ),
]

REJECTED = [
    ("set_illuminance_callback_configuration", (-1,)),
    ("set_illuminance_callback_configuration", (1, False, "?")),
    ("set_illuminance_callback_configuration", (1, False, "x", -1)),
    ("set_illuminance_callback_configuration", (1, False, "x", 0, -1)),
    ("set_configuration", (7, 0)),
    ("set_configuration", (0, 8)),
    # There is only the sid 0
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2131
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Ambient Light Bricklet 3.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_get_illuminance_prints_nothing(bricklet, connection, capsys):
    """The library must not write to stdout."""
    connection.reply(FunctionID.GET_ILLUMINANCE, "I", 1)
    assert run(bricklet.get_illuminance()) == Decimal("0.01")
    assert capsys.readouterr().out == ""


def test_events_are_converted_to_lux(bricklet, connection):
    """The callback belongs to sid 0."""
    connection.callback(CallbackID.ILLUMINANCE, "I", 455)
    assert summary(read_events(bricklet)) == [(0, CallbackID.ILLUMINANCE, Decimal("4.55"))]
