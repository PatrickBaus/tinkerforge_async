"""Tests for the LCD 128x64 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_lcd_128x64 import (
    BrickletLCD128x64,
    GetDisplayConfiguration,
    GetGUIButton,
    GetGUIGraphConfiguration,
    GetGUIGraphData,
    GetGUISlider,
    GetGUITabConfiguration,
    GetGUITabIcon,
    GetGUITabText,
    GetTouchGesture,
    GetTouchPosition,
    GUIButtonPressedEvent,
    GUISliderValueEvent,
    ReadPixels,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import Call, chunk, read_events, request, run, summary

DEVICE = BrickletLCD128x64
FunctionID = BrickletLCD128x64.FunctionID
CallbackID = BrickletLCD128x64.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "WRITE_PIXELS_LOW_LEVEL": 1,
    "READ_PIXELS_LOW_LEVEL": 2,
    "CLEAR_DISPLAY": 3,
    "SET_DISPLAY_CONFIGURATION": 4,
    "GET_DISPLAY_CONFIGURATION": 5,
    "WRITE_LINE": 6,
    "DRAW_BUFFERED_FRAME": 7,
    "GET_TOUCH_POSITION": 8,
    "SET_TOUCH_POSITION_CALLBACK_CONFIGURATION": 9,
    "GET_TOUCH_POSITION_CALLBACK_CONFIGURATION": 10,
    "GET_TOUCH_GESTURE": 12,
    "SET_TOUCH_GESTURE_CALLBACK_CONFIGURATION": 13,
    "GET_TOUCH_GESTURE_CALLBACK_CONFIGURATION": 14,
    "DRAW_LINE": 16,
    "DRAW_BOX": 17,
    "DRAW_TEXT": 18,
    "SET_GUI_BUTTON": 19,
    "GET_GUI_BUTTON": 20,
    "REMOVE_GUI_BUTTON": 21,
    "SET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION": 22,
    "GET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION": 23,
    "GET_GUI_BUTTON_PRESSED": 24,
    "SET_GUI_SLIDER": 26,
    "GET_GUI_SLIDER": 27,
    "REMOVE_GUI_SLIDER": 28,
    "SET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION": 29,
    "GET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION": 30,
    "GET_GUI_SLIDER_VALUE": 31,
    "SET_GUI_TAB_CONFIGURATION": 33,
    "GET_GUI_TAB_CONFIGURATION": 34,
    "SET_GUI_TAB_TEXT": 35,
    "GET_GUI_TAB_TEXT": 36,
    "SET_GUI_TAB_ICON": 37,
    "GET_GUI_TAB_ICON": 38,
    "REMOVE_GUI_TAB": 39,
    "SET_GUI_TAB_SELECTED": 40,
    "SET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION": 41,
    "GET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION": 42,
    "GET_GUI_TAB_SELECTED": 43,
    "SET_GUI_GRAPH_CONFIGURATION": 45,
    "GET_GUI_GRAPH_CONFIGURATION": 46,
    "SET_GUI_GRAPH_DATA_LOW_LEVEL": 47,
    "GET_GUI_GRAPH_DATA_LOW_LEVEL": 48,
    "REMOVE_GUI_GRAPH": 49,
    "REMOVE_ALL_GUI": 50,
    "SET_TOUCH_LED_CONFIG": 51,
    "GET_TOUCH_LED_CONFIG": 52,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "TOUCH_POSITION": 11,
    "TOUCH_GESTURE": 15,
    "GUI_BUTTON_PRESSED": 25,
    "GUI_SLIDER_VALUE": 32,
    "GUI_TAB_SELECTED": 44,
}

CALLS: list[Call] = [
    Call(
        "write_pixels_low_level",
        FunctionID.WRITE_PIXELS_LOW_LEVEL,
        (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)]),
        sent=("B B B B H H 448!", (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
    ),
    Call(
        "write_pixels_low_level",
        FunctionID.WRITE_PIXELS_LOW_LEVEL,
        (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)], False),
        sent=("B B B B H H 448!", (3, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
        response_expected=False,
    ),
    Call(
        "read_pixels_low_level",
        FunctionID.READ_PIXELS_LOW_LEVEL,
        (3, 3, 3, 3),
        sent=("B B B B", (3, 3, 3, 3)),
        reply=("H H 480!", (3, 4, [i % 2 == 0 for i in range(480)])),
        result=ReadPixels(3, 4, tuple(i % 2 == 0 for i in range(480))),
    ),
    Call("clear_display", FunctionID.CLEAR_DISPLAY, ()),
    Call("clear_display", FunctionID.CLEAR_DISPLAY, (False,), response_expected=False),
    Call(
        "set_display_configuration",
        FunctionID.SET_DISPLAY_CONFIGURATION,
        (3, 3, True, True),
        sent=("B B ! !", (3, 3, True, True)),
    ),
    Call(
        "set_display_configuration",
        FunctionID.SET_DISPLAY_CONFIGURATION,
        (3, 3, True, True, False),
        sent=("B B ! !", (3, 3, True, True)),
        response_expected=False,
    ),
    Call(
        "get_display_configuration",
        FunctionID.GET_DISPLAY_CONFIGURATION,
        (),
        reply=("B B ! !", (3, 4, True, True)),
        result=GetDisplayConfiguration(3, 4, True, True),
    ),
    Call("write_line", FunctionID.WRITE_LINE, (3, 3, "abc"), sent=("B B 22s", (3, 3, b"abc"))),
    Call(
        "write_line",
        FunctionID.WRITE_LINE,
        (3, 3, "abc", False),
        sent=("B B 22s", (3, 3, b"abc")),
        response_expected=False,
    ),
    Call("draw_buffered_frame", FunctionID.DRAW_BUFFERED_FRAME, (True,), sent=("!", (True,))),
    Call(
        "draw_buffered_frame",
        FunctionID.DRAW_BUFFERED_FRAME,
        (True, False),
        sent=("!", (True,)),
        response_expected=False,
    ),
    Call(
        "get_touch_position",
        FunctionID.GET_TOUCH_POSITION,
        (),
        reply=("H H H I", (3, 4, 5, 6)),
        result=GetTouchPosition(3, 4, 5, Decimal("0.006")),
    ),
    Call(
        "set_touch_position_callback_configuration",
        FunctionID.SET_TOUCH_POSITION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_touch_position_callback_configuration",
        FunctionID.SET_TOUCH_POSITION_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_touch_position_callback_configuration",
        FunctionID.GET_TOUCH_POSITION_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "get_touch_gesture",
        FunctionID.GET_TOUCH_GESTURE,
        (),
        reply=("B I H H H H H I", (3, 4, 5, 6, 7, 8, 9, 10)),
        result=GetTouchGesture(DEVICE.Gesture.BOTTOM_TO_TOP, Decimal("0.004"), 5, 6, 7, 8, 9, Decimal("0.01")),
    ),
    Call(
        "set_touch_gesture_callback_configuration",
        FunctionID.SET_TOUCH_GESTURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_touch_gesture_callback_configuration",
        FunctionID.SET_TOUCH_GESTURE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_touch_gesture_callback_configuration",
        FunctionID.GET_TOUCH_GESTURE_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("draw_line", FunctionID.DRAW_LINE, (3, 3, 3, 3, DEVICE.Color.BLACK), sent=("B B B B !", (3, 3, 3, 3, True))),
    Call(
        "draw_line",
        FunctionID.DRAW_LINE,
        (3, 3, 3, 3, DEVICE.Color.BLACK, False),
        sent=("B B B B !", (3, 3, 3, 3, True)),
        response_expected=False,
    ),
    Call(
        "draw_box",
        FunctionID.DRAW_BOX,
        (3, 3, 3, 3, True, DEVICE.Color.BLACK),
        sent=("B B B B ! !", (3, 3, 3, 3, True, True)),
    ),
    Call(
        "draw_box",
        FunctionID.DRAW_BOX,
        (3, 3, 3, 3, True, DEVICE.Color.BLACK, False),
        sent=("B B B B ! !", (3, 3, 3, 3, True, True)),
        response_expected=False,
    ),
    Call(
        "draw_text",
        FunctionID.DRAW_TEXT,
        (3, 3, DEVICE.Font.FONT_24X32, DEVICE.Color.BLACK, "abc"),
        sent=("B B B ! 22s", (3, 3, 9, True, b"abc")),
    ),
    Call(
        "draw_text",
        FunctionID.DRAW_TEXT,
        (3, 3, DEVICE.Font.FONT_24X32, DEVICE.Color.BLACK, "abc", False),
        sent=("B B B ! 22s", (3, 3, 9, True, b"abc")),
        response_expected=False,
    ),
    Call(
        "set_gui_button",
        FunctionID.SET_GUI_BUTTON,
        (3, 3, 3, 3, 3, "abc"),
        sent=("B B B B B 16s", (3, 3, 3, 3, 3, b"abc")),
    ),
    Call(
        "set_gui_button",
        FunctionID.SET_GUI_BUTTON,
        (3, 3, 3, 3, 3, "abc", False),
        sent=("B B B B B 16s", (3, 3, 3, 3, 3, b"abc")),
        response_expected=False,
    ),
    Call(
        "get_gui_button",
        FunctionID.GET_GUI_BUTTON,
        (3,),
        sent=("B", (3,)),
        reply=("! B B B B 16s", (True, 4, 5, 6, 7, b"abc")),
        result=GetGUIButton(True, 4, 5, 6, 7, "abc"),
    ),
    Call("remove_gui_button", FunctionID.REMOVE_GUI_BUTTON, (3,), sent=("B", (3,))),
    Call("remove_gui_button", FunctionID.REMOVE_GUI_BUTTON, (3, False), sent=("B", (3,)), response_expected=False),
    Call(
        "set_gui_button_pressed_callback_configuration",
        FunctionID.SET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_gui_button_pressed_callback_configuration",
        FunctionID.SET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_gui_button_pressed_callback_configuration",
        FunctionID.GET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call(
        "get_gui_button_pressed",
        FunctionID.GET_GUI_BUTTON_PRESSED,
        (3,),
        sent=("B", (3,)),
        reply=("!", (True,)),
        result=True,
    ),
    Call(
        "set_gui_slider",
        FunctionID.SET_GUI_SLIDER,
        (3, 3, 3, 8, DEVICE.Direction.VERTICAL, 3),
        sent=("B B B B B B", (3, 3, 3, 8, 1, 3)),
    ),
    Call(
        "set_gui_slider",
        FunctionID.SET_GUI_SLIDER,
        (3, 3, 3, 8, DEVICE.Direction.VERTICAL, 3, False),
        sent=("B B B B B B", (3, 3, 3, 8, 1, 3)),
        response_expected=False,
    ),
    Call(
        "get_gui_slider",
        FunctionID.GET_GUI_SLIDER,
        (3,),
        sent=("B", (3,)),
        reply=("! B B B B B", (True, 4, 5, 8, 1, 8)),
        result=GetGUISlider(True, 4, 5, 8, DEVICE.Direction.VERTICAL, 8),
    ),
    Call("remove_gui_slider", FunctionID.REMOVE_GUI_SLIDER, (3,), sent=("B", (3,))),
    Call("remove_gui_slider", FunctionID.REMOVE_GUI_SLIDER, (3, False), sent=("B", (3,)), response_expected=False),
    Call(
        "set_gui_slider_value_callback_configuration",
        FunctionID.SET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_gui_slider_value_callback_configuration",
        FunctionID.SET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_gui_slider_value_callback_configuration",
        FunctionID.GET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("get_gui_slider_value", FunctionID.GET_GUI_SLIDER_VALUE, (3,), sent=("B", (3,)), reply=("B", (3,)), result=3),
    Call(
        "set_gui_tab_configuration",
        FunctionID.SET_GUI_TAB_CONFIGURATION,
        (DEVICE.ChangeTabOn.CLICK_AND_SWIPE, True),
        sent=("B !", (3, True)),
    ),
    Call(
        "set_gui_tab_configuration",
        FunctionID.SET_GUI_TAB_CONFIGURATION,
        (DEVICE.ChangeTabOn.CLICK_AND_SWIPE, True, False),
        sent=("B !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_gui_tab_configuration",
        FunctionID.GET_GUI_TAB_CONFIGURATION,
        (),
        reply=("B !", (3, True)),
        result=GetGUITabConfiguration(DEVICE.ChangeTabOn.CLICK_AND_SWIPE, True),
    ),
    Call("set_gui_tab_text", FunctionID.SET_GUI_TAB_TEXT, (3, "abc"), sent=("B 5s", (3, b"abc"))),
    Call(
        "set_gui_tab_text",
        FunctionID.SET_GUI_TAB_TEXT,
        (3, "abc", False),
        sent=("B 5s", (3, b"abc")),
        response_expected=False,
    ),
    Call(
        "get_gui_tab_text",
        FunctionID.GET_GUI_TAB_TEXT,
        (3,),
        sent=("B", (3,)),
        reply=("! 5s", (True, b"abc")),
        result=GetGUITabText(True, "abc"),
    ),
    Call(
        "set_gui_tab_icon",
        FunctionID.SET_GUI_TAB_ICON,
        (3, [i % 2 == 0 for i in range(168)]),
        sent=("B 168!", (3, [i % 2 == 0 for i in range(168)])),
    ),
    Call(
        "set_gui_tab_icon",
        FunctionID.SET_GUI_TAB_ICON,
        (3, [i % 2 == 0 for i in range(168)], False),
        sent=("B 168!", (3, [i % 2 == 0 for i in range(168)])),
        response_expected=False,
    ),
    Call(
        "get_gui_tab_icon",
        FunctionID.GET_GUI_TAB_ICON,
        (3,),
        sent=("B", (3,)),
        reply=("! 168!", (True, [i % 2 == 0 for i in range(168)])),
        result=GetGUITabIcon(True, tuple(i % 2 == 0 for i in range(168))),
    ),
    Call("remove_gui_tab", FunctionID.REMOVE_GUI_TAB, (3,), sent=("B", (3,))),
    Call("remove_gui_tab", FunctionID.REMOVE_GUI_TAB, (3, False), sent=("B", (3,)), response_expected=False),
    Call("set_gui_tab_selected", FunctionID.SET_GUI_TAB_SELECTED, (3,), sent=("B", (3,))),
    Call(
        "set_gui_tab_selected", FunctionID.SET_GUI_TAB_SELECTED, (3, False), sent=("B", (3,)), response_expected=False
    ),
    Call(
        "set_gui_tab_selected_callback_configuration",
        FunctionID.SET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True),
        sent=("I !", (3, True)),
    ),
    Call(
        "set_gui_tab_selected_callback_configuration",
        FunctionID.SET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION,
        (Decimal("0.003"), True, False),
        sent=("I !", (3, True)),
        response_expected=False,
    ),
    Call(
        "get_gui_tab_selected_callback_configuration",
        FunctionID.GET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION,
        (),
        reply=("I !", (3, True)),
        result=SimpleCallbackConfiguration(Decimal("0.003"), True),
    ),
    Call("get_gui_tab_selected", FunctionID.GET_GUI_TAB_SELECTED, (), reply=("b", (3,)), result=3),
    Call(
        "set_gui_graph_configuration",
        FunctionID.SET_GUI_GRAPH_CONFIGURATION,
        (3, DEVICE.GraphType.BAR, 3, 3, 3, 3, "abc", "abc"),
        sent=("B B B B B B 4s 4s", (3, 2, 3, 3, 3, 3, b"abc", b"abc")),
    ),
    Call(
        "set_gui_graph_configuration",
        FunctionID.SET_GUI_GRAPH_CONFIGURATION,
        (3, DEVICE.GraphType.BAR, 3, 3, 3, 3, "abc", "abc", False),
        sent=("B B B B B B 4s 4s", (3, 2, 3, 3, 3, 3, b"abc", b"abc")),
        response_expected=False,
    ),
    Call(
        "get_gui_graph_configuration",
        FunctionID.GET_GUI_GRAPH_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
        reply=("! B B B B B 4s 4s", (True, 2, 5, 6, 7, 8, b"abc", b"abc")),
        result=GetGUIGraphConfiguration(True, DEVICE.GraphType.BAR, 5, 6, 7, 8, "abc", "abc"),
    ),
    Call(
        "set_gui_graph_data_low_level",
        FunctionID.SET_GUI_GRAPH_DATA_LOW_LEVEL,
        (3, 3, 3, [i % 256 for i in range(59)]),
        sent=("B H H 59B", (3, 3, 3, [i % 256 for i in range(59)])),
    ),
    Call(
        "set_gui_graph_data_low_level",
        FunctionID.SET_GUI_GRAPH_DATA_LOW_LEVEL,
        (3, 3, 3, [i % 256 for i in range(59)], False),
        sent=("B H H 59B", (3, 3, 3, [i % 256 for i in range(59)])),
        response_expected=False,
    ),
    Call(
        "get_gui_graph_data_low_level",
        FunctionID.GET_GUI_GRAPH_DATA_LOW_LEVEL,
        (3,),
        sent=("B", (3,)),
        reply=("H H 59B", (3, 4, [i % 256 for i in range(59)])),
        result=GetGUIGraphData(3, 4, tuple(i % 256 for i in range(59))),
    ),
    Call("remove_gui_graph", FunctionID.REMOVE_GUI_GRAPH, (3,), sent=("B", (3,))),
    Call("remove_gui_graph", FunctionID.REMOVE_GUI_GRAPH, (3, False), sent=("B", (3,)), response_expected=False),
    Call("remove_all_gui", FunctionID.REMOVE_ALL_GUI, ()),
    Call("remove_all_gui", FunctionID.REMOVE_ALL_GUI, (False,), response_expected=False),
    Call(
        "set_touch_led_config", FunctionID.SET_TOUCH_LED_CONFIG, (DEVICE.TouchLEDConfig.SHOW_TOUCH,), sent=("B", (3,))
    ),
    Call(
        "set_touch_led_config",
        FunctionID.SET_TOUCH_LED_CONFIG,
        (DEVICE.TouchLEDConfig.SHOW_TOUCH, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_touch_led_config",
        FunctionID.GET_TOUCH_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.TouchLEDConfig.SHOW_TOUCH,
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TOUCH_POSITION_CALLBACK_CONFIGURATION,
        (0, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TOUCH_POSITION_CALLBACK_CONFIGURATION,
        (0,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_TOUCH_GESTURE_CALLBACK_CONFIGURATION,
        (1, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_TOUCH_GESTURE_CALLBACK_CONFIGURATION,
        (1,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION,
        (2, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_GUI_BUTTON_PRESSED_CALLBACK_CONFIGURATION,
        (2,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION,
        (3, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_GUI_SLIDER_VALUE_CALLBACK_CONFIGURATION,
        (3,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
    Call("get_value", FunctionID.GET_GUI_TAB_SELECTED, (4,), reply=("b", (3,)), result=3),
    Call(
        "set_callback_configuration",
        FunctionID.SET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION,
        (4, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_GUI_TAB_SELECTED_CALLBACK_CONFIGURATION,
        (4,),
        reply=("I !", (1000, True)),
        result=AdvancedCallbackConfiguration(Decimal(1), True, None, None, None),
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write_pixels_low_level", (128, 3, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 64, 3, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 128, 3, 3, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 3, 64, 3, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 3, 3, 8193, 3, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 3, 3, 3, 65536, [i % 2 == 0 for i in range(448)])),
    ("write_pixels_low_level", (3, 3, 3, 3, 3, 3, ([i % 2 == 0 for i in range(448)])[:-1])),
    ("write_pixels", (3, 3, 3, 3, [True] * 65536)),
    ("read_pixels_low_level", (128, 3, 3, 3)),
    ("read_pixels_low_level", (3, 64, 3, 3)),
    ("read_pixels_low_level", (3, 3, 128, 3)),
    ("read_pixels_low_level", (3, 3, 3, 64)),
    ("set_display_configuration", (64, 3, True, True)),
    ("set_display_configuration", (3, 101, True, True)),
    ("write_line", (8, 3, "abc")),
    ("write_line", (3, 22, "abc")),
    ("set_touch_position_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_touch_gesture_callback_configuration", (Decimal("4294967.296"), True)),
    ("draw_line", (128, 3, 3, 3, DEVICE.Color.BLACK)),
    ("draw_line", (3, 64, 3, 3, DEVICE.Color.BLACK)),
    ("draw_line", (3, 3, 128, 3, DEVICE.Color.BLACK)),
    ("draw_line", (3, 3, 3, 64, DEVICE.Color.BLACK)),
    ("draw_line", (3, 3, 3, 3, 12345)),
    ("draw_box", (128, 3, 3, 3, True, DEVICE.Color.BLACK)),
    ("draw_box", (3, 64, 3, 3, True, DEVICE.Color.BLACK)),
    ("draw_box", (3, 3, 128, 3, True, DEVICE.Color.BLACK)),
    ("draw_box", (3, 3, 3, 64, True, DEVICE.Color.BLACK)),
    ("draw_box", (3, 3, 3, 3, True, 12345)),
    ("draw_text", (128, 3, DEVICE.Font.FONT_24X32, DEVICE.Color.BLACK, "abc")),
    ("draw_text", (3, 64, DEVICE.Font.FONT_24X32, DEVICE.Color.BLACK, "abc")),
    ("draw_text", (3, 3, 12345, DEVICE.Color.BLACK, "abc")),
    ("draw_text", (3, 3, DEVICE.Font.FONT_24X32, 12345, "abc")),
    ("set_gui_button", (12, 3, 3, 3, 3, "abc")),
    ("set_gui_button", (3, 128, 3, 3, 3, "abc")),
    ("set_gui_button", (3, 3, 64, 3, 3, "abc")),
    ("set_gui_button", (3, 3, 3, 129, 3, "abc")),
    ("set_gui_button", (3, 3, 3, 3, 65, "abc")),
    ("get_gui_button", (12,)),
    ("remove_gui_button", (256,)),
    ("set_gui_button_pressed_callback_configuration", (Decimal("4294967.296"), True)),
    ("get_gui_button_pressed", (12,)),
    ("set_gui_slider", (6, 3, 3, 8, DEVICE.Direction.VERTICAL, 3)),
    ("set_gui_slider", (3, 129, 3, 8, DEVICE.Direction.VERTICAL, 3)),
    ("set_gui_slider", (3, 3, 65, 8, DEVICE.Direction.VERTICAL, 3)),
    ("set_gui_slider", (3, 3, 3, 129, DEVICE.Direction.VERTICAL, 3)),
    ("set_gui_slider", (3, 3, 3, 8, 12345, 3)),
    ("set_gui_slider", (3, 3, 3, 8, DEVICE.Direction.VERTICAL, 121)),
    ("get_gui_slider", (6,)),
    ("remove_gui_slider", (256,)),
    ("set_gui_slider_value_callback_configuration", (Decimal("4294967.296"), True)),
    ("get_gui_slider_value", (6,)),
    ("set_gui_tab_configuration", (12345, True)),
    ("set_gui_tab_text", (10, "abc")),
    ("get_gui_tab_text", (10,)),
    ("set_gui_tab_icon", (10, [i % 2 == 0 for i in range(168)])),
    ("set_gui_tab_icon", (3, ([i % 2 == 0 for i in range(168)])[:-1])),
    ("get_gui_tab_icon", (10,)),
    ("remove_gui_tab", (256,)),
    ("set_gui_tab_selected", (10,)),
    ("set_gui_tab_selected_callback_configuration", (Decimal("4294967.296"), True)),
    ("set_gui_graph_configuration", (4, DEVICE.GraphType.BAR, 3, 3, 3, 3, "abc", "abc")),
    ("set_gui_graph_configuration", (3, 12345, 3, 3, 3, 3, "abc", "abc")),
    ("set_gui_graph_configuration", (3, DEVICE.GraphType.BAR, 128, 3, 3, 3, "abc", "abc")),
    ("set_gui_graph_configuration", (3, DEVICE.GraphType.BAR, 3, 64, 3, 3, "abc", "abc")),
    ("set_gui_graph_configuration", (3, DEVICE.GraphType.BAR, 3, 3, 119, 3, "abc", "abc")),
    ("set_gui_graph_configuration", (3, DEVICE.GraphType.BAR, 3, 3, 3, 64, "abc", "abc")),
    ("get_gui_graph_configuration", (4,)),
    ("set_gui_graph_data_low_level", (4, 3, 3, [i % 256 for i in range(59)])),
    ("set_gui_graph_data_low_level", (3, 119, 3, [i % 256 for i in range(59)])),
    ("set_gui_graph_data_low_level", (3, 3, 65536, [i % 256 for i in range(59)])),
    ("set_gui_graph_data_low_level", (3, 3, 3, ([i % 256 for i in range(59)])[:-1])),
    ("set_gui_graph_data", (3, [1] * 65536)),
    ("get_gui_graph_data_low_level", (4,)),
    ("remove_gui_graph", (256,)),
    ("set_touch_led_config", (12345,)),
    ("get_value", (5,)),
    ("set_callback_configuration", (5,)),
    ("get_callback_configuration", (5,)),
]


def test_identity(device):
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 298
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("LCD 128x64 Bricklet with uid 12345")


def test_ids_match_the_official_bindings():
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_write_pixels_transfers_the_stream(device, connection):
    """The high-level function write_pixels() uses write_pixels_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    result = run(device.write_pixels(*(3, 3, 3, 3, data)))
    assert connection.requests == [
        request(
            FunctionID.WRITE_PIXELS_LOW_LEVEL,
            "B B B B H H 448!",
            *(3, 3, 3, 3, 3, offset, chunk([i % 2 == 0 for i in range(3)], offset, 448, False)),
        )
        for offset in range(0, 1, 448)
    ]
    assert result is None


def test_read_pixels_transfers_the_stream(device, connection):
    """The high-level function read_pixels() uses read_pixels_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    for offset in range(0, 1, 480):
        connection.reply(FunctionID.READ_PIXELS_LOW_LEVEL, "H H 480!", *(3, offset, chunk(data, offset, 480, False)))
    result = run(device.read_pixels(*(3, 3, 3, 3)))
    assert connection.requests == [request(FunctionID.READ_PIXELS_LOW_LEVEL, "B B B B", *(3, 3, 3, 3))] * 1
    assert result == tuple(i % 2 == 0 for i in range(3))


def test_set_gui_graph_data_transfers_the_stream(device, connection):
    """The high-level function set_gui_graph_data() uses set_gui_graph_data_low_level()."""
    data = [i % 256 for i in range(3)]
    result = run(device.set_gui_graph_data(*(3, data)))
    assert connection.requests == [
        request(
            FunctionID.SET_GUI_GRAPH_DATA_LOW_LEVEL,
            "B H H 59B",
            *(3, 3, offset, chunk([i % 256 for i in range(3)], offset, 59, 0)),
        )
        for offset in range(0, 1, 59)
    ]
    assert result is None


def test_get_gui_graph_data_transfers_the_stream(device, connection):
    """The high-level function get_gui_graph_data() uses get_gui_graph_data_low_level()."""
    data = [i % 256 for i in range(3)]
    for offset in range(0, 1, 59):
        connection.reply(FunctionID.GET_GUI_GRAPH_DATA_LOW_LEVEL, "H H 59B", *(3, offset, chunk(data, offset, 59, 0)))
    result = run(device.get_gui_graph_data(*(3,)))
    assert connection.requests == [request(FunctionID.GET_GUI_GRAPH_DATA_LOW_LEVEL, "B", *(3,))] * 1
    assert result == bytes([i % 256 for i in range(3)])


def test_callback_touch_position(device, connection):
    """The callback TOUCH_POSITION is converted to an event."""
    connection.callback(CallbackID.TOUCH_POSITION, "H H H I", *(3, 4, 5, 6))
    assert summary(read_events(device)) == [(0, CallbackID.TOUCH_POSITION, GetTouchPosition(3, 4, 5, Decimal("0.006")))]


def test_callback_touch_gesture(device, connection):
    """The callback TOUCH_GESTURE is converted to an event."""
    connection.callback(CallbackID.TOUCH_GESTURE, "B I H H H H H I", *(3, 4, 5, 6, 7, 8, 9, 10))
    assert summary(read_events(device)) == [
        (
            1,
            CallbackID.TOUCH_GESTURE,
            GetTouchGesture(DEVICE.Gesture.BOTTOM_TO_TOP, Decimal("0.004"), 5, 6, 7, 8, 9, Decimal("0.01")),
        )
    ]


def test_callback_gui_button_pressed(device, connection):
    """The callback GUI_BUTTON_PRESSED is converted to an event."""
    connection.callback(CallbackID.GUI_BUTTON_PRESSED, "B !", *(3, True))
    assert summary(read_events(device)) == [(2, CallbackID.GUI_BUTTON_PRESSED, GUIButtonPressedEvent(3, True))]


def test_callback_gui_slider_value(device, connection):
    """The callback GUI_SLIDER_VALUE is converted to an event."""
    connection.callback(CallbackID.GUI_SLIDER_VALUE, "B B", *(3, 4))
    assert summary(read_events(device)) == [(3, CallbackID.GUI_SLIDER_VALUE, GUISliderValueEvent(3, 4))]


def test_callback_gui_tab_selected(device, connection):
    """The callback GUI_TAB_SELECTED is converted to an event."""
    connection.callback(CallbackID.GUI_TAB_SELECTED, "b", *(3,))
    assert summary(read_events(device)) == [(4, CallbackID.GUI_TAB_SELECTED, 3)]
