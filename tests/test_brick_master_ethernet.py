"""Tests for the Ethernet extension of the Master Brick."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

from tinkerforge_async.brick_master import (
    BrickMaster,
    EthernetConnection,
    GetEthernetConfiguration,
    GetEthernetStatus,
    GetEthernetWebsocketConfiguration,
)

from .device_tests import GATEWAY, IP, MAC, MASK, NULL, DeviceTests
from .fake_connection import Call

DEVICE = BrickMaster
FunctionID = BrickMaster.FunctionID


CALLS = [
    Call("is_ethernet_present", FunctionID.IS_ETHERNET_PRESENT, reply=("!", (True,)), result=True),
    Call(
        "set_ethernet_configuration",
        FunctionID.SET_ETHERNET_CONFIGURATION,
        (EthernetConnection.DHCP,),
        sent=("B 4B 4B 4B H", (0, NULL, NULL, NULL, 4223)),
    ),
    Call(
        "set_ethernet_configuration",
        FunctionID.SET_ETHERNET_CONFIGURATION,
        (1, IP, list(MASK), GATEWAY, 65535, False),
        sent=("B 4B 4B 4B H", (1, IP, MASK, GATEWAY, 65535)),
        response_expected=False,
    ),
    Call(
        "get_ethernet_configuration",
        FunctionID.GET_ETHERNET_CONFIGURATION,
        reply=("B 4B 4B 4B H", (1, IP, MASK, GATEWAY, 4223)),
        result=GetEthernetConfiguration(EthernetConnection.STATIC_IP, IP, MASK, GATEWAY, 4223),
    ),
    Call(
        "get_ethernet_status",
        FunctionID.GET_ETHERNET_STATUS,
        reply=("6B 4B 4B 4B I I 32s", (MAC, IP, MASK, GATEWAY, 1000, 2000, b"master-brick")),
        result=GetEthernetStatus(MAC, IP, MASK, GATEWAY, 1000, 2000, "master-brick"),
    ),
    # The hostname is converted to lower case
    Call(
        "set_ethernet_hostname", FunctionID.SET_ETHERNET_HOSTNAME, ("Master-Brick",), sent=("32s", (b"master-brick",))
    ),
    Call("set_ethernet_hostname", FunctionID.SET_ETHERNET_HOSTNAME, (b"a" * 32,), sent=("32s", (b"a" * 32,))),
    # An empty hostname selects the default
    Call("set_ethernet_hostname", FunctionID.SET_ETHERNET_HOSTNAME, ("",), sent=("32s", (b"",))),
    Call("set_ethernet_mac_address", FunctionID.SET_ETHERNET_MAC_ADDRESS, (MAC,), sent=("6B", (MAC,))),
    Call("set_ethernet_mac_address", FunctionID.SET_ETHERNET_MAC_ADDRESS, (list(MAC),), sent=("6B", (MAC,))),
    Call(
        "set_ethernet_websocket_configuration",
        FunctionID.SET_ETHERNET_WEBSOCKET_CONFIGURATION,
        (0, 1),
        sent=("B H", (0, 1)),
    ),
    Call(
        "set_ethernet_websocket_configuration",
        FunctionID.SET_ETHERNET_WEBSOCKET_CONFIGURATION,
        (7, 65535),
        sent=("B H", (7, 65535)),
    ),
    Call(
        "get_ethernet_websocket_configuration",
        FunctionID.GET_ETHERNET_WEBSOCKET_CONFIGURATION,
        reply=("B H", (3, 4280)),
        result=GetEthernetWebsocketConfiguration(3, 4280),
    ),
    Call(
        "set_ethernet_authentication_secret",
        FunctionID.SET_ETHERNET_AUTHENTICATION_SECRET,
        ("secret",),
        sent=("64s", (b"secret",)),
    ),
    Call(
        "set_ethernet_authentication_secret",
        FunctionID.SET_ETHERNET_AUTHENTICATION_SECRET,
        (b"x" * 64,),
        sent=("64s", (b"x" * 64,)),
    ),
    # An empty secret disables the authentication
    Call(
        "set_ethernet_authentication_secret",
        FunctionID.SET_ETHERNET_AUTHENTICATION_SECRET,
        ("",),
        sent=("64s", (b"",)),
    ),
    Call(
        "get_ethernet_authentication_secret",
        FunctionID.GET_ETHERNET_AUTHENTICATION_SECRET,
        reply=("64s", (b"secret",)),
        result="secret",
    ),
]

REJECTED = [
    ("set_ethernet_configuration", (2,)),
    ("set_ethernet_configuration", (0, (1, 2, 3))),
    ("set_ethernet_configuration", (0, "1.2.3.4")),
    ("set_ethernet_configuration", (0, IP, (1, 2, 3))),
    ("set_ethernet_configuration", (0, IP, "255.255.255.0")),
    ("set_ethernet_configuration", (0, IP, MASK, (1, 2, 3))),
    ("set_ethernet_configuration", (0, IP, MASK, "1.2.3.4")),
    ("set_ethernet_configuration", (0, IP, MASK, GATEWAY, 0)),
    ("set_ethernet_configuration", (0, IP, MASK, GATEWAY, 65536)),
    ("set_ethernet_hostname", ("a",)),  # Too short
    ("set_ethernet_hostname", ("a" * 33,)),  # Too long
    ("set_ethernet_hostname", ("-master",)),
    ("set_ethernet_hostname", ("master-",)),
    ("set_ethernet_hostname", ("master_brick",)),
    ("set_ethernet_mac_address", (MAC[:5],)),
    ("set_ethernet_mac_address", ("40:d8:55:02:a0:00",)),
    ("set_ethernet_websocket_configuration", (-1, 4280)),
    ("set_ethernet_websocket_configuration", (8, 4280)),
    ("set_ethernet_websocket_configuration", (1, 0)),
    ("set_ethernet_websocket_configuration", (1, 65536)),
    ("set_ethernet_authentication_secret", ("x" * 65,)),
]


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""
