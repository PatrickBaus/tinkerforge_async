"""Tests for the Ambient Light Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_ambient_light_v2 import BrickletAmbientLightV2, GetConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, read_events, request, run, summary

DEVICE = BrickletAmbientLightV2
FunctionID = BrickletAmbientLightV2.FunctionID
CallbackID = BrickletAmbientLightV2.CallbackID
IlluminanceRange = BrickletAmbientLightV2.IlluminanceRange
IntegrationTime = BrickletAmbientLightV2.IntegrationTime

CALLS = [
    Call("get_illuminance", FunctionID.GET_ILLUMINANCE, reply=("I", (123456,)), result=Decimal("1234.56")),
    Call("get_value", FunctionID.GET_ILLUMINANCE, (0,), reply=("I", (100,)), result=Decimal(1)),
    Call("set_illuminance_callback_period", FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD, sent=("I", (0,))),
    Call(
        "set_illuminance_callback_period",
        FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
        (Decimal("0.5"), False),
        sent=("I", (500,)),
        response_expected=False,
    ),
    Call(
        "get_illuminance_callback_period",
        FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD,
        reply=("I", (500,)),
        result=Decimal("0.5"),
    ),
    Call(
        "set_illuminance_callback_threshold",
        FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD,
        sent=("c I I", (b"x", 0, 0)),
    ),
    Call(
        "set_illuminance_callback_threshold",
        FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD,
        ("o", Decimal("0.5"), 64000),
        sent=("c I I", (b"o", 50, 6400000)),
    ),
    Call(
        "set_illuminance_callback_threshold",
        FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD,
        (Threshold.LESS_THAN, 10),
        sent=("c I I", (b"<", 1000, 0)),
    ),
    Call(
        "get_illuminance_callback_threshold",
        FunctionID.GET_ILLUMINANCE_CALLBACK_THRESHOLD,
        reply=("c I I", ("o", 50, 6400000)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.5"), Decimal(64000)),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (IlluminanceRange.RANGE_UNLIMITED, IntegrationTime.TIME_400MS),
        sent=("B B", (6, 7)),
    ),
    Call("set_configuration", FunctionID.SET_CONFIGURATION, (3, 3), sent=("B B", (3, 3))),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        reply=("B B", (3, 3)),
        result=GetConfiguration(IlluminanceRange.RANGE_8000LUX, IntegrationTime.TIME_200MS),
    ),
]

REJECTED = [
    ("set_illuminance_callback_period", (-1,)),
    ("set_illuminance_callback_threshold", ("?",)),
    ("set_illuminance_callback_threshold", ("x", -1)),
    ("set_illuminance_callback_threshold", ("x", 0, -1)),
    ("set_debounce_period", (-1,)),
    ("set_configuration", (7, 0)),
    ("set_configuration", (0, 8)),
    # There is only the sid 0
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(bricklet: BrickletAmbientLightV2) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 259
    assert bricklet.get_api_version() == (2, 0, 1)
    assert str(bricklet).startswith("Ambient Light Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_set_callback_configuration(bricklet: BrickletAmbientLightV2, connection: FakeConnection) -> None:
    """The period and the threshold are set by two requests."""
    run(bricklet.set_callback_configuration(0, 1, False, Threshold.GREATER_THAN, 50))
    assert connection.requests == [
        request(FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD, "I", 1000),
        request(FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD, "c I I", b">", 5000, 0),
    ]


def test_get_callback_configuration(bricklet: BrickletAmbientLightV2, connection: FakeConnection) -> None:
    """The period and the threshold are merged."""
    connection.reply(FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD, "I", 250)
    connection.reply(FunctionID.GET_ILLUMINANCE_CALLBACK_THRESHOLD, "c I I", "i", 100, 200)
    assert run(bricklet.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal("0.25"), True, Threshold.INSIDE, Decimal(1), Decimal(2)
    )


def test_events_are_converted_to_lux(bricklet: BrickletAmbientLightV2, connection: FakeConnection) -> None:
    """Both callbacks belong to sid 0."""
    connection.callback(CallbackID.ILLUMINANCE, "I", 455)
    connection.callback(CallbackID.ILLUMINANCE_REACHED, "I", 900)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.ILLUMINANCE, Decimal("4.55")),
        (0, CallbackID.ILLUMINANCE_REACHED, Decimal(9)),
    ]
