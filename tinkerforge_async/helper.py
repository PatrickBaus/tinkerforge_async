"""
General helper functions used by multiple modules.
"""

import asyncio
from typing import AsyncGenerator, TypeVar

T = TypeVar("T")


async def _read_into_queue(
    gen: AsyncGenerator[T, None],
    queue: asyncio.Queue[T],
    done: asyncio.Semaphore,
) -> None:
    try:
        async for item in gen:
            await queue.put(item)
    finally:
        # Once done, notify the semaphore
        await done.acquire()


async def join(*generators: AsyncGenerator[T, None]) -> AsyncGenerator[T, None]:
    queue: asyncio.Queue[T] = asyncio.Queue(maxsize=1)
    done_semaphore = asyncio.Semaphore(len(generators))

    # Read from each given generator into the shared queue.
    producers = [asyncio.create_task(_read_into_queue(gen, queue, done_semaphore)) for gen in generators]

    # Read items off the queue until it is empty and the semaphore value is down to zero.
    while not done_semaphore.locked() or not queue.empty():
        try:
            yield await asyncio.wait_for(queue.get(), 0.001)
        except TimeoutError:
            continue

    # Not strictly needed, but usually a good idea to await tasks, they are already finished here.
    try:
        await asyncio.wait_for(asyncio.gather(*producers), 0)
    except TimeoutError as exc:
        raise NotImplementedError("Impossible state: expected all tasks to be exhausted") from exc
