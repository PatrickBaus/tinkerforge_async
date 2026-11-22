"""Tests for the Chibi extension of the Master Brick."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

import pytest

from tinkerforge_async.brick_master import BrickMaster, ChibiFrequency, GetChibiErrorLog

from .device_tests import DeviceTests
from .fake_connection import Call, FakeConnection, request, run

DEVICE = BrickMaster
FunctionID = BrickMaster.FunctionID

CALLS = [
    Call("is_chibi_present", FunctionID.IS_CHIBI_PRESENT, reply=("!", (True,)), result=True),
    Call("set_chibi_address", FunctionID.SET_CHIBI_ADDRESS, (1,), sent=("B", (1,))),
    Call("set_chibi_address", FunctionID.SET_CHIBI_ADDRESS, (255, False), sent=("B", (255,)), response_expected=False),
    Call("get_chibi_address", FunctionID.GET_CHIBI_ADDRESS, reply=("B", (17,)), result=17),
    Call("set_chibi_master_address", FunctionID.SET_CHIBI_MASTER_ADDRESS, (1,), sent=("B", (1,))),
    Call("set_chibi_master_address", FunctionID.SET_CHIBI_MASTER_ADDRESS, (255,), sent=("B", (255,))),
    Call("get_chibi_master_address", FunctionID.GET_CHIBI_MASTER_ADDRESS, reply=("B", (17,)), result=17),
    Call("get_chibi_signal_strength", FunctionID.GET_CHIBI_SIGNAL_STRENGTH, reply=("B", (42,)), result=42),
    Call(
        "get_chibi_error_log",
        FunctionID.GET_CHIBI_ERROR_LOG,
        reply=("H H H H", (1, 2, 3, 4)),
        result=GetChibiErrorLog(1, 2, 3, 4),
    ),
    Call(
        "set_chibi_frequency",
        FunctionID.SET_CHIBI_FREQUENCY,
        (ChibiFrequency.BPSK40_915_MHZ,),
        sent=("B", (3,)),
    ),
    Call("set_chibi_frequency", FunctionID.SET_CHIBI_FREQUENCY, (0,), sent=("B", (0,))),
    Call("get_chibi_frequency", FunctionID.GET_CHIBI_FREQUENCY, reply=("B", (1,)), result=ChibiFrequency.OQPSK_915_MHZ),
    Call("set_chibi_channel", FunctionID.SET_CHIBI_CHANNEL, (3,), sent=("B", (3,))),
    Call("get_chibi_channel", FunctionID.GET_CHIBI_CHANNEL, reply=("B", (3,)), result=3),
]

REJECTED = [
    ("set_chibi_address", (0,)),
    ("set_chibi_address", (256,)),
    ("set_chibi_master_address", (0,)),
    ("set_chibi_master_address", (256,)),
    ("set_chibi_slave_addresses", ({17, 23},)),  # Not ordered
    ("set_chibi_slave_addresses", ([1] * 255,)),  # Too long, there is room for 254 addresses and the terminator
    ("set_chibi_frequency", (4,)),
]


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


@pytest.mark.parametrize(
    "addresses, sent",
    [
        ((17, 23, 42), (17, 23, 42, 0)),  # The list is terminated by the address 0
        ([17, 0], (17, 0)),  # It is already terminated
        ((), (0,)),  # Clears the list
        ([1] * 254, (1,) * 254 + (0,)),  # The maximum number of slaves
    ],
)
def test_set_chibi_slave_addresses(
    brick: BrickMaster, connection: FakeConnection, addresses: tuple[int, ...] | list[int], sent: tuple[int, ...]
) -> None:
    """The addresses are sent one by one with their index."""
    run(brick.set_chibi_slave_addresses(addresses))
    assert connection.requests == [
        request(FunctionID.SET_CHIBI_SLAVE_ADDRESS, "B B", index, address) for index, address in enumerate(sent)
    ]


def test_set_chibi_slave_addresses_rejects_invalid_addresses(brick: BrickMaster) -> None:
    """An address is a byte."""
    with pytest.raises(ValueError):
        run(brick.set_chibi_slave_addresses((17, 256), response_expected=False))
    with pytest.raises(ValueError):
        run(brick.set_chibi_slave_addresses((-1,)))


@pytest.mark.parametrize("addresses", [(), (17,), (17, 23, 42)])
def test_get_slave_addresses(brick: BrickMaster, connection: FakeConnection, addresses: tuple[int, ...]) -> None:
    """The addresses are read one by one until the terminator is found."""
    for address in (*addresses, 0):
        connection.reply(FunctionID.GET_CHIBI_SLAVE_ADDRESS, "B", address)
    assert run(brick.get_slave_addresses()) == addresses
    assert connection.requests == [
        request(FunctionID.GET_CHIBI_SLAVE_ADDRESS, "B", index) for index in range(len(addresses) + 1)
    ]
