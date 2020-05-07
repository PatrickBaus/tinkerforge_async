# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, IntEnum, unique

from .devices import DeviceIdentifier, DeviceWithMCU
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetHumidityCallbackConfiguration = namedtuple('HumidityCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'minimum', 'maximum'])
GetTemperatureCallbackConfiguration = namedtuple('TemperatureCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'minimum', 'maximum'])
GetMovingAverageConfiguration = namedtuple('MovingAverageConfiguration', ['moving_average_length_humidity', 'moving_average_length_temperature'])

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
    set_samples_per_second = 13
    get_samples_per_second = 14

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
class SamplesPerSecond(IntEnum):
    sps20 = 0
    sps10 = 1
    sps5  = 2
    sps1  = 3
    sps02 = 4
    sps01 = 5

class BrickletHumidityV2(DeviceWithMCU):
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
    SamplesPerSecond = SamplesPerSecond

    CALLBACK_FORMATS = {
        CallbackID.humidity: 'H',
        CallbackID.temperature: 'h',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        DeviceWithMCU.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 2)

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

    async def set_moving_average_configuration(self, moving_average_length_humidity=5, moving_average_length_temperature=5, response_expected=False):
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the humidity and temperature.

        Setting the length to 1 will turn the averaging off. With less
        averaging, there is more noise on the data.

        The range for the averaging is 1-1000.

        New data is gathered every 50ms. With a moving average of length 1000 the resulting
        averaging window has a length of 50s. If you want to do long term measurements the longest
        moving average will give the cleanest results.

        * In firmware version 2.0.3 we added the set_samples_per_second() function. It configures
        the measurement frequency. Since high frequencies can result in self-heating of th IC,
        changed the default value from 20 samples per second to 1. With 1 sample per second a
         moving average length of 1000 would result in an averaging window of 1000 seconds!

        The default value is 5.
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

    async def set_samples_per_second(self, sps=SamplesPerSecond.sps1, response_expected=False):
        """
        Sets the samples per second that are gathered by the humidity/temperature sensor HDC1080.
        We added this function since we found out that a high measurement frequency can lead to
        self-heating of the sensor. Which can distort the temperature measurement.
        If you don't need a lot of measurements, you can use the lowest available measurement
        frequency of 0.1 samples per second for the least amount of self-heating.

        Before version 2.0.3 the default was 20 samples per second. The new default is 1 sample per second.
        """
        assert type(sps) is SamplesPerSecond

        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.set_samples_per_second,
            data=pack_payload((sps,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_samples_per_second(self):
        """
        Sets the samples per second that are gathered by the humidity/temperature sensor HDC1080.
        We added this function since we found out that a high measurement frequency can lead to
        self-heating of the sensor. Which can distort the temperature measurement.
        If you don't need a lot of measurements, you can use the lowest available measurement
        frequency of 0.1 samples per second for the least amount of self-heating.

        Before version 2.0.3 the default was 20 samples per second. The new default is 1 sample per second.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidityV2.FunctionID.get_samples_per_second,
            response_expected=True
        )

        return SamplesPerSecond(unpack_payload(payload, 'B'))

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

    def _process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            if header['function_id'] is BrickletHumidityV2.CallbackID.humidity:
                payload = self.__humidity_sensor_to_SI(payload)
            elif header['function_id'] is BrickletHumidityV2.CallbackID.temperature:
                payload = self.__temperature_sensor_to_SI(payload)
            super()._process_callback(header, payload)
