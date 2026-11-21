"""Tests for the Temperature Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, summary

DEVICE = BrickletTemperatureV2
FunctionID = BrickletTemperatureV2.FunctionID
CallbackID = BrickletTemperatureV2.CallbackID
HeaterConfig = BrickletTemperatureV2.HeaterConfig

CONFIGURATION = AdvancedCallbackConfiguration(
    Decimal("0.25"), True, Threshold.INSIDE, Decimal("274.15"), Decimal("275.15")
)

CALLS = [
    Call("get_temperature", FunctionID.GET_TEMPERATURE, reply=("h", (2500,)), result=Decimal("298.15")),
    Call("get_value", FunctionID.GET_TEMPERATURE, (0,), reply=("h", (-4000,)), result=Decimal("233.15")),
    # The default of the thresholds is 0 °C
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        sent=("I ! c h h", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.25"), True, "i", Decimal("274.15"), 275.15, False),
        sent=("I ! c h h", (250, True, b"i", 100, 200)),
        response_expected=False,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (0, 1, True, Threshold.GREATER_THAN, Decimal("283.15")),
        sent=("I ! c h h", (1000, True, b">", 1000, 0)),
    ),
    Call(
        "get_temperature_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        reply=("I ! c h h", (250, True, "i", 100, 200)),
        result=CONFIGURATION,
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c h h", (250, True, "i", 100, 200)),
        result=CONFIGURATION,
    ),
    Call("set_heater_configuration", FunctionID.SET_HEATER_CONFIGURATION, sent=("B", (0,))),
    Call("set_heater_configuration", FunctionID.SET_HEATER_CONFIGURATION, (HeaterConfig.ENABLED,), sent=("B", (1,))),
    Call("set_heater_configuration", FunctionID.SET_HEATER_CONFIGURATION, (1,), sent=("B", (1,))),
    Call(
        "get_heater_configuration", FunctionID.GET_HEATER_CONFIGURATION, reply=("B", (1,)), result=HeaterConfig.ENABLED
    ),
]

REJECTED = [
    ("set_temperature_callback_configuration", (-1,)),
    ("set_temperature_callback_configuration", (1, False, "?")),
    ("set_heater_configuration", (2,)),
    # There is only the sid 0
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2113
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Temperature Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events_are_converted_to_kelvin(bricklet, connection):
    """The callback belongs to sid 0."""
    connection.callback(CallbackID.TEMPERATURE, "h", 2500)
    assert summary(read_events(bricklet)) == [(0, CallbackID.TEMPERATURE, Decimal("298.15"))]
