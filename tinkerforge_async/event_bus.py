# -*- coding: utf-8 -*-
import asyncio


class EventBus:
    def __init__(self):
        self.__listeners = {}

    async def register(self, event_name):
        queue = asyncio.Queue()
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

    def emit(self, event_name, event):
        listener_queues = self.__listeners.get(event_name, [])
        for queue in listener_queues:
            queue.put_nowait(event)
