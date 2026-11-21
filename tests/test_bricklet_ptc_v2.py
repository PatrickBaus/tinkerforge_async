"""Tests for the PTC Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

import pytest

from tinkerforge_async.bricklet_ptc_v2 import BrickletPtcV2, GetMovingAverageConfiguration
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, read_events, request, run, summary

DEVICE = BrickletPtcV2
FunctionID = BrickletPtcV2.FunctionID
CallbackID = BrickletPtcV2.CallbackID
LineFilter = BrickletPtcV2.LineFilter
WireMode = BrickletPtcV2.WireMode
SensorType = BrickletPtcV2.SensorType

CALLS = [
    Call("get_temperature", FunctionID.GET_TEMPERATURE, reply=("i", (2500,)), result=Decimal("298.15")),
    Call("get_value", FunctionID.GET_TEMPERATURE, (0,), reply=("i", (-4000,)), result=Decimal("233.15")),
    # The full scale of 32768 is 390 Ω for a Pt100
    Call("get_resistance", FunctionID.GET_RESISTANCE, reply=("i", (8192,)), result=Decimal("97.5")),
    Call("get_value", FunctionID.GET_RESISTANCE, (1,), reply=("i", (32768,)), result=Decimal(390)),
    Call("is_sensor_connected", FunctionID.IS_SENSOR_CONNECTED, reply=("!", (True,)), result=True),
    Call("get_value", FunctionID.IS_SENSOR_CONNECTED, (2,), reply=("!", (False,)), result=False),
    # The default of the temperature thresholds is 0 °C
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        sent=("I ! c i i", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.25"), True, "i", Decimal("274.15"), 275.15, False),
        sent=("I ! c i i", (250, True, b"i", 100, 200)),
        response_expected=False,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (0, 1, False, Threshold.GREATER_THAN, Decimal("283.15")),
        sent=("I ! c i i", (1000, False, b">", 1000, 0)),
    ),
    Call(
        "get_temperature_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        reply=("I ! c i i", (250, True, "i", -100, 200)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.25"), True, Threshold.INSIDE, Decimal("272.15"), Decimal("275.15")
        ),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c i i", (0, False, "x", 0, 0)),
        result=AdvancedCallbackConfiguration(Decimal(0), False, Threshold.OFF, Decimal("273.15"), Decimal("273.15")),
    ),
    Call(
        "set_resistance_callback_configuration",
        FunctionID.SET_RESISTANCE_CALLBACK_CONFIGURATION,
        sent=("I ! c i i", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_resistance_callback_configuration",
        FunctionID.SET_RESISTANCE_CALLBACK_CONFIGURATION,
        (Decimal("0.5"), True, ">", Decimal("97.5"), 390),
        sent=("I ! c i i", (500, True, b">", 8192, 32768)),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_RESISTANCE_CALLBACK_CONFIGURATION,
        (1, 1, False, Threshold.LESS_THAN, 390),
        sent=("I ! c i i", (1000, False, b"<", 32768, 0)),
    ),
    Call(
        "get_resistance_callback_configuration",
        FunctionID.GET_RESISTANCE_CALLBACK_CONFIGURATION,
        reply=("I ! c i i", (500, True, ">", 8192, 32768)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.5"), True, Threshold.GREATER_THAN, Decimal("97.5"), Decimal(390)
        ),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_RESISTANCE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c i i", (0, False, "x", 0, 0)),
        result=AdvancedCallbackConfiguration(Decimal(0), False, Threshold.OFF, Decimal(0), Decimal(0)),
    ),
    Call("set_noise_rejection_filter", FunctionID.SET_NOISE_REJECTION_FILTER, sent=("B", (0,))),
    Call(
        "set_noise_rejection_filter",
        FunctionID.SET_NOISE_REJECTION_FILTER,
        (LineFilter.FREQUENCY_60HZ,),
        sent=("B", (1,)),
    ),
    Call("set_noise_rejection_filter", FunctionID.SET_NOISE_REJECTION_FILTER, (1,), sent=("B", (1,))),
    Call(
        "get_noise_rejection_filter",
        FunctionID.GET_NOISE_REJECTION_FILTER,
        reply=("B", (1,)),
        result=LineFilter.FREQUENCY_60HZ,
    ),
    Call("set_wire_mode", FunctionID.SET_WIRE_MODE, sent=("B", (2,))),
    Call("set_wire_mode", FunctionID.SET_WIRE_MODE, (WireMode.WIRE_4,), sent=("B", (4,))),
    Call("set_wire_mode", FunctionID.SET_WIRE_MODE, (3,), sent=("B", (3,))),
    Call("get_wire_mode", FunctionID.GET_WIRE_MODE, reply=("B", (3,)), result=WireMode.WIRE_3),
    Call("set_moving_average_configuration", FunctionID.SET_MOVING_AVERAGE_CONFIGURATION, sent=("H H", (1, 40))),
    Call(
        "set_moving_average_configuration",
        FunctionID.SET_MOVING_AVERAGE_CONFIGURATION,
        (1000, 1),
        sent=("H H", (1000, 1)),
    ),
    Call(
        "get_moving_average_configuration",
        FunctionID.GET_MOVING_AVERAGE_CONFIGURATION,
        reply=("H H", (1, 40)),
        result=GetMovingAverageConfiguration(1, 40),
    ),
    Call(
        "set_sensor_connected_callback_configuration",
        FunctionID.SET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION,
        sent=("!", (False,)),
    ),
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
    ("set_temperature_callback_configuration", (-1,)),
    ("set_temperature_callback_configuration", (1, False, "?")),
    ("set_resistance_callback_configuration", (-1,)),
    ("set_resistance_callback_configuration", (1, False, "?")),
    ("set_resistance_callback_configuration", (1, False, "x", -1)),
    ("set_resistance_callback_configuration", (1, False, "x", 0, -1)),
    ("set_noise_rejection_filter", (2,)),
    ("set_wire_mode", (1,)),
    ("set_moving_average_configuration", (0, 1)),
    ("set_moving_average_configuration", (1, 0)),
    # There are the sids 0 to 2, but the sid 2 has no callback configuration
    ("get_value", (3,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2101
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("PTC Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_sensor_type(bricklet, connection):
    """The sensor type is a Pt100 by default. It can be set by its value and is part of the representation."""
    assert bricklet.sensor_type is SensorType.PT_100
    bricklet.sensor_type = 1
    assert bricklet.sensor_type is SensorType.PT_1000
    assert BrickletPtcV2(UID, connection, SensorType.PT_1000).sensor_type is SensorType.PT_1000
    assert repr(bricklet).endswith("sensor_type=SensorType.PT_1000)")
    with pytest.raises(ValueError):
        bricklet.sensor_type = 2


def test_resistance_of_a_pt1000(connection):
    """The full scale of 32768 is 3900 Ω for a Pt1000."""
    bricklet = BrickletPtcV2(UID, connection, SensorType.PT_1000)
    connection.reply(FunctionID.GET_RESISTANCE, "i", 8192)
    connection.reply(FunctionID.GET_RESISTANCE_CALLBACK_CONFIGURATION, "I ! c i i", 0, False, "<", 8192, 32768)
    connection.callback(CallbackID.RESISTANCE, "i", 16384)

    assert run(bricklet.get_resistance()) == Decimal(975)
    assert run(bricklet.get_resistance_callback_configuration())[2:] == (
        Threshold.LESS_THAN,
        Decimal(975),
        Decimal(3900),
    )
    run(bricklet.set_resistance_callback_configuration(0, False, Threshold.LESS_THAN, Decimal(975), 3900.0))
    assert connection.requests[-1] == request(
        FunctionID.SET_RESISTANCE_CALLBACK_CONFIGURATION, "I ! c i i", 0, False, b"<", 8192, 32768
    )
    assert summary(read_events(bricklet)) == [(1, CallbackID.RESISTANCE, Decimal(1950))]


def test_events(bricklet, connection):
    """The temperature is sid 0, the resistance sid 1 and the state of the sensor sid 2."""
    connection.callback(CallbackID.TEMPERATURE, "i", 2500)
    connection.callback(CallbackID.RESISTANCE, "i", 8192)
    connection.callback(CallbackID.SENSOR_CONNECTED, "!", True)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.TEMPERATURE, Decimal("298.15")),
        (1, CallbackID.RESISTANCE, Decimal("97.5")),
        (2, CallbackID.SENSOR_CONNECTED, True),
    ]
