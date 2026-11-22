"""
Module for the Tinkerforge Piezo Buzzer Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/PiezoBuzzer_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias, override

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import Duration, check_range, encode_string, seconds_to_ms
from .ip_connection_helper import pack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    BEEP_FINISHED = 3
    MORSE_CODE_FINISHED = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    BEEP = 1
    MORSE_CODE = 2


class BrickletPiezoBuzzer(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Creates 1kHz beep
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_PIEZO_BUZZER
    DEVICE_DISPLAY_NAME = "Piezo Buzzer Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.BEEP_FINISHED: "",
        CallbackID.MORSE_CODE_FINISHED: "",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.BEEP_FINISHED,)),
        Channel(1, callbacks=(CallbackID.MORSE_CODE_FINISHED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def beep(self, duration: Duration, response_expected: bool = True) -> None:
        """
        Beeps for the given duration.

        Units: duration in s.
        """
        duration_raw = seconds_to_ms(duration)
        check_range("duration", duration_raw, 0, 4294967295, duration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.BEEP,
            data=pack_payload((duration_raw,), "I"),
            response_expected=response_expected,
        )

    async def morse_code(self, morse: str, response_expected: bool = True) -> None:
        """
        Sets morse code that will be played by the piezo buzzer. The morse code
        is given as a string consisting of "." (dot), "-" (minus) and " " (space)
        for *dits*, *dahs* and *pauses*. Every other character is ignored.

        For example: If you set the string "...---...", the piezo buzzer will beep
        nine times with the durations "short short short long long long short
        short short".
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MORSE_CODE,
            data=pack_payload((encode_string("morse", morse, 60),), "60s"),
            response_expected=response_expected,
        )

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.BEEP_FINISHED:
            return 0, None
        return 1, None
