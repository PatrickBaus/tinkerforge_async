"""Tests for the Temperature Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_temperature import BrickletTemperature
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, request, run, summary

DEVICE = BrickletTemperature
FunctionID = BrickletTemperature.FunctionID
CallbackID = BrickletTemperature.CallbackID
I2cOption = BrickletTemperature.I2cOption

CALLS = [
    Call("get_temperature", FunctionID.GET_TEMPERATURE, reply=("h", (2500,)), result=Decimal("298.15")),
    Call("get_value", FunctionID.GET_TEMPERATURE, (0,), reply=("h", (-4000,)), result=Decimal("233.15")),
    Call(
        "set_temperature_callback_period",
        FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("1.5"),),
        sent=("I", (1500,)),
    ),
    Call(
        "set_temperature_callback_period",
        FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
        (0.29, False),
        sent=("I", (290,)),
        response_expected=False,
    ),
    Call(
        "get_temperature_callback_period",
        FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD,
        reply=("I", (1500,)),
        result=Decimal("1.5"),
    ),
    Call(
        "set_temperature_callback_threshold",
        FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
        sent=("c h h", (b"x", 0, 0)),
    ),
    Call(
        "set_temperature_callback_threshold",
        FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
        (">", Decimal("293.15"), Decimal("303.15")),
        sent=("c h h", (b">", 2000, 3000)),
    ),
    Call(
        "get_temperature_callback_threshold",
        FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD,
        reply=("c h h", ("o", -1000, 2000)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("263.15"), Decimal("293.15")),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (2,), sent=("I", (2000,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
    Call("set_i2c_mode", FunctionID.SET_I2C_MODE, sent=("B", (0,))),
    Call("set_i2c_mode", FunctionID.SET_I2C_MODE, (1,), sent=("B", (1,))),
    Call("get_i2c_mode", FunctionID.GET_I2C_MODE, reply=("B", (1,)), result=I2cOption.SLOW),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 216
    assert bricklet.get_api_version() == (2, 0, 1)
    assert str(bricklet).startswith("Temperature Bricklet with uid 12345")


REJECTED = [
    ("set_temperature_callback_period", (-1,)),
    ("set_debounce_period", (-1,)),
    ("set_temperature_callback_threshold", ("?",)),
    ("set_i2c_mode", (2,)),
    # There is only the sid 0
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_set_callback_configuration(bricklet, connection):
    """The period and the threshold are set by two requests. The default of the thresholds is 0 °C."""
    run(bricklet.set_callback_configuration(0, period=1, option=Threshold.LESS_THAN, minimum=Decimal("283.15")))
    assert connection.requests == [
        request(FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD, "I", 1000),
        request(FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD, "c h h", b"<", 1000, 0),
    ]


def test_get_callback_configuration(bricklet, connection):
    """The period and the threshold are merged."""
    connection.reply(FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD, "I", 250)
    connection.reply(FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD, "c h h", "i", 100, 200)
    assert run(bricklet.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal("0.25"), True, Threshold.INSIDE, Decimal("274.15"), Decimal("275.15")
    )


def test_events_are_converted_to_kelvin(bricklet, connection):
    """Both callbacks belong to sid 0."""
    connection.callback(CallbackID.TEMPERATURE, "h", 2500)
    connection.callback(CallbackID.TEMPERATURE_REACHED, "h", -500)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.TEMPERATURE, Decimal("298.15")),
        (0, CallbackID.TEMPERATURE_REACHED, Decimal("268.15")),
    ]
