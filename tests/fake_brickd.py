"""A fake Brick Daemon for the tests of the IP connection. It speaks the Tinkerforge TCP/IP protocol on a local port."""

from __future__ import annotations

import asyncio
import struct
from collections.abc import Callable
from types import TracebackType
from typing import NamedTuple, Self

HEADER = "<IBBBB"  # uid, packet size, function id, sequence number and options, flags
HEADER_SIZE = struct.calcsize(HEADER)


class Packet(NamedTuple):
    """A packet of the Tinkerforge TCP/IP protocol."""

    uid: int
    function_id: int
    sequence_number: int
    response_expected: bool
    payload: bytes = b""
    flags: int = 0

    def pack(self) -> bytes:
        """The packet as it is sent over the wire."""
        options = self.sequence_number << 4 | self.response_expected << 3
        header = struct.pack(HEADER, self.uid, HEADER_SIZE + len(self.payload), self.function_id, options, self.flags)
        return header + self.payload


def callback(uid: int, function_id: int, payload: bytes = b"") -> Packet:
    """A packet that was not requested. Callbacks have the sequence number 0."""
    return Packet(uid, function_id, 0, False, payload)


def reply(request: Packet, payload: bytes = b"", flags: int = 0) -> Packet:
    """The reply to a request."""
    return request._replace(payload=payload, flags=flags)


class FakeBrickd:
    """
    A server that records the packets it receives in `received`. If a `responder` is given, it is called with every
    packet and returns the reply, or `None` if the packet is not answered.
    """

    def __init__(self, responder: Callable[[Packet], Packet | bytes | None] | None = None) -> None:
        self.received: list[Packet] = []
        self.connections = 0
        self.__responder = responder
        self.__server: asyncio.Server | None = None
        self.__writers: list[asyncio.StreamWriter] = []
        self.__changed = asyncio.Condition()

    @property
    def port(self) -> int:
        """The port the server listens on. It is chosen by the operating system."""
        assert self.__server is not None
        return self.__server.sockets[0].getsockname()[1]

    async def __aenter__(self) -> Self:
        self.__server = await asyncio.start_server(self.__serve, "127.0.0.1", 0)
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc: BaseException | None, traceback: TracebackType | None
    ) -> None:
        assert self.__server is not None
        self.__server.close()
        self.drop_clients()
        await self.__server.wait_closed()

    async def __serve(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        self.__writers.append(writer)
        async with self.__changed:
            self.connections += 1
            self.__changed.notify_all()
        try:
            while True:
                header = await reader.readexactly(HEADER_SIZE)
                uid, size, function_id, options, flags = struct.unpack(HEADER, header)
                payload = await reader.readexactly(size - HEADER_SIZE)
                packet = Packet(uid, function_id, options >> 4, bool(options >> 3 & 1), payload, flags)
                async with self.__changed:
                    self.received.append(packet)
                    self.__changed.notify_all()
                answer = None if self.__responder is None else self.__responder(packet)
                if answer is not None:
                    writer.write(answer if isinstance(answer, bytes) else answer.pack())
        except (asyncio.IncompleteReadError, ConnectionError):
            pass  # The client has closed the connection
        finally:
            writer.close()

    def send(self, *packets: Packet | bytes) -> None:
        """Send packets to all clients. They are written at once, so the clients read them in one go."""
        data = b"".join(packet if isinstance(packet, bytes) else packet.pack() for packet in packets)
        for writer in self.__writers:
            writer.write(data)

    def drop_clients(self) -> None:
        """Close the connections to all clients, like a Brick Daemon that is shut down."""
        for writer in self.__writers:
            writer.close()
        self.__writers.clear()

    async def wait_for_packets(self, count: int) -> list[Packet]:
        """Wait until a number of packets has been received."""
        async with asyncio.timeout(5):
            async with self.__changed:
                await self.__changed.wait_for(lambda: len(self.received) >= count)
        return self.received

    async def wait_for_connections(self, count: int) -> None:
        """Wait until a number of clients has connected."""
        async with asyncio.timeout(5):
            async with self.__changed:
                await self.__changed.wait_for(lambda: self.connections >= count)
