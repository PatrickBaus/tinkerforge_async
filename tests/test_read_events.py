"""Tests for the filtering and the conversion of callbacks, that is shared by all devices in `Device.read_events()`."""

import asyncio
from decimal import Decimal
from types import SimpleNamespace

import pytest

from tinkerforge_async.bricklet_industrial_dual_0_20ma_v2 import BrickletIndustrialDual020mAV2
from tinkerforge_async.bricklet_io16 import BrickletIO16
from tinkerforge_async.bricklet_temperature import BrickletTemperature
from tinkerforge_async.ip_connection_helper import pack_payload


class FakeIpConnection:  # pylint: disable=too-few-public-methods
    """An IP connection, that delivers a fixed list of callback packets and then stays silent."""

    def __init__(self, packets):
        self.packets = packets

    async def read_events(self, _uid):
        """Yield the packets"""
        for function_id, payload in self.packets:
            yield SimpleNamespace(function_id=function_id), payload


def read(device, **filters):
    """Collect the events of a device, that are yielded for the given filters."""

    async def collect():
        return [event async for event in device.read_events(**filters)]

    return asyncio.run(collect())


@pytest.fixture(name="temperature")
def temperature_fixture():
    """A Temperature Bricklet that receives a periodic and a threshold callback."""
    callback_id = BrickletTemperature.CallbackID
    packets = [
        (callback_id.TEMPERATURE, pack_payload((2345,), "h")),
        (callback_id.TEMPERATURE_REACHED, pack_payload((-1000,), "h")),
        (99, b""),  # unknown callback, must be dropped
    ]
    return BrickletTemperature(12345, FakeIpConnection(packets))


def names(events):
    """The callback names of a list of events."""
    return [event.function_id.name for event in events]


def test_no_filter_yields_all_events_converted_to_si(temperature):
    """Without filter all callbacks are yielded and unknown callbacks are dropped."""
    events = read(temperature)
    assert names(events) == ["TEMPERATURE", "TEMPERATURE_REACHED"]
    assert [event.payload for event in events] == [Decimal("296.6"), Decimal("263.15")]
    assert {event.sid for event in events} == {0}
    assert all(event.sender is temperature for event in events)


def test_events_filter_accepts_callback_ids_and_ints_in_any_sequence(temperature):
    """The events can be CallbackID or int and a tuple or a list."""
    callback_id = BrickletTemperature.CallbackID
    assert names(read(temperature, events=[callback_id.TEMPERATURE_REACHED])) == ["TEMPERATURE_REACHED"]
    assert names(read(temperature, events=(callback_id.TEMPERATURE.value,))) == ["TEMPERATURE"]


def test_sids_filter_selects_the_callbacks_of_the_sid(temperature):
    """A sid selects all callbacks of that sid. Unknown sids select nothing."""
    assert names(read(temperature, sids=[0])) == ["TEMPERATURE", "TEMPERATURE_REACHED"]
    assert not read(temperature, sids=[5])


def test_events_and_sids_filters_are_combined(temperature):
    """Events matching either filter are yielded."""
    callback_id = BrickletTemperature.CallbackID
    assert names(read(temperature, events=[callback_id.TEMPERATURE], sids=[5])) == ["TEMPERATURE"]
    assert names(read(temperature, events=[callback_id.TEMPERATURE], sids=[0])) == [
        "TEMPERATURE",
        "TEMPERATURE_REACHED",
    ]


@pytest.mark.parametrize("filters", [{"events": []}, {"sids": []}, {"events": [], "sids": []}])
def test_empty_filter_selects_nothing(temperature, filters):
    """Only None means no filter. An empty filter selects nothing, for every device."""
    assert not read(temperature, **filters)


def test_invalid_event_raises_value_error(temperature):
    """An unknown callback id is rejected, when the generator is started."""
    with pytest.raises(ValueError):
        read(temperature, events=[9999])


@pytest.fixture(name="dual_current")
def dual_current_fixture():
    """A Bricklet, that reports the channel in the payload and receives a callback of both channels."""
    callback_id = BrickletIndustrialDual020mAV2.CallbackID
    packets = [
        (callback_id.CURRENT, pack_payload((0, 4_000_000), "B i")),
        (callback_id.CURRENT, pack_payload((1, 20_000_000), "B i")),
    ]
    return BrickletIndustrialDual020mAV2(12345, FakeIpConnection(packets))


def test_channel_in_payload_is_the_sid(dual_current):
    """Devices, that return the channel in the payload, use it as the sid, and filter the other channels."""
    assert [(event.sid, event.payload) for event in read(dual_current)] == [(0, Decimal("0.004")), (1, Decimal("0.02"))]
    assert [event.sid for event in read(dual_current, sids=[1])] == [1]


def test_io16_rejects_events_and_sids_together_and_unknown_sids():
    """The IO-16 uses sids as pins, so it validates them and does not combine the filters."""
    device = BrickletIO16(12345, FakeIpConnection([]))
    callback_id = BrickletIO16.CallbackID
    with pytest.raises(ValueError):
        read(device, events=[callback_id.INTERRUPT], sids=[0])
    with pytest.raises(ValueError):
        read(device, sids=[16])


def test_io16_yields_one_event_per_changed_pin():
    """The payload of one callback results in one event per changed pin."""
    callback_id = BrickletIO16.CallbackID
    port_a = b"a"
    packets = [(callback_id.INTERRUPT, pack_payload((port_a, 0b0000_0101, 0b0000_0100), "c B B"))]
    device = BrickletIO16(12345, FakeIpConnection(packets))
    assert [(event.sid, event.payload) for event in read(device, sids=[0, 1, 2])] == [(0, False), (2, True)]
