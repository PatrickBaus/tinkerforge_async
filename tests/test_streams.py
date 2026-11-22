"""Tests for the helpers of the high-level functions, that transfer streams in chunks."""

import pytest

from tinkerforge_async.streams import (
    Chunk,
    StreamAssembler,
    StreamOutOfSyncError,
    pad_single_chunk,
    read_stream,
    write_stream,
    write_stream_short,
)

from .fake_connection import run


class Recorder:  # pylint: disable=too-few-public-methods
    """A low-level write function, that records the chunks and returns a result."""

    def __init__(self, written=None):
        self.chunks = []
        self.written = written  # The number of items, that the device accepts per chunk

    async def __call__(self, length, offset, chunk):
        self.chunks.append((length, offset, chunk))
        if self.written is None:
            return f"result {len(self.chunks)}"
        return min(self.written, length - offset), f"result {len(self.chunks)}"


def test_write_splits_the_data_into_padded_chunks():
    """The last chunk is padded, and the result of the last chunk is returned."""
    send = Recorder()
    result = run(write_stream(send, [1, 2, 3, 4, 5], name="data", chunk_size=2, padding=0, max_length=10))
    assert send.chunks == [(5, 0, [1, 2]), (5, 2, [3, 4]), (5, 4, [5, 0])]
    assert result == "result 3"


def test_write_of_an_empty_stream_sends_one_chunk():
    """An empty stream is sent as a single padded chunk with length 0."""
    send = Recorder()
    run(write_stream(send, "", name="data", chunk_size=3, padding="\0"))
    assert send.chunks == [(0, 0, ["\0", "\0", "\0"])]


def test_write_rejects_invalid_lengths():
    """Too long streams and streams that do not have the fixed length are rejected before anything is sent."""
    send = Recorder()
    with pytest.raises(ValueError):
        run(write_stream(send, [1, 2, 3], name="data", chunk_size=2, padding=0, max_length=2))
    with pytest.raises(ValueError):
        run(write_stream(send, [1, 2, 3], name="data", chunk_size=2, padding=0, fixed_length=4))
    assert not send.chunks
    run(write_stream(send, [1, 2, 3, 4], name="data", chunk_size=2, padding=0, fixed_length=4))
    assert len(send.chunks) == 2


def test_short_write_stops_at_the_first_incomplete_chunk():
    """The device accepts less than a chunk, so the rest of the data is not sent."""
    send = Recorder(written=1)
    written, result = run(write_stream_short(send, "abcde", name="data", chunk_size=2, padding="\0", max_length=10))
    assert written == 1
    assert result == "result 1"
    assert send.chunks == [(5, 0, ["a", "b"])]


def test_short_write_of_a_complete_stream():
    """All chunks are accepted. The written items of all chunks are added."""
    send = Recorder(written=2)
    written, _ = run(write_stream_short(send, "abcd", name="data", chunk_size=2, padding="\0"))
    assert written == 4
    assert len(send.chunks) == 2
    send = Recorder(written=2)
    assert run(write_stream_short(send, "", name="data", chunk_size=2, padding="\0")) == (0, "result 1")
    with pytest.raises(ValueError):
        run(write_stream_short(send, "abc", name="data", chunk_size=2, padding="\0", max_length=2))


def test_pad_single_chunk():
    """A single chunk is padded to its size, and longer data is rejected."""
    assert pad_single_chunk([1, 2], name="data", chunk_size=4, padding=0) == [1, 2, 0, 0]
    with pytest.raises(ValueError):
        pad_single_chunk([1, 2, 3], name="data", chunk_size=2, padding=0)


def reader(chunks):
    """A low-level read function, that returns the given chunks one after another."""
    replies = iter(chunks)

    async def read_chunk():
        return next(replies)

    return read_chunk


def test_read_assembles_the_chunks():
    """The chunks are concatenated and the padding of the last chunk is removed."""
    chunks = [Chunk(5, 0, [1, 2], "first"), Chunk(5, 2, [3, 4], "second"), Chunk(5, 4, [5, 0], "last")]
    assert run(read_stream(reader(chunks), name="data", chunk_size=2)) == ([1, 2, 3, 4, 5], "last")


def test_read_of_an_empty_fixed_length_stream():
    """Streams with a fixed length signal that there is no data with the maximum chunk offset."""
    chunks = [Chunk(4, 0xFFFF, [0, 0], "empty")]
    assert run(read_stream(reader(chunks), name="data", chunk_size=2, empty_offset=0xFFFF)) == ([], "empty")


def test_read_out_of_sync_drops_the_rest_of_the_stream():
    """A chunk at the wrong offset raises an error, after the rest of the stream was read."""
    chunks = [Chunk(6, 0, [1, 2], None), Chunk(6, 4, [5, 6], None)]
    with pytest.raises(StreamOutOfSyncError):
        run(read_stream(reader(chunks), name="data", chunk_size=2))

    # The stream did not start at offset 0. The remaining chunks of the stream are read and dropped.
    chunks = [Chunk(6, 2, [3, 4], None), Chunk(6, 4, [5, 6], None), Chunk(6, 0, [1, 2], None)]
    read_chunk = reader(chunks)
    with pytest.raises(StreamOutOfSyncError):
        run(read_stream(read_chunk, name="data", chunk_size=2))
    assert run(read_chunk()) == Chunk(6, 0, [1, 2], None)  # The next stream starts in sync


def test_assembler():
    """The assembler returns the data once the stream is complete."""
    assembler = StreamAssembler()
    assert assembler.add(3, 0, [1, 2]) is None
    assert assembler.add(3, 2, [3, 0]) == [1, 2, 3]
    # A single chunk stream
    assert assembler.add(1, 0, [7, 0]) == [7]


def test_assembler_drops_streams_that_are_out_of_sync():
    """Chunks without the start of the stream are ignored, and a gap drops the stream."""
    assembler = StreamAssembler()
    assert assembler.add(4, 2, [3, 4]) is None  # The start is missing
    assert assembler.add(6, 0, [1, 2]) is None
    assert assembler.add(6, 4, [5, 6]) is None  # The chunk at offset 2 is missing
    assert assembler.add(6, 2, [3, 4]) is None  # Not the start of a new stream either
    assert assembler.add(2, 0, [8, 9]) == [8, 9]
