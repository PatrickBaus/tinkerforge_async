"""Tests for the Energy Monitor Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_energy_monitor import (
    BrickletEnergyMonitor,
    GetEnergyData,
    GetTransformerCalibration,
    GetTransformerStatus,
    GetWaveform,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletEnergyMonitor
FunctionID = BrickletEnergyMonitor.FunctionID
CallbackID = BrickletEnergyMonitor.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_ENERGY_DATA": 1,
    "RESET_ENERGY": 2,
    "GET_WAVEFORM_LOW_LEVEL": 3,
    "GET_TRANSFORMER_STATUS": 4,
    "SET_TRANSFORMER_CALIBRATION": 5,
    "GET_TRANSFORMER_CALIBRATION": 6,
    "CALIBRATE_OFFSET": 7,
    "SET_ENERGY_DATA_CALLBACK_CONFIGURATION": 8,
    "GET_ENERGY_DATA_CALLBACK_CONFIGURATION": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"ENERGY_DATA": 10}

CALLS: list[Call] = [
    Call(
        "get_energy_data",
        FunctionID.GET_ENERGY_DATA,
        (),
        reply=("i i i i i i H H", (3, 4, 5, 6, 7, 8, 9, 10)),
        result=GetEnergyData(
            Decimal("0.03"),
            Decimal("0.04"),
            Decimal("180"),
            Decimal("0.06"),
            Decimal("0.07"),
            Decimal("0.08"),
            Decimal("0.009"),
            Decimal("0.1"),
        ),
    ),
    Call("reset_energy", FunctionID.RESET_ENERGY, ()),
    Call("reset_energy", FunctionID.RESET_ENERGY, (False,), response_expected=False),
    Call(
        "get_waveform_low_level",
        FunctionID.GET_WAVEFORM_LOW_LEVEL,
        (),
        reply=("H 30h", (3, [4] * 30)),
        result=GetWaveform(3, (4,) * 30),
    ),
    Call(
        "get_transformer_status",
        FunctionID.GET_TRANSFORMER_STATUS,
        (),
        reply=("! !", (True, True)),
        result=GetTransformerStatus(True, True),
    ),
    Call("set_transformer_calibration", FunctionID.SET_TRANSFORMER_CALIBRATION, (3, 3, 0), sent=("H H h", (3, 3, 0))),
    Call(
        "set_transformer_calibration",
        FunctionID.SET_TRANSFORMER_CALIBRATION,
        (3, 3, 0, False),
        sent=("H H h", (3, 3, 0)),
        response_expected=False,
    ),
    Call(
        "get_transformer_calibration",
        FunctionID.GET_TRANSFORMER_CALIBRATION,
        (),
        reply=("H H h", (3, 4, 0)),
        result=GetTransformerCalibration(3, 4, 0),
    ),
    Call("calibrate_offset", FunctionID.CALIBRATE_OFFSET, ()),
    Call("calibrate_offset", FunctionID.CALIBRATE_OFFSET, (False,), response_expected=False),
    Call(
        "set_energy_data_callback_configuration",
        FunctionID.SET_ENERGY_DATA_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_energy_data_callback_configuration",
        FunctionID.SET_ENERGY_DATA_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_energy_data_callback_configuration",
        FunctionID.GET_ENERGY_DATA_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_ENERGY_DATA_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ENERGY_DATA_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_transformer_calibration", (65536, 3, 0)),
    ("set_transformer_calibration", (3, 65536, 0)),
    ("set_transformer_calibration", (3, 3, 1)),
    ("set_energy_data_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(device: BrickletEnergyMonitor) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2152
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Energy Monitor Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_get_waveform_transfers_the_stream(device: BrickletEnergyMonitor, connection: FakeConnection) -> None:
    """The high-level function get_waveform() uses get_waveform_low_level()."""
    data = [3] * 1536
    for offset in range(0, 1536, 30):
        connection.reply(FunctionID.GET_WAVEFORM_LOW_LEVEL, "H 30h", *(offset, chunk(data, offset, 30, 0)))
    result = run(device.get_waveform())
    assert connection.requests == [request(FunctionID.GET_WAVEFORM_LOW_LEVEL)] * 52
    assert result == (3,) * 1536


def test_callback_energy_data(device: BrickletEnergyMonitor, connection: FakeConnection) -> None:
    """The callback ENERGY_DATA is converted to an event."""
    connection.callback(CallbackID.ENERGY_DATA, "i i i i i i H H", *(3, 4, 5, 6, 7, 8, 9, 10))
    assert summary(read_events(device)) == [
        (
            0,
            CallbackID.ENERGY_DATA,
            GetEnergyData(
                Decimal("0.03"),
                Decimal("0.04"),
                Decimal("180"),
                Decimal("0.06"),
                Decimal("0.07"),
                Decimal("0.08"),
                Decimal("0.009"),
                Decimal("0.1"),
            ),
        )
    ]
