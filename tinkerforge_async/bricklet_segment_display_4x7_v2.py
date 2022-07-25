"""
Module for the Tinkerforge Segment Display 4x7 Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Segment_Display_4x7_V2.html) implemented using Python asyncIO. It
does the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI
units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, Iterable, NamedTuple

from .devices import BrickletWithMCU, DeviceIdentifier, Event, _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    COUNTER_FINISHED = 10


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_SEGMENTS = 1
    GET_SEGMENTS = 2
    SET_BRIGHTNESS = 3
    GET_BRIGHTNESS = 4
    SET_NUMERIC_VALUE = 5
    SET_SELECTED_SEGMENT = 6
    GET_SELECTED_SEGMENT = 7
    START_COUNTER = 8
    GET_COUNTER_VALUE = 9


class GetSegments(NamedTuple):
    segments: tuple[int, int, int, int]
    colon: tuple[bool, bool]
    tick: bool


class BrickletSegmentDisplay4x7V2(BrickletWithMCU):
    """
    Four 7-segment displays with switchable dots
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_SEGMENT_DISPLAY_4x7_V2
    DEVICE_DISPLAY_NAME = "Segment Display 4x7 Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.COUNTER_FINISHED: "",
    }

    SID_TO_CALLBACK = {0: (CallbackID.COUNTER_FINISHED,)}

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def set_segments(
        self,
        segments: tuple[int, int, int, int] = (0, 0, 0, 0),
        colon: tuple[bool, bool] = (False, False),
        tick: bool = False,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the segments of the Segment Display 4x7 Bricklet 2.0 segment-by-segment.

        The data is split into the four digits, two colon dots and the tick mark.

        The indices of the segments in the digit and colon parameters are as follows:

        .. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_segment_index.png
           :scale: 100 %
           :alt: Indices of segments
           :align: center
        """
        assert len(segments) == 4 and all(0 <= segment <= 255 for segment in segments)
        assert len(colon) == 2
        tick = bool(tick)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SEGMENTS,
            data=pack_payload((list(map(int, segments)), list(map(bool, colon)), tick), "4B 2! !"),
            response_expected=response_expected,
        )

    async def get_segments(self) -> GetSegments:
        """
        Returns the segment data as set by :func:`Set Segments`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SEGMENTS, response_expected=True
        )
        return GetSegments(*unpack_payload(payload, "4B 2! !"))

    async def set_brightness(self, brightness: int = 7, response_expected: bool = True) -> None:
        """
        The brightness can be set between 0 (dark) and 7 (bright).

        The default value is 7.
        """
        assert 0 <= brightness <= 7

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BRIGHTNESS,
            data=pack_payload((int(brightness),), "B"),
            response_expected=response_expected,
        )

    async def get_brightness(self) -> int:
        """
        Returns the brightness as set by :func:`Set Brightness`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BRIGHTNESS, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_numeric_value(self, value: Iterable[int], response_expected: bool = True) -> None:
        """
        Sets a numeric value for each of the digits. The values can be between
        -2 and 15. They represent:

        * -2: minus sign
        * -1: blank
        * 0-9: 0-9
        * 10: A
        * 11: b
        * 12: C
        * 13: d
        * 14: E
        * 15: F

        Example: A call with [-2, -1, 4, 2] will result in a display of "- 42".
        """
        value = list(map(int, value))

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_NUMERIC_VALUE,
            data=pack_payload((value,), "4b"),
            response_expected=response_expected,
        )

    async def set_selected_segment(self, segment: int, value: bool, response_expected: bool = True) -> None:
        """
        Turns one specified segment on or off.

        The indices of the segments are as follows:

        .. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_selected_segment_index.png
           :scale: 100 %
           :alt: Indices of selected segments
           :align: center
        """
        assert 0 <= segment <= 34

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SELECTED_SEGMENT,
            data=pack_payload((int(segment), bool(value)), "B !"),
            response_expected=response_expected,
        )

    async def get_selected_segment(self, segment: int) -> bool:
        """
        Returns the value of a single segment.
        """
        assert 0 <= segment <= 34

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SELECTED_SEGMENT,
            data=pack_payload((int(segment),), "B"),
            response_expected=True,
        )

        return unpack_payload(payload, "!")

    async def start_counter(  # pylint: disable=too-many-arguments
        self, value_from: int, value_to: int, increment: int, length: int, response_expected: bool = True
    ) -> None:
        """
        Turns one specified segment on or off.

        The indices of the segments are as follows:

        .. image:: /Images/Bricklets/bricklet_segment_display_4x7_v2_selected_segment_index.png
           :scale: 100 %
           :alt: Indices of selected segments
           :align: center
        """
        assert -999 <= value_from <= 9999
        assert -999 <= value_to <= 9999
        assert -999 <= increment <= 9999

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.START_COUNTER,
            data=pack_payload(
                (
                    int(value_from),
                    int(value_to),
                    int(increment),
                    int(length),
                ),
                "h h h I",
            ),
            response_expected=response_expected,
        )

    async def get_counter_value(self) -> int:
        """
        Returns the counter value that is currently shown on the display.

        If there is no counter running a 0 will be returned.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COUNTER_VALUE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def read_events(
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        registered_events = set()
        if events:
            for event in events:
                registered_events.add(self.CallbackID(event))
        if sids is not None:
            for sid in sids:
                for callback in self.SID_TO_CALLBACK.get(sid, []):
                    registered_events.add(callback)

        if events is None and sids is None:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                yield Event(self, 0, function_id, value)
