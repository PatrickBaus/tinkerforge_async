"""
General helper functions used by multiple modules.
"""

import asyncio
from collections.abc import AsyncGenerator
from contextlib import aclosing
from dataclasses import dataclass
from decimal import Decimal
from typing import TypeVar, cast

T = TypeVar("T")


@dataclass
class _Failure:
    """Wraps an exception of a producer, so it can be passed to the consumer of `join()`."""

    exception: BaseException


async def join(*generators: AsyncGenerator[T, None]) -> AsyncGenerator[T, None]:
    """
    Merge the items of all `generators` into a single stream, in the order they arrive. The stream ends when all
    generators are exhausted. If one generator raises an exception, it is raised by the stream, and all generators are
    closed. Leaving the loop early (e.g. with `break`) closes all generators, too.

    Note: This is not implemented with a `TaskGroup`, because task groups must not be used in async generators. They
    can not handle the `GeneratorExit` exception, that is thrown into the generator when it is closed.
    """
    done = object()  # Every producer puts this sentinel into the queue when it is finished
    queue: asyncio.Queue[object] = asyncio.Queue(maxsize=1)

    async def pump(generator: AsyncGenerator[T, None]) -> None:
        try:
            async with aclosing(generator):
                async for item in generator:
                    await queue.put(item)
        except Exception as exc:  # pylint: disable=broad-exception-caught  # Forwarded to the consumer
            await queue.put(_Failure(exc))
        else:
            await queue.put(done)

    producers = [asyncio.create_task(pump(generator)) for generator in generators]
    try:
        remaining = len(producers)
        while remaining:
            item = await queue.get()
            if item is done:
                remaining -= 1
            elif isinstance(item, _Failure):
                raise item.exception
            else:
                yield cast(T, item)
    finally:
        for producer in producers:
            producer.cancel()
        await asyncio.gather(*producers, return_exceptions=True)


def seconds_to_ms(value: float | Decimal) -> int:
    """
    Convert a duration in s to the integer value in ms used by the Tinkerforge protocol. Rounding avoids floating point
    errors, e.g. 0.29 s * 1000 = 290.00000000000006.
    """
    return round(Decimal(str(value)) * 1000)


def ms_to_seconds(value: int) -> Decimal:
    """
    Convert an integer value in ms, as used by the Tinkerforge protocol, to a duration in s.
    """
    return Decimal(value) / 1000
