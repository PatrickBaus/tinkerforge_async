"""Tests for the Analog In Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_analog_in import BrickletAnalogIn
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, read_events, request, run, summary

DEVICE = BrickletAnalogIn
FunctionID = BrickletAnalogIn.FunctionID
CallbackID = BrickletAnalogIn.CallbackID
Range = BrickletAnalogIn.Range

CALLS = [
    Call("get_voltage", FunctionID.GET_VOLTAGE, reply=("H", (12345,)), result=Decimal("12.345")),
    Call("get_value", FunctionID.GET_VOLTAGE, (0,), reply=("H", (1000,)), result=Decimal(1)),
    Call("get_analog_value", FunctionID.GET_ANALOG_VALUE, reply=("H", (4095,)), result=4095),
    Call("get_value", FunctionID.GET_ANALOG_VALUE, (1,), reply=("H", (1,)), result=1),
    Call("set_voltage_callback_period", FunctionID.SET_VOLTAGE_CALLBACK_PERIOD, sent=("I", (0,))),
    Call(
        "set_voltage_callback_period",
        FunctionID.SET_VOLTAGE_CALLBACK_PERIOD,
        (Decimal("0.5"), False),
        sent=("I", (500,)),
        response_expected=False,
    ),
    Call(
        "get_voltage_callback_period",
        FunctionID.GET_VOLTAGE_CALLBACK_PERIOD,
        reply=("I", (500,)),
        result=Decimal("0.5"),
    ),
    Call("set_analog_value_callback_period", FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD, (2,), sent=("I", (2000,))),
    Call(
        "get_analog_value_callback_period",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_PERIOD,
        reply=("I", (2000,)),
        result=Decimal(2),
    ),
    Call("set_voltage_callback_threshold", FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD, sent=("c H H", (b"x", 0, 0))),
    Call(
        "set_voltage_callback_threshold",
        FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
        ("o", Decimal("1.5"), 45),
        sent=("c H H", (b"o", 1500, 45000)),
    ),
    Call(
        "set_voltage_callback_threshold",
        FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
        (Threshold.GREATER_THAN, 0.29),
        sent=("c H H", (b">", 290, 0)),
    ),
    Call(
        "get_voltage_callback_threshold",
        FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD,
        reply=("c H H", ("o", 1500, 45000)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("1.5"), Decimal(45)),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        sent=("c H H", (b"x", 0, 0)),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        ("<", 100, 4000),
        sent=("c H H", (b"<", 100, 4000)),
    ),
    Call(
        "set_analog_value_callback_threshold",
        FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        (Threshold.INSIDE, 1, 2),
        sent=("c H H", (b"i", 1, 2)),
    ),
    Call(
        "get_analog_value_callback_threshold",
        FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD,
        reply=("c H H", ("<", 100, 4000)),
        result=BasicCallbackConfiguration(Threshold.LESS_THAN, 100, 4000),  # type: ignore[arg-type]  # The raw values are not converted
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
    Call("set_range", FunctionID.SET_RANGE, sent=("B", (0,))),
    Call("set_range", FunctionID.SET_RANGE, (Range.UP_TO_3V,), sent=("B", (5,))),
    Call("set_range", FunctionID.SET_RANGE, (2,), sent=("B", (2,))),
    Call("get_range", FunctionID.GET_RANGE, reply=("B", (4,)), result=Range.UP_TO_45V),
    Call("set_averaging", FunctionID.SET_AVERAGING, sent=("B", (50,))),
    Call("set_averaging", FunctionID.SET_AVERAGING, (0,), sent=("B", (0,))),
    Call("get_averaging", FunctionID.GET_AVERAGING, reply=("B", (50,)), result=50),
]

REJECTED = [
    ("set_voltage_callback_period", (-1,)),
    ("set_analog_value_callback_period", (-1,)),
    ("set_voltage_callback_threshold", ("?",)),
    ("set_analog_value_callback_threshold", ("?",)),
    ("set_debounce_period", (-1,)),
    ("set_range", (6,)),
    ("set_averaging", (-1,)),
    # There are the sids 0 and 1
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(bricklet: BrickletAnalogIn) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 219
    assert bricklet.get_api_version() == (2, 0, 3)
    assert str(bricklet).startswith("Analog In Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_set_callback_configuration(bricklet: BrickletAnalogIn, connection: FakeConnection) -> None:
    """The period and the threshold are set by two requests."""
    run(bricklet.set_callback_configuration(0, 1, False, Threshold.GREATER_THAN, 5))
    run(bricklet.set_callback_configuration(1, Decimal("0.1"), maximum=7, response_expected=False))
    assert connection.requests == [
        request(FunctionID.SET_VOLTAGE_CALLBACK_PERIOD, "I", 1000),
        request(FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD, "c H H", b">", 5000, 0),
        request(FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD, "I", 100, response_expected=False),
        request(FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD, "c H H", b"x", 0, 7, response_expected=False),
    ]


def test_get_callback_configuration(bricklet: BrickletAnalogIn, connection: FakeConnection) -> None:
    """The period and the threshold are merged."""
    connection.reply(FunctionID.GET_VOLTAGE_CALLBACK_PERIOD, "I", 250)
    connection.reply(FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD, "c H H", "i", 100, 200)
    connection.reply(FunctionID.GET_ANALOG_VALUE_CALLBACK_PERIOD, "I", 0)
    connection.reply(FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD, "c H H", "x", 0, 0)
    assert run(bricklet.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal("0.25"), True, Threshold.INSIDE, Decimal("0.1"), Decimal("0.2")
    )
    assert run(bricklet.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(0), True, Threshold.OFF, Decimal(0), Decimal(0)
    )


def test_events(bricklet: BrickletAnalogIn, connection: FakeConnection) -> None:
    """The voltage is sid 0 and converted to V, the analog value is sid 1."""
    connection.callback(CallbackID.VOLTAGE, "H", 455)
    connection.callback(CallbackID.ANALOG_VALUE, "H", 1234)
    connection.callback(CallbackID.VOLTAGE_REACHED, "H", 9000)
    connection.callback(CallbackID.ANALOG_VALUE_REACHED, "H", 4000)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.VOLTAGE, Decimal("0.455")),
        (1, CallbackID.ANALOG_VALUE, 1234),
        (0, CallbackID.VOLTAGE_REACHED, Decimal(9)),
        (1, CallbackID.ANALOG_VALUE_REACHED, 4000),
    ]
