# -*- coding: utf-8 -*-
from collections import namedtuple
from enum import Enum, unique

from .devices import DeviceIdentifier, Device
from .ip_connection_helper import pack_payload, unpack_payload

GetSegments = namedtuple('Segments', ['segments', 'brightness', 'colon'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

@unique
class CallbackID(Enum):
    COUNTER_FINISHED = 5

@unique
class FunctionID(Enum):
    SET_SEGMENTS = 1
    GET_SEGMENTS = 2
    START_COUNTER = 3
    GET_COUNTER_VALUE = 4

class BrickletSegmentDisplay4x7(Device):
    """
    Four 7-segment displays with switchable colon
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletSegmentDisplay4x7
    DEVICE_DISPLAY_NAME = 'Segment Display 4x7 Bricklet'
    DEVICE_URL_PART = 'segment_display_4x7' # internal

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
        super().__init__(uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_segments(self, segments=(0,0,0,0), brightness=7, colon=False, response_expected=True):
        """
        The 7-segment display can be set with bitmaps. Every bit controls one
        segment:

        .. image:: /Images/Bricklets/bricklet_segment_display_4x7_bit_order.png
           :scale: 100 %
           :alt: Bit order of one segment
           :align: center

        For example to set a "5" you would want to activate segments 0, 2, 3, 5 and 6.
        This is represented by the number 0b01101101 = 0x6d = 109.

        The brightness can be set between 0 (dark) and 7 (bright). The colon
        parameter turns the colon of the display on or off.
        """
        assert (all(0 <= segment <= 127 for segment in segments))
        assert (0 <= brightness <= 7)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SEGMENTS,
            data=pack_payload(
              (
                list(map(int, segments)),
                int(brightness),
                bool(colon),
              ), '4B B !'),
            response_expected=response_expected
        )

    async def get_segments(self):
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
            function_id=FunctionID.GET_SEGMENTS,
            response_expected=True
        )
        return GetSegments(*unpack_payload(payload, '4B B !'))

    async def start_counter(self, value_from, value_to, increment=1, length=1000, response_expected=True):
        """
        Starts a counter with the *from* value that counts to the *to*
        value with the each step incremented by *increment*.
        *length* is the pause between each increment.

        Example: If you set *from* to 0, *to* to 100, *increment* to 1 and
        *length* to 1000, a counter that goes from 0 to 100 with one second
        pause between each increment will be started.

        Using a negative increment allows to count backwards.

        You can stop the counter at every time by calling :func:`Set Segments`.
        """
        assert (-999 <= value_from <= 9999)
        assert (-999 <= value_to <= 9999)
        assert (-999 <= increment <= 9999)
        assert (0 <= length <= 2**32-1)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.START_COUNTER,
            data=pack_payload(
              (
                int(value_from),
                int(value_to),
                int(increment),
                int(length),
              ), 'h h h I'),
            response_expected=response_expected
        )

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

