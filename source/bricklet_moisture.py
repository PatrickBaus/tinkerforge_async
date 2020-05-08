# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, IntEnum, unique

from .devices import DeviceIdentifier, Device
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetMoistureCallbackThreshold = namedtuple('MoistureCallbackThreshold', ['option', 'minimum', 'maximum'])

@unique
class CallbackID(IntEnum):
    moisture = 8
    moisture_reached = 9

@unique
class FunctionID(IntEnum):
    get_moisture = 1
    set_moisture_callback_period = 2
    get_moisture_callback_period = 3
    set_moisture_callback_threshold = 4
    get_moisture_callback_threshold = 5
    set_debounce_period = 6
    get_debounce_period = 7
    set_moving_average = 10
    get_moving_average = 11

@unique
class ThresholdOption(Enum):
    off = 'x'
    outside = 'o'
    inside = 'i'
    less_than = '<'
    greater_than = '>'


class BrickletMoisture(Device):
    """
    Measures ambient light up to 64000lux
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletMoisture
    DEVICE_DISPLAY_NAME = 'Moisture Bricklet'
    DEVICE_URL_PART = 'moisture' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption

    CALLBACK_FORMATS = {
        CallbackID.moisture: 'H',
        CallbackID.moisture_reached: 'H',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_moisture_value(self):
        """
        Returns the current moisture value.
        A small value corresponds to little moisture, a big
        value corresponds to much moisture.

        If you want to get the moisture value periodically, it is recommended
        to use the :cb:`Moisture` callback and set the period with
        :func:`Set Moisture Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.get_moisture,
            response_expected=True
        )
        return unpack_payload(payload, 'H')

    async def set_moisture_callback_period(self, period=0, response_expected=True):
        """
        Sets the period with which the :cb:`Moisture` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Moisture` callback is only triggered if the moisture value has changed
        since the last triggering.
        """
        assert type(period) is int and period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.set_moisture_callback_period,
            data=pack_payload((period,), 'I'),
            response_expected = response_expected,
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.ok

    async def get_moisture_callback_period(self):
        """
        Returns the period as set by :func:`Set Moisture Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.get_moisture_callback_period,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_moisture_callback_threshold(self, option=ThresholdOption.off, minimum=0, maximum=0, response_expected=True):
        """
        Sets the thresholds for the :cb:`Moisture Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the moisture value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the moisture value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the moisture value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the moisture value is greater than the min value (max is ignored)"
        """
        assert type(option) is ThresholdOption
        assert type(minimum) is int and minimum >= 0
        assert type(maximum) is int and minimum >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.set_moisture_callback_threshold,
            data=pack_payload((option.value.encode(), minimum, maximum), 'c H H'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_moisture_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Illuminance Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.get_moisture_callback_threshold,
            response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, 'c H H')
        option = ThresholdOption(option)
        return GetMoistureCallbackThreshold(option, minimum, maximum)

    async def set_debounce_period(self, debounce_period=100, response_expected=True):
        """
        Sets the period with which the threshold callbacks

        * :cb:`Illuminance Reached`,

        are triggered, if the thresholds

        * :func:`Set Illuminance Callback Threshold`,

        keep being reached.
        """
        assert type(debounce_period) is int and debounce_period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.set_debounce_period,
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
            function_id=FunctionID.get_debounce_period,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_moving_average(self, average=100, response_expected=True):
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the moisture value.

        Setting the length to 0 will turn the averaging completely off. With less
        averaging, there is more noise on the data.
        """
        assert type(average) is int and average >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.set_moving_average,
            data=pack_payload((average,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_moving_average(self):
        """
        Returns the length moving average as set by :func:`Set Moving Average`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.get_moving_average,
            response_expected=True
        )
        return unpack_payload(payload, 'B')


    def register_event_queue(self, event_id, queue):
        """
        Registers the given *function* with the given *callback_id*.
        """
        assert type(event_id) is CallbackID
        super().register_event_queue(event_id, queue)

    def _process_callback(self, header, payload):
        try:
            header['function_id'] = CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            super()._process_callback(header, payload)

