"""
Module for the Tinkerforge LCD 128x64 Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/LCD128x64_Bricklet_Python.html) implemented using
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
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    SimpleCallbackConfiguration,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .streams import Chunk, read_stream, write_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    TOUCH_POSITION = 11
    TOUCH_GESTURE = 15
    GUI_BUTTON_PRESSED = 25
    GUI_SLIDER_VALUE = 32
    GUI_TAB_SELECTED = 44


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
    GET_TOUCH_POSITION = 8
    SET_TOUCH_POSITION_CALLBACK_CONFIGURATION = 9
    GET_TOUCH_POSITION_CALLBACK_CONFIGURATION = 10
    GET_TOUCH_GESTURE = 12
    SET_TOUCH_GESTURE_CALLBACK_CONFIGURATION = 13
    GET_TOUCH_GESTURE_CALLBACK_CONFIGURATION = 14
    DRAW_LINE = 16
    DRAW_BOX = 17
    DRAW_TEXT = 18
    SET_GUI_BUTTON = 19
    GET_GUI_BUTTON = 20
    REMOVE_GUI_BUTTON = 21
    SET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION = 22
    GET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION = 23
    GET_GUI_BUTTON_PRESSED = 24
    SET_GUI_SLIDER = 26
    GET_GUI_SLIDER = 27
    REMOVE_GUI_SLIDER = 28
    SET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION = 29
    GET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION = 30
    GET_GUI_SLIDER_VALUE = 31
    SET_GUI_TAB_CONFIGURATION = 33
    GET_GUI_TAB_CONFIGURATION = 34
    SET_GUI_TAB_TEXT = 35
    GET_GUI_TAB_TEXT = 36
    SET_GUI_TAB_ICON = 37
    GET_GUI_TAB_ICON = 38
    REMOVE_GUI_TAB = 39
    SET_GUI_TAB_SELECTED = 40
    SET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION = 41
    GET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION = 42
    GET_GUI_TAB_SELECTED = 43
    SET_GUI_GRAPH_CONFIGURATION = 45
    GET_GUI_GRAPH_CONFIGURATION = 46
    SET_GUI_GRAPH_DATA_LOW_LEVEL = 47
    GET_GUI_GRAPH_DATA_LOW_LEVEL = 48
    REMOVE_GUI_GRAPH = 49
    REMOVE_ALL_GUI = 50
    SET_TOUCH_LED_CONFIG = 51
    GET_TOUCH_LED_CONFIG = 52


@unique
class Gesture(Enum):
    """
    The gesture options
    """

    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1
    TOP_TO_BOTTOM = 2
    BOTTOM_TO_TOP = 3


@unique
class Color(Enum):
    """
    The color options
    """

    WHITE = False
    BLACK = True


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
class Direction(Enum):
    """
    The direction options
    """

    HORIZONTAL = 0
    VERTICAL = 1


@unique
class ChangeTabOn(Enum):
    """
    The change tab on options
    """

    CLICK = 1
    SWIPE = 2
    CLICK_AND_SWIPE = 3


@unique
class GraphType(Enum):
    """
    The graph type options
    """

    DOT = 0
    LINE = 1
    BAR = 2


@unique
class TouchLEDConfig(Enum):
    """
    The touch led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_TOUCH = 3


class ReadPixels(NamedTuple):
    pixels_length: int
    pixels_chunk_offset: int
    pixels_chunk_data: tuple[bool, ...]


class GetDisplayConfiguration(NamedTuple):
    contrast: int
    backlight: int
    invert: bool
    automatic_draw: bool


class GetTouchPosition(NamedTuple):
    pressure: int
    x: int
    y: int
    age: Decimal


class GetTouchGesture(NamedTuple):
    gesture: Gesture
    duration: Decimal
    pressure_max: int
    x_start: int
    y_start: int
    x_end: int
    y_end: int
    age: Decimal


class GetGUIButton(NamedTuple):
    active: bool
    position_x: int
    position_y: int
    width: int
    height: int
    text: str


class GetGUISlider(NamedTuple):
    active: bool
    position_x: int
    position_y: int
    length: int
    direction: Direction
    value: int


class GetGUITabConfiguration(NamedTuple):
    change_tab_config: ChangeTabOn
    clear_gui: bool


class GetGUITabText(NamedTuple):
    active: bool
    text: str


class GetGUITabIcon(NamedTuple):
    active: bool
    icon: tuple[bool, ...]


class GetGUIGraphConfiguration(NamedTuple):
    active: bool
    graph_type: GraphType
    position_x: int
    position_y: int
    width: int
    height: int
    text_x: str
    text_y: str


class GetGUIGraphData(NamedTuple):
    data_length: int
    data_chunk_offset: int
    data_chunk_data: tuple[int, ...]


class GUIButtonPressedEvent(NamedTuple):
    index_: int
    pressed: bool


class GUISliderValueEvent(NamedTuple):
    index_: int
    value: int


class BrickletLCD128x64(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    0.071 m (2.8") display with 128x64 pixel and touch screen
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_LCD_128X64
    DEVICE_DISPLAY_NAME = "LCD 128x64 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Gesture: TypeAlias = Gesture
    Color: TypeAlias = Color
    Font: TypeAlias = Font
    Direction: TypeAlias = Direction
    ChangeTabOn: TypeAlias = ChangeTabOn
    GraphType: TypeAlias = GraphType
    TouchLEDConfig: TypeAlias = TouchLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.TOUCH_POSITION: "H H H I",
        CallbackID.TOUCH_GESTURE: "B I H H H H H I",
        CallbackID.GUI_BUTTON_PRESSED: "B !",
        CallbackID.GUI_SLIDER_VALUE: "B B",
        CallbackID.GUI_TAB_SELECTED: "b",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.TOUCH_POSITION,),
            configuration=ChannelConfiguration("touch_position", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            1,
            callbacks=(CallbackID.TOUCH_GESTURE,),
            configuration=ChannelConfiguration("touch_gesture", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            2,
            callbacks=(CallbackID.GUI_BUTTON_PRESSED,),
            configuration=ChannelConfiguration("gui_button_pressed", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            3,
            callbacks=(CallbackID.GUI_SLIDER_VALUE,),
            configuration=ChannelConfiguration("gui_slider_value", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            4,
            getter="get_gui_tab_selected",
            callbacks=(CallbackID.GUI_TAB_SELECTED,),
            configuration=ChannelConfiguration("gui_tab_selected", thresholds=False, wrap_advanced=True),
        ),
    )

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

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
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
        self,
        contrast: int = 14,
        backlight: int = 100,
        invert: bool = False,
        automatic_draw: bool = True,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration of the display.

        If automatic draw is set to *true*, the display is automatically updated with every
        call of :func:`write_pixels` and :func:`write_line`. If it is set to false, the
        changes are written into an internal buffer and only shown on the display after
        a call of :func:`draw_buffered_frame`.
        """
        contrast = int(contrast)
        check_range("contrast", contrast, 0, 63)
        backlight = int(backlight)
        check_range("backlight", backlight, 0, 100)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISPLAY_CONFIGURATION,
            data=pack_payload((contrast, backlight, bool(invert), bool(automatic_draw)), "B B ! !"),
            response_expected=response_expected,
        )

    async def get_display_configuration(self) -> GetDisplayConfiguration:
        """
        Returns the configuration as set by :func:`set_display_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISPLAY_CONFIGURATION, response_expected=True
        )
        contrast, backlight, invert, automatic_draw = unpack_payload(payload, "B B ! !")
        return GetDisplayConfiguration(contrast, backlight, invert, automatic_draw)

    async def write_line(self, line: int, position: int, text: str, response_expected: bool = True) -> None:
        """
        Writes text to a specific line with a specific position.

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

        This function is a 1:1 replacement for the function with the same name
        in the LCD 20x4 Bricklet. You can draw text at a specific pixel position
        and with different font sizes with the :func:`draw_text` function.
        """
        line = int(line)
        check_range("line", line, 0, 7)
        position = int(position)
        check_range("position", position, 0, 21)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_LINE,
            data=pack_payload((line, position, str(text).encode("latin-1")), "B B 22s"),
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

    async def get_touch_position(self) -> GetTouchPosition:
        """
        Returns the last valid touch position:

        * Pressure: Amount of pressure applied by the user
        * X: Touch position on x-axis
        * Y: Touch position on y-axis
        * Age: Age of touch press (how long ago it was)

        Units: age in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_POSITION, response_expected=True
        )
        pressure, x, y, age = unpack_payload(payload, "H H H I")
        return GetTouchPosition(pressure, x, y, ms_to_seconds(age))

    async def set_touch_position_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.TOUCH_POSITION` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TOUCH_POSITION_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_touch_position_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_touch_position_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_POSITION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def get_touch_gesture(self) -> GetTouchGesture:
        """
        Returns one of four touch gestures that can be automatically detected by the Bricklet.

        The gestures are swipes from left to right, right to left, top to bottom and bottom to top.

        Additionally to the gestures a vector with a start and end position of the gesture is
        provided. You can use this vector do determine a more exact location of the gesture (e.g.
        the swipe from top to bottom was on the left or right part of the screen).

        The age parameter corresponds to the age of gesture (how long ago it was).

        Units: duration in s, age in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_GESTURE, response_expected=True
        )
        gesture, duration, pressure_max, x_start, y_start, x_end, y_end, age = unpack_payload(
            payload, "B I H H H H H I"
        )
        return GetTouchGesture(
            Gesture(gesture), ms_to_seconds(duration), pressure_max, x_start, y_start, x_end, y_end, ms_to_seconds(age)
        )

    async def set_touch_gesture_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.TOUCH_GESTURE` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TOUCH_GESTURE_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_touch_gesture_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_touch_gesture_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_GESTURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

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
        Draws a white or black line from (x, y)-start to (x, y)-end.

        .. versionadded:: 2.0.2 (Firmware)
        """
        position_x_start = int(position_x_start)
        check_range("position_x_start", position_x_start, 0, 127)
        position_y_start = int(position_y_start)
        check_range("position_y_start", position_y_start, 0, 63)
        position_x_end = int(position_x_end)
        check_range("position_x_end", position_x_end, 0, 127)
        position_y_end = int(position_y_end)
        check_range("position_y_end", position_y_end, 0, 63)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DRAW_LINE,
            data=pack_payload(
                (position_x_start, position_y_start, position_x_end, position_y_end, Color(color).value), "B B B B !"
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
        Draws a white or black box from (x, y)-start to (x, y)-end.

        If you set fill to true, the box will be filled with the
        color. Otherwise only the outline will be drawn.

        .. versionadded:: 2.0.2 (Firmware)
        """
        position_x_start = int(position_x_start)
        check_range("position_x_start", position_x_start, 0, 127)
        position_y_start = int(position_y_start)
        check_range("position_y_start", position_y_start, 0, 63)
        position_x_end = int(position_x_end)
        check_range("position_x_end", position_x_end, 0, 127)
        position_y_end = int(position_y_end)
        check_range("position_y_end", position_y_end, 0, 63)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DRAW_BOX,
            data=pack_payload(
                (position_x_start, position_y_start, position_x_end, position_y_end, bool(fill), Color(color).value),
                "B B B B ! !",
            ),
            response_expected=response_expected,
        )

    async def draw_text(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        position_x: int,
        position_y: int,
        font: Font | int,
        color: Color | int,
        text: str,
        response_expected: bool = True,
    ) -> None:
        """
        Draws a text at the pixel position (x, y).

        You can use one of 9 different font sizes and draw the text in white or black.

        The font conforms to code page 437.

        .. versionadded:: 2.0.2 (Firmware)
        """
        position_x = int(position_x)
        check_range("position_x", position_x, 0, 127)
        position_y = int(position_y)
        check_range("position_y", position_y, 0, 63)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DRAW_TEXT,
            data=pack_payload(
                (position_x, position_y, Font(font).value, Color(color).value, str(text).encode("latin-1")),
                "B B B ! 22s",
            ),
            response_expected=response_expected,
        )

    async def set_gui_button(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        index: int,
        position_x: int,
        position_y: int,
        width: int,
        height: int,
        text: str,
        response_expected: bool = True,
    ) -> None:
        """
        Draws a clickable button at position (x, y) with the given text.

        You can use up to 12 buttons.

        The x position + width has to be within the range of 1 to 128 and the y
        position + height has to be within the range of 1 to 64.

        The minimum useful width/height of a button is 3.

        You can enable a callback for a button press with
        :func:`set_gui_button_pressed_callback_configuration`. The callback will
        be triggered for press and release-events.

        The button is drawn in a separate GUI buffer and the button-frame will
        always stay on top of the graphics drawn with :func:`write_pixels`. To
        remove the button use :func:`remove_gui_button`.

        If you want an icon instead of text, you can draw the icon inside of the
        button with :func:`write_pixels`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 11)
        position_x = int(position_x)
        check_range("position_x", position_x, 0, 127)
        position_y = int(position_y)
        check_range("position_y", position_y, 0, 63)
        width = int(width)
        check_range("width", width, 1, 128)
        height = int(height)
        check_range("height", height, 1, 64)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_BUTTON,
            data=pack_payload(
                (index, position_x, position_y, width, height, str(text).encode("latin-1")), "B B B B B 16s"
            ),
            response_expected=response_expected,
        )

    async def get_gui_button(self, index: int) -> GetGUIButton:
        """
        Returns the button properties for a given `Index` as set by :func:`set_gui_button`.

        Additionally the `Active` parameter shows if a button is currently active/visible
        or not.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 11)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GUI_BUTTON, data=pack_payload((index,), "B"), response_expected=True
        )
        active, position_x, position_y, width, height, text = unpack_payload(payload, "! B B B B 16s")
        return GetGUIButton(active, position_x, position_y, width, height, text)

    async def remove_gui_button(self, index: int, response_expected: bool = True) -> None:
        """
        Removes the button with the given index.

        You can use index 255 to remove all buttons.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REMOVE_GUI_BUTTON,
            data=pack_payload((index,), "B"),
            response_expected=response_expected,
        )

    async def set_gui_button_pressed_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.GUI_BUTTON_PRESSED` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        .. versionadded:: 2.0.2 (Firmware)
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_gui_button_pressed_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_gui_button_pressed_callback_configuration`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def get_gui_button_pressed(self, index: int) -> bool:
        """
        Returns the state of the button for the given index.

        The state can either be pressed (true) or released (false).

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 11)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_GUI_BUTTON_PRESSED,
            data=pack_payload((index,), "B"),
            response_expected=True,
        )
        return unpack_payload(payload, "!")

    async def set_gui_slider(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        index: int,
        position_x: int,
        position_y: int,
        length: int,
        direction: Direction | int,
        value: int,
        response_expected: bool = True,
    ) -> None:
        """
        Draws a slider at position (x, y) with the given length.

        You can use up to 6 sliders.

        If you use the horizontal direction, the x position + length has to be
        within the range of 1 to 128 and the y position has to be within
        the range of 0 to 46.

        If you use the vertical direction, the y position + length has to be
        within the range of 1 to 64 and the x position has to be within
        the range of 0 to 110.

        The minimum length of a slider is 8.

        The parameter value is the start-position of the slider, it can
        be between 0 and length-8.

        You can enable a callback for the slider value with
        :func:`set_gui_slider_value_callback_configuration`.

        The slider is drawn in a separate GUI buffer and it will
        always stay on top of the graphics drawn with :func:`write_pixels`. To
        remove the button use :func:`remove_gui_slider`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 5)
        position_x = int(position_x)
        check_range("position_x", position_x, 0, 128)
        position_y = int(position_y)
        check_range("position_y", position_y, 0, 64)
        length = int(length)
        check_range("length", length, 8, 128)
        value = int(value)
        check_range("value", value, 0, 120)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_SLIDER,
            data=pack_payload(
                (index, position_x, position_y, length, Direction(direction).value, value), "B B B B B B"
            ),
            response_expected=response_expected,
        )

    async def get_gui_slider(self, index: int) -> GetGUISlider:
        """
        Returns the slider properties for a given `Index` as set by :func:`set_gui_slider`.

        Additionally the `Active` parameter shows if a button is currently active/visible
        or not.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 5)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GUI_SLIDER, data=pack_payload((index,), "B"), response_expected=True
        )
        active, position_x, position_y, length, direction, value = unpack_payload(payload, "! B B B B B")
        return GetGUISlider(active, position_x, position_y, length, Direction(direction), value)

    async def remove_gui_slider(self, index: int, response_expected: bool = True) -> None:
        """
        Removes the slider with the given index.

        You can use index 255 to remove all slider.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REMOVE_GUI_SLIDER,
            data=pack_payload((index,), "B"),
            response_expected=response_expected,
        )

    async def set_gui_slider_value_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.GUI_SLIDER_VALUE` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        .. versionadded:: 2.0.2 (Firmware)
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_gui_slider_value_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_gui_slider_value_callback_configuration`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def get_gui_slider_value(self, index: int) -> int:
        """
        Returns the current slider value for the given index.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 5)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_GUI_SLIDER_VALUE,
            data=pack_payload((index,), "B"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def set_gui_tab_configuration(
        self,
        change_tab_config: ChangeTabOn | int = ChangeTabOn.CLICK_AND_SWIPE,
        clear_gui: bool = True,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the general configuration for tabs. You can configure the tabs to only
        accept clicks or only swipes (gesture left/right and right/left) or both.

        Additionally, if you set `Clear GUI` to true, all of the GUI elements (buttons,
        slider, graphs) will automatically be removed on every tab change.

        .. versionadded:: 2.0.2 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_TAB_CONFIGURATION,
            data=pack_payload((ChangeTabOn(change_tab_config).value, bool(clear_gui)), "B !"),
            response_expected=response_expected,
        )

    async def get_gui_tab_configuration(self) -> GetGUITabConfiguration:
        """
        Returns the tab configuration as set by :func:`set_gui_tab_configuration`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GUI_TAB_CONFIGURATION, response_expected=True
        )
        change_tab_config, clear_gui = unpack_payload(payload, "B !")
        return GetGUITabConfiguration(ChangeTabOn(change_tab_config), clear_gui)

    async def set_gui_tab_text(self, index: int, text: str, response_expected: bool = True) -> None:
        """
        Adds a text-tab with the given index.

        You can use up to 10 tabs.

        A text-tab with the same index as a icon-tab will overwrite the icon-tab.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 9)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_TAB_TEXT,
            data=pack_payload((index, str(text).encode("latin-1")), "B 5s"),
            response_expected=response_expected,
        )

    async def get_gui_tab_text(self, index: int) -> GetGUITabText:
        """
        Returns the text for a given index as set by :func:`set_gui_tab_text`.

        Additionally the `Active` parameter shows if the tab is currently active/visible
        or not.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_GUI_TAB_TEXT,
            data=pack_payload((index,), "B"),
            response_expected=True,
        )
        active, text = unpack_payload(payload, "! 5s")
        return GetGUITabText(active, text)

    async def set_gui_tab_icon(self, index: int, icon: Sequence[bool], response_expected: bool = True) -> None:
        """
        Adds a icon-tab with the given index. The icon can have a width of 28 pixels
        with a height of 6 pixels. It is drawn line-by-line from left to right.

        You can use up to 10 tabs.

        A icon-tab with the same index as a text-tab will overwrite the text-tab.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 9)
        check_length("icon", icon, 168)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_TAB_ICON,
            data=pack_payload((index, [bool(item) for item in icon]), "B 168!"),
            response_expected=response_expected,
        )

    async def get_gui_tab_icon(self, index: int) -> GetGUITabIcon:
        """
        Returns the icon for a given index as set by :func:`set_gui_tab_icon`.

        Additionally the `Active` parameter shows if the tab is currently active/visible
        or not.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_GUI_TAB_ICON,
            data=pack_payload((index,), "B"),
            response_expected=True,
        )
        active, icon = unpack_payload(payload, "! 168!")
        return GetGUITabIcon(active, tuple(icon))

    async def remove_gui_tab(self, index: int, response_expected: bool = True) -> None:
        """
        Removes the tab with the given index.

        You can use index 255 to remove all tabs.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REMOVE_GUI_TAB,
            data=pack_payload((index,), "B"),
            response_expected=response_expected,
        )

    async def set_gui_tab_selected(self, index: int, response_expected: bool = True) -> None:
        """
        Sets the tab with the given index as selected (drawn as selected on the display).

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 9)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_TAB_SELECTED,
            data=pack_payload((index,), "B"),
            response_expected=response_expected,
        )

    async def set_gui_tab_selected_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.GUI_TAB_SELECTED` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        .. versionadded:: 2.0.2 (Firmware)
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_gui_tab_selected_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_gui_tab_selected_callback_configuration`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def get_gui_tab_selected(self) -> int:
        """
        Returns the index of the currently selected tab.
        If there are not tabs, the returned index is -1.

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_GUI_TAB_SELECTED, response_expected=True
        )
        return unpack_payload(payload, "b")

    async def set_gui_graph_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        index: int,
        graph_type: GraphType | int,
        position_x: int,
        position_y: int,
        width: int,
        height: int,
        text_x: str,
        text_y: str,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration for up to four graphs.

        The graph type can be dot-, line- or bar-graph.

        The x and y position are pixel positions.

        You can add a text for the x and y axis.
        The text is drawn at the inside of the graph and it can overwrite some
        of the graph data. If you need the text outside of the graph you can
        leave this text here empty and use :func:`draw_text` to draw the caption
        outside of the graph.

        The data of the graph can be set and updated with :func:`set_gui_graph_data`.

        The graph is drawn in a separate GUI buffer and the graph-frame and data will
        always stay on top of the graphics drawn with :func:`write_pixels`. To
        remove the graph use :func:`remove_gui_graph`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 3)
        position_x = int(position_x)
        check_range("position_x", position_x, 0, 127)
        position_y = int(position_y)
        check_range("position_y", position_y, 0, 63)
        width = int(width)
        check_range("width", width, 0, 118)
        height = int(height)
        check_range("height", height, 0, 63)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_GRAPH_CONFIGURATION,
            data=pack_payload(
                (
                    index,
                    GraphType(graph_type).value,
                    position_x,
                    position_y,
                    width,
                    height,
                    str(text_x).encode("latin-1"),
                    str(text_y).encode("latin-1"),
                ),
                "B B B B B B 4s 4s",
            ),
            response_expected=response_expected,
        )

    async def get_gui_graph_configuration(self, index: int) -> GetGUIGraphConfiguration:
        """
        Returns the graph properties for a given `Index` as set by :func:`set_gui_graph_configuration`.

        Additionally the `Active` parameter shows if a graph is currently active/visible
        or not.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_GUI_GRAPH_CONFIGURATION,
            data=pack_payload((index,), "B"),
            response_expected=True,
        )
        active, graph_type, position_x, position_y, width, height, text_x, text_y = unpack_payload(
            payload, "! B B B B B 4s 4s"
        )
        return GetGUIGraphConfiguration(
            active, GraphType(graph_type), position_x, position_y, width, height, text_x, text_y
        )

    async def set_gui_graph_data_low_level(
        self,
        index: int,
        data_length: int,
        data_chunk_offset: int,
        data_chunk_data: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Sets the data for a graph with the given index. You have to configure the graph with
        :func:`set_gui_graph_configuration` before you can set the first data.

        The graph will show the first n values of the data that you set, where
        n is the width set with :func:`set_gui_graph_configuration`. If you set
        less then n values it will show the rest of the values as zero.

        The maximum number of data-points you can set is 118 (which also corresponds to the
        maximum width of the graph).

        You have to scale your values to be between 0 and 255. 0 will be shown
        at the bottom of the graph and 255 at the top.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 3)
        data_length = int(data_length)
        check_range("data_length", data_length, 0, 118)
        data_chunk_offset = int(data_chunk_offset)
        check_range("data_chunk_offset", data_chunk_offset, 0, 65535)
        check_length("data_chunk_data", data_chunk_data, 59)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_GUI_GRAPH_DATA_LOW_LEVEL,
            data=pack_payload((index, data_length, data_chunk_offset, list(map(int, data_chunk_data))), "B H H 59B"),
            response_expected=response_expected,
        )

    async def set_gui_graph_data(self, index: int, data: bytes | Sequence[int]) -> None:
        """
        Sets the data for a graph with the given index. You have to configure the graph with
        :func:`set_gui_graph_configuration` before you can set the first data.

        The graph will show the first n values of the data that you set, where
        n is the width set with :func:`set_gui_graph_configuration`. If you set
        less then n values it will show the rest of the values as zero.

        The maximum number of data-points you can set is 118 (which also corresponds to the
        maximum width of the graph).

        You have to scale your values to be between 0 and 255. 0 will be shown
        at the bottom of the graph and 255 at the top.

        This function transfers the complete data stream and calls :func:`set_gui_graph_data_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.

        .. versionadded:: 2.0.2 (Firmware)
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.set_gui_graph_data_low_level(index, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk, [int(item) for item in data], name="data", chunk_size=59, padding=0, max_length=65535
            )

    async def get_gui_graph_data_low_level(self, index: int) -> GetGUIGraphData:
        """
        Returns the graph data for a given index as set by :func:`set_gui_graph_data`.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 3)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_GUI_GRAPH_DATA_LOW_LEVEL,
            data=pack_payload((index,), "B"),
            response_expected=True,
        )
        data_length, data_chunk_offset, data_chunk_data = unpack_payload(payload, "H H 59B")
        return GetGUIGraphData(data_length, data_chunk_offset, tuple(data_chunk_data))

    async def get_gui_graph_data(self, index: int) -> bytes:
        """
        Returns the graph data for a given index as set by :func:`set_gui_graph_data`.

        This function transfers the complete data stream and calls :func:`get_gui_graph_data_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.

        .. versionadded:: 2.0.2 (Firmware)
        """

        async def read_chunk() -> Chunk:
            result = await self.get_gui_graph_data_low_level(index)
            return Chunk(result.data_length, result.data_chunk_offset, result.data_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="data", chunk_size=59)
        return bytes(data)

    async def remove_gui_graph(self, index: int, response_expected: bool = True) -> None:
        """
        Removes the graph with the given index.

        You can use index 255 to remove all graphs.

        .. versionadded:: 2.0.2 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REMOVE_GUI_GRAPH,
            data=pack_payload((index,), "B"),
            response_expected=response_expected,
        )

    async def remove_all_gui(self, response_expected: bool = True) -> None:
        """
        Removes all GUI elements (buttons, slider, graphs, tabs).

        .. versionadded:: 2.0.2 (Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.REMOVE_ALL_GUI, response_expected=response_expected
        )

    async def set_touch_led_config(
        self, config: TouchLEDConfig | int = TouchLEDConfig.SHOW_TOUCH, response_expected: bool = True
    ) -> None:
        """
        Sets the touch LED configuration. By default the LED is on if the
        LCD is touched.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.

        .. versionadded:: 2.0.2 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TOUCH_LED_CONFIG,
            data=pack_payload((TouchLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_touch_led_config(self) -> TouchLEDConfig:
        """
        Returns the configuration as set by :func:`set_touch_led_config`

        .. versionadded:: 2.0.2 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_LED_CONFIG, response_expected=True
        )
        return TouchLEDConfig(unpack_payload(payload, "B"))

    def _convert_callback(  # pylint: disable=too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.TOUCH_POSITION:
            pressure, x, y, age = value
            return 0, GetTouchPosition(pressure, x, y, ms_to_seconds(age))
        if callback_id is CallbackID.TOUCH_GESTURE:
            gesture, duration, pressure_max, x_start, y_start, x_end, y_end, age = value
            return 1, GetTouchGesture(
                Gesture(gesture),
                ms_to_seconds(duration),
                pressure_max,
                x_start,
                y_start,
                x_end,
                y_end,
                ms_to_seconds(age),
            )
        if callback_id is CallbackID.GUI_BUTTON_PRESSED:
            index, pressed = value
            return 2, GUIButtonPressedEvent(index, pressed)
        if callback_id is CallbackID.GUI_SLIDER_VALUE:
            index, value = value
            return 3, GUISliderValueEvent(index, value)
        return 4, value
