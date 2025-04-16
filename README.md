[![pylint](../../actions/workflows/pylint.yml/badge.svg)](../../actions/workflows/pylint.yml)
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
|Brick|Supported|Tested|Comments|
|--|--|--|--|
|[Master](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html)|:heavy_check_mark:|:heavy_check_mark:|  |

| Bricklet                                                                                                                 |Supported|Tested|
|--------------------------------------------------------------------------------------------------------------------------|--|--|
| [Ambient Light 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V2.html)                         |:heavy_check_mark:|:heavy_check_mark:|
| [Ambient Light 3.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V3.html)                         |:heavy_check_mark:|:heavy_check_mark:|
| [Analog In](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Analog_In.html)                                        |:heavy_check_mark:|:heavy_check_mark:|
| [Barometer](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Barometer.html)                                        |:heavy_check_mark:|:heavy_check_mark:|
| [Barometer 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Barometer_V2.html)                                 |:heavy_check_mark:|:heavy_check_mark:|
| [Humidity](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Humidity.html)                                          |:heavy_check_mark:|:heavy_check_mark:|
| [Humidity 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Humidity_V2.html)                                   |:heavy_check_mark:|:heavy_check_mark:|
| [Industrial Dual Analog In 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_Dual_Analog_In_V2.html) |:heavy_check_mark:|:heavy_check_mark:|
| [Industrial PTC](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Industrial_PTC.html)                              |:heavy_check_mark:|:heavy_check_mark:|
| [IO-4 2.0](https://www.tinkerforge.com/de/doc/Hardware/Bricklets/IO4_V2.html)                                            |:heavy_check_mark:|:heavy_check_mark:|
| [IO-16](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/IO16.html)                                                 |:heavy_check_mark:|:heavy_check_mark:|
| [Isolator](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Isolator.html)                                          |:heavy_check_mark:|:heavy_check_mark:|
| [Moisture](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Moisture.html)                                          |:heavy_check_mark:|:heavy_check_mark:|
| [Motion Detector 2.0](https://www.tinkerforge.com/de/doc/Hardware/Bricklets/Motion_Detector_V2.html)                     |:heavy_check_mark:|:heavy_check_mark:|
| [PTC](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/PTC.html)                                                    |:heavy_check_mark:|:heavy_check_mark:|
| [PTC 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/PTC_V2.html)                                             |:heavy_check_mark:|:heavy_check_mark:|
| [RS232 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/RS232_V2.html)                                         |:heavy_check_mark:|:heavy_check_mark:|
| [Segment Display 4x7](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Segment_Display_4x7.html)                    |:heavy_check_mark:|:heavy_check_mark:|
| [Segment Display 4x7 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Segment_Display_4x7_V2.html)             |:heavy_check_mark:|:heavy_check_mark:|
| [Temperature](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature.html)                                    |:heavy_check_mark:|:heavy_check_mark:|
| [Temperature 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature_V2.html)                             |:heavy_check_mark:|:heavy_check_mark:|
| [Thermocouple 2.0](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermocouple_V2.html)                           |:heavy_check_mark:|:heavy_check_mark:|

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
       1000, response_expected=True
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
 - If physical quantities are measured we will now return standard SI units, not some unexpected stuff like centi °C (Temperature Bricklet). To preserve the precision the Decimal package is used. The only exception to this rule is the use of °C for temperature. This is for convenience.
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

## Authors
* **Patrick Baus** - *Initial work* - [PatrickBaus](https://github.com/PatrickBaus)

## License
This project is licensed under the GPL v3 license - see the
[LICENSE](LICENSE) file for details
