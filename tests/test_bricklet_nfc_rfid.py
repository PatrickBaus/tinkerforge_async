"""Tests for the NFC/RFID Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_nfc_rfid import BrickletNFCRFID, GetState, GetTagID, StateChangedEvent
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletNFCRFID
FunctionID = BrickletNFCRFID.FunctionID
CallbackID = BrickletNFCRFID.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "REQUEST_TAG_ID": 1,
    "GET_TAG_ID": 2,
    "GET_STATE": 3,
    "AUTHENTICATE_MIFARE_CLASSIC_PAGE": 4,
    "WRITE_PAGE": 5,
    "REQUEST_PAGE": 6,
    "GET_PAGE": 7,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"STATE_CHANGED": 8}

CALLS: list[Call] = [
    Call("request_tag_id", FunctionID.REQUEST_TAG_ID, (DEVICE.TagType.TYPE2,), sent=("B", (2,))),
    Call(
        "request_tag_id",
        FunctionID.REQUEST_TAG_ID,
        (DEVICE.TagType.TYPE2, False),
        sent=("B", (2,)),
        response_expected=False,
    ),
    Call(
        "get_tag_id",
        FunctionID.GET_TAG_ID,
        (),
        reply=("B B 7B", (2, 4, [i % 256 for i in range(7)])),
        result=GetTagID(DEVICE.TagType.TYPE2, 4, tuple(i % 256 for i in range(7))),
    ),
    Call(
        "get_state",
        FunctionID.GET_STATE,
        (),
        reply=("B !", (197, True)),
        result=GetState(DEVICE.State.REQUEST_PAGE_ERROR, True),
    ),
    Call(
        "authenticate_mifare_classic_page",
        FunctionID.AUTHENTICATE_MIFARE_CLASSIC_PAGE,
        (3, DEVICE.Key.B, [i % 256 for i in range(6)]),
        sent=("H B 6B", (3, 1, [i % 256 for i in range(6)])),
    ),
    Call(
        "authenticate_mifare_classic_page",
        FunctionID.AUTHENTICATE_MIFARE_CLASSIC_PAGE,
        (3, DEVICE.Key.B, [i % 256 for i in range(6)], False),
        sent=("H B 6B", (3, 1, [i % 256 for i in range(6)])),
        response_expected=False,
    ),
    Call(
        "write_page",
        FunctionID.WRITE_PAGE,
        (3, [i % 256 for i in range(16)]),
        sent=("H 16B", (3, [i % 256 for i in range(16)])),
    ),
    Call(
        "write_page",
        FunctionID.WRITE_PAGE,
        (3, [i % 256 for i in range(16)], False),
        sent=("H 16B", (3, [i % 256 for i in range(16)])),
        response_expected=False,
    ),
    Call("request_page", FunctionID.REQUEST_PAGE, (3,), sent=("H", (3,))),
    Call("request_page", FunctionID.REQUEST_PAGE, (3, False), sent=("H", (3,)), response_expected=False),
    Call(
        "get_page",
        FunctionID.GET_PAGE,
        (),
        reply=("16B", ([i % 256 for i in range(16)],)),
        result=tuple(i % 256 for i in range(16)),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("request_tag_id", (12345,)),
    ("authenticate_mifare_classic_page", (65536, DEVICE.Key.B, [i % 256 for i in range(6)])),
    ("authenticate_mifare_classic_page", (3, 12345, [i % 256 for i in range(6)])),
    ("authenticate_mifare_classic_page", (3, DEVICE.Key.B, ([i % 256 for i in range(6)])[:-1])),
    ("write_page", (65536, [i % 256 for i in range(16)])),
    ("write_page", (3, ([i % 256 for i in range(16)])[:-1])),
    ("request_page", (65536,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 246
    assert device.get_api_version() == (2, 0, 0)
    assert str(device).startswith("NFC/RFID Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_callback_state_changed(device, connection):
    """The callback STATE_CHANGED is converted to an event."""
    connection.callback(CallbackID.STATE_CHANGED, "B !", *(197, True))
    assert summary(read_events(device)) == [
        (0, CallbackID.STATE_CHANGED, StateChangedEvent(DEVICE.State.REQUEST_PAGE_ERROR, True))
    ]
