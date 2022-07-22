"""
The device factory which allows to create instances of Bricks and Bricklets from
their device id
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from .brick_master import BrickMaster
from .bricklet_ambient_light_v2 import BrickletAmbientLightV2
from .bricklet_ambient_light_v3 import BrickletAmbientLightV3
from .bricklet_analog_in import BrickletAnalogIn
from .bricklet_barometer import BrickletBarometer
from .bricklet_barometer_v2 import BrickletBarometerV2
from .bricklet_humidity import BrickletHumidity
from .bricklet_humidity_v2 import BrickletHumidityV2
from .bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2
from .bricklet_industrial_ptc import BrickletIndustrialPtc
from .bricklet_io4_v2 import BrickletIO4V2
from .bricklet_io16 import BrickletIO16
from .bricklet_moisture import BrickletMoisture
from .bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from .bricklet_ptc import BrickletPtc
from .bricklet_ptc_v2 import BrickletPtcV2
from .bricklet_rs232_v2 import BrickletRS232V2
from .bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
from .bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
from .bricklet_temperature import BrickletTemperature
from .bricklet_temperature_v2 import BrickletTemperatureV2

if TYPE_CHECKING:
    from . import IPConnectionAsync
    from .devices import Device, DeviceIdentifier


class DeviceFactory:
    """
    The factory. Do not import this, as it is instantiated below to create a
    class object.
    """

    def __init__(self):
        self.__available_devices = {}

    def register(self, device):
        """
        Register a new Brick or Bricklet with the factory
        """
        self.__available_devices[device.DEVICE_IDENTIFIER] = device

    def get(self, ipcon: IPConnectionAsync, device_id: DeviceIdentifier, uid: int, *_args, **_kwargs) -> Device:
        """
        Create a new instance of a Brick or Bricklet from its device id
        """
        try:
            return self.__available_devices[device_id](uid, ipcon)
        except KeyError:
            raise ValueError(f"No device available for id {device_id}") from None


device_factory = DeviceFactory()

device_factory.register(BrickMaster)
device_factory.register(BrickletAmbientLightV2)
device_factory.register(BrickletAmbientLightV3)
device_factory.register(BrickletAnalogIn)
device_factory.register(BrickletBarometer)
device_factory.register(BrickletBarometerV2)
device_factory.register(BrickletHumidity)
device_factory.register(BrickletHumidityV2)
device_factory.register(BrickletIndustrialDualAnalogInV2)
device_factory.register(BrickletIndustrialPtc)
device_factory.register(BrickletIO16)
device_factory.register(BrickletIO4V2)
device_factory.register(BrickletMoisture)
device_factory.register(BrickletMotionDetectorV2)
device_factory.register(BrickletPtc)
device_factory.register(BrickletPtcV2)
device_factory.register(BrickletSegmentDisplay4x7)
device_factory.register(BrickletSegmentDisplay4x7V2)
device_factory.register(BrickletRS232V2)
device_factory.register(BrickletTemperature)
device_factory.register(BrickletTemperatureV2)
