"""Tests for the Air Quality Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_air_quality import BrickletAirQuality, GetAllValues, GetIAQIndex
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletAirQuality
FunctionID = BrickletAirQuality.FunctionID
CallbackID = BrickletAirQuality.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_ALL_VALUES": 1,
    "SET_TEMPERATURE_OFFSET": 2,
    "GET_TEMPERATURE_OFFSET": 3,
    "SET_ALL_VALUES_CALLBACK_CONFIGURATION": 4,
    "GET_ALL_VALUES_CALLBACK_CONFIGURATION": 5,
    "GET_IAQ_INDEX": 7,
    "SET_IAQ_INDEX_CALLBACK_CONFIGURATION": 8,
    "GET_IAQ_INDEX_CALLBACK_CONFIGURATION": 9,
    "GET_TEMPERATURE": 11,
    "SET_TEMPERATURE_CALLBACK_CONFIGURATION": 12,
    "GET_TEMPERATURE_CALLBACK_CONFIGURATION": 13,
    "GET_HUMIDITY": 15,
    "SET_HUMIDITY_CALLBACK_CONFIGURATION": 16,
    "GET_HUMIDITY_CALLBACK_CONFIGURATION": 17,
    "GET_AIR_PRESSURE": 19,
    "SET_AIR_PRESSURE_CALLBACK_CONFIGURATION": 20,
    "GET_AIR_PRESSURE_CALLBACK_CONFIGURATION": 21,
    "REMOVE_CALIBRATION": 23,
    "SET_BACKGROUND_CALIBRATION_DURATION": 24,
    "GET_BACKGROUND_CALIBRATION_DURATION": 25,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "ALL_VALUES": 6,
    "IAQ_INDEX": 10,
    "TEMPERATURE": 14,
    "HUMIDITY": 18,
    "AIR_PRESSURE": 22,
}

CALLS: list[Call] = [
    Call(
        "get_all_values",
        FunctionID.GET_ALL_VALUES,
        (),
        reply=("i B i i i", (3, 3, 5, 6, 7)),
        result=GetAllValues(3, DEVICE.Accuracy.HIGH, Decimal("273.20"), Decimal("0.06"), Decimal("7")),
    ),
    Call("set_temperature_offset", FunctionID.SET_TEMPERATURE_OFFSET, (Decimal("0.03"),), sent=("i", (3,))),
    Call(
        "set_temperature_offset",
        FunctionID.SET_TEMPERATURE_OFFSET,
        (Decimal("0.03"), False),
        sent=("i", (3,)),
        response_expected=False,
    ),
    Call("get_temperature_offset", FunctionID.GET_TEMPERATURE_OFFSET, (), reply=("i", (3,)), result=Decimal("0.03")),
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
    Call(
        "get_iaq_index",
        FunctionID.GET_IAQ_INDEX,
        (),
        reply=("i B", (3, 3)),
        result=GetIAQIndex(3, DEVICE.Accuracy.HIGH),
    ),
    Call(
        "set_iaq_index_callback_configuration",
        FunctionID.SET_IAQ_INDEX_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_iaq_index_callback_configuration",
        FunctionID.SET_IAQ_INDEX_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_iaq_index_callback_configuration",
        FunctionID.GET_IAQ_INDEX_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("get_temperature", FunctionID.GET_TEMPERATURE, (), reply=("i", (3,)), result=Decimal("273.18")),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("273.18"), Decimal("273.18")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("273.18"), Decimal("273.18"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_temperature_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("273.21"), Decimal("273.22")
        ),
    ),
    Call("get_humidity", FunctionID.GET_HUMIDITY, (), reply=("i", (3,)), result=Decimal("0.03")),
    Call(
        "set_humidity_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("0.03")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_humidity_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("0.03"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_humidity_callback_configuration",
        FunctionID.GET_HUMIDITY_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(
            Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("0.06"), Decimal("0.07")
        ),
    ),
    Call("get_air_pressure", FunctionID.GET_AIR_PRESSURE, (), reply=("i", (3,)), result=Decimal("3")),
    Call(
        "set_air_pressure_callback_configuration",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("3"), Decimal("3")),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
    ),
    Call(
        "set_air_pressure_callback_configuration",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, "o", Decimal("3"), Decimal("3"), False),
        sent=("I ! c i i", (3, True, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_air_pressure_callback_configuration",
        FunctionID.GET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        (),
        reply=("I ! c i i", (3, True, "o", 6, 7)),
        result=AdvancedCallbackConfiguration(Decimal("0.003"), True, Threshold.OUTSIDE, Decimal("6"), Decimal("7")),
    ),
    Call("remove_calibration", FunctionID.REMOVE_CALIBRATION, ()),
    Call("remove_calibration", FunctionID.REMOVE_CALIBRATION, (False,), response_expected=False),
    Call(
        "set_background_calibration_duration",
        FunctionID.SET_BACKGROUND_CALIBRATION_DURATION,
        (DEVICE.BackgroundCalibrationDuration.DURATION_28_DAYS,),
        sent=("B", (1,)),
    ),
    Call(
        "set_background_calibration_duration",
        FunctionID.SET_BACKGROUND_CALIBRATION_DURATION,
        (DEVICE.BackgroundCalibrationDuration.DURATION_28_DAYS, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call(
        "get_background_calibration_duration",
        FunctionID.GET_BACKGROUND_CALIBRATION_DURATION,
        (),
        reply=("B", (1,)),
        result=DEVICE.BackgroundCalibrationDuration.DURATION_28_DAYS,
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
    Call(
        "set_callback_configuration",
        FunctionID.SET_IAQ_INDEX_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_IAQ_INDEX_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call("get_value", FunctionID.GET_TEMPERATURE, (2,), reply=("i", (3,)), result=Decimal("273.18")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (2, 1, True, Threshold.OUTSIDE, Decimal("273.18"), Decimal("273.19")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("273.18"), Decimal("273.19")),
    ),
    Call("get_value", FunctionID.GET_HUMIDITY, (3,), reply=("i", (3,)), result=Decimal("0.03")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_HUMIDITY_CALLBACK_CONFIGURATION,
        (3, 1, True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_HUMIDITY_CALLBACK_CONFIGURATION,
        (3,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("0.03"), Decimal("0.04")),
    ),
    Call("get_value", FunctionID.GET_AIR_PRESSURE, (4,), reply=("i", (3,)), result=Decimal("3")),
    Call(
        "set_callback_configuration",
        FunctionID.SET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        (4, 1, True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
        sent=("I ! c i i", (1000, True, "o", 3, 4)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
        (4,),
        reply=("I ! c i i", (1000, True, "o", 3, 4)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, Threshold.OUTSIDE, Decimal("3"), Decimal("4")),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_temperature_offset", (Decimal("21474836.48"),)),
    ("set_all_values_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_iaq_index_callback_configuration", (Decimal("4294967.296"), True)),
    (
        "set_temperature_callback_configuration",
        (Decimal("4294967.296"), True, "o", Decimal("273.18"), Decimal("273.18")),
    ),
    ("set_temperature_callback_configuration", (Decimal("0.003"), True, "?", Decimal("273.18"), Decimal("273.18"))),
    (
        "set_temperature_callback_configuration",
        (Decimal("0.003"), True, "o", Decimal("21475109.63"), Decimal("273.18")),
    ),
    (
        "set_temperature_callback_configuration",
        (Decimal("0.003"), True, "o", Decimal("273.18"), Decimal("21475109.63")),
    ),
    ("set_humidity_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("0.03"), Decimal("0.03"))),
    ("set_humidity_callback_configuration", (Decimal("0.003"), True, "?", Decimal("0.03"), Decimal("0.03"))),
    ("set_humidity_callback_configuration", (Decimal("0.003"), True, "o", Decimal("21474836.48"), Decimal("0.03"))),
    ("set_humidity_callback_configuration", (Decimal("0.003"), True, "o", Decimal("0.03"), Decimal("21474836.48"))),
    ("set_air_pressure_callback_configuration", (Decimal("4294967.296"), True, "o", Decimal("3"), Decimal("3"))),
    ("set_air_pressure_callback_configuration", (Decimal("0.003"), True, "?", Decimal("3"), Decimal("3"))),
    ("set_air_pressure_callback_configuration", (Decimal("0.003"), True, "o", Decimal("2147483648"), Decimal("3"))),
    ("set_air_pressure_callback_configuration", (Decimal("0.003"), True, "o", Decimal("3"), Decimal("2147483648"))),
    ("set_background_calibration_duration", (12345,)),
    ("get_value", (5,)),
    ("set_callback_configuration", (5,)),
    ("get_callback_configuration", (5,)),
]


def test_identity(device: BrickletAirQuality) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 297
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("Air Quality Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_all_values(device: BrickletAirQuality, connection: FakeConnection) -> None:
    """The callback ALL_VALUES is converted to an event."""
    connection.callback(CallbackID.ALL_VALUES, "i B i i i", *(3, 3, 5, 6, 7))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.ALL_VALUES,
            GetAllValues(3, DEVICE.Accuracy.HIGH, Decimal("273.20"), Decimal("0.06"), Decimal("7")),
        )
    ]


def test_callback_iaq_index(device: BrickletAirQuality, connection: FakeConnection) -> None:
    """The callback IAQ_INDEX is converted to an event."""
    connection.callback(CallbackID.IAQ_INDEX, "i B", *(3, 3))
    assert summary(read_events(device)) == [(1, CallbackID.IAQ_INDEX, GetIAQIndex(3, DEVICE.Accuracy.HIGH))]


def test_callback_temperature(device: BrickletAirQuality, connection: FakeConnection) -> None:
    """The callback TEMPERATURE is converted to an event."""
    connection.callback(CallbackID.TEMPERATURE, "i", *(3,))
    assert summary(read_events(device)) == [(2, CallbackID.TEMPERATURE, Decimal("273.18"))]


def test_callback_humidity(device: BrickletAirQuality, connection: FakeConnection) -> None:
    """The callback HUMIDITY is converted to an event."""
    connection.callback(CallbackID.HUMIDITY, "i", *(3,))
    assert summary(read_events(device)) == [(3, CallbackID.HUMIDITY, Decimal("0.03"))]


def test_callback_air_pressure(device: BrickletAirQuality, connection: FakeConnection) -> None:
    """The callback AIR_PRESSURE is converted to an event."""
    connection.callback(CallbackID.AIR_PRESSURE, "i", *(3,))
    assert summary(read_events(device)) == [(4, CallbackID.AIR_PRESSURE, Decimal("3"))]
