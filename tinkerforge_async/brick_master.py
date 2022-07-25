"""
Module for the Tinkerforge Master Brick (https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html)
implemented using Python AsyncIO. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""
# pylint: disable=too-many-lines
from __future__ import annotations

import asyncio
import re
import warnings
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, Iterable, NamedTuple

from .devices import BasicCallbackConfiguration
from .devices import BrickletPort as Port
from .devices import DeviceIdentifier, DeviceWithMCU, Event, GetSPITFPErrorCount
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


class GetChibiErrorLog(NamedTuple):
    underrun: int
    no_ack: int
    crc_error: int
    overflow: int


class GetRS485Configuration(NamedTuple):
    speed: int
    parity: Rs485Parity
    stopbits: int


class GetWifiConfiguration(NamedTuple):
    ssid: bytes
    connection: WifiConnection
    ip_address: tuple[int, int, int, int]
    subnet_mask: tuple[int, int, int, int]
    gateway: tuple[int, int, int, int]
    port: int


class GetWifiEncryption(NamedTuple):
    encryption: WifiEncryptionMode
    key_index: bytes
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
    ]
    data_length: int


class GetWifiBufferInfo(NamedTuple):
    overflow: int
    low_watermark: int
    used: int


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
    hostname: bytes


class GetEthernetWebsocketConfiguration(NamedTuple):
    sockets: int
    port: int


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


class GetSPITFPBaudrateConfig(NamedTuple):
    enable_dynamic_baudrate: bool
    minimum_dynamic_baudrate: int


class GetProtocol1BrickletName(NamedTuple):
    protocol_version: int
    firmware_version: tuple[int, int, int]
    name: bytes


class Wifi2BootloaderError(Exception):
    """
    Raised if the bootloader of the Wi-Fi 2.0 extension did not come up or is
    unresponsive
    """


@unique
class CallbackID(Enum):
    """
    The callbacks available to this brick
    """

    STACK_CURRENT = 59
    STACK_VOLTAGE = 60
    USB_VOLTAGE = 61
    STACK_CURRENT_REACHED = 62
    STACK_VOLTAGE_REACHED = 63
    USB_VOLTAGE_REACHED = 64


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """

    GET_STACK_VOLTAGE = 1
    GET_STACK_CURRENT = 2
    SET_EXTENSION_TYPE = 3
    GET_EXTENSION_TYPE = 4
    # Chibi
    IS_CHIBI_PRESENT = 5
    SET_CHIBI_ADDRESS = 6
    GET_CHIBI_ADDRESS = 7
    SET_CHIBI_MASTER_ADDRESS = 8
    GET_CHIBI_MASTER_ADDRESS = 9
    SET_CHIBI_SLAVE_ADDRESS = 10
    GET_CHIBI_SLAVE_ADDRESS = 11
    GET_CHIBI_SIGNAL_STRENGTH = 12
    GET_CHIBI_ERROR_LOG = 13
    SET_CHIBI_FREQUENCY = 14
    GET_CHIBI_FREQUENCY = 15
    SET_CHIBI_CHANNEL = 16
    GET_CHIBI_CHANNEL = 17
    # RS485
    IS_RS485_PRESENT = 18
    SET_RS485_ADDRESS = 19
    GET_RS485_ADDRESS = 20
    SET_RS485_SLAVE_ADDRESS = 21
    GET_RS485_SLAVE_ADDRESS = 22
    GET_RS485_ERROR_LOG = 23
    SET_RS485_CONFIGURATION = 24
    GET_RS485_CONFIGURATION = 25
    # Wi-Fi 1.0
    IS_WIFI_PRESENT = 26
    SET_WIFI_CONFIGURATION = 27
    GET_WIFI_CONFIGURATION = 28
    SET_WIFI_ENCRYPTION = 29
    GET_WIFI_ENCRYPTION = 30
    GET_WIFI_STATUS = 31
    REFRESH_WIFI_STATUS = 32
    SET_WIFI_CERTIFICATE = 33
    GET_WIFI_CERTIFICATE = 34
    SET_WIFI_POWER_MODE = 35
    GET_WIFI_POWER_MODE = 36
    GET_WIFI_BUFFER_INFO = 37
    SET_WIFI_REGULATORY_DOMAIN = 38
    GET_WIFI_REGULATORY_DOMAIN = 39
    SET_LONG_WIFI_KEY = 41
    GET_LONG_WIFI_KEY = 42
    SET_WIFI_HOSTNAME = 43
    GET_WIFI_HOSTNAME = 44
    SET_WIFI_AUTHENTICATION_SECRET = 75
    GET_WIFI_AUTHENTICATION_SECRET = 76
    # Wi-Fi 2.0
    IS_WIFI2_PRESENT = 78
    START_WIFI2_BOOTLOADER = 79
    WRITE_WIFI2_SERIAL_PORT = 80
    READ_WIFI2_SERIAL_PORT = 81
    SET_WIFI2_AUTHENTICATION_SECRET = 82
    GET_WIFI2_AUTHENTICATION_SECRET = 83
    SET_WIFI2_CONFIGURATION = 84
    GET_WIFI2_CONFIGURATION = 85
    GET_WIFI2_STATUS = 86
    SET_WIFI2_CLIENT_CONFIGURATION = 87
    GET_WIFI2_CLIENT_CONFIGURATION = 88
    SET_WIFI2_CLIENT_HOSTNAME = 89
    GET_WIFI2_CLIENT_HOSTNAME = 90
    SET_WIFI2_CLIENT_PASSWORD = 91
    GET_WIFI2_CLIENT_PASSWORD = 92
    SET_WIFI2_AP_CONFIGURATION = 93
    GET_WIFI2_AP_CONFIGURATION = 94
    SET_WIFI2_AP_PASSWORD = 95
    GET_WIFI2_AP_PASSWORD = 96
    SAVE_WIFI2_CONFIGURATION = 97
    GET_WIFI2_FIRMWARE_VERSION = 98
    ENABLE_WIFI2_STATUS_LED = 99
    DISABLE_WIFI2_STATUS_LED = 100
    IS_WIFI2_STATUS_LED_ENABLED = 101
    SET_WIFI2_MESH_CONFIGURATION = 102
    GET_WIFI2_MESH_CONFIGURATION = 103
    SET_WIFI2_MESH_ROUTER_SSID = 104
    GET_WIFI2_MESH_ROUTER_SSID = 105
    SET_WIFI2_MESH_ROUTER_PASSWORD = 106
    GET_WIFI2_MESH_ROUTER_PASSWORD = 107
    GET_WIFI2_MESH_COMMON_STATUS = 108
    GET_WIFI2_MESH_CLIENT_STATUS = 109
    GET_WIFI2_MESH_AP_STATUS = 110
    # Ethernet
    IS_ETHERNET_PRESENT = 65
    SET_ETHERNET_CONFIGURATION = 66
    GET_ETHERNET_CONFIGURATION = 67
    GET_ETHERNET_STATUS = 68
    SET_ETHERNET_HOSTNAME = 69
    SET_ETHERNET_MAC_ADDRESS = 70
    SET_ETHERNET_WEBSOCKET_CONFIGURATION = 71
    GET_ETHERNET_WEBSOCKET_CONFIGURATION = 72
    SET_ETHERNET_AUTHENTICATION_SECRET = 73
    GET_ETHERNET_AUTHENTICATION_SECRET = 74
    # Other
    GET_USB_VOLTAGE = 40
    SET_STACK_CURRENT_CALLBACK_PERIOD = 45
    GET_STACK_CURRENT_CALLBACK_PERIOD = 46
    SET_STACK_VOLTAGE_CALLBACK_PERIOD = 47
    GET_STACK_VOLTAGE_CALLBACK_PERIOD = 48
    SET_USB_VOLTAGE_CALLBACK_PERIOD = 49
    GET_USB_VOLTAGE_CALLBACK_PERIOD = 50
    SET_STACK_CURRENT_CALLBACK_THRESHOLD = 51
    GET_STACK_CURRENT_CALLBACK_THRESHOLD = 52
    SET_STACK_VOLTAGE_CALLBACK_THRESHOLD = 53
    GET_STACK_VOLTAGE_CALLBACK_THRESHOLD = 54
    SET_USB_VOLTAGE_CALLBACK_THRESHOLD = 55
    GET_USB_VOLTAGE_CALLBACK_THRESHOLD = 56
    SET_DEBOUNCE_PERIOD = 57
    GET_DEBOUNCE_PERIOD = 58
    GET_CONNECTION_TYPE = 77
    SET_SPITFP_BAUDRATE_CONFIG = 231
    GET_SPITFP_BAUDRATE_CONFIG = 232
    GET_SEND_TIMEOUT_COUNT = 233
    SET_SPITFP_BAUDRATE = 234
    GET_SPITFP_BAUDRATE = 235
    GET_SPITFP_ERROR_COUNT = 237
    ENABLE_STATUS_LED = 238
    DISABLE_STATUS_LED = 239
    IS_STATUS_LED_ENABLED = 240
    GET_PROTOCOL1_BRICKLET_NAME = 241
    GET_CHIP_TEMPERATURE = 242


@unique
class ExtensionPosition(Enum):
    """
    The position of the master extension in the stack.
    """

    BOTTOM = 0
    TOP = 1


_ExtensionPosition = ExtensionPosition


@unique
class ExtensionType(Enum):
    """
    The types of master extensions available.
    """

    CHIBI = 1
    RS485 = 2
    WIFI = 3
    ETHERNET = 4
    WIFI2 = 5


_ExtensionType = ExtensionType  # We need the alias for MyPy type hinting


@unique
class ConnectionType(Enum):
    """
    The physical connection to the master brick.
    """

    NONE = 0
    USB = 1
    SPI_STACK = 2
    CHIBI = 3
    RS485 = 4
    WIFI = 5
    ETHERNET = 6
    WIFI_V2 = 7


_ConnectionType = ConnectionType  # We need the alias for MyPy type hinting


@unique
class ChibiFrequency(Enum):
    """
    The Chibi frequencies available.
    """

    OQPSK_868_MHZ = 0
    OQPSK_915_MHZ = 1
    OQPSK_750_MHZ = 2
    BPSK40_915_MHZ = 3


_ChibiFrequency = ChibiFrequency  # We need the alias for MyPy type hinting


@unique
class Rs485Parity(Enum):
    """
    The parity bit used for error correction. NONE disables parity
    """

    NONE = "n"
    EVEN = "e"
    ODD = "o"


_Rs485Parity = Rs485Parity


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


_WifiConnection = WifiConnection  # We need the alias for MyPy type hinting


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
        return f"{self.__outer_auth}, {self.__inner_auth}, {self.__cert_type})"

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


@unique
class EthernetConnection(Enum):
    """
    Configures the Ethernet Extension for either DHCP or a static ip.
    """

    DHCP = 0
    STATIC_IP = 1


_EthernetConnection = EthernetConnection  # We need the alias for MyPy type hinting


class PhyMode(Enum):
    """
    Configures the Wi-Fi mode of the Wi-Fi 2.0 Extension
    """

    WIFI_B = 0
    WIFI_G = 1
    WIFI_N = 2


_PhyMode = PhyMode  # We need the alias for MyPy type hinting


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


_WifiApEncryption = WifiApEncryption  # We need the alias for MyPy type hinting


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


class BrickMaster(DeviceWithMCU):  # pylint: disable=too-many-public-methods
    """
    Basis to build stacks and has 4 Bricklet ports
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_MASTER
    DEVICE_DISPLAY_NAME = "Master Brick"

    CallbackID = CallbackID
    FunctionID = FunctionID
    ExtensionPosition = ExtensionPosition
    ExtensionType = ExtensionType
    BrickletPort = Port
    ConnectionType = ConnectionType
    ChibiFrequency = ChibiFrequency
    Rs485Parity = Rs485Parity
    WifiConnection = WifiConnection
    EthernetConnection = EthernetConnection
    PhyMode = PhyMode
    WifiClientStatus = WifiClientStatus
    WifiApEncryption = WifiApEncryption
    WifiMeshStatus = WifiMeshStatus
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.STACK_CURRENT: "H",
        CallbackID.STACK_VOLTAGE: "H",
        CallbackID.USB_VOLTAGE: "H",
        CallbackID.STACK_CURRENT_REACHED: "H",
        CallbackID.STACK_VOLTAGE_REACHED: "H",
        CallbackID.USB_VOLTAGE_REACHED: "H",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.USB_VOLTAGE, CallbackID.USB_VOLTAGE_REACHED),
        1: (CallbackID.STACK_VOLTAGE, CallbackID.STACK_VOLTAGE_REACHED),
        2: (CallbackID.STACK_CURRENT, CallbackID.STACK_CURRENT_REACHED),
    }

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 4)

    async def get_stack_voltage(self) -> Decimal:
        """
        Returns the stack voltage in mV. The stack voltage is the
        voltage that is supplied via the stack, i.e. it is given by a
        Step-Down or Step-Up Power Supply.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_VOLTAGE, response_expected=True
        )
        return self.__sensor_to_si(unpack_payload(payload, "H"))

    async def get_stack_current(self) -> Decimal:
        """
        Returns the stack current in mA. The stack current is the
        current that is drawn via the stack, i.e. it is given by a
        Step-Down or Step-Up Power Supply.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_CURRENT, response_expected=True
        )
        return self.__sensor_to_si(unpack_payload(payload, "H"))

    async def set_extension_type(
        self, extension: _ExtensionPosition, exttype: _ExtensionType | int, response_expected: bool = True
    ) -> None:
        """
        Writes the extension type to the EEPROM of a specified extension.
        The extension is either 0 or 1 (0 is the on the bottom, 1 is the one on top,
        if only one extension is present use 0).

        Possible extension types:

        .. csv-table::
         :header: "Type", "Description"
         :widths: 10, 100

         "1",    "Chibi"
         "2",    "RS485"
         "3",    "Wi-Fi"
         "4",    "Ethernet"
         "5",    "Wi-Fi 2.0"

        The extension type is already set when bought, and it can be set with the
        Brick Viewer, it is unlikely that you need this function.
        """
        if not isinstance(extension, ExtensionPosition):
            extension = ExtensionPosition(extension)
        if not isinstance(exttype, ExtensionType):
            exttype = ExtensionType(exttype)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EXTENSION_TYPE,
            data=pack_payload((extension.value, exttype.value), "B I"),
            response_expected=response_expected,
        )

    async def get_extension_type(self, extension: int) -> _ExtensionType:
        """
        Returns the type for a given extension as set by :func:`Set Extension Type`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EXTENSION_TYPE,
            data=pack_payload((int(extension),), "B"),
            response_expected=True,
        )
        return ExtensionType(unpack_payload(payload, "I"))

    async def is_chibi_present(self) -> bool:
        """
        Returns *true* if a Chibi Extension is available to be used by the Master Brick.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_CHIBI_PRESENT, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_chibi_address(self, address: int, response_expected: bool = True) -> None:
        """
        Sets the address (1-255) belonging to the Chibi Extension.

        It is possible to set the address with the Brick Viewer and it will be
        saved in the EEPROM of the Chibi Extension, it does not
        have to be set on every startup.
        """
        assert 1 <= address <= 255

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_ADDRESS,
            data=pack_payload((int(address),), "B"),
            response_expected=response_expected,
        )

    async def get_chibi_address(self) -> int:
        """
        Returns the address as set by :func:`Set Chibi Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_ADDRESS, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_chibi_master_address(self, address: int, response_expected: bool = True) -> None:
        """
        Sets the address (1-255) of the Chibi Master. This address is used if the
        Chibi Extension is used as slave (i.e. it does not have a USB connection).

        It is possible to set the address with the Brick Viewer and it will be
        saved in the EEPROM of the Chibi Extension, it does not
        have to be set on every startup.
        """
        assert 1 <= address <= 255

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_MASTER_ADDRESS,
            data=pack_payload((int(address),), "B"),
            response_expected=response_expected,
        )

    async def get_chibi_master_address(self) -> int:
        """
        Returns the address as set by :func:`Set Chibi Master Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_MASTER_ADDRESS, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def __set_chibi_slave_address(self, num: int, address: int, response_expected: bool = True) -> None:
        """
        Sets up to 254 slave addresses. Valid addresses are in range 1-255. 0 has a
        special meaning, it is used as list terminator and not allowed as normal slave
        address. The address numeration (via ``num`` parameter) has to be used
        ascending from 0. For example: If you use the Chibi Extension in Master mode
        (i.e. the stack has an USB connection) and you want to talk to three other
        Chibi stacks with the slave addresses 17, 23, and 42, you should call with
        ``(0, 17)``, ``(1, 23)``, ``(2, 42)`` and ``(3, 0)``. The last call with
        ``(3, 0)`` is a list terminator and indicates that the Chibi slave address
        list contains 3 addresses in this case.

        It is possible to set the addresses with the Brick Viewer, that will take care
        of correct address numeration and list termination.

        The slave addresses will be saved in the EEPROM of the Chibi Extension, they
        don't have to be set on every startup.
        """
        assert 0 <= num <= 255
        assert 0 <= address <= 255

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_SLAVE_ADDRESS,
            data=pack_payload((int(num), int(address)), "B B"),
            response_expected=response_expected,
        )

    async def set_chibi_slave_addresses(
        self, addresses: tuple[int, ...] | list[int], response_expected: bool = True
    ) -> None:
        """
        Sets up to 254 slave addresses. Valid addresses are in range 1-255. For
        example: If you use the Chibi Extension in Master mode
        (i.e. the stack has an USB connection) and you want to talk to three other
        Chibi stacks with the slave addresses 17, 23, and 42, you should call this
        function with ``(17, 23, 42)``

        The slave addresses will be saved in the EEPROM of the Chibi Extension, they
        don't have to be set on every startup.
        """
        assert isinstance(addresses, (tuple, list))
        addresses = list(addresses)
        if addresses[-1] != 0:
            addresses += [
                0,
            ]  # add a trailing [0], because it is the delimiter
        assert len(addresses) <= 255

        coros = [
            self.__set_chibi_slave_address(index, address, response_expected) for index, address in enumerate(addresses)
        ]
        await asyncio.gather(*coros)

    async def __get_chibi_slave_address(self, num: int) -> int:
        """
        Returns the slave address for a given ``num`` as set by
        :func:`Set Chibi Slave Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHIBI_SLAVE_ADDRESS,
            data=pack_payload((int(num),), "B"),
            response_expected=True,
        )

        return unpack_payload(payload, "B")

    async def get_slave_addresses(self) -> tuple[int, ...]:
        """
        Returns the slave addresses as a tuple.
        """
        addresses = [await self.__get_chibi_slave_address(0)]
        index = 1
        while addresses[-1] != 0:
            addresses.append(await self.__get_chibi_slave_address(index))
            index += 1

        return tuple(addresses[:-1])

    async def get_chibi_signal_strength(self) -> int:
        """
        Returns the signal strength in dBm. The signal strength updates every time a
        packet is received.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_SIGNAL_STRENGTH, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def get_chibi_error_log(self) -> GetChibiErrorLog:
        """
        Returns underrun, CRC error, no ACK and overflow error counts of the Chibi
        communication. If these errors start rising, it is likely that either the
        distance between two Chibi stacks is becoming too big or there are
        interferences.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_ERROR_LOG, response_expected=True
        )
        return GetChibiErrorLog(*unpack_payload(payload, "H H H H"))

    async def set_chibi_frequency(self, frequency: _ChibiFrequency | int, response_expected: bool = True) -> None:
        """
        Sets the Chibi frequency range for the Chibi Extension. Possible values are:

        .. csv-table::
         :header: "Type", "Description"
         :widths: 10, 100

         "0",    "OQPSK 868MHz (Europe)"
         "1",    "OQPSK 915MHz (US)"
         "2",    "OQPSK 780MHz (China)"
         "3",    "BPSK40 915MHz"

        It is possible to set the frequency with the Brick Viewer, and it will be saved in the EEPROM of the Chibi
        Extension, it does not have to be set on every startup.
        """
        if not isinstance(frequency, ChibiFrequency):
            frequency = ChibiFrequency(frequency)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_FREQUENCY,
            data=pack_payload((frequency.value,), "B"),
            response_expected=response_expected,
        )

    async def get_chibi_frequency(self) -> _ChibiFrequency:
        """
        Returns the frequency value as set by :func:`Set Chibi Frequency`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_FREQUENCY, response_expected=True
        )
        return ChibiFrequency(unpack_payload(payload, "B"))

    async def set_chibi_channel(self, channel: int, response_expected: bool = True) -> None:
        """
        Sets the channel used by the Chibi Extension. Possible channels are
        different for different frequencies:

        .. csv-table::
         :header: "Frequency",             "Possible Channels"
         :widths: 40, 60

         "OQPSK 868MHz (Europe)", "0"
         "OQPSK 915MHz (US)",     "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"
         "OQPSK 780MHz (China)",  "0, 1, 2, 3"
         "BPSK40 915MHz",         "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"

        It is possible to set the channel with the Brick Viewer, and it will be saved in the EEPROM of the Chibi
        Extension, it does not have to be set on every startup.
        """
        # TODO: Add sanity checking of the channel
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHIBI_CHANNEL,
            data=pack_payload((int(channel),), "B"),
            response_expected=response_expected,
        )

    async def get_chibi_channel(self) -> int:
        """
        Returns the channel as set by :func:`Set Chibi Channel`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIBI_CHANNEL, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def is_rs485_present(self) -> bool:
        """
        Returns *true* if a RS485 Extension is available to be used by the Master Brick.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_RS485_PRESENT, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_rs485_address(self, address: int, response_expected: bool = True) -> None:
        """
        Sets the address (0-255) belonging to the RS485 Extension.

        Set to 0 if the RS485 Extension should be the RS485 Master (i.e. connected to a PC via USB).

        It is possible to set the address with the Brick Viewer, and it will be saved in the EEPROM of the RS485
        Extension, it does not have to be set on every startup.
        """
        assert 0 <= address <= 255

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RS485_ADDRESS,
            data=pack_payload((int(address),), "B"),
            response_expected=response_expected,
        )

    async def get_rs485_address(self) -> int:
        """
        Returns the address as set by :func:`Set RS485 Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RS485_ADDRESS, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def __set_rs485_slave_address(self, num: int, address: int, response_expected: bool = True) -> None:
        """
        Sets up to 255 slave addresses. Valid addresses are in range 1-255. 0 has a special meaning, it is used as list
        terminator and not allowed as normal slave address. The address numeration (via ``num`` parameter) has to be
        used ascending from 0. For example: If you use the RS485 Extension in Master mode (i.e. the stack has a USB
        connection) and you want to talk to three other RS485 stacks with the addresses 17, 23, and 42, you should call
         with ``(0, 17)``, ``(1, 23)``, ``(2, 42)`` and ``(3, 0)``. The last call with ``(3, 0)`` is a list terminator
         and indicates that the RS485 slave address list contains 3 addresses in this case.

        It is possible to set the addresses with the Brick Viewer, that will take care of correct address numeration and
        list termination.

        The slave addresses will be saved in the EEPROM of the Chibi Extension, they don't have to be set on every
        startup.
        """
        assert 0 <= num <= 255
        assert 0 <= address <= 255

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RS485_SLAVE_ADDRESS,
            data=pack_payload((int(num), int(address)), "B B"),
            response_expected=response_expected,
        )

    async def set_rs485_slave_addresses(self, addresses: Iterable[int], response_expected: bool = True) -> None:
        """
        Sets up to 255 slave addresses. Valid addresses are in range 1-255. For example: If you use the RS485 Extension
        in Master mode (i.e. the stack has a USB connection) and you want to talk to three other RS485 stacks with the
        addresses 17, 23, and 42, you should call the function with ``(17, 23, 42)``

        The slave addresses will be saved in the EEPROM of the Chibi Extension, they don't have to be set on every
        startup.
        """
        assert isinstance(addresses, (tuple, list))
        addresses = list(addresses)
        if addresses[-1] != 0:
            addresses += [
                0,
            ]  # add a trailing [0], because it is the delimiter
        assert len(addresses) < 255

        coros = [
            self.__set_rs485_slave_address(index, address, response_expected) for index, address in enumerate(addresses)
        ]
        await asyncio.gather(*coros)

    async def __get_rs485_slave_address(self, num: int) -> int:
        """
        Returns the slave address for a given ``num`` as set by
        :func:`Set RS485 Slave Address`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RS485_SLAVE_ADDRESS,
            data=pack_payload((int(num),), "B"),
            response_expected=True,
        )

        return unpack_payload(payload, "B")

    async def get_rs485_slave_addresses(self) -> tuple[int, ...]:
        """
        Returns the slave addresses as a tuple.
        """
        addresses = [await self.__get_rs485_slave_address(0)]
        index = 1
        while addresses[-1] != 0:
            addresses.append(await self.__get_rs485_slave_address(index))
            index += 1
        return tuple(addresses[:-1])  # strip the trailing [0], because it is the delimiter

    async def get_rs485_error_log(self) -> int:
        """
        Returns CRC error counts of the RS485 communication.
        If this counter starts rising, it is likely that the distance
        between the RS485 nodes is too big or there is some kind of
        interference.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RS485_ERROR_LOG, response_expected=True
        )

        return unpack_payload(payload, "H")

    async def set_rs485_configuration(
        self, speed: int, parity: _Rs485Parity, stopbits: int, response_expected: bool = True
    ) -> None:
        """
        Sets the configuration of the RS485 Extension. Speed is given in baud. The
        Master Brick will try to match the given baud rate as exactly as possible.
        The maximum recommended baud rate is 2000000 (2Mbit/s).
        Possible values for parity are 'n' (none), 'e' (even) and 'o' (odd).
        Possible values for stop bits are 1 and 2.

        If your RS485 is unstable (lost messages etc.), the first thing you should
        try is to decrease the speed. On very large bus (e.g. 1km), you probably
        should use a value in the range of 100000 (100kbit/s).

        The values are stored in the EEPROM and only applied on startup. That means
        you have to restart the Master Brick after configuration.
        """
        assert stopbits in (1, 2)
        if not isinstance(parity, Rs485Parity):
            parity = Rs485Parity(parity)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RS485_CONFIGURATION,
            data=pack_payload((int(speed), parity.value, int(stopbits)), "I c B"),
            response_expected=response_expected,
        )

    async def get_rs485_configuration(self) -> GetRS485Configuration:
        """
        Returns the configuration as set by :func:`Set RS485 Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RS485_CONFIGURATION, response_expected=True
        )
        speed, parity, stopbits = unpack_payload(payload, "I c B")

        return GetRS485Configuration(speed, Rs485Parity(parity), stopbits)

    async def is_wifi_present(self) -> bool:
        """
        Returns *true* if a Wi-Fi Extension is available to be used by the Master Brick.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_WIFI_PRESENT, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_wifi_configuration(  # pylint: disable=too-many-arguments
        self,
        ssid: str | bytes,
        connection: _WifiConnection | int,
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
        assert isinstance(ip_address, (tuple, list)) and len(ip_address) == 4
        assert isinstance(subnet_mask, (tuple, list)) and len(subnet_mask) == 4
        assert isinstance(gateway, (tuple, list)) and len(gateway) == 4
        assert 1 <= port <= 65535
        if not isinstance(ssid, bytes):
            ssid = ssid.encode("utf-8")
        assert len(ssid) <= 32

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

    async def set_wifi_encryption(  # pylint: disable=too-many-arguments
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
            EapOptions(eap_options)
        if not isinstance(encryption, WifiEncryptionMode):
            encryption = WifiEncryptionMode(encryption)
        assert 1 <= key_index <= 4
        assert isinstance(eap_options, EapOptions)  # This is always true and only done for the typechecker

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
        assert len(username) <= 32

        data = list(username) + [0] * (32 - len(username))  # pad with null bytes

        return await self.set_wifi_certificate(0xFFFF, data, len(data), response_expected)

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
        assert len(password) <= 32

        data = list(password) + [0] * (32 - len(password))  # pad with null bytes

        return await self.set_wifi_certificate(0xFFFE, data, len(data), response_expected)

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

    async def get_usb_voltage(self) -> Decimal:
        """
        Returns the USB voltage in mV. Does not work with hardware version 2.1.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_USB_VOLTAGE, response_expected=True
        )

        return self.__sensor_to_si(unpack_payload(payload, "H"))

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
        assert 8 <= len(key) <= 63

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_LONG_WIFI_KEY,
            data=pack_payload((key,), "64s"),
            response_expected=response_expected,
        )

    async def get_long_wifi_key(self) -> bytes:
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
        # The bricks only allow 32 characters as opposed to 63 as per RFC.
        # Allow 0 characters to reset the hostname (this is TF specific)
        hostname = hostname.lower()
        if len(hostname) != 0:
            allowed = re.compile(rb"^(?!-)[a-z0-9-]{2,32}(?<!-)$")
            if not bool(allowed.match(hostname)):
                raise ValueError("Invalid hostname")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_HOSTNAME,
            data=pack_payload((hostname,), "16s"),
            response_expected=response_expected,
        )

    async def get_wifi_hostname(self) -> bytes:
        """
        Returns the hostname as set by :func:`Set Wifi Hostname`.

        An empty String means, that the default hostname is used.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_HOSTNAME, response_expected=True
        )

        return unpack_payload(payload, "16s")

    async def set_stack_current_callback_period(self, period: int, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the :cb:`Stack Current` callback is triggered periodically. A value of 0 turns
        the callback off.

        The :cb:`Stack Current` callback is only triggered if the current has changed since the last triggering.

        The default value is 0.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STACK_CURRENT_CALLBACK_PERIOD,
            data=pack_payload((int(period),), "I"),
            response_expected=response_expected,
        )

    async def get_stack_current_callback_period(self) -> int:
        """
        Returns the period as set by :func:`Set Stack Current Callback Period`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_CURRENT_CALLBACK_PERIOD, response_expected=True
        )

        return unpack_payload(payload, "I")

    async def set_stack_voltage_callback_period(self, period: int, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the :cb:`Stack Voltage` callback is triggered periodically. A value of 0 turns
        the callback off.

        The :cb:`Stack Voltage` callback is only triggered if the voltage has changed
        since the last triggering.

        The default value is 0.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STACK_VOLTAGE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), "I"),
            response_expected=response_expected,
        )

    async def get_stack_voltage_callback_period(self) -> int:
        """
        Returns the period as set by :func:`Set Stack Voltage Callback Period`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_VOLTAGE_CALLBACK_PERIOD, response_expected=True
        )

        return unpack_payload(payload, "I")

    async def set_usb_voltage_callback_period(self, period: int, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the :cb:`USB Voltage` callback is triggered periodically. A value of 0 turns
        the callback off.

        The :cb:`USB Voltage` callback is only triggered if the voltage has changed since the last triggering.

        The default value is 0.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_USB_VOLTAGE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), "I"),
            response_expected=response_expected,
        )

    async def get_usb_voltage_callback_period(self) -> int:
        """
        Returns the period as set by :func:`Set USB Voltage Callback Period`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_USB_VOLTAGE_CALLBACK_PERIOD, response_expected=True
        )

        return unpack_payload(payload, "I")

    async def set_stack_current_callback_threshold(
        self,
        option: Threshold | int,
        minimum: float | Decimal,
        maximum: float | Decimal,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Stack Current Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the current is *outside* the min and max values"
         "'i'",    "Callback is triggered when the current is *inside* the min and max values"
         "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STACK_CURRENT_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value,
                    self.__si_to_sensor(minimum),
                    self.__si_to_sensor(maximum),
                ),
                "c H H",
            ),
            response_expected=response_expected,
        )

    async def get_stack_current_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Stack Current Callback Threshold`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_CURRENT_CALLBACK_THRESHOLD, response_expected=True
        )

        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(
            Threshold(option),
            Decimal(minimum) / 1000,
            Decimal(maximum) / 1000,
        )

    async def set_stack_voltage_callback_threshold(
        self,
        option: Threshold | int,
        minimum: float | Decimal,
        maximum: float | Decimal,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Stack Voltage Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
         "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
         "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STACK_VOLTAGE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value,
                    self.__si_to_sensor(minimum),
                    self.__si_to_sensor(maximum),
                ),
                "c H H",
            ),
            response_expected=response_expected,
        )

    async def get_stack_voltage_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Stack Voltage Callback Threshold`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_VOLTAGE_CALLBACK_THRESHOLD, response_expected=True
        )

        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(
            Threshold(option),
            Decimal(minimum) / 1000,
            Decimal(maximum) / 1000,
        )

    async def set_usb_voltage_callback_threshold(
        self,
        option: Threshold | int,
        minimum: float | Decimal,
        maximum: float | Decimal,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`USB Voltage Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
         "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
         "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_USB_VOLTAGE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value,
                    self.__si_to_sensor(minimum),
                    self.__si_to_sensor(maximum),
                ),
                "c H H",
            ),
            response_expected=response_expected,
        )

    async def get_usb_voltage_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set USB Voltage Callback Threshold`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_USB_VOLTAGE_CALLBACK_THRESHOLD, response_expected=True
        )

        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(
            Threshold(option),
            Decimal(minimum) / 1000,
            Decimal(maximum) / 1000,
        )

    async def set_debounce_period(self, debounce: int = 100, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the threshold callbacks

        * :cb:`Stack Current Reached`,
        * :cb:`Stack Voltage Reached`,
        * :cb:`USB Voltage Reached`

        are triggered, if the thresholds

        * :func:`Set Stack Current Callback Threshold`,
        * :func:`Set Stack Voltage Callback Threshold`,
        * :func:`Set USB Voltage Callback Threshold`

        keep being reached.

        The default value is 100.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((int(debounce),), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> int:
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )

        return unpack_payload(payload, "I")

    async def is_ethernet_present(self) -> bool:
        """
        Returns *true* if a Ethernet Extension is available to be used by the Master
        Brick.

        .. versionadded:: 2.1.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_ETHERNET_PRESENT, response_expected=True
        )

        return unpack_payload(payload, "!")

    async def set_ethernet_configuration(  # pylint: disable=too-many-arguments
        self,
        connection: _EthernetConnection,
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
        assert isinstance(ip_address, (tuple, list)) and len(ip_address) == 4
        assert isinstance(subnet_mask, (tuple, list)) and len(subnet_mask) == 4
        assert isinstance(gateway, (tuple, list)) and len(gateway) == 4
        assert 1 <= port <= 65535

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

    async def set_ethernet_hostname(self, hostname: bytes | str, response_expected: bool = True):
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
        assert isinstance(mac_address, (tuple, list)) and len(mac_address) == 6

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
        assert 0 <= sockets <= 7
        assert 1 <= port <= 65535

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
        assert len(secret) <= 64

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ETHERNET_AUTHENTICATION_SECRET,
            data=pack_payload((secret,), "64s"),
            response_expected=response_expected,
        )

    async def get_ethernet_authentication_secret(self) -> bytes:
        """
        Returns the authentication secret as set by
        :func:`Set Ethernet Authentication Secret`.

        .. versionadded:: 2.2.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ETHERNET_AUTHENTICATION_SECRET, response_expected=True
        )

        return unpack_payload(payload, "64s")

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
        assert len(secret) <= 64

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIFI_AUTHENTICATION_SECRET,
            data=pack_payload((secret,), "64s"),
            response_expected=response_expected,
        )

    async def get_wifi_authentication_secret(self) -> bytes:
        """
        Returns the authentication secret as set by
        :func:`Set Wifi Authentication Secret`.

        .. versionadded:: 2.2.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WIFI_AUTHENTICATION_SECRET, response_expected=True
        )

        return unpack_payload(payload, "64s")

    async def get_connection_type(self) -> _ConnectionType:
        """
        Returns the type of the connection over which this function was called.

        .. versionadded:: 2.4.0$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONNECTION_TYPE, response_expected=True
        )

        return ConnectionType(unpack_payload(payload, "B"))

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

        data = bytearray(data)
        assert len(data) <= 60

        length = len(data)

        data.extend([0] * (60 - length))  # always send 60 bytes

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
        assert 0 <= length <= 60

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
        assert len(secret) <= 64

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

    async def set_wifi2_configuration(  # pylint: disable=too-many-arguments
        self,
        port: int = 4223,
        websocket_port: int = 4280,
        website_port: int = 80,
        phy_mode: _PhyMode = PhyMode.WIFI_G,
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
        assert 1 <= port <= 65535
        assert 1 <= websocket_port <= 65535
        assert 1 <= website_port <= 65535
        assert 0 <= sleep_mode <= 255
        assert 0 <= int(website) <= 255
        if not isinstance(phy_mode, PhyMode):
            phy_mode = PhyMode(PhyMode)

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

    async def set_wifi2_client_configuration(  # pylint: disable=too-many-arguments
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
        assert isinstance(ip_address, (tuple, list)) and len(ip_address) == 4
        assert isinstance(subnet_mask, (tuple, list)) and len(subnet_mask) == 4
        assert isinstance(gateway, (tuple, list)) and len(gateway) == 4
        assert isinstance(mac_address, (tuple, list)) and len(mac_address) == 6
        assert isinstance(bssid, (tuple, list)) and len(bssid) == 6

        if not isinstance(ssid, bytes):
            ssid = ssid.encode("utf-8")
        assert len(ssid) <= 32

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
        assert 8 <= len(password) <= 63

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

    async def set_wifi2_ap_configuration(  # pylint: disable=too-many-arguments
        self,
        enable: bool = True,
        ssid: bytes | str = "WIFI Extension 2.0 Access Point",
        ip_address: tuple[int, int, int, int] = (0, 0, 0, 0),
        subnet_mask: tuple[int, int, int, int] = (0, 0, 0, 0),
        gateway: tuple[int, int, int, int] = (0, 0, 0, 0),
        encryption: _WifiApEncryption = WifiApEncryption.WPA2_PSK,
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
        assert isinstance(ip_address, (tuple, list)) and len(ip_address) == 4
        assert isinstance(subnet_mask, (tuple, list)) and len(subnet_mask) == 4
        assert isinstance(gateway, (tuple, list)) and len(gateway) == 4
        assert isinstance(mac_address, (tuple, list)) and len(mac_address) == 6
        if not isinstance(encryption, WifiApEncryption):
            encryption = WifiApEncryption(encryption)
        assert 1 <= channel <= 13
        if not isinstance(ssid, bytes):
            ssid = ssid.encode("utf-8")
        assert len(ssid) <= 32

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
        assert 8 <= len(password) <= 63

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

    async def set_wifi2_mesh_configuration(  # pylint: disable=too-many-arguments
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
        assert isinstance(root_ip, (tuple, list)) and len(root_ip) == 4
        assert isinstance(root_subnet_mask, (tuple, list)) and len(root_subnet_mask) == 4
        assert isinstance(root_gateway, (tuple, list)) and len(root_gateway) == 4
        assert isinstance(gateway_ip, (tuple, list)) and len(gateway_ip) == 4
        assert isinstance(root_gateway, (tuple, list)) and len(root_gateway) == 4
        assert isinstance(router_bssid, (tuple, list)) and len(router_bssid) == 6
        assert isinstance(group_id, (tuple, list)) and len(group_id) == 6
        assert 1 <= gateway_port <= 65535
        if not isinstance(group_ssid_prefix, bytes):
            group_ssid_prefix = group_ssid_prefix.encode("utf-8")
        assert len(group_ssid_prefix) <= 16

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
        assert len(ssid) <= 32

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
        assert 8 <= len(password) <= 63

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

    async def set_spitfp_baudrate_config(
        self,
        enable_dynamic_baudrate: bool = True,
        minimum_dynamic_baudrate: int = 400000,
        response_expected: bool = True,
    ) -> None:
        """
        The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is
        enabled, the Brick will try to adapt the baudrate for the communication
        between Bricks and Bricklets according to the amount of data that is transferred.

        The baudrate will be increased exponentially if lots of data is sent/received and
        decreased linearly if little data is sent/received.

        This lowers the baudrate in applications where little data is transferred (e.g.
        a weather station) and increases the robustness. If there is lots of data to transfer
        (e.g. Thermal Imaging Bricklet) it automatically increases the baudrate as needed.

        In cases where some data has to transferred as fast as possible every few seconds
        (e.g. RS485 Bricklet with a high baudrate but small payload) you may want to turn
        the dynamic baudrate off to get the highest possible performance.

        The maximum value of the baudrate can be set per port with the function
        :func:`Set SPITFP Baudrate`. If the dynamic baudrate is disabled, the baudrate
        as set by :func:`Set SPITFP Baudrate` will be used statically.

        The minimum dynamic baudrate has a value range of 400000 to 2000000 baud.

        By default, dynamic baudrate is enabled and the minimum dynamic baudrate is 400000.

        .. versionadded:: 2.4.6$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
            data=pack_payload((bool(enable_dynamic_baudrate), int(minimum_dynamic_baudrate)), "! I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate_config(self) -> GetSPITFPBaudrateConfig:
        """
        Returns the baudrate config, see :func:`Set SPITFP Baudrate Config`.

        .. versionadded:: 2.4.6$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPITFP_BAUDRATE_CONFIG, response_expected=True
        )
        return GetSPITFPBaudrateConfig(*unpack_payload(payload, "! I"))

    async def get_send_timeout_count(self, communication_method: _ConnectionType | int) -> int:
        """
        Returns the timeout count for the different communication methods.

        The methods 0-2 are available for all Bricks, 3-7 only for Master Bricks.

        This function is mostly used for debugging during development, in normal operation
        the counters should nearly always stay at 0.

        .. versionadded:: 2.4.3$nbsp;(Firmware)
        """
        if not isinstance(communication_method, ConnectionType):
            communication_method = ConnectionType(communication_method)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SEND_TIMEOUT_COUNT,
            data=pack_payload((communication_method.value,), "B"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def set_spitfp_baudrate(
        self, bricklet_port: Port, baudrate: int = 1400000, response_expected: bool = True
    ) -> None:
        """
        Sets the baudrate for a specific Bricklet port ('a' - 'd'). The
        baudrate can be in the range 400000 to 2000000.

        If you want to increase the throughput of Bricklets you can increase
        the baudrate. If you get a high error count because of high
        interference (see :func:`Get SPITFP Error Count`) you can decrease the
        baudrate.

        If the dynamic baudrate feature is enabled, the baudrate set by this
        function corresponds to the maximum baudrate (see :func:`Set SPITFP Baudrate Config`).

        Regulatory testing is done with the default baudrate. If CE compatability
        or similar is necessary in you applications we recommend to not change
        the baudrate.

        The default baudrate for all ports is 1400000.

        .. versionadded:: 2.4.3$nbsp;(Firmware)
        """
        if not isinstance(bricklet_port, Port):
            bricklet_port = Port(bricklet_port)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE,
            data=pack_payload((bricklet_port.value.encode(), int(baudrate)), "c I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate(self, bricklet_port: Port) -> int:
        """
        Returns the baudrate for a given Bricklet port, see :func:`Set SPITFP Baudrate`.

        .. versionadded:: 2.4.3$nbsp;(Firmware)
        """
        if not isinstance(bricklet_port, Port):
            bricklet_port = Port(bricklet_port)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_BAUDRATE,
            data=pack_payload((bricklet_port.value.encode(),), "c"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def get_spitfp_error_count(self, bricklet_port: Port) -> GetSPITFPErrorCount:
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ACK checksum errors,
        * message checksum errors,
        * framing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Brick side. All
        Bricklets have a similar function that returns the errors on the Bricklet side.

        .. versionadded:: 2.4.3$nbsp;(Firmware)
        """
        # TODO: Are these values reset after some time? I see varying error rates
        if not isinstance(bricklet_port, Port):
            bricklet_port = Port(bricklet_port)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_ERROR_COUNT,
            data=pack_payload((bricklet_port.value.encode(),), "c"),
            response_expected=True,
        )
        return GetSPITFPErrorCount(*unpack_payload(payload, "I I I I"))

    async def enable_status_led(self, response_expected: bool = True) -> None:
        """
        Enables the status LED.

        The status LED is the blue LED next to the USB connector. If enabled is is
        on and it flickers if data is transfered. If disabled it is always off.

        The default state is enabled.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_STATUS_LED, response_expected=response_expected
        )

    async def disable_status_led(self, response_expected: bool = True) -> None:
        """
        Disables the status LED.

        The status LED is the blue LED next to the USB connector. If enabled is is
        on and it flickers if data is transfered. If disabled it is always off.

        The default state is enabled.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_STATUS_LED, response_expected=response_expected
        )

    async def is_status_led_enabled(self) -> bool:
        """
        Returns *true* if the status LED is enabled, *false* otherwise.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_STATUS_LED_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def get_protocol1_bricklet_name(self, bricklet_port: Port) -> GetProtocol1BrickletName:
        """
        Returns the firmware and protocol version and the name of the Bricklet for a
        given port.

        This functions sole purpose is to allow automatic flashing of v1.x.y Bricklet
        plugins.
        """
        if not isinstance(bricklet_port, Port):
            bricklet_port = Port(bricklet_port)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROTOCOL1_BRICKLET_NAME,
            data=pack_payload((bricklet_port.value.encode(),), "c"),
            response_expected=True,
        )
        return GetProtocol1BrickletName(*unpack_payload(payload, "B 3B 40s"))

    async def get_chip_temperature(self) -> Decimal:
        """
        Returns the temperature in K as measured inside the microcontroller. The value returned is not the ambient
        temperature!

        The temperature is only proportional to the real temperature, and it has an accuracy of +-15%. Practically it is
        only useful as an indicator for temperature changes.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIP_TEMPERATURE, response_expected=True
        )
        result = unpack_payload(payload, "h")
        return Decimal(result) / 10 + Decimal("273.15")

    # pylint: disable=duplicate-code
    @staticmethod
    def __sensor_to_si(value: int) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 1000

    @staticmethod
    def __si_to_sensor(value: Decimal | float) -> int:
        """
        Convert to the sensor value to SI units
        """
        return int(value * 1000)

    async def read_events(
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        registered_events = set()
        if events:
            for event in events:
                registered_events.add(self.CallbackID(event))
        if sids is not None:
            for sid in sids:
                for callback in self.SID_TO_CALLBACK.get(sid, []):
                    registered_events.add(callback)

        if events is None and sids is None:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                if function_id in (CallbackID.USB_VOLTAGE, CallbackID.USB_VOLTAGE_REACHED):
                    yield Event(self, 0, function_id, self.__sensor_to_si(value))
                elif function_id in (CallbackID.STACK_VOLTAGE, CallbackID.STACK_VOLTAGE_REACHED):
                    yield Event(self, 1, function_id, self.__sensor_to_si(value))
                else:
                    yield Event(self, 2, function_id, self.__sensor_to_si(value))
