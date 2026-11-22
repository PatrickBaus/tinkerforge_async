"""Tests for the Wi-Fi 2.0 extension of the Master Brick."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from enum import Enum

import pytest

from tinkerforge_async.brick_master import (
    BrickMaster,
    GetWifi2APConfiguration,
    GetWifi2ClientConfiguration,
    GetWifi2Configuration,
    GetWifi2MeshAPStatus,
    GetWifi2MeshClientStatus,
    GetWifi2MeshCommonStatus,
    GetWifi2MeshConfiguration,
    GetWifi2Status,
    PhyMode,
    ReadWifi2SerialPort,
    Wifi2BootloaderError,
    WifiApEncryption,
    WifiClientStatus,
    WifiMeshStatus,
)

from .device_tests import BSSID, GATEWAY, IP, MAC, MASK, NULL, DeviceTests
from .fake_connection import Call, FakeConnection, request, run

DEVICE = BrickMaster
FunctionID = BrickMaster.FunctionID

GROUP = (0x1A, 0xFE, 0x34, 0x00, 0x00, 0x00)
NULL_MAC = (0, 0, 0, 0, 0, 0)

CLIENT = "! 32s 4B 4B 4B 6B 6B"
ACCESS_POINT = "! 32s 4B 4B 4B B ! B 6B"
MESH = "! 4B 4B 4B 6B 6B 16s 4B H"
STATUS = "! B 4B 4B 4B 6B I I b ! 4B 4B 4B 6B I I B"


def padded(data: bytes) -> tuple[int, ...]:
    """The data of a serial port packet. It always has 60 bytes."""
    return tuple(data.ljust(60, b"\0"))


CALLS = [
    Call("is_wifi2_present", FunctionID.IS_WIFI2_PRESENT, reply=("!", (True,)), result=True),
    Call(
        "write_wifi2_serial_port",
        FunctionID.WRITE_WIFI2_SERIAL_PORT,
        (b"\xc0\x00\x08",),
        sent=("60B B", (padded(b"\xc0\x00\x08"), 3)),
        reply=("b", (0,)),
    ),
    Call(
        "write_wifi2_serial_port",
        FunctionID.WRITE_WIFI2_SERIAL_PORT,
        ("ü" * 30,),
        sent=("60B B", (tuple("ü".encode() * 30), 60)),
        reply=("b", (0,)),
    ),
    Call(
        "read_wifi2_serial_port",
        FunctionID.READ_WIFI2_SERIAL_PORT,
        (60,),
        sent=("B", (60,)),
        reply=("60B B", (padded(b"\xc0\x01"), 2)),
        result=ReadWifi2SerialPort(padded(b"\xc0\x01"), 2),
    ),
    Call(
        "read_wifi2_serial_port",
        FunctionID.READ_WIFI2_SERIAL_PORT,
        (0,),
        sent=("B", (0,)),
        reply=("60B B", (padded(b""), 0)),
        result=ReadWifi2SerialPort(padded(b""), 0),
    ),
    Call(
        "set_wifi2_authentication_secret",
        FunctionID.SET_WIFI2_AUTHENTICATION_SECRET,
        ("secret",),
        sent=("64s", (b"secret",)),
    ),
    Call(
        "set_wifi2_authentication_secret",
        FunctionID.SET_WIFI2_AUTHENTICATION_SECRET,
        (b"x" * 64, False),
        sent=("64s", (b"x" * 64,)),
        response_expected=False,
    ),
    Call(
        "get_wifi2_authentication_secret",
        FunctionID.GET_WIFI2_AUTHENTICATION_SECRET,
        reply=("64s", (b"secret",)),
        result="secret",
    ),
    Call(
        "set_wifi2_configuration", FunctionID.SET_WIFI2_CONFIGURATION, sent=("H H H B B B", (4223, 4280, 80, 1, 0, 0))
    ),
    Call(
        "set_wifi2_configuration",
        FunctionID.SET_WIFI2_CONFIGURATION,
        (1, 65535, 8080, PhyMode.WIFI_N, 255, True),
        sent=("H H H B B B", (1, 65535, 8080, 2, 255, 1)),
    ),
    Call(
        "set_wifi2_configuration",
        FunctionID.SET_WIFI2_CONFIGURATION,
        (4223, 4280, 80, 0),
        sent=("H H H B B B", (4223, 4280, 80, 0, 0, 0)),
    ),
    Call(
        "get_wifi2_configuration",
        FunctionID.GET_WIFI2_CONFIGURATION,
        reply=("H H H B B B", (4223, 4280, 80, 2, 0, 1)),
        result=GetWifi2Configuration(4223, 4280, 80, PhyMode.WIFI_N, 0, True),
    ),
    Call(
        "get_wifi2_status",
        FunctionID.GET_WIFI2_STATUS,
        reply=(STATUS, (True, 5, IP, MASK, GATEWAY, MAC, 1000, 2000, -60, False, NULL, NULL, NULL, BSSID, 3, 4, 1)),
        result=GetWifi2Status(
            True,
            WifiClientStatus.GOT_IP,
            IP,
            MASK,
            GATEWAY,
            MAC,
            1000,
            2000,
            -60,
            False,
            NULL,
            NULL,
            NULL,
            BSSID,
            3,
            4,
            1,
        ),
    ),
    Call(
        "set_wifi2_client_configuration",
        FunctionID.SET_WIFI2_CLIENT_CONFIGURATION,
        sent=(CLIENT, (True, b"tinkerforge", NULL, NULL, NULL, NULL_MAC, NULL_MAC)),
    ),
    Call(
        "set_wifi2_client_configuration",
        FunctionID.SET_WIFI2_CLIENT_CONFIGURATION,
        (False, b"x" * 32, IP, list(MASK), GATEWAY, MAC, list(BSSID)),
        sent=(CLIENT, (False, b"x" * 32, IP, MASK, GATEWAY, MAC, BSSID)),
    ),
    Call(
        "get_wifi2_client_configuration",
        FunctionID.GET_WIFI2_CLIENT_CONFIGURATION,
        reply=(CLIENT, (True, b"my network", IP, MASK, GATEWAY, MAC, BSSID)),
        result=GetWifi2ClientConfiguration(True, "my network", IP, MASK, GATEWAY, MAC, BSSID),
    ),
    Call("set_wifi2_client_hostname", FunctionID.SET_WIFI2_CLIENT_HOSTNAME, sent=("32s", (b"wifi-extension-v2",))),
    # The hostname is converted to lower case
    Call(
        "set_wifi2_client_hostname",
        FunctionID.SET_WIFI2_CLIENT_HOSTNAME,
        ("Master-Brick",),
        sent=("32s", (b"master-brick",)),
    ),
    Call("set_wifi2_client_hostname", FunctionID.SET_WIFI2_CLIENT_HOSTNAME, (b"a" * 32,), sent=("32s", (b"a" * 32,))),
    Call(
        "get_wifi2_client_hostname",
        FunctionID.GET_WIFI2_CLIENT_HOSTNAME,
        reply=("32s", (b"master-brick",)),
        result="master-brick",
    ),
    Call(
        "set_wifi2_client_password", FunctionID.SET_WIFI2_CLIENT_PASSWORD, ("12345678",), sent=("64s", (b"12345678",))
    ),
    Call("set_wifi2_client_password", FunctionID.SET_WIFI2_CLIENT_PASSWORD, (b"p" * 63,), sent=("64s", (b"p" * 63,))),
    Call(
        "set_wifi2_ap_configuration",
        FunctionID.SET_WIFI2_AP_CONFIGURATION,
        sent=(ACCESS_POINT, (True, b"WIFI Extension 2.0 Access Point", NULL, NULL, NULL, 3, False, 1, NULL_MAC)),
    ),
    Call(
        "set_wifi2_ap_configuration",
        FunctionID.SET_WIFI2_AP_CONFIGURATION,
        (False, b"x" * 32, IP, list(MASK), GATEWAY, WifiApEncryption.OPEN, True, 13, list(MAC)),
        sent=(ACCESS_POINT, (False, b"x" * 32, IP, MASK, GATEWAY, 0, True, 13, MAC)),
    ),
    Call(
        "set_wifi2_ap_configuration",
        FunctionID.SET_WIFI2_AP_CONFIGURATION,
        (True, "ap", NULL, NULL, NULL, 4),
        sent=(ACCESS_POINT, (True, b"ap", NULL, NULL, NULL, 4, False, 1, NULL_MAC)),
    ),
    Call(
        "get_wifi2_ap_configuration",
        FunctionID.GET_WIFI2_AP_CONFIGURATION,
        reply=(ACCESS_POINT, (True, b"ap", IP, MASK, GATEWAY, 2, True, 6, MAC)),
        result=GetWifi2APConfiguration(True, "ap", IP, MASK, GATEWAY, WifiApEncryption.WPA_PSK, True, 6, MAC),
    ),
    Call("set_wifi2_ap_password", FunctionID.SET_WIFI2_AP_PASSWORD, ("12345678",), sent=("64s", (b"12345678",))),
    Call("set_wifi2_ap_password", FunctionID.SET_WIFI2_AP_PASSWORD, (b"p" * 63,), sent=("64s", (b"p" * 63,))),
    Call("save_wifi2_configuration", FunctionID.SAVE_WIFI2_CONFIGURATION, reply=("B", (0,)), result=0),
    Call(
        "get_wifi2_firmware_version",
        FunctionID.GET_WIFI2_FIRMWARE_VERSION,
        reply=("3B", ((2, 1, 5),)),
        result=(2, 1, 5),
    ),
    Call("set_wifi2_status_led", FunctionID.ENABLE_WIFI2_STATUS_LED, (True,)),
    Call("set_wifi2_status_led", FunctionID.DISABLE_WIFI2_STATUS_LED, (False, False), response_expected=False),
    Call("enable_wifi2_status_led", FunctionID.ENABLE_WIFI2_STATUS_LED),
    Call("disable_wifi2_status_led", FunctionID.DISABLE_WIFI2_STATUS_LED),
    Call("is_wifi2_status_led_enabled", FunctionID.IS_WIFI2_STATUS_LED_ENABLED, reply=("!", (True,)), result=True),
    Call(
        "set_wifi2_mesh_configuration",
        FunctionID.SET_WIFI2_MESH_CONFIGURATION,
        sent=(MESH, (False, NULL, NULL, NULL, NULL_MAC, GROUP, b"TF_MESH", NULL, 4240)),
    ),
    Call(
        "set_wifi2_mesh_configuration",
        FunctionID.SET_WIFI2_MESH_CONFIGURATION,
        (True, IP, list(MASK), GATEWAY, list(BSSID), MAC, b"p" * 16, list(GATEWAY), 65535),
        sent=(MESH, (True, IP, MASK, GATEWAY, BSSID, MAC, b"p" * 16, GATEWAY, 65535)),
    ),
    Call(
        "get_wifi2_mesh_configuration",
        FunctionID.GET_WIFI2_MESH_CONFIGURATION,
        reply=(MESH, (True, IP, MASK, GATEWAY, BSSID, GROUP, b"TF_MESH", GATEWAY, 4240)),
        result=GetWifi2MeshConfiguration(True, IP, MASK, GATEWAY, BSSID, GROUP, "TF_MESH", GATEWAY, 4240),
    ),
    Call("set_wifi2_mesh_router_ssid", FunctionID.SET_WIFI2_MESH_ROUTER_SSID, ("router",), sent=("32s", (b"router",))),
    Call("set_wifi2_mesh_router_ssid", FunctionID.SET_WIFI2_MESH_ROUTER_SSID, (b"x" * 32,), sent=("32s", (b"x" * 32,))),
    Call(
        "get_wifi2_mesh_router_ssid",
        FunctionID.GET_WIFI2_MESH_ROUTER_SSID,
        reply=("32s", (b"router",)),
        result="router",
    ),
    Call(
        "set_wifi2_mesh_router_password",
        FunctionID.SET_WIFI2_MESH_ROUTER_PASSWORD,
        ("12345678",),
        sent=("64s", (b"12345678",)),
    ),
    Call(
        "set_wifi2_mesh_router_password",
        FunctionID.SET_WIFI2_MESH_ROUTER_PASSWORD,
        (b"p" * 63,),
        sent=("64s", (b"p" * 63,)),
    ),
    Call(
        "get_wifi2_mesh_common_status",
        FunctionID.GET_WIFI2_MESH_COMMON_STATUS,
        reply=("B ! ! H I I", (4, True, False, 3, 1000, 2000)),
        result=GetWifi2MeshCommonStatus(WifiMeshStatus.MESH_ONLINE, True, False, 3, 1000, 2000),
    ),
    Call(
        "get_wifi2_mesh_client_status",
        FunctionID.GET_WIFI2_MESH_CLIENT_STATUS,
        reply=("32s 4B 4B 4B 6B", (b"node", IP, MASK, GATEWAY, MAC)),
        result=GetWifi2MeshClientStatus("node", IP, MASK, GATEWAY, MAC),
    ),
    Call(
        "get_wifi2_mesh_ap_status",
        FunctionID.GET_WIFI2_MESH_AP_STATUS,
        reply=("32s 4B 4B 4B 6B", (b"TF_MESH_1", IP, MASK, GATEWAY, MAC)),
        result=GetWifi2MeshAPStatus("TF_MESH_1", IP, MASK, GATEWAY, MAC),
    ),
]

REJECTED = [
    ("write_wifi2_serial_port", (bytes(61),)),
    ("read_wifi2_serial_port", (-1,)),
    ("read_wifi2_serial_port", (61,)),
    ("set_wifi2_authentication_secret", ("x" * 65,)),
    ("set_wifi2_configuration", (0,)),
    ("set_wifi2_configuration", (65536,)),
    ("set_wifi2_configuration", (4223, 0)),
    ("set_wifi2_configuration", (4223, 65536)),
    ("set_wifi2_configuration", (4223, 4280, 0)),
    ("set_wifi2_configuration", (4223, 4280, 65536)),
    ("set_wifi2_configuration", (4223, 4280, 80, 3)),
    ("set_wifi2_configuration", (4223, 4280, 80, 0, -1)),
    ("set_wifi2_configuration", (4223, 4280, 80, 0, 256)),
    ("set_wifi2_configuration", (4223, 4280, 80, 0, 0, 256)),
    ("set_wifi2_client_configuration", (True, "ssid", (1, 2, 3))),
    ("set_wifi2_client_configuration", (True, "ssid", IP, "255.255.255.0")),
    ("set_wifi2_client_configuration", (True, "ssid", IP, MASK, (1, 2, 3))),
    ("set_wifi2_client_configuration", (True, "ssid", IP, MASK, GATEWAY, MAC[:5])),
    ("set_wifi2_client_configuration", (True, "ssid", IP, MASK, GATEWAY, MAC, BSSID[:5])),
    ("set_wifi2_client_configuration", (True, "x" * 33)),
    ("set_wifi2_client_hostname", ("",)),
    ("set_wifi2_client_hostname", ("a",)),
    ("set_wifi2_client_hostname", ("a" * 33,)),
    ("set_wifi2_client_hostname", ("-master",)),
    ("set_wifi2_client_hostname", ("master_brick",)),
    ("set_wifi2_client_password", ("1234567",)),
    ("set_wifi2_client_password", ("p" * 64,)),
    ("set_wifi2_ap_configuration", (True, "ssid", (1, 2, 3))),
    ("set_wifi2_ap_configuration", (True, "ssid", IP, "255.255.255.0")),
    ("set_wifi2_ap_configuration", (True, "ssid", IP, MASK, (1, 2, 3))),
    ("set_wifi2_ap_configuration", (True, "ssid", IP, MASK, GATEWAY, 5)),
    ("set_wifi2_ap_configuration", (True, "ssid", IP, MASK, GATEWAY, 0, False, 0)),
    ("set_wifi2_ap_configuration", (True, "ssid", IP, MASK, GATEWAY, 0, False, 14)),
    ("set_wifi2_ap_configuration", (True, "ssid", IP, MASK, GATEWAY, 0, False, 1, MAC[:5])),
    ("set_wifi2_ap_configuration", (True, "x" * 33)),
    ("set_wifi2_ap_password", ("1234567",)),
    ("set_wifi2_ap_password", ("p" * 64,)),
    ("set_wifi2_mesh_configuration", (True, (1, 2, 3))),
    ("set_wifi2_mesh_configuration", (True, IP, "255.255.255.0")),
    ("set_wifi2_mesh_configuration", (True, IP, MASK, (1, 2, 3))),
    ("set_wifi2_mesh_configuration", (True, IP, MASK, GATEWAY, BSSID[:5])),
    ("set_wifi2_mesh_configuration", (True, IP, MASK, GATEWAY, BSSID, GROUP[:5])),
    ("set_wifi2_mesh_configuration", (True, IP, MASK, GATEWAY, BSSID, GROUP, "p" * 17)),
    ("set_wifi2_mesh_configuration", (True, IP, MASK, GATEWAY, BSSID, GROUP, "prefix", (1, 2, 3))),
    ("set_wifi2_mesh_configuration", (True, IP, MASK, GATEWAY, BSSID, GROUP, "prefix", IP, 0)),
    ("set_wifi2_mesh_configuration", (True, IP, MASK, GATEWAY, BSSID, GROUP, "prefix", IP, 65536)),
    ("set_wifi2_mesh_router_ssid", ("x" * 33,)),
    ("set_wifi2_mesh_router_password", ("1234567",)),
    ("set_wifi2_mesh_router_password", ("p" * 64,)),
]


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_start_wifi2_bootloader(brick: BrickMaster, connection: FakeConnection) -> None:
    """The bootloader can only be started, if the Brick is connected via USB."""
    connection.reply(FunctionID.GET_CONNECTION_TYPE, "B", 1)
    connection.reply(FunctionID.START_WIFI2_BOOTLOADER, "b", 0)
    run(brick.start_wifi2_bootloader())
    assert connection.requests == [
        request(FunctionID.GET_CONNECTION_TYPE),
        request(FunctionID.START_WIFI2_BOOTLOADER),
    ]


def test_start_wifi2_bootloader_fails_if_not_connected_via_usb(brick: BrickMaster, connection: FakeConnection) -> None:
    """The extension cannot be flashed over itself."""
    connection.reply(FunctionID.GET_CONNECTION_TYPE, "B", 7)
    with pytest.raises(RuntimeError, match="USB"):
        run(brick.start_wifi2_bootloader())
    assert connection.requests == [request(FunctionID.GET_CONNECTION_TYPE)]


def test_errors_of_the_bootloader_are_raised(brick: BrickMaster, connection: FakeConnection) -> None:
    """The Brick returns an error code other than 0."""
    connection.reply(FunctionID.GET_CONNECTION_TYPE, "B", 1)
    connection.reply(FunctionID.START_WIFI2_BOOTLOADER, "b", -1)
    connection.reply(FunctionID.WRITE_WIFI2_SERIAL_PORT, "b", -1)
    with pytest.raises(Wifi2BootloaderError):
        run(brick.start_wifi2_bootloader())
    with pytest.raises(Wifi2BootloaderError, match="3 bytes"):
        run(brick.write_wifi2_serial_port(b"abc"))


@pytest.mark.parametrize(
    "method, function_id",
    [
        ("get_wifi2_client_password", FunctionID.GET_WIFI2_CLIENT_PASSWORD),
        ("get_wifi2_ap_password", FunctionID.GET_WIFI2_AP_PASSWORD),
        ("get_wifi2_mesh_router_password", FunctionID.GET_WIFI2_MESH_ROUTER_PASSWORD),
    ],
)
def test_reading_the_passwords_is_deprecated(
    brick: BrickMaster, connection: FakeConnection, method: str, function_id: Enum
) -> None:
    """Newer firmwares do not return the passwords any more."""
    connection.reply(function_id, "64s", b"12345678")
    with pytest.warns(DeprecationWarning, match=method):
        assert run(getattr(brick, method)()) == "12345678"
    assert connection.requests == [request(function_id)]
