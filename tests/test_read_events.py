"""Tests for the filtering and the conversion of callbacks, that is shared by all devices in `Device.read_events()`."""

import asyncio
from collections.abc import AsyncGenerator, Sequence
from decimal import Decimal
from enum import Enum
from types import SimpleNamespace
from typing import Any, cast

import pytest

from tinkerforge_async.bricklet_industrial_dual_0_20ma_v2 import BrickletIndustrialDual020mAV2
from tinkerforge_async.bricklet_io16 import BrickletIO16
from tinkerforge_async.bricklet_temperature import BrickletTemperature
from tinkerforge_async.devices import Event
from tinkerforge_async.ip_connection import IPConnectionAsync
from tinkerforge_async.ip_connection_helper import pack_payload


class FakeIpConnection:  # pylint: disable=too-few-public-methods
    """An IP connection, that delivers a fixed list of callback packets and then stays silent."""

    def __init__(self, packets: Sequence[tuple[Enum | int, bytes]]) -> None:
        self.packets = packets

    @property
    def ipcon(self) -> IPConnectionAsync:
        """This fake, typed as the `IPConnectionAsync` it replaces, so that it can be handed to a device."""
        return cast(IPConnectionAsync, self)

    async def read_events(self, _uid: int) -> AsyncGenerator[tuple[SimpleNamespace, bytes], None]:
        """Yield the packets"""
        for function_id, payload in self.packets:
            yield SimpleNamespace(function_id=function_id), payload


def read(device: Any, **filters: Any) -> list[Event]:
    """Collect the events of a device, that are yielded for the given filters."""

    async def collect() -> list[Event]:
        return [event async for event in device.read_events(**filters)]

    return asyncio.run(collect())


@pytest.fixture(name="temperature")
def temperature_fixture() -> BrickletTemperature:
    """A Temperature Bricklet that receives a periodic and a threshold callback."""
    callback_id = BrickletTemperature.CallbackID
    packets: list[tuple[Enum | int, bytes]] = [
        (callback_id.TEMPERATURE, pack_payload((2345,), "h")),
        (callback_id.TEMPERATURE_REACHED, pack_payload((-1000,), "h")),
        (99, b""),  # unknown callback, must be dropped
    ]
    return BrickletTemperature(12345, FakeIpConnection(packets).ipcon)


def names(events: list[Event]) -> list[str]:
    """The callback names of a list of events."""
    return [event.function_id.name for event in events]


def test_no_filter_yields_all_events_converted_to_si(temperature: BrickletTemperature) -> None:
    """Without filter all callbacks are yielded and unknown callbacks are dropped."""
    events = read(temperature)
    assert names(events) == ["TEMPERATURE", "TEMPERATURE_REACHED"]
    assert [event.payload for event in events] == [Decimal("296.6"), Decimal("263.15")]
    assert {event.sid for event in events} == {0}
    assert all(event.sender is temperature for event in events)


def test_events_filter_accepts_callback_ids_and_ints_in_any_sequence(temperature: BrickletTemperature) -> None:
    """The events can be CallbackID or int and a tuple or a list."""
    callback_id = BrickletTemperature.CallbackID
    assert names(read(temperature, events=[callback_id.TEMPERATURE_REACHED])) == ["TEMPERATURE_REACHED"]
    assert names(read(temperature, events=(callback_id.TEMPERATURE.value,))) == ["TEMPERATURE"]


def test_sids_filter_selects_the_callbacks_of_the_sid(temperature: BrickletTemperature) -> None:
    """A sid selects all callbacks of that sid. Unknown sids select nothing."""
    assert names(read(temperature, sids=[0])) == ["TEMPERATURE", "TEMPERATURE_REACHED"]
    assert not read(temperature, sids=[5])


def test_events_and_sids_filters_are_combined(temperature: BrickletTemperature) -> None:
    """Events matching either filter are yielded."""
    callback_id = BrickletTemperature.CallbackID
    assert names(read(temperature, events=[callback_id.TEMPERATURE], sids=[5])) == ["TEMPERATURE"]
    assert names(read(temperature, events=[callback_id.TEMPERATURE], sids=[0])) == [
        "TEMPERATURE",
        "TEMPERATURE_REACHED",
    ]


@pytest.mark.parametrize("filters", [{"events": []}, {"sids": []}, {"events": [], "sids": []}])
def test_empty_filter_selects_nothing(temperature: BrickletTemperature, filters: dict[str, list[int]]) -> None:
    """Only None means no filter. An empty filter selects nothing, for every device."""
    assert not read(temperature, **filters)


def test_invalid_event_raises_value_error(temperature: BrickletTemperature) -> None:
    """An unknown callback id is rejected, when the generator is started."""
    with pytest.raises(ValueError):
        read(temperature, events=[9999])


@pytest.fixture(name="dual_current")
def dual_current_fixture() -> BrickletIndustrialDual020mAV2:
    """A Bricklet, that reports the channel in the payload and receives a callback of both channels."""
    callback_id = BrickletIndustrialDual020mAV2.CallbackID
    packets = [
        (callback_id.CURRENT, pack_payload((0, 4_000_000), "B i")),
        (callback_id.CURRENT, pack_payload((1, 20_000_000), "B i")),
    ]
    return BrickletIndustrialDual020mAV2(12345, FakeIpConnection(packets).ipcon)


def test_channel_in_payload_is_the_sid(dual_current: BrickletIndustrialDual020mAV2) -> None:
    """Devices, that return the channel in the payload, use it as the sid, and filter the other channels."""
    assert [(event.sid, event.payload) for event in read(dual_current)] == [(0, Decimal("0.004")), (1, Decimal("0.02"))]
    assert [event.sid for event in read(dual_current, sids=[1])] == [1]


def test_io16_rejects_events_and_sids_together_and_unknown_sids() -> None:
    """The IO-16 uses sids as pins, so it validates them and does not combine the filters."""
    device = BrickletIO16(12345, FakeIpConnection([]).ipcon)
    callback_id = BrickletIO16.CallbackID
    with pytest.raises(ValueError):
        read(device, events=[callback_id.INTERRUPT], sids=[0])
    with pytest.raises(ValueError):
        read(device, sids=[16])


def test_io16_yields_one_event_per_changed_pin() -> None:
    """The payload of one callback results in one event per changed pin."""
    callback_id = BrickletIO16.CallbackID
    port_a = b"a"
    packets = [(callback_id.INTERRUPT, pack_payload((port_a, 0b0000_0101, 0b0000_0100), "c B B"))]
    device = BrickletIO16(12345, FakeIpConnection(packets).ipcon)
    assert [(event.sid, event.payload) for event in read(device, sids=[0, 1, 2])] == [(0, False), (2, True)]
