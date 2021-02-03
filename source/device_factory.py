# -*- coding: utf-8 -*-

from .brick_master import BrickMaster
from .bricklet_ambient_light_v2 import BrickletAmbientLightV2
from .bricklet_ambient_light_v3 import BrickletAmbientLightV3
from .bricklet_analog_in import BrickletAnalogIn
from .bricklet_barometer import BrickletBarometer
from .bricklet_humidity import BrickletHumidity
from .bricklet_humidity_v2 import BrickletHumidityV2
from .bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2
from .bricklet_io16 import BrickletIO16
from .bricklet_moisture import BrickletMoisture
from .bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from .bricklet_ptc import BrickletPtc
from .bricklet_ptc_v2 import BrickletPtcV2
from .bricklet_temperature import BrickletTemperature
from .bricklet_temperature_v2 import BrickletTemperatureV2
from .bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
from .bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2

class DeviceFactory:
    def __init__(self):
        self.__available_devices= {}

    def register(self, device):
        self.__available_devices[device.DEVICE_IDENTIFIER] = device

    def get(self, device_id, uid, ipcon):
        device = self.__available_devices.get(device_id)
        if device is None:
            raise ValueError(f"No device available for id {device_id}")
        return device(uid, ipcon)

device_factory = DeviceFactory()

device_factory.register(BrickMaster)
device_factory.register(BrickletAmbientLightV2)
device_factory.register(BrickletAmbientLightV3)
device_factory.register(BrickletAnalogIn)
device_factory.register(BrickletBarometer)
device_factory.register(BrickletHumidity)
device_factory.register(BrickletHumidityV2)
device_factory.register(BrickletIndustrialDualAnalogInV2)
device_factory.register(BrickletIO16)
device_factory.register(BrickletMoisture)
device_factory.register(BrickletMotionDetectorV2)
device_factory.register(BrickletPtc)
device_factory.register(BrickletPtcV2)
device_factory.register(BrickletSegmentDisplay4x7)
device_factory.register(BrickletSegmentDisplay4x7V2)
device_factory.register(BrickletTemperature)
device_factory.register(BrickletTemperatureV2)
