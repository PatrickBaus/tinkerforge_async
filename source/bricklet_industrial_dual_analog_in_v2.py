# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, unique

from .devices import DeviceIdentifier, BrickletWithMCU, device_factory, ThresholdOption
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetVoltageCallbackConfiguration = namedtuple('VoltageCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetCalibration = namedtuple('Calibration', ['offset', 'gain'])
GetChannelLEDStatusConfig = namedtuple('ChannelLEDStatusConfig', ['min', 'max', 'config'])

@unique
class CallbackID(Enum):
    VOLTAGE = 4

@unique
class FunctionID(Enum):
    GET_GET_VOLTAGE = 1
    SET_SET_VOLTAGE_CALLBACK_CONFIGURATION = 2
    GET_GET_VOLTAGE_CALLBACK_CONFIGURATION = 3
    SET_SET_SAMPLE_RATE = 5
    GET_GET_SAMPLE_RATE = 6
    SET_CALIBRATION = 7
    GET_CALIBRATION = 8
    GET_ADC_VALUES = 9
    SET_CHANNEL_LED_CONFIG = 10
    GET_CHANNEL_LED_CONFIG = 11
    SET_CHANNEL_LED_STATUS_CONFIG = 12
    GET_CHANNEL_LED_STATUS_CONFIG = 13

@unique
class ChannelLedConfig(Enum):
    OFF = 0
    ON = 1
    HEARTBEAT = 2
    CHANNEL_STATUS = 3

@unique
class ChannelLedStatusConfig(Enum):
    THRESHOLD = 0
    INTENSITY = 1


class BrickletIndustrialDualAnalogInV2(BrickletWithMCU):
    """
    Measures two DC voltages between -35V and +35V with 24bit resolution each
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletIndustrialDualAnalogIn_V2
    DEVICE_DISPLAY_NAME = 'Industrial Dual Analog In Bricklet 2.0'
    DEVICE_URL_PART = 'industrial_dual_analog_in_v2' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption
    ChannelLedConfig = ChannelLedConfig
    ChannelLedStatusConfig = ChannelLedStatusConfig

    CALLBACK_FORMATS = {
        CallbackID.VOLTAGE: 'B i',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        DeviceWithMCU.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_voltage(self, channel):
        """
        Returns the voltage for the given channel.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Voltage` callback. You can set the callback configuration
        with :func:`Set Voltage Callback Configuration`.
        """
        assert isinstance(channel, int) and (0 <= channel <= 1)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_VOLTAGE,
            data=pack_payload((channel,), 'B'),
            response_expected=True
        )
        return unpack_payload(payload, 'i')

    async def set_voltage_callback_configuration(self, channel, period=0, value_has_to_change=False, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
        """
        The period is the period with which the :cb:`Voltage` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Voltage` callback.

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
        assert isinstance(channel, int) and (0<= channel <= 1)
        assert type(option) is ThresholdOption
        assert isinstance(period, int) and period >= 0
        assert isinstance(minimum, int) and minimum >= 0
        assert isinstance(maximum, int) and maximum >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
              (
                channel,
                period,
                bool(value_has_to_change),
                option.value.encode('ascii'),
                minimum,
                maximum
              ), 'B I ! c i i'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_voltage_callback_configuration(self, channel):
        """
        Returns the callback configuration as set by :func:`Set Voltage Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload((channel,), 'B'),
            response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, 'I ! c i i')
        option = ThresholdOption(option)
        return GetVoltageCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def set_sample_rate(self, rate, response_expected=False):
        """
        Sets the sample rate. The sample rate can be between 1 sample per second
        and 976 samples per second. Decreasing the sample rate will also decrease the
        noise on the data.
        """
        assert isinstance(rate, int) and (1<= rate <= 976)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SAMPLE_RATE,
            data=pack_payload((channel,), 'B'),
            response_expected=response_expected
        )

    async def get_sample_rate(self):
        """
        Returns the sample rate as set by :func:`Set Sample Rate`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SAMPLE_RATE,
            response_expected=True
        )

        return unpack_payload(payload, 'B')

    async def set_calibration(self, offset, gain, response_expected=False):
        """
        Sets offset and gain of MCP3911 internal calibration registers.

        See MCP3911 datasheet 7.7 and 7.8. The Industrial Dual Analog In Bricklet 2.0
        is already factory calibrated by Tinkerforge. It should not be necessary
        for you to use this function
        """
        offset = list(map(int, offset))
        gain = list(map(int, gain))
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload((offset, gain), '2i 2i'),
            response_expected=response_expected
        )

    async def get_calibration(self):
        """
        Returns the calibration as set by :func:`Set Calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CALIBRATION,
            response_expected=True
        )

        return GetCalibration(*unpack_payload(payload, '2i 2i'))

    async def get_adc_values(self):
        """
        Returns the ADC values as given by the MCP3911 IC. This function
        is needed for proper calibration, see :func:`Set Calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ADC_VALUES,
            response_expected=True
        )

        return unpack_payload(payload, '2i')

    async def set_channel_led_config(self, channel, config, response_expected=False):
        """
        Each channel has a corresponding LED. You can turn the LED off, on or show a
        heartbeat. You can also set the LED to "Channel Status". In this mode the
        LED can either be turned on with a pre-defined threshold or the intensity
        of the LED can change with the measured value.

        You can configure the channel status behavior with :func:`Set Channel LED Status Config`.

        By default all channel LEDs are configured as "Channel Status".
        """
        assert isinstance(channel, int) and (0<= channel <= 1)
        assert type(config) is ChannelLedConfig
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_CONFIG,
            data=pack_payload((channel, config.value), 'B B'),
            response_expected=response_expected
        )

    async def get_channel_led_config(self, channel):
        """
        Returns the ADC values as given by the MCP3911 IC. This function
        is needed for proper calibration, see :func:`Set Calibration`.
        """
        assert isinstance(channel, int) and (0<= channel <= 1)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_CONFIG,
            data=pack_payload((channel,), 'B'),
            response_expected=True
        )

        return ChannelLedConfig(unpack_payload(payload, 'B'))

    async def set_channel_led_status_config(self, channel, minimum, maximum, response_expected=False):
        """
        Sets the channel LED status config. This config is used if the channel LED is
        configured as "Channel Status", see :func:`Set Channel LED Config`.

        For each channel you can choose between threshold and intensity mode.

        In threshold mode you can define a positive or a negative threshold.
        For a positive threshold set the "min" parameter to the threshold value in mV
        above which the LED should turn on and set the "max" parameter to 0. Example:
        If you set a positive threshold of 10V, the LED will turn on as soon as the
        voltage exceeds 10V and turn off again if it goes below 10V.
        For a negative threshold set the "max" parameter to the threshold value in mV
        below which the LED should turn on and set the "min" parameter to 0. Example:
        If you set a negative threshold of 10V, the LED will turn on as soon as the
        voltage goes below 10V and the LED will turn off when the voltage exceeds 10V.

        In intensity mode you can define a range in mV that is used to scale the brightness
        of the LED. Example with min=4V, max=20V: The LED is off at 4V, on at 20V
        and the brightness is linearly scaled between the values 4V and 20V. If the
        min value is greater than the max value, the LED brightness is scaled the other
        way around.
        """
        assert isinstance(channel, int) and (0<= channel <= 1)
        assert isinstance(minimum, int)
        assert isinstance(maximum, int)
        assert type(config) is ChannelLedStatusConfig
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CHANNEL_LED_STATUS_CONFIG,
            data=pack_payload((channel, minimum, maximum, config.value), 'B i i B'),
            response_expected=response_expected
        )

    async def get_channel_led_status_config(self, channel):
        """
        Returns the channel LED status configuration as set by
        :func:`Set Channel LED Status Config`.
        """
        assert isinstance(channel, int) and (0<= channel <= 1)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHANNEL_LED_STATUS_CONFIG,
            data=pack_payload((channel,), 'B'),
            response_expected=True
        )

        minimum, maximum, config = ChannelLedConfig(unpack_payload(payload, 'i i B'))
        config = ChannelLedStatusConfig(config)
        return GetChannelLEDStatusConfig(minimum, maximum, config)

    def __SI_to_value(self, value):
        return int(value * 100)

    def _process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            super()._process_callback(header, payload)

device_factory.register(BrickletIndustrialDualAnalogInV2.DEVICE_IDENTIFIER, BrickletIndustrialDualAnalogInV2)

