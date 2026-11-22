"""
Module for the Tinkerforge CAN Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/CAN_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from collections.abc import Sequence
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import Channel, Device, DeviceIdentifier, _FunctionID
from .helper import check_length, check_range
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    FRAME_READ = 11
    FRAME_READABLE = 14


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    WRITE_FRAME = 1
    READ_FRAME = 2
    ENABLE_FRAME_READ_CALLBACK = 3
    DISABLE_FRAME_READ_CALLBACK = 4
    IS_FRAME_READ_CALLBACK_ENABLED = 5
    SET_CONFIGURATION = 6
    GET_CONFIGURATION = 7
    SET_READ_FILTER = 8
    GET_READ_FILTER = 9
    GET_ERROR_LOG = 10
    SET_FRAME_READABLE_CALLBACK_CONFIGURATION = 12
    GET_FRAME_READABLE_CALLBACK_CONFIGURATION = 13


@unique
class FrameType(Enum):
    """
    The frame type options
    """

    STANDARD_DATA = 0
    STANDARD_REMOTE = 1
    EXTENDED_DATA = 2
    EXTENDED_REMOTE = 3


@unique
class BaudRate(Enum):
    """
    The baud rate options
    """

    BAUD_RATE_10KBPS = 0
    BAUD_RATE_20KBPS = 1
    BAUD_RATE_50KBPS = 2
    BAUD_RATE_125KBPS = 3
    BAUD_RATE_250KBPS = 4
    BAUD_RATE_500KBPS = 5
    BAUD_RATE_800KBPS = 6
    BAUD_RATE_1000KBPS = 7


@unique
class TransceiverMode(Enum):
    """
    The transceiver mode options
    """

    NORMAL = 0
    LOOPBACK = 1
    READ_ONLY = 2


@unique
class FilterMode(Enum):
    """
    The filter mode options
    """

    DISABLED = 0
    ACCEPT_ALL = 1
    MATCH_STANDARD = 2
    MATCH_STANDARD_AND_DATA = 3
    MATCH_EXTENDED = 4


class ReadFrame(NamedTuple):
    success: bool
    frame_type: FrameType
    identifier: int
    data: tuple[int, ...]
    length: int


class GetConfiguration(NamedTuple):
    baud_rate: BaudRate
    transceiver_mode: TransceiverMode
    write_timeout: int


class GetReadFilter(NamedTuple):
    mode: FilterMode
    mask: int
    filter1: int
    filter2: int


class GetErrorLog(NamedTuple):
    write_error_level: int
    read_error_level: int
    transceiver_disabled: bool
    write_timeout_count: int
    read_register_overflow_count: int
    read_buffer_overflow_count: int


class FrameReadEvent(NamedTuple):
    frame_type: FrameType
    identifier: int
    data: tuple[int, ...]
    length: int


class BrickletCAN(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Communicates with CAN bus devices
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_CAN
    DEVICE_DISPLAY_NAME = "CAN Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    FrameType: TypeAlias = FrameType
    BaudRate: TypeAlias = BaudRate
    TransceiverMode: TypeAlias = TransceiverMode
    FilterMode: TypeAlias = FilterMode

    CALLBACK_FORMATS = {
        CallbackID.FRAME_READ: "B I 8B B",
        CallbackID.FRAME_READABLE: "",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.FRAME_READ,)),
        Channel(1, callbacks=(CallbackID.FRAME_READABLE,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def write_frame(
        self, frame_type: FrameType | int, identifier: int, data: bytes | Sequence[int], length: int
    ) -> bool:
        """
        Writes a data or remote frame to the write buffer to be transmitted over the
        CAN transceiver.

        The Bricklet supports the standard 11-bit (CAN 2.0A) and the additional extended
        18-bit (CAN 2.0B) identifiers. For standard frames the Bricklet uses bit 0 to 10
        from the ``identifier`` parameter as standard 11-bit identifier. For extended
        frames the Bricklet additionally uses bit 11 to 28 from the ``identifier``
        parameter as extended 18-bit identifier.

        For remote frames the ``data`` parameter is ignored.

        Returns *true* if the frame was successfully added to the write buffer. Returns
        *false* if the frame could not be added because write buffer is already full.

        The write buffer can overflow if frames are written to it at a higher rate
        than the Bricklet can transmitted them over the CAN transceiver. This may
        happen if the CAN transceiver is configured as read-only or is using a low baud
        rate (see :func:`set_configuration`). It can also happen if the CAN bus is
        congested and the frame cannot be transmitted because it constantly loses
        arbitration or because the CAN transceiver is currently disabled due to a high
        write error level (see :func:`get_error_log`).
        """
        identifier = int(identifier)
        check_range("identifier", identifier, 0, 1073741823)
        check_length("data", data, 8)
        length = int(length)
        check_range("length", length, 0, 15)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_FRAME,
            data=pack_payload((FrameType(frame_type).value, identifier, list(map(int, data)), length), "B I 8B B"),
            response_expected=True,
        )
        return unpack_payload(payload, "!")

    async def read_frame(self) -> ReadFrame:
        """
        Tries to read the next data or remote frame from the read buffer and return it.
        If a frame was successfully read, then the ``success`` return value is set to
        *true* and the other return values contain the frame. If the read buffer is
        empty and no frame could be read, then the ``success`` return value is set to
        *false* and the other return values contain invalid data.

        The ``identifier`` return value follows the identifier format described for
        :func:`write_frame`.

        For remote frames the ``data`` return value always contains invalid data.

        A configurable read filter can be used to define which frames should be
        received by the CAN transceiver and put into the read buffer (see
        :func:`set_read_filter`).

        Instead of polling with this function, you can also use callbacks. See the
        :func:`enable_frame_read_callback` function and the :attr:`CallbackID.FRAME_READ` callback.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READ_FRAME, response_expected=True
        )
        success, frame_type, identifier, data, length = unpack_payload(payload, "! B I 8B B")
        return ReadFrame(success, FrameType(frame_type), identifier, tuple(data), length)

    async def enable_frame_read_callback(self, response_expected: bool = True) -> None:
        """
        Enables the :attr:`CallbackID.FRAME_READ` callback.

        By default the callback is disabled. Enabling this callback will disable the :attr:`CallbackID.FRAME_READABLE`
        callback.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_FRAME_READ_CALLBACK, response_expected=response_expected
        )

    async def disable_frame_read_callback(self, response_expected: bool = True) -> None:
        """
        Disables the :attr:`CallbackID.FRAME_READ` callback.

        By default the callback is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_FRAME_READ_CALLBACK, response_expected=response_expected
        )

    async def is_frame_read_callback_enabled(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.FRAME_READ` callback is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_FRAME_READ_CALLBACK_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_configuration(
        self,
        baud_rate: BaudRate | int = BaudRate.BAUD_RATE_125KBPS,
        transceiver_mode: TransceiverMode | int = TransceiverMode.NORMAL,
        write_timeout: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration for the CAN bus communication.

        The baud rate can be configured in steps between 10 and 1000 kbit/s.

        The CAN transceiver has three different modes:

        * Normal: Reads from and writes to the CAN bus and performs active bus
          error detection and acknowledgement.
        * Loopback: All reads and writes are performed internally. The transceiver
          is disconnected from the actual CAN bus.
        * Read-Only: Only reads from the CAN bus, but does neither active bus error
          detection nor acknowledgement. Only the receiving part of the transceiver
          is connected to the CAN bus.

        The write timeout has three different modes that define how a failed frame
        transmission should be handled:

        * One-Shot (= -1): Only one transmission attempt will be made. If the
          transmission fails then the frame is discarded.
        * Infinite (= 0): Infinite transmission attempts will be made. The frame will
          never be discarded.
        * Milliseconds (> 0): A limited number of transmission attempts will be made.
          If the frame could not be transmitted successfully after the configured
          number of milliseconds then the frame is discarded.
        """
        write_timeout = int(write_timeout)
        check_range("write_timeout", write_timeout, -2147483648, 2147483647)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload(
                (BaudRate(baud_rate).value, TransceiverMode(transceiver_mode).value, write_timeout), "B B i"
            ),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        baud_rate, transceiver_mode, write_timeout = unpack_payload(payload, "B B i")
        return GetConfiguration(BaudRate(baud_rate), TransceiverMode(transceiver_mode), write_timeout)

    async def set_read_filter(
        self, mode: FilterMode | int, mask: int, filter1: int, filter2: int, response_expected: bool = True
    ) -> None:
        """
        Set the read filter configuration. This can be used to define which frames
        should be received by the CAN transceiver and put into the read buffer.

        The read filter has five different modes that define if and how the mask and
        the two filters are applied:

        * Disabled: No filtering is applied at all. All frames are received even
          incomplete and defective frames. This mode should be used for debugging only.
        * Accept-All: All complete and error-free frames are received.
        * Match-Standard: Only standard frames with a matching identifier are received.
        * Match-Standard-and-Data: Only standard frames with matching identifier and
          data bytes are received.
        * Match-Extended: Only extended frames with a matching identifier are received.

        The mask and filters are used as bit masks. Their usage depends on the mode:

        * Disabled: Mask and filters are ignored.
        * Accept-All: Mask and filters are ignored.
        * Match-Standard: Bit 0 to 10 (11 bits) of mask and filters are used to match
          the 11-bit identifier of standard frames.
        * Match-Standard-and-Data: Bit 0 to 10 (11 bits) of mask and filters are used
          to match the 11-bit identifier of standard frames. Bit 11 to 18 (8 bits) and
          bit 19 to 26 (8 bits) of mask and filters are used to match the first and
          second data byte (if present) of standard frames.
        * Match-Extended: Bit 0 to 10 (11 bits) of mask and filters are used
          to match the standard 11-bit identifier part of extended frames. Bit 11 to 28
          (18 bits) of mask and filters are used to match the extended 18-bit identifier
          part of extended frames.

        The mask and filters are applied in this way: The mask is used to select the
        identifier and data bits that should be compared to the corresponding filter
        bits. All unselected bits are automatically accepted. All selected bits have
        to match one of the filters to be accepted. If all bits for the selected mode
        are accepted then the frame is accepted and is added to the read buffer.

        .. csv-table::
         :header: "Mask Bit", "Filter Bit", "Identifier/Data Bit", "Result"
         :widths: 10, 10, 10, 10

         0, X, X, Accept
         1, 0, 0, Accept
         1, 0, 1, Reject
         1, 1, 0, Reject
         1, 1, 1, Accept

        For example, to receive standard frames with identifier 0x123 only the mode can
        be set to Match-Standard with 0x7FF as mask and 0x123 as filter 1 and filter 2.
        The mask of 0x7FF selects all 11 identifier bits for matching so that the
        identifier has to be exactly 0x123 to be accepted.

        To accept identifier 0x123 and identifier 0x456 at the same time, just set
        filter 2 to 0x456 and keep mask and filter 1 unchanged.
        """
        mask = int(mask)
        check_range("mask", mask, 0, 1073741823)
        filter1 = int(filter1)
        check_range("filter1", filter1, 0, 1073741823)
        filter2 = int(filter2)
        check_range("filter2", filter2, 0, 1073741823)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_READ_FILTER,
            data=pack_payload((FilterMode(mode).value, mask, filter1, filter2), "B I I I"),
            response_expected=response_expected,
        )

    async def get_read_filter(self) -> GetReadFilter:
        """
        Returns the read filter as set by :func:`set_read_filter`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_READ_FILTER, response_expected=True
        )
        mode, mask, filter1, filter2 = unpack_payload(payload, "B I I I")
        return GetReadFilter(FilterMode(mode), mask, filter1, filter2)

    async def get_error_log(self) -> GetErrorLog:
        """
        Returns information about different kinds of errors.

        The write and read error levels indicate the current level of checksum,
        acknowledgement, form, bit and stuffing errors during CAN bus write and read
        operations.

        When the write error level exceeds 255 then the CAN transceiver gets disabled
        and no frames can be transmitted or received anymore. The CAN transceiver will
        automatically be activated again after the CAN bus is idle for a while.

        The write and read error levels are not available in read-only transceiver mode
        (see :func:`set_configuration`) and are reset to 0 as a side effect of changing
        the configuration or the read filter.

        The write timeout, read register and buffer overflow counts represents the
        number of these errors:

        * A write timeout occurs if a frame could not be transmitted before the
          configured write timeout expired (see :func:`set_configuration`).
        * A read register overflow occurs if the read register of the CAN transceiver
          still contains the last received frame when the next frame arrives. In this
          case the newly arrived frame is lost. This happens if the CAN transceiver
          receives more frames than the Bricklet can handle. Using the read filter
          (see :func:`set_read_filter`) can help to reduce the amount of received frames.
          This count is not exact, but a lower bound, because the Bricklet might not
          able detect all overflows if they occur in rapid succession.
        * A read buffer overflow occurs if the read buffer of the Bricklet is already
          full when the next frame should be read from the read register of the CAN
          transceiver. In this case the frame in the read register is lost. This
          happens if the CAN transceiver receives more frames to be added to the read
          buffer than are removed from the read buffer using the :func:`read_frame`
          function. Using the :attr:`CallbackID.FRAME_READ` callback ensures that the read buffer
          can not overflow.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_LOG, response_expected=True
        )
        (
            write_error_level,
            read_error_level,
            transceiver_disabled,
            write_timeout_count,
            read_register_overflow_count,
            read_buffer_overflow_count,
        ) = unpack_payload(payload, "B B ! I I I")
        return GetErrorLog(
            write_error_level,
            read_error_level,
            transceiver_disabled,
            write_timeout_count,
            read_register_overflow_count,
            read_buffer_overflow_count,
        )

    async def set_frame_readable_callback_configuration(
        self, enabled: bool = False, response_expected: bool = True
    ) -> None:
        """
        Enables/disables the :attr:`CallbackID.FRAME_READABLE` callback.

        By default the callback is disabled. Enabling this callback will disable the :attr:`CallbackID.FRAME_READ`
        callback.

        .. versionadded:: 2.0.1 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_frame_readable_callback_configuration(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.FRAME_READABLE` callback is enabled, *false* otherwise.

        .. versionadded:: 2.0.1 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.FRAME_READ:
            frame_type, identifier, data, length = value
            return 0, FrameReadEvent(FrameType(frame_type), identifier, tuple(data), length)
        return 1, None
