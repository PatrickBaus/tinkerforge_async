"""Tests for the RS232 Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

import asyncio

import pytest

from tinkerforge_async.bricklet_rs232_v2 import (
    BrickletRS232V2,
    GetBufferConfig,
    GetBufferStatus,
    GetConfiguration,
    GetErrorCount,
    Rs232IOError,
)

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, request, run, summary

DEVICE = BrickletRS232V2
FunctionID = BrickletRS232V2.FunctionID
CallbackID = BrickletRS232V2.CallbackID
Parity = BrickletRS232V2.Parity
StopBits = BrickletRS232V2.StopBits
WordLength = BrickletRS232V2.WordLength
FlowControl = BrickletRS232V2.FlowControl

CALLS = [
    Call("set_read_callback", FunctionID.DISABLE_READ_CALLBACK),
    Call("set_read_callback", FunctionID.ENABLE_READ_CALLBACK, (True, False), response_expected=False),
    Call("is_read_callback_enabled", FunctionID.IS_READ_CALLBACK_ENABLED, reply=("!", (True,)), result=True),
    Call("set_configuration", FunctionID.SET_CONFIGURATION, sent=("I B B B B", (115200, 0, 1, 8, 0))),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (100, Parity.EVEN, StopBits.TWO, WordLength.LENGTH_5, FlowControl.HARDWARE),
        sent=("I B B B B", (100, 2, 2, 5, 2)),
    ),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (2000000, 1, 1, 7, 1),
        sent=("I B B B B", (2000000, 1, 1, 7, 1)),
    ),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        reply=("I B B B B", (9600, 1, 2, 7, 1)),
        result=GetConfiguration(9600, Parity.ODD, StopBits.TWO, WordLength.LENGTH_7, FlowControl.SOFTWARE),
    ),
    Call("set_buffer_config", FunctionID.SET_BUFFER_CONFIG, sent=("H H", (5120, 5120))),
    Call("set_buffer_config", FunctionID.SET_BUFFER_CONFIG, (1024, 9216), sent=("H H", (1024, 9216))),
    Call(
        "get_buffer_config",
        FunctionID.GET_BUFFER_CONFIG,
        reply=("H H", (1024, 9216)),
        result=GetBufferConfig(1024, 9216),
    ),
    Call("get_buffer_status", FunctionID.GET_BUFFER_STATUS, reply=("H H", (10, 20)), result=GetBufferStatus(10, 20)),
    Call("get_error_count", FunctionID.GET_ERROR_COUNT, reply=("I I", (1, 2)), result=GetErrorCount(1, 2)),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        sent=("H", (0,)),
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (9216,),
        sent=("H", (9216,)),
    ),
    Call(
        "get_frame_readable_callback_configuration",
        FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        reply=("H", (16,)),
        result=16,
    ),
]

REJECTED = [
    ("set_configuration", (99,)),
    ("set_configuration", (2000001,)),
    ("set_configuration", (9600, 3)),
    ("set_configuration", (9600, 0, 3)),
    ("set_configuration", (9600, 0, 1, 9)),
    ("set_configuration", (9600, 0, 1, 8, 3)),
    ("set_buffer_config", (1023, 1024)),
    ("set_buffer_config", (9217, 1024)),
    ("set_buffer_config", (1024, 1023)),
    ("set_buffer_config", (1024, 9217)),
    ("set_buffer_config", (5120, 5121)),
    ("set_frame_readable_callback_configuration", (-1,)),
    ("set_frame_readable_callback_configuration", (9217,)),
]


def chunk(data: bytes) -> tuple[int, ...]:
    """The data of a packet. It always has 60 bytes."""
    return tuple(data.ljust(60, b"\0"))


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2108
    assert bricklet.get_api_version() == (2, 0, 1)
    assert str(bricklet).startswith("RS232 Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_empty_messages_are_not_requested(bricklet, connection):
    """There is nothing to read or to write."""
    assert run(bricklet.read(0)) == b""
    assert run(bricklet.write(b"")) == 0
    assert not connection.requests


def test_write_short_message(bricklet, connection):
    """A message is padded to 60 bytes. A string is encoded as UTF-8."""
    connection.reply(FunctionID.WRITE_LOW_LEVEL, "B", 7)
    assert run(bricklet.write("Grüße")) == 7
    message = "Grüße".encode()
    assert connection.requests == [request(FunctionID.WRITE_LOW_LEVEL, "H H 60B", 7, 0, chunk(message))]


def test_write_long_message(bricklet, connection):
    """A message is sent in chunks of 60 bytes. Each chunk has the length of the message and its offset."""
    message = bytes(range(130))
    for written in (60, 60, 10):
        connection.reply(FunctionID.WRITE_LOW_LEVEL, "B", written)
    assert run(bricklet.write(message)) == 130
    assert connection.requests == [
        request(FunctionID.WRITE_LOW_LEVEL, "H H 60B", 130, 0, chunk(message[:60])),
        request(FunctionID.WRITE_LOW_LEVEL, "H H 60B", 130, 60, chunk(message[60:120])),
        request(FunctionID.WRITE_LOW_LEVEL, "H H 60B", 130, 120, chunk(message[120:])),
    ]


def test_write_fails_if_the_bricklet_does_not_take_all_bytes(bricklet, connection):
    """The send buffer of the Bricklet is full."""
    connection.reply(FunctionID.WRITE_LOW_LEVEL, "B", 3)
    with pytest.raises(Rs232IOError, match="3 bytes written out of 5 bytes"):
        run(bricklet.write(b"hello"))


def test_write_rejects_a_message_that_is_too_long(bricklet, connection):
    """The length of the message is transferred as a 16 bit integer."""
    with pytest.raises(RuntimeError):
        run(bricklet.write(bytes(65536)))
    assert not connection.requests


def test_read_short_message(bricklet, connection):
    """Only the bytes of the message are returned, not the padding."""
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 5, 0, chunk(b"hello"))
    assert run(bricklet.read(5)) == b"hello"
    assert connection.requests == [request(FunctionID.READ_LOW_LEVEL, "H", 5)]


def test_read_long_message(bricklet, connection):
    """The chunks of the message are requested one by one."""
    message = bytes(range(130))
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 130, 0, chunk(message[:60]))
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 130, 60, chunk(message[60:120]))
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 130, 120, chunk(message[120:]))
    assert run(bricklet.read(130)) == message
    assert connection.requests == [request(FunctionID.READ_LOW_LEVEL, "H", 130)] * 3


def test_read_returns_less_if_the_buffer_is_empty(bricklet, connection):
    """An empty chunk with the offset 0 ends the message."""
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 60, 0, chunk(bytes(range(60))))
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 0, 0, chunk(b""))
    assert run(bricklet.read(180)) == bytes(range(60))
    assert len(connection.requests) == 2


def test_read_skips_the_rest_of_an_unfinished_message(bricklet, connection):
    """If another reader did not finish its message, its chunks are dropped until a new message starts."""
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 130, 60, chunk(b"old"))
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 130, 120, chunk(b"old"))
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 5, 0, chunk(b"hello"))
    assert run(bricklet.read(5)) == b"hello"
    assert len(connection.requests) == 3


def test_read_fails_if_a_chunk_is_missing(bricklet, connection):
    """The offset of a chunk must be the number of bytes that were read so far."""
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 180, 0, chunk(bytes(60)))
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 180, 120, chunk(bytes(60)))
    with pytest.raises(Rs232IOError, match="Wanted chunk 1, got chunk 2"):
        run(bricklet.read(180))


def test_read_and_write_do_not_interleave(bricklet, connection):
    """A message must be finished, before the next one is started. The calls are serialized by a lock."""
    connection.reply(FunctionID.WRITE_LOW_LEVEL, "B", 60)
    connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60B", 5, 0, chunk(b"hello"))

    async def scenario():
        return await asyncio.gather(bricklet.write(bytes(120)), bricklet.write(bytes([1]) * 120), bricklet.read(5))

    assert run(scenario()) == [120, 120, b"hello"]
    # The offset of the chunk and the first byte of its data
    assert [(sent.data[2], sent.data[4]) for sent in connection.requests[:4]] == [(0, 0), (60, 0), (0, 1), (60, 1)]
    assert connection.requests[4] == request(FunctionID.READ_LOW_LEVEL, "H", 5)


def test_read_events_reassemble_the_message(bricklet, connection):
    """The read callback delivers a message in chunks. One event with the whole message is yielded."""
    message = bytes(range(130))
    connection.callback(CallbackID.READ, "H H 60B", 130, 0, chunk(message[:60]))
    connection.callback(CallbackID.READ, "H H 60B", 130, 60, chunk(message[60:120]))
    connection.callback(CallbackID.READ, "H H 60B", 130, 120, chunk(message[120:]))
    connection.callback(CallbackID.READ, "H H 60B", 5, 0, chunk(b"hello"))
    assert summary(read_events(bricklet)) == [(0, CallbackID.READ, message), (0, CallbackID.READ, b"hello")]


def test_other_events(bricklet, connection):
    """The error counters and the number of readable frames are passed on."""
    connection.callback(CallbackID.ERROR_COUNT, "I I", 1, 2)
    connection.callback(CallbackID.FRAME_READABLE, "H", 3)
    assert summary(read_events(bricklet)) == [(1, CallbackID.ERROR_COUNT, [1, 2]), (1, CallbackID.FRAME_READABLE, 3)]
