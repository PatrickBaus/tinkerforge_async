"""Tests for the CO2 Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_co2_v2 import BrickletCO2V2, GetAllValues
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletCO2V2
FunctionID = BrickletCO2V2.FunctionID
CallbackID = BrickletCO2V2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_ALL_VALUES": 1,
    "SET_AIR_PRESSURE": 2,
    "GET_AIR_PRESSURE": 3,
    "SET_TEMPERATURE_OFFSET": 4,
    "GET_TEMPERATURE_OFFSET": 5,
    "SET_ALL_VALUES_CALLBACK_CONFIGURATION": 6,
    "GET_ALL_VALUES_CALLBACK_CONFIGURATION": 7,
    "GET_CO2_CONCENTRATION": 9,
    "SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION": 10,
    "GET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION": 11,
    "GET_TEMPERATURE": 13,
    "SET_TEMPERATURE_CALLBACK_CONFIGURATION": 14,
    "GET_TEMPERATURE_CALLBACK_CONFIGURATION": 15,
    "GET_HUMIDITY": 17,
    "SET_HUMIDITY_CALLBACK_CONFIGURATION": 18,
    "GET_HUMIDITY_CALLBACK_CONFIGURATION": 19,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"ALL_VALUES": 8, "CO2_CONCENTRATION": 12, "TEMPERATURE": 16, "HUMIDITY": 20}

CALLS: list[Call] = [
    Call(
        "get_all_values",
        FunctionID.GET_ALL_VALUES,
        (),
        reply=("H h H", (3, 4, 5)),
        result=GetAllValues(Decimal("3"), Decimal("273.19"), Decimal("0.05")),
    ),
    Call("set_air_pressure", FunctionID.SET_AIR_PRESSURE, (Decimal("0"),), sent=("H", (0,))),
    Call(
        "set_air_pressure",
        FunctionID.SET_AIR_PRESSURE,
        (Decimal("0"), False),
        sent=("H", (0,)),
        response_expected=False,
    ),
    Call("get_air_pressure", FunctionID.GET_AIR_PRESSURE, (), reply=("H", (0,)), result=Decimal("0")),
    Call("set_temperature_offset", FunctionID.SET_TEMPERATURE_OFFSET, (Decimal("273.18"),), sent=("H", (3,))),
    Call(
        "set_temperature_offset",
        FunctionID.SET_TEMPERATURE_OFFSET,
        (Decimal("273.18"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_temperature_offset", FunctionID.GET_TEMPERATURE_OFFSET, (), reply=("H", (3,)), result=Decimal("273.18")),
    Call(
        "set_all_values_callback_configuration",
        FunctionID.SET_ALL_VALUES_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_all_values_callback_configuration",
        FunctionID.SET_ALL_VALUES_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_all_values_callback_configuration",
        FunctionID.GET_ALL_VALUES_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("get_co2_concentration", FunctionID.GET_CO2_CONCENTRATION, (), reply=("H", (3,)), result=Decimal("3")),
    Call(
        "set_co2_concentration_callback_configuration",
        FunctionID.SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("3"), Decimal("3")),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_co2_concentration_callback_configuration",
        FunctionID.SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("3"), Decimal("3"), False),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_co2_concentration_callback_configuration",
        FunctionID.GET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c H H", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call("get_temperature", FunctionID.GET_TEMPERATURE, (), reply=("h", (3,)), result=Decimal("273.18")),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("273.18"), Decimal("273.18")),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("273.18"), Decimal("273.18"), False),
        sent=("I ! c h h", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_temperature_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c h h", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("273.21"), Decimal("273.22")
        ),
    ),
    Call("get_humidity", FunctionID.GET_HUMIDITY, (), reply=("H", (3,)), result=Decimal("0.03")),
    Call(
        "set_humidity_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("0.03")),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_humidity_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("0.03"), False),
        sent=("I ! c H H", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_humidity_callback_configuration",
        FunctionID.GET_HUMIDITY_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c H H", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.06"), Decimal("0.07")
        ),
    ),
    Call("set_automatic_self_calibration", FunctionID.SET_AUTOMATIC_SELF_CALIBRATION, (True,), sent=("!", (True,))),
    Call(
        "set_automatic_self_calibration",
        FunctionID.SET_AUTOMATIC_SELF_CALIBRATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_automatic_self_calibration",
        FunctionID.GET_AUTOMATIC_SELF_CALIBRATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call("set_forced_recalibration", FunctionID.SET_FORCED_RECALIBRATION, (Decimal("400"),), sent=("H", (400,))),
    Call(
        "set_forced_recalibration",
        FunctionID.SET_FORCED_RECALIBRATION,
        (Decimal("400"), False),
        sent=("H", (400,)),
        response_expected=False,
    ),
    Call(
        "get_forced_recalibration", FunctionID.GET_FORCED_RECALIBRATION, (), reply=("H", (400,)), result=Decimal("400")
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALL_VALUES_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALL_VALUES_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call("get_value", FunctionID.GET_CO2_CONCENTRATION, (1,), reply=("H", (3,)), result=Decimal("3")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION,
        (1, 1, True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
        sent=("I ! c H H", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I ! c H H", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
    Call("get_value", FunctionID.GET_TEMPERATURE, (2,), reply=("h", (3,)), result=Decimal("273.18")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (2, 1, True, Threshold.OUTSIDE, Decimal("273.18"), Decimal("273.19")),
        sent=("I ! c h h", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I ! c h h", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("273.18"), Decimal("273.19")),
    ),
    Call("get_value", FunctionID.GET_HUMIDITY, (3,), reply=("H", (3,)), result=Decimal("0.03")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        (3, 1, True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")),
        sent=("I ! c H H", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_HUMIDITY_CALLBACK_CONFIGURATION,
        (3,),
        reply=("I ! c H H", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_air_pressure", (Decimal("6553600"),)),
    ("set_temperature_offset", (Decimal("928.51"),)),
    ("set_all_values_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_co2_concentration_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("3"), Decimal("3"))),
    ("set_co2_concentration_callback_configuration", (Decimal("0.003"), True, "?", Decimal("3"), Decimal("3"))),
    ("set_co2_concentration_callback_configuration", (Decimal("0.003"), True, "o", Decimal("65536"), Decimal("3"))),
    ("set_co2_concentration_callback_configuration", (Decimal("0.003"), True, "o", Decimal("3"), Decimal("65536"))),
    (
        "set_temperature_callback_configuration",
        (Decimal("4294967.296"), True, "o", Decimal("273.18"), Decimal("273.18")),
    ),
    ("set_temperature_callback_configuration", (Decimal("0.003"), True, "?", Decimal("273.18"), Decimal("273.18"))),
    ("set_temperature_callback_configuration", (Decimal("0.003"), True, "o", Decimal("600.83"), Decimal("273.18"))),
    ("set_temperature_callback_configuration", (Decimal("0.003"), True, "o", Decimal("273.18"), Decimal("600.83"))),
    ("set_humidity_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.03"), Decimal("0.03"))),
    ("set_humidity_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.03"), Decimal("0.03"))),
    ("set_humidity_callback_configuration", (Decimal("0.003"), True, "o", Decimal("655.36"), Decimal("0.03"))),
    ("set_humidity_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("655.36"))),
    ("set_forced_recalibration", (Decimal("2001"),)),
    ("get_value", (4,)),
    ("set_callback_configuration", (4,)),
    ("get_callback_configuration", (4,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2147
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("CO2 Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_all_values(device, connection):
    """The callback ALL_VALUES is converted to an event."""
    connection.callback(CallbackID.ALL_VALUES, "H h H", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (0, CallbackID.ALL_VALUES, GetAllValues(Decimal("3"), Decimal("273.19"), Decimal("0.05")))
    ]


def test_callback_co2_concentration(device, connection):
    """The callback CO2_CONCENTRATION is converted to an event."""
    connection.callback(CallbackID.CO2_CONCENTRATION, "H", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.CO2_CONCENTRATION, Decimal("3"))]


def test_callback_temperature(device, connection):
    """The callback TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.TEMPERATURE, "h", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.TEMPERATURE, Decimal("273.18"))]


def test_callback_humidity(device, connection):
    """The callback HUMIDITY is converted to an event."""
    connection.callback(CallbackID.HUMIDITY, "H", *(3,))
    assert summary(read_events(device)) == [(3, CallbackID.HUMIDITY, Decimal("0.03"))]
