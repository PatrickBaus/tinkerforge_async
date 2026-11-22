"""Tests for the Industrial Dual Analog In Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_industrial_dual_analog_in import BrickletIndustrialDualAnalogIn, GetCalibration
from tinkerforge_async.devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletIndustrialDualAnalogIn
FunctionID = BrickletIndustrialDualAnalogIn.FunctionID
CallbackID = BrickletIndustrialDualAnalogIn.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_VOLTAGE": 1,
    "SET_VOLTAGE_CALLBACK_PERIOD": 2,
    "GET_VOLTAGE_CALLBACK_PERIOD": 3,
    "SET_VOLTAGE_CALLBACK_THRESHOLD": 4,
    "GET_VOLTAGE_CALLBACK_THRESHOLD": 5,
    "SET_DEBOUNCE_PERIOD": 6,
    "GET_DEBOUNCE_PERIOD": 7,
    "SET_SAMPLE_RATE": 8,
    "GET_SAMPLE_RATE": 9,
    "SET_CALIBRATION": 10,
    "GET_CALIBRATION": 11,
    "GET_ADC_VALUES": 12,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"VOLTAGE": 13, "VOLTAGE_REACHED": 14}

CALLS: list[Call] = [
    Call("get_voltage", FunctionID.GET_VOLTAGE, (1,), sent=("B", (1,)), reply=("i", (3,)), result=Decimal("0.003")),
    Call(
        "set_voltage_callback_period",
        FunctionID.SET_VOLTAGE_CALLBACK_PERIOD,
        (1, Decimal("0.003")),
        sent=("B I", (1, 3)),
    ),
    Call(
        "set_voltage_callback_period",
        FunctionID.SET_VOLTAGE_CALLBACK_PERIOD,
        (1, Decimal("0.003"), False),
        sent=("B I", (1, 3)),
        response_expected=False,
    ),
    Call(
        "get_voltage_callback_period",
        FunctionID.GET_VOLTAGE_CALLBACK_PERIOD,
        (1,),
        sent=("B", (1,)),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
    Call(
        "set_voltage_callback_threshold",
        FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
        (1, "o", Decimal("0.003"), Decimal("0.003")),
        sent=("B c i i", (1, "o", 3, 3)),
    ),
    Call(
        "set_voltage_callback_threshold",
        FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
        (1, "o", Decimal("0.003"), Decimal("0.003"), False),
        sent=("B c i i", (1, "o", 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_voltage_callback_threshold",
        FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD,
        (1,),
        sent=("B", (1,)),
        reply=("c i i", ("o", 4, 5)),
        result=BasicCallbackConfiguration(Threshold.OUTSIDE, Decimal("0.004"), Decimal("0.005")),
    ),
    Call("set_debounce_period", FunctionID.SET_DEBOUNCE_PERIOD, (Decimal("0.003"),), sent=("I", (3,))),
    Call(
        "set_debounce_period",
        FunctionID.SET_DEBOUNCE_PERIOD,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call("get_debounce_period", FunctionID.GET_DEBOUNCE_PERIOD, (), reply=("I", (3,)), result=Decimal("0.003")),
    Call("set_sample_rate", FunctionID.SET_SAMPLE_RATE, (DEVICE.SampleRate.SAMPLE_RATE_1_SPS,), sent=("B", (7,))),
    Call(
        "set_sample_rate",
        FunctionID.SET_SAMPLE_RATE,
        (DEVICE.SampleRate.SAMPLE_RATE_1_SPS, False),
        sent=("B", (7,)),
        response_expected=False,
    ),
    Call(
        "get_sample_rate", FunctionID.GET_SAMPLE_RATE, (), reply=("B", (7,)), result=DEVICE.SampleRate.SAMPLE_RATE_1_SPS
    ),
    Call("set_calibration", FunctionID.SET_CALIBRATION, ([3] * 2, [3] * 2), sent=("2i 2i", ([3] * 2, [3] * 2))),
    Call(
        "set_calibration",
        FunctionID.SET_CALIBRATION,
        ([3] * 2, [3] * 2, False),
        sent=("2i 2i", ([3] * 2, [3] * 2)),
        response_expected=False,
    ),
    Call(
        "get_calibration",
        FunctionID.GET_CALIBRATION,
        (),
        reply=("2i 2i", ([3] * 2, [4] * 2)),
        result=GetCalibration((3,) * 2, (4,) * 2),
    ),
    Call("get_adc_values", FunctionID.GET_ADC_VALUES, (), reply=("2i", ([3] * 2,)), result=(3,) * 2),
    Call("get_value", FunctionID.GET_VOLTAGE, (0,), sent=("B", (0,)), reply=("i", (3,)), result=Decimal("0.003")),
    Call("get_value", FunctionID.GET_VOLTAGE, (1,), sent=("B", (1,)), reply=("i", (3,)), result=Decimal("0.003")),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("get_voltage", (2,)),
    ("set_voltage_callback_period", (2, Decimal("0.003"))),
    ("set_voltage_callback_period", (1, Decimal("4294967.296"))),
    ("get_voltage_callback_period", (2,)),
    ("set_voltage_callback_threshold", (2, "o", Decimal("0.003"), Decimal("0.003"))),
    ("set_voltage_callback_threshold", (1, "?", Decimal("0.003"), Decimal("0.003"))),
    ("set_voltage_callback_threshold", (1, "o", Decimal("2147483.648"), Decimal("0.003"))),
    ("set_voltage_callback_threshold", (1, "o", Decimal("0.003"), Decimal("2147483.648"))),
    ("get_voltage_callback_threshold", (2,)),
    ("set_debounce_period", (Decimal("4294967.296"),)),
    ("set_sample_rate", (12345,)),
    ("set_calibration", (([3] * 2)[:-1], [3] * 2)),
    ("set_calibration", ([3] * 2, ([3] * 2)[:-1])),
    ("get_value", (2,)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device: BrickletIndustrialDualAnalogIn) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 249
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Industrial Dual Analog In Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_configuration_of_sid_0(device: BrickletIndustrialDualAnalogIn, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(0, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_VOLTAGE_CALLBACK_PERIOD, "B I", *(0, 1000)),
            request(FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD, "B c i i", *(0, "o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_VOLTAGE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(0)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")
    )


def test_callback_configuration_of_sid_1(device: BrickletIndustrialDualAnalogIn, connection: FakeConnection) -> None:
    """The period and the threshold are configured by separate functions."""
    run(device.set_callback_configuration(1, 1, True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")))
    assert sorted(connection.requests, key=lambda request: request.function_id.value) == sorted(
        [
            request(FunctionID.SET_VOLTAGE_CALLBACK_PERIOD, "B I", *(1, 1000)),
            request(FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD, "B c i i", *(1, "o", 3, 4)),
        ],
        key=lambda request: request.function_id.value,
    )
    connection.requests.clear()
    connection.reply(FunctionID.GET_VOLTAGE_CALLBACK_PERIOD, "I", 1000)
    connection.reply(FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD, "c i i", "o", 3, 4)
    assert run(device.get_callback_configuration(1)) == AdvancedCallbackConfiguration(
        Decimal(1), True, Threshold.OUTSIDE, Decimal("0.003"), Decimal("0.004")
    )


def test_callback_voltage(device: BrickletIndustrialDualAnalogIn, connection: FakeConnection) -> None:
    """The callback VOLTAGE is converted to an event."""
    connection.callback(CallbackID.VOLTAGE, "B i", *(1, 4))
    assert summary(read_events(device)) == [(1, CallbackID.VOLTAGE, Decimal("0.004"))]


def test_callback_voltage_reached(device: BrickletIndustrialDualAnalogIn, connection: FakeConnection) -> None:
    """The callback VOLTAGE_REACHED is converted to an event."""
    connection.callback(CallbackID.VOLTAGE_REACHED, "B i", *(1, 4))
    assert summary(read_events(device)) == [(1, CallbackID.VOLTAGE_REACHED, Decimal("0.004"))]
