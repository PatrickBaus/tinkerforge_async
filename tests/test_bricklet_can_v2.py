"""Tests for the CAN Bricklet 2.0. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_can_v2 import (
    BrickletCANV2,
    GetErrorLog,
    GetQueueConfiguration,
    GetReadFilterConfiguration,
    GetTransceiverConfiguration,
    ReadFrame,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletCANV2
FunctionID = BrickletCANV2.FunctionID
CallbackID = BrickletCANV2.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "WRITE_FRAME_LOW_LEVEL": 1,
    "READ_FRAME_LOW_LEVEL": 2,
    "SET_FRAME_READ_CALLBACK_CONFIGURATION": 3,
    "GET_FRAME_READ_CALLBACK_CONFIGURATION": 4,
    "SET_TRANSCEIVER_CONFIGURATION": 5,
    "GET_TRANSCEIVER_CONFIGURATION": 6,
    "SET_QUEUE_CONFIGURATION_LOW_LEVEL": 7,
    "GET_QUEUE_CONFIGURATION_LOW_LEVEL": 8,
    "SET_READ_FILTER_CONFIGURATION": 9,
    "GET_READ_FILTER_CONFIGURATION": 10,
    "GET_ERROR_LOG_LOW_LEVEL": 11,
    "SET_COMMUNICATION_LED_CONFIG": 12,
    "GET_COMMUNICATION_LED_CONFIG": 13,
    "SET_ERROR_LED_CONFIG": 14,
    "GET_ERROR_LED_CONFIG": 15,
    "SET_FRAME_READABLE_CALLBACK_CONFIGURATION": 17,
    "GET_FRAME_READABLE_CALLBACK_CONFIGURATION": 18,
    "SET_ERROR_OCCURRED_CALLBACK_CONFIGURATION": 20,
    "GET_ERROR_OCCURRED_CALLBACK_CONFIGURATION": 21,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"FRAME_READ_LOW_LEVEL": 16, "FRAME_READABLE": 19, "ERROR_OCCURRED": 22}

CALLS: list[Call] = [
    Call(
        "write_frame_low_level",
        FunctionID.WRITE_FRAME_LOW_LEVEL,
        (DEVICE.FrameType.EXTENDED_REMOTE, 3, 3, [i % 256 for i in range(15)]),
        sent=("B I B 15B", (3, 3, 3, [i % 256 for i in range(15)])),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "read_frame_low_level",
        FunctionID.READ_FRAME_LOW_LEVEL,
        (),
        reply=("! B I B 15B", (True, 3, 5, 6, [i % 256 for i in range(15)])),
        result=ReadFrame(True, DEVICE.FrameType.EXTENDED_REMOTE, 5, 6, tuple(i % 256 for i in range(15))),
    ),
    Call(
        "set_frame_read_callback_configuration",
        FunctionID.SET_FRAME_READ_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_frame_read_callback_configuration",
        FunctionID.SET_FRAME_READ_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_frame_read_callback_configuration",
        FunctionID.GET_FRAME_READ_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "set_transceiver_configuration",
        FunctionID.SET_TRANSCEIVER_CONFIGURATION,
        (10000, Decimal("50"), DEVICE.TransceiverMode.READ_ONLY),
        sent=("I H B", (10000, 500, 2)),
    ),
    Call(
        "set_transceiver_configuration",
        FunctionID.SET_TRANSCEIVER_CONFIGURATION,
        (10000, Decimal("50"), DEVICE.TransceiverMode.READ_ONLY, False),
        sent=("I H B", (10000, 500, 2)),
        response_expected=False,
    ),
    Call(
        "get_transceiver_configuration",
        FunctionID.GET_TRANSCEIVER_CONFIGURATION,
        (),
        reply=("I H B", (10000, 500, 2)),
        result=GetTransceiverConfiguration(10000, Decimal("50"), DEVICE.TransceiverMode.READ_ONLY),
    ),
    Call(
        "set_queue_configuration_low_level",
        FunctionID.SET_QUEUE_CONFIGURATION_LOW_LEVEL,
        (3, 3, 3, 3, [-1] * 32, 3),
        sent=("B i H B 32b H", (3, 3, 3, 3, [-1] * 32, 3)),
    ),
    Call(
        "set_queue_configuration_low_level",
        FunctionID.SET_QUEUE_CONFIGURATION_LOW_LEVEL,
        (3, 3, 3, 3, [-1] * 32, 3, False),
        sent=("B i H B 32b H", (3, 3, 3, 3, [-1] * 32, 3)),
        response_expected=False,
    ),
    Call(
        "get_queue_configuration_low_level",
        FunctionID.GET_QUEUE_CONFIGURATION_LOW_LEVEL,
        (),
        reply=("B i H B 32b H", (3, 4, 5, 6, [-1] * 32, 8)),
        result=GetQueueConfiguration(3, 4, 5, 6, (-1,) * 32, 8),
    ),
    Call(
        "set_read_filter_configuration",
        FunctionID.SET_READ_FILTER_CONFIGURATION,
        (3, DEVICE.FilterMode.MATCH_STANDARD_AND_EXTENDED, 3, 3),
        sent=("B B I I", (3, 3, 3, 3)),
    ),
    Call(
        "set_read_filter_configuration",
        FunctionID.SET_READ_FILTER_CONFIGURATION,
        (3, DEVICE.FilterMode.MATCH_STANDARD_AND_EXTENDED, 3, 3, False),
        sent=("B B I I", (3, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_read_filter_configuration",
        FunctionID.GET_READ_FILTER_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
        reply=("B I I", (3, 4, 5)),
        result=GetReadFilterConfiguration(DEVICE.FilterMode.MATCH_STANDARD_AND_EXTENDED, 4, 5),
    ),
    Call(
        "get_error_log_low_level",
        FunctionID.GET_ERROR_LOG_LOW_LEVEL,
        (),
        reply=(
            "B B B I I I I I I I I B 32! I",
            (2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, [i % 2 == 0 for i in range(32)], 16),
        ),
        result=GetErrorLog(
            DEVICE.TransceiverState.DISABLED,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            tuple(i % 2 == 0 for i in range(32)),
            16,
        ),
    ),
    Call(
        "set_communication_led_config",
        FunctionID.SET_COMMUNICATION_LED_CONFIG,
        (DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION,),
        sent=("B", (3,)),
    ),
    Call(
        "set_communication_led_config",
        FunctionID.SET_COMMUNICATION_LED_CONFIG,
        (DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_communication_led_config",
        FunctionID.GET_COMMUNICATION_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION,
    ),
    Call(
        "set_error_led_config", FunctionID.SET_ERROR_LED_CONFIG, (DEVICE.ErrorLEDConfig.SHOW_ERROR,), sent=("B", (4,))
    ),
    Call(
        "set_error_led_config",
        FunctionID.SET_ERROR_LED_CONFIG,
        (DEVICE.ErrorLEDConfig.SHOW_ERROR, False),
        sent=("B", (4,)),
        response_expected=False,
    ),
    Call(
        "get_error_led_config",
        FunctionID.GET_ERROR_LED_CONFIG,
        (),
        reply=("B", (4,)),
        result=DEVICE.ErrorLEDConfig.SHOW_ERROR,
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_frame_readable_callback_configuration",
        FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "set_error_occurred_callback_configuration",
        FunctionID.SET_ERROR_OCCURRED_CALLBACK_CONFIGURATION,
        (True,),
        sent=("!", (True,)),
    ),
    Call(
        "set_error_occurred_callback_configuration",
        FunctionID.SET_ERROR_OCCURRED_CALLBACK_CONFIGURATION,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_error_occurred_callback_configuration",
        FunctionID.GET_ERROR_OCCURRED_CALLBACK_CONFIGURATION,
        (),
        reply=("!", (True,)),
        result=True,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write_frame_low_level", (12345, 3, 3, [i % 256 for i in range(15)])),
    ("write_frame_low_level", (DEVICE.FrameType.EXTENDED_REMOTE, 1073741824, 3, [i % 256 for i in range(15)])),
    ("write_frame_low_level", (DEVICE.FrameType.EXTENDED_REMOTE, 3, 16, [i % 256 for i in range(15)])),
    ("write_frame_low_level", (DEVICE.FrameType.EXTENDED_REMOTE, 3, 3, ([i % 256 for i in range(15)])[:-1])),
    ("write_frame", (DEVICE.FrameType.EXTENDED_REMOTE, 3, [1] * 16)),
    ("set_transceiver_configuration", (1000001, Decimal("50"), DEVICE.TransceiverMode.READ_ONLY)),
    ("set_transceiver_configuration", (10000, Decimal("90.1"), DEVICE.TransceiverMode.READ_ONLY)),
    ("set_transceiver_configuration", (10000, Decimal("50"), 12345)),
    ("set_queue_configuration_low_level", (33, 3, 3, 3, [-1] * 32, 3)),
    ("set_queue_configuration_low_level", (3, 2147483648, 3, 3, [-1] * 32, 3)),
    ("set_queue_configuration_low_level", (3, 3, 769, 3, [-1] * 32, 3)),
    ("set_queue_configuration_low_level", (3, 3, 3, 33, [-1] * 32, 3)),
    ("set_queue_configuration_low_level", (3, 3, 3, 3, ([-1] * 32)[:-1], 3)),
    ("set_queue_configuration_low_level", (3, 3, 3, 3, [-1] * 32, 769)),
    ("set_queue_configuration", (3, 3, 3, 3, [1] * 33)),
    ("set_read_filter_configuration", (32, DEVICE.FilterMode.MATCH_STANDARD_AND_EXTENDED, 3, 3)),
    ("set_read_filter_configuration", (3, 12345, 3, 3)),
    ("set_read_filter_configuration", (3, DEVICE.FilterMode.MATCH_STANDARD_AND_EXTENDED, 1073741824, 3)),
    ("set_read_filter_configuration", (3, DEVICE.FilterMode.MATCH_STANDARD_AND_EXTENDED, 3, 1073741824)),
    ("get_read_filter_configuration", (32,)),
    ("set_communication_led_config", (12345,)),
    ("set_error_led_config", (12345,)),
]


def test_identity(device: BrickletCANV2) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 2107
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("CAN Bricklet 2.0 with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_write_frame_transfers_the_stream(device: BrickletCANV2, connection: FakeConnection) -> None:
    """The high-level function write_frame() uses write_frame_low_level()."""
    data = [i % 256 for i in range(3)]
    connection.reply(FunctionID.WRITE_FRAME_LOW_LEVEL, "!", *(True,))
    result = run(device.write_frame(*(DEVICE.FrameType.EXTENDED_REMOTE, 3, data)))
    assert connection.requests == [
        request(
            FunctionID.WRITE_FRAME_LOW_LEVEL, "B I B 15B", *(3, 3, 3, chunk([i % 256 for i in range(3)], offset, 15, 0))
        )
        for offset in range(0, 1, 15)
    ]
    assert result is not None


def test_read_frame_transfers_the_stream(device: BrickletCANV2, connection: FakeConnection) -> None:
    """The high-level function read_frame() uses read_frame_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 15):
        connection.reply(FunctionID.READ_FRAME_LOW_LEVEL, "! B I B 15B", *(True, 3, 5, 3, chunk(data, offset, 15, 0)))
    result = run(device.read_frame())
    assert connection.requests == [request(FunctionID.READ_FRAME_LOW_LEVEL)] * 1
    assert result.data == bytes([i % 256 for i in range(3)])


def test_set_queue_configuration_transfers_the_stream(device: BrickletCANV2, connection: FakeConnection) -> None:
    """The high-level function set_queue_configuration() uses set_queue_configuration_low_level()."""
    data = [-1] * 3
    result = run(device.set_queue_configuration(*(3, 3, 3, 3, data)))
    assert connection.requests == [
        request(
            FunctionID.SET_QUEUE_CONFIGURATION_LOW_LEVEL,
            "B i H B 32b H",
            *(3, 3, 3, 3, chunk([-1] * 3, offset, 32, 0), 3),
        )
        for offset in range(0, 1, 32)
    ]
    assert result is None


def test_get_queue_configuration_transfers_the_stream(device: BrickletCANV2, connection: FakeConnection) -> None:
    """The high-level function get_queue_configuration() uses get_queue_configuration_low_level()."""
    data = [-1] * 3
    for offset in range(0, 1, 32):
        connection.reply(
            FunctionID.GET_QUEUE_CONFIGURATION_LOW_LEVEL, "B i H B 32b H", *(3, 4, 5, 3, chunk(data, offset, 32, 0), 8)
        )
    result = run(device.get_queue_configuration())
    assert connection.requests == [request(FunctionID.GET_QUEUE_CONFIGURATION_LOW_LEVEL)] * 1
    assert result.read_buffer_sizes == (-1,) * 3


def test_get_error_log_transfers_the_stream(device: BrickletCANV2, connection: FakeConnection) -> None:
    """The high-level function get_error_log() uses get_error_log_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    for offset in range(0, 1, 32):
        connection.reply(
            FunctionID.GET_ERROR_LOG_LOW_LEVEL,
            "B B B I I I I I I I I B 32! I",
            *(2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 3, chunk(data, offset, 32, False), 16),
        )
    result = run(device.get_error_log())
    assert connection.requests == [request(FunctionID.GET_ERROR_LOG_LOW_LEVEL)] * 1
    assert result.read_buffer_overflow_error_occurred == tuple(i % 2 == 0 for i in range(3))


def test_callback_frame_read(device: BrickletCANV2, connection: FakeConnection) -> None:
    """The callback FRAME_READ is converted to an event."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 15):
        connection.callback(CallbackID.FRAME_READ, "B I B 15B", *(3, 4, 3, chunk(data, offset, 15, 0)))
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [(2, CallbackID.FRAME_READ)]
    assert events[0].payload.data == bytes([i % 256 for i in range(3)])


def test_callback_frame_readable(device: BrickletCANV2, connection: FakeConnection) -> None:
    """The callback FRAME_READABLE is converted to an event."""
    connection.callback(CallbackID.FRAME_READABLE)
    assert summary(read_events(device)) == [(0, CallbackID.FRAME_READABLE, None)]


def test_callback_error_occurred(device: BrickletCANV2, connection: FakeConnection) -> None:
    """The callback ERROR_OCCURRED is converted to an event."""
    connection.callback(CallbackID.ERROR_OCCURRED)
    assert summary(read_events(device)) == [(1, CallbackID.ERROR_OCCURRED, None)]
