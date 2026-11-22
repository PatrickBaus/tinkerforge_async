"""Tests for the PTC Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

import pytest

from tinkerforge_async.bricklet_ptc import BrickletPtc
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, read_events, request, run, summary

DEVICE = BrickletPtc
FunctionID = BrickletPtc.FunctionID
CallbackID = BrickletPtc.CallbackID
LineFilter = BrickletPtc.LineFilter
WireMode = BrickletPtc.WireMode
SensorType = BrickletPtc.SensorType

CALLS = [
    Call("get_temperature", FunctionID.GET_TEMPERATURE, reply=("i", (2500,)), result=Decimal("298.15")),
    Call("get_value", FunctionID.GET_TEMPERATURE, (0,), reply=("i", (-4000,)), result=Decimal("233.15")),
    # The full scale of 32768 is 390 Ω for a Pt100
    Call("get_resistance", FunctionID.GET_RESISTANCE, reply=("i", (8192,)), result=Decimal("97.5")),
    Call("get_value", FunctionID.GET_RESISTANCE, (1,), reply=("i", (32768,)), result=Decimal(390)),
    Call("is_sensor_connected", FunctionID.IS_SENSOR_CONNECTED, reply=("!", (True,)), result=True),
    Call("get_value", FunctionID.IS_SENSOR_CONNECTED, (2,), reply=("!", (False,)), result=False),
    Call("set_temperature_callback_period", FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD, sent=("I", (0,))),
    Call(
        "set_temperature_callback_period",
        FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
        (Decimal("0.5"), False),
        sent=("I", (500,)),
        response_expected=False,
    ),
    Call(
        "get_temperature_callback_period",
        FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD,
        reply=("I", (500,)),
        result=Decimal("0.5"),
    ),
    Call("set_resistance_callback_period", FunctionID.SET_RESISTANCE_CALLBACK_PERIOD, (2,), sent=("I", (2000,))),
    Call(
        "get_resistance_callback_period",
        FunctionID.GET_RESISTANCE_CALLBACK_PERIOD,
        reply=("I", (2000,)),
        result=Decimal(2),
    ),
    # The default of the temperature thresholds is 0 °C
    Call(
        "set_temperature_callback_threshold",
        FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
        sent=("c i i", (b"x", 0, 0)),
    ),
    Call(
        "set_temperature_callback_threshold",
        FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
        ("o", Decimal("263.15"), 293.15),
        sent=("c i i", (b"o", -1000, 2000)),
    ),
    Call(
        "get_temperature_callback_threshold",
        FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD,
        reply=("c i i", ("o", -1000, 2000)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("263.15"), Decimal("293.15")),
    ),
    Call(
        "set_resistance_callback_threshold",
        FunctionID.SET_RESISTANCE_CALLBACK_THRESHOLD,
        sent=("c i i", (b"x", 0, 0)),
    ),
    Call(
        "set_resistance_callback_threshold",
        FunctionID.SET_RESISTANCE_CALLBACK_THRESHOLD,
        (">", Decimal("97.5"), 390),
        sent=("c i i", (b">", 8192, 32768)),
    ),
    Call(
        "get_resistance_callback_threshold",
        FunctionID.GET_RESISTANCE_CALLBACK_THRESHOLD,
        reply=("c i i", (">", 8192, 32768)),
        result=BasicCallbackConfiguration(Threshold.GREATER_THAN, Decimal("97.5"), Decimal(390)),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
    Call("set_noise_rejection_filter", FunctionID.SET_NOISE_REJECTION_FILTER, sent=("B", (0,))),
    Call("set_noise_rejection_filter", FunctionID.SET_NOISE_REJECTION_FILTER, (1,), sent=("B", (1,))),
    Call(
        "get_noise_rejection_filter",
        FunctionID.GET_NOISE_REJECTION_FILTER,
        reply=("B", (1,)),
        result=LineFilter.FREQUENCY_60HZ,
    ),
    Call("set_wire_mode", FunctionID.SET_WIRE_MODE, sent=("B", (2,))),
    Call("set_wire_mode", FunctionID.SET_WIRE_MODE, (WireMode.WIRE_4,), sent=("B", (4,))),
    Call("get_wire_mode", FunctionID.GET_WIRE_MODE, reply=("B", (3,)), result=WireMode.WIRE_3),
    Call(
        "set_sensor_connected_callback_configuration",
        FunctionID.SET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "get_sensor_connected_callback_configuration",
        FunctionID.GET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION,
        reply=("!", (True,)),
        result=True,
    ),
]

REJECTED = [
    ("set_temperature_callback_period", (-1,)),
    ("set_resistance_callback_period", (-1,)),
    ("set_temperature_callback_threshold", ("?",)),
    ("set_resistance_callback_threshold", ("?",)),
    ("set_debounce_period", (-1,)),
    ("set_noise_rejection_filter", (2,)),
    ("set_wire_mode", (1,)),
    # There are the sids 0 to 2, but the sid 2 has no callback configuration
    ("get_value", (3,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(bricklet: BrickletPtc) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 226
    assert bricklet.get_api_version() == (2, 0, 1)
    assert str(bricklet).startswith("PTC Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_sensor_type(bricklet: BrickletPtc, connection: FakeConnection) -> None:
    """The sensor type is a Pt100 by default. It can be set by its value and is part of the representation."""
    assert bricklet.sensor_type is SensorType.PT_100
    bricklet.sensor_type = 1
    assert bricklet.sensor_type is SensorType.PT_1000
    assert BrickletPtc(UID, connection.ipcon, SensorType.PT_1000).sensor_type is SensorType.PT_1000
    assert repr(bricklet).endswith("sensor_type=SensorType.PT_1000)")
    with pytest.raises(ValueError):
        bricklet.sensor_type = 2


def test_resistance_of_a_pt1000(connection: FakeConnection) -> None:
    """The full scale of 32768 is 3900 Ω for a Pt1000."""
    bricklet = BrickletPtc(UID, connection.ipcon, SensorType.PT_1000)
    connection.reply(FunctionID.GET_RESISTANCE, "i", 8192)
    connection.reply(FunctionID.GET_RESISTANCE_CALLBACK_THRESHOLD, "c i i", "<", 8192, 32768)
    connection.callback(CallbackID.RESISTANCE, "i", 16384)

    assert run(bricklet.get_resistance()) == Decimal(975)
    assert run(bricklet.get_resistance_callback_threshold()) == (Threshold.LESS_THAN, Decimal(975), Decimal(3900))
    run(bricklet.set_resistance_callback_threshold(Threshold.LESS_THAN, Decimal(975), 3900.0))
    assert connection.requests[-1] == request(FunctionID.SET_RESISTANCE_CALLBACK_THRESHOLD, "c i i", b"<", 8192, 32768)
    assert summary(read_events(bricklet)) == [(1, CallbackID.RESISTANCE, Decimal(1950))]


def test_set_callback_configuration(bricklet: BrickletPtc, connection: FakeConnection) -> None:
    """The period and the threshold are set by two requests. The default of the temperature thresholds is 0 °C."""
    run(bricklet.set_callback_configuration(0, 1, False, Threshold.GREATER_THAN, Decimal("283.15")))
    run(bricklet.set_callback_configuration(1, Decimal("0.1"), maximum=390, response_expected=False))
    assert connection.requests == [
        request(FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD, "I", 1000),
        request(FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD, "c i i", b">", 1000, 0),
        request(FunctionID.SET_RESISTANCE_CALLBACK_PERIOD, "I", 100, response_expected=False),
        request(FunctionID.SET_RESISTANCE_CALLBACK_THRESHOLD, "c i i", b"x", 0, 32768, response_expected=False),
    ]


def test_get_callback_configuration(bricklet: BrickletPtc, connection: FakeConnection) -> None:
    """The period and the threshold are merged."""
    connection.reply(FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD, "I", 250)
    connection.reply(FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD, "c i i", "i", 100, 200)
    connection.reply(FunctionID.GET_RESISTANCE_CALLBACK_PERIOD, "I", 0)
    connection.reply(FunctionID.GET_RESISTANCE_CALLBACK_THRESHOLD, "c i i", "x", 0, 32768)
    assert run(bricklet.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal("0.25"), True, Threshold.INSIDE, Decimal("274.15"), Decimal("275.15")
    )
    assert run(bricklet.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(0), True, Threshold.OFF, Decimal(0), Decimal(390)
    )


def test_events(bricklet: BrickletPtc, connection: FakeConnection) -> None:
    """The temperature is sid 0, the resistance sid 1 and the state of the sensor sid 2."""
    connection.callback(CallbackID.TEMPERATURE, "i", 2500)
    connection.callback(CallbackID.TEMPERATURE_REACHED, "i", -500)
    connection.callback(CallbackID.RESISTANCE, "i", 8192)
    connection.callback(CallbackID.RESISTANCE_REACHED, "i", 32768)
    connection.callback(CallbackID.SENSOR_CONNECTED, "!", True)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.TEMPERATURE, Decimal("298.15")),
        (0, CallbackID.TEMPERATURE_REACHED, Decimal("268.15")),
        (1, CallbackID.RESISTANCE, Decimal("97.5")),
        (1, CallbackID.RESISTANCE_REACHED, Decimal(390)),
        (2, CallbackID.SENSOR_CONNECTED, True),
    ]
