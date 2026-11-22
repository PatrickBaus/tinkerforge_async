"""The fixtures shared by the tests."""

from typing import Any

import pytest

from .fake_connection import UID, FakeConnection


@pytest.fixture(name="connection")
def connection_fixture() -> FakeConnection:
    """An IP connection, that records the requests and returns canned replies."""
    return FakeConnection()


@pytest.fixture(name="device")
def device_fixture(request: pytest.FixtureRequest, connection: FakeConnection) -> Any:
    """The Brick or Bricklet under test. It is created from the class, that the test module names in `DEVICE`."""
    return request.module.DEVICE(UID, connection)


@pytest.fixture(name="bricklet")
def bricklet_fixture(device: Any) -> Any:
    """The Bricklet under test"""
    return device


@pytest.fixture(name="brick")
def brick_fixture(device: Any) -> Any:
    """The Brick under test"""
    return device


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Run the tests of `DeviceTests` once for every entry in the tables `CALLS` and `REJECTED` of the test module."""
    if "call" in metafunc.fixturenames:
        metafunc.parametrize("call", metafunc.module.CALLS, ids=str)
    if "rejected" in metafunc.fixturenames:
        metafunc.parametrize("rejected", metafunc.module.REJECTED, ids=lambda entry: f"{entry[0]}{entry[1]}")
