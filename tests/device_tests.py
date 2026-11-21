"""The tests that are the same for all Bricks and Bricklets. They are driven by tables in the test modules."""

from .fake_connection import check, check_rejected

# Addresses for the tests of the network settings
IP = (192, 168, 1, 2)
MASK = (255, 255, 255, 0)
GATEWAY = (192, 168, 1, 1)
MAC = (0x40, 0xD8, 0x55, 0x02, 0xA0, 0x00)
BSSID = (1, 2, 3, 4, 5, 6)
NULL = (0, 0, 0, 0)


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

    def test_requests_and_results(self, device, connection, call):
        """The functions send the correct request, and convert the reply to SI units."""
        check(device, connection, call)

    def test_invalid_arguments_are_rejected(self, device, connection, rejected):
        """Invalid arguments raise a ValueError, and nothing is sent to the device."""
        method, arguments = rejected
        check_rejected(device, connection, method, *arguments)
