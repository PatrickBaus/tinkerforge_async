"""
Module for the Segment Display 4x7 Bricklet
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Segment_Display_4x7.html) implemented using Python asyncIO. It
does the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI
units.
"""
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple

from .devices import Device, DeviceIdentifier, Event, _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    COUNTER_FINISHED = 5


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_SEGMENTS = 1
    GET_SEGMENTS = 2
    START_COUNTER = 3
    GET_COUNTER_VALUE = 4


class GetSegments(NamedTuple):
    segments: tuple[int, int, int, int]
    brightness: int
    colon: bool


class BrickletSegmentDisplay4x7(Device):
    """
    Four 7-segment displays with switchable colon
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_SEGMENT_DISPLAY_4x7
    DEVICE_DISPLAY_NAME = "Segment Display 4x7 Bricklet"

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
        brightness: int = 7,
        colon: bool = False,
        response_expected: bool = True,
    ) -> None:
        """
        The 7-segment display can be set with bitmaps. Every bit controls one
        segment:

        .. image:: /Images/Bricklets/bricklet_segment_display_4x7_bit_order.png
           :scale: 100 %
           :alt: Bit order of one segment
           :align: center

        For example to set a "5" you would want to activate segments 0, 2, 3, 5 and 6.
        This is represented by the number 0b01101101 = 0x6d = 109.

        The brightness can be set between 0 (dark) and 7 (bright). The colon
        parameter turns the colon of the display on or off.
        """
        assert all(0 <= segment <= 127 for segment in segments)
        assert 0 <= brightness <= 7

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SEGMENTS,
            data=pack_payload(
                (
                    list(map(int, segments)),
                    int(brightness),
                    bool(colon),
                ),
                "4B B !",
            ),
            response_expected=response_expected,
        )

    async def get_segments(self) -> GetSegments:
        """
        Returns the segment, brightness and color data as set by
        :func:`Set Segments`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SEGMENTS, response_expected=True
        )
        return GetSegments(*unpack_payload(payload, "4B B !"))

    async def start_counter(  # pylint: disable=too-many-arguments
        self, value_from: int, value_to: int, increment: int = 1, length: int = 1000, response_expected: bool = True
    ) -> None:
        """
        Starts a counter with the *from* value that counts to the *to*
        value each step incremented with by *increment*.
        *length* is the pause between each increment.

        Example: If you set *from* to 0, *to* to 100, *increment* to 1 and
        *length* to 1000, a counter that goes from 0 to 100 with one second
        pause between each increment will be started.

        Using a negative increment allows to count backwards.

        You can stop the counter at every time by calling :func:`Set Segments`.
        """
        assert -999 <= value_from <= 9999
        assert -999 <= value_to <= 9999
        assert -999 <= increment <= 9999
        assert 0 <= length <= 2**32 - 1

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
