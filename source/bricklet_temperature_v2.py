# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, IntEnum, unique

from .devices import DeviceIdentifier, DeviceWithMCU
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetTemperatureCallbackConfiguration = namedtuple('TemperatureCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'minimum', 'maximum'])

@unique
class CallbackID(IntEnum):
    temperature = 4

@unique
class FunctionID(IntEnum):
    get_temperature = 1
    set_temperature_callback_configuraton = 2
    get_temperature_callback_configuraton = 3
    set_heater_configuration = 5
    get_heater_configuration = 6

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

class BrickletTemperatureV2(DeviceWithMCU):
    """
    Measures ambient temperature with 0.2 K accuracy
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletTemperatureV2
    DEVICE_DISPLAY_NAME = 'Temperature Bricklet 2.0'
    DEVICE_URL_PART = 'temperature_v2' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption
    HeaterConfig = HeaterConfig

    CALLBACK_FORMATS = {
        CallbackID.temperature: 'h',
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
        Returns the temperature of the sensor. The value
        has a range of -2500 to 8500 and is given in °C/100,
        e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

        If you want to get the temperature periodically, it is recommended
        to use the :cb:`Temperature` callback and set the period with
        :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperatureV2.FunctionID.get_temperature,
            response_expected=True
        )
        return self.__value_to_SI(unpack_payload(payload, 'h'))

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
            function_id=BrickletTemperatureV2.FunctionID.set_temperature_callback_configuraton,
            data=pack_payload(
              (
                period,
                bool(value_has_to_change),
                option.value.encode(),
                self.__SI_to_value(minimum),
                self.__SI_to_value(maximum)
              ), 'I ! c h h'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.ok

    async def get_temperature_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperatureV2.FunctionID.get_temperature_callback_configuraton,
            response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, 'I ! c h h')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_SI(minimum), self.__value_to_SI(maximum)
        return GetTemperatureCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def set_heater_configuration(self, heater_config=HeaterConfig.disabled, response_expected=False):
        """
        Enables/disables the heater. The heater can be used to test the sensor.
        """
        assert type(heater_config) is HeaterConfig

        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperatureV2.FunctionID.set_heater_configuration,
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
            function_id=BrickletTemperatureV2.FunctionID.get_heater_configuration,
            response_expected=True
        )

        return HeaterConfig(unpack_payload(payload, 'B'))

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
