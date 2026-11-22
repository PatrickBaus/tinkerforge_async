"""Tests for the DMX Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_dmx import BrickletDMX, GetFrameCallbackConfig, GetFrameErrorCount, ReadFrame
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletDMX
FunctionID = BrickletDMX.FunctionID
CallbackID = BrickletDMX.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_DMX_MODE": 1,
    "GET_DMX_MODE": 2,
    "WRITE_FRAME_LOW_LEVEL": 3,
    "READ_FRAME_LOW_LEVEL": 4,
    "SET_FRAME_DURATION": 5,
    "GET_FRAME_DURATION": 6,
    "GET_FRAME_ERROR_COUNT": 7,
    "SET_COMMUNICATION_LED_CONFIG": 8,
    "GET_COMMUNICATION_LED_CONFIG": 9,
    "SET_ERROR_LED_CONFIG": 10,
    "GET_ERROR_LED_CONFIG": 11,
    "SET_FRAME_CALLBACK_CONFIG": 12,
    "GET_FRAME_CALLBACK_CONFIG": 13,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "FRAME_STARTED": 14,
    "FRAME_AVAILABLE": 15,
    "FRAME_LOW_LEVEL": 16,
    "FRAME_ERROR_COUNT": 17,
}

CALLS: list[Call] = [
    Call("set_dmx_mode", FunctionID.SET_DMX_MODE, (DEVICE.DMXMode.SLAVE,), sent=("B", (1,))),
    Call(
        "set_dmx_mode",
        FunctionID.SET_DMX_MODE,
        (DEVICE.DMXMode.SLAVE, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call("get_dmx_mode", FunctionID.GET_DMX_MODE, (), reply=("B", (1,)), result=DEVICE.DMXMode.SLAVE),
    Call(
        "write_frame_low_level",
        FunctionID.WRITE_FRAME_LOW_LEVEL,
        (3, 3, [i % 256 for i in range(60)]),
        sent=("H H 60B", (3, 3, [i % 256 for i in range(60)])),
    ),
    Call(
        "write_frame_low_level",
        FunctionID.WRITE_FRAME_LOW_LEVEL,
        (3, 3, [i % 256 for i in range(60)], False),
        sent=("H H 60B", (3, 3, [i % 256 for i in range(60)])),
        response_expected=False,
    ),
    Call(
        "read_frame_low_level",
        FunctionID.READ_FRAME_LOW_LEVEL,
        (),
        reply=("H H 56B I", (3, 4, [i % 256 for i in range(56)], 6)),
        result=ReadFrame(3, 4, tuple(i % 256 for i in range(56)), 6),
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
    Call(
        "get_frame_error_count",
        FunctionID.GET_FRAME_ERROR_COUNT,
        (),
        reply=("I I", (3, 4)),
        result=GetFrameErrorCount(3, 4),
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
        "set_error_led_config", FunctionID.SET_ERROR_LED_CONFIG, (DEVICE.ErrorLEDConfig.SHOW_ERROR,), sent=("B", (3,))
    ),
    Call(
        "set_error_led_config",
        FunctionID.SET_ERROR_LED_CONFIG,
        (DEVICE.ErrorLEDConfig.SHOW_ERROR, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_error_led_config",
        FunctionID.GET_ERROR_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.ErrorLEDConfig.SHOW_ERROR,
    ),
    Call(
        "set_frame_callback_config",
        FunctionID.SET_FRAME_CALLBACK_CONFIG,
        (True, True, True, True),
        sent=("! ! ! !", (True, True, True, True)),
    ),
    Call(
        "set_frame_callback_config",
        FunctionID.SET_FRAME_CALLBACK_CONFIG,
        (True, True, True, True, False),
        sent=("! ! ! !", (True, True, True, True)),
        response_expected=False,
    ),
    Call(
        "get_frame_callback_config",
        FunctionID.GET_FRAME_CALLBACK_CONFIG,
        (),
        reply=("! ! ! !", (True, True, True, True)),
        result=GetFrameCallbackConfig(True, True, True, True),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_dmx_mode", (12345,)),
    ("write_frame_low_level", (513, 3, [i % 256 for i in range(60)])),
    ("write_frame_low_level", (3, 65536, [i % 256 for i in range(60)])),
    ("write_frame_low_level", (3, 3, ([i % 256 for i in range(60)])[:-1])),
    ("write_frame", ([1] * 65536,)),
    ("set_frame_duration", (Decimal("65.536"),)),
    ("set_communication_led_config", (12345,)),
    ("set_error_led_config", (12345,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 285
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("DMX Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_write_frame_transfers_the_stream(device, connection):
    """The high-level function write_frame() uses write_frame_low_level()."""
    data = [i % 256 for i in range(3)]
    result = run(device.write_frame(*(data,)))
    assert connection.requests == [
        request(
            FunctionID.WRITE_FRAME_LOW_LEVEL, "H H 60B", *(3, offset, chunk([i % 256 for i in range(3)], offset, 60, 0))
        )
        for offset in range(0, 1, 60)
    ]
    assert result is None


def test_read_frame_transfers_the_stream(device, connection):
    """The high-level function read_frame() uses read_frame_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 56):
        connection.reply(FunctionID.READ_FRAME_LOW_LEVEL, "H H 56B I", *(3, offset, chunk(data, offset, 56, 0), 6))
    result = run(device.read_frame())
    assert connection.requests == [request(FunctionID.READ_FRAME_LOW_LEVEL)] * 1
    assert result.frame == bytes([i % 256 for i in range(3)])


def test_callback_frame_started(device, connection):
    """The callback FRAME_STARTED is converted to an event."""
    connection.callback(CallbackID.FRAME_STARTED)
    assert summary(read_events(device)) == [(0, CallbackID.FRAME_STARTED, None)]


def test_callback_frame_available(device, connection):
    """The callback FRAME_AVAILABLE is converted to an event."""
    connection.callback(CallbackID.FRAME_AVAILABLE, "I", *(3,))
    assert summary(read_events(device)) == [(1, CallbackID.FRAME_AVAILABLE, 3)]


def test_callback_frame(device, connection):
    """The callback FRAME is converted to an event."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 56):
        connection.callback(CallbackID.FRAME, "H H 56B I", *(3, offset, chunk(data, offset, 56, 0), 6))
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [(3, CallbackID.FRAME)]
    assert events[0].payload.frame == bytes([i % 256 for i in range(3)])
    connection_2 = FakeConnection()
    connection_2.callback(CallbackID.FRAME, "H H 56B I", *(59, 56, chunk(data, 0, 56, 0), 6))
    assert not read_events(DEVICE(UID, connection_2))


def test_callback_frame_error_count(device, connection):
    """The callback FRAME_ERROR_COUNT is converted to an event."""
    connection.callback(CallbackID.FRAME_ERROR_COUNT, "I I", *(3, 4))
    assert summary(read_events(device)) == [(2, CallbackID.FRAME_ERROR_COUNT, GetFrameErrorCount(3, 4))]
