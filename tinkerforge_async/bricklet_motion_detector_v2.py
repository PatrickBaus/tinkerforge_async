"""
Module for the Tinkerforge Barometer Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Barometer_V2.html) implemented using Python asyncio. It does the
low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    MOTION_DETECTED = 6
    DETECTION_CYCLE_ENDED = 7


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_MOTION_DETECTED = 1
    SET_SENSITIVITY = 2
    GET_SENSITIVITY = 3
    SET_INDICATOR = 4
    GET_INDICATOR = 5


class GetIndicator(NamedTuple):
    top_left: int
    top_right: int
    bottom: int


class BrickletMotionDetectorV2(BrickletWithMCU):
    """
    Passive infrared (PIR) motion sensor with 12m range and dimmable backlight
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_MOTION_DETECTOR_V2
    DEVICE_DISPLAY_NAME = "Motion Detector Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.MOTION_DETECTED: "",
        CallbackID.DETECTION_CYCLE_ENDED: "",
    }

    CHANNELS = (
        Channel(0, getter="get_motion_detected", callbacks=(CallbackID.MOTION_DETECTED,)),
        Channel(1, callbacks=(CallbackID.DETECTION_CYCLE_ENDED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> bool:
        return await self._get_value(sid)

    async def get_motion_detected(self) -> bool:
        """
        Returns True if a motion was detected. It returns True approx. for 1.8 seconds
        until the sensor checks for a new movement.

        There is also a blue LED on the Bricklet that is on as long as the Bricklet is
        in the "motion detected" state.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOTION_DETECTED, response_expected=True
        )
        return bool(unpack_payload(payload, "B"))

    async def set_sensitivity(self, sensitivity: int = 50, response_expected: bool = True) -> None:
        """
        Sets the sensitivity of the PIR sensor. At full
        sensitivity (100), the Bricklet can detect motion in a range of approximately 12m.

        The actual range depends on many things in the environment (e.g. reflections) and the
        size of the object to be detected. While a big person might be detected in a range
        of 10m a cat may only be detected at 2m distance with the same setting.

        So you will have to find a good sensitivity for your application by trial and error.
        """
        if not 0 <= sensitivity <= 100:
            raise ValueError(f"Invalid argument: expected 0 <= sensitivity <= 100, got sensitivity={sensitivity!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSITIVITY,
            data=pack_payload((int(sensitivity),), "B"),
            response_expected=response_expected,
        )

    async def get_sensitivity(self) -> int:
        """
        Returns the sensitivity as set by :func:`Set Sensitivity`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSITIVITY, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_indicator(
        self, top_left: int = 0, top_right: int = 0, bottom: int = 0, response_expected: bool = True
    ) -> None:
        """
        Sets the blue backlight of the fresnel lens. The backlight consists of three LEDs. The brightness of each LED
        can be controlled with an 8-bit value (0-255). A value of 0 turns the LED off and a value of 255 turns the LED
        to full brightness.
        """
        if not 0 <= top_left <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= top_left <= 255, got top_left={top_left!r}")
        if not 0 <= top_right <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= top_right <= 255, got top_right={top_right!r}")
        if not 0 <= bottom <= 255:
            raise ValueError(f"Invalid argument: expected 0 <= bottom <= 255, got bottom={bottom!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_INDICATOR,
            data=pack_payload(
                (
                    int(top_left),
                    int(top_right),
                    int(bottom),
                ),
                "B B B",
            ),
            response_expected=response_expected,
        )

    async def get_indicator(self) -> tuple[int, int, int]:
        """
        Returns the indicator configuration as set by :func:`Set Indicator`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_INDICATOR, response_expected=True
        )

        return GetIndicator(*unpack_payload(payload, "B B B"))
