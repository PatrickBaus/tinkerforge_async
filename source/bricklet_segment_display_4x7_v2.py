# -*- coding: utf-8 -*-
from collections import namedtuple
from enum import Enum, unique

from .devices import DeviceIdentifier, BrickletWithMCU
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetSegments = namedtuple('Segments', ['digit0', 'digit1', 'digit2', 'digit3', 'colon', 'tick'])

@unique
class CallbackID(Enum):
    COUNTER_FINISHED = 10

@unique
class FunctionID(Enum):
    SET_SEGMENTS = 1
    GET_SEGMENTS = 2
    SET_BRIGHTNESS = 3
    GET_BRIGHTNESS = 4
    SET_NUMERIC_VALUE = 5
    SET_SELECTED_SEGMENT = 6
    GET_SELECTED_SEGMENT = 7
    START_COUNTER = 8
    GET_COUNTER_VALUE = 9

class BrickletSegmentDisplay4x7V2(BrickletWithMCU):
    """
    Four 7-segment displays with switchable dots
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletSegmentDisplay4x7_V2
    DEVICE_DISPLAY_NAME = 'Segment Display 4x7 Bricklet 2.0'
    DEVICE_URL_PART = 'segment_display_4x7_v2' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.COUNTER_FINISHED: '',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        DeviceWithMCU.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_segments(self, digit0, digit1, digit2, digit3, colon, tick, response_expected=False):
        """
        Sets the segments of the Segment Display 4x7 Bricklet 2.0 segment-by-segment.

        The data is split into the four digits, two colon dots and the tick mark.

        The indices of the segments in the digit and colon parameters are as follows:

        .. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_segment_index.png
           :scale: 100 %
           :alt: Indices of segments
           :align: center
        """
        digit0 = list(map(bool, digit0))
        digit1 = list(map(bool, digit1))
        digit2 = list(map(bool, digit2))
        digit3 = list(map(bool, digit3))
        colon = list(map(bool, colon))
        tick = bool(tick)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SEGMENTS,
            data=pack_payload((digit0, digit1, digit2, digit3, colon, tick), '8! 8! 8! 8! 2! !'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_segments(self):
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
            function_id=FunctionID.GET_SEGMENTS,
            response_expected=True
        )
        return  GetSegments(*unpack_payload(payload, '8! 8! 8! 8! 2! !'))

    async def set_brightness(self, brightness=7, response_expected=False):
        """
        The brightness can be set between 0 (dark) and 7 (bright).

        The default value is 7.
        """
        assert isinstance(brightness, int) and (0 <= brightness <= 7)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SET_BRIGHTNESS,
            data=pack_payload((heater_config.value,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_brightness(self):
        """
        Returns the brightness as set by :func:`Set Brightness`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_BRIGHTNESS,
            response_expected=True
        )
        return unpack_payload(payload, 'B')

    async def set_numeric_value(self, value, response_expected=False):
        """
        Sets a numeric value for each of the digits. The values can be between
        -2 and 15. They represent:

        * -2: minus sign
        * -1: blank
        * 0-9: 0-9
        * 10: A
        * 11: b
        * 12: C
        * 13: d
        * 14: E
        * 15: F

        Example: A call with [-2, -1, 4, 2] will result in a display of "- 42".
        """
        value = list(map(int, value))

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_NUMERIC_VALUE,
            data=pack_payload((heater_config.value,), '4b'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def set_selected_segment(self, segment, value, response_expected=False):
        """
        Turns one specified segment on or off.

        The indices of the segments are as follows:

        .. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_selected_segment_index.png
           :scale: 100 %
           :alt: Indices of selected segments
           :align: center
        """
        assert isinstance(segment, int) and (0 <= segment <= 31)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_SEGMENT,
            data=pack_payload((segment, bool(value)), 'B !'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_selected_segment(self, segment):
        """
        Returns the value of a single segment.
        """
        assert isinstance(segment, int) and (0 <= segment <= 31)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SELECTED_SEGMENT,
            data=pack_payload((segment,), 'B'),
            response_expected=True
        )

        return unpack_payload(payload, '!')

    async def start_counter(self, value_from, value_to, increment, length, response_expected=False):
        """
        Turns one specified segment on or off.

        The indices of the segments are as follows:

        .. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_selected_segment_index.png
           :scale: 100 %
           :alt: Indices of selected segments
           :align: center
        """
        assert isinstance(value_from, int) and (-999 <= value_from <= 9999)
        assert isinstance(value_to, int) and (-999 <= value_to <= 9999)
        assert isinstance(increment, int) and (-999 <= increment <= 9999)
        assert isinstance(length, int)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.START_COUNTER,
            data=pack_payload((value_from, value_to, increment, length), 'h h h I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_counter_value(self):
        """
        Returns the counter value that is currently shown on the display.

        If there is no counter running a 0 will be returned.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_COUNTER_VALUE,
            response_expected=True
        )
        return unpack_payload(payload, 'H')

