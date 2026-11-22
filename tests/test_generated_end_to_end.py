"""
End-to-end tests of the generated devices. They talk to a fake Brick Daemon over the real IP connection, so the
enumeration, the device factory and the packets on the wire are tested together.
"""

import asyncio
import struct
import sys
from decimal import Decimal

import pytest

from tinkerforge_async import IPConnectionAsync
from tinkerforge_async.bricklet_rs485 import BrickletRS485
from tinkerforge_async.bricklet_voltage_current_v2 import BrickletVoltageCurrentV2
from tinkerforge_async.device_factory import device_factory
from tinkerforge_async.devices import DeviceIdentifier
from tinkerforge_async.ip_connection import EnumerationType, FunctionID
from tinkerforge_async.ip_connection_helper import base58encode, pack_payload

from .fake_brickd import FakeBrickd, callback, reply
from .fake_connection import run, take

HOST = "127.0.0.1"
ENUMERATION = "8s 8s c 3B 3B H B"


def generated_devices():
    """All registered devices, that were generated from the Tinkerforge API definitions."""
    devices = device_factory._DeviceFactory__available_devices.values()  # pylint: disable=protected-access
    marker = "generated from the Tinkerforge API definitions"
    return sorted(
        (cls for cls in devices if marker in (sys.modules[cls.__module__].__doc__ or "")),
        key=lambda cls: cls.DEVICE_IDENTIFIER.value,
    )


GENERATED = generated_devices()


def enumeration(uid: int, device_identifier: int) -> bytes:
    """The callback, that a device sends when it is enumerated."""
    payload = pack_payload(
        (
            base58encode(uid).encode(),
            b"21",
            "a",
            (1, 0, 0),
            (2, 0, 1),
            device_identifier,
            EnumerationType.AVAILABLE.value,
        ),
        ENUMERATION,
    )
    return callback(uid, FunctionID.CALLBACK_ENUMERATE.value, payload).pack()


def test_all_devices_are_generated():
    """All 124 generated Bricks and Bricklets (85 current, 39 discontinued) are registered with the factory."""
    assert len(GENERATED) == 124
    for cls in GENERATED:
        assert DeviceIdentifier(cls.DEVICE_IDENTIFIER.value) is cls.DEVICE_IDENTIFIER


def test_enumeration_creates_all_generated_devices():
    """The connection creates the matching object for every generated device, that answers the enumeration."""

    def responder(_request):
        return b"".join(enumeration(1000 + i, cls.DEVICE_IDENTIFIER.value) for i, cls in enumerate(GENERATED))

    async def scenario():
        async with FakeBrickd(responder) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            listener = asyncio.create_task(take(connection.read_enumeration(), len(GENERATED)))
            for _ in range(5):
                await asyncio.sleep(0)
            await connection.enumerate()
            return await listener

    devices = [device for _, device in run(scenario())]
    assert [type(device) for device in devices] == GENERATED
    assert [device.uid for device in devices] == [1000 + i for i in range(len(GENERATED))]


@pytest.mark.parametrize("value", [12345, -2000])
def test_get_voltage_over_the_wire(value):
    """The request is sent to the Brick Daemon, and the raw reply in mV is returned in V."""

    def responder(request):
        if request.function_id == BrickletVoltageCurrentV2.FunctionID.GET_VOLTAGE.value:
            return reply(request, struct.pack("<i", value))
        return None

    async def scenario():
        async with FakeBrickd(responder) as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            bricklet = BrickletVoltageCurrentV2(4711, connection)
            result = await bricklet.get_voltage()
            return result, brickd.received

    result, received = run(scenario())
    assert result == Decimal(value) / 1000
    assert [(packet.uid, packet.function_id, packet.response_expected) for packet in received] == [(4711, 5, True)]


def test_stream_callback_over_the_wire():
    """The RS485 Bricklet sends the received data in chunks of 60 characters. The chunks are reassembled."""
    message = "".join(chr(ord("a") + i % 26) for i in range(100))
    read = BrickletRS485.CallbackID.READ.value

    def chunk(offset):
        data = list(message[offset : offset + 60])
        data += ["\0"] * (60 - len(data))
        return callback(4711, read, pack_payload((len(message), offset, data), "H H 60c")).pack()

    async def scenario():
        async with FakeBrickd() as brickd, IPConnectionAsync(HOST, brickd.port) as connection:
            bricklet = BrickletRS485(4711, connection)
            listener = asyncio.create_task(take(bricklet.read_events(), 1))
            await brickd.wait_for_connections(1)
            for _ in range(5):
                await asyncio.sleep(0)
            brickd.send(chunk(0) + chunk(60))
            return await listener

    [event] = run(scenario())
    assert event.function_id is BrickletRS485.CallbackID.READ
    assert event.payload == message
