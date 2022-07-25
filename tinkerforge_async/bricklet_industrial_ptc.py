"""
Module for the Tinkerforge Industrial PTC Bricklet
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_PTC.html)
implemented using Python asyncIO. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""
from .bricklet_ptc_v2 import BrickletPtcV2
from .devices import DeviceIdentifier


class BrickletIndustrialPtc(BrickletPtcV2):
    """
    Reads temperatures from Pt100 und Pt1000 sensors
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_INDUSTRIAL_PTC
    DEVICE_DISPLAY_NAME = "Industrial PTC Bricklet"
