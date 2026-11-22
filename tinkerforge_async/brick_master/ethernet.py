"""
Ethernet Extension of the Master Brick.
"""

# pylint: disable=too-many-lines,duplicate-code
from __future__ import annotations

import re
from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple, cast

from ..devices import Device
from ..ip_connection_helper import pack_payload, unpack_payload
from .common import FunctionID

if TYPE_CHECKING:
    from ..ip_connection import IPConnectionAsync


class GetEthernetConfiguration(NamedTuple):
    connection: EthernetConnection
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    port: int


class GetEthernetStatus(NamedTuple):
    mac_address: tuple[int, int, int, int, int, int]
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    rx_count: int
    tx_count: int
    hostname: str


class GetEthernetWebsocketConfiguration(NamedTuple):
    sockets: int
    port: int


@unique
class EthernetConnection(Enum):
    """
    Configures the Ethernet Extension for either DHCP or a static ip.
    """

    DHCP = 0
    STATIC_IP = 1


class PhyMode(Enum):
    """
    Configures the Wi-Fi mode of the Wi-Fi 2.0 Extension
    """

    WIFI_B = 0
    WIFI_G = 1
    WIFI_N = 2


class EthernetExtension(Device):
    """
    The functions of the Ethernet Extension.
    """

    async def is_ethernet_present(self) -> bool:
        """
        Returns *true* if a Ethernet Extension is available to be used by the Master
        Brick.

        .. versionadded:: 2.1.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_ETHERNET_PRESENT, response_expected=True
        )

        return cast(bool, unpack_payload(payload, "!"))

    async def set_ethernet_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        connection: EthernetConnection,
        ip_address: tuple[int, int, int, int] = (0, 0, 0, 0),
        subnet_mask: tuple[int, int, int, int] = (0, 0, 0, 0),
        gateway: tuple[int, int, int, int] = (0, 0, 0, 0),
        port: int = 4223,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration of the Ethernet Extension. Possible values for
        ``connection`` are:

        .. csv-table::
         :header: "Value", "Description"
         :widths: 10, 90

         "0", "DHCP"
         "1", "Static IP"

        If you set ``connection`` to static IP options then you have to supply ``ip``,
        ``subnet_mask`` and ``gateway`` as an array of size 4 (first element of the
        array is the least significant byte of the address). If ``connection`` is set
        to the DHCP options then ``ip``, ``subnet_mask`` and ``gateway`` are ignored,
        you can set them to 0.

        The last parameter is the port that your program will connect to. The
        default port, that is used by brickd, is 4223.

        The values are stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after configuration.

        It is recommended to use the Brick Viewer to set the Ethernet configuration.

        .. versionadded:: 2.1.0$nbsp;(Firmware)
        """
        if not isinstance(connection, EthernetConnection):
            connection = EthernetConnection(connection)
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

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ETHERNET_CONFIGURATION,
            data=pack_payload(
                (
                    connection.value,
                    list(map(int, ip_address)),
                    list(map(int, subnet_mask)),
                    list(map(int, gateway)),
                    int(port),
                ),
                "B 4B 4B 4B H",
            ),
            response_expected=response_expected,
        )

    async def get_ethernet_configuration(self) -> GetEthernetConfiguration:
        """
        Returns the configuration as set by :func:`Set Ethernet Configuration`.

        .. versionadded:: 2.1.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ETHERNET_CONFIGURATION, response_expected=True
        )

        connection, ip_addr, subnet_mask, gateway, port = unpack_payload(payload, "B 4B 4B 4B H")
        return GetEthernetConfiguration(EthernetConnection(connection), ip_addr, subnet_mask, gateway, port)

    async def get_ethernet_status(self) -> GetEthernetStatus:
        """
        Returns the status of the Ethernet Extension.

        ``mac_address``, ``ip``, ``subnet_mask`` and ``gateway`` are given as an array.
        The first element of the array is the least significant byte of the address.

        ``rx_count`` and ``tx_count`` are the number of bytes that have been
        received/send since last restart.

        ``hostname`` is the currently used hostname.

        .. versionadded:: 2.1.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ETHERNET_STATUS, response_expected=True
        )

        return GetEthernetStatus(*unpack_payload(payload, "6B 4B 4B 4B I I 32s"))

    async def set_ethernet_hostname(self, hostname: bytes | str, response_expected: bool = True) -> None:
        """
        Sets the hostname of the Ethernet Extension. The hostname will be displayed
        by access points as the hostname in the DHCP clients table.

        Setting an empty String will restore the default hostname.

        The current hostname can be discovered with :func:`Get Ethernet Status`.

        .. versionadded:: 2.1.0$nbsp;(Firmware)
        """
        if not isinstance(hostname, bytes):
            hostname = hostname.encode("ascii")

        # Test if the hostname is valid
        # Check for hostnames as per RFC 1123. This allows labels that start with
        # a digit or hyphen, which was not allowed in RFC 952 originally
        # The bricks only allow 32 characters as opposed to 63 as per RFC.
        # Allow 0 characters to reset the hostname (this is TF specific)
        hostname = hostname.lower()
        if len(hostname) != 0:
            allowed = re.compile(rb"^(?!-)[a-z0-9-]{2,32}(?<!-)$")
            if not bool(allowed.match(hostname)):
                raise ValueError("Invalid hostname")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ETHERNET_HOSTNAME,
            data=pack_payload((hostname,), "32s"),
            response_expected=response_expected,
        )

    async def set_ethernet_mac_address(
        self, mac_address: tuple[int, int, int, int, int, int], response_expected: bool = True
    ) -> None:
        """
        Sets the MAC address of the Ethernet Extension. The Ethernet Extension should
        come configured with a valid MAC address, that is also written on a
        sticker of the extension itself.

        The MAC address can be read out again with :func:`Get Ethernet Status`.

        .. versionadded:: 2.1.0$nbsp;(Firmware)
        """
        if not (isinstance(mac_address, (tuple, list)) and len(mac_address) == 6):
            raise ValueError(
                "Invalid argument: expected isinstance(mac_address, (tuple, list)) and len(mac_address) "
                "== 6, "
                f"got mac_address={mac_address!r}"
            )

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ETHERNET_MAC_ADDRESS,
            data=pack_payload((list(map(int, mac_address)),), "6B"),
            response_expected=response_expected,
        )

    async def set_ethernet_websocket_configuration(
        self, sockets: int, port: int, response_expected: bool = True
    ) -> None:
        """
        Sets the Ethernet WebSocket configuration. The first parameter sets the number of socket
        connections that are reserved for WebSockets. The range is 0-7. The connections
        are shared with the plain sockets. Example: If you set the connections to 3,
        there will be 3 WebSocket and 4 plain socket connections available.

        The second parameter is the port for the WebSocket connections. The port can
        not be the same as the port for the plain socket connections.

        The values are stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after configuration.

        It is recommended to use the Brick Viewer to set the Ethernet configuration.

        The default values are 3 for the socket connections and 4280 for the port.

        .. versionadded:: 2.2.0$nbsp;(Firmware)
        """
        if not 0 <= sockets <= 7:
            raise ValueError(f"Invalid argument: expected 0 <= sockets <= 7, got sockets={sockets!r}")
        if not 1 <= port <= 65535:
            raise ValueError(f"Invalid argument: expected 1 <= port <= 65535, got port={port!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ETHERNET_WEBSOCKET_CONFIGURATION,
            data=pack_payload(
                (
                    int(sockets),
                    int(port),
                ),
                "B H",
            ),
            response_expected=response_expected,
        )

    async def get_ethernet_websocket_configuration(self) -> GetEthernetWebsocketConfiguration:
        """
        Returns the configuration as set by :func:`Set Ethernet Configuration`.

        .. versionadded:: 2.2.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ETHERNET_WEBSOCKET_CONFIGURATION, response_expected=True
        )

        return GetEthernetWebsocketConfiguration(*unpack_payload(payload, "B H"))

    async def set_ethernet_authentication_secret(self, secret: bytes | str, response_expected: bool = True) -> None:
        """
        Sets the Ethernet authentication secret. The secret can be a string of up to 64
        characters. An empty string disables the authentication.

        See the :ref:`authentication tutorial <tutorial_authentication>` for more
        information.

        The secret is stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after configuration.

        It is recommended to use the Brick Viewer to set the Ethernet authentication secret.

        The default value is an empty string (authentication disabled).

        .. versionadded:: 2.2.0$nbsp;(Firmware)
        """
        if not isinstance(secret, bytes):
            secret = secret.encode("utf-8")
        if len(secret) > 64:
            raise ValueError(f"Invalid argument: expected len(secret) <= 64, got secret={secret!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ETHERNET_AUTHENTICATION_SECRET,
            data=pack_payload((secret,), "64s"),
            response_expected=response_expected,
        )

    async def get_ethernet_authentication_secret(self) -> str:
        """
        Returns the authentication secret as set by
        :func:`Set Ethernet Authentication Secret`.

        .. versionadded:: 2.2.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ETHERNET_AUTHENTICATION_SECRET, response_expected=True
        )

        return cast(str, unpack_payload(payload, "64s"))
