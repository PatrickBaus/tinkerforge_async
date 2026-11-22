"""
Module for the Tinkerforge Piezo Speaker Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/PiezoSpeaker_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, TypeAlias

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import check_range, encode_string
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    BEEP_FINISHED = 4
    MORSE_CODE_FINISHED = 5


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    BEEP = 1
    MORSE_CODE = 2
    CALIBRATE = 3


@unique
class BeepDuration(Enum):
    """
    The beep duration options
    """

    OFF = 0
    INFINITE = 4294967295


HERTZ = LinearQuantity(1)  # raw: 1/1 Hertz, returned in Hz


class BrickletPiezoSpeaker(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Creates beep with configurable frequency
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_PIEZO_SPEAKER
    DEVICE_DISPLAY_NAME = "Piezo Speaker Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    BeepDuration: TypeAlias = BeepDuration

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

    async def beep(
        self, duration: BeepDuration | int, frequency: float | Decimal, response_expected: bool = True
    ) -> None:
        """
        Beeps with the given frequency for the given duration.

        .. versionchanged:: 2.0.2$nbsp;(Plugin)
           A duration of 0 stops the current beep if any, the frequency parameter is
           ignored. A duration of 4294967295 results in an infinite beep.

        The Piezo Speaker Bricklet can only approximate the frequency, it will play
        the best possible match by applying the calibration (see :func:`calibrate`).

        Units: frequency in Hz (585 to 7100 Hz).
        """
        frequency_raw = HERTZ.from_si(frequency)
        check_range("frequency", frequency_raw, 585, 7100, frequency)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.BEEP,
            data=pack_payload((BeepDuration(duration).value, frequency_raw), "I H"),
            response_expected=response_expected,
        )

    async def morse_code(self, morse: str, frequency: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets morse code that will be played by the piezo buzzer. The morse code
        is given as a string consisting of "." (dot), "-" (minus) and " " (space)
        for *dits*, *dahs* and *pauses*. Every other character is ignored.

        For example: If you set the string "...---...", the piezo buzzer will beep
        nine times with the durations "short short short long long long short
        short short".

        Units: frequency in Hz (585 to 7100 Hz).
        """
        frequency_raw = HERTZ.from_si(frequency)
        check_range("frequency", frequency_raw, 585, 7100, frequency)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MORSE_CODE,
            data=pack_payload((encode_string("morse", morse, 60), frequency_raw), "60s H"),
            response_expected=response_expected,
        )

    async def calibrate(self) -> bool:
        """
        The Piezo Speaker Bricklet can play 512 different tones. This function
        plays each tone and measures the exact frequency back. The result is a
        mapping between setting value and frequency. This mapping is stored
        in the EEPROM and loaded on startup.

        The Bricklet should come calibrated, you only need to call this
        function (once) every time you reflash the Bricklet plugin.

        Returns *true* after the calibration finishes.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.CALIBRATE, response_expected=True
        )
        return unpack_payload(payload, "!")

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.BEEP_FINISHED:
            return 0, None
        return 1, None
