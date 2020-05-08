# -*- coding: utf-8 -*-
from collections import namedtuple
from enum import IntEnum, unique

from .devices import DeviceIdentifier, Device
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetSegments = namedtuple('Segments', ['segments', 'brightness', 'colon'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

@unique
class CallbackID(IntEnum):
    counter_finished = 5

@unique
class FunctionID(IntEnum):
    set_segments = 1
    get_segments = 2
    start_counter = 3
    get_counter_value = 4

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
        CallbackID.counter_finished: '',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_segments(self, segments, brightness=7, colon=False, response_expected=False):
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
        assert(all(isinstance(segment, int) and segment <= 127 and segment >= 0 for segment in segments))
        assert(isinstance(brightness, int) and brightness <= 7 and brightness >= 0)
        assert(isinstance(colon, bool))

        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletSegmentDisplay4x7.FunctionID.set_segments,
            data=pack_payload((segments, brightness, colon), '4B B !'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

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
            function_id=BrickletSegmentDisplay4x7.FunctionID.get_segments,
            response_expected=True
        )
        return GetSegments(*unpack_payload(payload, '4B B !'))

    async def start_counter(self, value_from, value_to, increment=1, length=1000, response_expected=False):
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
        assert(isinstance(value_from, int) and value_from <= 9999 and value_from >= -999)
        assert(isinstance(value_to, int) and value_to <= 9999 and value_to >= -999)
        assert(isinstance(increment, int) and increment <= 9999 and increment >= -999)
        assert(isinstance(length, int) and length <= 2**32-1 and length >= 0)

        result = await self.ipcon.send_request(
            device=self,
            function_id=BrickletSegmentDisplay4x7.FunctionID.start_counter,
            data=pack_payload((value_from, value_to, increment, length, ), 'h h h I'),
            response_expected=response_expected
        )

        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_counter_value(self):
        """
        Returns the counter value that is currently shown on the display.

        If there is no counter running a 0 will be returned.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=BrickletSegmentDisplay4x7.FunctionID.get_counter_value,
            response_expected=True
        )
        return unpack_payload(payload, 'H')

    def register_event_queue(self, event_id, queue):
        """
        Registers the given *function* with the given *callback_id*.
        """
        assert type(event_id) is BrickletSegmentDisplay4x7.CallbackID
        super().register_event_queue(event_id, queue)

    def _process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            super()._process_callback(header, payload)

