"""
Wi-Fi Extension 1.0 of the Master Brick.
"""

# pylint: disable=too-many-lines,duplicate-code
from __future__ import annotations

import re
from collections.abc import Iterable
from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple

from ..devices import Device
from ..ip_connection_helper import pack_payload, unpack_payload
from .common import FunctionID

if TYPE_CHECKING:
    from ..ip_connection import IPConnectionAsync


class GetWifiConfiguration(NamedTuple):
    ssid: str
    connection: WifiConnection
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    port: int


class GetWifiEncryption(NamedTuple):
    encryption: WifiEncryptionMode
    key_index: int
    eap_options: EapOptions
    ca_certificate_length: int
    client_certificate_length: int
    private_key_length: int


class GetWifiStatus(NamedTuple):
    mac_address: tuple[int, int, int, int, int, int]
    bssid: tuple[int, int, int, int, int, int]
    channel: int
    rssi: int
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    rx_count: int
    tx_count: int
    state: WifiState


class GetWifiCertificate(NamedTuple):
    data: tuple[int, ...]
    data_length: int


class GetWifiBufferInfo(NamedTuple):
    overflow: int
    low_watermark: int
    used: int


@unique
class WifiConnection(Enum):
    """
    Wi-Fi configuration options, that define the operating mode.
    """

    DHCP = 0
    STATIC_IP = 1
    ACCESS_POINT_DHCP = 2
    ACCESS_POINT_STATIC_IP = 3
    AD_HOC_DHCP = 4
    AD_HOC_STATIC_IP = 5


@unique
class WifiEncryptionMode(Enum):
    """
    Wi-Fi encryption options
    """

    WPA_WPA2 = 0
    WPA_ENTERPRISE = 1
    WEP = 2
    NONE = 3


@unique
class WifiEapOuterAuth(Enum):
    """
    Wi-Fi outer encryption options, when WPA_ENTERPRISE is selected.
    """

    EAP_FAST = 0
    EAP_TLS = 1
    EAP_TTLS = 2
    EAP_PEAP = 3


@unique
class WifiEapInnerAuth(Enum):
    """
    Wi-Fi inner encryption options, when WPA_ENTERPRISE is selected.
    """

    EAP_MSCHAP = 0
    EAP_GTC = 1


@unique
class WifiEapCertType(Enum):
    """
    Wi-Fi certificate type, when WPA_ENTERPRISE is selected.
    """

    CA_CERT = 0
    CLIENT_CERT = 1
    PRIVATE_KEY = 2


class EapOptions:
    """
    This class combines the Wi-Fi EAP options WifiEapOuterAuth, WifiEapInnerAuth,
    WifiEapCertType
    """

    def __repr__(self) -> str:
        return f"EapOptions({self.__outer_auth}, {self.__inner_auth}, {self.__cert_type})"

    def __init__(self, value: int) -> None:
        self.__outer_auth = WifiEapOuterAuth(value & 0b11)
        self.__inner_auth = WifiEapInnerAuth((value >> 2) & 0b1)
        self.__cert_type = WifiEapCertType((value >> 3) & 0b11)

    @property
    def value(self) -> int:
        """
        Returns the binary representation of the EAP options
        """
        return self.__outer_auth.value | (self.__inner_auth.value << 2) | (self.__cert_type.value << 3)

    @property
    def outer_auth(self) -> WifiEapOuterAuth:
        """
        Returns a WifiEapOuterAuth enum
        """
        return self.__outer_auth

    @outer_auth.setter
    def outer_auth(self, value: WifiEapOuterAuth):
        if not isinstance(value, WifiEapOuterAuth):
            value = WifiEapOuterAuth(value)
        self.__outer_auth = value

    @property
    def inner_auth(self) -> WifiEapInnerAuth:
        """
        Returns a WifiEapInnerAuth enum
        """
        return self.__inner_auth

    @inner_auth.setter
    def inner_auth(self, value: WifiEapInnerAuth):
        if not isinstance(value, WifiEapInnerAuth):
            value = WifiEapInnerAuth(value)
        self.__inner_auth = value

    @property
    def cert_type(self) -> WifiEapCertType:
        """
        Returns a WifiEapCertType enum
        """
        return self.__cert_type

    @cert_type.setter
    def cert_type(self, value: WifiEapCertType):
        if not isinstance(value, WifiEapCertType):
            value = WifiEapCertType(value)
        self.__cert_type = value


@unique
class WifiState(Enum):
    """
    Describes the Wi-Fi Extension status
    """

    DISASSOCIATED = 0
    ASSOCIATED = 1
    ASSOCIATING = 2
    ERROR = 3
    NOT_INITIALIZED = 255


@unique
class WifiPowerMode(Enum):
    """
    Describes the power mode of the Wi-Fi Extension. Either Full speed, or low
    power.
    """

    HIGH = 0
    LOW = 1


@unique
class WifiDomain(Enum):
    """
    This is the Wi-Fi regulatory domain.
    """

    FCC = 0  # N/S America, Australia, New Zealand
    ETSI = 1  # Europe, Middle East, Africa
    TELEC = 2  # Japan


class WifiExtension(Device):  # pylint: disable=too-many-public-methods
    """
    The functions of the Wi-Fi Extension 1.0.
    """

    async def is_wifi_present(self) -> bool:
        """
        Returns *true* if a Wi-Fi Extension is available to be used by the Master Brick.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_WIFI_PRESENT, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_wifi_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        ssid: str | bytes,
        connection: WifiConnection | int,
        ip_address: tuple[int, int, int, int] | list[int] = (0, 0, 0, 0),
        subnet_mask: tuple[int, int, int, int] | list[int] = (0, 0, 0, 0),
        gateway: tuple[int, int, int, int] | list[int] = (0, 0, 0, 0),
        port: int = 4223,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration of the Wi-Fi Extension. The ``ssid`` can have a max length
        of 32 characters. Possible values for ``connection`` are:

        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 90

         "0", "DHCP"
         "1", "Static IP"
         "2", "Access Point: DHCP"
         "3", "Access Point: Static IP"
         "4", "Ad Hoc: DHCP"
         "5", "Ad Hoc: Static IP"

        If you set ``connection`` to one of the static IP options then you have to
        supply ``ip``, ``subnet_mask`` and ``gateway`` as an array of size 4 (first
        element of the array is the least significant byte of the address). If
        ``connection`` is set to one of the DHCP options then ``ip``, ``subnet_mask``
        and ``gateway`` are ignored, you can set them to 0.

        The last parameter is the port that your program will connect to. The
        default port, that is used by brickd, is 4223.

        The values are stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after configuration.

        It is recommended to use the Brick Viewer to set the Wi-Fi configuration.
        """
        if not isinstance(connection, WifiConnection):
            connection = WifiConnection(connection)
        if not (isinstance(ip_address, (tuple, list)) and len(ip_address) == 4):
            raise ValueError(
                "Invalid argument: expected isinstance(ip_address, (tuple, list)) and len(ip_address) == "
                "4, "
                f"got ip_address={ip_address!r}"
            )
        if not (isinstance(subnet_mask, (tuple, list)) and len(subnet_mask) == 4):
            raise ValueError(
                "Invalid argument: expected isinstance(subnet_mask, (tuple, list)) and len(subnet_mask) "
                "== 4, "
                f"got subnet_mask={subnet_mask!r}"
            )
        if not (isinstance(gateway, (tuple, list)) and len(gateway) == 4):
            raise ValueError(
                "Invalid argument: expected isinstance(gateway, (tuple, list)) and len(gateway) == 4, "
                f"got gateway={gateway!r}"
            )
        if not 1 <= port <= 65535:
            raise ValueError(f"Invalid argument: expected 1 <= port <= 65535, got port={port!r}")
        if not isinstance(ssid, bytes):
            ssid = ssid.encode("utf-8")
        if len(ssid) > 32:
            raise ValueError(f"Invalid argument: expected len(ssid) <= 32, got ssid={ssid!r}")

        # TODO: Do some more sanity checking like DHCP -> IP, etc.
        # TODO: Change documentation for the IP parameters (they are reversed and in correct order now)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_CONFIGURATION,
            data=pack_payload(
                (
                    ssid,
                    connection.value,
                    list(map(int, reversed(ip_address))),
                    list(map(int, reversed(subnet_mask))),
                    list(map(int, reversed(gateway))),
                    int(port),
                ),
                "32s B 4B 4B 4B H",
            ),
            response_expected=response_expected,
        )

    async def get_wifi_configuration(self) -> GetWifiConfiguration:
        """
        Returns the configuration as set by :func:`Set Wifi Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_CONFIGURATION, response_expected=True
        )
        ssid, connection, ip_addr, subnet_mask, gateway, port = unpack_payload(payload, "32s B 4B 4B 4B H")
        # Note ip, subnet_mask and gateway need to be reversed
        return GetWifiConfiguration(
            ssid, WifiConnection(connection), ip_addr[::-1], subnet_mask[::-1], gateway[::-1], port
        )

    async def set_wifi_encryption(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        encryption: WifiEncryptionMode,
        key_index: int = 1,
        eap_options: EapOptions | int | None = None,
        ca_certificate_length: int = 0,
        client_certificate_length: int = 0,
        private_key_length: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the encryption of the Wi-Fi Extension. The first parameter is the
        type of the encryption. Possible values are:

        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 90

         "0", "WPA/WPA2"
         "1", "WPA Enterprise (EAP-FAST, EAP-TLS, EAP-TTLS, PEAP)"
         "2", "WEP"
         "3", "No Encryption"

        The ``key`` has a max length of 50 characters and is used if ``encryption`` is set to 0 or 2 (WPA/WPA2 or WEP).
        Otherwise, the value is ignored.

        For WPA/WPA2 the key has to be at least 8 characters long. If you want to set a key with more than 50
        characters, see :func:`Set Long Wi-fi Key`.

        For WEP the key has to be either 10 or 26 hexadecimal digits long. It is possible to set the WEP
        ``key_index`` (1-4). If you don't know your ``key_index``, it is likely 1.

        If you choose WPA Enterprise as encryption, you have to set ``eap_options`` and the length of the certificates
        (for other encryption types these parameters are ignored). The certificate length are given in byte and the
        certificates themselves can be set with :func:`Set Wifi Certificate`. ``eap_options`` consist of the outer
        authentication (bits 1-2), inner authentication (bit 3) and certificate type (bits 4-5):

        .. csv-table::
         :header: "Option", "Bits", "Description"
         :widths: 20, 10, 70

         "outer authentication", "1-2", "0=EAP-FAST, 1=EAP-TLS, 2=EAP-TTLS, 3=EAP-PEAP"
         "inner authentication", "3", "0=EAP-MSCHAP, 1=EAP-GTC"
         "certificate type", "4-5", "0=CA Certificate, 1=Client Certificate, 2=Private Key"

        Example for EAP-TTLS + EAP-GTC + Private Key: ``option = 2 | (1 << 2) | (2 << 3)``.

        The values are stored in the EEPROM and only applied on startup. That means you have to restart the Master Brick
        after configuration.

        It is recommended to use the Brick Viewer to set the Wi-Fi encryption.
        """
        if eap_options is None:
            eap_options = EapOptions(0)
        elif not isinstance(eap_options, EapOptions):
            eap_options = EapOptions(eap_options)
        if not isinstance(encryption, WifiEncryptionMode):
            encryption = WifiEncryptionMode(encryption)
        if not 1 <= key_index <= 4:
            raise ValueError(f"Invalid argument: expected 1 <= key_index <= 4, got key_index={key_index!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_ENCRYPTION,
            data=pack_payload(
                (
                    encryption.value,
                    b"-",  # do not set the key here, use set_long_wifi_key()
                    int(key_index),
                    eap_options.value,
                    int(ca_certificate_length),
                    int(client_certificate_length),
                    int(private_key_length),
                ),
                "B 50s B B H H H",
            ),
            response_expected=response_expected,
        )

    async def get_wifi_encryption(self) -> GetWifiEncryption:
        """
        Returns the encryption as set by :func:`Set Wi-fi Encryption`.

        .. note::
         Since Master Brick Firmware version 2.4.4 the key is not returned anymore.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_ENCRYPTION, response_expected=True
        )
        # Drop the "key" value. It is empty anyway, and we do not use it with this API
        (
            encryption,
            _,
            key_index,
            eap_options,
            ca_certificate_length,
            client_certificate_length,
            private_key_length,
        ) = unpack_payload(payload, "B 50s B B H H H")

        return GetWifiEncryption(
            WifiEncryptionMode(encryption),
            key_index,
            EapOptions(eap_options),
            ca_certificate_length,
            client_certificate_length,
            private_key_length,
        )

    async def get_wifi_status(self) -> GetWifiStatus:
        """
        Returns the status of the Wi-Fi Extension. The ``state`` is updated automatically, all the other parameters are
        updated on startup and every time :func:`Refresh Wifi Status` is called.

        Possible states are:

        .. csv-table::
         :header: "State", "Description"
         :widths: 10, 90

         "0", "Disassociated"
         "1", "Associated"
         "2", "Associating"
         "3", "Error"
         "255", "Not initialized yet"
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_STATUS, response_expected=True
        )
        mac_address, bssid, channel, rssi, ip_addr, subnet_mask, gateway, rx_count, tx_count, state = unpack_payload(
            payload, "6B 6B B h 4B 4B 4B I I B"
        )
        return GetWifiStatus(
            mac_address[::-1],
            bssid[::-1],
            channel,
            rssi,
            ip_addr[::-1],
            subnet_mask[::-1],
            gateway[::-1],
            rx_count,
            tx_count,
            WifiState(state),
        )

    async def refresh_wifi_status(self, response_expected: bool = True) -> None:
        """
        Refreshes the Wi-Fi status (see :func:`Get Wifi Status`). To read the status
        of the Wi-Fi module, the Master Brick has to change from data mode to
        command mode and back. This transaction and the readout itself is
        unfortunately time-consuming. This means, that it might take some ms
        until the stack with attached Wi-Fi Extension reacts again after this
        function is called.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.REFRESH_WIFI_STATUS, response_expected=response_expected
        )

    async def set_wpa_enterprise_username(self, username: str | bytes, response_expected: bool = True) -> None:
        """
        This is a convenience method, that wraps set_wifi_certificate() to allow setting
        the WPA Enterprise username without worrying about the correct offsets.
        """
        if not isinstance(username, bytes):
            username = username.encode("utf-8")
        if len(username) > 32:
            raise ValueError(f"Invalid argument: expected len(username) <= 32, got username={username!r}")

        data = list(username) + [0] * (32 - len(username))  # pad with null bytes

        return await self.set_wifi_certificate(0xFFFF, data, len(username), response_expected)

    async def get_wpa_enterprise_username(self) -> bytes:
        """
        This is a convenience method, that wraps get_wifi_certificate() without worrying about
        the correct offsets and return type. It will return a string.
        """
        data = await self.get_wifi_certificate(0xFFFF)
        return bytes(data.data[: data.data_length])

    async def set_wpa_enterprise_password(self, password: bytes | str, response_expected: bool = True) -> None:
        """
        This is a convenience method, that wraps set_wifi_certificate() to allow setting
        the WPA Enterprise password without worrying about the correct offsets.
        """
        if not isinstance(password, bytes):
            password = password.encode("utf-8")
        if len(password) > 32:
            raise ValueError(f"Invalid argument: expected len(password) <= 32, got password={password!r}")

        data = list(password) + [0] * (32 - len(password))  # pad with null bytes

        return await self.set_wifi_certificate(0xFFFE, data, len(password), response_expected)

    async def get_wpa_enterprise_password(self) -> bytes:
        """
        This is a convenience method, that wraps get_wifi_certificate() without worrying about
        the correct offsets and return type. It will return a string.
        """
        data = await self.get_wifi_certificate(0xFFFE)
        return bytes(data.data[: data.data_length])

    async def set_wifi_certificate(
        self, index: int, data: Iterable[int], data_length: int, response_expected: bool = True
    ) -> None:
        """
        This function is used to set the certificate as well as password and username
        for WPA Enterprise. To set the username use index 0xFFFF,
        to set the password use index 0xFFFE. The max length of username and
        password is 32.

        The certificate is written in chunks of size 32 and the index is used as
        the index of the chunk. ``data_length`` should nearly always be 32. Only
        the last chunk can have a length that is not equal to 32.

        The starting index of the CA Certificate is 0, of the Client Certificate
        10000 and for the Private Key 20000. Maximum sizes are 1312, 1312 and
        4320 byte respectively.

        The values are stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after uploading the certificate.

        It is recommended to use the Brick Viewer to set the certificate, username
        and password.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_CERTIFICATE,
            data=pack_payload(
                (
                    int(index),
                    list(map(int, data)),
                    int(data_length),
                ),
                "H 32B B",
            ),
            response_expected=response_expected,
        )

    async def get_wifi_certificate(self, index: int) -> GetWifiCertificate:
        """
        Returns the certificate for a given index as set by :func:`Set Wifi Certificate`.
        """

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_WIFI_CERTIFICATE,
            data=pack_payload((int(index),), "H"),
            response_expected=True,
        )

        return GetWifiCertificate(*unpack_payload(payload, "32B B"))

    async def set_wifi_power_mode(self, mode: WifiPowerMode, response_expected: bool = True) -> None:
        """
        Sets the power mode of the Wi-Fi Extension. Possible modes are:

        .. csv-table::
         :header: "Mode", "Description"
         :widths: 10, 90

         "0", "Full Speed (high power consumption, high throughput)"
         "1", "Low Power (low power consumption, low throughput)"

        The default value is 0 (Full Speed).
        """
        if not isinstance(mode, WifiPowerMode):
            mode = WifiPowerMode(mode)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_POWER_MODE,
            data=pack_payload((mode.value,), "B"),
            response_expected=response_expected,
        )

    async def get_wifi_power_mode(self) -> WifiPowerMode:
        """
        Returns the power mode as set by :func:`Set Wifi Power Mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_POWER_MODE, response_expected=True
        )

        return WifiPowerMode(unpack_payload(payload, "B"))

    async def get_wifi_buffer_info(self) -> GetWifiBufferInfo:
        """
        Returns information about the Wi-Fi receive buffer. The Wi-Fi receive buffer has a max size of 1500 byte and if
        data is transferred too fast, it might overflow.

        The return values are the number of overflows, the low watermark (i.e. the smallest number of bytes that were
        free in the buffer) and the bytes that are currently used.

        You should always try to keep the buffer empty, otherwise you will have a permanent latency. A good rule of
        thumb is, that you can transfer 1000 messages per second without problems.

        Try to not send more than 50 messages at a time without any kind of break between them.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_BUFFER_INFO, response_expected=True
        )

        return GetWifiBufferInfo(*unpack_payload(payload, "I H H"))

    async def set_wifi_regulatory_domain(self, domain: WifiDomain, response_expected: bool = True) -> None:
        """
        Sets the regulatory domain of the Wi-Fi Extension. Possible domains are:

        .. csv-table::
         :header: "Domain", "Description"
         :widths: 10, 90

         "0", "FCC: Channel 1-11 (N/S America, Australia, New Zealand)"
         "1", "ETSI: Channel 1-13 (Europe, Middle East, Africa)"
         "2", "TELEC: Channel 1-14 (Japan)"

        The default value is 1 (ETSI).
        """
        if not isinstance(domain, WifiDomain):
            domain = WifiDomain(domain)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_REGULATORY_DOMAIN,
            data=pack_payload((domain.value,), "B"),
            response_expected=response_expected,
        )

    async def get_wifi_regulatory_domain(self) -> WifiDomain:
        """
        Returns the regulatory domain as set by :func:`Set Wifi Regulatory Domain`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_REGULATORY_DOMAIN, response_expected=True
        )

        return WifiDomain(unpack_payload(payload, "B"))

    async def set_long_wifi_key(self, key: bytes | str, response_expected: bool = True) -> None:
        """
        Sets a long Wi-Fi key (up to 63 chars, at least 8 chars) for WPA encryption. This key will be used if the key
        in :func:`Set Wifi Encryption` is set to "-". In the old protocol, a payload of size 63 was not possible, so the
        maximum key length was 50 chars.

        With the new protocol this is possible, since we didn't want to break API, this function was added additionally.

        .. versionadded:: 2.0.2$nbsp;(Firmware)
        """
        if not isinstance(key, bytes):
            key = key.encode("utf-8")
        if not 8 <= len(key) <= 63:
            raise ValueError(f"Invalid argument: expected 8 <= len(key) <= 63, got key={key!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_LONG_WIFI_KEY,
            data=pack_payload((key,), "64s"),
            response_expected=response_expected,
        )

    async def get_long_wifi_key(self) -> str:
        """
        Returns the encryption key as set by :func:`Set Long Wifi Key`.

        .. note::
         Since Master Brick firmware version 2.4.4 the key is not returned anymore.

        .. versionadded:: 2.0.2$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_LONG_WIFI_KEY, response_expected=True
        )

        return unpack_payload(payload, "64s")

    async def set_wifi_hostname(self, hostname: bytes | str, response_expected: bool = True) -> None:
        """
        Sets the hostname of the Wi-Fi Extension. The hostname will be displayed by access points as the hostname in the
        DHCP clients table.

        Setting an empty String will restore the default hostname.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        if not isinstance(hostname, bytes):
            hostname = hostname.encode("ascii")

        # Test if the hostname is valid
        # Check for hostnames as per RFC 1123. This allows labels that start with
        # a digit or hyphen, which was not allowed in RFC 952 originally
        # The Wi-Fi extension only allows 16 characters as opposed to 63 as per RFC.
        # Allow 0 characters to reset the hostname (this is TF specific)
        hostname = hostname.lower()
        if len(hostname) != 0:
            allowed = re.compile(rb"^(?!-)[a-z0-9-]{2,16}(?<!-)$")
            if not bool(allowed.match(hostname)):
                raise ValueError("Invalid hostname")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_HOSTNAME,
            data=pack_payload((hostname,), "16s"),
            response_expected=response_expected,
        )

    async def get_wifi_hostname(self) -> str:
        """
        Returns the hostname as set by :func:`Set Wifi Hostname`.

        An empty String means, that the default hostname is used.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_HOSTNAME, response_expected=True
        )

        return unpack_payload(payload, "16s")

    async def set_wifi_authentication_secret(self, secret: bytes | str, response_expected: bool = True) -> None:
        """
        Sets the Wi-Fi authentication secret. The secret can be a string of up to 64
        characters. An empty string disables the authentication.

        See the :ref:`authentication tutorial <tutorial_authentication>` for more
        information.

        The secret is stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after configuration.

        It is recommended to use the Brick Viewer to set the Wi-Fi authentication secret.

        The default value is an empty string (authentication disabled).

        .. versionadded:: 2.2.0$nbsp;(Firmware)
        """
        if not isinstance(secret, bytes):
            secret = secret.encode("utf-8")
        if len(secret) > 64:
            raise ValueError(f"Invalid argument: expected len(secret) <= 64, got secret={secret!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_AUTHENTICATION_SECRET,
            data=pack_payload((secret,), "64s"),
            response_expected=response_expected,
        )

    async def get_wifi_authentication_secret(self) -> str:
        """
        Returns the authentication secret as set by
        :func:`Set Wifi Authentication Secret`.

        .. versionadded:: 2.2.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_AUTHENTICATION_SECRET, response_expected=True
        )

        return unpack_payload(payload, "64s")
