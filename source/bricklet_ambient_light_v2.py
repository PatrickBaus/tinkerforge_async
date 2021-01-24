# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, unique

from .devices import DeviceIdentifier, Device, ThresholdOption
from .ip_connection import Flags
from .ip_connection_helper import pack_payload, unpack_payload

GetIlluminanceCallbackThreshold = namedtuple('IlluminanceCallbackThreshold', ['option', 'minimum', 'maximum'])

@unique
class CallbackID(Enum):
    ILLUMINANCE = 10
    ILLUMINANCE_REACHED = 11

@unique
class FunctionID(Enum):
    GET_ILLUMINANCE = 1
    SET_ILLUMINANCE_CALLBACK_PERIOD = 2
    GET_ILLUMINANCE_CALLBACK_PERIOD = 3
    SET_ILLUMINANCE_CALLBACK_THRESHOLD = 4
    GET_ILLUMINANCE_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7

class BrickletAmbientLightV2(Device):
    """
    Measures ambient light up to 64000lux
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletAmbientLight_V2
    DEVICE_DISPLAY_NAME = 'Ambient Light Bricklet 2.0'
    DEVICE_URL_PART = 'ambient_light_v2' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption

    CALLBACK_FORMATS = {
        CallbackID.ILLUMINANCE: 'I',
        CallbackID.ILLUMINANCE_REACHED: 'I',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_illuminance(self):
        """
        Returns the illuminance of the ambient light sensor. The measurement range goes
        up to about 100000lux, but above 64000lux the precision starts to drop.

        .. versionchanged:: 2.0.2$nbsp;(Plugin)
          An illuminance of 0lux indicates that the sensor is saturated and the
          configuration should be modified, see :func:`Set Configuration`.

        If you want to get the illuminance periodically, it is recommended to use the
        :cb:`Illuminance` callback and set the period with
        :func:`Set Illuminance Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ILLUMINANCE,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_illuminance_callback_period(self, period=0, response_expected=True):
        """
        Sets the period with which the :cb:`Illuminance` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Illuminance` callback is only triggered if the illuminance has changed
        since the last triggering.
        """
        assert type(period) is int and period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
            data=pack_payload((period,), 'I'),
            response_expected = response_expected,
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_illuminance_callback_period(self):
        """
        Returns the period as set by :func:`Set Illuminance Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_illuminance_callback_threshold(self, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
        """
        Sets the thresholds for the :cb:`Illuminance Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the illuminance is *outside* the min and max values"
         "'i'",    "Callback is triggered when the illuminance is *inside* the min and max values"
         "'<'",    "Callback is triggered when the illuminance is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the illuminance is greater than the min value (max is ignored)"
        """
        assert type(option) is ThresholdOption
        assert type(minimum) is int and minimum >= 0
        assert type(maximum) is int and minimum >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD,
            data=pack_payload((option.value.encode('ascii'), minimum, maximum), 'c I I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_illuminance_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Illuminance Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_THRESHOLD,
            response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, 'c I I')
        option = ThresholdOption(option)
        return GetIlluminanceCallbackThreshold(option, minimum, maximum)

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
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((debounce_period,), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

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

