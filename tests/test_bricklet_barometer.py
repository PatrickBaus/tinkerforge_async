"""Tests for the Barometer Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_barometer import BrickletBarometer, GetAveraging
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, request, run, summary

DEVICE = BrickletBarometer
FunctionID = BrickletBarometer.FunctionID
I2CMode = BrickletBarometer.I2CMode
CallbackID = BrickletBarometer.CallbackID

CALLS = [
    # The air pressure is transferred in 1/1000 hPa, the altitude in cm
    Call("get_air_pressure", FunctionID.GET_AIR_PRESSURE, reply=("i", (1013250,)), result=Decimal(101325)),
    Call("get_value", FunctionID.GET_AIR_PRESSURE, (0,), reply=("i", (1,)), result=Decimal("0.1")),
    Call("get_altitude", FunctionID.GET_ALTITUDE, reply=("i", (-12345,)), result=Decimal("-123.45")),
    Call("get_value", FunctionID.GET_ALTITUDE, (1,), reply=("i", (100,)), result=Decimal(1)),
    Call("set_air_pressure_callback_period", FunctionID.SET_AIR_PRESSURE_CALLBACK_PERIOD, sent=("I", (0,))),
    Call(
        "set_air_pressure_callback_period",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_PERIOD,
        (Decimal("0.5"), False),
        sent=("I", (500,)),
        response_expected=False,
    ),
    Call(
        "get_air_pressure_callback_period",
        FunctionID.GET_AIR_PRESSURE_CALLBACK_PERIOD,
        reply=("I", (500,)),
        result=Decimal("0.5"),
    ),
    Call("set_altitude_callback_period", FunctionID.SET_ALTITUDE_CALLBACK_PERIOD, (2,), sent=("I", (2000,))),
    Call(
        "get_altitude_callback_period",
        FunctionID.GET_ALTITUDE_CALLBACK_PERIOD,
        reply=("I", (2000,)),
        result=Decimal(2),
    ),
    Call(
        "set_air_pressure_callback_threshold",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_THRESHOLD,
        sent=("c i i", (b"x", 0, 0)),
    ),
    Call(
        "set_air_pressure_callback_threshold",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_THRESHOLD,
        ("o", 90000, Decimal("101325.5")),
        sent=("c i i", (b"o", 900000, 1013255)),
    ),
    Call(
        "set_air_pressure_callback_threshold",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_THRESHOLD,
        (Threshold.LESS_THAN, 1000),
        sent=("c i i", (b"<", 10000, 0)),
    ),
    Call(
        "get_air_pressure_callback_threshold",
        FunctionID.GET_AIR_PRESSURE_CALLBACK_THRESHOLD,
        reply=("c i i", ("o", 900000, 1013255)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal(90000), Decimal("101325.5")),
    ),
    Call("set_altitude_callback_threshold", FunctionID.SET_ALTITUDE_CALLBACK_THRESHOLD, sent=("c i i", (b"x", 0, 0))),
    Call(
        "set_altitude_callback_threshold",
        FunctionID.SET_ALTITUDE_CALLBACK_THRESHOLD,
        ("i", Decimal("-10.5"), 8848),
        sent=("c i i", (b"i", -1050, 884800)),
    ),
    Call(
        "set_altitude_callback_threshold",
        FunctionID.SET_ALTITUDE_CALLBACK_THRESHOLD,
        (Threshold.GREATER_THAN, 1),
        sent=("c i i", (b">", 100, 0)),
    ),
    Call(
        "get_altitude_callback_threshold",
        FunctionID.GET_ALTITUDE_CALLBACK_THRESHOLD,
        reply=("c i i", ("i", -1050, 884800)),
        result=BasicCallbackConfiguration(Threshold.INSIDE, Decimal("-10.5"), Decimal(8848)),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, sent=("I", (100,))),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, reply=("I", (100,)), result=Decimal("0.1")),
    Call("get_chip_temperature", FunctionID.GET_CHIP_TEMPERATURE, reply=("h", (2500,)), result=Decimal("298.15")),
    # The default is the mean air pressure at sea level
    Call("set_reference_air_pressure", FunctionID.SET_REFERENCE_AIR_PRESSURE, sent=("i", (1013250,))),
    Call("set_reference_air_pressure", FunctionID.SET_REFERENCE_AIR_PRESSURE, (0,), sent=("i", (0,))),
    Call("set_reference_air_pressure", FunctionID.SET_REFERENCE_AIR_PRESSURE, (1000,), sent=("i", (10000,))),
    Call("set_reference_air_pressure", FunctionID.SET_REFERENCE_AIR_PRESSURE, (120000,), sent=("i", (1200000,))),
    Call(
        "get_reference_air_pressure",
        FunctionID.GET_REFERENCE_AIR_PRESSURE,
        reply=("i", (1013250,)),
        result=Decimal(101325),
    ),
    Call("set_averaging", FunctionID.SET_AVERAGING, sent=("B B B", (25, 10, 10))),
    Call("set_averaging", FunctionID.SET_AVERAGING, (0, 0, 255), sent=("B B B", (0, 0, 255))),
    Call("get_averaging", FunctionID.GET_AVERAGING, reply=("B B B", (25, 10, 255)), result=GetAveraging(25, 10, 255)),
    Call("set_i2c_mode", FunctionID.SET_I2C_MODE, sent=("B", (0,))),
    Call("set_i2c_mode", FunctionID.SET_I2C_MODE, (I2CMode.SLOW,), sent=("B", (1,))),
    Call("set_i2c_mode", FunctionID.SET_I2C_MODE, (1, False), sent=("B", (1,)), response_expected=False),
    Call("get_i2c_mode", FunctionID.GET_I2C_MODE, reply=("B", (1,)), result=I2CMode.SLOW),
]

REJECTED = [
    ("set_i2c_mode", (2,)),
    ("set_air_pressure_callback_period", (-1,)),
    ("set_altitude_callback_period", (-1,)),
    ("set_air_pressure_callback_threshold", ("?",)),
    ("set_altitude_callback_threshold", ("?",)),
    ("set_debounce_period", (-1,)),
    ("set_reference_air_pressure", (999,)),
    ("set_reference_air_pressure", (120001,)),
    ("set_averaging", (-1, 0, 0)),
    ("set_averaging", (26, 0, 0)),
    ("set_averaging", (0, -1, 0)),
    ("set_averaging", (0, 11, 0)),
    ("set_averaging", (0, 0, -1)),
    ("set_averaging", (0, 0, 256)),
    # There are the sids 0 and 1
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 221
    assert bricklet.get_api_version() == (2, 0, 1)
    assert str(bricklet).startswith("Barometer Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_set_callback_configuration(bricklet, connection):
    """The period and the threshold are set by two requests."""
    run(bricklet.set_callback_configuration(0, 1, False, Threshold.GREATER_THAN, 100000))
    run(bricklet.set_callback_configuration(1, Decimal("0.1"), maximum=7, response_expected=False))
    assert connection.requests == [
        request(FunctionID.SET_AIR_PRESSURE_CALLBACK_PERIOD, "I", 1000),
        request(FunctionID.SET_AIR_PRESSURE_CALLBACK_THRESHOLD, "c i i", b">", 1000000, 0),
        request(FunctionID.SET_ALTITUDE_CALLBACK_PERIOD, "I", 100, response_expected=False),
        request(FunctionID.SET_ALTITUDE_CALLBACK_THRESHOLD, "c i i", b"x", 0, 700, response_expected=False),
    ]


def test_get_callback_configuration(bricklet, connection):
    """The period and the threshold are merged."""
    connection.reply(FunctionID.GET_AIR_PRESSURE_CALLBACK_PERIOD, "I", 250)
    connection.reply(FunctionID.GET_AIR_PRESSURE_CALLBACK_THRESHOLD, "c i i", "i", 100, 200)
    connection.reply(FunctionID.GET_ALTITUDE_CALLBACK_PERIOD, "I", 0)
    connection.reply(FunctionID.GET_ALTITUDE_CALLBACK_THRESHOLD, "c i i", "x", -100, 0)
    assert run(bricklet.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal("0.25"), True, Threshold.INSIDE, Decimal(10), Decimal(20)
    )
    assert run(bricklet.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(0), True, Threshold.OFF, Decimal(-1), Decimal(0)
    )


def test_events(bricklet, connection):
    """The air pressure is sid 0 and converted to Pa, the altitude is sid 1 and converted to m."""
    connection.callback(CallbackID.AIR_PRESSURE, "i", 1013250)
    connection.callback(CallbackID.ALTITUDE, "i", -1234)
    connection.callback(CallbackID.AIR_PRESSURE_REACHED, "i", 900005)
    connection.callback(CallbackID.ALTITUDE_REACHED, "i", 4000)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.AIR_PRESSURE, Decimal(101325)),
        (1, CallbackID.ALTITUDE, Decimal("-12.34")),
        (0, CallbackID.AIR_PRESSURE_REACHED, Decimal("90000.5")),
        (1, CallbackID.ALTITUDE_REACHED, Decimal(40)),
    ]
