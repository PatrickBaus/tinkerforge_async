"""Tests for the helper that merges async generators."""

import asyncio

import pytest

from tinkerforge_async.helper import join

from .fake_connection import run, take


class Source:  # pylint: disable=too-few-public-methods
    """An async generator, that records whether it was closed."""

    def __init__(self, *items, error=None, delay=0.0, endless=False):
        self.items = items
        self.error = error
        self.delay = delay
        self.endless = endless
        self.closed = False

    async def generate(self):
        """Yield the items, then raise the error, wait forever or stop."""
        try:
            for item in self.items:
                await asyncio.sleep(self.delay)
                yield item
            if self.error is not None:
                raise self.error
            if self.endless:
                await asyncio.Event().wait()
        finally:
            self.closed = True


async def collect(*sources, count=None):
    """Read the merged stream of the sources. Stop after a number of items, if `count` is given."""
    return await take(join(*(source.generate() for source in sources)), count)


def test_the_items_of_all_generators_are_merged():
    """The stream ends, when all generators are exhausted."""
    sources = Source(1, 2, 3), Source("a", "b"), Source()
    items = run(collect(*sources))
    assert sorted(map(str, items)) == ["1", "2", "3", "a", "b"]
    # The order of the items of a generator is kept
    assert [item for item in items if isinstance(item, int)] == [1, 2, 3]
    assert [item for item in items if isinstance(item, str)] == ["a", "b"]
    assert all(source.closed for source in sources)


def test_items_are_yielded_in_the_order_they_arrive():
    """A slow generator does not block a fast generator."""
    slow, fast = Source("slow", delay=0.05), Source("fast 1", "fast 2")
    assert run(collect(slow, fast)) == ["fast 1", "fast 2", "slow"]


def test_join_without_generators_is_empty():
    """There is nothing to merge."""
    assert run(collect()) == []


def test_an_exception_is_raised_by_the_stream_and_all_generators_are_closed():
    """The error of one generator ends the stream."""
    failing, endless = Source(1, error=RuntimeError("broken")), Source("a", endless=True)
    with pytest.raises(RuntimeError, match="broken"):
        run(collect(failing, endless))
    assert failing.closed
    assert endless.closed


def test_leaving_the_loop_closes_all_generators():
    """The generators must not keep running, if nobody reads the stream any more."""
    sources = Source(1, 2, 3, endless=True), Source("a", endless=True)
    assert len(run(collect(*sources, count=2))) == 2
    assert all(source.closed for source in sources)
