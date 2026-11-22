"""Tests for the factory, that creates the devices from their device identifier."""

import pytest

from tinkerforge_async import device_factory
from tinkerforge_async.brick_master import BrickMaster
from tinkerforge_async.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge_async.device_factory import DeviceFactory
from tinkerforge_async.devices import Device, DeviceIdentifier

from .fake_connection import UID, FakeConnection

# There is no driver for the Ambient Light Bricklet 1.0
SUPPORTED = [identifier for identifier in DeviceIdentifier if identifier is not DeviceIdentifier.BRICKLET_AMBIENT_LIGHT]


@pytest.mark.parametrize("device_identifier", SUPPORTED, ids=lambda identifier: identifier.name)
def test_all_devices_with_an_identifier_are_registered(
    connection: FakeConnection, device_identifier: DeviceIdentifier
) -> None:
    """The factory creates the device for an identifier, as it is sent by the device when it is enumerated."""
    device = device_factory.get(connection.ipcon, device_identifier, UID)
    assert isinstance(device, Device)
    assert device.DEVICE_IDENTIFIER is device_identifier
    assert device.uid == UID
    assert device.ipcon is connection.ipcon


def test_get_creates_the_registered_class(connection: FakeConnection) -> None:
    """Bricks and Bricklets are created alike."""
    assert isinstance(device_factory.get(connection.ipcon, DeviceIdentifier.BRICK_MASTER, UID), BrickMaster)
    assert isinstance(
        device_factory.get(connection.ipcon, DeviceIdentifier.BRICKLET_TEMPERATURE_V2, UID), BrickletTemperatureV2
    )


@pytest.mark.parametrize("device_identifier", [9999, None])
def test_unknown_devices_raise_a_value_error(connection: FakeConnection, device_identifier: int | None) -> None:
    """There is no driver for the device."""
    with pytest.raises(ValueError, match="No device available"):
        device_factory.get(connection.ipcon, device_identifier, UID)


def test_unregistered_devices_raise_a_value_error(connection: FakeConnection) -> None:
    """A known device, that was not registered with the factory, can not be created."""
    with pytest.raises(ValueError, match="No device available"):
        DeviceFactory().get(connection.ipcon, DeviceIdentifier.BRICKLET_AMBIENT_LIGHT, UID)


def test_all_device_identifiers_have_a_driver() -> None:
    """Every Brick and Bricklet, that the library knows, can be created by the factory."""
    connection = FakeConnection().ipcon
    for device_identifier in DeviceIdentifier:
        assert device_factory.get(connection, device_identifier, UID).DEVICE_IDENTIFIER is device_identifier


def test_register() -> None:
    """A device is found by its identifier after it was registered."""
    factory = DeviceFactory()
    connection = FakeConnection().ipcon
    with pytest.raises(ValueError):
        factory.get(connection, DeviceIdentifier.BRICKLET_TEMPERATURE_V2, UID)

    factory.register(BrickletTemperatureV2)
    device = factory.get(connection, DeviceIdentifier.BRICKLET_TEMPERATURE_V2, UID)
    assert isinstance(device, BrickletTemperatureV2)
