"""
Module for the Tinkerforge Thermal Imaging Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/ThermalImaging_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, Event, _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
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

    HIGH_CONTRAST_IMAGE = 12
    TEMPERATURE_IMAGE = 13


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_HIGH_CONTRAST_IMAGE_LOW_LEVEL = 1
    GET_TEMPERATURE_IMAGE_LOW_LEVEL = 2
    GET_STATISTICS = 3
    SET_RESOLUTION = 4
    GET_RESOLUTION = 5
    SET_SPOTMETER_CONFIG = 6
    GET_SPOTMETER_CONFIG = 7
    SET_HIGH_CONTRAST_CONFIG = 8
    GET_HIGH_CONTRAST_CONFIG = 9
    SET_IMAGE_TRANSFER_CONFIG = 10
    GET_IMAGE_TRANSFER_CONFIG = 11
    SET_FLUX_LINEAR_PARAMETERS = 14
    GET_FLUX_LINEAR_PARAMETERS = 15
    SET_FFC_SHUTTER_MODE = 16
    GET_FFC_SHUTTER_MODE = 17
    RUN_FFC_NORMALIZATION = 18


@unique
class Resolution(Enum):
    """
    The resolution options
    """

    RESOLUTION_0_TO_6553_KELVIN = 0
    RESOLUTION_0_TO_655_KELVIN = 1


@unique
class FFCStatus(Enum):
    """
    The ffc status options
    """

    NEVER_COMMANDED = 0
    IMMINENT = 1
    IN_PROGRESS = 2
    COMPLETE = 3


@unique
class ImageTransfer(Enum):
    """
    The image transfer options
    """

    MANUAL_HIGH_CONTRAST_IMAGE = 0
    MANUAL_TEMPERATURE_IMAGE = 1
    CALLBACK_HIGH_CONTRAST_IMAGE = 2
    CALLBACK_TEMPERATURE_IMAGE = 3


@unique
class ShutterMode(Enum):
    """
    The shutter mode options
    """

    MANUAL = 0
    AUTO = 1
    EXTERNAL = 2


@unique
class ShutterLockout(Enum):
    """
    The shutter lockout options
    """

    INACTIVE = 0
    HIGH = 1
    LOW = 2


class GetHighContrastImage(NamedTuple):
    image_chunk_offset: int
    image_chunk_data: tuple[int, ...]


class GetTemperatureImage(NamedTuple):
    image_chunk_offset: int
    image_chunk_data: tuple[int, ...]


class GetStatistics(NamedTuple):
    spotmeter_statistics: tuple[int, ...]
    temperatures: tuple[int, ...]
    resolution: Resolution
    ffc_status: FFCStatus
    temperature_warning: tuple[bool, ...]


class GetHighContrastConfig(NamedTuple):
    region_of_interest: tuple[int, ...]
    dampening_factor: int
    clip_limit: tuple[int, ...]
    empty_counts: int


class GetFluxLinearParameters(NamedTuple):
    scene_emissivity: Decimal
    temperature_background: Decimal
    tau_window: Decimal
    temperatur_window: Decimal
    tau_atmosphere: Decimal
    temperature_atmosphere: Decimal
    reflection_window: Decimal
    temperature_reflection: Decimal


class GetFFCShutterMode(NamedTuple):
    shutter_mode: ShutterMode
    temp_lockout_state: ShutterLockout
    video_freeze_during_ffc: bool
    ffc_desired: bool
    elapsed_time_since_last_ffc: Decimal
    desired_ffc_period: Decimal
    explicit_cmd_to_open: bool
    desired_ffc_temp_delta: Decimal
    imminent_delay: int


DESIRED_FFC_TEMP_DELTA = LinearQuantity(1, 100)  # raw: 1/100 Kelvin, returned in K
REFLECTION_WINDOW = LinearQuantity(25, 2048)  # raw: 25/2048 Percent, returned in %
SCENE_EMISSIVITY = LinearQuantity(25, 2048)  # raw: 25/2048 Percent, returned in %
TAU_ATMOSPHERE = LinearQuantity(25, 2048)  # raw: 25/2048 Percent, returned in %
TAU_WINDOW = LinearQuantity(25, 2048)  # raw: 25/2048 Percent, returned in %
TEMPERATURE_ATMOSPHERE = LinearQuantity(1, 100)  # raw: 1/100 Kelvin, returned in K
TEMPERATURE_BACKGROUND = LinearQuantity(1, 100)  # raw: 1/100 Kelvin, returned in K
TEMPERATURE_REFLECTION = LinearQuantity(1, 100)  # raw: 1/100 Kelvin, returned in K
TEMPERATUR_WINDOW = LinearQuantity(1, 100)  # raw: 1/100 Kelvin, returned in K


class BrickletThermalImaging(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    80x60 pixel thermal imaging camera
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_THERMAL_IMAGING
    DEVICE_DISPLAY_NAME = "Thermal Imaging Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Resolution: TypeAlias = Resolution
    FFCStatus: TypeAlias = FFCStatus
    ImageTransfer: TypeAlias = ImageTransfer
    ShutterMode: TypeAlias = ShutterMode
    ShutterLockout: TypeAlias = ShutterLockout

    CALLBACK_FORMATS = {
        CallbackID.HIGH_CONTRAST_IMAGE: "H 62B",
        CallbackID.TEMPERATURE_IMAGE: "H 31H",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.HIGH_CONTRAST_IMAGE,)),
        Channel(1, callbacks=(CallbackID.TEMPERATURE_IMAGE,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 2)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()
        self._stream_assemblers = {
            CallbackID.HIGH_CONTRAST_IMAGE: StreamAssembler(),
            CallbackID.TEMPERATURE_IMAGE: StreamAssembler(),
        }

    async def get_high_contrast_image_low_level(self) -> GetHighContrastImage:
        """
        Returns the current high contrast image. See `here
        <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image>`__
        for the difference between
        High Contrast and Temperature Image. If you don't know what to use
        the High Contrast Image is probably right for you.

        The data is organized as a 8-bit value 80x60 pixel matrix linearized in
        a one-dimensional array. The data is arranged line by line from top left to
        bottom right.

        Each 8-bit value represents one gray-scale image pixel that can directly be
        shown to a user on a display.

        Before you can use this function you have to enable it with
        :func:`set_image_transfer_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HIGH_CONTRAST_IMAGE_LOW_LEVEL, response_expected=True
        )
        image_chunk_offset, image_chunk_data = unpack_payload(payload, "H 62B")
        return GetHighContrastImage(image_chunk_offset, tuple(image_chunk_data))

    async def get_high_contrast_image(self) -> bytes:
        """
        Returns the current high contrast image. See `here
        <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image>`__
        for the difference between
        High Contrast and Temperature Image. If you don't know what to use
        the High Contrast Image is probably right for you.

        The data is organized as a 8-bit value 80x60 pixel matrix linearized in
        a one-dimensional array. The data is arranged line by line from top left to
        bottom right.

        Each 8-bit value represents one gray-scale image pixel that can directly be
        shown to a user on a display.

        Before you can use this function you have to enable it with
        :func:`set_image_transfer_config`.

        This function transfers the complete image stream and calls :func:`get_high_contrast_image_low_level` as often
        as necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.get_high_contrast_image_low_level()
            return Chunk(4800, result.image_chunk_offset, result.image_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="image", chunk_size=62, empty_offset=65535)
        return bytes(data)

    async def get_temperature_image_low_level(self) -> GetTemperatureImage:
        """
        Returns the current temperature image. See `here
        <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image>`__
        for the difference between High Contrast and Temperature Image.
        If you don't know what to use the High Contrast Image is probably right for you.

        The data is organized as a 16-bit value 80x60 pixel matrix linearized in
        a one-dimensional array. The data is arranged line by line from top left to
        bottom right.

        Each 16-bit value represents one temperature measurement in either
        Kelvin/10 or Kelvin/100 (depending on the resolution set with :func:`set_resolution`).

        Before you can use this function you have to enable it with
        :func:`set_image_transfer_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_IMAGE_LOW_LEVEL, response_expected=True
        )
        image_chunk_offset, image_chunk_data = unpack_payload(payload, "H 31H")
        return GetTemperatureImage(image_chunk_offset, tuple(image_chunk_data))

    async def get_temperature_image(self) -> tuple[int, ...]:
        """
        Returns the current temperature image. See `here
        <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image>`__
        for the difference between High Contrast and Temperature Image.
        If you don't know what to use the High Contrast Image is probably right for you.

        The data is organized as a 16-bit value 80x60 pixel matrix linearized in
        a one-dimensional array. The data is arranged line by line from top left to
        bottom right.

        Each 16-bit value represents one temperature measurement in either
        Kelvin/10 or Kelvin/100 (depending on the resolution set with :func:`set_resolution`).

        Before you can use this function you have to enable it with
        :func:`set_image_transfer_config`.

        This function transfers the complete image stream and calls :func:`get_temperature_image_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.get_temperature_image_low_level()
            return Chunk(4800, result.image_chunk_offset, result.image_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="image", chunk_size=31, empty_offset=65535)
        return tuple(data)

    async def get_statistics(self) -> GetStatistics:
        """
        Returns the spotmeter statistics, various temperatures, current resolution and status bits.

        The spotmeter statistics are:

        * Index 0: Mean Temperature.
        * Index 1: Maximum Temperature.
        * Index 2: Minimum Temperature.
        * Index 3: Pixel Count of spotmeter region of interest.

        The temperatures are:

        * Index 0: Focal Plain Array temperature.
        * Index 1: Focal Plain Array temperature at last FFC (Flat Field Correction).
        * Index 2: Housing temperature.
        * Index 3: Housing temperature at last FFC.

        The resolution is either `0 to 6553 Kelvin` or `0 to 655 Kelvin`. If the resolution is the former,
        the temperatures are in Kelvin/10, if it is the latter the temperatures are in Kelvin/100.

        FFC (Flat Field Correction) Status:

        * FFC Never Commanded: Only seen on startup before first FFC.
        * FFC Imminent: This state is entered 2 seconds prior to initiating FFC.
        * FFC In Progress: Flat field correction is started (shutter moves in front of lens and back). Takes about 1
          second.
        * FFC Complete: Shutter is in waiting position again, FFC done.

        Temperature warning bits:

        * Index 0: Shutter lockout (if true shutter is locked out because temperature is outside 263.15 K to 338.15 K)
        * Index 1: Overtemperature shut down imminent (goes true 10 seconds before shutdown)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATISTICS, response_expected=True
        )
        spotmeter_statistics, temperatures, resolution, ffc_status, temperature_warning = unpack_payload(
            payload, "4H 4H B B 2!"
        )
        return GetStatistics(
            tuple(spotmeter_statistics),
            tuple(temperatures),
            Resolution(resolution),
            FFCStatus(ffc_status),
            tuple(temperature_warning),
        )

    async def set_resolution(
        self, resolution: Resolution | int = Resolution.RESOLUTION_0_TO_655_KELVIN, response_expected: bool = True
    ) -> None:
        """
        Sets the resolution. The Thermal Imaging Bricklet can either measure

        * from 0 to 6553 Kelvin (0 K to 6553 K) with 0.1 K resolution or
        * from 0 to 655 Kelvin (0 K to 655 K) with 0.01 K resolution.

        The accuracy is specified for 263.15 K to 723.15 K in the
        first range and 263.15 K and 413.15 K in the second range.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RESOLUTION,
            data=pack_payload((Resolution(resolution).value,), "B"),
            response_expected=response_expected,
        )

    async def get_resolution(self) -> Resolution:
        """
        Returns the resolution as set by :func:`set_resolution`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RESOLUTION, response_expected=True
        )
        return Resolution(unpack_payload(payload, "B"))

    async def set_spotmeter_config(
        self, region_of_interest: bytes | Sequence[int], response_expected: bool = True
    ) -> None:
        """
        Sets the spotmeter region of interest. The 4 values are

        * Index 0: Column start (has to be smaller than column end).
        * Index 1: Row start (has to be smaller than row end).
        * Index 2: Column end (has to be smaller than 80).
        * Index 3: Row end (has to be smaller than 60).

        The spotmeter statistics can be read out with :func:`get_statistics`.
        """
        check_length("region_of_interest", region_of_interest, 4)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPOTMETER_CONFIG,
            data=pack_payload((list(map(int, region_of_interest)),), "4B"),
            response_expected=response_expected,
        )

    async def get_spotmeter_config(self) -> tuple[int, ...]:
        """
        Returns the spotmeter config as set by :func:`set_spotmeter_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPOTMETER_CONFIG, response_expected=True
        )
        return tuple(unpack_payload(payload, "4B"))

    async def set_high_contrast_config(
        self,
        region_of_interest: bytes | Sequence[int],
        dampening_factor: int,
        clip_limit: Sequence[int],
        empty_counts: int = 2,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the high contrast region of interest, dampening factor, clip limit and empty counts.
        This config is only used in high contrast mode (see :func:`set_image_transfer_config`).

        The high contrast region of interest consists of four values:

        * Index 0: Column start (has to be smaller than or equal to column end).
        * Index 1: Row start (has to be smaller than row end).
        * Index 2: Column end (has to be smaller than 80).
        * Index 3: Row end (has to be smaller than 60).

        The algorithm to generate the high contrast image is applied to this region.

        Dampening Factor: This parameter is the amount of temporal dampening applied to the HEQ
        (history equalization) transformation function. An IIR filter of the form::

         (N / 256) * previous + ((256 - N) / 256) * current

        is applied, and the HEQ dampening factor
        represents the value N in the equation, i.e., a value that applies to the amount of
        influence the previous HEQ transformation function has on the current function. The
        lower the value of N the higher the influence of the current video frame whereas
        the higher the value of N the more influence the previous damped transfer function has.

        Clip Limit Index 0 (AGC HEQ Clip Limit High): This parameter defines the maximum number of pixels allowed
        to accumulate in any given histogram bin. Any additional pixels in a given bin are clipped.
        The effect of this parameter is to limit the influence of highly-populated bins on the
        resulting HEQ transformation function.

        Clip Limit Index 1 (AGC HEQ Clip Limit Low): This parameter defines an artificial population that is added to
        every non-empty histogram bin. In other words, if the Clip Limit Low is set to L, a bin
        with an actual population of X will have an effective population of L + X. Any empty bin
        that is nearby a populated bin will be given an artificial population of L. The effect of
        higher values is to provide a more linear transfer function; lower values provide a more
        non-linear (equalized) transfer function.

        Empty Counts: This parameter specifies the maximum number of pixels in a bin that will be
        interpreted as an empty bin. Histogram bins with this number of pixels or less will be
        processed as an empty bin.
        """
        check_length("region_of_interest", region_of_interest, 4)
        dampening_factor = int(dampening_factor)
        check_range("dampening_factor", dampening_factor, 0, 256)
        check_length("clip_limit", clip_limit, 2)
        empty_counts = int(empty_counts)
        check_range("empty_counts", empty_counts, 0, 16383)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HIGH_CONTRAST_CONFIG,
            data=pack_payload(
                (list(map(int, region_of_interest)), dampening_factor, list(map(int, clip_limit)), empty_counts),
                "4B H 2H H",
            ),
            response_expected=response_expected,
        )

    async def get_high_contrast_config(self) -> GetHighContrastConfig:
        """
        Returns the high contrast config as set by :func:`set_high_contrast_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HIGH_CONTRAST_CONFIG, response_expected=True
        )
        region_of_interest, dampening_factor, clip_limit, empty_counts = unpack_payload(payload, "4B H 2H H")
        return GetHighContrastConfig(tuple(region_of_interest), dampening_factor, tuple(clip_limit), empty_counts)

    async def set_image_transfer_config(
        self, config: ImageTransfer | int = ImageTransfer.MANUAL_HIGH_CONTRAST_IMAGE, response_expected: bool = True
    ) -> None:
        """
        The necessary bandwidth of this Bricklet is too high to use getter/callback or
        high contrast/temperature image at the same time. You have to configure the one
        you want to use, the Bricklet will optimize the internal configuration accordingly.

        Corresponding functions:

        * Manual High Contrast Image: :func:`get_high_contrast_image`.
        * Manual Temperature Image: :func:`get_temperature_image`.
        * Callback High Contrast Image: :attr:`CallbackID.HIGH_CONTRAST_IMAGE` callback.
        * Callback Temperature Image: :attr:`CallbackID.TEMPERATURE_IMAGE` callback.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_IMAGE_TRANSFER_CONFIG,
            data=pack_payload((ImageTransfer(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_image_transfer_config(self) -> ImageTransfer:
        """
        Returns the image transfer config, as set by :func:`set_image_transfer_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_IMAGE_TRANSFER_CONFIG, response_expected=True
        )
        return ImageTransfer(unpack_payload(payload, "B"))

    async def set_flux_linear_parameters(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        scene_emissivity: float | Decimal = 100,
        temperature_background: float | Decimal = Decimal("295.15"),
        tau_window: float | Decimal = 100,
        temperatur_window: float | Decimal = Decimal("295.15"),
        tau_atmosphere: float | Decimal = 100,
        temperature_atmosphere: float | Decimal = Decimal("295.15"),
        reflection_window: float | Decimal = 0,
        temperature_reflection: float | Decimal = Decimal("295.15"),
        response_expected: bool = True,
    ) -> None:
        """
        Sets the flux linear parameters that can be used for radiometry calibration.

        See FLIR document 102-PS245-100-01 for more details.

        Units: scene_emissivity in % (1.000976562 to 100 %), temperature_background in K, tau_window in % (1.000976562
        to 100 %), temperatur_window in K, tau_atmosphere in % (1.000976562 to 100 %), temperature_atmosphere in K,
        reflection_window in % (0 to 100 %), temperature_reflection in K.

        .. versionadded:: 2.0.5 (Firmware)
        """
        scene_emissivity_raw = SCENE_EMISSIVITY.from_si(scene_emissivity)
        check_range("scene_emissivity", scene_emissivity_raw, 82, 8192, scene_emissivity)
        temperature_background_raw = TEMPERATURE_BACKGROUND.from_si(temperature_background)
        check_range("temperature_background", temperature_background_raw, 0, 65535, temperature_background)
        tau_window_raw = TAU_WINDOW.from_si(tau_window)
        check_range("tau_window", tau_window_raw, 82, 8192, tau_window)
        temperatur_window_raw = TEMPERATUR_WINDOW.from_si(temperatur_window)
        check_range("temperatur_window", temperatur_window_raw, 0, 65535, temperatur_window)
        tau_atmosphere_raw = TAU_ATMOSPHERE.from_si(tau_atmosphere)
        check_range("tau_atmosphere", tau_atmosphere_raw, 82, 8192, tau_atmosphere)
        temperature_atmosphere_raw = TEMPERATURE_ATMOSPHERE.from_si(temperature_atmosphere)
        check_range("temperature_atmosphere", temperature_atmosphere_raw, 0, 65535, temperature_atmosphere)
        reflection_window_raw = REFLECTION_WINDOW.from_si(reflection_window)
        check_range("reflection_window", reflection_window_raw, 0, 8192, reflection_window)
        temperature_reflection_raw = TEMPERATURE_REFLECTION.from_si(temperature_reflection)
        check_range("temperature_reflection", temperature_reflection_raw, 0, 65535, temperature_reflection)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FLUX_LINEAR_PARAMETERS,
            data=pack_payload(
                (
                    scene_emissivity_raw,
                    temperature_background_raw,
                    tau_window_raw,
                    temperatur_window_raw,
                    tau_atmosphere_raw,
                    temperature_atmosphere_raw,
                    reflection_window_raw,
                    temperature_reflection_raw,
                ),
                "H H H H H H H H",
            ),
            response_expected=response_expected,
        )

    async def get_flux_linear_parameters(self) -> GetFluxLinearParameters:
        """
        Returns the flux linear parameters, as set by :func:`set_flux_linear_parameters`.

        Units: scene_emissivity in % (1.000976562 to 100 %), temperature_background in K, tau_window in % (1.000976562
        to 100 %), temperatur_window in K, tau_atmosphere in % (1.000976562 to 100 %), temperature_atmosphere in K,
        reflection_window in % (0 to 100 %), temperature_reflection in K.

        .. versionadded:: 2.0.5 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FLUX_LINEAR_PARAMETERS, response_expected=True
        )
        (
            scene_emissivity,
            temperature_background,
            tau_window,
            temperatur_window,
            tau_atmosphere,
            temperature_atmosphere,
            reflection_window,
            temperature_reflection,
        ) = unpack_payload(payload, "H H H H H H H H")
        return GetFluxLinearParameters(
            SCENE_EMISSIVITY.to_si(scene_emissivity),
            TEMPERATURE_BACKGROUND.to_si(temperature_background),
            TAU_WINDOW.to_si(tau_window),
            TEMPERATUR_WINDOW.to_si(temperatur_window),
            TAU_ATMOSPHERE.to_si(tau_atmosphere),
            TEMPERATURE_ATMOSPHERE.to_si(temperature_atmosphere),
            REFLECTION_WINDOW.to_si(reflection_window),
            TEMPERATURE_REFLECTION.to_si(temperature_reflection),
        )

    async def set_ffc_shutter_mode(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        shutter_mode: ShutterMode | int = ShutterMode.AUTO,
        temp_lockout_state: ShutterLockout | int = ShutterLockout.INACTIVE,
        video_freeze_during_ffc: bool = True,
        ffc_desired: bool = False,
        elapsed_time_since_last_ffc: Duration = 0,
        desired_ffc_period: Duration = 300,
        explicit_cmd_to_open: bool = False,
        desired_ffc_temp_delta: float | Decimal = 3,
        imminent_delay: int = 52,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the FFC shutter mode parameters.

        See FLIR document 110-0144-03 4.5.15 for more details.

        Units: elapsed_time_since_last_ffc in s, desired_ffc_period in s, desired_ffc_temp_delta in K.

        .. versionadded:: 2.0.6 (Firmware)
        """
        elapsed_time_since_last_ffc_raw = seconds_to_ms(elapsed_time_since_last_ffc)
        check_range(
            "elapsed_time_since_last_ffc", elapsed_time_since_last_ffc_raw, 0, 4294967295, elapsed_time_since_last_ffc
        )
        desired_ffc_period_raw = seconds_to_ms(desired_ffc_period)
        check_range("desired_ffc_period", desired_ffc_period_raw, 0, 4294967295, desired_ffc_period)
        desired_ffc_temp_delta_raw = DESIRED_FFC_TEMP_DELTA.from_si(desired_ffc_temp_delta)
        check_range("desired_ffc_temp_delta", desired_ffc_temp_delta_raw, 0, 65535, desired_ffc_temp_delta)
        imminent_delay = int(imminent_delay)
        check_range("imminent_delay", imminent_delay, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FFC_SHUTTER_MODE,
            data=pack_payload(
                (
                    ShutterMode(shutter_mode).value,
                    ShutterLockout(temp_lockout_state).value,
                    bool(video_freeze_during_ffc),
                    bool(ffc_desired),
                    elapsed_time_since_last_ffc_raw,
                    desired_ffc_period_raw,
                    bool(explicit_cmd_to_open),
                    desired_ffc_temp_delta_raw,
                    imminent_delay,
                ),
                "B B ! ! I I ! H H",
            ),
            response_expected=response_expected,
        )

    async def get_ffc_shutter_mode(self) -> GetFFCShutterMode:
        """
        Sets the FFC shutter mode parameters.

        See FLIR document 110-0144-03 4.5.15 for more details.

        Units: elapsed_time_since_last_ffc in s, desired_ffc_period in s, desired_ffc_temp_delta in K.

        .. versionadded:: 2.0.6 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FFC_SHUTTER_MODE, response_expected=True
        )
        (
            shutter_mode,
            temp_lockout_state,
            video_freeze_during_ffc,
            ffc_desired,
            elapsed_time_since_last_ffc,
            desired_ffc_period,
            explicit_cmd_to_open,
            desired_ffc_temp_delta,
            imminent_delay,
        ) = unpack_payload(payload, "B B ! ! I I ! H H")
        return GetFFCShutterMode(
            ShutterMode(shutter_mode),
            ShutterLockout(temp_lockout_state),
            video_freeze_during_ffc,
            ffc_desired,
            ms_to_seconds(elapsed_time_since_last_ffc),
            ms_to_seconds(desired_ffc_period),
            explicit_cmd_to_open,
            DESIRED_FFC_TEMP_DELTA.to_si(desired_ffc_temp_delta),
            imminent_delay,
        )

    async def run_ffc_normalization(self, response_expected: bool = True) -> None:
        """
        Starts the Flat-Field Correction (FFC) normalization.

        See FLIR document 110-0144-03 4.5.16 for more details.

        .. versionadded:: 2.0.6 (Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.RUN_FFC_NORMALIZATION, response_expected=response_expected
        )

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        raise NotImplementedError  # All callbacks are streams, see _to_events()

    def _to_events(  # pylint: disable=too-many-locals,too-many-return-statements,too-many-branches
        self, callback_id: CallbackID, value: Any, sids: Sequence[int] | None
    ) -> Iterable[Event]:
        if callback_id is CallbackID.HIGH_CONTRAST_IMAGE:
            image_chunk_offset, image_chunk_data = value
            data = self._stream_assemblers[CallbackID.HIGH_CONTRAST_IMAGE].add(
                4800, image_chunk_offset, image_chunk_data
            )
            if data is None:
                return ()
            return (Event(self, 0, callback_id, bytes(data)),)
        if callback_id is CallbackID.TEMPERATURE_IMAGE:
            image_chunk_offset, image_chunk_data = value
            data = self._stream_assemblers[CallbackID.TEMPERATURE_IMAGE].add(4800, image_chunk_offset, image_chunk_data)
            if data is None:
                return ()
            return (Event(self, 1, callback_id, tuple(data)),)
        raise AssertionError(f"Unknown callback {callback_id}")
