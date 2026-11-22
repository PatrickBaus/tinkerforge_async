"""
Module for the Tinkerforge CAN Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/CANV2_Bricklet_Python.html) implemented using
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
from .helper import check_length, check_range
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity
from .streams import pad_single_chunk

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    FRAME_READ = 16
    FRAME_READABLE = 19
    ERROR_OCCURRED = 22


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    WRITE_FRAME_LOW_LEVEL = 1
    READ_FRAME_LOW_LEVEL = 2
    SET_FRAME_READ_CALLBACK_CONFIGURATION = 3
    GET_FRAME_READ_CALLBACK_CONFIGURATION = 4
    SET_TRANSCEIVER_CONFIGURATION = 5
    GET_TRANSCEIVER_CONFIGURATION = 6
    SET_QUEUE_CONFIGURATION_LOW_LEVEL = 7
    GET_QUEUE_CONFIGURATION_LOW_LEVEL = 8
    SET_READ_FILTER_CONFIGURATION = 9
    GET_READ_FILTER_CONFIGURATION = 10
    GET_ERROR_LOG_LOW_LEVEL = 11
    SET_COMMUNICATION_LED_CONFIG = 12
    GET_COMMUNICATION_LED_CONFIG = 13
    SET_ERROR_LED_CONFIG = 14
    GET_ERROR_LED_CONFIG = 15
    SET_FRAME_READABLE_CALLBACK_CONFIGURATION = 17
    GET_FRAME_READABLE_CALLBACK_CONFIGURATION = 18
    SET_ERROR_OCCURRED_CALLBACK_CONFIGURATION = 20
    GET_ERROR_OCCURRED_CALLBACK_CONFIGURATION = 21


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

    ACCEPT_ALL = 0
    MATCH_STANDARD_ONLY = 1
    MATCH_EXTENDED_ONLY = 2
    MATCH_STANDARD_AND_EXTENDED = 3


@unique
class TransceiverState(Enum):
    """
    The transceiver state options
    """

    ACTIVE = 0
    PASSIVE = 1
    DISABLED = 2


@unique
class CommunicationLEDConfig(Enum):
    """
    The communication led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_COMMUNICATION = 3


@unique
class ErrorLEDConfig(Enum):
    """
    The error led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_TRANSCEIVER_STATE = 3
    SHOW_ERROR = 4


class ReadFrame(NamedTuple):
    success: bool
    frame_type: FrameType
    identifier: int
    data_length: int
    data_data: tuple[int, ...]


class ReadFrameResult(NamedTuple):
    success: bool
    frame_type: FrameType
    identifier: int
    data: bytes


class GetTransceiverConfiguration(NamedTuple):
    baud_rate: int
    sample_point: Decimal
    transceiver_mode: TransceiverMode


class GetQueueConfiguration(NamedTuple):
    write_buffer_size: int
    write_buffer_timeout: int
    write_backlog_size: int
    read_buffer_sizes_length: int
    read_buffer_sizes_data: tuple[int, ...]
    read_backlog_size: int


class GetQueueConfigurationResult(NamedTuple):
    write_buffer_size: int
    write_buffer_timeout: int
    write_backlog_size: int
    read_backlog_size: int
    read_buffer_sizes: tuple[int, ...]


class GetReadFilterConfiguration(NamedTuple):
    filter_mode: FilterMode
    filter_mask: int
    filter_identifier: int


class GetErrorLog(NamedTuple):
    transceiver_state: TransceiverState
    transceiver_write_error_level: int
    transceiver_read_error_level: int
    transceiver_stuffing_error_count: int
    transceiver_format_error_count: int
    transceiver_ack_error_count: int
    transceiver_bit1_error_count: int
    transceiver_bit0_error_count: int
    transceiver_crc_error_count: int
    write_buffer_timeout_error_count: int
    read_buffer_overflow_error_count: int
    read_buffer_overflow_error_occurred_length: int
    read_buffer_overflow_error_occurred_data: tuple[bool, ...]
    read_backlog_overflow_error_count: int


class GetErrorLogResult(NamedTuple):
    transceiver_state: TransceiverState
    transceiver_write_error_level: int
    transceiver_read_error_level: int
    transceiver_stuffing_error_count: int
    transceiver_format_error_count: int
    transceiver_ack_error_count: int
    transceiver_bit1_error_count: int
    transceiver_bit0_error_count: int
    transceiver_crc_error_count: int
    write_buffer_timeout_error_count: int
    read_buffer_overflow_error_count: int
    read_backlog_overflow_error_count: int
    read_buffer_overflow_error_occurred: tuple[bool, ...]


class FrameReadEvent(NamedTuple):
    frame_type: FrameType
    identifier: int
    data: bytes


DECI_PERCENT = LinearQuantity(1, 10)  # raw: 1/10 Percent, returned in %


class BrickletCANV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Communicates with CAN bus devices
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_CAN_V2
    DEVICE_DISPLAY_NAME = "CAN Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    FrameType: TypeAlias = FrameType
    TransceiverMode: TypeAlias = TransceiverMode
    FilterMode: TypeAlias = FilterMode
    TransceiverState: TypeAlias = TransceiverState
    CommunicationLEDConfig: TypeAlias = CommunicationLEDConfig
    ErrorLEDConfig: TypeAlias = ErrorLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.FRAME_READ: "B I B 15B",
        CallbackID.FRAME_READABLE: "",
        CallbackID.ERROR_OCCURRED: "",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.FRAME_READABLE,)),
        Channel(1, callbacks=(CallbackID.ERROR_OCCURRED,)),
        Channel(2, callbacks=(CallbackID.FRAME_READ,)),
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

    async def write_frame_low_level(
        self, frame_type: FrameType | int, identifier: int, data_length: int, data_data: bytes | Sequence[int]
    ) -> bool:
        """
        Writes a data or remote frame to the write queue to be transmitted over the
        CAN transceiver.

        The Bricklet supports the standard 11-bit (CAN 2.0A) and the additional extended
        29-bit (CAN 2.0B) identifiers. For standard frames the Bricklet uses bit 0 to 10
        from the ``identifier`` parameter as standard 11-bit identifier. For extended
        frames the Bricklet uses bit 0 to 28 from the ``identifier`` parameter as
        extended 29-bit identifier.

        The ``data`` parameter can be up to 15 bytes long. For data frames up to 8 bytes
        will be used as the actual data. The length (DLC) field in the data or remote
        frame will be set to the actual length of the ``data`` parameter. This allows
        to transmit data and remote frames with excess length. For remote frames only
        the length of the ``data`` parameter is used. The actual ``data`` bytes are
        ignored.

        Returns *true* if the frame was successfully added to the write queue. Returns
        *false* if the frame could not be added because write queue is already full or
        because the write buffer or the write backlog are configured with a size of
        zero (see :func:`set_queue_configuration`).

        The write queue can overflow if frames are written to it at a higher rate
        than the Bricklet can transmitted them over the CAN transceiver. This may
        happen if the CAN transceiver is configured as read-only or is using a low baud
        rate (see :func:`set_transceiver_configuration`). It can also happen if the CAN
        bus is congested and the frame cannot be transmitted because it constantly loses
        arbitration or because the CAN transceiver is currently disabled due to a high
        write error level (see :func:`get_error_log`).
        """
        identifier = int(identifier)
        check_range("identifier", identifier, 0, 1073741823)
        data_length = int(data_length)
        check_range("data_length", data_length, 0, 15)
        check_length("data_data", data_data, 15)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_FRAME_LOW_LEVEL,
            data=pack_payload(
                (FrameType(frame_type).value, identifier, data_length, list(map(int, data_data))), "B I B 15B"
            ),
            response_expected=True,
        )
        return unpack_payload(payload, "!")

    async def write_frame(self, frame_type: FrameType | int, identifier: int, data: bytes | Sequence[int]) -> bool:
        """
        Writes a data or remote frame to the write queue to be transmitted over the
        CAN transceiver.

        The Bricklet supports the standard 11-bit (CAN 2.0A) and the additional extended
        29-bit (CAN 2.0B) identifiers. For standard frames the Bricklet uses bit 0 to 10
        from the ``identifier`` parameter as standard 11-bit identifier. For extended
        frames the Bricklet uses bit 0 to 28 from the ``identifier`` parameter as
        extended 29-bit identifier.

        The ``data`` parameter can be up to 15 bytes long. For data frames up to 8 bytes
        will be used as the actual data. The length (DLC) field in the data or remote
        frame will be set to the actual length of the ``data`` parameter. This allows
        to transmit data and remote frames with excess length. For remote frames only
        the length of the ``data`` parameter is used. The actual ``data`` bytes are
        ignored.

        Returns *true* if the frame was successfully added to the write queue. Returns
        *false* if the frame could not be added because write queue is already full or
        because the write buffer or the write backlog are configured with a size of
        zero (see :func:`set_queue_configuration`).

        The write queue can overflow if frames are written to it at a higher rate
        than the Bricklet can transmitted them over the CAN transceiver. This may
        happen if the CAN transceiver is configured as read-only or is using a low baud
        rate (see :func:`set_transceiver_configuration`). It can also happen if the CAN
        bus is congested and the frame cannot be transmitted because it constantly loses
        arbitration or because the CAN transceiver is currently disabled due to a high
        write error level (see :func:`get_error_log`).

        This function transfers the complete data stream and calls :func:`write_frame_low_level` as often as necessary.
        Concurrent transfers of the stream are serialized.
        """
        chunk = pad_single_chunk([int(item) for item in data], name="data", chunk_size=15, padding=0)
        length = len(data)
        return await self.write_frame_low_level(frame_type, identifier, length, chunk)

    async def read_frame_low_level(self) -> ReadFrame:
        """
        Tries to read the next data or remote frame from the read queue and returns it.
        If a frame was successfully read, then the ``success`` return value is set to
        *true* and the other return values contain the frame. If the read queue is
        empty and no frame could be read, then the ``success`` return value is set to
        *false* and the other return values contain invalid data.

        The ``identifier`` return value follows the identifier format described for
        :func:`write_frame`.

        The ``data`` return value can be up to 15 bytes long. For data frames up to the
        first 8 bytes are the actual received data. All bytes after the 8th byte are
        always zero and only there to indicate the length of a data or remote frame
        with excess length. For remote frames the length of the ``data`` return value
        represents the requested length. The actual ``data`` bytes are always zero.

        A configurable read filter can be used to define which frames should be
        received by the CAN transceiver and put into the read queue (see
        :func:`set_read_filter_configuration`).

        Instead of polling with this function, you can also use callbacks. See the
        :func:`set_frame_read_callback_configuration` function and the :attr:`CallbackID.FRAME_READ`
        callback.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READ_FRAME_LOW_LEVEL, response_expected=True
        )
        success, frame_type, identifier, data_length, data_data = unpack_payload(payload, "! B I B 15B")
        return ReadFrame(success, FrameType(frame_type), identifier, data_length, tuple(data_data))

    async def read_frame(self) -> ReadFrameResult:
        """
        Tries to read the next data or remote frame from the read queue and returns it.
        If a frame was successfully read, then the ``success`` return value is set to
        *true* and the other return values contain the frame. If the read queue is
        empty and no frame could be read, then the ``success`` return value is set to
        *false* and the other return values contain invalid data.

        The ``identifier`` return value follows the identifier format described for
        :func:`write_frame`.

        The ``data`` return value can be up to 15 bytes long. For data frames up to the
        first 8 bytes are the actual received data. All bytes after the 8th byte are
        always zero and only there to indicate the length of a data or remote frame
        with excess length. For remote frames the length of the ``data`` return value
        represents the requested length. The actual ``data`` bytes are always zero.

        A configurable read filter can be used to define which frames should be
        received by the CAN transceiver and put into the read queue (see
        :func:`set_read_filter_configuration`).

        Instead of polling with this function, you can also use callbacks. See the
        :func:`set_frame_read_callback_configuration` function and the :attr:`CallbackID.FRAME_READ`
        callback.

        This function transfers the complete data stream and calls :func:`read_frame_low_level` as often as necessary.
        Concurrent transfers of the stream are serialized.
        """
        result = await self.read_frame_low_level()
        return ReadFrameResult(
            result.success, result.frame_type, result.identifier, bytes(result.data_data[: result.data_length])
        )

    async def set_frame_read_callback_configuration(
        self, enabled: bool = False, response_expected: bool = True
    ) -> None:
        """
        Enables and disables the :attr:`CallbackID.FRAME_READ` callback.

        By default the callback is disabled. Enabling this callback will disable the :attr:`CallbackID.FRAME_READABLE`
        callback.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_READ_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_frame_read_callback_configuration(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.FRAME_READ` callback is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_READ_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_transceiver_configuration(
        self,
        baud_rate: int = 125000,
        sample_point: float | Decimal = Decimal("62.5"),
        transceiver_mode: TransceiverMode | int = TransceiverMode.NORMAL,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the transceiver configuration for the CAN bus communication.

        The CAN transceiver has three different modes:

        * Normal: Reads from and writes to the CAN bus and performs active bus
          error detection and acknowledgement.
        * Loopback: All reads and writes are performed internally. The transceiver
          is disconnected from the actual CAN bus.
        * Read-Only: Only reads from the CAN bus, but does neither active bus error
          detection nor acknowledgement. Only the receiving part of the transceiver
          is connected to the CAN bus.

        Units: sample_point in % (50 to 90 %).
        """
        baud_rate = int(baud_rate)
        check_range("baud_rate", baud_rate, 10000, 1000000)
        sample_point_raw = DECI_PERCENT.from_si(sample_point)
        check_range("sample_point", sample_point_raw, 500, 900, sample_point)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TRANSCEIVER_CONFIGURATION,
            data=pack_payload((baud_rate, sample_point_raw, TransceiverMode(transceiver_mode).value), "I H B"),
            response_expected=response_expected,
        )

    async def get_transceiver_configuration(self) -> GetTransceiverConfiguration:
        """
        Returns the configuration as set by :func:`set_transceiver_configuration`.

        Units: sample_point in % (50 to 90 %).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TRANSCEIVER_CONFIGURATION, response_expected=True
        )
        baud_rate, sample_point, transceiver_mode = unpack_payload(payload, "I H B")
        return GetTransceiverConfiguration(
            baud_rate, DECI_PERCENT.to_si(sample_point), TransceiverMode(transceiver_mode)
        )

    async def set_queue_configuration_low_level(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        write_buffer_size: int,
        write_buffer_timeout: int,
        write_backlog_size: int,
        read_buffer_sizes_length: int,
        read_buffer_sizes_data: Sequence[int],
        read_backlog_size: int = 383,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the write and read queue configuration.

        The CAN transceiver has 32 buffers in total in hardware for transmitting and
        receiving frames. Additionally, the Bricklet has a backlog for 768 frames in
        total in software. The buffers and the backlog can be freely assigned to the
        write and read queues.

        :func:`write_frame` writes a frame into the write backlog. The Bricklet moves
        the frame from the backlog into a free write buffer. The CAN transceiver then
        transmits the frame from the write buffer to the CAN bus. If there are no
        write buffers (``write_buffer_size`` is zero) or there is no write backlog
        (``write_backlog_size`` is zero) then no frames can be transmitted and
        :func:`write_frame` returns always *false*.

        The CAN transceiver receives a frame from the CAN bus and stores it into a
        free read buffer. The Bricklet moves the frame from the read buffer into the
        read backlog. :func:`read_frame` reads the frame from the read backlog and
        returns it. If there are no read buffers (``read_buffer_sizes`` is empty) or
        there is no read backlog (``read_backlog_size`` is zero) then no frames can be
        received and :func:`read_frame` returns always *false*.

        There can be multiple read buffers, because the CAN transceiver cannot receive
        data and remote frames into the same read buffer. A positive read buffer size
        represents a data frame read buffer and a negative read buffer size represents
        a remote frame read buffer. A read buffer size of zero is not allowed. By
        default the first read buffer is configured for data frames and the second read
        buffer is configured for remote frame. There can be up to 32 different read
        buffers, assuming that no write buffer is used. Each read buffer has its own
        filter configuration (see :func:`set_read_filter_configuration`).

        A valid queue configuration fulfills these conditions::

         write_buffer_size + abs(read_buffer_size_0) + abs(read_buffer_size_1) + ... + abs(read_buffer_size_31) <= 32
         write_backlog_size + read_backlog_size <= 768

        The write buffer timeout has three different modes that define how a failed
        frame transmission should be handled:

        * Single-Shot (< 0): Only one transmission attempt will be made. If the
          transmission fails then the frame is discarded.
        * Infinite (= 0): Infinite transmission attempts will be made. The frame will
          never be discarded.
        * Milliseconds (> 0): A limited number of transmission attempts will be made.
          If the frame could not be transmitted successfully after the configured
          number of milliseconds then the frame is discarded.

        The current content of the queues is lost when this function is called.
        """
        write_buffer_size = int(write_buffer_size)
        check_range("write_buffer_size", write_buffer_size, 0, 32)
        write_buffer_timeout = int(write_buffer_timeout)
        check_range("write_buffer_timeout", write_buffer_timeout, -2147483648, 2147483647)
        write_backlog_size = int(write_backlog_size)
        check_range("write_backlog_size", write_backlog_size, 0, 768)
        read_buffer_sizes_length = int(read_buffer_sizes_length)
        check_range("read_buffer_sizes_length", read_buffer_sizes_length, 0, 32)
        check_length("read_buffer_sizes_data", read_buffer_sizes_data, 32)
        read_backlog_size = int(read_backlog_size)
        check_range("read_backlog_size", read_backlog_size, 0, 768)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_QUEUE_CONFIGURATION_LOW_LEVEL,
            data=pack_payload(
                (
                    write_buffer_size,
                    write_buffer_timeout,
                    write_backlog_size,
                    read_buffer_sizes_length,
                    list(map(int, read_buffer_sizes_data)),
                    read_backlog_size,
                ),
                "B i H B 32b H",
            ),
            response_expected=response_expected,
        )

    async def set_queue_configuration(
        self,
        write_buffer_size: int,
        write_buffer_timeout: int,
        write_backlog_size: int,
        read_backlog_size: int,
        read_buffer_sizes: Sequence[int],
    ) -> None:
        """
        Sets the write and read queue configuration.

        The CAN transceiver has 32 buffers in total in hardware for transmitting and
        receiving frames. Additionally, the Bricklet has a backlog for 768 frames in
        total in software. The buffers and the backlog can be freely assigned to the
        write and read queues.

        :func:`write_frame` writes a frame into the write backlog. The Bricklet moves
        the frame from the backlog into a free write buffer. The CAN transceiver then
        transmits the frame from the write buffer to the CAN bus. If there are no
        write buffers (``write_buffer_size`` is zero) or there is no write backlog
        (``write_backlog_size`` is zero) then no frames can be transmitted and
        :func:`write_frame` returns always *false*.

        The CAN transceiver receives a frame from the CAN bus and stores it into a
        free read buffer. The Bricklet moves the frame from the read buffer into the
        read backlog. :func:`read_frame` reads the frame from the read backlog and
        returns it. If there are no read buffers (``read_buffer_sizes`` is empty) or
        there is no read backlog (``read_backlog_size`` is zero) then no frames can be
        received and :func:`read_frame` returns always *false*.

        There can be multiple read buffers, because the CAN transceiver cannot receive
        data and remote frames into the same read buffer. A positive read buffer size
        represents a data frame read buffer and a negative read buffer size represents
        a remote frame read buffer. A read buffer size of zero is not allowed. By
        default the first read buffer is configured for data frames and the second read
        buffer is configured for remote frame. There can be up to 32 different read
        buffers, assuming that no write buffer is used. Each read buffer has its own
        filter configuration (see :func:`set_read_filter_configuration`).

        A valid queue configuration fulfills these conditions::

         write_buffer_size + abs(read_buffer_size_0) + abs(read_buffer_size_1) + ... + abs(read_buffer_size_31) <= 32
         write_backlog_size + read_backlog_size <= 768

        The write buffer timeout has three different modes that define how a failed
        frame transmission should be handled:

        * Single-Shot (< 0): Only one transmission attempt will be made. If the
          transmission fails then the frame is discarded.
        * Infinite (= 0): Infinite transmission attempts will be made. The frame will
          never be discarded.
        * Milliseconds (> 0): A limited number of transmission attempts will be made.
          If the frame could not be transmitted successfully after the configured
          number of milliseconds then the frame is discarded.

        The current content of the queues is lost when this function is called.

        This function transfers the complete read_buffer_sizes stream and calls
        :func:`set_queue_configuration_low_level` as often as necessary. Concurrent transfers of the stream are
        serialized.
        """
        chunk = pad_single_chunk(
            [int(item) for item in read_buffer_sizes], name="read_buffer_sizes", chunk_size=32, padding=0
        )
        length = len(read_buffer_sizes)
        await self.set_queue_configuration_low_level(
            write_buffer_size, write_buffer_timeout, write_backlog_size, length, chunk, read_backlog_size
        )

    async def get_queue_configuration_low_level(self) -> GetQueueConfiguration:
        """
        Returns the queue configuration as set by :func:`set_queue_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_QUEUE_CONFIGURATION_LOW_LEVEL, response_expected=True
        )
        (
            write_buffer_size,
            write_buffer_timeout,
            write_backlog_size,
            read_buffer_sizes_length,
            read_buffer_sizes_data,
            read_backlog_size,
        ) = unpack_payload(payload, "B i H B 32b H")
        return GetQueueConfiguration(
            write_buffer_size,
            write_buffer_timeout,
            write_backlog_size,
            read_buffer_sizes_length,
            tuple(read_buffer_sizes_data),
            read_backlog_size,
        )

    async def get_queue_configuration(self) -> GetQueueConfigurationResult:
        """
        Returns the queue configuration as set by :func:`set_queue_configuration`.

        This function transfers the complete read_buffer_sizes stream and calls
        :func:`get_queue_configuration_low_level` as often as necessary. Concurrent transfers of the stream are
        serialized.
        """
        result = await self.get_queue_configuration_low_level()
        return GetQueueConfigurationResult(
            result.write_buffer_size,
            result.write_buffer_timeout,
            result.write_backlog_size,
            result.read_backlog_size,
            tuple(result.read_buffer_sizes_data[: result.read_buffer_sizes_length]),
        )

    async def set_read_filter_configuration(
        self,
        buffer_index: int,
        filter_mode: FilterMode | int,
        filter_mask: int,
        filter_identifier: int,
        response_expected: bool = True,
    ) -> None:
        """
        Set the read filter configuration for the given read buffer index. This can be
        used to define which frames should be received by the CAN transceiver and put
        into the read buffer.

        The read filter has four different modes that define if and how the filter mask
        and the filter identifier are applied:

        * Accept-All: All frames are received.
        * Match-Standard-Only: Only standard frames with a matching identifier are
          received.
        * Match-Extended-Only: Only extended frames with a matching identifier are
          received.
        * Match-Standard-And-Extended: Standard and extended frames with a matching
          identifier are received.

        The filter mask and filter identifier are used as bit masks. Their usage
        depends on the mode:

        * Accept-All: Mask and identifier are ignored.
        * Match-Standard-Only: Bit 0 to 10 (11 bits) of filter mask and filter
          identifier are used to match the 11-bit identifier of standard frames.
        * Match-Extended-Only: Bit 0 to 28 (29 bits) of filter mask and filter
          identifier are used to match the 29-bit identifier of extended frames.
        * Match-Standard-And-Extended: Bit 18 to 28 (11 bits) of filter mask and filter
          identifier are used to match the 11-bit identifier of standard frames, bit 0
          to 17 (18 bits) are ignored in this case. Bit 0 to 28 (29 bits) of filter
          mask and filter identifier are used to match the 29-bit identifier of extended
          frames.

        The filter mask and filter identifier are applied in this way: The filter mask
        is used to select the frame identifier bits that should be compared to the
        corresponding filter identifier bits. All unselected bits are automatically
        accepted. All selected bits have to match the filter identifier to be accepted.
        If all bits for the selected mode are accepted then the frame is accepted and
        is added to the read buffer.

        .. csv-table::
         :header: "Filter Mask Bit", "Filter Identifier Bit", "Frame Identifier Bit", "Result"
         :widths: 10, 10, 10, 10

         0, X, X, Accept
         1, 0, 0, Accept
         1, 0, 1, Reject
         1, 1, 0, Reject
         1, 1, 1, Accept

        For example, to receive standard frames with identifier 0x123 only, the mode
        can be set to Match-Standard-Only with 0x7FF as mask and 0x123 as identifier.
        The mask of 0x7FF selects all 11 identifier bits for matching so that the
        identifier has to be exactly 0x123 to be accepted.

        To accept identifier 0x123 and identifier 0x456 at the same time, just set
        filter 2 to 0x456 and keep mask and filter 1 unchanged.

        There can be up to 32 different read filters configured at the same time,
        because there can be up to 32 read buffer (see :func:`set_queue_configuration`).

        The default mode is accept-all for all read buffers.
        """
        buffer_index = int(buffer_index)
        check_range("buffer_index", buffer_index, 0, 31)
        filter_mask = int(filter_mask)
        check_range("filter_mask", filter_mask, 0, 1073741823)
        filter_identifier = int(filter_identifier)
        check_range("filter_identifier", filter_identifier, 0, 1073741823)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_READ_FILTER_CONFIGURATION,
            data=pack_payload((buffer_index, FilterMode(filter_mode).value, filter_mask, filter_identifier), "B B I I"),
            response_expected=response_expected,
        )

    async def get_read_filter_configuration(self, buffer_index: int) -> GetReadFilterConfiguration:
        """
        Returns the read filter configuration as set by :func:`set_read_filter_configuration`.
        """
        buffer_index = int(buffer_index)
        check_range("buffer_index", buffer_index, 0, 31)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_READ_FILTER_CONFIGURATION,
            data=pack_payload((buffer_index,), "B"),
            response_expected=True,
        )
        filter_mode, filter_mask, filter_identifier = unpack_payload(payload, "B I I")
        return GetReadFilterConfiguration(FilterMode(filter_mode), filter_mask, filter_identifier)

    async def get_error_log_low_level(  # pylint: disable=too-many-locals
        self,
    ) -> GetErrorLog:
        """
        Returns information about different kinds of errors.

        The write and read error levels indicate the current level of stuffing, form,
        acknowledgement, bit and checksum errors during CAN bus write and read
        operations. For each of this error kinds there is also an individual counter.

        When the write error level extends 255 then the CAN transceiver gets disabled
        and no frames can be transmitted or received anymore. The CAN transceiver will
        automatically be activated again after the CAN bus is idle for a while.

        The write buffer timeout, read buffer and backlog overflow counts represents the
        number of these errors:

        * A write buffer timeout occurs if a frame could not be transmitted before the
          configured write buffer timeout expired (see :func:`set_queue_configuration`).
        * A read buffer overflow occurs if a read buffer of the CAN transceiver
          still contains the last received frame when the next frame arrives. In this
          case the last received frame is lost. This happens if the CAN transceiver
          receives more frames than the Bricklet can handle. Using the read filter
          (see :func:`set_read_filter_configuration`) can help to reduce the amount of
          received frames. This count is not exact, but a lower bound, because the
          Bricklet might not able detect all overflows if they occur in rapid succession.
        * A read backlog overflow occurs if the read backlog of the Bricklet is already
          full when the next frame should be read from a read buffer of the CAN
          transceiver. In this case the frame in the read buffer is lost. This
          happens if the CAN transceiver receives more frames to be added to the read
          backlog than are removed from the read backlog using the :func:`read_frame`
          function. Using the :attr:`CallbackID.FRAME_READ` callback ensures that the read backlog
          can not overflow.

        The read buffer overflow counter counts the overflows of all configured read
        buffers. Which read buffer exactly suffered from an overflow can be figured
        out from the read buffer overflow occurrence list
        (``read_buffer_overflow_error_occurred``). Reading the error log clears the
        occurence list.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_LOG_LOW_LEVEL, response_expected=True
        )
        (
            transceiver_state,
            transceiver_write_error_level,
            transceiver_read_error_level,
            transceiver_stuffing_error_count,
            transceiver_format_error_count,
            transceiver_ack_error_count,
            transceiver_bit1_error_count,
            transceiver_bit0_error_count,
            transceiver_crc_error_count,
            write_buffer_timeout_error_count,
            read_buffer_overflow_error_count,
            read_buffer_overflow_error_occurred_length,
            read_buffer_overflow_error_occurred_data,
            read_backlog_overflow_error_count,
        ) = unpack_payload(payload, "B B B I I I I I I I I B 32! I")
        return GetErrorLog(
            TransceiverState(transceiver_state),
            transceiver_write_error_level,
            transceiver_read_error_level,
            transceiver_stuffing_error_count,
            transceiver_format_error_count,
            transceiver_ack_error_count,
            transceiver_bit1_error_count,
            transceiver_bit0_error_count,
            transceiver_crc_error_count,
            write_buffer_timeout_error_count,
            read_buffer_overflow_error_count,
            read_buffer_overflow_error_occurred_length,
            tuple(read_buffer_overflow_error_occurred_data),
            read_backlog_overflow_error_count,
        )

    async def get_error_log(self) -> GetErrorLogResult:
        """
        Returns information about different kinds of errors.

        The write and read error levels indicate the current level of stuffing, form,
        acknowledgement, bit and checksum errors during CAN bus write and read
        operations. For each of this error kinds there is also an individual counter.

        When the write error level extends 255 then the CAN transceiver gets disabled
        and no frames can be transmitted or received anymore. The CAN transceiver will
        automatically be activated again after the CAN bus is idle for a while.

        The write buffer timeout, read buffer and backlog overflow counts represents the
        number of these errors:

        * A write buffer timeout occurs if a frame could not be transmitted before the
          configured write buffer timeout expired (see :func:`set_queue_configuration`).
        * A read buffer overflow occurs if a read buffer of the CAN transceiver
          still contains the last received frame when the next frame arrives. In this
          case the last received frame is lost. This happens if the CAN transceiver
          receives more frames than the Bricklet can handle. Using the read filter
          (see :func:`set_read_filter_configuration`) can help to reduce the amount of
          received frames. This count is not exact, but a lower bound, because the
          Bricklet might not able detect all overflows if they occur in rapid succession.
        * A read backlog overflow occurs if the read backlog of the Bricklet is already
          full when the next frame should be read from a read buffer of the CAN
          transceiver. In this case the frame in the read buffer is lost. This
          happens if the CAN transceiver receives more frames to be added to the read
          backlog than are removed from the read backlog using the :func:`read_frame`
          function. Using the :attr:`CallbackID.FRAME_READ` callback ensures that the read backlog
          can not overflow.

        The read buffer overflow counter counts the overflows of all configured read
        buffers. Which read buffer exactly suffered from an overflow can be figured
        out from the read buffer overflow occurrence list
        (``read_buffer_overflow_error_occurred``). Reading the error log clears the
        occurence list.

        This function transfers the complete read_buffer_overflow_error_occurred stream and calls
        :func:`get_error_log_low_level` as often as necessary. Concurrent transfers of the stream are serialized.
        """
        result = await self.get_error_log_low_level()
        return GetErrorLogResult(
            result.transceiver_state,
            result.transceiver_write_error_level,
            result.transceiver_read_error_level,
            result.transceiver_stuffing_error_count,
            result.transceiver_format_error_count,
            result.transceiver_ack_error_count,
            result.transceiver_bit1_error_count,
            result.transceiver_bit0_error_count,
            result.transceiver_crc_error_count,
            result.write_buffer_timeout_error_count,
            result.read_buffer_overflow_error_count,
            result.read_backlog_overflow_error_count,
            tuple(result.read_buffer_overflow_error_occurred_data[: result.read_buffer_overflow_error_occurred_length]),
        )

    async def set_communication_led_config(
        self,
        config: CommunicationLEDConfig | int = CommunicationLEDConfig.SHOW_COMMUNICATION,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the communication LED configuration. By default the LED shows
        CAN-Bus traffic, it flickers once for every 40 transmitted or received frames.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COMMUNICATION_LED_CONFIG,
            data=pack_payload((CommunicationLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_communication_led_config(self) -> CommunicationLEDConfig:
        """
        Returns the configuration as set by :func:`set_communication_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COMMUNICATION_LED_CONFIG, response_expected=True
        )
        return CommunicationLEDConfig(unpack_payload(payload, "B"))

    async def set_error_led_config(
        self, config: ErrorLEDConfig | int = ErrorLEDConfig.SHOW_TRANSCEIVER_STATE, response_expected: bool = True
    ) -> None:
        """
        Sets the error LED configuration.

        By default (show-transceiver-state) the error LED turns on if the CAN
        transceiver is passive or disabled state (see :func:`get_error_log`). If
        the CAN transceiver is in active state the LED turns off.

        If the LED is configured as show-error then the error LED turns on if any error
        occurs. If you call this function with the show-error option again, the LED will
        turn off until the next error occurs.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ERROR_LED_CONFIG,
            data=pack_payload((ErrorLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_error_led_config(self) -> ErrorLEDConfig:
        """
        Returns the configuration as set by :func:`set_error_led_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_LED_CONFIG, response_expected=True
        )
        return ErrorLEDConfig(unpack_payload(payload, "B"))

    async def set_frame_readable_callback_configuration(
        self, enabled: bool = False, response_expected: bool = True
    ) -> None:
        """
        Enables and disables the :attr:`CallbackID.FRAME_READABLE` callback.

        By default the callback is disabled. Enabling this callback will disable the :attr:`CallbackID.FRAME_READ`
        callback.

        .. versionadded:: 2.0.3 (Firmware)
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

        .. versionadded:: 2.0.3 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_error_occurred_callback_configuration(
        self, enabled: bool = False, response_expected: bool = True
    ) -> None:
        """
        Enables and disables the :attr:`CallbackID.ERROR_OCCURRED` callback.

        By default the callback is disabled.

        .. versionadded:: 2.0.3 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ERROR_OCCURRED_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_error_occurred_callback_configuration(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.ERROR_OCCURRED` callback is enabled, *false* otherwise.

        .. versionadded:: 2.0.3 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_OCCURRED_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.FRAME_READABLE:
            return 0, None
        return 1, None

    def _to_events(  # pylint: disable=too-many-locals,too-many-return-statements,too-many-branches
        self, callback_id: CallbackID, value: Any, sids: Sequence[int] | None
    ) -> Iterable[Event]:
        if callback_id is CallbackID.FRAME_READ:
            frame_type, identifier, data_length, data_data = value
            data = data_data[:data_length]  # A single chunk
            return (Event(self, 2, callback_id, FrameReadEvent(FrameType(frame_type), identifier, bytes(data))),)
        return super()._to_events(callback_id, value, sids)
