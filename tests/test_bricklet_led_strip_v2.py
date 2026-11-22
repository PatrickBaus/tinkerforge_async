"""Tests for the LED Strip Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_led_strip_v2 import BrickletLEDStripV2, GetLEDValues
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletLEDStripV2
FunctionID = BrickletLEDStripV2.FunctionID
CallbackID = BrickletLEDStripV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_LED_VALUES_LOW_LEVEL": 1,
    "GET_LED_VALUES_LOW_LEVEL": 2,
    "SET_FRAME_DURATION": 3,
    "GET_FRAME_DURATION": 4,
    "GET_SUPPLY_VOLTAGE": 5,
    "SET_CLOCK_FREQUENCY": 7,
    "GET_CLOCK_FREQUENCY": 8,
    "SET_CHIP_TYPE": 9,
    "GET_CHIP_TYPE": 10,
    "SET_CHANNEL_MAPPING": 11,
    "GET_CHANNEL_MAPPING": 12,
    "SET_FRAME_STARTED_CALLBACK_CONFIGURATION": 13,
    "GET_FRAME_STARTED_CALLBACK_CONFIGURATION": 14,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"FRAME_STARTED": 6}

CALLS: list[Call] = [
    Call(
        "set_led_values_low_level",
        FunctionID.SET_LED_VALUES_LOW_LEVEL,
        (3, 3, 3, [i % 256 for i in range(58)]),
        sent=("H H H 58B", (3, 3, 3, [i % 256 for i in range(58)])),
    ),
    Call(
        "set_led_values_low_level",
        FunctionID.SET_LED_VALUES_LOW_LEVEL,
        (3, 3, 3, [i % 256 for i in range(58)], False),
        sent=("H H H 58B", (3, 3, 3, [i % 256 for i in range(58)])),
        response_expected=False,
    ),
    Call(
        "get_led_values_low_level",
        FunctionID.GET_LED_VALUES_LOW_LEVEL,
        (3, 3),
        sent=("H H", (3, 3)),
        reply=("H H 60B", (3, 4, [i % 256 for i in range(60)])),
        result=GetLEDValues(3, 4, tuple(i % 256 for i in range(60))),
    ),
    Call("set_frame_duration", FunctionID.SET_FRAME_DURATION, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_frame_duration",
        FunctionID.SET_FRAME_DURATION,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_frame_duration", FunctionID.GET_FRAME_DURATION, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("get_supply_voltage", FunctionID.GET_SUPPLY_VOLTAGE, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call("set_clock_frequency", FunctionID.SET_CLOCK_FREQUENCY, (Decimal("10000"),), sent=("I", (10000,))),
    Call(
        "set_clock_frequency",
        FunctionID.SET_CLOCK_FREQUENCY,
        (Decimal("10000"), False),
        sent=("I", (10000,)),
        response_expected=False,
    ),
    Call("get_clock_frequency", FunctionID.GET_CLOCK_FREQUENCY, (), reply=("I", (10000,)), result=Decimal("10000")),
    Call("set_chip_type", FunctionID.SET_CHIP_TYPE, (DEVICE.ChipType.APA102,), sent=("H", (102,))),
    Call(
        "set_chip_type",
        FunctionID.SET_CHIP_TYPE,
        (DEVICE.ChipType.APA102, False),
        sent=("H", (102,)),
        response_expected=False,
    ),
    Call("get_chip_type", FunctionID.GET_CHIP_TYPE, (), reply=("H", (102,)), result=DEVICE.ChipType.APA102),
    Call("set_channel_mapping", FunctionID.SET_CHANNEL_MAPPING, (DEVICE.ChannelMapping.WBRG,), sent=("B", (225,))),
    Call(
        "set_channel_mapping",
        FunctionID.SET_CHANNEL_MAPPING,
        (DEVICE.ChannelMapping.WBRG, False),
        sent=("B", (225,)),
        response_expected=False,
    ),
    Call(
        "get_channel_mapping",
        FunctionID.GET_CHANNEL_MAPPING,
        (),
        reply=("B", (225,)),
        result=DEVICE.ChannelMapping.WBRG,
    ),
    Call(
        "set_frame_started_callback_configuration",
        FunctionID.SET_FRAME_STARTED_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_frame_started_callback_configuration",
        FunctionID.SET_FRAME_STARTED_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_frame_started_callback_configuration",
        FunctionID.GET_FRAME_STARTED_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call("start_frame", FunctionID.START_FRAME, ()),
    Call("start_frame", FunctionID.START_FRAME, (False,), response_expected=False),
    Call("truncate_frame", FunctionID.TRUNCATE_FRAME, (3,), sent=("H", (3,))),
    Call("truncate_frame", FunctionID.TRUNCATE_FRAME, (3, False), sent=("H", (3,)), response_expected=False),
    Call("set_auto_truncate", FunctionID.SET_AUTO_TRUNCATE, (3,), sent=("H", (3,))),
    Call("set_auto_truncate", FunctionID.SET_AUTO_TRUNCATE, (3, False), sent=("H", (3,)), response_expected=False),
    Call("get_auto_truncate", FunctionID.GET_AUTO_TRUNCATE, (), reply=("H", (3,)), result=3),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_led_values_low_level", (6145, 3, 3, [i % 256 for i in range(58)])),
    ("set_led_values_low_level", (3, 6145, 3, [i % 256 for i in range(58)])),
    ("set_led_values_low_level", (3, 3, 65536, [i % 256 for i in range(58)])),
    ("set_led_values_low_level", (3, 3, 3, ([i % 256 for i in range(58)])[:-1])),
    ("set_led_values", (3, [1] * 65536)),
    ("get_led_values_low_level", (6145, 3)),
    ("get_led_values_low_level", (3, 6145)),
    ("set_frame_duration", (Decimal("65.536"),)),
    ("set_clock_frequency", (Decimal("2000001"),)),
    ("set_chip_type", (12345,)),
    ("set_channel_mapping", (12345,)),
    ("truncate_frame", (6145,)),
    ("set_auto_truncate", (6145,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2103
    assert device.get_api_version() == (2, 0, 2)
    assert str(device).startswith("LED Strip Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_set_led_values_transfers_the_stream(device, connection):
    """The high-level function set_led_values() uses set_led_values_low_level()."""
    data = [i % 256 for i in range(3)]
    result = run(device.set_led_values(*(3, data)))
    assert connection.requests == [
        request(
            FunctionID.SET_LED_VALUES_LOW_LEVEL,
            "H H H 58B",
            *(3, 3, offset, chunk([i % 256 for i in range(3)], offset, 58, 0)),
        )
        for offset in range(0, 1, 58)
    ]
    assert result is None


def test_get_led_values_transfers_the_stream(device, connection):
    """The high-level function get_led_values() uses get_led_values_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 60):
        connection.reply(FunctionID.GET_LED_VALUES_LOW_LEVEL, "H H 60B", *(3, offset, chunk(data, offset, 60, 0)))
    result = run(device.get_led_values(*(3, 3)))
    assert connection.requests == [request(FunctionID.GET_LED_VALUES_LOW_LEVEL, "H H", *(3, 3))] * 1
    assert result == bytes([i % 256 for i in range(3)])


def test_callback_frame_started(device, connection):
    """The callback FRAME_STARTED is converted to an event."""
    connection.callback(CallbackID.FRAME_STARTED, "H", *(3,))
    assert summary(read_events(device)) == [(0, CallbackID.FRAME_STARTED, 3)]
