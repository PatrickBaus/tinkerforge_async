"""The tests that are the same for all Bricks and Bricklets. They are driven by tables in the test modules."""

from collections.abc import Mapping, Sequence
from typing import Any, Protocol

from tinkerforge_async.device_factory import DeviceClass, device_factory
from tinkerforge_async.devices import Channel, DeviceIdentifier

from .fake_connection import Call, FakeConnection, check, check_rejected

# Addresses for the tests of the network settings
IP = (192, 168, 1, 2)
MASK = (255, 255, 255, 0)
GATEWAY = (192, 168, 1, 1)
MAC = (0x40, 0xD8, 0x55, 0x02, 0xA0, 0x00)
BSSID = (1, 2, 3, 4, 5, 6)
NULL = (0, 0, 0, 0)


class RegisteredDevice(DeviceClass, Protocol):  # pylint: disable=too-few-public-methods
    """The class of a Brick or Bricklet, that is registered with the device factory."""

    __name__: str
    __module__: str
    CHANNELS: Sequence[Channel]
    CALLBACK_FORMATS: Mapping[Any, str]
    SID_TO_CALLBACK: Mapping[int, Sequence[Any]]


def registered_devices() -> list[RegisteredDevice]:
    """All Bricks and Bricklets, that are registered with the device factory."""
    devices: dict[DeviceIdentifier, RegisteredDevice] = getattr(device_factory, "_DeviceFactory__available_devices")
    return list(devices.values())


class DeviceTests:
    """
    Tests for the functions of a device. A test module subclasses it, so the tests are collected for the module, and
    defines:

    DEVICE: type
        The class of the Brick or Bricklet. The fixtures `device`, `bricklet` and `brick` are instances of it.
    CALLS: list of Call
        The calls of the functions with valid arguments, the requests they must send and the results they must return.
    REJECTED: list of tuple
        The names of functions and their invalid arguments.
    """

    def test_requests_and_results(self, device: Any, connection: FakeConnection, call: Call) -> None:
        """The functions send the correct request, and convert the reply to SI units."""
        check(device, connection, call)

    def test_invalid_arguments_are_rejected(
        self, device: Any, connection: FakeConnection, rejected: tuple[str, tuple[Any, ...]]
    ) -> None:
        """Invalid arguments raise a ValueError, and nothing is sent to the device."""
        method, arguments = rejected
        check_rejected(device, connection, method, *arguments)
