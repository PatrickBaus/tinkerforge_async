"""Tests for the package `tinkerforge_async.brick_master`, which was split into one module per extension."""

# pylint: disable=duplicate-code

import importlib
import inspect
import pkgutil

import pytest

from tinkerforge_async import brick_master
from tinkerforge_async.brick_master import BrickMaster

# Everything that could be imported from the module before it was split into a package
FORMER_NAMES = (
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
)

EXTENSION_BASES = {
    "ChibiExtension": "chibi",
    "Rs485Extension": "rs485",
    "WifiExtension": "wifi",
    "EthernetExtension": "ethernet",
    "Wifi2Extension": "wifi2",
    "MasterConnection": "common",
}


@pytest.mark.parametrize("name", FORMER_NAMES)
def test_former_names_are_still_importable(name):
    """All classes, enums and named tuples of the former module can be imported from the package."""
    assert hasattr(brick_master, name)
    assert name in brick_master.__all__


def test_all_lists_exactly_the_public_names_of_the_modules():
    """__all__ contains the classes of all modules, except for the extensions, which are mixins of the BrickMaster."""
    defined = set()
    for module_info in pkgutil.iter_modules(brick_master.__path__):
        module = importlib.import_module(f"{brick_master.__name__}.{module_info.name}")
        for name, obj in vars(module).items():
            if inspect.isclass(obj) and obj.__module__ == module.__name__ and name not in EXTENSION_BASES:
                defined.add(name)
                assert getattr(brick_master, name) is obj
    assert defined == set(brick_master.__all__)


@pytest.mark.parametrize("name,module_name", EXTENSION_BASES.items())
def test_functions_of_the_extensions_are_inherited_by_the_master_brick(name, module_name):
    """The BrickMaster inherits the functions of each extension from its own module."""
    extension = getattr(importlib.import_module(f"{brick_master.__name__}.{module_name}"), name)
    assert issubclass(BrickMaster, extension)
    functions = [f for f, obj in vars(extension).items() if inspect.iscoroutinefunction(obj) and not f.startswith("_")]
    assert functions
    for function in functions:
        assert getattr(BrickMaster, function).__qualname__.startswith(f"{name}.")


def test_the_enums_are_available_as_attributes_of_the_master_brick():
    """The enums that are used as arguments of the functions are also available as attributes of the BrickMaster."""
    for name in ("ChibiFrequency", "Rs485Parity", "WifiConnection", "EthernetConnection", "PhyMode", "ConnectionType"):
        assert getattr(BrickMaster, name) is getattr(brick_master, name)
