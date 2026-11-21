"""Tests for the functions, that all Bricks and Bricklets inherit from their base classes."""

import time
from decimal import Decimal

from tinkerforge_async.bricklet_temperature import BrickletTemperature
from tinkerforge_async.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge_async.devices import (
    BootloaderMode,
    BootloaderStatus,
    BrickletPort,
    BrickletWithMCU,
    Device,
    DeviceIdentifier,
    Event,
    FunctionID,
    GetIdentity,
    GetSPITFPErrorCount,
    LedConfig,
)

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, read_events, request, run

# A Bricklet with a microcontroller. It has all the functions, that the devices inherit from their base classes.
DEVICE = BrickletTemperatureV2
IDENTITY = "8s 8s c 3B 3B H"

CALLS = [
    # The functions of the Bricklets with a microcontroller
    Call("get_chip_temperature", FunctionID.GET_CHIP_TEMPERATURE, reply=("h", (25,)), result=Decimal("298.15")),
    Call("get_chip_temperature", FunctionID.GET_CHIP_TEMPERATURE, reply=("h", (-10,)), result=Decimal("263.15")),
    Call("reset", FunctionID.RESET, response_expected=False),
    Call(
        "set_bootloader_mode",
        FunctionID.SET_BOOTLOADER_MODE,
        (BootloaderMode.BOOTLOADER,),
        sent=("B", (0,)),
        reply=("B", (0,)),
        result=BootloaderStatus.OK,
    ),
    Call(
        "set_bootloader_mode",
        FunctionID.SET_BOOTLOADER_MODE,
        (1,),
        sent=("B", (1,)),
        reply=("B", (5,)),
        result=BootloaderStatus.CRC_MISMATCH,
    ),
    Call(
        "get_bootloader_mode",
        FunctionID.GET_BOOTLOADER_MODE,
        reply=("B", (4,)),
        result=BootloaderMode.FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT,
    ),
    Call(
        "set_write_firmware_pointer",
        FunctionID.SET_WRITE_FIRMWARE_POINTER,
        (0,),
        sent=("I", (0,)),
        response_expected=False,
    ),
    Call(
        "set_write_firmware_pointer",
        FunctionID.SET_WRITE_FIRMWARE_POINTER,
        (2**32 - 64, True),
        sent=("I", (2**32 - 64,)),
    ),
    Call(
        "write_firmware",
        FunctionID.WRITE_FIRMWARE,
        (range(64),),
        sent=("64B", (tuple(range(64)),)),
        reply=("B", (0,)),
        result=0,
    ),
    Call(
        "write_firmware",
        FunctionID.WRITE_FIRMWARE,
        (bytes(64),),
        sent=("64B", ((0,) * 64,)),
        reply=("B", (1,)),
        result=1,
    ),
    Call("set_status_led_config", FunctionID.SET_STATUS_LED_CONFIG, sent=("B", (3,)), response_expected=False),
    Call("set_status_led_config", FunctionID.SET_STATUS_LED_CONFIG, (LedConfig.OFF, True), sent=("B", (0,))),
    Call("set_status_led_config", FunctionID.SET_STATUS_LED_CONFIG, (2, True), sent=("B", (2,))),
    Call("get_status_led_config", FunctionID.GET_STATUS_LED_CONFIG, reply=("B", (2,)), result=LedConfig.SHOW_HEARTBEAT),
    Call("write_uid", FunctionID.WRITE_BRICKLET_UID, (0,), sent=("I", (0,)), response_expected=False),
    Call("write_uid", FunctionID.WRITE_BRICKLET_UID, (2**32 - 1, True), sent=("I", (2**32 - 1,))),
    Call("read_uid", FunctionID.READ_BRICKLET_UID, reply=("I", (UID,)), result=UID),
    Call(
        "get_spitfp_error_count",
        FunctionID.GET_SPITFP_ERROR_COUNT,
        reply=("I I I I", (1, 2, 3, 4)),
        result=GetSPITFPErrorCount(1, 2, 3, 4),
    ),
    # The functions of all devices. The uids are transferred in base58, "4ER" is 12345, "21" is 58.
    Call(
        "get_identity",
        FunctionID.GET_IDENTITY,
        reply=(IDENTITY, (b"4ER", b"21", "c", (1, 0, 0), (2, 0, 1), 2113)),
        result=GetIdentity(UID, 58, BrickletPort.C, (1, 0, 0), (2, 0, 1), DeviceIdentifier.BRICKLET_TEMPERATURE_V2),
    ),
    # A Brick that is not stacked on another Brick, is not connected to anything. Its position is a number.
    Call(
        "get_identity",
        FunctionID.GET_IDENTITY,
        reply=(IDENTITY, (b"4ER", b"0", "0", (2, 1, 0), (2, 5, 1), 13)),
        result=GetIdentity(UID, None, 0, (2, 1, 0), (2, 5, 1), DeviceIdentifier.BRICK_MASTER),
    ),
    Call(
        "get_identity",
        FunctionID.GET_IDENTITY,
        reply=(IDENTITY, (b"4ER", b"21", "z", (1, 0, 0), (2, 0, 1), 2122)),
        result=GetIdentity(UID, 58, BrickletPort.Z, (1, 0, 0), (2, 0, 1), DeviceIdentifier.BRICKLET_ISOLATOR),
    ),
]

REJECTED = [
    ("set_bootloader_mode", (5,)),
    ("set_write_firmware_pointer", (-1,)),
    ("set_status_led_config", (4,)),
    ("write_uid", (-1,)),
]


def test_the_device_under_test_has_a_microcontroller():
    """The functions in `CALLS` are tested with a Bricklet, that inherits them."""
    assert issubclass(DEVICE, BrickletWithMCU)
    assert not issubclass(BrickletTemperature, BrickletWithMCU)


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_identity_of_a_device_without_microcontroller(connection):
    """The older Bricklets have the common functions of all devices."""
    connection.reply(FunctionID.GET_IDENTITY, IDENTITY, b"4ER", b"21", "a", (1, 1, 0), (2, 0, 3), 216)
    bricklet = BrickletTemperature(UID, connection)
    assert run(bricklet.get_identity()) == GetIdentity(
        UID, 58, BrickletPort.A, (1, 1, 0), (2, 0, 3), DeviceIdentifier.BRICKLET_TEMPERATURE
    )
    assert connection.requests == [request(FunctionID.GET_IDENTITY)]
    assert not hasattr(bricklet, "get_chip_temperature")


def test_properties(bricklet, connection):
    """A device knows its uid and its connection."""
    assert bricklet.uid == UID
    assert bricklet.ipcon is connection
    assert str(bricklet) == f"Temperature Bricklet 2.0 with uid 12345 connected at {connection}"
    assert repr(bricklet) == (
        f"tinkerforge_async.bricklet_temperature_v2.BrickletTemperatureV2(uid=12345, ipcon={connection!r})"
    )


def test_uids_with_64_bits_are_shortened(connection):
    """The uids of the newer devices have 64 bits. The protocol uses 32 bits of them."""
    assert BrickletTemperatureV2(0xFFFF_FFFF, connection).uid == 0xFFFF_FFFF
    assert BrickletTemperatureV2(0x1_0000_0000, connection).uid == 0x1_0000
    assert BrickletTemperatureV2(0x3F0F_003F_0F00_0FFF, connection).uid == 0xFFFF_FFFF


def test_connect_and_disconnect_are_passed_on_to_the_connection(bricklet, connection):
    """A device can be used to connect, if the connection is not at hand."""
    run(bricklet.connect())
    assert connection.connected
    run(bricklet.disconnect())
    assert not connection.connected


def test_events_of_a_device_without_converter(connection):
    """By default, a device has one sid and its events have the raw value of the callback."""

    class Raw(Device):
        """A device that does not convert its callbacks"""

        CallbackID = BrickletTemperatureV2.CallbackID
        CALLBACK_FORMATS = {BrickletTemperatureV2.CallbackID.TEMPERATURE: "h"}
        SID_TO_CALLBACK = {0: (BrickletTemperatureV2.CallbackID.TEMPERATURE,)}

    connection.callback(BrickletTemperatureV2.CallbackID.TEMPERATURE, "h", 2500)
    (event,) = read_events(Raw("Raw device", UID, connection))
    assert (event.sid, event.payload) == (0, 2500)


def test_event():
    """An event has the time it was created, and can be printed."""
    connection = FakeConnection()
    bricklet = BrickletTemperatureV2(UID, connection)
    before = time.time()
    event = Event(bricklet, 0, BrickletTemperatureV2.CallbackID.TEMPERATURE, Decimal("298.15"))
    assert before <= event.timestamp <= time.time()
    assert event.additional is None
    assert str(event) == (
        f"Event(timestamp={event.timestamp}, sender={bricklet}, sid=0, "
        "function_id=CallbackID.TEMPERATURE, payload=298.15)"
    )
