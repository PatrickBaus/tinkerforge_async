"""Tests for the factory, that creates the devices from their device identifier."""

import pytest

from tinkerforge_async import device_factory
from tinkerforge_async.brick_master import BrickMaster
from tinkerforge_async.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge_async.device_factory import DeviceFactory
from tinkerforge_async.devices import Device, DeviceIdentifier

from .fake_connection import UID

# There is no driver for the Ambient Light Bricklet 1.0
SUPPORTED = [identifier for identifier in DeviceIdentifier if identifier is not DeviceIdentifier.BRICKLET_AMBIENT_LIGHT]


@pytest.mark.parametrize("device_identifier", SUPPORTED, ids=lambda identifier: identifier.name)
def test_all_devices_with_an_identifier_are_registered(connection, device_identifier):
    """The factory creates the device for an identifier, as it is sent by the device when it is enumerated."""
    device = device_factory.get(connection, device_identifier, UID)
    assert isinstance(device, Device)
    assert device.DEVICE_IDENTIFIER is device_identifier
    assert device.uid == UID
    assert device.ipcon is connection


def test_get_creates_the_registered_class(connection):
    """Bricks and Bricklets are created alike."""
    assert isinstance(device_factory.get(connection, DeviceIdentifier.BRICK_MASTER, UID), BrickMaster)
    assert isinstance(
        device_factory.get(connection, DeviceIdentifier.BRICKLET_TEMPERATURE_V2, UID), BrickletTemperatureV2
    )


@pytest.mark.parametrize("device_identifier", [DeviceIdentifier.BRICKLET_AMBIENT_LIGHT, 9999, None])
def test_unknown_devices_raise_a_value_error(connection, device_identifier):
    """There is no driver for the device."""
    with pytest.raises(ValueError, match="No device available"):
        device_factory.get(connection, device_identifier, UID)


def test_register():
    """A device is found by its identifier after it was registered."""
    factory = DeviceFactory()
    with pytest.raises(ValueError):
        factory.get(None, DeviceIdentifier.BRICKLET_TEMPERATURE_V2, UID)

    factory.register(BrickletTemperatureV2)
    device = factory.get(None, DeviceIdentifier.BRICKLET_TEMPERATURE_V2, UID)
    assert isinstance(device, BrickletTemperatureV2)
