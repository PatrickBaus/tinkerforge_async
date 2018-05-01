# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, IntEnum, unique

from .devices import DeviceIdentifier
from .ip_connection import Device, IPConnectionAsync, Flags, UnknownFunctionError#, Error, create_char, create_char_list, create_string, create_chunk_data
from .ip_connection_helper import base58decode, pack_payload, unpack_payload

GetHumidityCallbackThreshold = namedtuple('HumidityCallbackThreshold', ['option', 'minimum', 'maximum'])
GetAnalogValueCallbackThreshold = namedtuple('AnalogValueCallbackThreshold', ['option', 'minimum', 'maximum'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

@unique
class CallbackID(IntEnum):
    humidity = 13
    analog_value = 14
    humidity_reached = 15
    analog_value_reached = 16

@unique
class FunctionID(IntEnum):
    get_humidity = 1
    get_analog_value = 2
    set_humidity_callback_period = 3
    get_humidity_callback_period = 4
    set_analog_value_callback_period = 5
    get_analog_value_callback_period = 6
    set_humidity_callback_threshold = 7
    get_humidity_callback_threshold = 8
    set_analog_value_callback_threshold = 9
    get_analog_value_callback_threshold = 10
    set_debounce_period = 11
    get_debounce_period = 12
    get_identity = 255

@unique
class ThresholdOption(Enum):
    off = 'x'
    outside = 'o'
    inside = 'i'
    less_than = '<'
    greater_than = '>'

class BrickletHumidity(Device):
    """
    Measures relative humidity
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletHumidity
    DEVICE_DISPLAY_NAME = 'Humidity Bricklet'
    DEVICE_URL_PART = 'humidity' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption

    CALLBACK_FORMATS = {
        CallbackID.humidity: 'H',
        CallbackID.analog_value: 'H',
        CallbackID.humidity_reached: 'H',
        CallbackID.analog_value_reached: 'H',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 1)

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
            function_id=BrickletHumidity.FunctionID.get_humidity,
            response_expected=True
        )
        return self.__value_to_SI(unpack_payload(payload, 'H'))

    async def get_analog_value(self):
        """
        Returns the value as read by a 12-bit analog-to-digital converter.
        The value is between 0 and 4095.

        .. note::
         The value returned by :func:`Get Humidity` is averaged over several samples
         to yield less noise, while :func:`Get Analog Value` gives back raw
         unfiltered analog values. The returned humidity value is calibrated for
         room temperatures, if you use the sensor in extreme cold or extreme
         warm environments, you might want to calculate the humidity from
         the analog value yourself. See the `HIH 5030 datasheet
         <https://github.com/Tinkerforge/humidity-bricklet/raw/master/datasheets/hih-5030.pdf>`__.

        If you want the analog value periodically, it is recommended to use the
        :cb:`Analog Value` callback and set the period with
        :func:`Set Analog Value Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.get_analog_value,
            response_expected=True
        )
        return unpack_payload(payload, 'H')

    async def set_humidity_callback_period(self, period=0, response_expected=True):
        """
        Sets the period in ms with which the :cb:`Humidity` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Humidity` callback is only triggered if the humidity has changed
        since the last triggering.

        The default value is 0.
        """
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.set_humidity_callback_period,
            data=pack_payload((int(period),), 'I'),
            response_expected = response_expected,
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.ok

    async def get_humidity_callback_period(self):
        """
        Returns the period as set by :func:`Set Humidity Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.get_humidity_callback_period,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_analog_value_callback_period(self, period=0, response_expected=True):
        """
        Sets the period in ms with which the :cb:`Analog Value` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Analog Value` callback is only triggered if the analog value has
        changed since the last triggering.

        The default value is 0.
        """
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.set_analog_value_callback_period,
            data=pack_payload((int(period),), 'I'),
            response_expected = response_expected,
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_analog_value_callback_period(self):
        """
        Returns the period as set by :func:`Set Analog Value Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.get_analog_value_callback_period,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_humidity_callback_threshold(self, option=ThresholdOption.off, minimum=0, maximum=0, response_expected=True):
        """
        Sets the thresholds for the :cb:`Humidity Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the humidity is *outside* the min and max values"
         "'i'",    "Callback is triggered when the humidity is *inside* the min and max values"
         "'<'",    "Callback is triggered when the humidity is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the humidity is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        assert type(option) is ThresholdOption
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.set_humidity_callback_threshold,
            data=pack_payload((option.value.encode(), self.__SI_to_value(minimum), self.__SI_to_value(maximum)), 'c H H'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_humidity_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Humidity Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.get_humidity_callback_threshold,
            response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, 'c h h')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_SI(minimum), self.__value_to_SI(maximum)
        return GetHumidityCallbackThreshold(option, minimum, maximum)

    async def set_analog_value_callback_threshold(self, option=ThresholdOption.off, minimum=0, maximum=0, response_expected=True):
        """
        Sets the thresholds for the :cb:`Analog Value Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the analog value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the analog value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the analog value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the analog value is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        assert type(option) is ThresholdOption
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.set_analog_value_callback_threshold,
            data=pack_payload((option.value.encode(), int(minimum), int(maximum)), 'c H H'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_analog_value_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Analog Value Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.get_analog_value_callback_threshold,
            response_expected=True
        )
        payload = unpack_payload(payload, 'c H H')
        payload[0] = ThresholdOption(payload[0])
        return GetAnalogValueCallbackThreshold(*payload)

    async def set_debounce_period(self, debounce_period=100, response_expected=True):
        """
        Sets the period in ms with which the threshold callbacks

        * :cb:`Humidity Reached`,
        * :cb:`Analog Value Reached`

        are triggered, if the thresholds

        * :func:`Set Humidity Callback Threshold`,
        * :func:`Set Analog Value Callback Threshold`

        keep being reached.

        The default value is 100.
        """
        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletHumidity.FunctionID.set_debounce_period,
            data=pack_payload((int(debounce_period),), 'I'),
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
            function_id=BrickletHumidity.FunctionID.get_debounce_period,
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
            function_id=BrickletHumidity.FunctionID.get_identity,
            response_expected=True
        )
        uid, connected_uid, position, hw_version, fw_version, device_id = unpack_payload(payload, '8s 8s c 3B 3B H')
        uid, connected_uid = base58decode(uid), base58decode(connected_uid)
        device_id = DeviceIdentifier(device_id)
        return GetIdentity(uid, connected_uid, position, hw_version, fw_version, device_id)

    def register_event_queue(self, event_id, queue):
        """
        Registers the given *function* with the given *callback_id*.
        """
        assert type(event_id) is BrickletHumidity.CallbackID
        super().register_event_queue(event_id, queue)

    def __value_to_SI(self, value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 10

    def __SI_to_value(self, value):
        return int(value * 10)

    def process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            if header['function_id'] in (BrickletHumidity.CallbackID.humidity, BrickletHumidity.CallbackID.humidity_reached):
                payload = self.__value_to_SI(payload)
            super().process_callback(header, payload)
