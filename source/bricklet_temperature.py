# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, IntEnum, unique

from .devices import DeviceIdentifier, Device
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetTemperatureCallbackThreshold = namedtuple('TemperatureCallbackThreshold', ['option', 'minimum', 'maximum'])

@unique
class CallbackID(IntEnum):
    temperature = 8
    temperature_reached = 9

@unique
class FunctionID(IntEnum):
    get_temperature = 1
    set_temperature_callback_period = 2
    get_temperature_callback_period = 3
    set_temperature_callback_threshold = 4
    get_temperature_callback_threshold = 5
    set_debounce_period = 6
    get_debounce_period = 7
    set_i2c_mode = 10
    get_i2c_mode = 11

@unique
class ThresholdOption(Enum):
    off = 'x'
    outside = 'o'
    inside = 'i'
    less_than = '<'
    greater_than = '>'

@unique
class I2cOption(IntEnum):
  fast = 0
  slow = 1

class BrickletTemperature(Device):
    """
    Measures ambient temperature with 0.5 K accuracy
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletTemperature
    DEVICE_DISPLAY_NAME = 'Temperature Bricklet'
    DEVICE_URL_PART = 'temperature' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption
    I2cOption = I2cOption

    CALLBACK_FORMATS = {
        CallbackID.temperature: 'h',
        CallbackID.temperature_reached: 'h',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

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
            function_id=BrickletTemperature.FunctionID.get_temperature,
            response_expected=True
        )
        return self.__value_to_SI(unpack_payload(payload, 'h'))

    async def set_temperature_callback_period(self, period=0, response_expected=True):
        """
        Sets the period in ms with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Temperature` callback is only triggered if the temperature has changed
        since the last triggering.

        The default value is 0.
        """
        assert type(period) is int and period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.set_temperature_callback_period,
            data=pack_payload((period,), 'I'),
            response_expected = response_expected,
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.ok

    async def get_temperature_callback_period(self):
        """
        Returns the period as set by :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.get_temperature_callback_period,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_temperature_callback_threshold(self, option=ThresholdOption.off, minimum=0, maximum=0, response_expected=True):
        """
        Sets the thresholds for the :cb:`Temperature Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        assert type(option) is ThresholdOption
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.set_temperature_callback_threshold,
            data=pack_payload((option.value.encode(), self.__SI_to_value(minimum), self.__SI_to_value(maximum)), 'c h h'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_temperature_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.get_temperature_callback_threshold,
            response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, 'c h h')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_SI(minimum), self.__value_to_SI(maximum)
        return GetTemperatureCallbackThreshold(option, minimum, maximum)

    async def set_debounce_period(self, debounce_period=100, response_expected=True):
        """
        Sets the period in ms with which the threshold callback

        * :cb:`Temperature Reached`

        is triggered, if the threshold

        * :func:`Set Temperature Callback Threshold`

        keeps being reached.

        The default value is 100.
        """
        assert type(debounce_period) is int and debounce_period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.set_debounce_period,
            data=pack_payload((debounce_period,), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.get_debounce_period,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_i2c_mode(self, mode=I2cOption.fast, response_expected=False):
        """
        Sets the I2C mode. Possible modes are:

        * 0: Fast (400kHz, default)
        * 1: Slow (100kHz)

        If you have problems with obvious outliers in the
        Temperature Bricklet measurements, they may be caused by EMI issues.
        In this case it may be helpful to lower the I2C speed.

        It is however not recommended to lower the I2C speed in applications where
        a high throughput needs to be achieved.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        assert type(mode) is BrickletTemperature.I2cOption
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.set_i2c_mode,
            data=pack_payload((mode.value,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_i2c_mode(self):
        """
        Returns the I2C mode as set by :func:`Set I2C Mode`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.get_i2c_mode,
            response_expected=True
        )
        return BrickletTemperature.I2cOption(unpack_payload(payload, 'B'))

    def register_event_queue(self, event_id, queue):
        """
        Registers the given *function* with the given *callback_id*.
        """
        assert type(event_id) is BrickletTemperature.CallbackID
        super().register_event_queue(event_id, queue)

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

