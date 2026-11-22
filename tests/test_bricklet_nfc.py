"""Tests for the NFC Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_nfc import (
    BrickletNFC,
    CardemuGetState,
    CardemuGetTagID,
    CardemuStateChangedEvent,
    P2PGetState,
    P2PReadNDEF,
    P2PStateChangedEvent,
    ReaderGetState,
    ReaderGetTagID,
    ReaderReadNDEF,
    ReaderReadPage,
    ReaderStateChangedEvent,
    SimpleGetTagID,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletNFC
FunctionID = BrickletNFC.FunctionID
CallbackID = BrickletNFC.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "SET_MODE": 1,
    "GET_MODE": 2,
    "READER_REQUEST_TAG_ID": 3,
    "READER_GET_TAG_ID_LOW_LEVEL": 4,
    "READER_GET_STATE": 5,
    "READER_WRITE_NDEF_LOW_LEVEL": 6,
    "READER_REQUEST_NDEF": 7,
    "READER_READ_NDEF_LOW_LEVEL": 8,
    "READER_AUTHENTICATE_MIFARE_CLASSIC_PAGE": 9,
    "READER_WRITE_PAGE_LOW_LEVEL": 10,
    "READER_REQUEST_PAGE": 11,
    "READER_READ_PAGE_LOW_LEVEL": 12,
    "CARDEMU_GET_STATE": 14,
    "CARDEMU_START_DISCOVERY": 15,
    "CARDEMU_WRITE_NDEF_LOW_LEVEL": 16,
    "CARDEMU_START_TRANSFER": 17,
    "P2P_GET_STATE": 19,
    "P2P_START_DISCOVERY": 20,
    "P2P_WRITE_NDEF_LOW_LEVEL": 21,
    "P2P_START_TRANSFER": 22,
    "P2P_READ_NDEF_LOW_LEVEL": 23,
    "SET_DETECTION_LED_CONFIG": 25,
    "GET_DETECTION_LED_CONFIG": 26,
    "SET_MAXIMUM_TIMEOUT": 27,
    "GET_MAXIMUM_TIMEOUT": 28,
    "SIMPLE_GET_TAG_ID_LOW_LEVEL": 29,
    "CARDEMU_SET_TAG_ID": 30,
    "CARDEMU_GET_TAG_ID": 31,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "READER_STATE_CHANGED": 13,
    "CARDEMU_STATE_CHANGED": 18,
    "P2P_STATE_CHANGED": 24,
}

CALLS: list[Call] = [
    Call("set_mode", FunctionID.SET_MODE, (DEVICE.Mode.SIMPLE,), sent=("B", (4,))),
    Call("set_mode", FunctionID.SET_MODE, (DEVICE.Mode.SIMPLE, False), sent=("B", (4,)), response_expected=False),
    Call("get_mode", FunctionID.GET_MODE, (), reply=("B", (4,)), result=DEVICE.Mode.SIMPLE),
    Call("reader_request_tag_id", FunctionID.READER_REQUEST_TAG_ID, ()),
    Call("reader_request_tag_id", FunctionID.READER_REQUEST_TAG_ID, (False,), response_expected=False),
    Call(
        "reader_get_tag_id_low_level",
        FunctionID.READER_GET_TAG_ID_LOW_LEVEL,
        (),
        reply=("B B 32B", (6, 4, [i % 256 for i in range(32)])),
        result=ReaderGetTagID(DEVICE.TagType.PHONE, 4, tuple(i % 256 for i in range(32))),
    ),
    Call(
        "reader_get_state",
        FunctionID.READER_GET_STATE,
        (),
        reply=("B !", (199, True)),
        result=ReaderGetState(DEVICE.ReaderState.REQUEST_NDEF_ERROR, True),
    ),
    Call(
        "reader_write_ndef_low_level",
        FunctionID.READER_WRITE_NDEF_LOW_LEVEL,
        (3, 3, [i % 256 for i in range(60)]),
        sent=("H H 60B", (3, 3, [i % 256 for i in range(60)])),
    ),
    Call(
        "reader_write_ndef_low_level",
        FunctionID.READER_WRITE_NDEF_LOW_LEVEL,
        (3, 3, [i % 256 for i in range(60)], False),
        sent=("H H 60B", (3, 3, [i % 256 for i in range(60)])),
        response_expected=False,
    ),
    Call("reader_request_ndef", FunctionID.READER_REQUEST_NDEF, ()),
    Call("reader_request_ndef", FunctionID.READER_REQUEST_NDEF, (False,), response_expected=False),
    Call(
        "reader_read_ndef_low_level",
        FunctionID.READER_READ_NDEF_LOW_LEVEL,
        (),
        reply=("H H 60B", (3, 4, [i % 256 for i in range(60)])),
        result=ReaderReadNDEF(3, 4, tuple(i % 256 for i in range(60))),
    ),
    Call(
        "reader_authenticate_mifare_classic_page",
        FunctionID.READER_AUTHENTICATE_MIFARE_CLASSIC_PAGE,
        (3, DEVICE.Key.B, [i % 256 for i in range(6)]),
        sent=("H B 6B", (3, 1, [i % 256 for i in range(6)])),
    ),
    Call(
        "reader_authenticate_mifare_classic_page",
        FunctionID.READER_AUTHENTICATE_MIFARE_CLASSIC_PAGE,
        (3, DEVICE.Key.B, [i % 256 for i in range(6)], False),
        sent=("H B 6B", (3, 1, [i % 256 for i in range(6)])),
        response_expected=False,
    ),
    Call(
        "reader_write_page_low_level",
        FunctionID.READER_WRITE_PAGE_LOW_LEVEL,
        (DEVICE.ReaderWrite.TYPE4_NDEF, 3, 3, [i % 256 for i in range(58)]),
        sent=("H H H 58B", (4, 3, 3, [i % 256 for i in range(58)])),
    ),
    Call(
        "reader_write_page_low_level",
        FunctionID.READER_WRITE_PAGE_LOW_LEVEL,
        (DEVICE.ReaderWrite.TYPE4_NDEF, 3, 3, [i % 256 for i in range(58)], False),
        sent=("H H H 58B", (4, 3, 3, [i % 256 for i in range(58)])),
        response_expected=False,
    ),
    Call(
        "reader_request_page",
        FunctionID.READER_REQUEST_PAGE,
        (DEVICE.ReaderRequest.TYPE4_NDEF, 3),
        sent=("H H", (4, 3)),
    ),
    Call(
        "reader_request_page",
        FunctionID.READER_REQUEST_PAGE,
        (DEVICE.ReaderRequest.TYPE4_NDEF, 3, False),
        sent=("H H", (4, 3)),
        response_expected=False,
    ),
    Call(
        "reader_read_page_low_level",
        FunctionID.READER_READ_PAGE_LOW_LEVEL,
        (),
        reply=("H H 60B", (3, 4, [i % 256 for i in range(60)])),
        result=ReaderReadPage(3, 4, tuple(i % 256 for i in range(60))),
    ),
    Call(
        "cardemu_get_state",
        FunctionID.CARDEMU_GET_STATE,
        (),
        reply=("B !", (195, True)),
        result=CardemuGetState(DEVICE.CardemuState.TRANSFER_NDEF_ERROR, True),
    ),
    Call("cardemu_start_discovery", FunctionID.CARDEMU_START_DISCOVERY, ()),
    Call("cardemu_start_discovery", FunctionID.CARDEMU_START_DISCOVERY, (False,), response_expected=False),
    Call(
        "cardemu_write_ndef_low_level",
        FunctionID.CARDEMU_WRITE_NDEF_LOW_LEVEL,
        (3, 3, [i % 256 for i in range(60)]),
        sent=("H H 60B", (3, 3, [i % 256 for i in range(60)])),
    ),
    Call(
        "cardemu_write_ndef_low_level",
        FunctionID.CARDEMU_WRITE_NDEF_LOW_LEVEL,
        (3, 3, [i % 256 for i in range(60)], False),
        sent=("H H 60B", (3, 3, [i % 256 for i in range(60)])),
        response_expected=False,
    ),
    Call(
        "cardemu_start_transfer", FunctionID.CARDEMU_START_TRANSFER, (DEVICE.CardemuTransfer.WRITE,), sent=("B", (1,))
    ),
    Call(
        "cardemu_start_transfer",
        FunctionID.CARDEMU_START_TRANSFER,
        (DEVICE.CardemuTransfer.WRITE, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call(
        "p2p_get_state",
        FunctionID.P2P_GET_STATE,
        (),
        reply=("B !", (195, True)),
        result=P2PGetState(DEVICE.P2PState.TRANSFER_NDEF_ERROR, True),
    ),
    Call("p2p_start_discovery", FunctionID.P2P_START_DISCOVERY, ()),
    Call("p2p_start_discovery", FunctionID.P2P_START_DISCOVERY, (False,), response_expected=False),
    Call(
        "p2p_write_ndef_low_level",
        FunctionID.P2P_WRITE_NDEF_LOW_LEVEL,
        (3, 3, [i % 256 for i in range(60)]),
        sent=("H H 60B", (3, 3, [i % 256 for i in range(60)])),
    ),
    Call(
        "p2p_write_ndef_low_level",
        FunctionID.P2P_WRITE_NDEF_LOW_LEVEL,
        (3, 3, [i % 256 for i in range(60)], False),
        sent=("H H 60B", (3, 3, [i % 256 for i in range(60)])),
        response_expected=False,
    ),
    Call("p2p_start_transfer", FunctionID.P2P_START_TRANSFER, (DEVICE.P2PTransfer.READ,), sent=("B", (2,))),
    Call(
        "p2p_start_transfer",
        FunctionID.P2P_START_TRANSFER,
        (DEVICE.P2PTransfer.READ, False),
        sent=("B", (2,)),
        response_expected=False,
    ),
    Call(
        "p2p_read_ndef_low_level",
        FunctionID.P2P_READ_NDEF_LOW_LEVEL,
        (),
        reply=("H H 60B", (3, 4, [i % 256 for i in range(60)])),
        result=P2PReadNDEF(3, 4, tuple(i % 256 for i in range(60))),
    ),
    Call(
        "set_detection_led_config",
        FunctionID.SET_DETECTION_LED_CONFIG,
        (DEVICE.DetectionLEDConfig.SHOW_DETECTION,),
        sent=("B", (3,)),
    ),
    Call(
        "set_detection_led_config",
        FunctionID.SET_DETECTION_LED_CONFIG,
        (DEVICE.DetectionLEDConfig.SHOW_DETECTION, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_detection_led_config",
        FunctionID.GET_DETECTION_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.DetectionLEDConfig.SHOW_DETECTION,
    ),
    Call("set_maximum_timeout", FunctionID.SET_MAXIMUM_TIMEOUT, (Decimal("0.003"),), sent=("H", (3,))),
    Call(
        "set_maximum_timeout",
        FunctionID.SET_MAXIMUM_TIMEOUT,
        (Decimal("0.003"), False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call("get_maximum_timeout", FunctionID.GET_MAXIMUM_TIMEOUT, (), reply=("H", (3,)), result=Decimal("0.003")),
    Call(
        "simple_get_tag_id_low_level",
        FunctionID.SIMPLE_GET_TAG_ID_LOW_LEVEL,
        (3,),
        sent=("B", (3,)),
        reply=("B B 10B I", (6, 4, [i % 256 for i in range(10)], 6)),
        result=SimpleGetTagID(DEVICE.TagType.PHONE, 4, tuple(i % 256 for i in range(10)), Decimal("0.006")),
    ),
    Call(
        "cardemu_set_tag_id",
        FunctionID.CARDEMU_SET_TAG_ID,
        (3, [i % 256 for i in range(7)]),
        sent=("B 7B", (3, [i % 256 for i in range(7)])),
    ),
    Call(
        "cardemu_set_tag_id",
        FunctionID.CARDEMU_SET_TAG_ID,
        (3, [i % 256 for i in range(7)], False),
        sent=("B 7B", (3, [i % 256 for i in range(7)])),
        response_expected=False,
    ),
    Call(
        "cardemu_get_tag_id",
        FunctionID.CARDEMU_GET_TAG_ID,
        (),
        reply=("B 7B", (3, [i % 256 for i in range(7)])),
        result=CardemuGetTagID(3, tuple(i % 256 for i in range(7))),
    ),
    Call(
        "set_simple_tag_seen_callback_configuration",
        FunctionID.SET_SIMPLE_TAG_SEEN_CALLBACK_CONFIGURATION,
        (Decimal("0.003"),),
        sent=("I", (3,)),
    ),
    Call(
        "set_simple_tag_seen_callback_configuration",
        FunctionID.SET_SIMPLE_TAG_SEEN_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), False),
        sent=("I", (3,)),
        response_expected=False,
    ),
    Call(
        "get_simple_tag_seen_callback_configuration",
        FunctionID.GET_SIMPLE_TAG_SEEN_CALLBACK_CONFIGURATION,
        (),
        reply=("I", (3,)),
        result=Decimal("0.003"),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_mode", (12345,)),
    ("reader_write_ndef_low_level", (8193, 3, [i % 256 for i in range(60)])),
    ("reader_write_ndef_low_level", (3, 65536, [i % 256 for i in range(60)])),
    ("reader_write_ndef_low_level", (3, 3, ([i % 256 for i in range(60)])[:-1])),
    ("reader_write_ndef", ([1] * 65536,)),
    ("reader_authenticate_mifare_classic_page", (65536, DEVICE.Key.B, [i % 256 for i in range(6)])),
    ("reader_authenticate_mifare_classic_page", (3, 12345, [i % 256 for i in range(6)])),
    ("reader_authenticate_mifare_classic_page", (3, DEVICE.Key.B, ([i % 256 for i in range(6)])[:-1])),
    ("reader_write_page_low_level", (12345, 3, 3, [i % 256 for i in range(58)])),
    ("reader_write_page_low_level", (DEVICE.ReaderWrite.TYPE4_NDEF, 8193, 3, [i % 256 for i in range(58)])),
    ("reader_write_page_low_level", (DEVICE.ReaderWrite.TYPE4_NDEF, 3, 65536, [i % 256 for i in range(58)])),
    ("reader_write_page_low_level", (DEVICE.ReaderWrite.TYPE4_NDEF, 3, 3, ([i % 256 for i in range(58)])[:-1])),
    ("reader_write_page", (DEVICE.ReaderWrite.TYPE4_NDEF, [1] * 65536)),
    ("reader_request_page", (12345, 3)),
    ("reader_request_page", (DEVICE.ReaderRequest.TYPE4_NDEF, 8193)),
    ("cardemu_write_ndef_low_level", (256, 3, [i % 256 for i in range(60)])),
    ("cardemu_write_ndef_low_level", (3, 65536, [i % 256 for i in range(60)])),
    ("cardemu_write_ndef_low_level", (3, 3, ([i % 256 for i in range(60)])[:-1])),
    ("cardemu_write_ndef", ([1] * 65536,)),
    ("cardemu_start_transfer", (12345,)),
    ("p2p_write_ndef_low_level", (256, 3, [i % 256 for i in range(60)])),
    ("p2p_write_ndef_low_level", (3, 65536, [i % 256 for i in range(60)])),
    ("p2p_write_ndef_low_level", (3, 3, ([i % 256 for i in range(60)])[:-1])),
    ("p2p_write_ndef", ([1] * 65536,)),
    ("p2p_start_transfer", (12345,)),
    ("set_detection_led_config", (12345,)),
    ("set_maximum_timeout", (Decimal("65.536"),)),
    ("simple_get_tag_id_low_level", (8,)),
    ("cardemu_set_tag_id", (8, [i % 256 for i in range(7)])),
    ("cardemu_set_tag_id", (3, ([i % 256 for i in range(7)])[:-1])),
    ("set_simple_tag_seen_callback_configuration", (Decimal("4294967.296"),)),
]


def test_identity(device: BrickletNFC) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 286
    assert device.get_api_version() == (2, 0, 4)
    assert str(device).startswith("NFC Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_reader_get_tag_id_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function reader_get_tag_id() uses reader_get_tag_id_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 32):
        connection.reply(FunctionID.READER_GET_TAG_ID_LOW_LEVEL, "B B 32B", *(6, 3, chunk(data, offset, 32, 0)))
    result = run(device.reader_get_tag_id())
    assert connection.requests == [request(FunctionID.READER_GET_TAG_ID_LOW_LEVEL)] * 1
    assert result.tag_id == bytes([i % 256 for i in range(3)])


def test_reader_write_ndef_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function reader_write_ndef() uses reader_write_ndef_low_level()."""
    data = [i % 256 for i in range(3)]
    result = run(device.reader_write_ndef(*(data,)))
    assert connection.requests == [
        request(
            FunctionID.READER_WRITE_NDEF_LOW_LEVEL,
            "H H 60B",
            *(3, offset, chunk([i % 256 for i in range(3)], offset, 60, 0)),
        )
        for offset in range(0, 1, 60)
    ]
    assert result is None


def test_reader_read_ndef_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function reader_read_ndef() uses reader_read_ndef_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 60):
        connection.reply(FunctionID.READER_READ_NDEF_LOW_LEVEL, "H H 60B", *(3, offset, chunk(data, offset, 60, 0)))
    result = run(device.reader_read_ndef())
    assert connection.requests == [request(FunctionID.READER_READ_NDEF_LOW_LEVEL)] * 1
    assert result == bytes([i % 256 for i in range(3)])


def test_reader_write_page_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function reader_write_page() uses reader_write_page_low_level()."""
    data = [i % 256 for i in range(3)]
    result = run(device.reader_write_page(*(DEVICE.ReaderWrite.TYPE4_NDEF, data)))
    assert connection.requests == [
        request(
            FunctionID.READER_WRITE_PAGE_LOW_LEVEL,
            "H H H 58B",
            *(4, 3, offset, chunk([i % 256 for i in range(3)], offset, 58, 0)),
        )
        for offset in range(0, 1, 58)
    ]
    assert result is None


def test_reader_read_page_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function reader_read_page() uses reader_read_page_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 60):
        connection.reply(FunctionID.READER_READ_PAGE_LOW_LEVEL, "H H 60B", *(3, offset, chunk(data, offset, 60, 0)))
    result = run(device.reader_read_page())
    assert connection.requests == [request(FunctionID.READER_READ_PAGE_LOW_LEVEL)] * 1
    assert result == bytes([i % 256 for i in range(3)])


def test_cardemu_write_ndef_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function cardemu_write_ndef() uses cardemu_write_ndef_low_level()."""
    data = [i % 256 for i in range(3)]
    result = run(device.cardemu_write_ndef(*(data,)))
    assert connection.requests == [
        request(
            FunctionID.CARDEMU_WRITE_NDEF_LOW_LEVEL,
            "H H 60B",
            *(3, offset, chunk([i % 256 for i in range(3)], offset, 60, 0)),
        )
        for offset in range(0, 1, 60)
    ]
    assert result is None


def test_p2p_write_ndef_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function p2p_write_ndef() uses p2p_write_ndef_low_level()."""
    data = [i % 256 for i in range(3)]
    result = run(device.p2p_write_ndef(*(data,)))
    assert connection.requests == [
        request(
            FunctionID.P2P_WRITE_NDEF_LOW_LEVEL,
            "H H 60B",
            *(3, offset, chunk([i % 256 for i in range(3)], offset, 60, 0)),
        )
        for offset in range(0, 1, 60)
    ]
    assert result is None


def test_p2p_read_ndef_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function p2p_read_ndef() uses p2p_read_ndef_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 60):
        connection.reply(FunctionID.P2P_READ_NDEF_LOW_LEVEL, "H H 60B", *(3, offset, chunk(data, offset, 60, 0)))
    result = run(device.p2p_read_ndef())
    assert connection.requests == [request(FunctionID.P2P_READ_NDEF_LOW_LEVEL)] * 1
    assert result == bytes([i % 256 for i in range(3)])


def test_simple_get_tag_id_transfers_the_stream(device: BrickletNFC, connection: FakeConnection) -> None:
    """The high-level function simple_get_tag_id() uses simple_get_tag_id_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 10):
        connection.reply(FunctionID.SIMPLE_GET_TAG_ID_LOW_LEVEL, "B B 10B I", *(6, 3, chunk(data, offset, 10, 0), 6))
    result = run(device.simple_get_tag_id(*(3,)))
    assert connection.requests == [request(FunctionID.SIMPLE_GET_TAG_ID_LOW_LEVEL, "B", *(3,))] * 1
    assert result.tag_id == bytes([i % 256 for i in range(3)])


def test_callback_reader_state_changed(device: BrickletNFC, connection: FakeConnection) -> None:
    """The callback READER_STATE_CHANGED is converted to an event."""
    connection.callback(CallbackID.READER_STATE_CHANGED, "B !", *(199, True))
    assert summary(read_events(device)) == [
        (0, CallbackID.READER_STATE_CHANGED, ReaderStateChangedEvent(DEVICE.ReaderState.REQUEST_NDEF_ERROR, True))
    ]


def test_callback_cardemu_state_changed(device: BrickletNFC, connection: FakeConnection) -> None:
    """The callback CARDEMU_STATE_CHANGED is converted to an event."""
    connection.callback(CallbackID.CARDEMU_STATE_CHANGED, "B !", *(195, True))
    assert summary(read_events(device)) == [
        (1, CallbackID.CARDEMU_STATE_CHANGED, CardemuStateChangedEvent(DEVICE.CardemuState.TRANSFER_NDEF_ERROR, True))
    ]


def test_callback_p2p_state_changed(device: BrickletNFC, connection: FakeConnection) -> None:
    """The callback P2P_STATE_CHANGED is converted to an event."""
    connection.callback(CallbackID.P2P_STATE_CHANGED, "B !", *(195, True))
    assert summary(read_events(device)) == [
        (2, CallbackID.P2P_STATE_CHANGED, P2PStateChangedEvent(DEVICE.P2PState.TRANSFER_NDEF_ERROR, True))
    ]


def test_callback_simple_tag_seen(device: BrickletNFC, connection: FakeConnection) -> None:
    """The callback SIMPLE_TAG_SEEN is converted to an event."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 10):
        connection.callback(CallbackID.SIMPLE_TAG_SEEN, "B B 10B", *(6, 3, chunk(data, offset, 10, 0)))
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [(3, CallbackID.SIMPLE_TAG_SEEN)]
    assert events[0].payload.tag_id == bytes([i % 256 for i in range(3)])
