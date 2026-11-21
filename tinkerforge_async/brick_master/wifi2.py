"""
Wi-Fi Extension 2.0 of the Master Brick.
"""

# pylint: disable=too-many-lines,duplicate-code
from __future__ import annotations

import re
import warnings
from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple

from ..ip_connection_helper import pack_payload, unpack_payload
from .common import ConnectionType, FunctionID, MasterConnection
from .ethernet import PhyMode

if TYPE_CHECKING:
    from ..ip_connection import IPConnectionAsync


class ReadWifi2SerialPort(NamedTuple):
    data: tuple[
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
        int,
    ]
    result: int


class GetWifi2Configuration(NamedTuple):
    port: int
    websocket_port: int
    website_port: int
    phy_mode: PhyMode
    sleep_mode: int
    website: bool


class GetWifi2Status(NamedTuple):
    client_enabled: bool
    client_status: WifiClientStatus
    client_ip: tuple[int, int, int, int]
    client_subnet_mask: tuple[int, int, int, int]
    client_gateway: tuple[int, int, int, int]
    client_mac_address: tuple[int, int, int, int, int, int]
    client_rx_count: int
    client_tx_count: int
    client_rssi: int
    ap_enabled: bool
    ap_ip: tuple[int, int, int, int]
    ap_subnet_mask: tuple[int, int, int, int]
    ap_gateway: tuple[int, int, int, int]
    ap_mac_address: tuple[int, int, int, int, int, int]
    ap_rx_count: int
    ap_tx_count: int
    ap_connected_count: int


class GetWifi2ClientConfiguration(NamedTuple):
    enable: bool
    ssid: bytes
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    mac_address: tuple[int, int, int, int, int, int]
    bssid: tuple[int, int, int, int, int, int]


class GetWifi2APConfiguration(NamedTuple):
    enable: bool
    ssid: bytes
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    encryption: WifiApEncryption
    hidden: bool
    channel: int
    mac_address: tuple[int, int, int, int, int, int]


class GetWifi2MeshConfiguration(NamedTuple):
    enable: bool
    root_ip: tuple[int, int, int, int]
    root_subnet_mask: tuple[int, int, int, int]
    root_gateway: tuple[int, int, int, int]
    router_bssid: tuple[int, int, int, int, int, int]
    group_id: tuple[int, int, int, int, int, int]
    group_ssid_prefix: bytes
    gateway_ip: tuple[int, int, int, int]
    gateway_port: int


class GetWifi2MeshCommonStatus(NamedTuple):
    status: WifiMeshStatus
    root_node: bool
    root_candidate: bool
    connected_nodes: int
    rx_count: int
    tx_count: int


class GetWifi2MeshClientStatus(NamedTuple):
    hostname: bytes
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    mac_address: tuple[int, int, int, int, int, int]


class GetWifi2MeshAPStatus(NamedTuple):
    ssid: bytes
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    mac_address: tuple[int, int, int, int, int, int]


class Wifi2BootloaderError(Exception):
    """
    Raised if the bootloader of the Wi-Fi 2.0 extension did not come up or is
    unresponsive
    """


@unique
class WifiClientStatus(Enum):
    """
    Wi-Fi 2.0 Extension status when in client mode
    """

    IDLE = 0
    CONNECTING = 1
    WRONG_PASSWORD = 2
    NO_AP_FOUND = 3
    CONNECT_FAILED = 4
    GOT_IP = 5
    UNKNOWN = 255


@unique
class WifiApEncryption(Enum):
    """
    Wi-Fi 2.0 Extension configuration when in AP mode
    """

    OPEN = 0
    WEP = 1
    WPA_PSK = 2
    WPA2_PSK = 3
    WPA_WPA2_PSK = 4


@unique
class WifiMeshStatus(Enum):
    """
    Wi-Fi 2.0 Extension configuration when in mesh mode
    """

    DISABLED = 0
    WIFI_CONNECTING = 1
    GOT_IP = 2
    MESH_LOCAL = 3
    MESH_ONLINE = 4
    AP_AVAILABLE = 5
    AP_SETUP = 6
    LEAF_AVAILABLE = 7


class Wifi2Extension(MasterConnection):  # pylint: disable=too-many-public-methods
    """
    The functions of the Wi-Fi Extension 2.0, which can only be used if the Master Brick is connected via USB.
    """

    async def is_wifi2_present(self) -> bool:
        """
        Returns *true* if a Wi-Fi Extension 2.0 is available to be used by the Master
        Brick.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_WIFI2_PRESENT, response_expected=True
        )

        return unpack_payload(payload, "!")

    async def start_wifi2_bootloader(self) -> None:
        """
        Starts the bootloader of the Wi-Fi Extension 2.0. Returns 0 on success.
        Afterwards the :func:`Write Wifi2 Serial Port` and :func:`Read Wifi2 Serial Port`
        functions can be used to communicate with the bootloader to flash a new
        firmware.

        The bootloader should only be started over a USB connection. It cannot be
        started over a Wi-Fi2 connection, see the :func:`Get Connection Type` function.

        It is recommended to use the Brick Viewer to update the firmware of the Wi-Fi
        Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        connection_type = await self.get_connection_type()
        if connection_type is not ConnectionType.USB:
            raise RuntimeError("This function can only be called when connected via USB.")

        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.START_WIFI2_BOOTLOADER, response_expected=True
        )
        result = unpack_payload(payload, "b")
        if result != 0:
            raise Wifi2BootloaderError("Failed to start the Wi-Fi 2.0 bootloader.")

    async def write_wifi2_serial_port(self, data: bytes | str):
        """
        Writes up to 60 bytes (number of bytes to be written specified by ``length``)
        to the serial port of the bootloader of the Wi-Fi Extension 2.0. Returns 0 on
        success.

        Before this function can be used the bootloader has to be started using the
        :func:`Start Wifi2 Bootloader` function.

        It is recommended to use the Brick Viewer to update the firmware of the Wi-Fi
        Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        if not isinstance(data, bytes):
            data = data.encode("utf-8")

        if len(data) > 60:
            raise ValueError(f"Invalid argument: expected len(data) <= 60, got data={data!r}")

        length = len(data)
        data = data.ljust(60, b"\x00")  # always send 60 bytes, fill with b"\x00"

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_WIFI2_SERIAL_PORT,
            data=pack_payload((data, length), "60B B"),
            response_expected=True,
        )
        result = unpack_payload(payload, "b")
        if result != 0:
            raise Wifi2BootloaderError(f"Failed to write {length} bytes to the serial port.")

    async def read_wifi2_serial_port(self, length: int) -> ReadWifi2SerialPort:
        """
        Reads up to 60 bytes (number of bytes to be read specified by ``length``)
        from the serial port of the bootloader of the Wi-Fi Extension 2.0.
        Returns the number of actually read bytes.

        Before this function can be used the bootloader has to be started using the
        :func:`Start Wifi2 Bootloader` function.

        It is recommended to use the Brick Viewer to update the firmware of the Wi-Fi
        Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        if not 0 <= length <= 60:
            raise ValueError(f"Invalid argument: expected 0 <= length <= 60, got length={length!r}")

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_WIFI2_SERIAL_PORT,
            data=pack_payload((int(length),), "B"),
            response_expected=True,
        )
        return ReadWifi2SerialPort(*unpack_payload(payload, "60B B"))

    async def set_wifi2_authentication_secret(self, secret: bytes | str, response_expected: bool = True):
        """
        Sets the Wi-Fi authentication secret. The secret can be a string of up to 64
        characters. An empty string disables the authentication. The default value is
        an empty string (authentication disabled).

        See the :ref:`authentication tutorial <tutorial_authentication>` for more
        information.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        if not isinstance(secret, bytes):
            secret = secret.encode("utf-8")
        if len(secret) > 64:
            raise ValueError(f"Invalid argument: expected len(secret) <= 64, got secret={secret!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_AUTHENTICATION_SECRET,
            data=pack_payload((secret,), "64s"),
            response_expected=response_expected,
        )

    async def get_wifi2_authentication_secret(self) -> bytes:
        """
        Returns the Wi-Fi authentication secret as set by
        :func:`Set Wifi2 Authentication Secret`.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_AUTHENTICATION_SECRET, response_expected=True
        )

        return unpack_payload(payload, "64s")

    async def set_wifi2_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        port: int = 4223,
        websocket_port: int = 4280,
        website_port: int = 80,
        phy_mode: PhyMode = PhyMode.WIFI_G,
        sleep_mode: int = 0,
        website: bool = False,
        response_expected=True,
    ) -> None:
        """
        Sets the general configuration of the Wi-Fi Extension 2.0.

        The ``port`` parameter sets the port number that your program will connect
        to. The default value is 4223.

        The ``websocket_port`` parameter sets the WebSocket port number that your
        JavaScript programm will connect to. The default value is 4280.

        The ``website_port`` parameter sets the port number for the website of the
        Wi-Fi Extension 2.0. The default value is 80.

        The ``phy_mode`` parameter sets the specific wireless network mode to be used.
        Possible values are B, G and N. The default value is G.

        The ``sleep_mode`` parameter is currently unused.

        The ``website`` parameter is used to enable or disable the web interface of
        the Wi-Fi Extension 2.0, which is available from firmware version 2.0.1. Note
        that, for firmware version 2.0.3 and older, to disable the the web interface
        the ``website_port`` parameter must be set to 1 and greater than 1 to enable
        the web interface. For firmware version 2.0.4 and later, setting this parameter
        to 1 will enable the web interface and setting it to 0 will disable the web
        interface.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        if not 1 <= port <= 65535:
            raise ValueError(f"Invalid argument: expected 1 <= port <= 65535, got port={port!r}")
        if not 1 <= websocket_port <= 65535:
            raise ValueError(
                f"Invalid argument: expected 1 <= websocket_port <= 65535, got websocket_port={websocket_port!r}"
            )
        if not 1 <= website_port <= 65535:
            raise ValueError(
                f"Invalid argument: expected 1 <= website_port <= 65535, got website_port={website_port!r}"
            )
        if not 0 <= sleep_mode <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= sleep_mode <= 255, got sleep_mode={sleep_mode!r}")
        if not 0 <= int(website) <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= int(website) <= 255, got website={website!r}")
        if not isinstance(phy_mode, PhyMode):
            phy_mode = PhyMode(phy_mode)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_CONFIGURATION,
            data=pack_payload(
                (int(port), int(websocket_port), int(website_port), phy_mode.value, int(sleep_mode), int(website)),
                "H H H B B B",
            ),
            response_expected=response_expected,
        )

    async def get_wifi2_configuration(self) -> GetWifi2Configuration:
        """
        Returns the general configuration as set by :func:`Set Wifi2 Configuration`.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_CONFIGURATION, response_expected=True
        )

        port, websocket_port, website_port, phy_mode, sleep_mode, website = unpack_payload(payload, "H H H B B B")
        phy_mode = PhyMode(phy_mode)
        website = bool(website)
        return GetWifi2Configuration(port, websocket_port, website_port, phy_mode, sleep_mode, website)

    async def get_wifi2_status(self) -> GetWifi2Status:  # pylint: disable=too-many-locals
        """
        Returns the client and access point status of the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_STATUS, response_expected=True
        )

        (
            client_enabled,
            client_status,
            client_ip,
            client_subnet_mask,
            client_gateway,
            client_mac_address,
            client_rx_count,
            client_tx_count,
            client_rssi,
            ap_enabled,
            ap_ip,
            ap_subnet_mask,
            ap_gateway,
            ap_mac_address,
            ap_rx_count,
            ap_tx_count,
            ap_connected_count,
        ) = unpack_payload(payload, "! B 4B 4B 4B 6B I I b ! 4B 4B 4B 6B I I B")

        return GetWifi2Status(
            client_enabled,
            WifiClientStatus(client_status),
            client_ip,
            client_subnet_mask,
            client_gateway,
            client_mac_address,
            client_rx_count,
            client_tx_count,
            client_rssi,
            ap_enabled,
            ap_ip,
            ap_subnet_mask,
            ap_gateway,
            ap_mac_address,
            ap_rx_count,
            ap_tx_count,
            ap_connected_count,
        )

    async def set_wifi2_client_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        enable: bool = True,
        ssid: bytes | str = "tinkerforge",
        ip_address: tuple[int, int, int, int] = (0, 0, 0, 0),
        subnet_mask: tuple[int, int, int, int] = (0, 0, 0, 0),
        gateway: tuple[int, int, int, int] = (0, 0, 0, 0),
        mac_address: tuple[int, int, int, int, int, int] = (0, 0, 0, 0, 0, 0),
        bssid: tuple[int, int, int, int, int, int] = (0, 0, 0, 0, 0, 0),
        response_expected: bool = True,
    ) -> None:
        """
        Sets the client specific configuration of the Wi-Fi Extension 2.0.

        The ``enable`` parameter enables or disables the client part of the
        Wi-Fi Extension 2.0. The default value is *true*.

        The ``ssid`` parameter sets the SSID (up to 32 characters) of the access point
        to connect to.

        If the ``ip`` parameter is set to all zero then ``subnet_mask`` and ``gateway``
        parameters are also set to all zero and DHCP is used for IP address configuration.
        Otherwise those three parameters can be used to configure a static IP address.
        The default configuration is DHCP.

        If the ``mac_address`` parameter is set to all zero then the factory MAC
        address is used. Otherwise this parameter can be used to set a custom MAC
        address.

        If the ``bssid`` parameter is set to all zero then Wi-Fi Extension 2.0 will
        connect to any access point that matches the configured SSID. Otherwise this
        parameter can be used to make the Wi-Fi Extension 2.0 only connect to an
        access point if SSID and BSSID match.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
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
        if not (isinstance(mac_address, (tuple, list)) and len(mac_address) == 6):
            raise ValueError(
                "Invalid argument: expected isinstance(mac_address, (tuple, list)) and len(mac_address) "
                "== 6, "
                f"got mac_address={mac_address!r}"
            )
        if not (isinstance(bssid, (tuple, list)) and len(bssid) == 6):
            raise ValueError(
                "Invalid argument: expected isinstance(bssid, (tuple, list)) and len(bssid) == 6, "
                f"got bssid={bssid!r}"
            )

        if not isinstance(ssid, bytes):
            ssid = ssid.encode("utf-8")
        if len(ssid) > 32:
            raise ValueError(f"Invalid argument: expected len(ssid) <= 32, got ssid={ssid!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_CLIENT_CONFIGURATION,
            data=pack_payload(
                (
                    bool(enable),
                    ssid,
                    list(map(int, ip_address)),
                    list(map(int, subnet_mask)),
                    list(map(int, gateway)),
                    list(map(int, mac_address)),
                    list(map(int, bssid)),
                ),
                "! 32s 4B 4B 4B 6B 6B",
            ),
            response_expected=response_expected,
        )

    async def get_wifi2_client_configuration(self) -> GetWifi2ClientConfiguration:
        """
        Returns the client configuration as set by :func:`Set Wifi2 Client Configuration`.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_CLIENT_CONFIGURATION, response_expected=True
        )

        enable, ssid, ip_address, subnet_mask, gateway, mac_address, bssid = unpack_payload(
            payload, "! 32s 4B 4B 4B 6B 6B"
        )
        return GetWifi2ClientConfiguration(enable, ssid, ip_address, subnet_mask, gateway, mac_address, bssid)

    async def set_wifi2_client_hostname(
        self, hostname: bytes | str = "wifi-extension-v2", response_expected: bool = True
    ) -> None:
        """
        Sets the client hostname (up to 32 characters) of the Wi-Fi Extension 2.0. The
        hostname will be displayed by access points as the hostname in the DHCP clients
        table.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        if not isinstance(hostname, bytes):
            hostname = hostname.encode("ascii")

        # Test if the hostname is valid
        # Check for hostnames as per RFC 1123. This allows labels that start with
        # a digit or hyphen, which was not allowed in RFC 952 originally
        # The bricks only allow 32 characters as opposed to 63 as per RFC.
        hostname = hostname.lower()
        allowed = re.compile(rb"^(?!-)[a-z0-9-]{2,32}(?<!-)$")
        if not bool(allowed.match(hostname)):
            raise ValueError("Invalid hostname")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_CLIENT_HOSTNAME,
            data=pack_payload((hostname,), "32s"),
            response_expected=response_expected,
        )

    async def get_wifi2_client_hostname(self) -> bytes:
        """
        Returns the client hostname as set by :func:`Set Wifi2 Client Hostname`.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_CLIENT_HOSTNAME, response_expected=True
        )
        return unpack_payload(payload, "32s")

    async def set_wifi2_client_password(self, password: bytes | str, response_expected: bool = True) -> None:
        """
        Sets the client password (up to 63 chars) for WPA/WPA2 encryption.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        if not isinstance(password, bytes):
            password = password.encode("utf-8")
        if not 8 <= len(password) <= 63:
            raise ValueError(f"Invalid argument: expected 8 <= len(password) <= 63, got password={password!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_CLIENT_PASSWORD,
            data=pack_payload((password,), "64s"),
            response_expected=response_expected,
        )

    async def get_wifi2_client_password(self) -> bytes:
        """
        Returns the client password as set by :func:`Set Wifi2 Client Password`.

        .. note::
         Since Wi-Fi Extension 2.0 firmware version 2.1.3 the password is not
         returned anymore.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        warnings.warn(
            "get_wifi2_client_password is deprecated. It will only return the password in FW version <= 2.1.2.",
            DeprecationWarning,
        )
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_CLIENT_PASSWORD, response_expected=True
        )
        return unpack_payload(payload, "64s")

    async def set_wifi2_ap_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        enable: bool = True,
        ssid: bytes | str = "WIFI Extension 2.0 Access Point",
        ip_address: tuple[int, int, int, int] = (0, 0, 0, 0),
        subnet_mask: tuple[int, int, int, int] = (0, 0, 0, 0),
        gateway: tuple[int, int, int, int] = (0, 0, 0, 0),
        encryption: WifiApEncryption = WifiApEncryption.WPA2_PSK,
        hidden: bool = False,
        channel: int = 1,
        mac_address: tuple[int, int, int, int, int, int] = (0, 0, 0, 0, 0, 0),
        response_expected: bool = True,
    ) -> None:
        """
        Sets the access point specific configuration of the Wi-Fi Extension 2.0.

        The ``enable`` parameter enables or disables the access point part of the
        Wi-Fi Extension 2.0. The default value is true.

        The ``ssid`` parameter sets the SSID (up to 32 characters) of the access point.

        If the ``ip`` parameter is set to all zero then ``subnet_mask`` and ``gateway``
        parameters are also set to all zero and DHCP is used for IP address configuration.
        Otherwise those three parameters can be used to configure a static IP address.
        The default configuration is DHCP.

        The ``encryption`` parameter sets the encryption mode to be used. Possible
        values are Open (no encryption), WEP or WPA/WPA2 PSK. The default value is
        WPA/WPA2 PSK. Use the :func:`Set Wifi2 AP Password` function to set the encryption
        password.

        The ``hidden`` parameter makes the access point hide or show its SSID.
        The default value is *false*.

        The ``channel`` parameter sets the channel (1 to 13) of the access point.
        The default value is 1.

        If the ``mac_address`` parameter is set to all zero then the factory MAC
        address is used. Otherwise this parameter can be used to set a custom MAC
        address.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
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
        if not (isinstance(mac_address, (tuple, list)) and len(mac_address) == 6):
            raise ValueError(
                "Invalid argument: expected isinstance(mac_address, (tuple, list)) and len(mac_address) "
                "== 6, "
                f"got mac_address={mac_address!r}"
            )
        if not isinstance(encryption, WifiApEncryption):
            encryption = WifiApEncryption(encryption)
        if not 1 <= channel <= 13:
            raise ValueError(f"Invalid argument: expected 1 <= channel <= 13, got channel={channel!r}")
        if not isinstance(ssid, bytes):
            ssid = ssid.encode("utf-8")
        if len(ssid) > 32:
            raise ValueError(f"Invalid argument: expected len(ssid) <= 32, got ssid={ssid!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_AP_CONFIGURATION,
            data=pack_payload(
                (
                    bool(enable),
                    ssid,
                    list(map(int, ip_address)),
                    list(map(int, subnet_mask)),
                    list(map(int, gateway)),
                    encryption.value,
                    hidden,
                    int(channel),
                    list(map(int, mac_address)),
                ),
                "! 32s 4B 4B 4B B ! B 6B",
            ),
            response_expected=response_expected,
        )

    async def get_wifi2_ap_configuration(self) -> GetWifi2APConfiguration:
        """
        Returns the access point configuration as set by :func:`Set Wifi2 AP Configuration`.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_AP_CONFIGURATION, response_expected=True
        )

        enable, ssid, ip_address, subnet_mask, gateway, encryption, hidden, channel, mac_address = unpack_payload(
            payload, "! 32s 4B 4B 4B B ! B 6B"
        )

        return GetWifi2APConfiguration(
            enable,
            ssid,
            ip_address,
            subnet_mask,
            gateway,
            WifiApEncryption(encryption),
            hidden,
            channel,
            mac_address,
        )

    async def set_wifi2_ap_password(self, password: bytes | str, response_expected: bool = True) -> None:
        """
        Sets the access point password (up to 63 chars) for the configured encryption
        mode, see :func:`Set Wifi2 AP Configuration`.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        if not isinstance(password, bytes):
            password = password.encode("utf-8")
        if not 8 <= len(password) <= 63:
            raise ValueError(f"Invalid argument: expected 8 <= len(password) <= 63, got password={password!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_AP_PASSWORD,
            data=pack_payload((password,), "64s"),
            response_expected=response_expected,
        )

    async def get_wifi2_ap_password(self) -> bytes:
        """
        Returns the access point password as set by :func:`Set Wifi2 AP Password`.

        .. note::
         Since Wi-Fi Extension 2.0 firmware version 2.1.3 the password is not
         returned anymore.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        warnings.warn(
            "get_wifi2_ap_password is deprecated. It will only return the password in FW version <= 2.1.2.",
            DeprecationWarning,
        )
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_AP_PASSWORD, response_expected=True
        )
        return unpack_payload(payload, "64s")

    async def save_wifi2_configuration(self) -> int:
        """
        All configuration functions for the Wi-Fi Extension 2.0 do not change the
        values permanently. After configuration this function has to be called to
        permanently store the values.

        The values are stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after configuration.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.SAVE_WIFI2_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def get_wifi2_firmware_version(self) -> tuple[int, int, int]:
        """
        Returns the current version of the Wi-Fi Extension 2.0 firmware (major, minor, revision).

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_FIRMWARE_VERSION, response_expected=True
        )
        return unpack_payload(payload, "3B")

    async def set_wifi2_status_led(self, enabled: bool, response_expected: bool = True) -> None:
        """
        Configure the green status LED of the Wi-Fi Extension 2.0. Alternatively
        you can call enable_wifi2_status_led() and disable_wifi2_status_led().
        """
        if enabled:  # pylint: disable=no-else-return
            return await self.enable_wifi2_status_led(response_expected)
        else:
            return await self.disable_wifi2_status_led(response_expected)

    async def enable_wifi2_status_led(self, response_expected: bool = True) -> None:
        """
        Turns the green status LED of the Wi-Fi Extension 2.0 on.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_WIFI2_STATUS_LED, response_expected=response_expected
        )

    async def disable_wifi2_status_led(self, response_expected: bool = True) -> None:
        """
        Turns the green status LED of the Wi-Fi Extension 2.0 off.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_WIFI2_STATUS_LED, response_expected=response_expected
        )

    async def is_wifi2_status_led_enabled(self) -> bool:
        """
        Returns *true* if the green status LED of the Wi-Fi Extension 2.0 is turned on.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_WIFI2_STATUS_LED_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_wifi2_mesh_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        enable: bool = False,
        root_ip: tuple[int, int, int, int] = (0, 0, 0, 0),
        root_subnet_mask: tuple[int, int, int, int] = (0, 0, 0, 0),
        root_gateway: tuple[int, int, int, int] = (0, 0, 0, 0),
        router_bssid: tuple[int, int, int, int, int, int] = (0, 0, 0, 0, 0, 0),
        group_id: tuple[int, int, int, int, int, int] = (0x1A, 0xFE, 0x34, 0, 0, 0),
        group_ssid_prefix: bytes | str = "TF_MESH",
        gateway_ip: tuple[int, int, int, int] = (0, 0, 0, 0),
        gateway_port: int = 4240,
        response_expected: bool = True,
    ) -> None:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Sets the mesh specific configuration of the Wi-Fi Extension 2.0.

        The ``enable`` parameter enables or disables the mesh part of the
        Wi-Fi Extension 2.0. The default value is *false*. The mesh part cannot be
        enabled together with the client and access-point part.

        If the ``root_ip`` parameter is set to all zero then ``root_subnet_mask``
        and ``root_gateway`` parameters are also set to all zero and DHCP is used for
        IP address configuration. Otherwise those three parameters can be used to
        configure a static IP address. The default configuration is DHCP.

        If the ``router_bssid`` parameter is set to all zero then the information is
        taken from Wi-Fi scan when connecting the SSID as set by
        :func:`Set Wifi2 Mesh Router SSID`. This only works if the the SSID is not hidden.
        In case the router has hidden SSID this parameter must be specified, otherwise
        the node will not be able to reach the mesh router.

        The ``group_id`` and the ``group_ssid_prefix`` parameters identifies a
        particular mesh network and nodes configured with same ``group_id`` and the
        ``group_ssid_prefix`` are considered to be in the same mesh network.

        The ``gateway_ip`` and the ``gateway_port`` parameters specifies the location
        of the brickd that supports mesh feature.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        if not (isinstance(root_ip, (tuple, list)) and len(root_ip) == 4):
            raise ValueError(
                "Invalid argument: expected isinstance(root_ip, (tuple, list)) and len(root_ip) == 4, "
                f"got root_ip={root_ip!r}"
            )
        if not (isinstance(root_subnet_mask, (tuple, list)) and len(root_subnet_mask) == 4):
            raise ValueError(
                "Invalid argument: expected isinstance(root_subnet_mask, (tuple, list)) and "
                "len(root_subnet_mask) == 4, "
                f"got root_subnet_mask={root_subnet_mask!r}"
            )
        if not (isinstance(root_gateway, (tuple, list)) and len(root_gateway) == 4):
            raise ValueError(
                "Invalid argument: expected isinstance(root_gateway, (tuple, list)) and len(root_gateway) "
                "== 4, "
                f"got root_gateway={root_gateway!r}"
            )
        if not (isinstance(gateway_ip, (tuple, list)) and len(gateway_ip) == 4):
            raise ValueError(
                "Invalid argument: expected isinstance(gateway_ip, (tuple, list)) and len(gateway_ip) == "
                "4, "
                f"got gateway_ip={gateway_ip!r}"
            )
        if not (isinstance(root_gateway, (tuple, list)) and len(root_gateway) == 4):
            raise ValueError(
                "Invalid argument: expected isinstance(root_gateway, (tuple, list)) and len(root_gateway) "
                "== 4, "
                f"got root_gateway={root_gateway!r}"
            )
        if not (isinstance(router_bssid, (tuple, list)) and len(router_bssid) == 6):
            raise ValueError(
                "Invalid argument: expected isinstance(router_bssid, (tuple, list)) and len(router_bssid) "
                "== 6, "
                f"got router_bssid={router_bssid!r}"
            )
        if not (isinstance(group_id, (tuple, list)) and len(group_id) == 6):
            raise ValueError(
                "Invalid argument: expected isinstance(group_id, (tuple, list)) and len(group_id) == 6, "
                f"got group_id={group_id!r}"
            )
        if not 1 <= gateway_port <= 65535:
            raise ValueError(
                f"Invalid argument: expected 1 <= gateway_port <= 65535, got gateway_port={gateway_port!r}"
            )
        if not isinstance(group_ssid_prefix, bytes):
            group_ssid_prefix = group_ssid_prefix.encode("utf-8")
        if len(group_ssid_prefix) > 16:
            raise ValueError(
                "Invalid argument: expected len(group_ssid_prefix) <= 16, "
                f"got group_ssid_prefix={group_ssid_prefix!r}"
            )

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_MESH_CONFIGURATION,
            data=pack_payload(
                (
                    bool(enable),
                    list(map(int, root_ip)),
                    list(map(int, root_subnet_mask)),
                    list(map(int, root_gateway)),
                    list(map(int, router_bssid)),
                    list(map(int, group_id)),
                    group_ssid_prefix,
                    list(map(int, gateway_ip)),
                    int(gateway_port),
                ),
                "! 4B 4B 4B 6B 6B 16s 4B H",
            ),
            response_expected=response_expected,
        )

    async def get_wifi2_mesh_configuration(self) -> GetWifi2MeshConfiguration:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Returns the mesh configuration as set by :func:`Set Wifi2 Mesh Configuration`.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_MESH_CONFIGURATION, response_expected=True
        )
        (
            enable,
            root_ip,
            root_subnet_mask,
            root_gateway,
            router_bssid,
            group_id,
            group_ssid_prefix,
            gateway_ip,
            gateway_port,
        ) = unpack_payload(payload, "! 4B 4B 4B 6B 6B 16s 4B H")

        return GetWifi2MeshConfiguration(
            enable,
            root_ip,
            root_subnet_mask,
            root_gateway,
            router_bssid,
            group_id,
            group_ssid_prefix,
            gateway_ip,
            gateway_port,
        )

    async def set_wifi2_mesh_router_ssid(self, ssid: bytes | str, response_expected: bool = True) -> None:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Sets the mesh router SSID of the Wi-Fi Extension 2.0.
        It is used to specify the mesh router to connect to.

        Note that even though in the argument of this function a 32 characters long SSID
        is allowed, in practice valid SSID should have a maximum of 31 characters. This
        is due to a bug in the mesh library that we use in the firmware of the extension.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        if not isinstance(ssid, bytes):
            ssid = ssid.encode("utf-8")
        if len(ssid) > 32:
            raise ValueError(f"Invalid argument: expected len(ssid) <= 32, got ssid={ssid!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_MESH_ROUTER_SSID,
            data=pack_payload((ssid,), "32s"),
            response_expected=response_expected,
        )

    async def get_wifi2_mesh_router_ssid(self) -> bytes:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Returns the mesh router SSID as set by :func:`Set Wifi2 Mesh Router SSID`.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_MESH_ROUTER_SSID, response_expected=True
        )
        return unpack_payload(payload, "32s")

    async def set_wifi2_mesh_router_password(self, password: bytes | str, response_expected: bool = True) -> None:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Sets the mesh router password (up to 64 characters) for WPA/WPA2 encryption.
        The password will be used to connect to the mesh router.

        To apply configuration changes to the Wi-Fi Extension 2.0 the
        :func:`Save Wifi2 Configuration` function has to be called and the Master Brick
        has to be restarted afterwards.

        It is recommended to use the Brick Viewer to configure the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        if not isinstance(password, bytes):
            password = password.encode("utf-8")
        if not 8 <= len(password) <= 63:
            raise ValueError(f"Invalid argument: expected 8 <= len(password) <= 63, got password={password!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI2_MESH_ROUTER_PASSWORD,
            data=pack_payload((password,), "64s"),
            response_expected=response_expected,
        )

    async def get_wifi2_mesh_router_password(self) -> bytes:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Returns the mesh router password as set by :func:`Set Wifi2 Mesh Router Password`.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        warnings.warn(
            "get_wifi2_mesh_router_password is deprecated. It will only return the password in FW version <= 2.1.2.",
            DeprecationWarning,
        )
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_MESH_ROUTER_PASSWORD, response_expected=True
        )
        return unpack_payload(payload, "64s")

    async def get_wifi2_mesh_common_status(self) -> GetWifi2MeshCommonStatus:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Returns the common mesh status of the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_MESH_COMMON_STATUS, response_expected=True
        )
        status, is_root_node, is_root_candidate, connected_nodes, rx_count, tx_count = unpack_payload(
            payload, "B ! ! H I I"
        )
        status = WifiMeshStatus(status)

        return GetWifi2MeshCommonStatus(status, is_root_node, is_root_candidate, connected_nodes, rx_count, tx_count)

    async def get_wifi2_mesh_client_status(self) -> GetWifi2MeshClientStatus:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Returns the mesh client status of the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_MESH_CLIENT_STATUS, response_expected=True
        )
        hostname, ip_address, subnet_mask, gateway, mac_address = unpack_payload(payload, "32s 4B 4B 4B 6B")
        return GetWifi2MeshClientStatus(
            hostname,
            ip_address,
            subnet_mask,
            gateway,
            mac_address,
        )

    async def get_wifi2_mesh_ap_status(self) -> GetWifi2MeshAPStatus:
        """
        Requires Wi-Fi Extension 2.0 firmware 2.1.0.

        Returns the mesh AP status of the Wi-Fi Extension 2.0.

        .. versionadded:: 2.4.2$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI2_MESH_AP_STATUS, response_expected=True
        )
        hostname, ip_address, subnet_mask, gateway, mac_address = unpack_payload(payload, "32s 4B 4B 4B 6B")
        return GetWifi2MeshAPStatus(
            hostname,
            ip_address,
            subnet_mask,
            gateway,
            mac_address,
        )
