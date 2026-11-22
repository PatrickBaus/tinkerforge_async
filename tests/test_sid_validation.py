"""Tests for the validation of secondary ids (sids)."""

import asyncio
import inspect
import subprocess
import sys
from collections.abc import Iterator
from unittest.mock import Mock

import pytest

import tinkerforge_async
from tinkerforge_async.bricklet_ptc import BrickletPtc
from tinkerforge_async.bricklet_ptc_v2 import BrickletPtcV2
from tinkerforge_async.bricklet_thermocouple_v2 import BrickletThermocoupleV2
from tinkerforge_async.devices import InvalidSidError

from .device_tests import RegisteredDevice, registered_devices

SID_METHODS = ("get_value", "set_callback_configuration", "get_callback_configuration")


def sid_methods() -> Iterator[object]:
    """All (device class, method name) pairs of the registered devices, that take a sid."""
    for device_class in sorted(registered_devices(), key=lambda cls: cls.__name__):
        for name in SID_METHODS:
            method = getattr(device_class, name, None)
            if method is not None and "sid" in inspect.signature(method).parameters:
                yield pytest.param(device_class, name, id=f"{device_class.__name__}.{name}")


def test_invalid_sid_error_is_a_value_error() -> None:
    """InvalidSidError inherits from ValueError for backwards compatibility and is exported by the package."""
    assert issubclass(InvalidSidError, ValueError)
    assert tinkerforge_async.InvalidSidError is InvalidSidError


@pytest.mark.parametrize("device_class,method_name", list(sid_methods()))
def test_unknown_sid_raises_invalid_sid_error(device_class: RegisteredDevice, method_name: str) -> None:
    """Every function, that takes a sid, rejects a sid that does not exist with an InvalidSidError."""
    device = device_class(12345, Mock())

    with pytest.raises(InvalidSidError, match="Invalid sid 99"):
        asyncio.run(getattr(device, method_name)(99))


@pytest.mark.parametrize("device_class", [BrickletPtc, BrickletPtcV2])
@pytest.mark.parametrize("method_name", ["set_callback_configuration", "get_callback_configuration"])
def test_ptc_sensor_connected_callback_cannot_be_configured(
    device_class: type[BrickletPtcV2] | type[BrickletPtc], method_name: str
) -> None:
    """Sid 2 (sensor connected) of the PTC Bricklets exists, but has no callback configuration."""
    device = device_class(12345, Mock())

    with pytest.raises(InvalidSidError, match="Invalid sid 2"):
        asyncio.run(getattr(device, method_name)(2))


@pytest.mark.parametrize("method_name", ["set_callback_configuration", "get_callback_configuration"])
def test_thermocouple_error_state_cannot_be_configured(method_name: str) -> None:
    """Sid 1 (error state) of the Thermocouple Bricklet 2.0 exists, but has no callback configuration."""
    device = BrickletThermocoupleV2(12345, Mock())

    with pytest.raises(InvalidSidError, match="Invalid sid 1"):
        asyncio.run(getattr(device, method_name)(1))


def test_sid_validation_works_without_assert_statements() -> None:
    """The sids are also validated when Python runs with -OO, which removes assert statements."""
    script = """
import asyncio
from unittest.mock import Mock
from tinkerforge_async.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge_async.devices import InvalidSidError
try:
    asyncio.run(BrickletTemperatureV2(12345, Mock()).set_callback_configuration(5))
except InvalidSidError:
    print("rejected")
"""
    result = subprocess.run([sys.executable, "-OO", "-c", script], capture_output=True, text=True, check=True)

    assert result.stdout.strip() == "rejected"
