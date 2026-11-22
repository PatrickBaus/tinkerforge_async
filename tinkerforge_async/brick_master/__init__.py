"""
Module for the Tinkerforge Master Brick (https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html)
implemented using Python AsyncIO. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.

The module is a package, so there is one module for each extension of the Master Brick. All names that were defined in
the former module `brick_master` can still be imported from this package.
"""

from .chibi import ChibiFrequency, GetChibiErrorLog
from .common import ConnectionType, FunctionID
from .ethernet import (
    EthernetConnection,
    GetEthernetConfiguration,
    GetEthernetStatus,
    GetEthernetWebsocketConfiguration,
    PhyMode,
)
from .master import (
    BrickMaster,
    CallbackID,
    ExtensionPosition,
    ExtensionType,
    GetProtocol1BrickletName,
    SetBrickletXMCFlashConfig,
)
from .rs485 import GetRS485Configuration, Rs485Parity
from .wifi import (
    EapOptions,
    GetWifiBufferInfo,
    GetWifiCertificate,
    GetWifiConfiguration,
    GetWifiEncryption,
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
from .wifi2 import (
    GetWifi2APConfiguration,
    GetWifi2ClientConfiguration,
    GetWifi2Configuration,
    GetWifi2MeshAPStatus,
    GetWifi2MeshClientStatus,
    GetWifi2MeshCommonStatus,
    GetWifi2MeshConfiguration,
    GetWifi2Status,
    ReadWifi2SerialPort,
    Wifi2BootloaderError,
    WifiApEncryption,
    WifiClientStatus,
    WifiMeshStatus,
)

__all__ = [
    "BrickMaster",
    "CallbackID",
    "ChibiFrequency",
    "ConnectionType",
    "EapOptions",
    "EthernetConnection",
    "ExtensionPosition",
    "ExtensionType",
    "FunctionID",
    "GetChibiErrorLog",
    "GetEthernetConfiguration",
    "GetEthernetStatus",
    "GetEthernetWebsocketConfiguration",
    "GetProtocol1BrickletName",
    "SetBrickletXMCFlashConfig",
    "GetRS485Configuration",
    "GetWifi2APConfiguration",
    "GetWifi2ClientConfiguration",
    "GetWifi2Configuration",
    "GetWifi2MeshAPStatus",
    "GetWifi2MeshClientStatus",
    "GetWifi2MeshCommonStatus",
    "GetWifi2MeshConfiguration",
    "GetWifi2Status",
    "GetWifiBufferInfo",
    "GetWifiCertificate",
    "GetWifiConfiguration",
    "GetWifiEncryption",
    "GetWifiStatus",
    "PhyMode",
    "ReadWifi2SerialPort",
    "Rs485Parity",
    "Wifi2BootloaderError",
    "WifiApEncryption",
    "WifiClientStatus",
    "WifiConnection",
    "WifiDomain",
    "WifiEapCertType",
    "WifiEapInnerAuth",
    "WifiEapOuterAuth",
    "WifiEncryptionMode",
    "WifiMeshStatus",
    "WifiPowerMode",
    "WifiState",
]
