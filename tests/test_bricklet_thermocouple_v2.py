"""Tests for the Thermocouple Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

import pytest

from tinkerforge_async.bricklet_thermocouple_v2 import BrickletThermocoupleV2, GetConfiguration, GetErrorState
from tinkerforge_async.devices import AdvancedCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, read_events, request, run, summary

DEVICE = BrickletThermocoupleV2
FunctionID = BrickletThermocoupleV2.FunctionID
CallbackID = BrickletThermocoupleV2.CallbackID
Averaging = BrickletThermocoupleV2.Averaging
SensorType = BrickletThermocoupleV2.SensorType
LineFilter = BrickletThermocoupleV2.LineFilter

CONFIGURATION = AdvancedCallbackConfiguration(
    Decimal("0.25"), True, Threshold.INSIDE, Decimal("272.15"), Decimal("275.15")
)

CALLS = [
    Call("get_temperature", FunctionID.GET_TEMPERATURE, reply=("i", (2500,)), result=Decimal("298.15")),
    Call("get_value", FunctionID.GET_TEMPERATURE, (0,), reply=("i", (-4000,)), result=Decimal("233.15")),
    Call(
        "get_error_state", FunctionID.GET_ERROR_STATE, reply=("! !", (True, False)), result=GetErrorState(True, False)
    ),
    Call(
        "get_value", FunctionID.GET_ERROR_STATE, (1,), reply=("! !", (False, True)), result=GetErrorState(False, True)
    ),
    # The default of the thresholds is 0 °C
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        sent=("I ! c i i", (0, False, b"x", 0, 0)),
    ),
    Call(
        "set_temperature_callback_configuration",
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (Decimal("0.25"), True, "i", Decimal("272.15"), 275.15, False),
        sent=("I ! c i i", (250, True, b"i", -100, 200)),
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
        result=CONFIGURATION,
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I ! c i i", (250, True, "i", -100, 200)),
        result=CONFIGURATION,
    ),
    Call("set_configuration", FunctionID.SET_CONFIGURATION, sent=("B B B", (16, 3, 0))),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (Averaging.AVERAGING_1, SensorType.TYPE_B, LineFilter.FREQUENCY_60HZ),
        sent=("B B B", (1, 0, 1)),
    ),
    Call("set_configuration", FunctionID.SET_CONFIGURATION, (2, 9, 1), sent=("B B B", (2, 9, 1))),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        reply=("B B B", (4, 7, 1)),
        result=GetConfiguration(Averaging.AVERAGING_4, SensorType.TYPE_T, LineFilter.FREQUENCY_60HZ),
    ),
]

REJECTED = [
    ("set_temperature_callback_configuration", (-1,)),
    ("set_temperature_callback_configuration", (1, False, "?")),
    ("set_configuration", (3, 0, 0)),
    ("set_configuration", (1, 10, 0)),
    ("set_configuration", (1, 0, 2)),
    # There are the sids 0 and 1, but the sid 1 has no callback configuration
    ("get_value", (2,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(bricklet: BrickletThermocoupleV2) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2109
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Thermocouple Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_sensor_type(bricklet: BrickletThermocoupleV2, connection: FakeConnection) -> None:
    """The sensor is of type K by default. The type is updated, when the Bricklet is configured."""
    assert bricklet.sensor_type is SensorType.TYPE_K
    bricklet.sensor_type = 1
    assert bricklet.sensor_type is SensorType.TYPE_E
    assert BrickletThermocoupleV2(UID, connection.ipcon, SensorType.TYPE_J).sensor_type is SensorType.TYPE_J
    assert repr(bricklet).endswith("sensor_type=SensorType.TYPE_E)")
    with pytest.raises(ValueError):
        bricklet.sensor_type = 10

    run(bricklet.set_configuration(sensor_type=SensorType.TYPE_G32))
    assert bricklet.sensor_type is SensorType.TYPE_G32


@pytest.mark.parametrize("sensor_type, gain", [(SensorType.TYPE_G8, 8), (SensorType.TYPE_G32, 32)])
def test_the_gain_types_return_a_voltage(connection: FakeConnection, sensor_type: SensorType, gain: int) -> None:
    """The types G8 and G32 do not convert the voltage to a temperature. The value is `gain * 1.6 * 2^17 * voltage`."""
    bricklet = BrickletThermocoupleV2(UID, connection.ipcon, sensor_type)
    raw = gain * 2**17 * 2  # 1.25 V
    connection.reply(FunctionID.GET_TEMPERATURE, "i", raw)
    connection.reply(FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION, "I ! c i i", 0, False, "x", raw, -raw)
    connection.callback(CallbackID.TEMPERATURE, "i", raw)

    assert run(bricklet.get_temperature()) == Decimal("1.25")
    assert run(bricklet.get_temperature_callback_configuration())[3:] == (Decimal("1.25"), Decimal("-1.25"))
    run(bricklet.set_temperature_callback_configuration(0, False, Threshold.OFF, Decimal("1.25"), -1.25))
    assert connection.requests[-1] == request(
        FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION, "I ! c i i", 0, False, b"x", raw, -raw
    )
    assert summary(read_events(bricklet)) == [(0, CallbackID.TEMPERATURE, Decimal("1.25"))]


def test_events(bricklet: BrickletThermocoupleV2, connection: FakeConnection) -> None:
    """The temperature is sid 0 and the error state sid 1."""
    connection.callback(CallbackID.TEMPERATURE, "i", 2500)
    connection.callback(CallbackID.ERROR_STATE, "! !", True, False)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.TEMPERATURE, Decimal("298.15")),
        (1, CallbackID.ERROR_STATE, [True, False]),
    ]
