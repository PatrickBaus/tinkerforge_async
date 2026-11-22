"""
The device factory which allows to create instances of Bricks and Bricklets from
their device id
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .brick_esp32 import BrickESP32
from .brick_esp32_ethernet import BrickESP32Ethernet
from .brick_hat import BrickHAT
from .brick_hat_zero import BrickHATZero
from .brick_imu_v2 import BrickIMUV2
from .brick_master import BrickMaster
from .brick_red import BrickRED
from .brick_silent_stepper import BrickSilentStepper
from .bricklet_accelerometer_v2 import BrickletAccelerometerV2
from .bricklet_air_quality import BrickletAirQuality
from .bricklet_ambient_light_v2 import BrickletAmbientLightV2
from .bricklet_ambient_light_v3 import BrickletAmbientLightV3
from .bricklet_analog_in import BrickletAnalogIn
from .bricklet_analog_in_v3 import BrickletAnalogInV3
from .bricklet_analog_out_v3 import BrickletAnalogOutV3
from .bricklet_barometer import BrickletBarometer
from .bricklet_barometer_v2 import BrickletBarometerV2
from .bricklet_can import BrickletCAN
from .bricklet_can_v2 import BrickletCANV2
from .bricklet_co2_v2 import BrickletCO2V2
from .bricklet_color import BrickletColor
from .bricklet_color_v2 import BrickletColorV2
from .bricklet_compass import BrickletCompass
from .bricklet_dc_v2 import BrickletDCV2
from .bricklet_distance_ir import BrickletDistanceIR
from .bricklet_distance_ir_v2 import BrickletDistanceIRV2
from .bricklet_distance_us_v2 import BrickletDistanceUSV2
from .bricklet_dmx import BrickletDMX
from .bricklet_dual_button_v2 import BrickletDualButtonV2
from .bricklet_dust_detector import BrickletDustDetector
from .bricklet_e_paper_296x128 import BrickletEPaper296x128
from .bricklet_energy_monitor import BrickletEnergyMonitor
from .bricklet_gps_v2 import BrickletGPSV2
from .bricklet_gps_v3 import BrickletGPSV3
from .bricklet_hall_effect import BrickletHallEffect
from .bricklet_hall_effect_v2 import BrickletHallEffectV2
from .bricklet_humidity import BrickletHumidity
from .bricklet_humidity_v2 import BrickletHumidityV2
from .bricklet_imu_v3 import BrickletIMUV3
from .bricklet_industrial_analog_out_v2 import BrickletIndustrialAnalogOutV2
from .bricklet_industrial_counter import BrickletIndustrialCounter
from .bricklet_industrial_digital_in_4_v2 import BrickletIndustrialDigitalIn4V2
from .bricklet_industrial_digital_out_4 import BrickletIndustrialDigitalOut4
from .bricklet_industrial_digital_out_4_v2 import BrickletIndustrialDigitalOut4V2
from .bricklet_industrial_dual_0_20ma import BrickletIndustrialDual020mA
from .bricklet_industrial_dual_0_20ma_v2 import BrickletIndustrialDual020mAV2
from .bricklet_industrial_dual_ac_in import BrickletIndustrialDualACIn
from .bricklet_industrial_dual_ac_relay import BrickletIndustrialDualACRelay
from .bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2
from .bricklet_industrial_dual_relay import BrickletIndustrialDualRelay
from .bricklet_industrial_ptc import BrickletIndustrialPtc
from .bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
from .bricklet_io4_v2 import BrickletIO4V2
from .bricklet_io16 import BrickletIO16
from .bricklet_io16_v2 import BrickletIO16V2
from .bricklet_isolator import BrickletIsolator
from .bricklet_joystick import BrickletJoystick
from .bricklet_joystick_v2 import BrickletJoystickV2
from .bricklet_laser_range_finder_v2 import BrickletLaserRangeFinderV2
from .bricklet_lcd_20x4 import BrickletLCD20x4
from .bricklet_lcd_128x64 import BrickletLCD128x64
from .bricklet_led_strip_v2 import BrickletLEDStripV2
from .bricklet_line import BrickletLine
from .bricklet_linear_poti import BrickletLinearPoti
from .bricklet_linear_poti_v2 import BrickletLinearPotiV2
from .bricklet_load_cell_v2 import BrickletLoadCellV2
from .bricklet_moisture import BrickletMoisture
from .bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from .bricklet_motorized_linear_poti import BrickletMotorizedLinearPoti
from .bricklet_multi_touch import BrickletMultiTouch
from .bricklet_multi_touch_v2 import BrickletMultiTouchV2
from .bricklet_nfc import BrickletNFC
from .bricklet_oled_64x48 import BrickletOLED64x48
from .bricklet_oled_128x64_v2 import BrickletOLED128x64V2
from .bricklet_one_wire import BrickletOneWire
from .bricklet_outdoor_weather import BrickletOutdoorWeather
from .bricklet_particulate_matter import BrickletParticulateMatter
from .bricklet_performance_dc import BrickletPerformanceDC
from .bricklet_piezo_speaker import BrickletPiezoSpeaker
from .bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2
from .bricklet_ptc import BrickletPtc
from .bricklet_ptc_v2 import BrickletPtcV2
from .bricklet_real_time_clock import BrickletRealTimeClock
from .bricklet_real_time_clock_v2 import BrickletRealTimeClockV2
from .bricklet_remote_switch_v2 import BrickletRemoteSwitchV2
from .bricklet_rgb_led_button import BrickletRGBLEDButton
from .bricklet_rgb_led_v2 import BrickletRGBLEDV2
from .bricklet_rotary_encoder_v2 import BrickletRotaryEncoderV2
from .bricklet_rotary_poti import BrickletRotaryPoti
from .bricklet_rotary_poti_v2 import BrickletRotaryPotiV2
from .bricklet_rs232 import BrickletRS232
from .bricklet_rs232_v2 import BrickletRS232V2
from .bricklet_rs485 import BrickletRS485
from .bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
from .bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
from .bricklet_servo_v2 import BrickletServoV2
from .bricklet_silent_stepper_v2 import BrickletSilentStepperV2
from .bricklet_solid_state_relay_v2 import BrickletSolidStateRelayV2
from .bricklet_sound_intensity import BrickletSoundIntensity
from .bricklet_sound_pressure_level import BrickletSoundPressureLevel
from .bricklet_temperature import BrickletTemperature
from .bricklet_temperature_ir_v2 import BrickletTemperatureIRV2
from .bricklet_temperature_v2 import BrickletTemperatureV2
from .bricklet_thermal_imaging import BrickletThermalImaging
from .bricklet_thermocouple_v2 import BrickletThermocoupleV2
from .bricklet_tilt import BrickletTilt
from .bricklet_uv_light_v2 import BrickletUVLightV2
from .bricklet_voltage_current_v2 import BrickletVoltageCurrentV2
from .bricklet_xmc1400_breakout import BrickletXMC1400Breakout

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
            raise ValueError(f"No device available for id {device_id!s}") from None


device_factory = DeviceFactory()

device_factory.register(BrickESP32)
device_factory.register(BrickESP32Ethernet)
device_factory.register(BrickHAT)
device_factory.register(BrickHATZero)
device_factory.register(BrickIMUV2)
device_factory.register(BrickletAccelerometerV2)
device_factory.register(BrickletAirQuality)
device_factory.register(BrickletAmbientLightV2)
device_factory.register(BrickletAmbientLightV3)
device_factory.register(BrickletAnalogIn)
device_factory.register(BrickletAnalogInV3)
device_factory.register(BrickletAnalogOutV3)
device_factory.register(BrickletBarometer)
device_factory.register(BrickletBarometerV2)
device_factory.register(BrickletCAN)
device_factory.register(BrickletCANV2)
device_factory.register(BrickletCO2V2)
device_factory.register(BrickletColor)
device_factory.register(BrickletColorV2)
device_factory.register(BrickletCompass)
device_factory.register(BrickletDCV2)
device_factory.register(BrickletDistanceIR)
device_factory.register(BrickletDistanceIRV2)
device_factory.register(BrickletDistanceUSV2)
device_factory.register(BrickletDMX)
device_factory.register(BrickletDualButtonV2)
device_factory.register(BrickletDustDetector)
device_factory.register(BrickletEnergyMonitor)
device_factory.register(BrickletEPaper296x128)
device_factory.register(BrickletGPSV2)
device_factory.register(BrickletGPSV3)
device_factory.register(BrickletHallEffect)
device_factory.register(BrickletHallEffectV2)
device_factory.register(BrickletHumidity)
device_factory.register(BrickletHumidityV2)
device_factory.register(BrickletIMUV3)
device_factory.register(BrickletIndustrialAnalogOutV2)
device_factory.register(BrickletIndustrialCounter)
device_factory.register(BrickletIndustrialDigitalIn4V2)
device_factory.register(BrickletIndustrialDigitalOut4)
device_factory.register(BrickletIndustrialDigitalOut4V2)
device_factory.register(BrickletIndustrialDual020mA)
device_factory.register(BrickletIndustrialDual020mAV2)
device_factory.register(BrickletIndustrialDualACIn)
device_factory.register(BrickletIndustrialDualACRelay)
device_factory.register(BrickletIndustrialDualAnalogInV2)
device_factory.register(BrickletIndustrialDualRelay)
device_factory.register(BrickletIndustrialPtc)
device_factory.register(BrickletIndustrialQuadRelayV2)
device_factory.register(BrickletIO16)
device_factory.register(BrickletIO16V2)
device_factory.register(BrickletIO4V2)
device_factory.register(BrickletIsolator)
device_factory.register(BrickletJoystick)
device_factory.register(BrickletJoystickV2)
device_factory.register(BrickletLaserRangeFinderV2)
device_factory.register(BrickletLCD128x64)
device_factory.register(BrickletLCD20x4)
device_factory.register(BrickletLEDStripV2)
device_factory.register(BrickletLine)
device_factory.register(BrickletLinearPoti)
device_factory.register(BrickletLinearPotiV2)
device_factory.register(BrickletLoadCellV2)
device_factory.register(BrickletMoisture)
device_factory.register(BrickletMotionDetectorV2)
device_factory.register(BrickletMotorizedLinearPoti)
device_factory.register(BrickletMultiTouch)
device_factory.register(BrickletMultiTouchV2)
device_factory.register(BrickletNFC)
device_factory.register(BrickletOLED128x64V2)
device_factory.register(BrickletOLED64x48)
device_factory.register(BrickletOneWire)
device_factory.register(BrickletOutdoorWeather)
device_factory.register(BrickletParticulateMatter)
device_factory.register(BrickletPerformanceDC)
device_factory.register(BrickletPiezoSpeaker)
device_factory.register(BrickletPiezoSpeakerV2)
device_factory.register(BrickletPtc)
device_factory.register(BrickletPtcV2)
device_factory.register(BrickletRealTimeClock)
device_factory.register(BrickletRealTimeClockV2)
device_factory.register(BrickletRemoteSwitchV2)
device_factory.register(BrickletRGBLEDButton)
device_factory.register(BrickletRGBLEDV2)
device_factory.register(BrickletRotaryEncoderV2)
device_factory.register(BrickletRotaryPoti)
device_factory.register(BrickletRotaryPotiV2)
device_factory.register(BrickletRS232)
device_factory.register(BrickletRS232V2)
device_factory.register(BrickletRS485)
device_factory.register(BrickletSegmentDisplay4x7)
device_factory.register(BrickletSegmentDisplay4x7V2)
device_factory.register(BrickletServoV2)
device_factory.register(BrickletSilentStepperV2)
device_factory.register(BrickletSolidStateRelayV2)
device_factory.register(BrickletSoundIntensity)
device_factory.register(BrickletSoundPressureLevel)
device_factory.register(BrickletTemperature)
device_factory.register(BrickletTemperatureIRV2)
device_factory.register(BrickletTemperatureV2)
device_factory.register(BrickletThermalImaging)
device_factory.register(BrickletThermocoupleV2)
device_factory.register(BrickletTilt)
device_factory.register(BrickletUVLightV2)
device_factory.register(BrickletVoltageCurrentV2)
device_factory.register(BrickletXMC1400Breakout)
device_factory.register(BrickMaster)
device_factory.register(BrickRED)
device_factory.register(BrickSilentStepper)
