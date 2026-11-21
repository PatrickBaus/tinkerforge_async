"""Tests for the Industrial PTC Bricklet. It has the API of the PTC Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from decimal import Decimal

from tinkerforge_async.bricklet_industrial_ptc import BrickletIndustrialPtc
from tinkerforge_async.bricklet_ptc_v2 import BrickletPtcV2

from .device_tests import DeviceTests
from .fake_connection import read_events, summary
from .test_bricklet_ptc_v2 import CALLS, REJECTED

__all__ = ["CALLS", "REJECTED"]  # The tables of the PTC Bricklet 2.0 are used by `DeviceTests`

DEVICE = BrickletIndustrialPtc
CallbackID = BrickletIndustrialPtc.CallbackID


def test_identity(bricklet):
    """The Bricklet knows who it is. It is a PTC Bricklet 2.0 with another name."""
    assert isinstance(bricklet, BrickletPtcV2)
    assert bricklet.DEVICE_IDENTIFIER.value == 2164
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("Industrial PTC Bricklet with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_events(bricklet, connection):
    """The temperature is sid 0, the resistance sid 1 and the state of the sensor sid 2."""
    connection.callback(CallbackID.TEMPERATURE, "i", 2500)
    connection.callback(CallbackID.RESISTANCE, "i", 8192)
    connection.callback(CallbackID.SENSOR_CONNECTED, "!", True)
    assert summary(read_events(bricklet)) == [
        (0, CallbackID.TEMPERATURE, Decimal("298.15")),
        (1, CallbackID.RESISTANCE, Decimal("97.5")),
        (2, CallbackID.SENSOR_CONNECTED, True),
    ]
