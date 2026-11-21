"""Tests for the Humidity Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_humidity import BrickletHumidity
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, request, run, summary

DEVICE = BrickletHumidity
FunctionID = BrickletHumidity.FunctionID
CallbackID = BrickletHumidity.CallbackID

CALLS = [
    Call("get_humidity", FunctionID.GET_HUMIDITY, reply=("H", (455,)), result=Decimal("45.5")),
    Call("get_value", FunctionID.GET_HUMIDITY, (0,), reply=("H", (1000,)), result=Decimal("100")),
    Call("get_analog_value", FunctionID.GET_ANALOG_VALUE, reply=("H", (4095,)), result=4095),
    Call("get_value", FunctionID.GET_ANALOG_VALUE, (1,), reply=("H", (1,)), result=1),
    Call("set_humidity_callback_period", FunctionID.SET_HUMIDITY_CALLBACK_PERIOD, sent=("I", (0,))),
    Call(
        "set_humidity_callback_period",
        FunctionID.SET_HUMIDITY_CALLBACK_PERIOD,
        (Decimal("0.5"), False),
        sent=("I", (500,)),
        response_expected=False,
    ),
    Call(
        "get_humidity_callback_period",
        FunctionID.GET_HUMIDITY_CALLBACK_PERIOD,
        reply=("I", (500,)),
        result=Decimal("0.5"),
    ),
    Call("set_analog_value_callback_period", FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD, (2,), sent=("I", (2000,))),
    Call(
        "get_analog_value_callback_period",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_PERIOD,
        reply=("I", (2000,)),
        result=Decimal("2"),
    ),
    Call("set_humidity_callback_threshold", FunctionID.SET_HUMIDITY_CALLBACK_THRESHOLD, sent=("c H H", (b"x", 0, 0))),
    Call(
        "set_humidity_callback_threshold",
        FunctionID.SET_HUMIDITY_CALLBACK_THRESHOLD,
        ("o", Decimal("20.5"), 80),
        sent=("c H H", (b"o", 205, 800)),
    ),
    # The thresholds are unsigned. 6000 does not fit into a signed 16 bit integer.
    Call(
        "get_humidity_callback_threshold",
        FunctionID.GET_HUMIDITY_CALLBACK_THRESHOLD,
        reply=("c H H", ("o", 205, 60000)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("20.5"), Decimal("6000")),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        sent=("c H H", (b"x", 0, 0)),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        (Threshold.LESS_THAN, 100, 4000),
        sent=("c H H", (b"<", 100, 4000)),
    ),
    Call(
        "get_analog_value_callback_threshold",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        reply=("c H H", ("<", 100, 4000)),
        result=BasicCallbackConfiguration(Threshold.LESS_THAN, Decimal(100), Decimal(4000)),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
]

REJECTED = [
    ("set_humidity_callback_period", (-1,)),
    ("set_analog_value_callback_period", (-1,)),
    ("set_debounce_period", (-1,)),
    ("set_humidity_callback_threshold", ("?",)),
    ("set_analog_value_callback_threshold", ("?",)),
    # There are the sids 0 and 1
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 27
    assert bricklet.get_api_version() == (2, 0, 1)
    assert str(bricklet).startswith("Humidity Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_set_callback_configuration(bricklet, connection):
    """The period and the threshold are set by two requests."""
    run(bricklet.set_callback_configuration(0, 1, False, Threshold.GREATER_THAN, 50))
    run(bricklet.set_callback_configuration(1, Decimal("0.1"), maximum=7, response_expected=False))
    assert connection.requests == [
        request(FunctionID.SET_HUMIDITY_CALLBACK_PERIOD, "I", 1000),
        request(FunctionID.SET_HUMIDITY_CALLBACK_THRESHOLD, "c H H", b">", 500, 0),
        request(FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD, "I", 100, response_expected=False),
        request(FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD, "c H H", b"x", 0, 7, response_expected=False),
    ]


def test_get_callback_configuration(bricklet, connection):
    """The period and the threshold are merged."""
    connection.reply(FunctionID.GET_HUMIDITY_CALLBACK_PERIOD, "I", 250)
    connection.reply(FunctionID.GET_HUMIDITY_CALLBACK_THRESHOLD, "c H H", "i", 100, 200)
    connection.reply(FunctionID.GET_ANALOG_VALUE_CALLBACK_PERIOD, "I", 0)
    connection.reply(FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD, "c H H", "x", 0, 0)
    assert run(bricklet.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal("0.25"), True, Threshold.INSIDE, Decimal(10), Decimal(20)
    )
    assert run(bricklet.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(0), True, Threshold.OFF, Decimal(0), Decimal(0)
    )


def test_events(bricklet, connection):
    """The humidity is sid 0 and converted to %RH, the analog value is sid 1."""
    connection.callback(CallbackID.HUMIDITY, "H", 455)
    connection.callback(CallbackID.ANALOG_VALUE, "H", 1234)
    connection.callback(CallbackID.HUMIDITY_REACHED, "H", 900)
    connection.callback(CallbackID.ANALOG_VALUE_REACHED, "H", 4000)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.HUMIDITY, Decimal("45.5")),
        (1, CallbackID.ANALOG_VALUE, 1234),
        (0, CallbackID.HUMIDITY_REACHED, Decimal("90")),
        (1, CallbackID.ANALOG_VALUE_REACHED, 4000),
    ]
    assert summary(read_events(bricklet, sids=(1,))) == [
        (1, CallbackID.ANALOG_VALUE, 1234),
        (1, CallbackID.ANALOG_VALUE_REACHED, 4000),
    ]
