"""Tests for the Particulate Matter Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_particulate_matter import (
    BrickletParticulateMatter,
    GetPMConcentration,
    GetPMCount,
    GetSensorInfo,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletParticulateMatter
FunctionID = BrickletParticulateMatter.FunctionID
CallbackID = BrickletParticulateMatter.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_PM_CONCENTRATION": 1,
    "GET_PM_COUNT": 2,
    "SET_ENABLE": 3,
    "GET_ENABLE": 4,
    "GET_SENSOR_INFO": 5,
    "SET_PM_CONCENTRATION_CALLBACK_CONFIGURATION": 6,
    "GET_PM_CONCENTRATION_CALLBACK_CONFIGURATION": 7,
    "SET_PM_COUNT_CALLBACK_CONFIGURATION": 8,
    "GET_PM_COUNT_CALLBACK_CONFIGURATION": 9,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"PM_CONCENTRATION": 10, "PM_COUNT": 11}

CALLS: list[Call] = [
    Call(
        "get_pm_concentration",
        FunctionID.GET_PM_CONCENTRATION,
        (),
        reply=("H H H", (3, 4, 5)),
        result=GetPMConcentration(Decimal("3E-9"), Decimal("4E-9"), Decimal("5E-9")),
    ),
    Call(
        "get_pm_count",
        FunctionID.GET_PM_COUNT,
        (),
        reply=("H H H H H H", (3, 4, 5, 6, 7, 8)),
        result=GetPMCount(
            Decimal("30000"), Decimal("40000"), Decimal("50000"), Decimal("60000"), Decimal("70000"), Decimal("80000")
        ),
    ),
    Call("set_enable", FunctionID.SET_ENABLE, (True,), sent=("!", (True,))),
    Call("set_enable", FunctionID.SET_ENABLE, (True, False), sent=("!", (True,)), response_expected=False),
    Call("get_enable", FunctionID.GET_ENABLE, (), reply=("!", (True,)), result=True),
    Call(
        "get_sensor_info",
        FunctionID.GET_SENSOR_INFO,
        (),
        reply=("B B B B", (3, 4, 5, 6)),
        result=GetSensorInfo(3, 4, 5, 6),
    ),
    Call(
        "set_pm_concentration_callback_configuration",
        FunctionID.SET_PM_CONCENTRATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_pm_concentration_callback_configuration",
        FunctionID.SET_PM_CONCENTRATION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_pm_concentration_callback_configuration",
        FunctionID.GET_PM_CONCENTRATION_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_pm_count_callback_configuration",
        FunctionID.SET_PM_COUNT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_pm_count_callback_configuration",
        FunctionID.SET_PM_COUNT_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_pm_count_callback_configuration",
        FunctionID.GET_PM_COUNT_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_PM_CONCENTRATION_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_PM_CONCENTRATION_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_PM_COUNT_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_PM_COUNT_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_pm_concentration_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_pm_count_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_callback_configuration", (2,)),
    ("get_callback_configuration", (2,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2110
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("Particulate Matter Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_pm_concentration(device, connection):
    """The callback PM_CONCENTRATION is converted to an event."""
    connection.callback(CallbackID.PM_CONCENTRATION, "H H H", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (0, CallbackID.PM_CONCENTRATION, GetPMConcentration(Decimal("3E-9"), Decimal("4E-9"), Decimal("5E-9")))
    ]


def test_callback_pm_count(device, connection):
    """The callback PM_COUNT is converted to an event."""
    connection.callback(CallbackID.PM_COUNT, "H H H H H H", *(3, 4, 5, 6, 7, 8))
    assert summary(read_events(device)) == [
        (
            1,
            CallbackID.PM_COUNT,
            GetPMCount(
                Decimal("30000"),
                Decimal("40000"),
                Decimal("50000"),
                Decimal("60000"),
                Decimal("70000"),
                Decimal("80000"),
            ),
        )
    ]
