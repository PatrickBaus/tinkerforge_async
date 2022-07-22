"""
A lightweight event bus for the asyncio framework, that relies on asynchronous
generators to deliver messages.
"""
import asyncio
from typing import Any, AsyncGenerator


class EventBus:
    """
    An event bus, that is using the async generator syntax for distributing events.
    It uses dicts and sets internally to ensure good performance.
    """

    def __init__(self) -> None:
        self.__listeners: dict[str, set[asyncio.Queue]] = {}

    async def register(self, event_name: str) -> AsyncGenerator[Any, None]:
        """
        The async generator, that yields events subscribed to `event_name`.

        Parameters
        ----------
        event_name: str
            The type of event to listen for.

        Yields
        -------
        Any
            The events
        """
        queue: asyncio.Queue = asyncio.Queue()
        if self.__listeners.get(event_name, None) is None:
            self.__listeners[event_name] = {queue}
        else:
            self.__listeners[event_name].add(queue)

        try:
            while "listening":
                event = await queue.get()
                yield event
        finally:
            # Cleanup
            self.__listeners[event_name].remove(queue)
            if len(self.__listeners[event_name]) == 0:
                del self.__listeners[event_name]

    def publish(self, event_name: str, event: Any) -> None:
        """
        Publish an event called `event_name` with the payload `event`.

        Parameters
        ----------
        event_name: str
            The event address.
        event: any
            The data to be published.
        """
        listener_queues: set[asyncio.Queue] = self.__listeners.get(event_name, set())
        for queue in listener_queues:
            queue.put_nowait(event)
