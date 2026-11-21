"""Tests for the temperature unit convention: all temperatures are given in K."""

import asyncio
import pathlib
import struct
from decimal import Decimal
from unittest.mock import AsyncMock, Mock

import tinkerforge_async
from tinkerforge_async.bricklet_barometer import BrickletBarometer
from tinkerforge_async.bricklet_barometer_v2 import BrickletBarometerV2
from tinkerforge_async.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge_async.devices import DeviceWithMCU


def fake_ipcon(response: bytes = b"") -> Mock:
    """An IP connection, that answers every request with the payload."""
    ipcon = Mock()
    ipcon.send_request = AsyncMock(return_value=(None, response))
    return ipcon


def sent_payload(ipcon: Mock) -> bytes:
    """The payload of the last request."""
    return ipcon.send_request.call_args.kwargs["data"]


def test_barometer_v2_temperature_is_in_kelvin():
    """Raw 2345 (23.45 °C) is 296.60 K."""
    ipcon = fake_ipcon(struct.pack("<i", 2345))
    assert asyncio.run(BrickletBarometerV2(1, ipcon).get_temperature()) == Decimal("296.60")


def test_barometer_v2_negative_temperature_is_in_kelvin():
    """Raw -1000 (-10 °C) is 263.15 K."""
    ipcon = fake_ipcon(struct.pack("<i", -1000))
    assert asyncio.run(BrickletBarometerV2(1, ipcon).get_temperature()) == Decimal("263.15")


def test_barometer_v2_temperature_threshold_is_sent_in_raw_units():
    """283.15 K is raw 1000, the default maximum 273.15 K is the device default 0."""
    ipcon = fake_ipcon()
    device = BrickletBarometerV2(1, ipcon)
    asyncio.run(device.set_temperature_callback_configuration(0, False, ">", Decimal("283.15")))
    assert struct.unpack("<I?cii", sent_payload(ipcon)) == (0, False, b">", 1000, 0)


def test_barometer_v2_temperature_threshold_is_read_in_kelvin():
    """Raw 1000 and 0 are 283.15 K and 273.15 K."""
    ipcon = fake_ipcon(struct.pack("<I?cii", 0, False, b">", 1000, 0))
    config = asyncio.run(BrickletBarometerV2(1, ipcon).get_temperature_callback_configuration())
    assert (config.minimum, config.maximum) == (Decimal("283.15"), Decimal("273.15"))


def test_barometer_v2_generic_configuration_defaults():
    """The default thresholds of every sid are the raw value 0."""
    for sid in (0, 1, 2):
        ipcon = fake_ipcon()
        asyncio.run(BrickletBarometerV2(1, ipcon).set_callback_configuration(sid, 1))
        assert struct.unpack("<I?cii", sent_payload(ipcon)) == (1000, False, b"x", 0, 0), sid


def test_barometer_v1_chip_temperature_is_in_kelvin():
    """Raw 2345 (1/100 °C) is 296.60 K, returned as a Decimal."""
    ipcon = fake_ipcon(struct.pack("<h", 2345))
    result = asyncio.run(BrickletBarometer(1, ipcon).get_chip_temperature())
    assert isinstance(result, Decimal)
    assert result == Decimal("296.60")


def test_mcu_chip_temperature_is_in_kelvin():
    """Raw 25 (°C) is 298.15 K."""
    ipcon = fake_ipcon(struct.pack("<h", 25))
    assert asyncio.run(BrickletTemperatureV2(1, ipcon).get_chip_temperature()) == Decimal("298.15")


def test_docstrings_do_not_claim_degrees_celsius_for_kelvin_values():
    """The docstrings describe the values returned by the library (K), not the raw values of the device (°C/100)."""
    package = pathlib.Path(tinkerforge_async.__file__).parent
    offenders = [path.name for path in package.glob("*.py") if "°C/100" in path.read_text(encoding="utf-8")]
    assert not offenders
    assert "in K" in DeviceWithMCU.get_chip_temperature.__doc__
    assert "in K" in BrickletBarometer.get_chip_temperature.__doc__
    assert "in K" in BrickletBarometerV2.get_temperature.__doc__


def test_docstrings_only_use_si_units():
    """All values are returned in SI units, so the docstrings must not use the raw units of the devices."""
    package = pathlib.Path(tinkerforge_async.__file__).parent
    forbidden = ("°C", "%RH/10", "lux/100", "in mV", "in mA", "hPa", "mbar", "0cm", "0mm")
    offenders = {
        f"{path.name}: {unit}"
        for path in package.glob("*.py")
        for unit in forbidden
        if unit in path.read_text(encoding="utf-8")
    }
    assert not offenders
