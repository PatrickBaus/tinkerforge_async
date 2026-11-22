"""
Module for the Tinkerforge OLED 128x64 Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/OLED128x64V2_Bricklet_Python.html) implemented using
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
from collections.abc import Sequence
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, DeviceIdentifier, _FunctionID
from .helper import check_length, check_range, encode_string
from .ip_connection_helper import pack_payload, unpack_payload
from .streams import Chunk, read_stream, write_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    WRITE_PIXELS_LOW_LEVEL = 1
    READ_PIXELS_LOW_LEVEL = 2
    CLEAR_DISPLAY = 3
    SET_DISPLAY_CONFIGURATION = 4
    GET_DISPLAY_CONFIGURATION = 5
    WRITE_LINE = 6
    DRAW_BUFFERED_FRAME = 7
    WRITE_LINE_2 = 8


class ReadPixels(NamedTuple):
    pixels_length: int
    pixels_chunk_offset: int
    pixels_chunk_data: tuple[bool, ...]


class GetDisplayConfiguration(NamedTuple):
    contrast: int
    invert: bool
    automatic_draw: bool


class BrickletOLED128x64V2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    0.033 m (1.3") OLED display with 128x64 pixels
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_OLED_128X64_V2
    DEVICE_DISPLAY_NAME = "OLED 128x64 Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {}

    SID_TO_CALLBACK = {}

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()

    async def write_pixels_low_level(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        x_start: int,
        y_start: int,
        x_end: int,
        y_end: int,
        pixels_length: int,
        pixels_chunk_offset: int,
        pixels_chunk_data: Sequence[bool],
        response_expected: bool = True,
    ) -> None:
        """
        Writes pixels to the specified window.

        The pixels are written into the window line by line top to bottom
        and each line is written from left to right.

        If automatic draw is enabled (default) the pixels are directly written to
        the screen. Only pixels that have actually changed are updated on the screen,
        the rest stays the same.

        If automatic draw is disabled the pixels are written to an internal buffer and
        the buffer is transferred to the display only after :func:`draw_buffered_frame`
        is called. This can be used to avoid flicker when drawing a complex frame in
        multiple steps.

        Automatic draw can be configured with the :func:`set_display_configuration`
        function.
        """
        x_start = int(x_start)
        check_range("x_start", x_start, 0, 127)
        y_start = int(y_start)
        check_range("y_start", y_start, 0, 63)
        x_end = int(x_end)
        check_range("x_end", x_end, 0, 127)
        y_end = int(y_end)
        check_range("y_end", y_end, 0, 63)
        pixels_length = int(pixels_length)
        check_range("pixels_length", pixels_length, 0, 8192)
        pixels_chunk_offset = int(pixels_chunk_offset)
        check_range("pixels_chunk_offset", pixels_chunk_offset, 0, 65535)
        check_length("pixels_chunk_data", pixels_chunk_data, 448)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_PIXELS_LOW_LEVEL,
            data=pack_payload(
                (
                    x_start,
                    y_start,
                    x_end,
                    y_end,
                    pixels_length,
                    pixels_chunk_offset,
                    [bool(item) for item in pixels_chunk_data],
                ),
                "B B B B H H 448!",
            ),
            response_expected=response_expected,
        )

    async def write_pixels(self, x_start: int, y_start: int, x_end: int, y_end: int, pixels: Sequence[bool]) -> None:
        """
        Writes pixels to the specified window.

        The pixels are written into the window line by line top to bottom
        and each line is written from left to right.

        If automatic draw is enabled (default) the pixels are directly written to
        the screen. Only pixels that have actually changed are updated on the screen,
        the rest stays the same.

        If automatic draw is disabled the pixels are written to an internal buffer and
        the buffer is transferred to the display only after :func:`draw_buffered_frame`
        is called. This can be used to avoid flicker when drawing a complex frame in
        multiple steps.

        Automatic draw can be configured with the :func:`set_display_configuration`
        function.

        This function transfers the complete pixels stream and calls :func:`write_pixels_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.write_pixels_low_level(x_start, y_start, x_end, y_end, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk,
                [bool(item) for item in pixels],
                name="pixels",
                chunk_size=448,
                padding=False,
                max_length=65535,
            )

    async def read_pixels_low_level(self, x_start: int, y_start: int, x_end: int, y_end: int) -> ReadPixels:
        """
        Reads pixels from the specified window.

        The pixels are read from the window line by line top to bottom
        and each line is read from left to right.

        If automatic draw is enabled (default) the pixels that are read are always the
        same that are shown on the display.

        If automatic draw is disabled the pixels are read from the internal buffer
        (see :func:`draw_buffered_frame`).

        Automatic draw can be configured with the :func:`set_display_configuration`
        function.
        """
        x_start = int(x_start)
        check_range("x_start", x_start, 0, 127)
        y_start = int(y_start)
        check_range("y_start", y_start, 0, 63)
        x_end = int(x_end)
        check_range("x_end", x_end, 0, 127)
        y_end = int(y_end)
        check_range("y_end", y_end, 0, 63)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_PIXELS_LOW_LEVEL,
            data=pack_payload((x_start, y_start, x_end, y_end), "B B B B"),
            response_expected=True,
        )
        pixels_length, pixels_chunk_offset, pixels_chunk_data = unpack_payload(payload, "H H 480!")
        return ReadPixels(pixels_length, pixels_chunk_offset, tuple(pixels_chunk_data))

    async def read_pixels(self, x_start: int, y_start: int, x_end: int, y_end: int) -> tuple[bool, ...]:
        """
        Reads pixels from the specified window.

        The pixels are read from the window line by line top to bottom
        and each line is read from left to right.

        If automatic draw is enabled (default) the pixels that are read are always the
        same that are shown on the display.

        If automatic draw is disabled the pixels are read from the internal buffer
        (see :func:`draw_buffered_frame`).

        Automatic draw can be configured with the :func:`set_display_configuration`
        function.

        This function transfers the complete pixels stream and calls :func:`read_pixels_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.read_pixels_low_level(x_start, y_start, x_end, y_end)
            return Chunk(result.pixels_length, result.pixels_chunk_offset, result.pixels_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="pixels", chunk_size=480)
        return tuple(data)

    async def clear_display(self, response_expected: bool = True) -> None:
        """
        Clears the complete content of the display.

        If automatic draw is enabled (default) the pixels are directly cleared.

        If automatic draw is disabled the the internal buffer is cleared and
        the buffer is transferred to the display only after :func:`draw_buffered_frame`
        is called. This can be used to avoid flicker when drawing a complex frame in
        multiple steps.

        Automatic draw can be configured with the :func:`set_display_configuration`
        function.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.CLEAR_DISPLAY, response_expected=response_expected
        )

    async def set_display_configuration(
        self, contrast: int = 143, invert: bool = False, automatic_draw: bool = True, response_expected: bool = True
    ) -> None:
        """
        Sets the configuration of the display.

        You can set a contrast value from 0 to 255 and you can invert the color
        (white/black) of the display.

        If automatic draw is set to *true*, the display is automatically updated with every
        call of :func:`write_pixels` or :func:`write_line`. If it is set to false, the
        changes are written into an internal buffer and only shown on the display after
        a call of :func:`draw_buffered_frame`.
        """
        contrast = int(contrast)
        check_range("contrast", contrast, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISPLAY_CONFIGURATION,
            data=pack_payload((contrast, bool(invert), bool(automatic_draw)), "B ! !"),
            response_expected=response_expected,
        )

    async def get_display_configuration(self) -> GetDisplayConfiguration:
        """
        Returns the configuration as set by :func:`set_display_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISPLAY_CONFIGURATION, response_expected=True
        )
        contrast, invert, automatic_draw = unpack_payload(payload, "B ! !")
        return GetDisplayConfiguration(contrast, invert, automatic_draw)

    async def write_line(self, line: int, position: int, text: str, response_expected: bool = True) -> None:
        """
        .. note::
         This function is deprecated and only here for backward compatibility.
         Since firmware version 2.0.5 we recommend :func:`write_line_2`.
         It has an additional parameter for letter spacing.

        Writes text to a specific line with a specific position.
        The text can have a maximum of 22 characters.

        For example: (1, 10, "Hello") will write *Hello* in the middle of the
        second line of the display.

        The display uses a special 5x7 pixel charset. You can view the characters
        of the charset in Brick Viewer.

        If automatic draw is enabled (default) the text is directly written to
        the screen. Only pixels that have actually changed are updated on the screen,
        the rest stays the same.

        If automatic draw is disabled the text is written to an internal buffer and
        the buffer is transferred to the display only after :func:`draw_buffered_frame`
        is called. This can be used to avoid flicker when drawing a complex frame in
        multiple steps.

        Automatic draw can be configured with the :func:`set_display_configuration`
        function.

        The font conforms to code page 437.
        """
        line = int(line)
        check_range("line", line, 0, 7)
        position = int(position)
        check_range("position", position, 0, 21)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_LINE,
            data=pack_payload((line, position, encode_string("text", text, 22)), "B B 22s"),
            response_expected=response_expected,
        )

    async def draw_buffered_frame(self, force_complete_redraw: bool, response_expected: bool = True) -> None:
        """
        Draws the currently buffered frame. Normally each call of :func:`write_pixels` and
        :func:`write_line` draws directly onto the display. If you turn automatic draw off
        (:func:`set_display_configuration`), the data is written in an internal buffer and
        only transferred to the display by calling this function. This can be used to
        avoid flicker when drawing a complex frame in multiple steps.

        Set the `force complete redraw` to *true* to redraw the whole display
        instead of only the changed parts. Normally it should not be necessary to set this to
        *true*. It may only become necessary in case of stuck pixels because of errors.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DRAW_BUFFERED_FRAME,
            data=pack_payload((bool(force_complete_redraw),), "!"),
            response_expected=response_expected,
        )

    async def write_line_2(
        self, line: int, position: int, letter_spacing: int, text: str, response_expected: bool = True
    ) -> None:
        """
        Writes text to a specific line with a specific position.
        The text can have a maximum of 26 characters.

        With a letter spacing of 0, a maximum of 26 characters can be written and
        with a letter spacing of 1 a maximum of 22 characters can be written.

        For example: (1, 10, "Hello") will write *Hello* in the middle of the
        second line of the display.

        The display uses a special 5x7 pixel charset. You can view the characters
        of the charset in Brick Viewer.

        If automatic draw is enabled (default) the text is directly written to
        the screen. Only pixels that have actually changed are updated on the screen,
        the rest stays the same.

        If automatic draw is disabled the text is written to an internal buffer and
        the buffer is transferred to the display only after :func:`draw_buffered_frame`
        is called. This can be used to avoid flicker when drawing a complex frame in
        multiple steps.

        Automatic draw can be configured with the :func:`set_display_configuration`
        function.
        """
        line = int(line)
        check_range("line", line, 0, 7)
        position = int(position)
        check_range("position", position, 0, 25)
        letter_spacing = int(letter_spacing)
        check_range("letter_spacing", letter_spacing, 0, 1)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_LINE_2,
            data=pack_payload((line, position, letter_spacing, encode_string("text", text, 26)), "B B B 26s"),
            response_expected=response_expected,
        )
