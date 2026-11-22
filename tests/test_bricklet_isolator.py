"""Tests for the Isolator Bricklet."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_isolator import BrickletIsolator, GetStatistics
from tinkerforge_async.devices import GetSPITFPBaudrateConfig, GetSPITFPErrorCount, SimpleCallbackConfiguration

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, read_events, summary

DEVICE = BrickletIsolator
FunctionID = BrickletIsolator.FunctionID
CallbackID = BrickletIsolator.CallbackID

# The uid "21" of the connected Bricklet is 58 in base58
STATISTICS = ("I I H 8s", (1000, 2000, 2113, b"21"))

CALLS = [
    Call("get_statistics", FunctionID.GET_STATISTICS, reply=STATISTICS, result=GetStatistics(1000, 2000, 2113, 58)),
    Call("get_value", FunctionID.GET_STATISTICS, (0,), reply=STATISTICS, result=GetStatistics(1000, 2000, 2113, 58)),
    Call("set_spitfp_baudrate_config", FunctionID.SET_SPITFP_BAUDRATE_CONFIG, sent=("! I", (True, 400000))),
    Call(
        "set_spitfp_baudrate_config",
        FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
        (False, 2000000, False),
        sent=("! I", (False, 2000000)),
        response_expected=False,
    ),
    Call(
        "get_spitfp_baudrate_config",
        FunctionID.GET_SPITFP_BAUDRATE_CONFIG,
        reply=("! I", (True, 400000)),
        result=GetSPITFPBaudrateConfig(True, 400000),
    ),
    Call("set_spitfp_baudrate", FunctionID.SET_SPITFP_BAUDRATE, sent=("I", (1400000,))),
    Call("set_spitfp_baudrate", FunctionID.SET_SPITFP_BAUDRATE, (400000,), sent=("I", (400000,))),
    Call("get_spitfp_baudrate", FunctionID.GET_SPITFP_BAUDRATE, reply=("I", (1400000,)), result=1400000),
    Call(
        "get_isolator_spitfp_error_count",
        FunctionID.GET_ISOLATOR_SPITFP_ERROR_COUNT,
        reply=("I I I I", (1, 2, 3, 4)),
        result=GetSPITFPErrorCount(1, 2, 3, 4),
    ),
    Call(
        "set_statistics_callback_configuration",
        FunctionID.SET_STATISTICS_CALLBACK_CONFIGURATION,
        sent=("I !", (0, False)),
    ),
    Call(
        "set_statistics_callback_configuration",
        FunctionID.SET_STATISTICS_CALLBACK_CONFIGURATION,
        (Decimal("0.5"), True),
        sent=("I !", (500, True)),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_STATISTICS_CALLBACK_CONFIGURATION,
        (0, 2, True, False),
        sent=("I !", (2000, True)),
        response_expected=False,
    ),
    Call(
        "get_statistics_callback_configuration",
        FunctionID.GET_STATISTICS_CALLBACK_CONFIGURATION,
        reply=("I !", (500, True)),
        result=SimpleCallbackConfiguration(Decimal("0.5"), True),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_STATISTICS_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (0, False)),
        result=SimpleCallbackConfiguration(Decimal(0), False),
    ),
]

REJECTED = [
    ("set_statistics_callback_configuration", (-1,)),
    # There is only the sid 0
    ("get_value", (1,)),
    ("set_callback_configuration", (1,)),
    ("get_callback_configuration", (1,)),
]


def test_identity(bricklet: BrickletIsolator) -> None:
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2122
    assert bricklet.get_api_version() == (2, 0, 1)
    assert str(bricklet).startswith("Isolator Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet: BrickletIsolator, connection: FakeConnection) -> None:
    """The statistics are sid 0. The uid of the connected Bricklet is decoded like it is by `get_statistics()`."""
    connection.callback(CallbackID.STATISTICS, *STATISTICS[0:1], *STATISTICS[1])
    assert summary(read_events(bricklet)) == [(0, CallbackID.STATISTICS, GetStatistics(1000, 2000, 2113, 58))]
