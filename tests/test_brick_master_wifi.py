"""Tests for the Wi-Fi extension of the Master Brick."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

import pytest

from tinkerforge_async.brick_master import (
    BrickMaster,
    EapOptions,
    GetWifiBufferInfo,
    GetWifiCertificate,
    GetWifiConfiguration,
    GetWifiStatus,
    WifiConnection,
    WifiDomain,
    WifiEapCertType,
    WifiEapInnerAuth,
    WifiEapOuterAuth,
    WifiEncryptionMode,
    WifiPowerMode,
    WifiState,
)

from .device_tests import BSSID, GATEWAY, IP, MAC, MASK, NULL, DeviceTests
from .fake_connection import Call, request, run

DEVICE = BrickMaster
FunctionID = BrickMaster.FunctionID

# The Wi-Fi extension transfers the addresses in reversed order
IP_REVERSED, MASK_REVERSED, GATEWAY_REVERSED = IP[::-1], MASK[::-1], GATEWAY[::-1]
MAC_REVERSED, BSSID_REVERSED = MAC[::-1], BSSID[::-1]


def padded(text: bytes) -> tuple[int, ...]:
    """The data of a certificate packet. It always has 32 bytes."""
    return tuple(text.ljust(32, b"\0"))


CALLS = [
    Call("is_wifi_present", FunctionID.IS_WIFI_PRESENT, reply=("!", (True,)), result=True),
    Call(
        "set_wifi_configuration",
        FunctionID.SET_WIFI_CONFIGURATION,
        ("my network", WifiConnection.DHCP),
        sent=("32s B 4B 4B 4B H", (b"my network", 0, NULL, NULL, NULL, 4223)),
    ),
    Call(
        "set_wifi_configuration",
        FunctionID.SET_WIFI_CONFIGURATION,
        (b"x" * 32, 1, IP, list(MASK), GATEWAY, 65535, False),
        sent=("32s B 4B 4B 4B H", (b"x" * 32, 1, IP_REVERSED, MASK_REVERSED, GATEWAY_REVERSED, 65535)),
        response_expected=False,
    ),
    Call(
        "get_wifi_configuration",
        FunctionID.GET_WIFI_CONFIGURATION,
        reply=("32s B 4B 4B 4B H", (b"my network", 1, IP_REVERSED, MASK_REVERSED, GATEWAY_REVERSED, 4223)),
        result=GetWifiConfiguration("my network", WifiConnection.STATIC_IP, IP, MASK, GATEWAY, 4223),
    ),
    # The key is not set by this function, see set_long_wifi_key()
    Call(
        "set_wifi_encryption",
        FunctionID.SET_WIFI_ENCRYPTION,
        (WifiEncryptionMode.WPA_WPA2,),
        sent=("B 50s B B H H H", (0, b"-", 1, 0, 0, 0, 0)),
    ),
    Call(
        "set_wifi_encryption",
        FunctionID.SET_WIFI_ENCRYPTION,
        (1, 4, EapOptions(0b10111), 100, 200, 300),
        sent=("B 50s B B H H H", (1, b"-", 4, 0b10111, 100, 200, 300)),
    ),
    Call(
        "set_wifi_encryption",
        FunctionID.SET_WIFI_ENCRYPTION,
        (WifiEncryptionMode.WPA_ENTERPRISE, 1, 0b01001),
        sent=("B 50s B B H H H", (1, b"-", 1, 0b01001, 0, 0, 0)),
    ),
    Call(
        "get_wifi_status",
        FunctionID.GET_WIFI_STATUS,
        reply=(
            "6B 6B B h 4B 4B 4B I I B",
            (MAC_REVERSED, BSSID_REVERSED, 11, -60, IP_REVERSED, MASK_REVERSED, GATEWAY_REVERSED, 1000, 2000, 1),
        ),
        result=GetWifiStatus(MAC, BSSID, 11, -60, IP, MASK, GATEWAY, 1000, 2000, WifiState.ASSOCIATED),
    ),
    Call("refresh_wifi_status", FunctionID.REFRESH_WIFI_STATUS),
    Call("refresh_wifi_status", FunctionID.REFRESH_WIFI_STATUS, (False,), response_expected=False),
    Call(
        "set_wifi_certificate",
        FunctionID.SET_WIFI_CERTIFICATE,
        (10000, range(32), 32),
        sent=("H 32B B", (10000, tuple(range(32)), 32)),
    ),
    Call(
        "get_wifi_certificate",
        FunctionID.GET_WIFI_CERTIFICATE,
        (10000,),
        sent=("H", (10000,)),
        reply=("32B B", (tuple(range(32)), 20)),
        result=GetWifiCertificate(tuple(range(32)), 20),
    ),
    # The username and the password are stored like a certificate. The index tells them apart.
    Call(
        "set_wpa_enterprise_username",
        FunctionID.SET_WIFI_CERTIFICATE,
        ("user",),
        sent=("H 32B B", (0xFFFF, padded(b"user"), 4)),
    ),
    Call(
        "set_wpa_enterprise_username",
        FunctionID.SET_WIFI_CERTIFICATE,
        (b"u" * 32,),
        sent=("H 32B B", (0xFFFF, padded(b"u" * 32), 32)),
    ),
    Call(
        "get_wpa_enterprise_username",
        FunctionID.GET_WIFI_CERTIFICATE,
        sent=("H", (0xFFFF,)),
        reply=("32B B", (padded(b"user"), 4)),
        result=b"user",
    ),
    Call(
        "set_wpa_enterprise_password",
        FunctionID.SET_WIFI_CERTIFICATE,
        ("Pässword",),
        sent=("H 32B B", (0xFFFE, padded("Pässword".encode()), 9)),
    ),
    Call(
        "set_wpa_enterprise_password",
        FunctionID.SET_WIFI_CERTIFICATE,
        (b"p" * 32,),
        sent=("H 32B B", (0xFFFE, padded(b"p" * 32), 32)),
    ),
    Call(
        "get_wpa_enterprise_password",
        FunctionID.GET_WIFI_CERTIFICATE,
        sent=("H", (0xFFFE,)),
        reply=("32B B", (padded(b"secret"), 6)),
        result=b"secret",
    ),
    Call("set_wifi_power_mode", FunctionID.SET_WIFI_POWER_MODE, (WifiPowerMode.LOW,), sent=("B", (1,))),
    Call("set_wifi_power_mode", FunctionID.SET_WIFI_POWER_MODE, (0,), sent=("B", (0,))),
    Call("get_wifi_power_mode", FunctionID.GET_WIFI_POWER_MODE, reply=("B", (1,)), result=WifiPowerMode.LOW),
    Call(
        "get_wifi_buffer_info",
        FunctionID.GET_WIFI_BUFFER_INFO,
        reply=("I H H", (1, 200, 300)),
        result=GetWifiBufferInfo(1, 200, 300),
    ),
    Call("set_wifi_regulatory_domain", FunctionID.SET_WIFI_REGULATORY_DOMAIN, (WifiDomain.ETSI,), sent=("B", (1,))),
    Call("set_wifi_regulatory_domain", FunctionID.SET_WIFI_REGULATORY_DOMAIN, (2,), sent=("B", (2,))),
    Call("get_wifi_regulatory_domain", FunctionID.GET_WIFI_REGULATORY_DOMAIN, reply=("B", (0,)), result=WifiDomain.FCC),
    Call("set_long_wifi_key", FunctionID.SET_LONG_WIFI_KEY, ("12345678",), sent=("64s", (b"12345678",))),
    Call("set_long_wifi_key", FunctionID.SET_LONG_WIFI_KEY, (b"k" * 63,), sent=("64s", (b"k" * 63,))),
    Call("get_long_wifi_key", FunctionID.GET_LONG_WIFI_KEY, reply=("64s", (b"12345678",)), result="12345678"),
    # The hostname is converted to lower case
    Call("set_wifi_hostname", FunctionID.SET_WIFI_HOSTNAME, ("Master-Brick",), sent=("16s", (b"master-brick",))),
    Call("set_wifi_hostname", FunctionID.SET_WIFI_HOSTNAME, (b"a" * 16,), sent=("16s", (b"a" * 16,))),
    # An empty hostname selects the default
    Call("set_wifi_hostname", FunctionID.SET_WIFI_HOSTNAME, ("",), sent=("16s", (b"",))),
    Call("get_wifi_hostname", FunctionID.GET_WIFI_HOSTNAME, reply=("16s", (b"master-brick",)), result="master-brick"),
    Call(
        "set_wifi_authentication_secret",
        FunctionID.SET_WIFI_AUTHENTICATION_SECRET,
        ("secret",),
        sent=("64s", (b"secret",)),
    ),
    Call(
        "set_wifi_authentication_secret",
        FunctionID.SET_WIFI_AUTHENTICATION_SECRET,
        (b"x" * 64,),
        sent=("64s", (b"x" * 64,)),
    ),
    Call(
        "get_wifi_authentication_secret",
        FunctionID.GET_WIFI_AUTHENTICATION_SECRET,
        reply=("64s", (b"secret",)),
        result="secret",
    ),
]

REJECTED = [
    ("set_wifi_configuration", ("ssid", 6)),
    ("set_wifi_configuration", ("ssid", 0, (1, 2, 3))),
    ("set_wifi_configuration", ("ssid", 0, "1.2.3.4")),
    ("set_wifi_configuration", ("ssid", 0, IP, (1, 2, 3))),
    ("set_wifi_configuration", ("ssid", 0, IP, "255.255.255.0")),
    ("set_wifi_configuration", ("ssid", 0, IP, MASK, (1, 2, 3))),
    ("set_wifi_configuration", ("ssid", 0, IP, MASK, "1.2.3.4")),
    ("set_wifi_configuration", ("ssid", 0, IP, MASK, GATEWAY, 0)),
    ("set_wifi_configuration", ("ssid", 0, IP, MASK, GATEWAY, 65536)),
    ("set_wifi_configuration", ("x" * 33, 0)),
    ("set_wifi_encryption", (4,)),
    ("set_wifi_encryption", (0, 0)),
    ("set_wifi_encryption", (0, 5)),
    ("set_wifi_encryption", (0, 1, 0b11000)),  # There is no such type of certificate
    ("set_wpa_enterprise_username", ("u" * 33,)),
    ("set_wpa_enterprise_password", ("p" * 33,)),
    ("set_wifi_power_mode", (2,)),
    ("set_wifi_regulatory_domain", (3,)),
    ("set_long_wifi_key", ("1234567",)),
    ("set_long_wifi_key", ("k" * 64,)),
    ("set_wifi_hostname", ("a",)),  # Too short
    ("set_wifi_hostname", ("a" * 17,)),  # Too long
    ("set_wifi_hostname", ("-master",)),
    ("set_wifi_hostname", ("master-",)),
    ("set_wifi_hostname", ("master_brick",)),
    ("set_wifi_authentication_secret", ("x" * 65,)),
]


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_get_wifi_encryption(brick, connection):
    """The key is not returned by the Brick."""
    connection.reply(FunctionID.GET_WIFI_ENCRYPTION, "B 50s B B H H H", 1, b"", 2, 0b10111, 100, 200, 300)
    encryption = run(brick.get_wifi_encryption())
    assert connection.requests == [request(FunctionID.GET_WIFI_ENCRYPTION)]
    assert encryption.encryption is WifiEncryptionMode.WPA_ENTERPRISE
    assert encryption.key_index == 2
    assert encryption.eap_options.value == 0b10111
    assert encryption[3:] == (100, 200, 300)


def test_eap_options():
    """The options of the authentication are packed into one byte."""
    options = EapOptions(0b10111)
    assert options.outer_auth is WifiEapOuterAuth.EAP_PEAP
    assert options.inner_auth is WifiEapInnerAuth.EAP_GTC
    assert options.cert_type is WifiEapCertType.PRIVATE_KEY
    assert repr(options) == (
        "EapOptions(WifiEapOuterAuth.EAP_PEAP, WifiEapInnerAuth.EAP_GTC, WifiEapCertType.PRIVATE_KEY)"
    )

    options.outer_auth = WifiEapOuterAuth.EAP_TLS
    options.inner_auth = WifiEapInnerAuth.EAP_MSCHAP
    options.cert_type = WifiEapCertType.CLIENT_CERT
    assert options.value == 0b01001

    # The values of the enums are accepted as well
    options.outer_auth = 2
    options.inner_auth = 1
    options.cert_type = 0
    assert options.value == 0b00110
    assert EapOptions(0).value == 0

    with pytest.raises(ValueError):
        options.outer_auth = 4
    with pytest.raises(ValueError):
        options.inner_auth = 2
    with pytest.raises(ValueError):
        options.cert_type = 3
