"""Tests for the time unit convention: all durations are given in s, while the Tinkerforge protocol uses ms."""

import asyncio
import struct
from decimal import Decimal
from unittest.mock import AsyncMock, Mock

import pytest

from tinkerforge_async.brick_master import BrickMaster
from tinkerforge_async.bricklet_barometer import BrickletBarometer
from tinkerforge_async.bricklet_barometer_v2 import BrickletBarometerV2
from tinkerforge_async.bricklet_io4_v2 import BrickletIO4V2
from tinkerforge_async.bricklet_io16 import BrickletIO16
from tinkerforge_async.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
from tinkerforge_async.helper import ms_to_seconds, seconds_to_ms


def fake_ipcon(response: bytes = b"") -> Mock:
    """An IP connection, that answers every request with the payload."""
    ipcon = Mock()
    ipcon.send_request = AsyncMock(return_value=(None, response))
    return ipcon


def sent_payload(ipcon: Mock) -> bytes:
    """The payload of the last request."""
    return ipcon.send_request.call_args.kwargs["data"]


@pytest.mark.parametrize(
    "seconds,milliseconds", [(0, 0), (1, 1000), (0.5, 500), (0.29, 290), (Decimal("0.1"), 100), (1.5, 1500)]
)
def test_seconds_to_ms(seconds, milliseconds):
    """Seconds are converted to integer milliseconds without floating point errors."""
    result = seconds_to_ms(seconds)
    assert result == milliseconds
    assert isinstance(result, int)


def test_ms_to_seconds():
    """Milliseconds are converted to a Decimal in seconds."""
    assert ms_to_seconds(1500) == Decimal("1.5")
    assert isinstance(ms_to_seconds(1500), Decimal)


def test_callback_period_is_sent_in_ms():
    """A period of 0.5 s is 500 ms."""
    ipcon = fake_ipcon()
    asyncio.run(BrickletBarometer(1, ipcon).set_air_pressure_callback_period(0.5))
    assert struct.unpack("<I", sent_payload(ipcon)) == (500,)


def test_callback_period_is_read_in_seconds():
    """A period of 250 ms is 0.25 s."""
    ipcon = fake_ipcon(struct.pack("<I", 250))
    assert asyncio.run(BrickletBarometer(1, ipcon).get_air_pressure_callback_period()) == Decimal("0.25")


def test_debounce_period_defaults_to_100_ms():
    """The default debounce period is 0.1 s, which is the 100 ms default of the Bricklet."""
    ipcon = fake_ipcon()
    asyncio.run(BrickletBarometer(1, ipcon).set_debounce_period())
    assert struct.unpack("<I", sent_payload(ipcon)) == (100,)


def test_master_debounce_period():
    """The Master Brick takes and returns seconds, too."""
    ipcon = fake_ipcon(struct.pack("<I", 100))
    master = BrickMaster(1, ipcon)
    assert asyncio.run(master.get_debounce_period()) == Decimal("0.1")
    asyncio.run(master.set_debounce_period(2))
    assert struct.unpack("<I", sent_payload(ipcon)) == (2000,)


def test_callback_configuration_period_is_in_seconds():
    """Sending and reading the callback configuration uses seconds."""
    ipcon = fake_ipcon()
    asyncio.run(BrickletBarometerV2(1, ipcon).set_air_pressure_callback_configuration(1.5))
    assert struct.unpack("<I?cii", sent_payload(ipcon))[0] == 1500

    ipcon = fake_ipcon(struct.pack("<I?cii", 1500, False, b"x", 0, 0))
    config = asyncio.run(BrickletBarometerV2(1, ipcon).get_air_pressure_callback_configuration())
    assert config.period == Decimal("1.5")


def test_monoflop_time_is_in_seconds():
    """Sending a monoflop time of 1.5 s sends 1500 ms and the remaining time is returned in seconds."""
    ipcon = fake_ipcon()
    asyncio.run(BrickletIO4V2(1, ipcon).set_monoflop(0, True, 1.5))
    assert struct.unpack("<B?I", sent_payload(ipcon)) == (0, True, 1500)

    ipcon = fake_ipcon(struct.pack("<?II", True, 1500, 500))
    result = asyncio.run(BrickletIO4V2(1, ipcon).get_monoflop(0))
    assert (result.value, result.time, result.time_remaining) == (True, Decimal("1.5"), Decimal("0.5"))


def test_io16_edge_count_debounce_is_in_seconds():
    """The debounce time is stored in a byte of ms, so it is limited to 0.255 s."""
    ipcon = fake_ipcon()
    device = BrickletIO16(1, ipcon)
    asyncio.run(device.set_edge_count_config(0))
    assert struct.unpack("<BBB", sent_payload(ipcon)) == (0, 0, 100)
    with pytest.raises(AssertionError):
        asyncio.run(device.set_edge_count_config(0, debounce=0.3))

    ipcon = fake_ipcon(struct.pack("<BB", 0, 5))
    assert asyncio.run(BrickletIO16(1, ipcon).get_edge_count_config(0)).debounce == Decimal("0.005")


def test_segment_display_counter_length_is_in_seconds():
    """The pause between two steps of the counter is given in seconds."""
    ipcon = fake_ipcon()
    asyncio.run(BrickletSegmentDisplay4x7(1, ipcon).start_counter(0, 100))
    assert struct.unpack("<hhhI", sent_payload(ipcon)) == (0, 100, 1, 1000)
