"""
Module for the Tinkerforge Piezo Speaker Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/PiezoSpeakerV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    BEEP_FINISHED = 7
    ALARM_FINISHED = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_BEEP = 1
    GET_BEEP = 2
    SET_ALARM = 3
    GET_ALARM = 4
    UPDATE_VOLUME = 5
    UPDATE_FREQUENCY = 6


@unique
class BeepDuration(Enum):
    """
    The beep duration options
    """

    OFF = 0
    INFINITE = 4294967295


@unique
class AlarmDuration(Enum):
    """
    The alarm duration options
    """

    OFF = 0
    INFINITE = 4294967295


class GetBeep(NamedTuple):
    frequency: Decimal
    volume: int
    duration: BeepDuration
    duration_remaining: Decimal


class GetAlarm(NamedTuple):
    start_frequency: Decimal
    end_frequency: Decimal
    step_size: Decimal
    step_delay: Decimal
    volume: int
    duration: AlarmDuration
    duration_remaining: AlarmDuration
    current_frequency: Decimal


HERTZ = LinearQuantity(1)  # raw: 1/1 Hertz, returned in Hz


class BrickletPiezoSpeakerV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Creates beep and alarm with configurable volume and frequency
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_PIEZO_SPEAKER_V2
    DEVICE_DISPLAY_NAME = "Piezo Speaker Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    BeepDuration: TypeAlias = BeepDuration
    AlarmDuration: TypeAlias = AlarmDuration

    CALLBACK_FORMATS = {
        CallbackID.BEEP_FINISHED: "",
        CallbackID.ALARM_FINISHED: "",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.BEEP_FINISHED,)),
        Channel(1, callbacks=(CallbackID.ALARM_FINISHED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_beep(
        self, frequency: float | Decimal, volume: int, duration: BeepDuration | int, response_expected: bool = True
    ) -> None:
        """
        Beeps with the given frequency and volume for the duration.

        A duration of 0 stops the current beep if any is ongoing.
        A duration of 4294967295 results in an infinite beep.

        Units: frequency in Hz (50 to 15000 Hz).
        """
        frequency_raw = HERTZ.from_si(frequency)
        check_range("frequency", frequency_raw, 50, 15000, frequency)
        volume = int(volume)
        check_range("volume", volume, 0, 10)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BEEP,
            data=pack_payload((frequency_raw, volume, BeepDuration(duration).value), "H B I"),
            response_expected=response_expected,
        )

    async def get_beep(self) -> GetBeep:
        """
        Returns the last beep settings as set by :func:`set_beep`. If a beep is currently
        running it also returns the remaining duration of the beep.

        If the frequency or volume is updated during a beep (with :func:`update_frequency`
        or :func:`update_volume`) this function returns the updated value.

        Units: frequency in Hz (50 to 15000 Hz), duration_remaining in s.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_BEEP, response_expected=True)
        frequency, volume, duration, duration_remaining = unpack_payload(payload, "H B I I")
        return GetBeep(HERTZ.to_si(frequency), volume, BeepDuration(duration), ms_to_seconds(duration_remaining))

    async def set_alarm(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        start_frequency: float | Decimal,
        end_frequency: float | Decimal,
        step_size: float | Decimal,
        step_delay: Duration,
        volume: int,
        duration: AlarmDuration | int,
        response_expected: bool = True,
    ) -> None:
        """
        Creates an alarm (a tone that goes back and force between two specified frequencies).

        The following parameters can be set:

        * Start Frequency: Start frequency of the alarm.
        * End Frequency: End frequency of the alarm.
        * Step Size: Size of one step of the sweep between the start/end frequencies.
        * Step Delay: Delay between two steps (duration of time that one tone is used in a sweep).
        * Duration: Duration of the alarm.

        A duration of 0 stops the current alarm if any is ongoing.
        A duration of 4294967295 results in an infinite alarm.

        Below you can find two sets of example settings that you can try out. You can use
        these as a starting point to find an alarm signal that suits your application.

        Example 1: 10 seconds of loud annoying fast alarm

        * Start Frequency = 800
        * End Frequency = 2000
        * Step Size = 10
        * Step Delay = 1
        * Volume = 10
        * Duration = 10000

        Example 2: 10 seconds of soft siren sound with slow build-up

        * Start Frequency = 250
        * End Frequency = 750
        * Step Size = 1
        * Step Delay = 5
        * Volume = 0
        * Duration = 10000

        The following conditions must be met:

        * Start Frequency: has to be smaller than end frequency
        * End Frequency: has to be bigger than start frequency
        * Step Size: has to be small enough to fit into the frequency range
        * Step Delay: has to be small enough to fit into the duration

        Units: start_frequency in Hz (50 to 14999 Hz), end_frequency in Hz (51 to 15000 Hz), step_size in Hz (0 to 14950
        Hz), step_delay in s.
        """
        start_frequency_raw = HERTZ.from_si(start_frequency)
        check_range("start_frequency", start_frequency_raw, 50, 14999, start_frequency)
        end_frequency_raw = HERTZ.from_si(end_frequency)
        check_range("end_frequency", end_frequency_raw, 51, 15000, end_frequency)
        step_size_raw = HERTZ.from_si(step_size)
        check_range("step_size", step_size_raw, 0, 14950, step_size)
        step_delay_raw = seconds_to_ms(step_delay)
        check_range("step_delay", step_delay_raw, 0, 65535, step_delay)
        volume = int(volume)
        check_range("volume", volume, 0, 10)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALARM,
            data=pack_payload(
                (
                    start_frequency_raw,
                    end_frequency_raw,
                    step_size_raw,
                    step_delay_raw,
                    volume,
                    AlarmDuration(duration).value,
                ),
                "H H H H B I",
            ),
            response_expected=response_expected,
        )

    async def get_alarm(self) -> GetAlarm:
        """
        Returns the last alarm settings as set by :func:`set_alarm`. If an alarm is currently
        running it also returns the remaining duration of the alarm as well as the
        current frequency of the alarm.

        If the volume is updated during an alarm (with :func:`update_volume`)
        this function returns the updated value.

        Units: start_frequency in Hz (50 to 14999 Hz), end_frequency in Hz (51 to 15000 Hz), step_size in Hz (50 to
        14950 Hz), step_delay in s, current_frequency in Hz (50 to 15000 Hz).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALARM, response_expected=True
        )
        (
            start_frequency,
            end_frequency,
            step_size,
            step_delay,
            volume,
            duration,
            duration_remaining,
            current_frequency,
        ) = unpack_payload(payload, "H H H H B I I H")
        return GetAlarm(
            HERTZ.to_si(start_frequency),
            HERTZ.to_si(end_frequency),
            HERTZ.to_si(step_size),
            ms_to_seconds(step_delay),
            volume,
            AlarmDuration(duration),
            AlarmDuration(duration_remaining),
            HERTZ.to_si(current_frequency),
        )

    async def update_volume(self, volume: int, response_expected: bool = True) -> None:
        """
        Updates the volume of an ongoing beep or alarm.
        """
        volume = int(volume)
        check_range("volume", volume, 0, 10)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.UPDATE_VOLUME,
            data=pack_payload((volume,), "B"),
            response_expected=response_expected,
        )

    async def update_frequency(self, frequency: float | Decimal, response_expected: bool = True) -> None:
        """
        Updates the frequency of an ongoing beep.

        Units: frequency in Hz (50 to 15000 Hz).
        """
        frequency_raw = HERTZ.from_si(frequency)
        check_range("frequency", frequency_raw, 50, 15000, frequency)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.UPDATE_FREQUENCY,
            data=pack_payload((frequency_raw,), "H"),
            response_expected=response_expected,
        )

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.BEEP_FINISHED:
            return 0, None
        return 1, None
