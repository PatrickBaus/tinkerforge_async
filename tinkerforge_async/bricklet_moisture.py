# -*- coding: utf-8 -*-
"""
Module for the Tinkerforge Moisture Bricklet
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Moisture.html)
implemented using Python AsyncIO. It does the low-lvel communication with the
Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""
import asyncio
from collections import namedtuple
from enum import Enum, unique

from .devices import DeviceIdentifier, Device, ThresholdOption, GetCallbackConfiguration
from .ip_connection_helper import pack_payload, unpack_payload

GetMoistureCallbackThreshold = namedtuple('MoistureCallbackThreshold', ['option', 'minimum', 'maximum'])


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """
    MOISTURE = 8
    MOISTURE_REACHED = 9


@unique
class FunctionID(Enum):
    """
    The function calls available to this bricklet
    """
    GET_MOISTURE = 1
    SET_MOISTURE_CALLBACK_PERIOD = 2
    GET_MOISTURE_CALLBACK_PERIOD = 3
    SET_MOISTURE_CALLBACK_THRESHOLD = 4
    GET_MOISTURE_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_MOVING_AVERAGE = 10
    GET_MOVING_AVERAGE = 11


class BrickletMoisture(Device):
    """
    Measures ambient light up to 64000lux
    """
    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_MOISTURE
    DEVICE_DISPLAY_NAME = 'Moisture Bricklet'

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption

    CALLBACK_FORMATS = {
        CallbackID.MOISTURE: 'H',
        CallbackID.MOISTURE_REACHED: 'H',
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.MOISTURE, CallbackID.MOISTURE_REACHED),
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid):
        assert sid == 0

        return await self.get_moisture_value()

    async def set_callback_configuration(self, sid, period=0, value_has_to_change=False, option=ThresholdOption.OFF, minimum=None, maximum=None, response_expected=True):  # pylint: disable=too-many-arguments
        minimum = 0 if minimum is None else minimum
        maximum = 0 if maximum is None else maximum

        assert sid == 0

        await asyncio.gather(
            self.set_moisture_callback_period(period, response_expected),
            self.set_moisture_callback_threshold(option, minimum, maximum, response_expected)
        )

    async def get_callback_configuration(self, sid):
        assert sid == 0

        period, config = await asyncio.gather(
            self.get_moisture_callback_period(),
            self.get_moisture_callback_threshold()
        )
        return GetCallbackConfiguration(period, True, *config)

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
            function_id=FunctionID.GET_MOISTURE,
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
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOISTURE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), 'I'),
            response_expected=response_expected,
        )

    async def get_moisture_callback_period(self):
        """
        Returns the period as set by :func:`Set Moisture Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_MOISTURE_CALLBACK_PERIOD,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_moisture_callback_threshold(self, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
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
        if not isinstance(option, ThresholdOption):
            option = ThresholdOption(option)
        assert minimum >= 0
        assert minimum >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOISTURE_CALLBACK_THRESHOLD,
            data=pack_payload(
              (
                option.value.encode('ascii'),
                int(minimum),
                int(maximum),
              ), 'c H H'),
            response_expected=response_expected
        )

    async def get_moisture_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Illuminance Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_MOISTURE_CALLBACK_THRESHOLD,
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
        assert debounce_period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((int(debounce_period),), 'I'),
            response_expected=response_expected
        )

    async def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_DEBOUNCE_PERIOD,
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
        assert average >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE,
            data=pack_payload((int(average),), 'B'),
            response_expected=response_expected
        )

    async def get_moving_average(self):
        """
        Returns the length moving average as set by :func:`Set Moving Average`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_MOVING_AVERAGE,
            response_expected=True
        )
        return unpack_payload(payload, 'B')

    async def read_events(self):
        async for header, payload in super().read_events():
            try:
                function_id = CallbackID(header['function_id'])
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in self._registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                yield self.build_event(0, function_id, value)
