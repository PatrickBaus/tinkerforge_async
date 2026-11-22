"""
Helpers for the high-level functions and callbacks of Bricks and Bricklets, that transfer data, which does not fit into
a single packet. The data is split into chunks, that are transferred by the low-level functions or callbacks. These
helpers implement the same rules as the official Tinkerforge bindings.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Sequence
from typing import Any, NamedTuple


class StreamOutOfSyncError(Exception):
    """
    Raised when the chunks of a stream, that is read from a device, do not fit together. This happens if two readers
    request the same stream at the same time. The remaining chunks are dropped, so the next read works again.
    """


def _chunk(data: Sequence[Any], offset: int, size: int, padding: Any) -> list[Any]:
    chunk = list(data[offset : offset + size])
    if len(chunk) < size:
        chunk += [padding] * (size - len(chunk))
    return chunk


async def write_stream(  # pylint: disable=too-many-arguments
    send_chunk: Callable[[int, int, list[Any]], Awaitable[Any]],
    data: Sequence[Any],
    *,
    name: str,
    chunk_size: int,
    padding: Any,
    max_length: int | None = None,
    fixed_length: int | None = None,
) -> Any:
    """
    Write the `data` in chunks.

    Parameters
    ----------
    send_chunk: Callable
        The low-level function. It is called with the total length of the stream, the offset of the chunk and the
        chunk, that is padded to `chunk_size`.
    data: Sequence
        The data to send.
    name: str
        The name of the stream used in error messages.
    chunk_size: int
        The number of items per chunk.
    padding: Any
        The value that is used to fill the last chunk.
    max_length: int, optional
        The maximum length of the stream.
    fixed_length: int, optional
        The length of the stream if it has a fixed length.

    Returns
    -------
    Any
        The result of the last call of `send_chunk`.

    Raises
    ------
    ValueError
        If the data is too long or does not have the fixed length.
    """
    length = len(data)
    if fixed_length is not None and length != fixed_length:
        raise ValueError(f"Invalid argument: {name} must be exactly {fixed_length} items long, got {length} items")
    if max_length is not None and length > max_length:
        raise ValueError(f"Invalid argument: {name} can be at most {max_length} items long, got {length} items")

    if length == 0:
        return await send_chunk(0, 0, [padding] * chunk_size)

    result = None
    for offset in range(0, length, chunk_size):
        result = await send_chunk(length, offset, _chunk(data, offset, chunk_size, padding))
    return result


async def write_stream_short(  # pylint: disable=too-many-arguments
    send_chunk: Callable[[int, int, list[Any]], Awaitable[tuple[int, Any]]],
    data: Sequence[Any],
    *,
    name: str,
    chunk_size: int,
    padding: Any,
    max_length: int | None = None,
) -> tuple[int, Any]:
    """
    Write the `data` in chunks to a device, that may accept less items than sent ("short write"), e.g. because its
    buffer is full. The transfer stops at the first chunk, that was not written completely.

    `send_chunk` must return the number of items written and the result of the low-level function.

    Returns
    -------
    tuple of int and Any
        The total number of items written and the result of the last call of `send_chunk`.
    """
    length = len(data)
    if max_length is not None and length > max_length:
        raise ValueError(f"Invalid argument: {name} can be at most {max_length} items long, got {length} items")

    if length == 0:
        return await send_chunk(0, 0, [padding] * chunk_size)

    written = 0
    result = None
    for offset in range(0, length, chunk_size):
        chunk_written, result = await send_chunk(length, offset, _chunk(data, offset, chunk_size, padding))
        written += chunk_written
        if chunk_written < chunk_size:
            break  # Either the last chunk or a short write
    return written, result


def pad_single_chunk(data: Sequence[Any], *, name: str, chunk_size: int, padding: Any) -> list[Any]:
    """
    Pad the data of a stream, that is sent as a single chunk.

    Raises
    ------
    ValueError
        If the data does not fit into a single chunk.
    """
    if len(data) > chunk_size:
        raise ValueError(f"Invalid argument: {name} can be at most {chunk_size} items long, got {len(data)} items")
    return _chunk(data, 0, chunk_size, padding)


class Chunk(NamedTuple):
    """A chunk of a stream as it is returned by a low-level function, together with the other values of the reply."""

    length: int
    offset: int
    data: Sequence[Any]
    result: Any


async def read_stream(
    read_chunk: Callable[[], Awaitable[Chunk]],
    *,
    name: str,
    chunk_size: int,
    empty_offset: int | None = None,
) -> tuple[list[Any], Any]:
    """
    Read a stream from a device.

    Parameters
    ----------
    read_chunk: Callable
        The low-level function. It returns the next chunk. Streams with a fixed length return the fixed length.
    name: str
        The name of the stream used in error messages.
    chunk_size: int
        The number of items per chunk.
    empty_offset: int, optional
        Streams with a fixed length signal, that there is no data, with this chunk offset.

    Returns
    -------
    tuple of list and Any
        The data and the result of the last call of `read_chunk`.

    Raises
    ------
    StreamOutOfSyncError
        If the chunks do not fit together.
    """
    chunk = await read_chunk()
    if empty_offset is not None and chunk.offset == empty_offset:
        return [], chunk.result
    out_of_sync = chunk.offset != 0
    data = list(chunk.data)
    length = chunk.length

    while not out_of_sync and len(data) < length:
        chunk = await read_chunk()
        length = chunk.length
        out_of_sync = chunk.offset != len(data)
        data += chunk.data

    if out_of_sync:
        # Discard the rest of the stream to bring it back in sync
        while chunk.offset + chunk_size < chunk.length:
            chunk = await read_chunk()
        raise StreamOutOfSyncError(f"The {name} stream is out of sync")

    return data[:length], chunk.result


class StreamAssembler:  # pylint: disable=too-few-public-methods
    """
    Reassembles the chunks of a stream, that is sent by a callback.
    """

    def __init__(self) -> None:
        self.__data: list[Any] | None = None

    def add(self, length: int, offset: int, chunk: Sequence[Any]) -> list[Any] | None:
        """
        Add a chunk.

        Returns
        -------
        list or None
            The data of the stream, if it is complete, otherwise `None`. Chunks that do not fit to the stream are
            dropped together with the incomplete stream.
        """
        if self.__data is None:
            if offset != 0:
                return None  # The tail of a stream, that we did not see the start of. Wait for the next stream.
            self.__data = list(chunk)
        elif offset != len(self.__data):
            self.__data = None  # Out of sync, drop the stream
            return None
        else:
            self.__data += chunk

        if len(self.__data) >= length:
            data, self.__data = self.__data[:length], None
            return data
        return None
