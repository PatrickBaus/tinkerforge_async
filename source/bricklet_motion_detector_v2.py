# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, unique

from .devices import DeviceIdentifier, BrickletWithMCU, device_factory
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetIndicator = namedtuple('Indicator', ['top_left', 'top_right', 'bottom'])

@unique
class CallbackID(Enum):
    MOTION_DETECTED = 6
    DETECTION_CYCLE_ENDED = 7

@unique
class FunctionID(Enum):
    GET_MOTION_DETECTED = 1
    SET_SENSITIVITY = 2
    GET_SENSITIVITY = 3
    SET_INDICATOR = 4
    GET_INDICATOR = 5

class BrickletMotionDetectorV2(BrickletWithMCU):
    """
    Passive infrared (PIR) motion sensor with 12m range and dimmable backlight
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletMotionDetector_V2
    DEVICE_DISPLAY_NAME = 'Motion Detector Bricklet 2.0'
    DEVICE_URL_PART = 'motion_detector_v2' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.MOTION_DETECTED: '',
        CallbackID.DETECTION_CYCLE_ENDED: '',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_motion_detected(self):
        """
        Returns True if a motion was detected. It returns True approx. for 1.8 seconds
        until the sensor checks for a new movement.

        There is also a blue LED on the Bricklet that is on as long as the Bricklet is
        in the "motion detected" state.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_MOTION_DETECTED,
            response_expected=True
        )
        return bool(unpack_payload(payload, 'B'))

    async def set_sensitivity(self, sensitivity=50, response_expected=True):
        """
        Sets the sensitivity of the PIR sensor. At full
        sensitivity (100), the Bricklet can detect motion in a range of approximately 12m.

        The actual range depends on many things in the environment (e.g. reflections) and the
        size of the object to be detected. While a big person might be detected in a range
        of 10m a cat may only be detected at 2m distance with the same setting.

        So you will have to find a good sensitivity for your application by trial and error.
        """
        assert isinstance(sensitivity, int) and (0 <= sensitivity <= 100)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSITIVITY,
            data=pack_payload((sensitivity,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_sensitivity(self):
        """
        Returns the sensitivity as set by :func:`Set Sensitivity`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SENSITIVITY,
            response_expected=True
        )
        return unpack_payload(payload, 'B')

    async def set_indicator(self, top_left=0, top_right=0, bottom=0, response_expected=False):
        """
        Sets the blue backlight of the fresnel lens. The backlight consists of
        three LEDs. The brightness of each LED can be controlled with a 8-bit value
        (0-255). A value of 0 turns the LED off and a value of 255 turns the LED
        to full brightness.
        """
        assert isinstance(top_left, int) and (0 <= top_left <= 255)
        assert isinstance(top_right, int) and (0 <= top_right <= 255)
        assert isinstance(bottom, int) and (0 <= bottom <= 255)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_INDICATOR,
            data=pack_payload((top_left,top_right,bottom), 'B B B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_indicator(self):
        """
        Returns the indicator configuration as set by :func:`Set Indicator`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_INDICATOR,
            response_expected=True
        )

        return GetIndicator(*unpack_payload(payload, 'B B B'))

    def _process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            super()._process_callback(header, payload)

device_factory.register(BrickletMotionDetectorV2.DEVICE_IDENTIFIER, BrickletMotionDetectorV2)

