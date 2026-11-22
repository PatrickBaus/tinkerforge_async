"""
Module for the Tinkerforge Motion Detector Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/MotionDetector_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, Any, TypeAlias

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    MOTION_DETECTED = 2
    DETECTION_CYCLE_ENDED = 3


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_MOTION_DETECTED = 1
    SET_STATUS_LED_CONFIG = 4
    GET_STATUS_LED_CONFIG = 5


@unique
class Motion(Enum):
    """
    The motion options
    """

    NOT_DETECTED = 0
    DETECTED = 1


@unique
class StatusLEDConfig(Enum):
    """
    The status led config options
    """

    OFF = 0
    ON = 1
    SHOW_STATUS = 2


class BrickletMotionDetector(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Passive infrared (PIR) motion sensor with 7m range
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_MOTION_DETECTOR
    DEVICE_DISPLAY_NAME = "Motion Detector Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Motion: TypeAlias = Motion
    StatusLEDConfig: TypeAlias = StatusLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.MOTION_DETECTED: "",
        CallbackID.DETECTION_CYCLE_ENDED: "",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.MOTION_DETECTED,)),
        Channel(1, callbacks=(CallbackID.DETECTION_CYCLE_ENDED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_motion_detected(self) -> Motion:
        """
        Returns 1 if a motion was detected. How long this returns 1 after a motion
        was detected can be adjusted with one of the small potentiometers on the
        Motion Detector Bricklet, see ``here
        <motion_detector_bricklet_sensitivity_delay_block_time>``.

        There is also a blue LED on the Bricklet that is on as long as the Bricklet is
        in the "motion detected" state.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOTION_DETECTED, response_expected=True
        )
        return Motion(unpack_payload(payload, "B"))

    async def set_status_led_config(
        self, config: StatusLEDConfig | int = StatusLEDConfig.SHOW_STATUS, response_expected: bool = True
    ) -> None:
        """
        Sets the status led configuration.

        By default the status LED turns on if a motion is detected and off is no motion
        is detected.

        You can also turn the LED permanently on/off.

        .. versionadded:: 2.0.1 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STATUS_LED_CONFIG,
            data=pack_payload((StatusLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_status_led_config(self) -> StatusLEDConfig:
        """
        Returns the configuration as set by :func:`set_status_led_config`.

        .. versionadded:: 2.0.1 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATUS_LED_CONFIG, response_expected=True
        )
        return StatusLEDConfig(unpack_payload(payload, "B"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.MOTION_DETECTED:
            return 0, None
        return 1, None
