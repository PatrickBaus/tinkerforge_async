"""
Module for the Tinkerforge E-Paper 296x128 Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/EPaper296x128_Bricklet_Python.html) implemented using
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

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
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

    DRAW_STATUS = 11


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    DRAW = 1
    GET_DRAW_STATUS = 2
    WRITE_BLACK_WHITE_LOW_LEVEL = 3
    READ_BLACK_WHITE_LOW_LEVEL = 4
    WRITE_COLOR_LOW_LEVEL = 5
    READ_COLOR_LOW_LEVEL = 6
    FILL_DISPLAY = 7
    DRAW_TEXT = 8
    DRAW_LINE = 9
    DRAW_BOX = 10
    SET_UPDATE_MODE = 12
    GET_UPDATE_MODE = 13
    SET_DISPLAY_TYPE = 14
    GET_DISPLAY_TYPE = 15
    SET_DISPLAY_DRIVER = 16
    GET_DISPLAY_DRIVER = 17


@unique
class DrawStatus(Enum):
    """
    The draw status options
    """

    IDLE = 0
    COPYING = 1
    DRAWING = 2


class Color(Enum):
    """
    The color options
    """

    BLACK = 0
    WHITE = 1
    RED = 2
    GRAY = 2


@unique
class Font(Enum):
    """
    The font options
    """

    FONT_6X8 = 0
    FONT_6X16 = 1
    FONT_6X24 = 2
    FONT_6X32 = 3
    FONT_12X16 = 4
    FONT_12X24 = 5
    FONT_12X32 = 6
    FONT_18X24 = 7
    FONT_18X32 = 8
    FONT_24X32 = 9


@unique
class Orientation(Enum):
    """
    The orientation options
    """

    HORIZONTAL = 0
    VERTICAL = 1


@unique
class UpdateMode(Enum):
    """
    The update mode options
    """

    DEFAULT = 0
    BLACK_WHITE = 1
    DELTA = 2


@unique
class DisplayType(Enum):
    """
    The display type options
    """

    BLACK_WHITE_RED = 0
    BLACK_WHITE_GRAY = 1


@unique
class DisplayDriver(Enum):
    """
    The display driver options
    """

    SSD1675A = 0
    SSD1680 = 1


class ReadBlackWhite(NamedTuple):
    pixels_length: int
    pixels_chunk_offset: int
    pixels_chunk_data: tuple[bool, ...]


class ReadColor(NamedTuple):
    pixels_length: int
    pixels_chunk_offset: int
    pixels_chunk_data: tuple[bool, ...]


class BrickletEPaper296x128(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Three color 296x128 e-paper display
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_E_PAPER_296X128
    DEVICE_DISPLAY_NAME = "E-Paper 296x128 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    DrawStatus: TypeAlias = DrawStatus
    Color: TypeAlias = Color
    Font: TypeAlias = Font
    Orientation: TypeAlias = Orientation
    UpdateMode: TypeAlias = UpdateMode
    DisplayType: TypeAlias = DisplayType
    DisplayDriver: TypeAlias = DisplayDriver

    CALLBACK_FORMATS = {
        CallbackID.DRAW_STATUS: "B",
    }

    CHANNELS = (Channel(0, getter="get_draw_status", callbacks=(CallbackID.DRAW_STATUS,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()

    async def get_value(self, sid: int) -> Any:
        """
        Returns the value of the channel with the secondary id `sid`. See `CHANNELS` for the channels.
        """
        return await self._get_value(sid)

    async def draw(self, response_expected: bool = True) -> None:
        """
        Draws the current black/white and red or gray buffer to the e-paper display.

        The Bricklet does not have any double-buffering. You should not call
        this function while writing to the buffer. See :func:`get_draw_status`.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.DRAW, response_expected=response_expected)

    async def get_draw_status(self) -> DrawStatus:
        """
        Returns one of three draw statuses:

        * Idle
        * Copying: Data is being copied from the buffer of the Bricklet to the buffer of the display.
        * Drawing: The display is updating its content (during this phase the flickering etc happens).

        You can write to the buffer (through one of the write or draw functions) when the status is
        either *idle* or *drawing*. You should not write to the buffer while it is being *copied* to the
        display. There is no double-buffering.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DRAW_STATUS, response_expected=True
        )
        return DrawStatus(unpack_payload(payload, "B"))

    async def write_black_white_low_level(  # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        Writes black/white pixels to the specified window into the buffer.

        The pixels are written into the window line by line top to bottom
        and each line is written from left to right.

        The value 0 (false) corresponds to a black pixel and the value 1 (true) to a
        white pixel.

        This function writes the pixels into the black/white pixel buffer, to draw the
        buffer to the display use :func:`draw`.

        Use :func:`write_color` to write red or gray pixels.
        """
        x_start = int(x_start)
        check_range("x_start", x_start, 0, 295)
        y_start = int(y_start)
        check_range("y_start", y_start, 0, 127)
        x_end = int(x_end)
        check_range("x_end", x_end, 0, 295)
        y_end = int(y_end)
        check_range("y_end", y_end, 0, 127)
        pixels_length = int(pixels_length)
        check_range("pixels_length", pixels_length, 0, 37888)
        pixels_chunk_offset = int(pixels_chunk_offset)
        check_range("pixels_chunk_offset", pixels_chunk_offset, 0, 65535)
        check_length("pixels_chunk_data", pixels_chunk_data, 432)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_BLACK_WHITE_LOW_LEVEL,
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
                "H B H B H H 432!",
            ),
            response_expected=response_expected,
        )

    async def write_black_white(
        self, x_start: int, y_start: int, x_end: int, y_end: int, pixels: Sequence[bool]
    ) -> None:
        """
        Writes black/white pixels to the specified window into the buffer.

        The pixels are written into the window line by line top to bottom
        and each line is written from left to right.

        The value 0 (false) corresponds to a black pixel and the value 1 (true) to a
        white pixel.

        This function writes the pixels into the black/white pixel buffer, to draw the
        buffer to the display use :func:`draw`.

        Use :func:`write_color` to write red or gray pixels.

        This function transfers the complete pixels stream and calls :func:`write_black_white_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.write_black_white_low_level(x_start, y_start, x_end, y_end, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk,
                [bool(item) for item in pixels],
                name="pixels",
                chunk_size=432,
                padding=False,
                max_length=65535,
            )

    async def read_black_white_low_level(self, x_start: int, y_start: int, x_end: int, y_end: int) -> ReadBlackWhite:
        """
        Returns the current content of the black/white pixel buffer for the specified window.

        The pixels are read into the window line by line top to bottom and
        each line is read from left to right.

        The current content of the buffer does not have to be the current content of the display.
        It is possible that the data was not drawn to the display yet and after a restart of
        the Bricklet the buffer will be reset to black, while the display retains its content.
        """
        x_start = int(x_start)
        check_range("x_start", x_start, 0, 295)
        y_start = int(y_start)
        check_range("y_start", y_start, 0, 127)
        x_end = int(x_end)
        check_range("x_end", x_end, 0, 295)
        y_end = int(y_end)
        check_range("y_end", y_end, 0, 127)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_BLACK_WHITE_LOW_LEVEL,
            data=pack_payload((x_start, y_start, x_end, y_end), "H B H B"),
            response_expected=True,
        )
        pixels_length, pixels_chunk_offset, pixels_chunk_data = unpack_payload(payload, "H H 464!")
        return ReadBlackWhite(pixels_length, pixels_chunk_offset, tuple(pixels_chunk_data))

    async def read_black_white(self, x_start: int, y_start: int, x_end: int, y_end: int) -> tuple[bool, ...]:
        """
        Returns the current content of the black/white pixel buffer for the specified window.

        The pixels are read into the window line by line top to bottom and
        each line is read from left to right.

        The current content of the buffer does not have to be the current content of the display.
        It is possible that the data was not drawn to the display yet and after a restart of
        the Bricklet the buffer will be reset to black, while the display retains its content.

        This function transfers the complete pixels stream and calls :func:`read_black_white_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.read_black_white_low_level(x_start, y_start, x_end, y_end)
            return Chunk(result.pixels_length, result.pixels_chunk_offset, result.pixels_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="pixels", chunk_size=464)
        return tuple(data)

    async def write_color_low_level(  # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        The E-Paper 296x128 Bricklet is available with the colors black/white/red and
        black/white/gray. Depending on the model this function writes either red or
        gray pixels to the specified window into the buffer.

        The pixels are written into the window line by line top to bottom
        and each line is written from left to right.

        The value 0 (false) means that this pixel does not have color. It will be either black
        or white (see :func:`write_black_white`). The value 1 (true) corresponds to a red or gray
        pixel, depending on the Bricklet model.

        This function writes the pixels into the red or gray pixel buffer, to draw the buffer
        to the display use :func:`draw`.

        Use :func:`write_black_white` to write black/white pixels.
        """
        x_start = int(x_start)
        check_range("x_start", x_start, 0, 295)
        y_start = int(y_start)
        check_range("y_start", y_start, 0, 127)
        x_end = int(x_end)
        check_range("x_end", x_end, 0, 295)
        y_end = int(y_end)
        check_range("y_end", y_end, 0, 127)
        pixels_length = int(pixels_length)
        check_range("pixels_length", pixels_length, 0, 37888)
        pixels_chunk_offset = int(pixels_chunk_offset)
        check_range("pixels_chunk_offset", pixels_chunk_offset, 0, 65535)
        check_length("pixels_chunk_data", pixels_chunk_data, 432)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_COLOR_LOW_LEVEL,
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
                "H B H B H H 432!",
            ),
            response_expected=response_expected,
        )

    async def write_color(self, x_start: int, y_start: int, x_end: int, y_end: int, pixels: Sequence[bool]) -> None:
        """
        The E-Paper 296x128 Bricklet is available with the colors black/white/red and
        black/white/gray. Depending on the model this function writes either red or
        gray pixels to the specified window into the buffer.

        The pixels are written into the window line by line top to bottom
        and each line is written from left to right.

        The value 0 (false) means that this pixel does not have color. It will be either black
        or white (see :func:`write_black_white`). The value 1 (true) corresponds to a red or gray
        pixel, depending on the Bricklet model.

        This function writes the pixels into the red or gray pixel buffer, to draw the buffer
        to the display use :func:`draw`.

        Use :func:`write_black_white` to write black/white pixels.

        This function transfers the complete pixels stream and calls :func:`write_color_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.write_color_low_level(x_start, y_start, x_end, y_end, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk,
                [bool(item) for item in pixels],
                name="pixels",
                chunk_size=432,
                padding=False,
                max_length=65535,
            )

    async def read_color_low_level(self, x_start: int, y_start: int, x_end: int, y_end: int) -> ReadColor:
        """
        Returns the current content of the red or gray pixel buffer for the specified window.

        The pixels are written into the window line by line top to bottom
        and each line is written from left to right.

        The current content of the buffer does not have to be the current content of the display.
        It is possible that the data was not drawn to the display yet and after a restart of
        the Bricklet the buffer will be reset to black, while the display retains its content.
        """
        x_start = int(x_start)
        check_range("x_start", x_start, 0, 295)
        y_start = int(y_start)
        check_range("y_start", y_start, 0, 127)
        x_end = int(x_end)
        check_range("x_end", x_end, 0, 295)
        y_end = int(y_end)
        check_range("y_end", y_end, 0, 127)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_COLOR_LOW_LEVEL,
            data=pack_payload((x_start, y_start, x_end, y_end), "H B H B"),
            response_expected=True,
        )
        pixels_length, pixels_chunk_offset, pixels_chunk_data = unpack_payload(payload, "H H 464!")
        return ReadColor(pixels_length, pixels_chunk_offset, tuple(pixels_chunk_data))

    async def read_color(self, x_start: int, y_start: int, x_end: int, y_end: int) -> tuple[bool, ...]:
        """
        Returns the current content of the red or gray pixel buffer for the specified window.

        The pixels are written into the window line by line top to bottom
        and each line is written from left to right.

        The current content of the buffer does not have to be the current content of the display.
        It is possible that the data was not drawn to the display yet and after a restart of
        the Bricklet the buffer will be reset to black, while the display retains its content.

        This function transfers the complete pixels stream and calls :func:`read_color_low_level` as often as necessary.
        Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.read_color_low_level(x_start, y_start, x_end, y_end)
            return Chunk(result.pixels_length, result.pixels_chunk_offset, result.pixels_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="pixels", chunk_size=464)
        return tuple(data)

    async def fill_display(self, color: Color | int, response_expected: bool = True) -> None:
        """
        Fills the complete content of the display with the given color.

        This function writes the pixels into the black/white/red|gray pixel buffer, to draw the buffer
        to the display use :func:`draw`.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.FILL_DISPLAY,
            data=pack_payload((Color(color).value,), "B"),
            response_expected=response_expected,
        )

    async def draw_text(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        position_x: int,
        position_y: int,
        font: Font | int,
        color: Color | int,
        orientation: Orientation | int,
        text: str,
        response_expected: bool = True,
    ) -> None:
        """
        Draws a text with up to 50 characters at the pixel position (x, y).

        You can use one of 9 different font sizes and draw the text in
        black/white/red|gray. The text can be drawn horizontal or vertical.

        This function writes the pixels into the black/white/red|gray pixel buffer, to draw the buffer
        to the display use :func:`draw`.

        The font conforms to code page 437.
        """
        position_x = int(position_x)
        check_range("position_x", position_x, 0, 295)
        position_y = int(position_y)
        check_range("position_y", position_y, 0, 127)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DRAW_TEXT,
            data=pack_payload(
                (
                    position_x,
                    position_y,
                    Font(font).value,
                    Color(color).value,
                    Orientation(orientation).value,
                    encode_string("text", text, 50),
                ),
                "H B B B B 50s",
            ),
            response_expected=response_expected,
        )

    async def draw_line(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        position_x_start: int,
        position_y_start: int,
        position_x_end: int,
        position_y_end: int,
        color: Color | int,
        response_expected: bool = True,
    ) -> None:
        """
        Draws a line from (x, y)-start to (x, y)-end in the given color.

        This function writes the pixels into the black/white/red|gray pixel buffer, to draw the buffer
        to the display use :func:`draw`.
        """
        position_x_start = int(position_x_start)
        check_range("position_x_start", position_x_start, 0, 295)
        position_y_start = int(position_y_start)
        check_range("position_y_start", position_y_start, 0, 127)
        position_x_end = int(position_x_end)
        check_range("position_x_end", position_x_end, 0, 295)
        position_y_end = int(position_y_end)
        check_range("position_y_end", position_y_end, 0, 127)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DRAW_LINE,
            data=pack_payload(
                (position_x_start, position_y_start, position_x_end, position_y_end, Color(color).value), "H B H B B"
            ),
            response_expected=response_expected,
        )

    async def draw_box(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        position_x_start: int,
        position_y_start: int,
        position_x_end: int,
        position_y_end: int,
        fill: bool,
        color: Color | int,
        response_expected: bool = True,
    ) -> None:
        """
        Draws a box from (x, y)-start to (x, y)-end in the given color.

        If you set fill to true, the box will be filled with the
        color. Otherwise only the outline will be drawn.

        This function writes the pixels into the black/white/red|gray pixel buffer, to draw the buffer
        to the display use :func:`draw`.
        """
        position_x_start = int(position_x_start)
        check_range("position_x_start", position_x_start, 0, 295)
        position_y_start = int(position_y_start)
        check_range("position_y_start", position_y_start, 0, 127)
        position_x_end = int(position_x_end)
        check_range("position_x_end", position_x_end, 0, 295)
        position_y_end = int(position_y_end)
        check_range("position_y_end", position_y_end, 0, 127)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DRAW_BOX,
            data=pack_payload(
                (position_x_start, position_y_start, position_x_end, position_y_end, bool(fill), Color(color).value),
                "H B H B ! B",
            ),
            response_expected=response_expected,
        )

    async def set_update_mode(
        self, update_mode: UpdateMode | int = UpdateMode.DEFAULT, response_expected: bool = True
    ) -> None:
        """
        .. note::
         The default update mode corresponds to the default e-paper display
         manufacturer settings. All of the other modes are experimental and
         will result in increased ghosting and possibly other long-term
         side effects.

         If you want to know more about the inner workings of an e-paper display
         take a look at this excellent video from Ben Krasnow:
         `https://www.youtube.com/watch?v=MsbiO8EAsGw <https://www.youtube.com/watch?v=MsbiO8EAsGw>`__.

         If you are not sure about this option, leave the update mode at default.

        Currently there are three update modes available:

        * Default: Settings as given by the manufacturer. An update will take about
          7.5 seconds and during the update the screen will flicker several times.
        * Black/White: This will only update the black/white pixel. It uses the manufacturer
          settings for black/white and ignores the red or gray pixel buffer. With this mode the
          display will flicker once and it takes about 2.5 seconds. Compared to the default settings
          there is more ghosting.
        * Delta: This will only update the black/white pixel. It uses an aggressive method where
          the changes are not applied for a whole buffer but only for the delta between the last
          and the next buffer. With this mode the display will not flicker during an update and
          it takes about 900-950ms. Compared to the other two settings there is more ghosting. This
          mode can be used for something like a flicker-free live update of a text.

        With the black/white/red display if you use either the black/white or the delta mode,
        after a while of going back and forth between black and white the white color will
        start to appear red-ish or pink-ish.

        If you use the aggressive delta mode and rapidly change the content, we recommend that you
        change back to the default mode every few hours and in the default mode cycle between the
        three available colors a few times. This will get rid of the ghosting and after that you can
        go back to the delta mode with flicker-free updates.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_UPDATE_MODE,
            data=pack_payload((UpdateMode(update_mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_update_mode(self) -> UpdateMode:
        """
        Returns the update mode as set by :func:`set_update_mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_UPDATE_MODE, response_expected=True
        )
        return UpdateMode(unpack_payload(payload, "B"))

    async def set_display_type(self, display_type: DisplayType | int, response_expected: bool = True) -> None:
        """
        Sets the type of the display. The e-paper display is available
        in black/white/red and black/white/gray. This will be factory set
        during the flashing and testing phase. The value is saved in
        non-volatile memory and will stay after a power cycle.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISPLAY_TYPE,
            data=pack_payload((DisplayType(display_type).value,), "B"),
            response_expected=response_expected,
        )

    async def get_display_type(self) -> DisplayType:
        """
        Returns the type of the e-paper display. It can either be
        black/white/red or black/white/gray.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISPLAY_TYPE, response_expected=True
        )
        return DisplayType(unpack_payload(payload, "B"))

    async def set_display_driver(self, display_driver: DisplayDriver | int, response_expected: bool = True) -> None:
        """
        Sets the type of display driver. The Bricklet can currently support
        SSD1675A and SSD1680. This will be factory set
        during the flashing and testing phase. The value is saved in
        non-volatile memory and will stay after a power cycle.

        .. versionadded:: 2.0.3 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISPLAY_DRIVER,
            data=pack_payload((DisplayDriver(display_driver).value,), "B"),
            response_expected=response_expected,
        )

    async def get_display_driver(self) -> DisplayDriver:
        """
        Returns the e-paper display driver.

        .. versionadded:: 2.0.3 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISPLAY_DRIVER, response_expected=True
        )
        return DisplayDriver(unpack_payload(payload, "B"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, DrawStatus(value)
