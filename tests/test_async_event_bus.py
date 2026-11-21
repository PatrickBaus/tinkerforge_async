"""Tests for the event bus, that distributes the packets of the IP connection to the devices."""

import asyncio

from tinkerforge_async.async_event_bus import EventBus

from .fake_connection import run, take


async def started(task: asyncio.Task) -> None:
    """Give a task the time to run up to its first await, i.e. to register with the event bus."""
    for _ in range(3):
        await asyncio.sleep(0)
    assert not task.done()


def test_events_are_delivered_in_order():
    """A listener gets all events, that are published after it has registered."""

    async def scenario():
        bus = EventBus()
        listener = asyncio.create_task(take(bus.register("/events/1"), 3))
        await started(listener)
        for event in ("a", "b", "c"):
            bus.publish("/events/1", event)
        return await listener

    assert run(scenario()) == ["a", "b", "c"]


def test_all_listeners_of_an_event_get_it():
    """An event is delivered to every listener, but not to the listeners of other events."""

    async def scenario():
        bus = EventBus()
        first = asyncio.create_task(take(bus.register("/events/1"), 1))
        second = asyncio.create_task(take(bus.register("/events/1"), 1))
        other = asyncio.create_task(take(bus.register("/events/2"), 1))
        await asyncio.gather(started(first), started(second), started(other))
        bus.publish("/events/1", "one")
        bus.publish("/events/2", "two")
        return await asyncio.gather(first, second, other)

    assert run(scenario()) == [["one"], ["one"], ["two"]]


def test_events_without_listener_are_dropped():
    """Events are not stored for listeners, that register later."""

    async def scenario():
        bus = EventBus()
        bus.publish("/events/1", "lost")
        listener = asyncio.create_task(take(bus.register("/events/1"), 1))
        await started(listener)
        bus.publish("/events/1", "delivered")
        return await listener

    assert run(scenario()) == ["delivered"]


def test_a_listener_is_removed_when_it_stops_listening():
    """A listener that has left gets no more events, and the other listeners are not affected."""

    async def scenario():
        bus = EventBus()
        leaving = asyncio.create_task(take(bus.register("/events/1"), 1))
        staying = asyncio.create_task(take(bus.register("/events/1"), 2))
        await asyncio.gather(started(leaving), started(staying))
        bus.publish("/events/1", "first")
        assert await leaving == ["first"]
        bus.publish("/events/1", "second")
        assert await staying == ["first", "second"]

        # Nobody is listening any more, the bus has cleaned up and can be used again
        bus.publish("/events/1", "lost")
        listener = asyncio.create_task(take(bus.register("/events/1"), 1))
        await started(listener)
        bus.publish("/events/1", "third")
        return await listener

    assert run(scenario()) == ["third"]


def test_a_cancelled_listener_is_removed():
    """Cancelling the task of a listener unregisters it."""

    async def scenario():
        bus = EventBus()
        listener = asyncio.create_task(take(bus.register("/events/1"), 1))
        await started(listener)
        listener.cancel()
        await asyncio.gather(listener, return_exceptions=True)
        bus.publish("/events/1", "lost")  # Must not raise
        return listener.cancelled()

    assert run(scenario())
