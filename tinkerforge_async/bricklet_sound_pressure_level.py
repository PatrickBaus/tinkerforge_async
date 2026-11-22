"""
Module for the Tinkerforge Sound Pressure Level Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/SoundPressureLevel_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

import asyncio
from collections.abc import Iterable, Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    Event,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity
from .streams import Chunk, StreamAssembler, read_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    DECIBEL = 4
    SPECTRUM = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_DECIBEL = 1
    SET_DECIBEL_CALLBACK_CONFIGURATION = 2
    GET_DECIBEL_CALLBACK_CONFIGURATION = 3
    GET_SPECTRUM_LOW_LEVEL = 5
    SET_SPECTRUM_CALLBACK_CONFIGURATION = 6
    GET_SPECTRUM_CALLBACK_CONFIGURATION = 7
    SET_CONFIGURATION = 9
    GET_CONFIGURATION = 10


@unique
class FFTSize(Enum):
    """
    The fft size options
    """

    FFT_SIZE_128 = 0
    FFT_SIZE_256 = 1
    FFT_SIZE_512 = 2
    FFT_SIZE_1024 = 3


@unique
class Weighting(Enum):
    """
    The weighting options
    """

    A = 0
    B = 1
    C = 2
    D = 3
    Z = 4
    ITU_R_468 = 5


class GetSpectrum(NamedTuple):
    spectrum_length: int
    spectrum_chunk_offset: int
    spectrum_chunk_data: tuple[int, ...]


class GetConfiguration(NamedTuple):
    fft_size: FFTSize
    weighting: Weighting


DECI_DECIBEL = LinearQuantity(1, 10)  # raw: 1/10 Decibel, returned in dB


class BrickletSoundPressureLevel(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures Sound Pressure Level in dB(A/B/C/D/Z)
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_SOUND_PRESSURE_LEVEL
    DEVICE_DISPLAY_NAME = "Sound Pressure Level Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    FFTSize: TypeAlias = FFTSize
    Weighting: TypeAlias = Weighting

    CALLBACK_FORMATS = {
        CallbackID.DECIBEL: "H",
        CallbackID.SPECTRUM: "H H 30H",
    }

    CHANNELS = (
        Channel(
            0, getter="get_decibel", callbacks=(CallbackID.DECIBEL,), configuration=ChannelConfiguration("decibel")
        ),
        Channel(1, callbacks=(CallbackID.SPECTRUM,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()
        self._stream_assemblers = {
            CallbackID.SPECTRUM: StreamAssembler(),
        }

    async def get_value(self, sid: int) -> Any:
        """
        Returns the value of the channel with the secondary id `sid`. See `CHANNELS` for the channels.
        """
        return await self._get_value(sid)

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the callbacks of the channel with the secondary id `sid`. The thresholds are ignored by
        channels without thresholds.
        """
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return await self._get_callback_configuration(sid)

    async def get_decibel(self) -> Decimal:
        """
        Returns the measured sound pressure in decibels.

        The Bricklet supports the weighting standards dB(A), dB(B), dB(C), dB(D),
        dB(Z) and ITU-R 468. You can configure the weighting with :func:`set_configuration`.

        By default dB(A) will be used.

        Units: decibel in dB (0 to 12 dB).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DECIBEL, response_expected=True
        )
        return DECI_DECIBEL.to_si(unpack_payload(payload, "H"))

    async def set_decibel_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.DECIBEL` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.DECIBEL` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in dB, maximum in dB.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = DECI_DECIBEL.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = DECI_DECIBEL.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DECIBEL_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c H H"
            ),
            response_expected=response_expected,
        )

    async def get_decibel_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_decibel_callback_configuration`.

        Units: minimum in dB, maximum in dB.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DECIBEL_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            DECI_DECIBEL.to_si(minimum),
            DECI_DECIBEL.to_si(maximum),
        )

    async def get_spectrum_low_level(self) -> GetSpectrum:
        """
        Returns the frequency spectrum. The length of the spectrum is between
        512 (FFT size 1024) and 64 (FFT size 128). See :func:`set_configuration`.

        Each array element is one bin of the FFT. The first bin is always the
        DC offset and the other bins have a size between 40Hz (FFT size 1024) and
        320Hz (FFT size 128).

        In sum the frequency of the spectrum always has a range from 0 to
        20480Hz (the FFT is applied to samples with a frequency of 40960Hz).

        The returned data is already equalized, which means that the microphone
        frequency response is compensated and the weighting function is applied
        (see :func:`set_configuration` for the available weighting standards). Use
        dB(Z) if you need the unaltered spectrum.

        The values are not in dB form yet. If you want a proper dB scale of the
        spectrum you have to apply the formula f(x) = 20*log10(max(1, x/sqrt(2)))
        on each value.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPECTRUM_LOW_LEVEL, response_expected=True
        )
        spectrum_length, spectrum_chunk_offset, spectrum_chunk_data = unpack_payload(payload, "H H 30H")
        return GetSpectrum(spectrum_length, spectrum_chunk_offset, tuple(spectrum_chunk_data))

    async def get_spectrum(self) -> tuple[int, ...]:
        """
        Returns the frequency spectrum. The length of the spectrum is between
        512 (FFT size 1024) and 64 (FFT size 128). See :func:`set_configuration`.

        Each array element is one bin of the FFT. The first bin is always the
        DC offset and the other bins have a size between 40Hz (FFT size 1024) and
        320Hz (FFT size 128).

        In sum the frequency of the spectrum always has a range from 0 to
        20480Hz (the FFT is applied to samples with a frequency of 40960Hz).

        The returned data is already equalized, which means that the microphone
        frequency response is compensated and the weighting function is applied
        (see :func:`set_configuration` for the available weighting standards). Use
        dB(Z) if you need the unaltered spectrum.

        The values are not in dB form yet. If you want a proper dB scale of the
        spectrum you have to apply the formula f(x) = 20*log10(max(1, x/sqrt(2)))
        on each value.

        This function transfers the complete spectrum stream and calls :func:`get_spectrum_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.get_spectrum_low_level()
            return Chunk(result.spectrum_length, result.spectrum_chunk_offset, result.spectrum_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="spectrum", chunk_size=30)
        return tuple(data)

    async def set_spectrum_callback_configuration(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        The period is the period with which the :attr:`CallbackID.SPECTRUM` callback is
        triggered periodically. A value of 0 turns the callback off.

        Every new measured spectrum will be send at most once. Set the period to 1 to
        make sure that you get every spectrum.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPECTRUM_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_spectrum_callback_configuration(self) -> Decimal:
        """
        Returns the callback configuration as set by
        :func:`get_spectrum_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPECTRUM_CALLBACK_CONFIGURATION, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_configuration(
        self,
        fft_size: FFTSize | int = FFTSize.FFT_SIZE_1024,
        weighting: Weighting | int = Weighting.A,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the Sound Pressure Level Bricklet configuration.

        With different FFT sizes the Bricklet has a different
        amount of samples per second and the size of the FFT bins
        changes. The higher the FFT size the more precise is the result
        of the dB(X) calculation.

        Available FFT sizes are:

        * 1024: 512 bins, 10 samples per second, each bin has size 40Hz
        * 512: 256 bins, 20 samples per second, each bin has size 80Hz
        * 256: 128 bins, 40 samples per second, each bin has size 160Hz
        * 128: 64 bins, 80 samples per second, each bin has size 320Hz

        The Bricklet supports different weighting functions. You can choose
        between dB(A), dB(B), dB(C), dB(D), dB(Z) and ITU-R 468.

        dB(A/B/C/D) are the standard dB weighting curves. dB(A) is
        often used to measure volumes at concerts etc. dB(Z) has a
        flat response, no weighting is applied. ITU-R 468 is an ITU
        weighting standard mostly used in the UK and Europe.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((FFTSize(fft_size).value, Weighting(weighting).value), "B B"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        fft_size, weighting = unpack_payload(payload, "B B")
        return GetConfiguration(FFTSize(fft_size), Weighting(weighting))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, DECI_DECIBEL.to_si(value)

    @override
    def _to_events(  # pylint: disable=too-many-locals,too-many-return-statements,too-many-branches
        self, callback_id: CallbackID, value: Any, sids: Sequence[int] | None
    ) -> Iterable[Event]:
        if callback_id is CallbackID.SPECTRUM:
            spectrum_length, spectrum_chunk_offset, spectrum_chunk_data = value
            data = self._stream_assemblers[CallbackID.SPECTRUM].add(
                spectrum_length, spectrum_chunk_offset, spectrum_chunk_data
            )
            if data is None:
                return ()
            return (Event(self, 1, callback_id, tuple(data)),)
        return super()._to_events(callback_id, value, sids)
