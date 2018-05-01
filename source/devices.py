# -*- coding: utf-8 -*-
from enum import IntEnum, unique

@unique
class DeviceIdentifier(IntEnum):
    BrickMaster = 13
    BrickletAmbientLight = 21
    BrickletHumidity = 27
    BrickletTemperature = 216
    
