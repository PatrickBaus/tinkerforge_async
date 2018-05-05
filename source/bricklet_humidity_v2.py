# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, IntEnum, unique

from .devices import DeviceIdentifier
from .ip_connection import Device, IPConnectionAsync, Flags, UnknownFunctionError
from .ip_connection_helper import base58decode, pack_payload, unpack_payload
from .brick_master import BrickletPort

GetHumidityCallbackConfiguration = namedtuple('HumidityCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetTemperatureCallbackConfiguration = namedtuple('TemperatureCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetMovingAverageConfiguration = namedtuple('MovingAverageConfiguration', ['moving_average_length_humidity', 'moving_average_length_temperature'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

@unique
class CallbackID(IntEnum):
    humidity = 4
    temperature = 8

@unique
class FunctionID(IntEnum):
    get_humidity = 1
    set_humidity_callback_configuraton = 2
    get_humidity_callback_configuraton = 3
    get_temperature = 5
    set_temperature_callback_configuraton = 6
    get_temperature_callback_configuraton = 7
    set_heater_configuration = 9
    get_heater_configuration = 10
    set_moving_average_configuration = 11
    get_moving_average_configuration = 12
    get_spitfp_error_count = 234
    set_bootloader_mode = 235
    get_bootloader_mode = 236
    set_write_firmware_pointer = 237
    write_firmare = 238
    set_status_led_config = 239
    get_status_led_config = 240
    get_chip_temperature = 242
    reset = 243
    write_uid = 248
    read_uid = 249
    get_identity = 255

@unique
class ThresholdOption(Enum):
    off = 'x'
    outside = 'o'
    inside = 'i'
    less_than = '<'
    greater_than = '>'

@unique
class HeaterConfig(IntEnum):
    disabled = 0
    enabled = 1

@unique
class BootloaderMode(IntEnum):
    bootloader = 0
    firmware = 1
    bootloader_wait_for_reboot = 2
    firmware_wait_for_reboot = 3
    firmware_wait_for_erase_and_reboot = 4

@unique
class BootloaderStatus(IntEnum):
    ok = 0
    invalid_mode = 1
    no_change = 2
    entry_function_not_present = 3
    device_identifier_incorrect = 4
    crc_mismatch = 5

@unique
class LedConfig(IntEnum):
    off = 0
    on = 1
    show_heartbeat = 2
    show_status = 3

class BrickletHumidityV2(Device):
    """
    Measures relative humidity
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletHumidityV2
    DEVICE_DISPLAY_NAME = 'Humidity Bricklet 2.0'
    DEVICE_URL_PART = 'humidity_v2' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption
    HeaterConfig = HeaterConfig
    BootloaderMode = BootloaderMode
    BootloaderStatus = BootloaderStatus
    LedConfig = LedConfig

    CALLBACK_FORMATS = {
        CallbackID.humidity: 'H',
        CallbackID.temperature: 'h',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_humidity(self):
        """
        Returns the humidity of the sensor. The value
        has a range of 0 to 1000 and is given in %RH/10 (Relative Humidity),
        i.e. a value of 421 means that a humidity of 42.1 %RH is measured.

        If you want to get the humidity periodically, it is recommended to use the
        :cb:`Humidity` callback and set the period with
        :func:`Set Humidity Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_humidity,
            response_expected=True
        )
        return self.__humidity_sensor_to_SI(unpack_payload(payload, 'H'))

    async def set_humidity_callback_configuration(self, period=0, value_has_to_change=False, option=ThresholdOption.off, minimum=0, maximum=0, response_expected=True):
        """
        The period in ms is the period with which the :cb:`Humidity` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Humidity` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"


        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        assert type(option) is ThresholdOption
        assert type(period) is int and period >= 0
        assert type(minimum) is int and minimum >= 0
        assert type(maximum) is int and maximum >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.set_humidity_callback_configuraton,
            data=pack_payload(
              (
                period,
                bool(value_has_to_change),
                option.value.encode(),
                self.__SI_to_humidity_sensor(minimum),
                self.__SI_to_humidity_sensor(maximum)
              ), 'I ! c H H'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_humidity_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Humidity Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_humidity_callback_configuraton,
            response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, 'I ! c H H')
        option = ThresholdOption(option)
        minimum, maximum = self.__humidity_sensor_to_SI(minimum), self.__humidity_sensor_to_SI(maximum)
        return GetHumidityCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def get_temperature(self):
        """
        Returns the temperature measured by the sensor. The value
        has a range of -4000 to 16500 and is given in °C/100,
        i.e. a value of 3200 means that a temperature of 32.00 °C is measured.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Temperature` callback. You can set the callback configuration
        with :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_temperature,
            response_expected=True
        )
        return self.__temperature_sensor_to_SI(unpack_payload(payload, 'h'))

    async def set_temperature_callback_configuration(self, period=0, value_has_to_change=False, option=ThresholdOption.off, minimum=0, maximum=0, response_expected=True):
        """
        The period in ms is the period with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Temperature` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"


        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        assert type(option) is ThresholdOption
        assert type(period) is int and period >= 0
        assert type(minimum) is int and minimum >= 0
        assert type(maximum) is int and maximum >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.set_temperature_callback_configuraton,
            data=pack_payload(
              (
                period,
                bool(value_has_to_change),
                option.value.encode(),
                self.__SI_to_temperature_sensor(minimum),
                self.__SI_to_temperature_sensor(maximum)
              ), 'I ! c H H'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_temperature_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_temperature_callback_configuraton,
            response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, 'I ! c H H')
        option = ThresholdOption(option)
        minimum, maximum = self.__temperature_sensor_to_SI(minimum), self.__temperature_sensor_to_SI(maximum)
        return GetTemperatureCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def set_heater_configuration(self, heater_config=HeaterConfig.disabled, response_expected=False):
        """
        Enables/disables the heater. The heater can be used to dry the sensor in
        extremely wet conditions.

        By default the heater is disabled.
        """
        assert type(heater_config) is HeaterConfig

        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.set_heater_configuration,
            data=pack_payload((heater_config.value,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_heater_configuration(self):
        """
        Returns the heater configuration as set by :func:`Set Heater Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_heater_configuration,
            response_expected=True
        )

        return HeaterConfig(unpack_payload(payload, 'B'))

    async def set_moving_average_configuration(self, moving_average_length_humidity=100, moving_average_length_temperature=100, response_expected=False):
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the humidity and temperature.

        Setting the length to 1 will turn the averaging off. With less
        averaging, there is more noise on the data.

        The range for the averaging is 1-1000.

        New data is gathered every 50ms. With a moving average of length 1000 the resulting
        averaging window has a length of 50s. If you want to do long term measurements the longest
        moving average will give the cleanest results.

        The default value is 100.
        """
        assert type(moving_average_length_humidity) is int and moving_average_length_humidity > 0
        assert type(moving_average_length_temperature) is int and moving_average_length_temperature > 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.set_moving_average_configuration,
            data=pack_payload((moving_average_length_humidity,moving_average_length_temperature), 'H H'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_moving_average_configuration(self):
        """
        Returns the moving average configuration as set by :func:`Set Moving Average Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_moving_average_configuration,
            response_expected=True
        )

        return GetMovingAverageConfiguration(*unpack_payload(payload, 'H H'))

    async def get_spitfp_error_count(self):
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ack checksum errors,
        * message checksum errors,
        * frameing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Bricklet side. All
        Bricks have a similar function that returns the errors on the Brick side.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_spitfp_error_count,
            response_expected=True
        )

        return GetSPITFPErrorCount(*unpack_payload(payload, 'I I I I'))

    async def set_bootloader_mode(self, mode):
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier und crc are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        assert type(mode) is BootloaderMode

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.set_bootloader_mode,
            data=pack_payload((mode.value,), 'B'),
            response_expected=True
        )
        return BootloaderStatus(unpack_payload(payload, 'B'))

    async def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_bootloader_mode,
            response_expected=True
        )
        return BootloaderMode(unpack_payload(payload, 'B'))

    async def set_write_firmware_pointer(self, pointer, response_expected=False):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        assert type(pointer) is int and pointer >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.set_write_firmware_pointer,
            data=pack_payload((pointer,), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def write_firmware(self, data):
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.write_firmware,
            data=pack_payload((list(map(int, data)),), '64B'),
            response_expected=True
        )
        return unpack_payload(payload, 'B')

    async def set_status_led_config(self, config=LedConfig.show_status, response_expected=False):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        assert type(config) is LedConfig

        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.set_status_led_config,
            data=pack_payload((config.value,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_status_led_config,
            response_expected=True
        )
        return LedConfig(unpack_payload(payload, 'B'))

    async def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_chip_temperature,
            response_expected=True
        )
        return unpack_payload(payload, 'h')

    async def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.reset,
            response_expected=False
        )

    async def write_uid(self, uid, response_expected=False):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        assert type(uid) is int and uid >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.write_uid,
            data=pack_payload((uid,), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.read_uid,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_identity,
            response_expected=True
        )
        uid, connected_uid, position, hw_version, fw_version, device_id = unpack_payload(payload, '8s 8s c 3B 3B H')
        return GetIdentity(
            base58decode(uid),
            base58decode(connected_uid),
            BrickletPort(position),
            hw_version,
            fw_version,
            DeviceIdentifier(device_id)
        )

    def register_event_queue(self, event_id, queue):
        """
        Registers the given *function* with the given *callback_id*.
        """
        assert type(event_id) is BrickletHumidityV2.CallbackID
        super().register_event_queue(event_id, queue)

    def __humidity_sensor_to_SI(self, value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 100

    def __SI_to_humidity_sensor(self, value):
        return int(value * 100)

    def __temperature_sensor_to_SI(self, value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 100

    def __SI_to_temperature_sensor(self, value):
        return int(value * 100)

    def process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            if header['function_id'] is BrickletHumidityV2.CallbackID.humidity:
                payload = self.__humidity_sensor_to_SI(payload)
            super().process_callback(header, payload)
