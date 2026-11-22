"""
Module for the Tinkerforge ESP32 Ethernet Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/ESP32Ethernet_Brick_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, TypeAlias

from .devices import Device, DeviceIdentifier, _FunctionID

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this brick
    """


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """


class BrickESP32Ethernet(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    ESP32 microcontroller based Brick with Ethernet and 6 Bricklet ports
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_ESP32_ETHERNET
    DEVICE_DISPLAY_NAME = "ESP32 Ethernet Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {}

    SID_TO_CALLBACK = {}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
