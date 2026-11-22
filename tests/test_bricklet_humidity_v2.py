"""Tests for the Humidity Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_humidity_v2 import BrickletHumidityV2, GetMovingAverageConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, read_events, summary

DEVICE = BrickletHumidityV2
FunctionID = BrickletHumidityV2.FunctionID
CallbackID = BrickletHumidityV2.CallbackID
HeaterConfig = BrickletHumidityV2.HeaterConfig
SamplesPerSecond = BrickletHumidityV2.SamplesPerSecond

CALLS = [
    Call("get_humidity", FunctionID.GET_HUMIDITY, reply=("H", (4550,)), result=Decimal("45.5")),
    Call("get_value", FunctionID.GET_HUMIDITY, (0,), reply=("H", (10000,)), result=Decimal("100")),
    Call("get_temperature", FunctionID.GET_TEMPERATURE, reply=("h", (2500,)), result=Decimal("298.15")),
    Call("get_value", FunctionID.GET_TEMPERATURE, (1,), reply=("h", (-4000,)), result=Decimal("233.15")),
    Call(
        "set_humidity_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        sent=("I ! c H H", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_humidity_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        (Decimal("0.5"), True, "o", Decimal("20.5"), 80, False),
        sent=("I ! c H H", (500, True, b"o", 2050, 8000)),
        response_expected=False,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        (0, 1, False, Threshold.LESS_THAN, 30),
        sent=("I ! c H H", (1000, False, b"<", 3000, 0)),
    ),
    Call(
        "get_humidity_callback_configuration",
        FunctionID.GET_HUMIDITY_CALLBACK_CONFIGURATION,
        reply=("I ! c H H", (500, True, "o", 2050, 8000)),
        result=AdvancedCallbackConfiguration(Decimal("0.5"), True, Threshold.OUTSIDE, Decimal("20.5"), Decimal(80)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_HUMIDITY_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c H H", (0, False, "x", 0, 0)),
        result=AdvancedCallbackConfiguration(Decimal(0), False, Threshold.OFF, Decimal(0), Decimal(0)),
    ),
    # The default of the temperature thresholds is 0 °C
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        sent=("I ! c h h", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.25"), True, "i", Decimal("274.15"), 275.15),
        sent=("I ! c h h", (250, True, b"i", 100, 200)),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (1, 1, False, Threshold.GREATER_THAN, Decimal("283.15")),
        sent=("I ! c h h", (1000, False, b">", 1000, 0)),
    ),
    Call(
        "get_temperature_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        reply=("I ! c h h", (250, True, "i", -100, 200)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.25"), True, Threshold.INSIDE, Decimal("272.15"), Decimal("275.15")
        ),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c h h", (0, False, "x", 0, 0)),
        result=AdvancedCallbackConfiguration(Decimal(0), False, Threshold.OFF, Decimal("273.15"), Decimal("273.15")),
    ),
    Call("set_heater_configuration", FunctionID.SET_HEATER_CONFIGURATION, sent=("B", (0,))),
    Call("set_heater_configuration", FunctionID.SET_HEATER_CONFIGURATION, (HeaterConfig.ENABLED,), sent=("B", (1,))),
    Call("set_heater_configuration", FunctionID.SET_HEATER_CONFIGURATION, (1,), sent=("B", (1,))),
    Call(
        "get_heater_configuration", FunctionID.GET_HEATER_CONFIGURATION, reply=("B", (1,)), result=HeaterConfig.ENABLED
    ),
    Call("set_moving_average_configuration", FunctionID.SET_MOVING_AVERAGE_CONFIGURATION, sent=("H H", (5, 5))),
    Call(
        "set_moving_average_configuration",
        FunctionID.SET_MOVING_AVERAGE_CONFIGURATION,
        (1, 1000),
        sent=("H H", (1, 1000)),
    ),
    Call(
        "get_moving_average_configuration",
        FunctionID.GET_MOVING_AVERAGE_CONFIGURATION,
        reply=("H H", (5, 10)),
        result=GetMovingAverageConfiguration(5, 10),
    ),
    Call("set_samples_per_second", FunctionID.SET_SAMPLES_PER_SECOND, sent=("B", (3,))),
    Call("set_samples_per_second", FunctionID.SET_SAMPLES_PER_SECOND, (SamplesPerSecond.SPS_20,), sent=("B", (0,))),
    Call("set_samples_per_second", FunctionID.SET_SAMPLES_PER_SECOND, (5,), sent=("B", (5,))),
    Call(
        "get_samples_per_second", FunctionID.GET_SAMPLES_PER_SECOND, reply=("B", (4,)), result=SamplesPerSecond.SPS_02
    ),
]

REJECTED = [
    ("set_humidity_callback_configuration", (-1,)),
    ("set_humidity_callback_configuration", (1, False, "?")),
    ("set_humidity_callback_configuration", (1, False, "x", -1)),
    ("set_humidity_callback_configuration", (1, False, "x", 0, -1)),
    ("set_temperature_callback_configuration", (-1,)),
    ("set_temperature_callback_configuration", (1, False, "?")),
    ("set_heater_configuration", (2,)),
    ("set_moving_average_configuration", (0, 1)),
    ("set_moving_average_configuration", (1, 0)),
    ("set_samples_per_second", (6,)),
    # There are the sids 0 and 1
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(bricklet: BrickletHumidityV2) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 283
    assert bricklet.get_api_version() == (2, 0, 2)
    assert str(bricklet).startswith("Humidity Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet: BrickletHumidityV2, connection: FakeConnection) -> None:
    """The humidity is sid 0 and converted to %RH, the temperature is sid 1 and converted to K."""
    connection.callback(CallbackID.HUMIDITY, "H", 4550)
    connection.callback(CallbackID.TEMPERATURE, "h", -500)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.HUMIDITY, Decimal("45.5")),
        (1, CallbackID.TEMPERATURE, Decimal("268.15")),
    ]
