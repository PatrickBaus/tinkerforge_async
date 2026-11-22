[![pylint](../../actions/workflows/pylint.yml/badge.svg)](../../actions/workflows/pylint.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/PatrickBaus/tinkerforge_async/python-coverage-comment-action-data/endpoint.json)](https://github.com/PatrickBaus/tinkerforge_async/tree/python-coverage-comment-action-data)
[![PyPI](https://img.shields.io/pypi/v/tinkerforge-async)](https://pypi.org/project/tinkerforge-async/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinkerforge-async)
![PyPI - Status](https://img.shields.io/pypi/status/tinkerforge-async)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# TinkerforgeAsync
This is a reimplementation of the Tinkerforge Python bindings ([original Python bindings](https://www.tinkerforge.com/en/doc/Software/API_Bindings_Python.html)) using Python 3 asyncio. The original bindings used threads to manage the blocking operations. A much cleaner implementation is possible using the `await` syntax from asyncio.

**Note: This API implementation is not an official Tinkerforge implementation. I am in no way affiliated with the Tinkerforge GmbH. Use at your own risk. If you find any bugs, please report them.**

The library is fully type-hinted.

# Supported Bricks/Bricklets

| Brick                                                                                                | Supported          | Tested             |
|------------------------------------------------------------------------------------------------------|--------------------|--------------------|
| [DC (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricks/DC_Brick.html)                | :heavy_check_mark: |                    |
| [ESP32](https://www.tinkerforge.com/en/doc/Software/Bricks/ESP32_Brick_Python.html)                  | :heavy_check_mark: |                    |
| [ESP32 Ethernet](https://www.tinkerforge.com/en/doc/Software/Bricks/ESP32Ethernet_Brick_Python.html) | :heavy_check_mark: |                    |
| [HAT](https://www.tinkerforge.com/en/doc/Software/Bricks/HAT_Brick_Python.html)                      | :heavy_check_mark: |                    |
| [HAT Zero](https://www.tinkerforge.com/en/doc/Software/Bricks/HATZero_Brick_Python.html)             | :heavy_check_mark: |                    |
| [IMU (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricks/IMU_Brick.html)              | :heavy_check_mark: |                    |
| [IMU 2.0](https://www.tinkerforge.com/en/doc/Software/Bricks/IMUV2_Brick_Python.html)                | :heavy_check_mark: |                    |
| [Master](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html)                       | :heavy_check_mark: | :heavy_check_mark: |
| [RED](https://www.tinkerforge.com/en/doc/Software/Bricks/RED_Brick_Python.html)                      | :heavy_check_mark: |                    |
| [Servo (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Servo_Brick.html)          | :heavy_check_mark: |                    |
| [Silent Stepper](https://www.tinkerforge.com/en/doc/Software/Bricks/SilentStepper_Brick_Python.html) | :heavy_check_mark: |                    |
| [Stepper (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Stepper_Brick.html)      | :heavy_check_mark: |                    |

| Bricklet                                                                                                                           | Supported          | Tested             |
|------------------------------------------------------------------------------------------------------------------------------------|--------------------|--------------------|
| [Accelerometer (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Accelerometer.html)                           | :heavy_check_mark: |                    |
| [Accelerometer 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/AccelerometerV2_Bricklet_Python.html)                    | :heavy_check_mark: |                    |
| [Air Quality](https://www.tinkerforge.com/en/doc/Software/Bricklets/AirQuality_Bricklet_Python.html)                               | :heavy_check_mark: |                    |
| [Ambient Light (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light.html)                           | :heavy_check_mark: |                    |
| [Ambient Light 2.0 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V2.html)                    | :heavy_check_mark: | :heavy_check_mark: |
| [Ambient Light 3.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V3.html)                                   | :heavy_check_mark: | :heavy_check_mark: |
| [Analog In (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Analog_In.html)                                   | :heavy_check_mark: | :heavy_check_mark: |
| [Analog In 2.0 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Analog_In_V2.html)                            | :heavy_check_mark: |                    |
| [Analog In 3.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/AnalogInV3_Bricklet_Python.html)                             | :heavy_check_mark: |                    |
| [Analog Out (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Analog_Out.html)                                 | :heavy_check_mark: |                    |
| [Analog Out 2.0 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Analog_Out_V2.html)                          | :heavy_check_mark: |                    |
| [Analog Out 3.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/AnalogOutV3_Bricklet_Python.html)                           | :heavy_check_mark: |                    |
| [Barometer](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Barometer.html)                                                  | :heavy_check_mark: | :heavy_check_mark: |
| [Barometer 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Barometer_V2.html)                                           | :heavy_check_mark: | :heavy_check_mark: |
| [CAN](https://www.tinkerforge.com/en/doc/Software/Bricklets/CAN_Bricklet_Python.html)                                              | :heavy_check_mark: |                    |
| [CAN 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/CANV2_Bricklet_Python.html)                                        | :heavy_check_mark: |                    |
| [CO2 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/CO2.html)                                               | :heavy_check_mark: |                    |
| [CO2 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/CO2V2_Bricklet_Python.html)                                        | :heavy_check_mark: |                    |
| [Color](https://www.tinkerforge.com/en/doc/Software/Bricklets/Color_Bricklet_Python.html)                                          | :heavy_check_mark: |                    |
| [Color 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/ColorV2_Bricklet_Python.html)                                    | :heavy_check_mark: |                    |
| [Compass](https://www.tinkerforge.com/en/doc/Software/Bricklets/Compass_Bricklet_Python.html)                                      | :heavy_check_mark: |                    |
| [Current12 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Current12.html)                                   | :heavy_check_mark: |                    |
| [Current25 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Current25.html)                                   | :heavy_check_mark: |                    |
| [DC 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/DCV2_Bricklet_Python.html)                                          | :heavy_check_mark: |                    |
| [Distance IR](https://www.tinkerforge.com/en/doc/Software/Bricklets/DistanceIR_Bricklet_Python.html)                               | :heavy_check_mark: |                    |
| [Distance IR 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/DistanceIRV2_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [Distance US (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Distance_US.html)                               | :heavy_check_mark: |                    |
| [Distance US 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/DistanceUSV2_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [DMX](https://www.tinkerforge.com/en/doc/Software/Bricklets/DMX_Bricklet_Python.html)                                              | :heavy_check_mark: |                    |
| [Dual Button (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Dual_Button.html)                               | :heavy_check_mark: |                    |
| [Dual Button 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/DualButtonV2_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [Dual Relay (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Dual_Relay.html)                                 | :heavy_check_mark: |                    |
| [Dust Detector](https://www.tinkerforge.com/en/doc/Software/Bricklets/DustDetector_Bricklet_Python.html)                           | :heavy_check_mark: |                    |
| [E-Paper 296x128](https://www.tinkerforge.com/en/doc/Software/Bricklets/EPaper296x128_Bricklet_Python.html)                        | :heavy_check_mark: |                    |
| [Energy Monitor](https://www.tinkerforge.com/en/doc/Software/Bricklets/EnergyMonitor_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [GPS (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/GPS.html)                                               | :heavy_check_mark: |                    |
| [GPS 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/GPSV2_Bricklet_Python.html)                                        | :heavy_check_mark: |                    |
| [GPS 3.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/GPSV3_Bricklet_Python.html)                                        | :heavy_check_mark: |                    |
| [Hall Effect](https://www.tinkerforge.com/en/doc/Software/Bricklets/HallEffect_Bricklet_Python.html)                               | :heavy_check_mark: |                    |
| [Hall Effect 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/HallEffectV2_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [Humidity (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Humidity.html)                                     | :heavy_check_mark: | :heavy_check_mark: |
| [Humidity 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Humidity_V2.html)                                             | :heavy_check_mark: | :heavy_check_mark: |
| [IMU 3.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/IMUV3_Bricklet_Python.html)                                        | :heavy_check_mark: |                    |
| [Industrial Analog Out (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Analog_Out.html)           | :heavy_check_mark: |                    |
| [Industrial Analog Out 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialAnalogOutV2_Bricklet_Python.html)      | :heavy_check_mark: |                    |
| [Industrial Counter](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialCounter_Bricklet_Python.html)                 | :heavy_check_mark: |                    |
| [Industrial Digital In 4 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Digital_In_4.html)       | :heavy_check_mark: |                    |
| [Industrial Digital In 4 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDigitalIn4V2_Bricklet_Python.html)   | :heavy_check_mark: |                    |
| [Industrial Digital Out 4](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDigitalOut4_Bricklet_Python.html)       | :heavy_check_mark: |                    |
| [Industrial Digital Out 4 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDigitalOut4V2_Bricklet_Python.html) | :heavy_check_mark: |                    |
| [Industrial Dual 0-20mA](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDual020mA_Bricklet_Python.html)           | :heavy_check_mark: |                    |
| [Industrial Dual 0-20mA 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Dual_020mA_V2.html)                  | :heavy_check_mark: | :heavy_check_mark: |
| [Industrial Dual AC In](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDualACIn_Bricklet_Python.html)             | :heavy_check_mark: |                    |
| [Industrial Dual AC Relay](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDualACRelay_Bricklet_Python.html)       | :heavy_check_mark: |                    |
| [Industrial Dual Analog In (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Dual_Analog_In.html)   | :heavy_check_mark: |                    |
| [Industrial Dual Analog In 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Dual_Analog_In_V2.html)           | :heavy_check_mark: | :heavy_check_mark: |
| [Industrial Dual Relay](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialDualRelay_Bricklet_Python.html)            | :heavy_check_mark: |                    |
| [Industrial PTC](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_PTC.html)                                        | :heavy_check_mark: | :heavy_check_mark: |
| [Industrial Quad Relay (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Quad_Relay.html)           | :heavy_check_mark: |                    |
| [Industrial Quad Relay 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/IndustrialQuadRelayV2_Bricklet_Python.html)      | :heavy_check_mark: |                    |
| [IO-16](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/IO16.html)                                                           | :heavy_check_mark: | :heavy_check_mark: |
| [IO-16 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/IO16V2_Bricklet_Python.html)                                     | :heavy_check_mark: |                    |
| [IO-4 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/IO4.html)                                              | :heavy_check_mark: |                    |
| [IO-4 2.0](https://www.tinkerforge.com/de/doc/Hardware/Bricklets/IO4_V2.html)                                                      | :heavy_check_mark: | :heavy_check_mark: |
| [Isolator](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Isolator.html)                                                    | :heavy_check_mark: | :heavy_check_mark: |
| [Joystick](https://www.tinkerforge.com/en/doc/Software/Bricklets/Joystick_Bricklet_Python.html)                                    | :heavy_check_mark: |                    |
| [Joystick 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/JoystickV2_Bricklet_Python.html)                              | :heavy_check_mark: |                    |
| [Laser Range Finder (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Laser_Range_Finder.html)                 | :heavy_check_mark: |                    |
| [Laser Range Finder 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/LaserRangeFinderV2_Bricklet_Python.html)            | :heavy_check_mark: |                    |
| [LCD 128x64](https://www.tinkerforge.com/en/doc/Software/Bricklets/LCD128x64_Bricklet_Python.html)                                 | :heavy_check_mark: |                    |
| [LCD 16x2 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/LCD_16x2.html)                                     | :heavy_check_mark: |                    |
| [LCD 20x4](https://www.tinkerforge.com/en/doc/Software/Bricklets/LCD20x4_Bricklet_Python.html)                                     | :heavy_check_mark: |                    |
| [LED Strip (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/LED_Strip.html)                                   | :heavy_check_mark: |                    |
| [LED Strip 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/LEDStripV2_Bricklet_Python.html)                             | :heavy_check_mark: |                    |
| [Line](https://www.tinkerforge.com/en/doc/Software/Bricklets/Line_Bricklet_Python.html)                                            | :heavy_check_mark: |                    |
| [Linear Poti](https://www.tinkerforge.com/en/doc/Software/Bricklets/LinearPoti_Bricklet_Python.html)                               | :heavy_check_mark: |                    |
| [Linear Poti 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/LinearPotiV2_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [Load Cell (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Load_Cell.html)                                   | :heavy_check_mark: |                    |
| [Load Cell 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/LoadCellV2_Bricklet_Python.html)                             | :heavy_check_mark: |                    |
| [Moisture (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Moisture.html)                                     | :heavy_check_mark: | :heavy_check_mark: |
| [Motion Detector (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Motion_Detector.html)                       | :heavy_check_mark: |                    |
| [Motion Detector 2.0](https://www.tinkerforge.com/de/doc/Hardware/Bricklets/Motion_Detector_V2.html)                               | :heavy_check_mark: | :heavy_check_mark: |
| [Motorized Linear Poti](https://www.tinkerforge.com/en/doc/Software/Bricklets/MotorizedLinearPoti_Bricklet_Python.html)            | :heavy_check_mark: |                    |
| [Multi Touch](https://www.tinkerforge.com/en/doc/Software/Bricklets/MultiTouch_Bricklet_Python.html)                               | :heavy_check_mark: |                    |
| [Multi Touch 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/MultiTouchV2_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [NFC](https://www.tinkerforge.com/en/doc/Software/Bricklets/NFC_Bricklet_Python.html)                                              | :heavy_check_mark: |                    |
| [NFC/RFID (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/NFC_RFID.html)                                     | :heavy_check_mark: |                    |
| [OLED 128x64 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/OLED_128x64.html)                               | :heavy_check_mark: |                    |
| [OLED 128x64 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/OLED128x64V2_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [OLED 64x48](https://www.tinkerforge.com/en/doc/Software/Bricklets/OLED64x48_Bricklet_Python.html)                                 | :heavy_check_mark: |                    |
| [One Wire](https://www.tinkerforge.com/en/doc/Software/Bricklets/OneWire_Bricklet_Python.html)                                     | :heavy_check_mark: |                    |
| [Outdoor Weather](https://www.tinkerforge.com/en/doc/Software/Bricklets/OutdoorWeather_Bricklet_Python.html)                       | :heavy_check_mark: |                    |
| [Particulate Matter](https://www.tinkerforge.com/en/doc/Software/Bricklets/ParticulateMatter_Bricklet_Python.html)                 | :heavy_check_mark: |                    |
| [Performance DC](https://www.tinkerforge.com/en/doc/Software/Bricklets/PerformanceDC_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [Piezo Buzzer (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Piezo_Buzzer.html)                             | :heavy_check_mark: |                    |
| [Piezo Speaker](https://www.tinkerforge.com/en/doc/Software/Bricklets/PiezoSpeaker_Bricklet_Python.html)                           | :heavy_check_mark: |                    |
| [Piezo Speaker 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/PiezoSpeakerV2_Bricklet_Python.html)                     | :heavy_check_mark: |                    |
| [PTC (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/PTC.html)                                               | :heavy_check_mark: | :heavy_check_mark: |
| [PTC 2.0 (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/PTC_V2.html)                                        | :heavy_check_mark: | :heavy_check_mark: |
| [Real-Time Clock](https://www.tinkerforge.com/en/doc/Software/Bricklets/RealTimeClock_Bricklet_Python.html)                        | :heavy_check_mark: |                    |
| [Real-Time Clock 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/RealTimeClockV2_Bricklet_Python.html)                  | :heavy_check_mark: |                    |
| [Remote Switch (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Remote_Switch.html)                           | :heavy_check_mark: |                    |
| [Remote Switch 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/RemoteSwitchV2_Bricklet_Python.html)                     | :heavy_check_mark: |                    |
| [RGB LED (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED.html)                                       | :heavy_check_mark: |                    |
| [RGB LED 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDV2_Bricklet_Python.html)                                 | :heavy_check_mark: |                    |
| [RGB LED Button](https://www.tinkerforge.com/en/doc/Software/Bricklets/RGBLEDButton_Bricklet_Python.html)                          | :heavy_check_mark: |                    |
| [RGB LED Matrix (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RGB_LED_Matrix.html)                         | :heavy_check_mark: |                    |
| [Rotary Encoder (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Rotary_Encoder.html)                         | :heavy_check_mark: |                    |
| [Rotary Encoder 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/RotaryEncoderV2_Bricklet_Python.html)                   | :heavy_check_mark: |                    |
| [Rotary Poti](https://www.tinkerforge.com/en/doc/Software/Bricklets/RotaryPoti_Bricklet_Python.html)                               | :heavy_check_mark: |                    |
| [Rotary Poti 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/RotaryPotiV2_Bricklet_Python.html)                         | :heavy_check_mark: |                    |
| [RS232](https://www.tinkerforge.com/en/doc/Software/Bricklets/RS232_Bricklet_Python.html)                                          | :heavy_check_mark: |                    |
| [RS232 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RS232_V2.html)                                                   | :heavy_check_mark: | :heavy_check_mark: |
| [RS485](https://www.tinkerforge.com/en/doc/Software/Bricklets/RS485_Bricklet_Python.html)                                          | :heavy_check_mark: |                    |
| [Segment Display 4x7](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Segment_Display_4x7.html)                              | :heavy_check_mark: | :heavy_check_mark: |
| [Segment Display 4x7 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Segment_Display_4x7_V2.html)                       | :heavy_check_mark: | :heavy_check_mark: |
| [Servo 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/ServoV2_Bricklet_Python.html)                                    | :heavy_check_mark: |                    |
| [Silent Stepper 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/SilentStepperV2_Bricklet_Python.html)                   | :heavy_check_mark: |                    |
| [Solid State Relay (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Solid_State_Relay.html)                   | :heavy_check_mark: |                    |
| [Solid State Relay 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/SolidStateRelayV2_Bricklet_Python.html)              | :heavy_check_mark: |                    |
| [Sound Intensity](https://www.tinkerforge.com/en/doc/Software/Bricklets/SoundIntensity_Bricklet_Python.html)                       | :heavy_check_mark: |                    |
| [Sound Pressure Level](https://www.tinkerforge.com/en/doc/Software/Bricklets/SoundPressureLevel_Bricklet_Python.html)              | :heavy_check_mark: |                    |
| [Temperature](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature.html)                                              | :heavy_check_mark: | :heavy_check_mark: |
| [Temperature 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature_V2.html)                                       | :heavy_check_mark: | :heavy_check_mark: |
| [Temperature IR (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature_IR.html)                         | :heavy_check_mark: |                    |
| [Temperature IR 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/TemperatureIRV2_Bricklet_Python.html)                   | :heavy_check_mark: |                    |
| [Thermal Imaging](https://www.tinkerforge.com/en/doc/Software/Bricklets/ThermalImaging_Bricklet_Python.html)                       | :heavy_check_mark: |                    |
| [Thermocouple (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermocouple.html)                             | :heavy_check_mark: |                    |
| [Thermocouple 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermocouple_V2.html)                                     | :heavy_check_mark: | :heavy_check_mark: |
| [Tilt](https://www.tinkerforge.com/en/doc/Software/Bricklets/Tilt_Bricklet_Python.html)                                            | :heavy_check_mark: |                    |
| [UV Light (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/UV_Light.html)                                     | :heavy_check_mark: |                    |
| [UV Light 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/UVLightV2_Bricklet_Python.html)                               | :heavy_check_mark: |                    |
| [Voltage (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Voltage.html)                                       | :heavy_check_mark: |                    |
| [Voltage/Current (discontinued)](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Voltage_Current.html)                       | :heavy_check_mark: |                    |
| [Voltage/Current 2.0](https://www.tinkerforge.com/en/doc/Software/Bricklets/VoltageCurrentV2_Bricklet_Python.html)                 | :heavy_check_mark: |                    |
| [XMC1400 Breakout](https://www.tinkerforge.com/en/doc/Software/Bricklets/XMC1400Breakout_Bricklet_Python.html)                     | :heavy_check_mark: |                    |

*Tested* means tested with the hardware. The other devices are tested against the protocol only, see below.
Devices marked *(discontinued)* are no longer sold by Tinkerforge.

## Generated Bricks and Bricklets
The modules of the Bricks and Bricklets without a check mark in the *Tested* column were generated from the
[Tinkerforge API definitions](https://github.com/Tinkerforge/generators) (CC0 licensed) and follow the same
conventions as the hand-written modules:

- All values are converted to SI units and returned as `Decimal`, e.g. V, A, W, m, s, K, Pa, kg, T and m/s².
  Energy is returned in J, speeds in m/s and accelerations given in g are converted to m/s². Angles stay in
  degrees, percentages in percent and dimensionless values (ppm, dB, UV index) as they are. Counts (bytes, steps,
  baud) are returned as `int`.
- Every function documents the units of its parameters and results in a *Units* line of its docstring. The rest
  of the docstrings is taken from the official documentation, so numbers in the descriptions can refer to raw
  values.
- Constants are `Enum`s, invalid arguments raise a `ValueError` before anything is sent.
- Functions, that transfer more data than fits into a single packet (e.g. `write_pixels()` of the LCD 128x64
  Bricklet or `write()` of the RS485 Bricklet), have a high-level version, that splits the data into chunks. The
  `*_low_level()` functions are available, too. Streamed callbacks are reassembled before they are yielded by
  `read_events()`.
- `get_value()`, `set_callback_configuration()` and `get_callback_configuration()` work with the secondary ids
  (sids) listed in the `CHANNELS` table of each device.

The function ids and payload formats are checked against the official Python bindings by the tests.
## Documentation
The documentation is currently work in progress. The full documentation will be moved to
[https://patrickbaus.github.io/tinkerforge_async/](https://patrickbaus.github.io/tinkerforge_async/). Below you can
find the current state of the documentation. I use the
[Numpydoc](https://numpydoc.readthedocs.io/en/latest/format.html) style for documentation and
[Sphinx](https://www.sphinx-doc.org/en/master/index.html) for compiling it.

# Setup
To install the library in a virtual environment (always use venvs with every project):
```bash
python3 -m venv env  # virtual environment, optional
source env/bin/activate  # only if the virtual environment is used
pip install tinkerforge-async
```

# Changes made to the API
Some design choices of the original Tinkerforge API are overly complex. I therefore replaced them with a simpler and more intuitive approach. A list of things that were changed can be found below:
## Design Changes
- Only Python 3 is supported (3.9+)
 - Replaced threads with an async event loop
 - Completely rewritten how responses from bricks/bricklets work. All setters now have a `response_expected` parameter, which is set to `True` by default. If there is an error when calling the function, it will then raise an exception - either an `AttributeError` if the function is unknown, or a `ValueError` if one or more parameters are invalid.

   Old style:
   ```python
   bricklet = BrickletHumidity(UID, ipcon)
   bricklet.set_response_expected(
       BrickletHumidity.FUNCTION_SET_HUMIDITY_CALLBACK_PERIOD, True
   )
   bricklet.set_humidity_callback_period(1000)
   ```
   New style:
   ```python
   bricklet = BrickletHumidity(UID, ipcon)
   await bricklet.set_humidity_callback_period(
       1, response_expected=True
   )  # Raises an exception if unsuccessful
   ```
 - Replaced all constants with Enums and enforced their use using assertions. This will allow beginners to spot their mistakes earlier and make the code more readable, including any debug output statements.

   Old style:
   ```python
   class BrickletHumidity(Device):
       FUNCTION_GET_HUMIDITY = 1
       FUNCTION_GET_ANALOG_VALUE = 2
       FUNCTION_SET_HUMIDITY_CALLBACK_PERIOD = 3
       FUNCTION_GET_HUMIDITY_CALLBACK_PERIOD = 4
       FUNCTION_SET_ANALOG_VALUE_CALLBACK_PERIOD = 5
       FUNCTION_GET_ANALOG_VALUE_CALLBACK_PERIOD = 6
       FUNCTION_SET_HUMIDITY_CALLBACK_THRESHOLD = 7
       FUNCTION_GET_HUMIDITY_CALLBACK_THRESHOLD = 8
       FUNCTION_SET_ANALOG_VALUE_CALLBACK_THRESHOLD = 9
       FUNCTION_GET_ANALOG_VALUE_CALLBACK_THRESHOLD = 10
       FUNCTION_SET_DEBOUNCE_PERIOD = 11
       FUNCTION_GET_DEBOUNCE_PERIOD = 12
       FUNCTION_GET_IDENTITY = 255
   ```

   New style:
   ```python
   class BrickletHumidity(Device):
       @unique
       class FunctionID(Enum):
           GET_HUMIDITY = 1
           GET_ANALOG_VALUE = 2
           SET_HUMIDITY_CALLBACK_PERIOD = 3
           GET_HUMIDITY_CALLBACK_PERIOD = 4
           SET_ANALOG_VALUE_CALLBACK_PERIOD = 5
           GET_ANALOG_VALUE_CALLBACK_PERIOD = 6
           SET_HUMIDITY_CALLBACK_THRESHOLD = 7
           GET_HUMIDITY_CALLBACK_THRESHOLD = 8
           SET_ANALOG_VALUE_CALLBACK_THRESHOLD = 9
           GET_ANALOG_VALUE_CALLBACK_THRESHOLD = 10
           SET_DEBOUNCE_PERIOD = 11
           GET_DEBOUNCE_PERIOD = 12
   ```
 - Moved from base58 encoded uids to integers.
 - Moved from callbacks to queues in order to keep users out of the callback hell. It makes the code style more readable when using the `await` syntax anyway.
 - Payloads will now be decoded by the `Device` object and no longer by the `ip_connection`. This makes the code a lot more readable. To do so, the payload and decoded header will be handed to the device. It will then decode it, if possible, and pass it on to the queue.
 - If physical quantities are measured we will now return standard SI units, not some unexpected stuff like centi °C (Temperature Bricklet). To preserve the precision the Decimal package is used. This includes temperatures, which are given in K, not °C. Durations (callback periods, debounce periods, monoflop times, ...) are given in s, not ms, like the delay of `asyncio.sleep()`. Durations that are passed to the library can be `int`, `float` or `Decimal`, durations returned by the library are `Decimal`.
 - All callbacks now contain a timestamp (Unix timestamp) and the device object.

   Example:
   ```
    Event(timestamp=1658756708.6839857, sender=Temperature Bricklet 2.0 with uid 161085 connected at IPConnectionAsync(192.168.1.164:4223), sid=0, function_id=CallbackID.TEMPERATURE, payload=305.46)
   ```

 - Added the concept of secondary ids (`sid`). By default, the secondary id is `0`. If there is more than one sensor on the bricklet, they will have a `sid` value of 1,2, etc. This is especially useful for sensors like the [Industrial Dual Analog In Bricklet 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Dual_Analog_In_V2.html), which returns its two channels via the same callback.
 - New functions:

   `BrickMaster.set_wpa_enterprise_username(username)`: Set the WPA enterprise username without calling `BrickMaster.set_wifi_certificate()`. Takes a `string` instead of an array of `int`.
   `BrickMaster.set_wpa_enterprise_password(password)`: Set the WPA enterprise password without calling `BrickMaster.set_wifi_certificate()`. Takes a `string` instead of an array of `int`.
   `BrickMaster.get_wpa_enterprise_username()`: Get the WPA enterprise password without calling `BrickMaster.get_wifi_certificate()`. Also returns a `string` instead of an array of `int`.
   `BrickMaster.get_wpa_enterprise_password()`: Get the WPA enterprise password without calling `BrickMaster.get_wifi_certificate()`. Also returns a `string` instead of an array of `int`.

- ### [IP Connection](https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html#api)
   - `IPConnection.authenticate(secret)`: removed. This can now be done through connect()
   - `IPConnection.set_timeout/IPConnection.get_timeout`: Replaced by a property
   - `IPConnection.register_callback(callback_id, function)`: Replaced by `register_event_queue()`
   - `IPConnection.connect(host, port=4223, authentication_secret='')`: If `authentication_secret` is not empty, try to authenticate.

- ### [IO-4 Bricklet 2.0](https://www.tinkerforge.com/de/doc/Software/Bricklets/IO4V2_Bricklet_Python.html)
   - `BrickletIO4V2.set_pwm_configuration()` will now take the frequency in units of Hz and the duty cycle is normalized to 1, so it will take a float from [0...1].
   - `BrickletIO4V2.get_pwm_configuration()` will return the frequency in units of Hz and the duty cycle is normalized to 1.
   - `BrickletIO4V2.set_edge_count_callback_configuration()` sets the callback configuration for the edge counter callback. Its secondary ids are in [5...8] for channels [0...3].
   - `BrickletIO4V2.get_edge_count_callback_configuration()` returns the callback configuration for the edge counter callback.

- ### [Master Brick](https://www.tinkerforge.com/en/doc/Software/Bricks/Master_Brick_Python.html)
   - `BrickMaster.set_wifi_configuration()`/`BrickMaster.get_wifi_configuration()` will take/return all ips in natural order
   - `BrickMaster.set_ethernet_configuration()`/`BrickMaster.get_ethernet_configuration()` will take/return all ips in natural order
   - `BrickMaster.write_wifi2_serial_port()` will only accept a `bytestring` and no length argument. The length will be automatically determined from the string.
   - `BrickMaster.set_wifi2_status_led(enabled)` added. This allows setting the status led by value instead of calling `enable_wifi2_status_led`/`disable_wifi2_status_led`

- ### [PTC Bricklet](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/PTC.html)
   - `BrickletPtc()` takes an additional parameter to define the type of sensor. The options are `BrickletPtc.SensorType.PT_100` and `BrickletPtc.SensorType.PT_1000`. This only determines the resistance returned by the bricklet. The default is `BrickletPtc.SensorType.PT_100`.
   - `BrickletPtc.sensor_type` getter and setter to change the type of sensor used.

- ### [PTC Bricklet 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/PTC_V2.html)
   - `BrickletPtcV2()` takes an additional parameter to define the type of sensor. The options are `BrickletPtc.SensorType.PT_100` and `BrickletPtc.SensorType.PT_1000`. This only determines the resistance returned by the bricklet. The default is `BrickletPtc.SensorType.PT_100`.
   - `BrickletPtcV2.sensor_type` getter and setter to change the type of sensor used.

- ### [Thermocouple Bricklet 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermocouple_V2.html)
   - `BrickletThermocoupleV2()` takes an additional parameter to define the type of sensor. The options are of type `BrickletThermocoupleV2.SensorType`. The default is `BrickletPtc.SensorType.TYPE_K`.
   - `BrickletThermocoupleV2.sensor_type` getter and setter to change the type of sensor used.

- ### [Segment Display 4x7 Bricklet 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Segment_Display_4x7_V2.html)
   - `BrickletSegmentDisplay4x7V2.set_segments()` takes a `list`/`tuple` of 4 `int` instead of digit0, digit1, digit2, digit3. This is the same API as the older [Segment Display 4x7 Bricklet](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Segment_Display_4x7.html).

# Setup
There are currently no packages available at the PyPi repository. To install the module, clone the repository and run:
```bash
python3 -m venv env  # virtual environment, optional
source env/bin/activate  # only if the virtual environment is used
python3 setup.py install
```

## Versioning
I use [SemVer](http://semver.org/) for versioning. For the versions available, see the
[tags on this repository](../../tags).

The version is not stored in the source code. It is taken from the git tag by
[setuptools-scm](https://setuptools-scm.readthedocs.io/) when the package is built. To release a new version, publish a
GitHub release with a new tag, e.g. `1.9.0`. This builds the package as version 1.9.0 and uploads it to PyPI. Commits
after a tag get a development version like `1.9.1.dev3`.

For development, install the package in editable mode, which also generates `tinkerforge_async/_version.py`:
```bash
pip install -e .[dev]
```

## Authors
* **Patrick Baus** - *Initial work* - [PatrickBaus](https://github.com/PatrickBaus)

## License
This project is licensed under the GPL v3 license - see the
[LICENSE](LICENSE) file for details
