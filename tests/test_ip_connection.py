"""Tests for the IP connection. They talk to a fake Brick Daemon on a local port."""

# pylint: disable=too-many-lines
import asyncio
import errno
import hashlib
import hmac
import logging
import socket
import struct
from collections.abc import Callable
from decimal import Decimal
from types import SimpleNamespace
from typing import Any, cast

import pytest

from tinkerforge_async import IPConnectionAsync
from tinkerforge_async.brick_master import BrickMaster
from tinkerforge_async.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge_async.devices import Device, Event
from tinkerforge_async.ip_connection import (
    DEFAULT_WAIT_TIMEOUT,
    EnumerationType,
    Flags,
    FunctionID,
    HeaderPayload,
    NetworkUnreachableError,
    NotConnectedError,
)
from tinkerforge_async.ip_connection_helper import pack_payload

from .fake_brickd import FakeBrickd, Packet, callback, reply
from .fake_connection import run, take

HOST = "127.0.0.1"
UID = 12345  # "4ER" in base58
# A stand-in for a device. The connection only needs its uid.
DEVICE = cast(Device, SimpleNamespace(uid=UID))
GET_TEMPERATURE = BrickletTemperatureV2.FunctionID.GET_TEMPERATURE
TEMPERATURE = BrickletTemperatureV2.CallbackID.TEMPERATURE
LOGGER = "tinkerforge_async.ip_connection"
ENUMERATION = "8s 8s c 3B 3B H B"


def answer_with(payload: bytes = b"", flags: int = 0) -> Callable[[Packet], Packet | None]:
    """A Brick Daemon that answers every request, that expects a response, with the same payload."""
    return lambda request: reply(request, payload, flags) if request.response_expected else None


async def until(condition: Callable[[], object]) -> None:
    """Wait until a condition is met, that is fulfilled by a task in the background."""
    async with asyncio.timeout(5):
        while not condition():
            await asyncio.sleep(0.001)


async def registered() -> None:
    """Give the tasks, that were just created, the time to register as a listener."""
    for _ in range(5):
        await asyncio.sleep(0)


def enumeration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
    enumeration_type: int, uid: bytes = b"4ER", connected_uid: bytes = b"21", position: str = "a", device: int = 2113
) -> Packet:
    """The callback, that a device sends when it is enumerated."""
    payload = pack_payload((uid, connected_uid, position, (1, 0, 0), (2, 0, 1), device, enumeration_type), ENUMERATION)
    return callback(int.from_bytes(b"\x39\x30\x00\x00", "little"), FunctionID.CALLBACK_ENUMERATE.value, payload)


def free_port() -> int:
    """A port that nobody listens on."""
    with socket.socket() as sock:
        sock.bind((HOST, 0))
        return cast(int, sock.getsockname()[1])


# ----------------------------------------------------------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------------------------------------------------------
def test_properties() -> None:
    """The parameters of the connection can be read."""
    connection = IPConnectionAsync("localhost", 1234, timeout=3)
    assert connection.uid == 1
    assert connection.hostname == "localhost"
    assert connection.port == 1234
    assert connection.timeout == 3
    assert not connection.is_connected
    assert str(connection) == "IPConnectionAsync(localhost:1234)"
    assert repr(connection) == (
        "tinkerforge_async.ip_connection.IPConnectionAsync(host=localhost, port=1234, authentication_secret=None)"
    )


def test_defaults() -> None:
    """The host must be given before connecting. The port is the port of the Brick Daemon."""
    connection = IPConnectionAsync()
    assert connection.hostname is None
    assert connection.port == 4223
    assert connection.timeout == DEFAULT_WAIT_TIMEOUT == 2.5


def test_the_authentication_secret_is_not_printed() -> None:
    """The representation is written to logs."""
    connection = IPConnectionAsync("localhost", authentication_secret="top secret")
    assert "top secret" not in repr(connection)
    assert "authentication_secret=*****" in repr(connection)
    assert "top secret" not in str(connection)


def test_timeout() -> None:
    """The timeout is a positive number of seconds, or `None` to wait forever."""
    connection = IPConnectionAsync(timeout=0)
    assert connection.timeout == 0
    connection.timeout = 5
    assert connection.timeout == 5.0
    assert isinstance(connection.timeout, float)
    connection.timeout = -1.5
    assert connection.timeout == 1.5
    connection.timeout = None
    assert connection.timeout is None


# ----------------------------------------------------------------------------------------------------------------------
# Connecting and disconnecting
# ----------------------------------------------------------------------------------------------------------------------
def test_connect_and_disconnect() -> None:
    """Connecting twice, or disconnecting twice does no harm."""

    async def scenario() -> int:
        async with FakeBrickd() as brickd:
            connection = IPConnectionAsync(HOST, brickd.port)
            await connection.disconnect()  # It is not connected yet
            assert not connection.is_connected

            await connection.connect()
            assert connection.is_connected
            await connection.connect()
            await brickd.wait_for_connections(1)

            await connection.disconnect()
            assert not connection.is_connected
            await connection.disconnect()
            return brickd.connections

    assert run(scenario()) == 1


def test_context_manager() -> None:
    """The connection is open within the context."""

    async def scenario() -> bool:
        async with FakeBrickd() as brickd:
            async with IPConnectionAsync(HOST, brickd.port) as connection:
                assert isinstance(connection, IPConnectionAsync)
                assert connection.is_connected
            return connection.is_connected

    assert run(scenario()) is False


def test_host_and_port_can_be_given_when_connecting() -> None:
    """They replace the parameters, that were given when the connection was created."""

    async def scenario() -> None:
        async with FakeBrickd() as brickd:
            connection = IPConnectionAsync("unknown.invalid", 1)
            await connection.connect(HOST, brickd.port)
            assert connection.is_connected
            assert (connection.hostname, connection.port) == (HOST, brickd.port)
            await connection.disconnect()

            # They are kept for the next connection attempt
            await connection.connect()
            assert connection.is_connected
            await connection.disconnect()

    run(scenario())


def test_connecting_without_host_fails() -> None:
    """There is no default for the host."""
    with pytest.raises(TypeError, match="Invalid hostname"):
        run(IPConnectionAsync().connect())
    with pytest.raises(TypeError, match="Invalid hostname"):
        run(IPConnectionAsync().connect(port=4223))


def test_connection_refused() -> None:
    """Nobody listens on the port."""
    connection = IPConnectionAsync(HOST, free_port())
    with pytest.raises(ConnectionRefusedError, match=f"Connection refused by host '{HOST}:{connection.port}'"):
        run(connection.connect())
    assert not connection.is_connected


@pytest.mark.parametrize("error_number", [errno.ENETUNREACH, errno.EHOSTUNREACH])
def test_network_unreachable(monkeypatch: pytest.MonkeyPatch, error_number: int) -> None:
    """There is no route to the host."""

    async def unreachable(*_args: object) -> None:
        raise OSError(error_number, "unreachable")

    monkeypatch.setattr(asyncio, "open_connection", unreachable)
    with pytest.raises(NetworkUnreachableError, match="The network for host 'host:4223' is unreachable"):
        run(IPConnectionAsync("host").connect())


def test_other_errors_of_the_operating_system_are_passed_on(monkeypatch: pytest.MonkeyPatch) -> None:
    """Only the common errors are translated."""

    async def forbidden(*_args: object) -> None:
        raise OSError(errno.EACCES, "forbidden")

    monkeypatch.setattr(asyncio, "open_connection", forbidden)
    with pytest.raises(PermissionError, match="forbidden"):
        run(IPConnectionAsync("host").connect())


def test_connection_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    """The host does not answer in time."""

    async def hang(*_args: object) -> None:
        await asyncio.Event().wait()

    monkeypatch.setattr(asyncio, "open_connection", hang)
    connection = IPConnectionAsync("host", timeout=0.01)
    with pytest.raises(TimeoutError, match="Timeout during connection attempt to 'host:4223'"):
        run(connection.connect())
    assert not connection.is_connected


def test_disconnect_cancels_a_connection_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    """A connection attempt, that is still running, is aborted."""

    async def hang(*_args: object) -> None:
        await asyncio.Event().wait()

    monkeypatch.setattr(asyncio, "open_connection", hang)

    async def scenario() -> bool:
        connection = IPConnectionAsync("host", timeout=None)
        attempt = asyncio.create_task(connection.connect())
        await registered()
        await connection.disconnect()
        with pytest.raises(asyncio.CancelledError):
            await attempt
        return connection.is_connected

    assert run(scenario()) is False


def test_the_connection_is_closed_if_the_brick_daemon_goes_away() -> None:
    """The connection notices the end of the stream. It can be connected again."""

    async def scenario() -> None:
        async with FakeBrickd() as brickd:
            connection = IPConnectionAsync(HOST, brickd.port)
            await connection.connect()
            await brickd.wait_for_connections(1)
            brickd.drop_clients()
            await until(lambda: not connection.is_connected)

            with pytest.raises(NotConnectedError):
                await connection.enumerate()

            await connection.connect()
            await brickd.wait_for_connections(2)
            assert connection.is_connected
            await connection.disconnect()

    run(scenario())


# ----------------------------------------------------------------------------------------------------------------------
# Requests
# ----------------------------------------------------------------------------------------------------------------------
def test_requests_need_a_connection() -> None:
    """Nothing can be sent, before the connection is established."""
    connection = IPConnectionAsync(HOST)
    with pytest.raises(NotConnectedError):
        run(connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True))
    with pytest.raises(NotConnectedError):
        run(connection.ping())


def test_request_without_response() -> None:
    """The request is sent with the uid of the device, and the caller does not wait for a reply."""

    async def scenario() -> list[Packet]:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            await connection.send_request(DEVICE, GET_TEMPERATURE, b"\x01\x02")
            return list(await brickd.wait_for_packets(1))

    assert run(scenario()) == [Packet(UID, 1, 1, False, b"\x01\x02")]


def test_enumerate_and_ping_are_broadcasts() -> None:
    """They are sent to the uid 0, and are not answered."""

    async def scenario() -> list[Packet]:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            await connection.enumerate()
            await connection.ping()
            return list(await brickd.wait_for_packets(2))

    assert run(scenario()) == [Packet(0, 254, 1, False), Packet(0, 128, 2, False)]


def test_sequence_numbers_are_reused() -> None:
    """The sequence number is a number from 1 to 15. The number 0 is reserved for callbacks."""

    async def scenario() -> list[int]:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            for _ in range(17):
                await connection.ping()
            return [packet.sequence_number for packet in await brickd.wait_for_packets(17)]

    assert run(scenario()) == [*range(1, 16), 1, 2]


def test_request_with_response() -> None:
    """The reply is matched to the request by its sequence number."""

    async def scenario() -> tuple[tuple[HeaderPayload, bytes], Packet]:
        async with FakeBrickd(answer_with(b"\xc4\x09")) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            await connection.ping()  # Use up the first sequence number
            result = await connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True)
            return result, brickd.received[-1]

    (header, payload), request = run(scenario())
    assert request == Packet(UID, 1, 2, True)
    assert payload == b"\xc4\x09"
    # The function id is only translated for the functions of the IP connection, not for those of the devices
    assert header == HeaderPayload(UID, 2, True, 1, Flags.OK)
    assert isinstance(header.function_id, int)


def test_a_device_talks_through_the_connection() -> None:
    """The devices use the connection to send their requests."""

    async def scenario() -> tuple[Decimal, list[Packet]]:
        async with FakeBrickd(answer_with(struct.pack("<h", 2500))) as brickd:
            async with IPConnectionAsync(HOST, brickd.port) as connection:
                bricklet = BrickletTemperatureV2(UID, connection)
                return await bricklet.get_temperature(), brickd.received

    temperature, requests = run(scenario())
    assert temperature == Decimal("298.15")
    assert requests == [Packet(UID, 1, 1, True)]


def test_concurrent_requests_get_their_own_reply() -> None:
    """Each request has its own sequence number."""

    def echo(request: Packet) -> Packet:
        return reply(request, request.payload)

    async def scenario() -> list[bytes]:
        async with FakeBrickd(echo) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            results = await asyncio.gather(
                *(
                    connection.send_request(DEVICE, GET_TEMPERATURE, bytes([i]), response_expected=True)
                    for i in range(15)
                )
            )
            return [payload for _, payload in results]

    assert run(scenario()) == [bytes([i]) for i in range(15)]


@pytest.mark.parametrize(
    "flags, error, message",
    [
        (Flags.INVALID_PARAMETER.value, ValueError, "Invalid parameter"),
        (Flags.FUNCTION_NOT_SUPPORTED.value, AttributeError, "Function not supported: 1"),
    ],
)
def test_errors_of_the_device_are_raised(flags: int, error: type[Exception], message: str) -> None:
    """The device rejects the request with a flag in the header."""

    async def scenario() -> None:
        async with FakeBrickd(answer_with(flags=flags)) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            await connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True)

    with pytest.raises(error, match=message):
        run(scenario())


@pytest.mark.parametrize("flags, parsed", [(1, 1), (192, Flags.INVALID_PARAMETER | Flags.FUNCTION_NOT_SUPPORTED)])
def test_unknown_flags_are_returned_to_the_caller(flags: int, parsed: Flags | int) -> None:
    """The reply is passed on, the caller has to decide what to do with it."""

    async def scenario() -> tuple[HeaderPayload, bytes]:
        async with FakeBrickd(answer_with(b"\x01", flags)) as brickd:
            async with IPConnectionAsync(HOST, brickd.port) as connection:
                return await connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True)

    header, payload = run(scenario())
    assert header.flags == parsed
    assert payload == b"\x01"


def test_request_timeout() -> None:
    """If the reply does not arrive in time, the request fails and the connection is closed."""

    async def scenario() -> None:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port, timeout=0.01) as connection:
            with pytest.raises(TimeoutError):
                await connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True)
            await until(lambda: not connection.is_connected)

    run(scenario())


def test_pending_requests_fail_if_the_connection_is_closed() -> None:
    """The caller of a request must not wait for a reply, that can never arrive."""

    async def scenario() -> None:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port, timeout=None) as connection:
            request = asyncio.create_task(connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True))
            await brickd.wait_for_packets(1)
            await connection.disconnect()
            with pytest.raises(NotConnectedError, match="closed"):
                await request

    run(scenario())


def test_replies_to_other_requests_are_dropped() -> None:
    """A reply with a sequence number, that nobody is waiting for, is ignored."""

    def responder(request: Packet) -> bytes:
        stray = request._replace(sequence_number=request.sequence_number % 15 + 1, payload=b"stray")
        return stray.pack() + reply(request, b"mine").pack()

    async def scenario() -> tuple[HeaderPayload, bytes]:
        async with FakeBrickd(responder) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            return await connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True)

    assert run(scenario())[1] == b"mine"


def test_a_second_reply_to_a_request_is_logged(caplog: pytest.LogCaptureFixture) -> None:
    """Only the first reply is returned."""

    def responder(request: Packet) -> bytes:
        return reply(request, b"first").pack() + reply(request, b"second").pack()

    async def scenario() -> tuple[HeaderPayload, bytes]:
        async with FakeBrickd(responder) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            result = await connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True)
            await connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True)
            return result

    assert run(scenario())[1] == b"first"
    assert "Invalid sequence number: 1. The request was already processed" in caplog.text


def test_a_reply_to_a_cancelled_request_is_dropped(caplog: pytest.LogCaptureFixture) -> None:
    """
    The caller of a request was cancelled, but has not cleaned up yet, when the reply arrives. This race cannot be
    provoked from the outside, so the cancelled request is planted.
    """

    async def scenario() -> None:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            cancelled = asyncio.get_running_loop().create_future()
            cancelled.cancel()
            pending: dict[int, asyncio.Future[Any]] = getattr(connection, "_IPConnectionAsync__pending_requests")
            pending[5] = cancelled
            listener = asyncio.create_task(anext(connection.read_events(UID)))
            await registered()
            # The packets are processed in order, so the reply was processed when the callback arrives
            brickd.send(Packet(UID, 1, 5, True, b"late"), callback(UID, TEMPERATURE.value))
            await listener
            del pending[5]

    run(scenario())
    assert not caplog.records


def test_requests_are_logged(caplog: pytest.LogCaptureFixture) -> None:
    """The requests and the replies are logged at the debug level. It is off by default."""

    async def scenario(level: int) -> None:
        async with FakeBrickd(answer_with(b"\x01")) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            caplog.set_level(level, LOGGER)  # The connection sets the level when it is created
            await connection.send_request(DEVICE, GET_TEMPERATURE, response_expected=True)
            await connection.enumerate()

    run(scenario(logging.WARNING))
    assert not caplog.records

    run(scenario(logging.DEBUG))
    assert "Sending request to device" in caplog.text
    assert "Got reply for request number 1" in caplog.text
    assert "Enumerating Node." in caplog.text
    assert f"Tinkerforge IP connection ({HOST}:" in caplog.text


# ----------------------------------------------------------------------------------------------------------------------
# Authentication
# ----------------------------------------------------------------------------------------------------------------------
SERVER_NONCE = b"\x01\x02\x03\x04"


def authenticator(request: Packet) -> Packet | None:
    """A Brick Daemon with authentication. It hands out its nonce."""
    if request.function_id == FunctionID.GET_AUTHENTICATION_NONCE.value:
        return reply(request, SERVER_NONCE)
    return None


def digest(secret: bytes, client_nonce: bytes) -> bytes:
    """The proof, that the client knows the secret."""
    return hmac.new(secret, SERVER_NONCE + client_nonce, hashlib.sha1).digest()


@pytest.mark.parametrize("secret", ["My Authentication Secret!", b"My Authentication Secret!"])
def test_authentication(monkeypatch: pytest.MonkeyPatch, secret: bytes | str) -> None:
    """The connection authenticates with the HMAC of the nonces of the server and the client."""
    monkeypatch.setattr("os.urandom", lambda size: b"\xaa\xbb\xcc\xdd"[:size])

    async def scenario() -> list[Packet]:
        async with FakeBrickd(authenticator) as brickd:
            async with IPConnectionAsync(HOST, brickd.port, authentication_secret=secret):
                return list(await brickd.wait_for_packets(2))

    get_nonce, authenticate = run(scenario())
    # The authentication is requested from the Brick Daemon, which has the uid 1
    assert get_nonce == Packet(1, FunctionID.GET_AUTHENTICATION_NONCE.value, 1, True)
    client_nonce = b"\xaa\xbb\xcc\xdd"
    assert authenticate == Packet(
        1, FunctionID.AUTHENTICATE.value, 2, False, client_nonce + digest(b"My Authentication Secret!", client_nonce)
    )


def test_the_secret_can_be_given_when_connecting(monkeypatch: pytest.MonkeyPatch) -> None:
    """It replaces the secret, that was given when the connection was created, for this connection attempt."""
    monkeypatch.setattr("os.urandom", lambda size: bytes(size - 1) + b"\x01")

    async def scenario() -> list[Packet]:
        async with FakeBrickd(authenticator) as brickd:
            connection = IPConnectionAsync(HOST, brickd.port, authentication_secret="wrong")
            await connection.connect(authentication_secret="right")
            packets = list(await brickd.wait_for_packets(2))
            await connection.disconnect()
            return packets

    assert run(scenario())[1].payload[4:] == digest(b"right", b"\x00\x00\x00\x01")


def test_the_client_nonce_is_never_reused(monkeypatch: pytest.MonkeyPatch) -> None:
    """The nonce is a random number, that is incremented with every authentication."""
    random_numbers = iter([b"\xfe\xff\xff\xff", b"\x07\x00\x00\x00"])
    monkeypatch.setattr("os.urandom", lambda size: next(random_numbers))

    async def scenario() -> list[bytes]:
        async with FakeBrickd(authenticator) as brickd:
            connection = IPConnectionAsync(HOST, brickd.port, authentication_secret="secret")
            for attempt in range(1, 5):
                await connection.connect()
                await brickd.wait_for_packets(2 * attempt)
                await connection.disconnect()
            return [packet.payload[:4] for packet in brickd.received[1::2]]

    assert run(scenario()) == [
        b"\xfe\xff\xff\xff",
        b"\xff\xff\xff\xff",
        b"\x07\x00\x00\x00",  # The counter has overflown, so a new random number is drawn
        b"\x08\x00\x00\x00",
    ]


def test_connection_without_secret_does_not_authenticate() -> None:
    """The Brick Daemon is not asked for a nonce."""

    async def scenario() -> list[Packet]:
        async with FakeBrickd(authenticator) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            await connection.ping()
            return list(await brickd.wait_for_packets(1))

    assert run(scenario()) == [Packet(0, 128, 1, False)]


# ----------------------------------------------------------------------------------------------------------------------
# Callbacks
# ----------------------------------------------------------------------------------------------------------------------
def test_callbacks_are_delivered_to_the_listeners_of_the_device() -> None:
    """The callbacks are distributed by the uid of the device, that sent them."""

    async def scenario() -> tuple[list[tuple[HeaderPayload, bytes]], list[tuple[HeaderPayload, bytes]]]:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            mine = asyncio.create_task(take(connection.read_events(UID), 2))
            other = asyncio.create_task(take(connection.read_events(42), 1))
            await registered()
            brickd.send(callback(UID, 4, b"\x01"), callback(42, 8, b"\x02"), callback(7, 4), callback(UID, 13, b"\x03"))
            return await asyncio.gather(mine, other)

    mine, other = run(scenario())
    # A callback has no sequence number, and its function id is not translated
    assert mine == [
        (HeaderPayload(UID, None, False, 4, Flags.OK), b"\x01"),
        (HeaderPayload(UID, None, False, 13, Flags.OK), b"\x03"),
    ]
    assert other == [(HeaderPayload(42, None, False, 8, Flags.OK), b"\x02")]


def test_a_device_reads_its_callbacks_from_the_connection() -> None:
    """The devices convert the callbacks to events."""

    async def scenario() -> Event:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            bricklet = BrickletTemperatureV2(UID, connection)
            listener = asyncio.create_task(anext(bricklet.read_events()))
            await registered()
            brickd.send(callback(UID, TEMPERATURE.value, struct.pack("<h", 2500)))
            return await listener

    event = run(scenario())
    assert (event.sid, event.function_id, event.payload) == (0, TEMPERATURE, Decimal("298.15"))


def test_packets_that_are_neither_a_callback_nor_a_reply_are_dropped(caplog: pytest.LogCaptureFixture) -> None:
    """The connection keeps running, if it receives a packet that it cannot handle."""

    async def scenario() -> tuple[HeaderPayload, bytes]:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            caplog.set_level(logging.DEBUG, LOGGER)
            listener = asyncio.create_task(anext(connection.read_events(UID)))
            await registered()
            brickd.send(
                Packet(UID, 4, 3, False, b"request"),  # A request, that is addressed to a device
                callback(UID, FunctionID.DISCONNECT_PROBE.value),  # A function of the connection, but not a callback
                struct.pack("<IBBBB", UID, 4, 4, 0, 0),  # The size is smaller than the size of the header
                callback(UID, 4, b"callback"),
            )
            return await listener

    assert run(scenario())[1] == b"callback"
    assert "Unknown packet" in caplog.text
    assert "Invalid data received" in caplog.text


def test_the_reader_stops_if_the_connection_is_lost(monkeypatch: pytest.MonkeyPatch) -> None:
    """The packets, that were received before the connection was lost, are still delivered."""

    async def collect(connection: IPConnectionAsync, events: list[bytes]) -> None:
        async for event in connection.read_events(UID):
            events.append(event[1])

    async def scenario() -> list[bytes]:
        events: list[bytes] = []
        async with FakeBrickd() as brickd:
            connection = IPConnectionAsync(HOST, brickd.port)
            await connection.connect()
            listener = asyncio.create_task(collect(connection, events))
            await registered()

            with monkeypatch.context() as patch:
                # The transport is closing
                patch.setattr(IPConnectionAsync, "is_connected", property(lambda self: False))
                brickd.send(callback(UID, 4, b"first"))
                await until(lambda: events)
                brickd.send(callback(UID, 4, b"second"))
                await asyncio.sleep(0.05)

            listener.cancel()
            await connection.disconnect()
        return events

    assert run(scenario()) == [b"first"]


# ----------------------------------------------------------------------------------------------------------------------
# Enumeration
# ----------------------------------------------------------------------------------------------------------------------
async def enumerate_devices(
    brickd: FakeBrickd, connection: IPConnectionAsync, count: int, **filters: int
) -> list[tuple[EnumerationType, Device]]:
    """Request the enumeration, and read the devices that answer."""
    listener = asyncio.create_task(take(connection.read_enumeration(**filters), count))
    await registered()
    await connection.enumerate()
    await brickd.wait_for_packets(1)
    return await listener


def test_enumeration_creates_the_devices() -> None:
    """The devices answer with their uid and their type. The connection creates the matching objects."""

    def responder(_request: Packet) -> bytes:
        bricklet = enumeration(EnumerationType.AVAILABLE.value)
        # A Brick, that is not stacked on another Brick, is connected to "0"
        brick = enumeration(EnumerationType.CONNECTED.value, b"21", b"0", "0", 13)
        return bricklet.pack() + brick.pack()

    async def scenario() -> tuple[IPConnectionAsync, list[tuple[EnumerationType, Device]]]:
        async with FakeBrickd(responder) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            return connection, await enumerate_devices(brickd, connection, 2)

    connection, [(first_type, bricklet), (second_type, brick)] = run(scenario())
    assert first_type is EnumerationType.AVAILABLE
    assert isinstance(bricklet, BrickletTemperatureV2)
    assert bricklet.uid == UID
    assert bricklet.ipcon is connection
    assert second_type is EnumerationType.CONNECTED
    assert isinstance(brick, BrickMaster)
    assert brick.uid == 58


def test_enumeration_can_be_filtered_by_uid() -> None:
    """Only the device with the uid is reported."""

    def responder(_request: Packet) -> bytes:
        other = enumeration(EnumerationType.AVAILABLE.value, b"21", b"0", "0", 13)
        return other.pack() + enumeration(EnumerationType.AVAILABLE.value).pack()

    async def scenario() -> list[tuple[EnumerationType, Device]]:
        async with FakeBrickd(responder) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            return await enumerate_devices(brickd, connection, 1, uid=UID)

    [(_, device)] = run(scenario())
    assert isinstance(device, BrickletTemperatureV2)


def test_devices_without_driver_are_skipped(caplog: pytest.LogCaptureFixture) -> None:
    """A device, that is not supported by the library, is logged."""

    def responder(_request: Packet) -> bytes:
        unknown = enumeration(EnumerationType.AVAILABLE.value, device=9999)
        # A device that was disconnected, does not report its type any more
        disconnected = enumeration(EnumerationType.DISCONNECTED.value, connected_uid=b"", position="\0", device=0)
        return unknown.pack() + disconnected.pack() + enumeration(EnumerationType.AVAILABLE.value).pack()

    async def scenario() -> list[tuple[EnumerationType, Device]]:
        async with FakeBrickd(responder) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            return await enumerate_devices(brickd, connection, 1)

    [(_, device)] = run(scenario())
    assert isinstance(device, BrickletTemperatureV2)
    assert "No driver for device id '9999' found." in caplog.text
    assert "No driver for device id 'None' found." in caplog.text


def test_an_error_while_processing_a_packet_closes_the_connection(caplog: pytest.LogCaptureFixture) -> None:
    """The connection cannot recover from an unexpected error, so it is closed."""

    async def scenario() -> None:
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            await brickd.wait_for_connections(1)
            brickd.send(enumeration(9))  # There is no such type of enumeration
            await until(lambda: not connection.is_connected)

    run(scenario())
    assert "Error reading packet from host 127.0.0.1" in caplog.text


# ----------------------------------------------------------------------------------------------------------------------
# Closing the transport
# ----------------------------------------------------------------------------------------------------------------------
def test_disconnect_if_the_socket_is_no_longer_connected(monkeypatch: pytest.MonkeyPatch) -> None:
    """The end of the stream cannot be sent, if the peer is gone. The connection is closed nevertheless."""

    def write_eof(writer: asyncio.StreamWriter) -> None:
        writer.close()
        raise OSError(errno.ENOTCONN, "Transport endpoint is not connected")

    async def scenario() -> bool:
        async with FakeBrickd() as brickd:
            connection = IPConnectionAsync(HOST, brickd.port)
            await connection.connect()
            monkeypatch.setattr(asyncio.StreamWriter, "write_eof", write_eof)
            await connection.disconnect()
            return connection.is_connected

    assert run(scenario()) is False


def test_other_errors_while_disconnecting_are_raised(monkeypatch: pytest.MonkeyPatch) -> None:
    """The connection is closed, but the caller is told that something went wrong."""

    def write_eof(writer: asyncio.StreamWriter) -> None:
        writer.close()
        raise OSError(errno.EIO, "Input/output error")

    async def scenario() -> bool:
        async with FakeBrickd() as brickd:
            connection = IPConnectionAsync(HOST, brickd.port)
            await connection.connect()
            monkeypatch.setattr(asyncio.StreamWriter, "write_eof", write_eof)
            with pytest.raises(OSError, match="Input/output error"):
                await connection.disconnect()
            return connection.is_connected

    assert run(scenario()) is False


def test_finished_requests_are_not_touched_when_the_connection_is_closed() -> None:
    """
    A request got its reply, but its caller has not cleaned up yet, when the connection is closed. This race cannot
    be provoked from the outside, so the finished request is planted.
    """

    async def scenario() -> tuple[None, bytes]:
        async with FakeBrickd() as brickd:
            connection = IPConnectionAsync(HOST, brickd.port)
            await connection.connect()
            finished: asyncio.Future[tuple[None, bytes]] = asyncio.get_running_loop().create_future()
            finished.set_result((None, b"reply"))
            pending: dict[int, asyncio.Future[Any]] = getattr(connection, "_IPConnectionAsync__pending_requests")
            pending[5] = finished
            await connection.disconnect()
            return finished.result()

    assert run(scenario()) == (None, b"reply")
