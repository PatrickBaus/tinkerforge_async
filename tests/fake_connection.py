"""A fake IP connection for the tests of the devices. It records the requests and returns canned replies."""

from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import AsyncGenerator, Coroutine
from contextlib import aclosing
from enum import Enum
from typing import TYPE_CHECKING, Any, NamedTuple, cast, override

from tinkerforge_async.ip_connection import Flags, HeaderPayload
from tinkerforge_async.ip_connection_helper import pack_payload

if TYPE_CHECKING:
    from tinkerforge_async.ip_connection import IPConnectionAsync

UID = 12345  # The uid of the devices under test


class Request(NamedTuple):
    """A request as it is passed to `IPConnectionAsync.send_request()`."""

    function_id: Enum
    data: bytes
    response_expected: bool


def request(function_id: Enum, *payload: Any, response_expected: bool = True) -> Request:
    """
    Create the request, that a device is expected to send. The `payload` is the Tinkerforge format string, followed by
    the values that are packed with it. A request without payload has neither.
    """
    return Request(function_id, pack_payload(payload[1:], payload[0]) if payload else b"", response_expected)


class FakeConnection:
    """
    Replaces the `IPConnectionAsync` of a device. It records all requests in `requests`, answers them with the replies
    that were registered with `reply()` and delivers the callbacks that were registered with `callback()`.
    """

    def __init__(self) -> None:
        self.requests: list[Request] = []
        self.connected = False
        self.__replies: dict[Enum, list[bytes]] = defaultdict(list)
        self.__errors: dict[Enum, Exception] = {}
        self.__callbacks: list[tuple[int, bytes]] = []

    @property
    def ipcon(self) -> IPConnectionAsync:
        """This fake, typed as the `IPConnectionAsync` it replaces, so that it can be handed to a device."""
        return cast("IPConnectionAsync", self)

    def reply(self, function_id: Enum, form: str, *values: Any) -> None:
        """
        Register the reply to the function `function_id`. If the function is called more often than replies were
        registered, the last reply is repeated.
        """
        self.__replies[function_id].append(pack_payload(values, form))

    def fail(self, function_id: Enum, error: Exception) -> None:
        """Let all requests of the function `function_id` raise an error, like a device that rejects the request."""
        self.__errors[function_id] = error

    def callback(self, callback_id: Enum | int, *payload: Any) -> None:
        """
        Register a callback packet, that is delivered by `read_events()`. The `payload` is the Tinkerforge format
        string, followed by the values that are packed with it. A callback without payload has neither.
        """
        function_id = callback_id.value if isinstance(callback_id, Enum) else callback_id
        self.__callbacks.append((function_id, pack_payload(payload[1:], payload[0]) if payload else b""))

    async def send_request(
        self, device: Any, function_id: Enum, data: bytes = b"", *, response_expected: bool = False
    ) -> tuple[HeaderPayload, bytes] | None:
        """Record the request and return the registered reply."""
        assert device.uid == UID
        self.requests.append(Request(function_id, bytes(data), response_expected))
        if function_id in self.__errors:
            raise self.__errors[function_id]
        if not response_expected:
            return None
        replies = self.__replies[function_id]
        payload = replies.pop(0) if len(replies) > 1 else replies[0] if replies else b""
        return HeaderPayload(device.uid, 1, True, function_id.value, Flags.OK), payload

    async def read_events(self, uid: int) -> AsyncGenerator[tuple[HeaderPayload, bytes], None]:
        """Deliver the registered callbacks, then stop."""
        assert uid == UID
        for function_id, payload in self.__callbacks:
            yield HeaderPayload(uid, None, False, function_id, Flags.OK), payload

    async def connect(self) -> None:
        """Pretend to connect"""
        self.connected = True

    async def disconnect(self) -> None:
        """Pretend to disconnect"""
        self.connected = False


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    """Run a coroutine to completion."""
    return asyncio.run(coroutine)


async def take[T](stream: AsyncGenerator[T, None], count: int | None = None) -> list[T]:
    """
    Read items from an async generator, and close it. Stop after `count` items, or read until the generator is
    exhausted if no `count` is given.
    """
    items: list[T] = []
    async with asyncio.timeout(5):
        async with aclosing(stream) as items_of_stream:
            async for item in items_of_stream:
                items.append(item)
                if len(items) == count:
                    break
    return items


def read_events(device: Any, **filters: Any) -> list[Any]:
    """Collect the events, that a device yields for the callbacks registered with the connection."""

    return run(take(device.read_events(**filters)))


def summary(events: list[Any]) -> list[tuple[int, Enum, Any]]:
    """The sid, callback and payload of a list of events."""
    return [(event.sid, event.function_id, event.payload) for event in events]


class Call(NamedTuple):
    """
    A call of a method of a device, the request it must send and the result it must return for a given reply.

    Parameters
    ----------
    method: str
        The name of the method.
    function_id: Enum
        The function, that is requested from the device.
    arguments: tuple
        The arguments of the method.
    sent: tuple of str and tuple, optional
        The format and the values of the payload of the request.
    reply: tuple of str and tuple, optional
        The format and the values of the payload of the reply. If `None`, the method does not expect a response by
        default, see `response_expected`.
    result: Any
        The result of the method.
    response_expected: bool, optional
        Whether the request asks for a response. The default is `True`, unless neither a `reply` nor a `result` is
        given.
    """

    method: str
    function_id: Enum
    arguments: tuple[Any, ...] = ()
    sent: tuple[str, tuple[Any, ...]] = ("", ())
    reply: tuple[str, tuple[Any, ...]] | None = None
    result: Any = None
    response_expected: bool = True

    @override
    def __str__(self) -> str:
        return f"{self.method}{self.arguments}"


def check(device: Any, connection: FakeConnection, call: Call) -> None:
    """Call the method of the device, and compare the request that was sent and the result with the expectation."""
    if call.reply is not None:
        connection.reply(call.function_id, call.reply[0], *call.reply[1])
    result = run(getattr(device, call.method)(*call.arguments))
    form, values = call.sent
    payload = (form, *values) if form else ()
    assert connection.requests == [request(call.function_id, *payload, response_expected=call.response_expected)]
    assert result == call.result
    assert type(result) is type(call.result)  # e.g. a Decimal must not be returned as an int


def check_rejected(
    device: Any, connection: FakeConnection, method: str, *arguments: Any, error: type[Exception] = ValueError
) -> None:
    """Call the method of the device with invalid arguments. It must raise an error and must not send a request."""
    try:
        run(getattr(device, method)(*arguments))
    except error:
        assert not connection.requests
    else:
        raise AssertionError(f"{method}{arguments} did not raise {error.__name__}")


def chunk(data: Any, offset: int, size: int, padding: Any) -> list[Any]:
    """The chunk of a stream starting at `offset`, padded to `size` items, as it is transferred by the device."""
    part = list(data[offset : offset + size])
    return part + [padding] * (size - len(part))
