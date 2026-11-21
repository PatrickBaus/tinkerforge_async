"""Tests for the Moisture Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_moisture import BrickletMoisture
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, request, run, summary

DEVICE = BrickletMoisture
FunctionID = BrickletMoisture.FunctionID
CallbackID = BrickletMoisture.CallbackID

CALLS = [
    Call("get_moisture_value", FunctionID.GET_MOISTURE, reply=("H", (4095,)), result=4095),
    Call("get_value", FunctionID.GET_MOISTURE, (0,), reply=("H", (1,)), result=1),
    Call("set_moisture_callback_period", FunctionID.SET_MOISTURE_CALLBACK_PERIOD, sent=("I", (0,))),
    Call(
        "set_moisture_callback_period",
        FunctionID.SET_MOISTURE_CALLBACK_PERIOD,
        (Decimal("0.5"), False),
        sent=("I", (500,)),
        response_expected=False,
    ),
    Call(
        "get_moisture_callback_period",
        FunctionID.GET_MOISTURE_CALLBACK_PERIOD,
        reply=("I", (500,)),
        result=Decimal("0.5"),
    ),
    Call("set_moisture_callback_threshold", FunctionID.SET_MOISTURE_CALLBACK_THRESHOLD, sent=("c H H", (b"x", 0, 0))),
    Call(
        "set_moisture_callback_threshold",
        FunctionID.SET_MOISTURE_CALLBACK_THRESHOLD,
        ("i", 100, 4000),
        sent=("c H H", (b"i", 100, 4000)),
    ),
    Call(
        "get_moisture_callback_threshold",
        FunctionID.GET_MOISTURE_CALLBACK_THRESHOLD,
        reply=("c H H", ("i", 100, 4000)),
        result=BasicCallbackConfiguration(Threshold.INSIDE, 100, 4000),  # type: ignore[arg-type]  # The raw values are not converted
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (1,), sent=("I", (1000,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, sent=("B", (100,))),
    Call("set_moving_average", FunctionID.SET_MOVING_AVERAGE, (0,), sent=("B", (0,))),
    Call("get_moving_average", FunctionID.GET_MOVING_AVERAGE, reply=("B", (100,)), result=100),
]

REJECTED = [
    ("set_moisture_callback_period", (-1,)),
    ("set_moisture_callback_threshold", ("?",)),
    ("set_moisture_callback_threshold", ("x", -1)),
    ("set_moisture_callback_threshold", ("x", 0, -1)),
    ("set_debounce_period", (-1,)),
    ("set_moving_average", (-1,)),
    # There is only the sid 0
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 232
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Moisture Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_set_callback_configuration(bricklet, connection):
    """The period and the threshold are set by two requests."""
    run(bricklet.set_callback_configuration(0, 1, False, Threshold.GREATER_THAN, 50))
    assert connection.requests == [
        request(FunctionID.SET_MOISTURE_CALLBACK_PERIOD, "I", 1000),
        request(FunctionID.SET_MOISTURE_CALLBACK_THRESHOLD, "c H H", b">", 50, 0),
    ]


def test_get_callback_configuration(bricklet, connection):
    """The period and the threshold are merged."""
    connection.reply(FunctionID.GET_MOISTURE_CALLBACK_PERIOD, "I", 250)
    connection.reply(FunctionID.GET_MOISTURE_CALLBACK_THRESHOLD, "c H H", "i", 100, 200)
    assert run(bricklet.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal("0.25"), True, Threshold.INSIDE, Decimal(100), Decimal(200)
    )


def test_events(bricklet, connection):
    """Both callbacks belong to sid 0."""
    connection.callback(CallbackID.MOISTURE, "H", 455)
    connection.callback(CallbackID.MOISTURE_REACHED, "H", 900)
    assert summary(read_events(bricklet)) == [(0, CallbackID.MOISTURE, 455), (0, CallbackID.MOISTURE_REACHED, 900)]
