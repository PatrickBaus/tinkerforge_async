# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, IntEnum, unique

from .ip_connection import Device, IPConnectionAsync, Flags, UnknownFunctionError
from .ip_connection_helper import base58decode, pack_payload, unpack_payload

GetTemperatureCallbackThreshold = namedtuple('TemperatureCallbackThreshold', ['option', 'min', 'max'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletTemperature(Device):
    """
    Measures ambient temperature with 0.5°C accuracy
    """

    DEVICE_IDENTIFIER = 216
    DEVICE_DISPLAY_NAME = 'Temperature Bricklet'
    DEVICE_URL_PART = 'temperature' # internal

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
        set_debouce_period = 6
        get_debounce_period = 7
        set_i2c_mode = 10
        get_i2c_mode = 11
        get_identity = 255

    @unique
    class ThresholdOption(Enum):
        off = b'x'
        outside = b'o'
        inside = b'i'
        less_than = b'<'
        greater_than = b'>'

    @unique
    class I2cOption(IntEnum):
        fast = 0
        slow = 1

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
            function_id=BrickletTemperture.FunctionID.get_temperature,
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
        period = int(period)

        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperture.FunctionID.set_temperature_callback_period,
            data=pack_payload((int(period),), 'I'),
            response_expected = response_expected,
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.ok

    def get_temperature_callback_period(self):
        """
        Returns the period as set by :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperture.FunctionID.get_temperature_callback_period,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_temperature_callback_threshold(self, option, minimum, maximum, response_expected=True):
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
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperture.FunctionID.set_temperature_callback_threshold,
            data=pack_payload((option.value, int(minimum), int(maximum)), 'c h h'),
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
            function_id=BrickletTemperture.FunctionID.get_temperature_callback_threshold,
            response_expected=True
        )
        payload = unpack_payload(payload, 'c h h')
        payload[0] = BrickletTemperature.ThresholdOption(payload[0])
        return GetTemperatureCallbackThreshold(*payload)

    async def set_debounce_period(self, debounce_period, response_expected=True)):
        """
        Sets the period in ms with which the threshold callback

        * :cb:`Temperature Reached`

        is triggered, if the threshold

        * :func:`Set Temperature Callback Threshold`

        keeps being reached.

        The default value is 100.
        """
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.set_debounce_period,
            data=pack_payload((int(debounce_period),), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.get_debounce_period,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    def set_i2c_mode(self, mode=I2cOption.fast, response_expected=True):
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
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.set_i2c_mode,
            data=pack_payload(mode,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    def get_i2c_mode(self):
        """
        Returns the I2C mode as set by :func:`Set I2C Mode`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletTemperature.FunctionID.get_i2c_mode,
            response_expected=True
        )
        return I2cOption(unpack_payload(payload, 'B'))

    def get_identity(self):
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
            function_id=BrickletTemperature.FunctionID.get_identity,
            response_expected=True
        )
        payload = unpack_payload(payload, '8s 8s c 3B 3B H')
        payload[0] = base58decode(payload[0])
        payload[1] = base58decode(payload[1])
        return GetIdentity(*payload)

    def register_callback_queue(self, callback_id, queue):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if queue is None:
            self.registered_queues.pop(callback_id, None)
        else:
            self.registered_queues[callback_id] = queue

    def __value_to_SI(self, value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 100

    def process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = self.__value_to_SI(
                          unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
                      )
            super().process_callback(header, payload)

