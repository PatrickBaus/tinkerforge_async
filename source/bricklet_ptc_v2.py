# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, unique

from .devices import DeviceIdentifier, BrickletWithMCU, device_factory, ThresholdOption
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetTemperatureCallbackConfiguration = namedtuple('TemperatureCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetResistanceCallbackConfiguration = namedtuple('ResistanceCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetMovingAverageConfiguration = namedtuple('MovingAverageConfiguration', ['moving_average_length_resistance', 'moving_average_length_temperature'])


@unique
class CallbackID(Enum):
    TEMPERATURE = 4
    RESISTANCE = 8
    SENSOR_CONNECTED = 18

@unique
class FunctionID(Enum):
    GET_TEMPERATURE = 1
    SET_TEMPERATURE_CALLBACK_CONFIGURATION = 2
    GET_TEMPERATURE_CALLBACK_CONFIGURATION = 3
    GET_RESISTANCE = 5
    SET_RESISTANCE_CALLBACK_CONFIGURATION = 6
    GET_RESISTANCE_CALLBACK_CONFIGURATION = 7
    SET_NOISE_REJECTION_FILTER = 9
    GET_NOISE_REJECTION_FILTER = 10
    IS_SENSOR_CONNECTED = 11
    SET_WIRE_MODE = 12
    GET_WIRE_MODE = 13
    SET_MOVING_AVERAGE_CONFIGURATION = 14
    GET_MOVING_AVERAGE_CONFIGURATION = 15
    SET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION = 16
    GET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION = 17

@unique
class LineFilter(Enum):
    FREQUENCY_50HZ = 0
    FREQUENCY_60HZ = 1

@unique
class WireMode(Enum):
    WIRE_2 = 2
    WIRE_3 = 3
    WIRE_4 = 4

class BrickletPtcV2(BrickletWithMCU):
    """
    Measures ambient temperature with 0.2 K accuracy
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletPtc_V2
    DEVICE_DISPLAY_NAME = 'PTC Bricklet 2.0'
    DEVICE_URL_PART = 'ptc_v2' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption
    LineFilter = LineFilter
    WireMode = WireMode

    CALLBACK_FORMATS = {
        CallbackID.TEMPERATURE: 'i',
        CallbackID.RESISTANCE: 'i',
        CallbackID.SENSOR_CONNECTED: '!',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        DeviceWithMCU.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_temperature(self):
        """
        Returns the temperature of the connected sensor. The value
        has a range of -246 to 849 °C and is given in °C/100,
        e.g. a value of 4223 means that a temperature of 42.23 °C is measured.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Temperature` callback. You can set the callback configuration
        with :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_TEMPERATURE,
            response_expected=True
        )
        return self.__value_to_SI(unpack_payload(payload, 'i'))

    async def set_temperature_callback_configuration(self, period=0, value_has_to_change=False, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
        """
        The period is the period with which the :cb:`Temperature` callback is triggered
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
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.
        """
        assert type(option) is ThresholdOption
        assert type(period) is int and period >= 0
        assert type(minimum) is int and minimum >= 0
        assert type(maximum) is int and maximum >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
              (
                period,
                bool(value_has_to_change),
                option.value.encode('ascii'),
                self.__SI_to_value(minimum),
                self.__SI_to_value(maximum)
              ), 'I ! c i i'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_temperature_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
            response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, 'I ! c i i')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_SI(minimum), self.__value_to_SI(maximum)
        return GetTemperatureCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def get_resistance(self):
        """
        Returns the value as measured by the MAX31865 precision delta-sigma ADC.

        The value can be converted with the following formulas:

        * Pt100:  resistance = (value * 390) / 32768
        * Pt1000: resistance = (value * 3900) / 32768


        If you want to get the value periodically, it is recommended to use the
        :cb:`Resistance` callback. You can set the callback configuration
        with :func:`Set Resistance Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RESISTANCE,
            response_expected=True
        )
        return unpack_payload(payload, 'i')

    async def set_resistance_callback_configuration(self, period=0, value_has_to_change=False, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
        """
        The period is the period with which the :cb:`Resistance` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Resistance` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.
        """
        assert type(option) is ThresholdOption
        assert type(period) is int and period >= 0
        assert type(minimum) is int and minimum >= 0
        assert type(maximum) is int and maximum >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RESISTANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
              (
                period,
                bool(value_has_to_change),
                option.value.encode('ascii'),
                minimum,
                maximum
              ), 'I ! c i i'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_temperature_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Resistance Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RESISTANCE_CALLBACK_CONFIGURATION,
            response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, 'I ! c i i')
        option = ThresholdOption(option)
        return GetTemperatureCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def set_noise_rejection_filter(self, line_filter=LineFilter.FREQUENCY_50HZ, response_expected=False):
        """
        Sets the noise rejection filter to either 50Hz (0) or 60Hz (1).
        Noise from 50Hz or 60Hz power sources (including
        harmonics of the AC power's fundamental frequency) is
        attenuated by 82dB.

        Default value is 0 = 50Hz.
        """
        assert type(line_filter) is LineFilter
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_NOISE_REJECTION_FILTER,
            data=pack_payload((line_filter.value,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_noise_rejection_filter(self):
        """
        Returns the noise rejection filter option as set by
        :func:`Set Noise Rejection Filter`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_NOISE_REJECTION_FILTER,
            response_expected=True
        )
        return LineFilter(unpack_payload(payload, 'B'))

    async def is_sensor_connected(self):
        """
        Returns *true* if the sensor is connected correctly.

        If this function
        returns *false*, there is either no Pt100 or Pt1000 sensor connected,
        the sensor is connected incorrectly or the sensor itself is faulty.

        If you want to get the status automatically, it is recommended to use the
        :cb:`Sensor Connected` callback. You can set the callback configuration
        with :func:`Set Sensor Connected Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.IS_SENSOR_CONNECTED,
            response_expected=True
        )
        return unpack_payload(payload, '!')

    async def set_wire_mode(self, mode=WireMode.WIRE_2, response_expected=False):
        """
        Sets the wire mode of the sensor. Possible values are 2, 3 and 4 which
        correspond to 2-, 3- and 4-wire sensors. The value has to match the jumper
        configuration on the Bricklet.

        The default value is 2 = 2-wire.
        """
        assert type(mode) is WireMode
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIRE_MODE,
            data=pack_payload((mode.value,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_wire_mode(self):
        """
        Returns the wire mode as set by :func:`Set Wire Mode`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_WIRE_MODE,
            response_expected=True
        )
        return WireMode(unpack_payload(payload, 'B'))

    async def set_moving_average_configuration(self, moving_average_length_resistance=1, moving_average_length_temperature=40, response_expected=False):
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the resistance and temperature.

        Setting the length to 1 will turn the averaging off. With less
        averaging, there is more noise on the data.

        The range for the averaging is 1-1000.

        New data is gathered every 20ms. With a moving average of length 1000 the resulting
        averaging window has a length of 20s. If you want to do long term measurements the longest
        moving average will give the cleanest results.

        The default value is 1 for resistance and 40 for temperature. The default values match
        the non-changeable averaging settings of the old PTC Bricklet 1.0
        """
        assert type(moving_average_length_humidity) is int and moving_average_length_humidity > 0
        assert type(moving_average_length_temperature) is int and moving_average_length_temperature > 0

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE_CONFIGURATION,
            data=pack_payload((moving_average_length_resistance,moving_average_length_temperature), 'H H'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_moving_average_configuration(self):
        """
        Returns the moving average configuration as set by :func:`Set Moving Average Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_MOVING_AVERAGE_CONFIGURATION,
            response_expected=True
        )

        return GetMovingAverageConfiguration(*unpack_payload(payload, 'H H'))

    async def set_sensor_connected_callback_configuration(self, enabled):
        """
        If you enable this callback, the :cb:`Sensor Connected` callback is triggered
        every time a Pt sensor is connected/disconnected.

        By default this callback is disabled.

        .. versionadded:: 2.0.2$nbsp;(Plugin)
        """
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), '!'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_sensor_connected_callback_configuration(self):
        """
        Returns the configuration as set by :func:`Set Sensor Connected Callback Configuration`.

        .. versionadded:: 2.0.2$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION,
            response_expected=True
        )
        return unpack_payload(payload, '!')

    def __value_to_SI(self, value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 100

    def __SI_to_value(self, value):
        return int(value * 100)

    def _process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = self.__value_to_SI(
                unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            )
            super()._process_callback(header, payload)

device_factory.register(BrickletPtcV2.DEVICE_IDENTIFIER, BrickletPtcV2)

