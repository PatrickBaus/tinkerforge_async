"""Tests for the Barometer Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_barometer_v2 import (
    BrickletBarometerV2,
    GetCalibration,
    GetMovingAverageConfiguration,
    GetSensorConfiguration,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, summary

DEVICE = BrickletBarometerV2
FunctionID = BrickletBarometerV2.FunctionID
CallbackID = BrickletBarometerV2.CallbackID
DataRate = BrickletBarometerV2.DataRate
LowPassFilter = BrickletBarometerV2.LowPassFilter

CALLS = [
    # The air pressure is transferred in 1/1000 hPa, the altitude in mm, and the temperature in 1/100 °C
    Call("get_air_pressure", FunctionID.GET_AIR_PRESSURE, reply=("i", (1013250,)), result=Decimal(101325)),
    Call("get_value", FunctionID.GET_AIR_PRESSURE, (0,), reply=("i", (1,)), result=Decimal("0.1")),
    Call("get_altitude", FunctionID.GET_ALTITUDE, reply=("i", (-12345,)), result=Decimal("-12.345")),
    Call("get_value", FunctionID.GET_ALTITUDE, (1,), reply=("i", (1000,)), result=Decimal(1)),
    Call("get_temperature", FunctionID.GET_TEMPERATURE, reply=("i", (2500,)), result=Decimal("298.15")),
    Call("get_value", FunctionID.GET_TEMPERATURE, (2,), reply=("i", (-4000,)), result=Decimal("233.15")),
    Call(
        "set_air_pressure_callback_configuration",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        sent=("I ! c i i", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_air_pressure_callback_configuration",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        (Decimal("0.5"), True, "o", 90000, Decimal("101325.5"), False),
        sent=("I ! c i i", (500, True, b"o", 900000, 1013255)),
        response_expected=False,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        (0, 1, False, Threshold.LESS_THAN, 1000),
        sent=("I ! c i i", (1000, False, b"<", 10000, 0)),
    ),
    Call(
        "get_air_pressure_callback_configuration",
        FunctionID.GET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        reply=("I ! c i i", (500, True, "o", 900000, 1013255)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.5"), True, Threshold.OUTSIDE, Decimal(90000), Decimal("101325.5")
        ),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c i i", (0, False, "x", 0, 0)),
        result=AdvancedCallbackConfiguration(Decimal(0), False, Threshold.OFF, Decimal(0), Decimal(0)),
    ),
    Call(
        "set_altitude_callback_configuration",
        FunctionID.SET_ALTITUDE_CALLBACK_CONFIGURATION,
        sent=("I ! c i i", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_altitude_callback_configuration",
        FunctionID.SET_ALTITUDE_CALLBACK_CONFIGURATION,
        (Decimal("0.5"), True, "i", Decimal("-10.5"), 8848),
        sent=("I ! c i i", (500, True, b"i", -10500, 8848000)),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALTITUDE_CALLBACK_CONFIGURATION,
        (1, 1, False, Threshold.GREATER_THAN, 1),
        sent=("I ! c i i", (1000, False, b">", 1000, 0)),
    ),
    Call(
        "get_altitude_callback_configuration",
        FunctionID.GET_ALTITUDE_CALLBACK_CONFIGURATION,
        reply=("I ! c i i", (500, True, "i", -10500, 8848000)),
        result=AdvancedCallbackConfiguration(Decimal("0.5"), True, Threshold.INSIDE, Decimal("-10.5"), Decimal(8848)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALTITUDE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c i i", (0, False, "x", 0, 0)),
        result=AdvancedCallbackConfiguration(Decimal(0), False, Threshold.OFF, Decimal(0), Decimal(0)),
    ),
    # The default of the temperature thresholds is 0 °C
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        sent=("I ! c i i", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.25"), True, "i", Decimal("274.15"), 275.15),
        sent=("I ! c i i", (250, True, b"i", 100, 200)),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (2, 1, False, Threshold.GREATER_THAN, Decimal("283.15")),
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
        (2,),
        reply=("I ! c i i", (0, False, "x", 0, 0)),
        result=AdvancedCallbackConfiguration(Decimal(0), False, Threshold.OFF, Decimal("273.15"), Decimal("273.15")),
    ),
    Call("set_moving_average_configuration", FunctionID.SET_MOVING_AVERAGE_CONFIGURATION, sent=("H H", (100, 100))),
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
    # The default is the mean air pressure at sea level
    Call("set_reference_air_pressure", FunctionID.SET_REFERENCE_AIR_PRESSURE, sent=("i", (1013250,))),
    Call("set_reference_air_pressure", FunctionID.SET_REFERENCE_AIR_PRESSURE, (0,), sent=("i", (0,))),
    Call(
        "set_reference_air_pressure",
        FunctionID.SET_REFERENCE_AIR_PRESSURE,
        (Decimal("99000.1"),),
        sent=("i", (990001,)),
    ),
    Call(
        "get_reference_air_pressure",
        FunctionID.GET_REFERENCE_AIR_PRESSURE,
        reply=("i", (1013250,)),
        result=Decimal(101325),
    ),
    Call(
        "set_calibration",
        FunctionID.SET_CALIBRATION,
        (Decimal("101325.1"), 101300),
        sent=("i i", (1013251, 1013000)),
    ),
    Call(
        "get_calibration",
        FunctionID.GET_CALIBRATION,
        reply=("i i", (1013251, 1013000)),
        result=GetCalibration(Decimal("101325.1"), Decimal(101300)),
    ),
    Call("set_sensor_configuration", FunctionID.SET_SENSOR_CONFIGURATION, sent=("B B", (4, 1))),
    Call(
        "set_sensor_configuration",
        FunctionID.SET_SENSOR_CONFIGURATION,
        (DataRate.OFF, LowPassFilter.FILTER_20TH),
        sent=("B B", (0, 2)),
    ),
    Call("set_sensor_configuration", FunctionID.SET_SENSOR_CONFIGURATION, (5, 0), sent=("B B", (5, 0))),
    Call(
        "get_sensor_configuration",
        FunctionID.GET_SENSOR_CONFIGURATION,
        reply=("B B", (1, 2)),
        result=GetSensorConfiguration(DataRate.RATE_1HZ, LowPassFilter.FILTER_20TH),
    ),
]

REJECTED = [
    ("set_air_pressure_callback_configuration", (-1,)),
    ("set_air_pressure_callback_configuration", (1, False, "?")),
    ("set_air_pressure_callback_configuration", (1, False, "x", -1)),
    ("set_air_pressure_callback_configuration", (1, False, "x", 0, -1)),
    ("set_altitude_callback_configuration", (-1,)),
    ("set_altitude_callback_configuration", (1, False, "?")),
    ("set_temperature_callback_configuration", (-1,)),
    ("set_temperature_callback_configuration", (1, False, "?")),
    ("set_moving_average_configuration", (0, 1)),
    ("set_moving_average_configuration", (1, 0)),
    ("set_sensor_configuration", (6, 0)),
    ("set_sensor_configuration", (0, 3)),
    # There are the sids 0 to 2
    ("get_value", (3,)),
    ("set_callback_configuration", (3,)),
    ("get_callback_configuration", (3,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2117
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Barometer Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet, connection):
    """The air pressure (sid 0) is converted to Pa, the altitude (sid 1) to m and the temperature (sid 2) to K."""
    connection.callback(CallbackID.AIR_PRESSURE, "i", 1013250)
    connection.callback(CallbackID.ALTITUDE, "i", -1234)
    connection.callback(CallbackID.TEMPERATURE, "i", 2500)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.AIR_PRESSURE, Decimal(101325)),
        (1, CallbackID.ALTITUDE, Decimal("-1.234")),
        (2, CallbackID.TEMPERATURE, Decimal("298.15")),
    ]
