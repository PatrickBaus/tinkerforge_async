"""Tests for the RS485 extension of the Master Brick."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from collections.abc import Sequence

import pytest

from tinkerforge_async.brick_master import BrickMaster, GetRS485Configuration, Rs485Parity

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, request, run

DEVICE = BrickMaster
FunctionID = BrickMaster.FunctionID

CALLS = [
    Call("is_rs485_present", FunctionID.IS_RS485_PRESENT, reply=("!", (True,)), result=True),
    # The address 0 is the master
    Call("set_rs485_address", FunctionID.SET_RS485_ADDRESS, (0,), sent=("B", (0,))),
    Call("set_rs485_address", FunctionID.SET_RS485_ADDRESS, (255, False), sent=("B", (255,)), response_expected=False),
    Call("get_rs485_address", FunctionID.GET_RS485_ADDRESS, reply=("B", (17,)), result=17),
    Call("get_rs485_error_log", FunctionID.GET_RS485_ERROR_LOG, reply=("H", (3,)), result=3),
    Call(
        "set_rs485_configuration",
        FunctionID.SET_RS485_CONFIGURATION,
        (2000000, Rs485Parity.EVEN, 1),
        sent=("I c B", (2000000, b"e", 1)),
    ),
    Call(
        "set_rs485_configuration",
        FunctionID.SET_RS485_CONFIGURATION,
        (9600, "n", 2),
        sent=("I c B", (9600, b"n", 2)),
    ),
    Call(
        "get_rs485_configuration",
        FunctionID.GET_RS485_CONFIGURATION,
        reply=("I c B", (9600, "o", 2)),
        result=GetRS485Configuration(9600, Rs485Parity.ODD, 2),
    ),
]

REJECTED = [
    ("set_rs485_address", (-1,)),
    ("set_rs485_address", (256,)),
    ("set_rs485_slave_addresses", ({17, 23},)),  # Not ordered
    ("set_rs485_slave_addresses", ([1] * 254,)),  # Too long
    ("set_rs485_configuration", (9600, "n", 0)),
    ("set_rs485_configuration", (9600, "n", 3)),
    ("set_rs485_configuration", (9600, "x", 1)),
]


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


@pytest.mark.parametrize(
    "addresses, sent",
    [
        ((17, 23, 42), (17, 23, 42, 0)),  # The list is terminated by the address 0
        ([17, 0], (17, 0)),  # It is already terminated
        ((), (0,)),  # Clears the list
        ([1] * 253, (1,) * 253 + (0,)),  # The maximum number of slaves
    ],
)
def test_set_rs485_slave_addresses(
    brick: BrickMaster, connection: FakeConnection, addresses: Sequence[int], sent: tuple[int, ...]
) -> None:
    """The addresses are sent one by one with their index."""
    run(brick.set_rs485_slave_addresses(addresses))
    assert connection.requests == [
        request(FunctionID.SET_RS485_SLAVE_ADDRESS, "B B", index, address) for index, address in enumerate(sent)
    ]


def test_set_rs485_slave_addresses_rejects_invalid_addresses(brick: BrickMaster) -> None:
    """An address is a byte."""
    with pytest.raises(ValueError):
        run(brick.set_rs485_slave_addresses((17, 256), response_expected=False))
    with pytest.raises(ValueError):
        run(brick.set_rs485_slave_addresses((-1,)))


@pytest.mark.parametrize("addresses", [(), (17,), (17, 23, 42)])
def test_get_rs485_slave_addresses(brick: BrickMaster, connection: FakeConnection, addresses: tuple[int, ...]) -> None:
    """The addresses are read one by one until the terminator is found."""
    for address in (*addresses, 0):
        connection.reply(FunctionID.GET_RS485_SLAVE_ADDRESS, "B", address)
    assert run(brick.get_rs485_slave_addresses()) == addresses
    assert connection.requests == [
        request(FunctionID.GET_RS485_SLAVE_ADDRESS, "B", index) for index in range(len(addresses) + 1)
    ]
