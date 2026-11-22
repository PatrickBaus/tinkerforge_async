"""
Module for the Tinkerforge NFC Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/NFC_Bricklet_Python.html) implemented using
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
from .streams import Chunk, read_stream, write_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    READER_STATE_CHANGED = 13
    CARDEMU_STATE_CHANGED = 18
    P2P_STATE_CHANGED = 24
    SIMPLE_TAG_SEEN = 32


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_MODE = 1
    GET_MODE = 2
    READER_REQUEST_TAG_ID = 3
    READER_GET_TAG_ID_LOW_LEVEL = 4
    READER_GET_STATE = 5
    READER_WRITE_NDEF_LOW_LEVEL = 6
    READER_REQUEST_NDEF = 7
    READER_READ_NDEF_LOW_LEVEL = 8
    READER_AUTHENTICATE_MIFARE_CLASSIC_PAGE = 9
    READER_WRITE_PAGE_LOW_LEVEL = 10
    READER_REQUEST_PAGE = 11
    READER_READ_PAGE_LOW_LEVEL = 12
    CARDEMU_GET_STATE = 14
    CARDEMU_START_DISCOVERY = 15
    CARDEMU_WRITE_NDEF_LOW_LEVEL = 16
    CARDEMU_START_TRANSFER = 17
    P2P_GET_STATE = 19
    P2P_START_DISCOVERY = 20
    P2P_WRITE_NDEF_LOW_LEVEL = 21
    P2P_START_TRANSFER = 22
    P2P_READ_NDEF_LOW_LEVEL = 23
    SET_DETECTION_LED_CONFIG = 25
    GET_DETECTION_LED_CONFIG = 26
    SET_MAXIMUM_TIMEOUT = 27
    GET_MAXIMUM_TIMEOUT = 28
    SIMPLE_GET_TAG_ID_LOW_LEVEL = 29
    CARDEMU_SET_TAG_ID = 30
    CARDEMU_GET_TAG_ID = 31
    SET_SIMPLE_TAG_SEEN_CALLBACK_CONFIGURATION = 33
    GET_SIMPLE_TAG_SEEN_CALLBACK_CONFIGURATION = 34


@unique
class Mode(Enum):
    """
    The mode options
    """

    OFF = 0
    CARDEMU = 1
    P2P = 2
    READER = 3
    SIMPLE = 4


@unique
class TagType(Enum):
    """
    The tag type options
    """

    MIFARE_CLASSIC = 0
    TYPE1 = 1
    TYPE2 = 2
    TYPE3 = 3
    TYPE4 = 4
    TYPE5 = 5
    PHONE = 6


@unique
class ReaderState(Enum):
    """
    The reader state options
    """

    INITIALIZATION = 0
    IDLE = 128
    ERROR = 192
    REQUEST_TAG_ID = 2
    REQUEST_TAG_ID_READY = 130
    REQUEST_TAG_ID_ERROR = 194
    AUTHENTICATE_MIFARE_CLASSIC_PAGE = 3
    AUTHENTICATE_MIFARE_CLASSIC_PAGE_READY = 131
    AUTHENTICATE_MIFARE_CLASSIC_PAGE_ERROR = 195
    WRITE_PAGE = 4
    WRITE_PAGE_READY = 132
    WRITE_PAGE_ERROR = 196
    REQUEST_PAGE = 5
    REQUEST_PAGE_READY = 133
    REQUEST_PAGE_ERROR = 197
    WRITE_NDEF = 6
    WRITE_NDEF_READY = 134
    WRITE_NDEF_ERROR = 198
    REQUEST_NDEF = 7
    REQUEST_NDEF_READY = 135
    REQUEST_NDEF_ERROR = 199


@unique
class Key(Enum):
    """
    The key options
    """

    A = 0
    B = 1


@unique
class ReaderWrite(Enum):
    """
    The reader write options
    """

    TYPE4_CAPABILITY_CONTAINER = 3
    TYPE4_NDEF = 4


@unique
class ReaderRequest(Enum):
    """
    The reader request options
    """

    TYPE4_CAPABILITY_CONTAINER = 3
    TYPE4_NDEF = 4


@unique
class CardemuState(Enum):
    """
    The cardemu state options
    """

    INITIALIZATION = 0
    IDLE = 128
    ERROR = 192
    DISCOVER = 2
    DISCOVER_READY = 130
    DISCOVER_ERROR = 194
    TRANSFER_NDEF = 3
    TRANSFER_NDEF_READY = 131
    TRANSFER_NDEF_ERROR = 195


@unique
class CardemuTransfer(Enum):
    """
    The cardemu transfer options
    """

    ABORT = 0
    WRITE = 1


@unique
class P2PState(Enum):
    """
    The p2p state options
    """

    INITIALIZATION = 0
    IDLE = 128
    ERROR = 192
    DISCOVER = 2
    DISCOVER_READY = 130
    DISCOVER_ERROR = 194
    TRANSFER_NDEF = 3
    TRANSFER_NDEF_READY = 131
    TRANSFER_NDEF_ERROR = 195


@unique
class P2PTransfer(Enum):
    """
    The p2p transfer options
    """

    ABORT = 0
    WRITE = 1
    READ = 2


@unique
class DetectionLEDConfig(Enum):
    """
    The detection led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_DETECTION = 3


class ReaderGetTagID(NamedTuple):
    tag_type: TagType
    tag_id_length: int
    tag_id_data: tuple[int, ...]


class ReaderGetTagId(NamedTuple):
    tag_type: TagType
    tag_id: bytes


class ReaderGetState(NamedTuple):
    state: ReaderState
    idle: bool


class ReaderReadNDEF(NamedTuple):
    ndef_length: int
    ndef_chunk_offset: int
    ndef_chunk_data: tuple[int, ...]


class ReaderReadPage(NamedTuple):
    data_length: int
    data_chunk_offset: int
    data_chunk_data: tuple[int, ...]


class CardemuGetState(NamedTuple):
    state: CardemuState
    idle: bool


class P2PGetState(NamedTuple):
    state: P2PState
    idle: bool


class P2PReadNDEF(NamedTuple):
    ndef_length: int
    ndef_chunk_offset: int
    ndef_chunk_data: tuple[int, ...]


class SimpleGetTagID(NamedTuple):
    tag_type: TagType
    tag_id_length: int
    tag_id_data: tuple[int, ...]
    last_seen: Decimal


class SimpleGetTagId(NamedTuple):
    tag_type: TagType
    last_seen: Decimal
    tag_id: bytes


class CardemuGetTagID(NamedTuple):
    tag_id_length: int
    tag_id_data: tuple[int, ...]


class ReaderStateChangedEvent(NamedTuple):
    state: ReaderState
    idle: bool


class CardemuStateChangedEvent(NamedTuple):
    state: CardemuState
    idle: bool


class P2PStateChangedEvent(NamedTuple):
    state: P2PState
    idle: bool


class SimpleTagSeenEvent(NamedTuple):
    tag_type: TagType
    tag_id: bytes


class BrickletNFC(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    NFC tag read/write, NFC P2P and Card Emulation
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_NFC
    DEVICE_DISPLAY_NAME = "NFC Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Mode: TypeAlias = Mode
    TagType: TypeAlias = TagType
    ReaderState: TypeAlias = ReaderState
    Key: TypeAlias = Key
    ReaderWrite: TypeAlias = ReaderWrite
    ReaderRequest: TypeAlias = ReaderRequest
    CardemuState: TypeAlias = CardemuState
    CardemuTransfer: TypeAlias = CardemuTransfer
    P2PState: TypeAlias = P2PState
    P2PTransfer: TypeAlias = P2PTransfer
    DetectionLEDConfig: TypeAlias = DetectionLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.READER_STATE_CHANGED: "B !",
        CallbackID.CARDEMU_STATE_CHANGED: "B !",
        CallbackID.P2P_STATE_CHANGED: "B !",
        CallbackID.SIMPLE_TAG_SEEN: "B B 10B",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.READER_STATE_CHANGED,)),
        Channel(1, callbacks=(CallbackID.CARDEMU_STATE_CHANGED,)),
        Channel(2, callbacks=(CallbackID.P2P_STATE_CHANGED,)),
        Channel(3, callbacks=(CallbackID.SIMPLE_TAG_SEEN,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 4)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()

    async def set_mode(self, mode: Mode | int = Mode.OFF, response_expected: bool = True) -> None:
        """
        Sets the mode. The NFC Bricklet supports four modes:

        * Off
        * Card Emulation (Cardemu): Emulates a tag for other readers
        * Peer to Peer (P2P): Exchange data with other readers
        * Reader: Reads and writes tags
        * Simple: Automatically reads tag IDs

        If you change a mode, the Bricklet will reconfigure the hardware for this mode.
        Therefore, you can only use functions corresponding to the current mode. For
        example, in Reader mode you can only use Reader functions.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MODE,
            data=pack_payload((Mode(mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_mode(self) -> Mode:
        """
        Returns the mode as set by :func:`set_mode`.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_MODE, response_expected=True)
        return Mode(unpack_payload(payload, "B"))

    async def reader_request_tag_id(self, response_expected: bool = True) -> None:
        """
        After you call :func:`reader_request_tag_id` the NFC Bricklet will try to read
        the tag ID from the tag. After this process is done the state will change.
        You can either register the :attr:`CallbackID.READER_STATE_CHANGED` callback or you can poll
        :func:`reader_get_state` to find out about the state change.

        If the state changes to *ReaderRequestTagIDError* it means that either there was
        no tag present or that the tag has an incompatible type. If the state
        changes to *ReaderRequestTagIDReady* it means that a compatible tag was found
        and that the tag ID has been saved. You can now read out the tag ID by
        calling :func:`reader_get_tag_id`.

        If two tags are in the proximity of the NFC Bricklet, this
        function will cycle through the tags. To select a specific tag you have
        to call :func:`reader_request_tag_id` until the correct tag ID is found.

        In case of any *ReaderError* state the selection is lost and you have to
        start again by calling :func:`reader_request_tag_id`.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.READER_REQUEST_TAG_ID, response_expected=response_expected
        )

    async def reader_get_tag_id_low_level(self) -> ReaderGetTagID:
        """
        Returns the tag type and the tag ID. This function can only be called if the
        NFC Bricklet is currently in one of the *ReaderReady* states. The returned tag ID
        is the tag ID that was saved through the last call of :func:`reader_request_tag_id`.

        To get the tag ID of a tag the approach is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`reader_get_state` or
           :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. Call :func:`reader_get_tag_id`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READER_GET_TAG_ID_LOW_LEVEL, response_expected=True
        )
        tag_type, tag_id_length, tag_id_data = unpack_payload(payload, "B B 32B")
        return ReaderGetTagID(TagType(tag_type), tag_id_length, tuple(tag_id_data))

    async def reader_get_tag_id(self) -> ReaderGetTagId:
        """
        Returns the tag type and the tag ID. This function can only be called if the
        NFC Bricklet is currently in one of the *ReaderReady* states. The returned tag ID
        is the tag ID that was saved through the last call of :func:`reader_request_tag_id`.

        To get the tag ID of a tag the approach is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`reader_get_state` or
           :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. Call :func:`reader_get_tag_id`

        This function transfers the complete tag_id stream and calls :func:`reader_get_tag_id_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """
        result = await self.reader_get_tag_id_low_level()
        return ReaderGetTagId(result.tag_type, bytes(result.tag_id_data[: result.tag_id_length]))

    async def reader_get_state(self) -> ReaderGetState:
        """
        Returns the current reader state of the NFC Bricklet.

        On startup the Bricklet will be in the *ReaderInitialization* state. The
        initialization will only take about 20ms. After that it changes to *ReaderIdle*.

        The Bricklet is also reinitialized if the mode is changed, see :func:`set_mode`.

        The functions of this Bricklet can be called in the *ReaderIdle* state and all of
        the *ReaderReady* and *ReaderError* states.

        Example: If you call :func:`reader_request_page`, the state will change to
        *ReaderRequestPage* until the reading of the page is finished. Then it will change
        to either *ReaderRequestPageReady* if it worked or to *ReaderRequestPageError* if it
        didn't. If the request worked you can get the page by calling :func:`reader_read_page`.

        The same approach is used analogously for the other API functions.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READER_GET_STATE, response_expected=True
        )
        state, idle = unpack_payload(payload, "B !")
        return ReaderGetState(ReaderState(state), idle)

    async def reader_write_ndef_low_level(
        self,
        ndef_length: int,
        ndef_chunk_offset: int,
        ndef_chunk_data: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Writes NDEF formated data.

        This function currently supports NFC Forum Type 2, 4, 5 and Mifare Classic.

        The general approach for writing a NDEF message is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *ReaderRequestTagIDReady* (see
           :func:`reader_get_state` or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`reader_get_tag_id` and check
           if the expected tag was found, if it was not found got back to step 1
        4. Call :func:`reader_write_ndef` with the NDEF message that you want to write
        5. Wait for state to change to *ReaderWriteNDEFReady* (see :func:`reader_get_state`
           or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        """
        ndef_length = int(ndef_length)
        check_range("ndef_length", ndef_length, 0, 8192)
        ndef_chunk_offset = int(ndef_chunk_offset)
        check_range("ndef_chunk_offset", ndef_chunk_offset, 0, 65535)
        check_length("ndef_chunk_data", ndef_chunk_data, 60)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READER_WRITE_NDEF_LOW_LEVEL,
            data=pack_payload((ndef_length, ndef_chunk_offset, list(map(int, ndef_chunk_data))), "H H 60B"),
            response_expected=response_expected,
        )

    async def reader_write_ndef(self, ndef: bytes | Sequence[int]) -> None:
        """
        Writes NDEF formated data.

        This function currently supports NFC Forum Type 2, 4, 5 and Mifare Classic.

        The general approach for writing a NDEF message is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *ReaderRequestTagIDReady* (see
           :func:`reader_get_state` or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`reader_get_tag_id` and check
           if the expected tag was found, if it was not found got back to step 1
        4. Call :func:`reader_write_ndef` with the NDEF message that you want to write
        5. Wait for state to change to *ReaderWriteNDEFReady* (see :func:`reader_get_state`
           or :attr:`CallbackID.READER_STATE_CHANGED` callback)

        This function transfers the complete ndef stream and calls :func:`reader_write_ndef_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.reader_write_ndef_low_level(length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk, [int(item) for item in ndef], name="ndef", chunk_size=60, padding=0, max_length=65535
            )

    async def reader_request_ndef(self, response_expected: bool = True) -> None:
        """
        Reads NDEF formated data from a tag.

        This function currently supports NFC Forum Type 1, 2, 3, 4, 5 and Mifare Classic.

        The general approach for reading a NDEF message is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *RequestTagIDReady* (see :func:`reader_get_state`
           or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`reader_get_tag_id` and check if the
           expected tag was found, if it was not found got back to step 1
        4. Call :func:`reader_request_ndef`
        5. Wait for state to change to *ReaderRequestNDEFReady* (see :func:`reader_get_state`
           or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        6. Call :func:`reader_read_ndef` to retrieve the NDEF message from the buffer
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.READER_REQUEST_NDEF, response_expected=response_expected
        )

    async def reader_read_ndef_low_level(self) -> ReaderReadNDEF:
        """
        Returns the NDEF data from an internal buffer. To fill the buffer
        with a NDEF message you have to call :func:`reader_request_ndef` beforehand.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READER_READ_NDEF_LOW_LEVEL, response_expected=True
        )
        ndef_length, ndef_chunk_offset, ndef_chunk_data = unpack_payload(payload, "H H 60B")
        return ReaderReadNDEF(ndef_length, ndef_chunk_offset, tuple(ndef_chunk_data))

    async def reader_read_ndef(self) -> bytes:
        """
        Returns the NDEF data from an internal buffer. To fill the buffer
        with a NDEF message you have to call :func:`reader_request_ndef` beforehand.

        This function transfers the complete ndef stream and calls :func:`reader_read_ndef_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.reader_read_ndef_low_level()
            return Chunk(result.ndef_length, result.ndef_chunk_offset, result.ndef_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="ndef", chunk_size=60)
        return bytes(data)

    async def reader_authenticate_mifare_classic_page(
        self, page: int, key_number: Key | int, key: bytes | Sequence[int], response_expected: bool = True
    ) -> None:
        """
        Mifare Classic tags use authentication. If you want to read from or write to
        a Mifare Classic page you have to authenticate it beforehand.
        Each page can be authenticated with two keys: A (``key_number`` = 0) and B
        (``key_number`` = 1). A new Mifare Classic
        tag that has not yet been written to can be accessed with key A
        and the default key ``[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]``.

        The approach to read or write a Mifare Classic page is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`reader_get_state`
           or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`reader_get_tag_id` and check if the
           expected tag was found, if it was not found got back to step 1
        4. Call :func:`reader_authenticate_mifare_classic_page` with page and key for the page
        5. Wait for state to change to *ReaderAuthenticatingMifareClassicPageReady* (see
           :func:`reader_get_state` or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        6. Call :func:`reader_request_page` or :func:`reader_write_page` to read/write page

        The authentication will always work for one whole sector (4 pages).
        """
        page = int(page)
        check_range("page", page, 0, 65535)
        check_length("key", key, 6)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READER_AUTHENTICATE_MIFARE_CLASSIC_PAGE,
            data=pack_payload((page, Key(key_number).value, list(map(int, key))), "H B 6B"),
            response_expected=response_expected,
        )

    async def reader_write_page_low_level(
        self,
        page: ReaderWrite | int,
        data_length: int,
        data_chunk_offset: int,
        data_chunk_data: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Writes a maximum of 8192 bytes starting from the given page. How many pages are written
        depends on the tag type. The page sizes are as follows:

        * Mifare Classic page size: 16 byte
        * NFC Forum Type 1 page size: 8 byte
        * NFC Forum Type 2 page size: 4 byte
        * NFC Forum Type 3 page size: 16 byte
        * NFC Forum Type 4: No pages, page = file selection (CC or NDEF, see below)
        * NFC Forum Type 5 page size: 4 byte

        The general approach for writing to a tag is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`reader_get_state` or
           :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`reader_get_tag_id` and check if the
           expected tag was found, if it was not found got back to step 1
        4. Call :func:`reader_write_page` with page number and data
        5. Wait for state to change to *ReaderWritePageReady* (see :func:`reader_get_state` or
           :attr:`CallbackID.READER_STATE_CHANGED` callback)

        If you use a Mifare Classic tag you have to authenticate a page before you
        can write to it. See :func:`reader_authenticate_mifare_classic_page`.

        NFC Forum Type 4 tags are not organized into pages but different files. We currently
        support two files: Capability Container file (CC) and NDEF file.

        Choose CC by setting page to 3 or NDEF by setting page to 4.
        """
        data_length = int(data_length)
        check_range("data_length", data_length, 0, 8192)
        data_chunk_offset = int(data_chunk_offset)
        check_range("data_chunk_offset", data_chunk_offset, 0, 65535)
        check_length("data_chunk_data", data_chunk_data, 58)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READER_WRITE_PAGE_LOW_LEVEL,
            data=pack_payload(
                (ReaderWrite(page).value, data_length, data_chunk_offset, list(map(int, data_chunk_data))), "H H H 58B"
            ),
            response_expected=response_expected,
        )

    async def reader_write_page(self, page: ReaderWrite | int, data: bytes | Sequence[int]) -> None:
        """
        Writes a maximum of 8192 bytes starting from the given page. How many pages are written
        depends on the tag type. The page sizes are as follows:

        * Mifare Classic page size: 16 byte
        * NFC Forum Type 1 page size: 8 byte
        * NFC Forum Type 2 page size: 4 byte
        * NFC Forum Type 3 page size: 16 byte
        * NFC Forum Type 4: No pages, page = file selection (CC or NDEF, see below)
        * NFC Forum Type 5 page size: 4 byte

        The general approach for writing to a tag is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *ReaderRequestTagIDReady* (see :func:`reader_get_state` or
           :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`reader_get_tag_id` and check if the
           expected tag was found, if it was not found got back to step 1
        4. Call :func:`reader_write_page` with page number and data
        5. Wait for state to change to *ReaderWritePageReady* (see :func:`reader_get_state` or
           :attr:`CallbackID.READER_STATE_CHANGED` callback)

        If you use a Mifare Classic tag you have to authenticate a page before you
        can write to it. See :func:`reader_authenticate_mifare_classic_page`.

        NFC Forum Type 4 tags are not organized into pages but different files. We currently
        support two files: Capability Container file (CC) and NDEF file.

        Choose CC by setting page to 3 or NDEF by setting page to 4.

        This function transfers the complete data stream and calls :func:`reader_write_page_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.reader_write_page_low_level(page, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk, [int(item) for item in data], name="data", chunk_size=58, padding=0, max_length=65535
            )

    async def reader_request_page(self, page: ReaderRequest | int, length: int, response_expected: bool = True) -> None:
        """
        Reads a maximum of 8192 bytes starting from the given page and stores them into a buffer.
        The buffer can then be read out with :func:`reader_read_page`.
        How many pages are read depends on the tag type. The page sizes are
        as follows:

        * Mifare Classic page size: 16 byte
        * NFC Forum Type 1 page size: 8 byte
        * NFC Forum Type 2 page size: 4 byte
        * NFC Forum Type 3 page size: 16 byte
        * NFC Forum Type 4: No pages, page = file selection (CC or NDEF, see below)
        * NFC Forum Type 5 page size: 4 byte

        The general approach for reading a tag is as follows:

        1. Call :func:`reader_request_tag_id`
        2. Wait for state to change to *RequestTagIDReady* (see :func:`reader_get_state`
           or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`reader_get_tag_id` and check if the
           expected tag was found, if it was not found got back to step 1
        4. Call :func:`reader_request_page` with page number
        5. Wait for state to change to *ReaderRequestPageReady* (see :func:`reader_get_state`
           or :attr:`CallbackID.READER_STATE_CHANGED` callback)
        6. Call :func:`reader_read_page` to retrieve the page from the buffer

        If you use a Mifare Classic tag you have to authenticate a page before you
        can read it. See :func:`reader_authenticate_mifare_classic_page`.

        NFC Forum Type 4 tags are not organized into pages but different files. We currently
        support two files: Capability Container file (CC) and NDEF file.

        Choose CC by setting page to 3 or NDEF by setting page to 4.
        """
        length = int(length)
        check_range("length", length, 0, 8192)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READER_REQUEST_PAGE,
            data=pack_payload((ReaderRequest(page).value, length), "H H"),
            response_expected=response_expected,
        )

    async def reader_read_page_low_level(self) -> ReaderReadPage:
        """
        Returns the page data from an internal buffer. To fill the buffer
        with specific pages you have to call :func:`reader_request_page` beforehand.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READER_READ_PAGE_LOW_LEVEL, response_expected=True
        )
        data_length, data_chunk_offset, data_chunk_data = unpack_payload(payload, "H H 60B")
        return ReaderReadPage(data_length, data_chunk_offset, tuple(data_chunk_data))

    async def reader_read_page(self) -> bytes:
        """
        Returns the page data from an internal buffer. To fill the buffer
        with specific pages you have to call :func:`reader_request_page` beforehand.

        This function transfers the complete data stream and calls :func:`reader_read_page_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.reader_read_page_low_level()
            return Chunk(result.data_length, result.data_chunk_offset, result.data_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="data", chunk_size=60)
        return bytes(data)

    async def cardemu_get_state(self) -> CardemuGetState:
        """
        Returns the current cardemu state of the NFC Bricklet.

        On startup the Bricklet will be in the *CardemuInitialization* state. The
        initialization will only take about 20ms. After that it changes to *CardemuIdle*.

        The Bricklet is also reinitialized if the mode is changed, see :func:`set_mode`.

        The functions of this Bricklet can be called in the *CardemuIdle* state and all of
        the *CardemuReady* and *CardemuError* states.

        Example: If you call :func:`cardemu_start_discovery`, the state will change to
        *CardemuDiscover* until the discovery is finished. Then it will change
        to either *CardemuDiscoverReady* if it worked or to *CardemuDiscoverError* if it
        didn't.

        The same approach is used analogously for the other API functions.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.CARDEMU_GET_STATE, response_expected=True
        )
        state, idle = unpack_payload(payload, "B !")
        return CardemuGetState(CardemuState(state), idle)

    async def cardemu_start_discovery(self, response_expected: bool = True) -> None:
        """
        Starts the discovery process. If you call this function while a NFC
        reader device is near to the NFC Bricklet the state will change from
        *CardemuDiscovery* to *CardemuDiscoveryReady*.

        If no NFC reader device can be found or if there is an error during
        discovery the cardemu state will change to *CardemuDiscoveryError*. In this case you
        have to restart the discovery process.

        If the cardemu state changes to *CardemuDiscoveryReady* you can start the NDEF message
        transfer with :func:`cardemu_write_ndef` and :func:`cardemu_start_transfer`.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.CARDEMU_START_DISCOVERY, response_expected=response_expected
        )

    async def cardemu_write_ndef_low_level(
        self,
        ndef_length: int,
        ndef_chunk_offset: int,
        ndef_chunk_data: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Writes the NDEF message that is to be transferred to the NFC peer.

        The maximum supported NDEF message size in Cardemu mode is 255 byte.

        You can call this function at any time in Cardemu mode. The internal buffer
        will not be overwritten until you call this function again or change the
        mode.
        """
        ndef_length = int(ndef_length)
        check_range("ndef_length", ndef_length, 0, 255)
        ndef_chunk_offset = int(ndef_chunk_offset)
        check_range("ndef_chunk_offset", ndef_chunk_offset, 0, 65535)
        check_length("ndef_chunk_data", ndef_chunk_data, 60)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.CARDEMU_WRITE_NDEF_LOW_LEVEL,
            data=pack_payload((ndef_length, ndef_chunk_offset, list(map(int, ndef_chunk_data))), "H H 60B"),
            response_expected=response_expected,
        )

    async def cardemu_write_ndef(self, ndef: bytes | Sequence[int]) -> None:
        """
        Writes the NDEF message that is to be transferred to the NFC peer.

        The maximum supported NDEF message size in Cardemu mode is 255 byte.

        You can call this function at any time in Cardemu mode. The internal buffer
        will not be overwritten until you call this function again or change the
        mode.

        This function transfers the complete ndef stream and calls :func:`cardemu_write_ndef_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.cardemu_write_ndef_low_level(length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk, [int(item) for item in ndef], name="ndef", chunk_size=60, padding=0, max_length=65535
            )

    async def cardemu_start_transfer(self, transfer: CardemuTransfer | int, response_expected: bool = True) -> None:
        """
        You can start the transfer of a NDEF message if the cardemu state is *CardemuDiscoveryReady*.

        Before you call this function to start a write transfer, the NDEF message that
        is to be transferred has to be written via :func:`cardemu_write_ndef` first.

        After you call this function the state will change to *CardemuTransferNDEF*. It will
        change to *CardemuTransferNDEFReady* if the transfer was successful or
        *CardemuTransferNDEFError* if it wasn't.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.CARDEMU_START_TRANSFER,
            data=pack_payload((CardemuTransfer(transfer).value,), "B"),
            response_expected=response_expected,
        )

    async def p2p_get_state(self) -> P2PGetState:
        """
        Returns the current P2P state of the NFC Bricklet.

        On startup the Bricklet will be in the *P2PInitialization* state. The
        initialization will only take about 20ms. After that it changes to *P2PIdle*.

        The Bricklet is also reinitialized if the mode is changed, see :func:`set_mode`.

        The functions of this Bricklet can be called in the *P2PIdle* state and all of
        the *P2PReady* and *P2PError* states.

        Example: If you call :func:`p2p_start_discovery`, the state will change to
        *P2PDiscover* until the discovery is finished. Then it will change
        to either P2PDiscoverReady* if it worked or to *P2PDiscoverError* if it
        didn't.

        The same approach is used analogously for the other API functions.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.P2P_GET_STATE, response_expected=True
        )
        state, idle = unpack_payload(payload, "B !")
        return P2PGetState(P2PState(state), idle)

    async def p2p_start_discovery(self, response_expected: bool = True) -> None:
        """
        Starts the discovery process. If you call this function while another NFC
        P2P enabled device is near to the NFC Bricklet the state will change from
        *P2PDiscovery* to *P2PDiscoveryReady*.

        If no NFC P2P enabled device can be found or if there is an error during
        discovery the P2P state will change to *P2PDiscoveryError*. In this case you
        have to restart the discovery process.

        If the P2P state changes to *P2PDiscoveryReady* you can start the NDEF message
        transfer with :func:`p2p_start_transfer`.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.P2P_START_DISCOVERY, response_expected=response_expected
        )

    async def p2p_write_ndef_low_level(
        self,
        ndef_length: int,
        ndef_chunk_offset: int,
        ndef_chunk_data: bytes | Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        Writes the NDEF message that is to be transferred to the NFC peer.

        The maximum supported NDEF message size for P2P transfer is 255 byte.

        You can call this function at any time in P2P mode. The internal buffer
        will not be overwritten until you call this function again, change the
        mode or use P2P to read an NDEF messages.
        """
        ndef_length = int(ndef_length)
        check_range("ndef_length", ndef_length, 0, 255)
        ndef_chunk_offset = int(ndef_chunk_offset)
        check_range("ndef_chunk_offset", ndef_chunk_offset, 0, 65535)
        check_length("ndef_chunk_data", ndef_chunk_data, 60)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.P2P_WRITE_NDEF_LOW_LEVEL,
            data=pack_payload((ndef_length, ndef_chunk_offset, list(map(int, ndef_chunk_data))), "H H 60B"),
            response_expected=response_expected,
        )

    async def p2p_write_ndef(self, ndef: bytes | Sequence[int]) -> None:
        """
        Writes the NDEF message that is to be transferred to the NFC peer.

        The maximum supported NDEF message size for P2P transfer is 255 byte.

        You can call this function at any time in P2P mode. The internal buffer
        will not be overwritten until you call this function again, change the
        mode or use P2P to read an NDEF messages.

        This function transfers the complete ndef stream and calls :func:`p2p_write_ndef_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.p2p_write_ndef_low_level(length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk, [int(item) for item in ndef], name="ndef", chunk_size=60, padding=0, max_length=65535
            )

    async def p2p_start_transfer(self, transfer: P2PTransfer | int, response_expected: bool = True) -> None:
        """
        You can start the transfer of a NDEF message if the P2P state is *P2PDiscoveryReady*.

        Before you call this function to start a write transfer, the NDEF message that
        is to be transferred has to be written via :func:`p2p_write_ndef` first.

        After you call this function the P2P state will change to *P2PTransferNDEF*. It will
        change to *P2PTransferNDEFReady* if the transfer was successfull or
        *P2PTransferNDEFError* if it wasn't.

        If you started a write transfer you are now done. If you started a read transfer
        you can now use :func:`p2p_read_ndef` to read the NDEF message that was written
        by the NFC peer.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.P2P_START_TRANSFER,
            data=pack_payload((P2PTransfer(transfer).value,), "B"),
            response_expected=response_expected,
        )

    async def p2p_read_ndef_low_level(self) -> P2PReadNDEF:
        """
        Returns the NDEF message that was written by a NFC peer in NFC P2P mode.

        The NDEF message is ready if you called :func:`p2p_start_transfer` with a
        read transfer and the P2P state changed to *P2PTransferNDEFReady*.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.P2P_READ_NDEF_LOW_LEVEL, response_expected=True
        )
        ndef_length, ndef_chunk_offset, ndef_chunk_data = unpack_payload(payload, "H H 60B")
        return P2PReadNDEF(ndef_length, ndef_chunk_offset, tuple(ndef_chunk_data))

    async def p2p_read_ndef(self) -> bytes:
        """
        Returns the NDEF message that was written by a NFC peer in NFC P2P mode.

        The NDEF message is ready if you called :func:`p2p_start_transfer` with a
        read transfer and the P2P state changed to *P2PTransferNDEFReady*.

        This function transfers the complete ndef stream and calls :func:`p2p_read_ndef_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.p2p_read_ndef_low_level()
            return Chunk(result.ndef_length, result.ndef_chunk_offset, result.ndef_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="ndef", chunk_size=60)
        return bytes(data)

    async def set_detection_led_config(
        self, config: DetectionLEDConfig | int = DetectionLEDConfig.SHOW_DETECTION, response_expected: bool = True
    ) -> None:
        """
        Sets the detection LED configuration. By default the LED shows
        if a card/reader is detected.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DETECTION_LED_CONFIG,
            data=pack_payload((DetectionLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_detection_led_config(self) -> DetectionLEDConfig:
        """
        Returns the configuration as set by :func:`set_detection_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DETECTION_LED_CONFIG, response_expected=True
        )
        return DetectionLEDConfig(unpack_payload(payload, "B"))

    async def set_maximum_timeout(self, timeout: Duration = 2, response_expected: bool = True) -> None:
        """
        Sets the maximum timeout.

        This is a global maximum used for all internal state timeouts. The timeouts depend heavily
        on the used tags etc. For example: If you use a Type 2 tag and you want to detect if
        it is present, you have to use :func:`reader_request_tag_id` and wait for the state
        to change to either the error state or the ready state.

        With the default configuration this takes 2-3 seconds. By setting the maximum timeout to
        100ms you can reduce this time to ~150-200ms. For Type 2 this would also still work
        with a 20ms timeout (a Type 2 tag answers usually within 10ms). A type 4 tag can take
        up to 500ms in our tests.

        If you need a fast response time to discover if a tag is present or not you can find
        a good timeout value by trial and error for your specific tag.

        By default we use a very conservative timeout, to be sure that any tag can always
        answer in time.

        Units: timeout in s.

        .. versionadded:: 2.0.1 (Firmware)
        """
        timeout_raw = seconds_to_ms(timeout)
        check_range("timeout", timeout_raw, 0, 65535, timeout)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MAXIMUM_TIMEOUT,
            data=pack_payload((timeout_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_maximum_timeout(self) -> Decimal:
        """
        Returns the timeout as set by :func:`set_maximum_timeout`

        Units: timeout in s.

        .. versionadded:: 2.0.1 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAXIMUM_TIMEOUT, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "H"))

    async def simple_get_tag_id_low_level(self, index: int) -> SimpleGetTagID:
        """
        Returns the tag type and tag ID from simple mode sorted by last seen time for a given index.

        Up to eight tags are saved.

        Units: last_seen in s.

        .. versionadded:: 2.0.6 (Firmware)
        """
        index = int(index)
        check_range("index", index, 0, 7)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SIMPLE_GET_TAG_ID_LOW_LEVEL,
            data=pack_payload((index,), "B"),
            response_expected=True,
        )
        tag_type, tag_id_length, tag_id_data, last_seen = unpack_payload(payload, "B B 10B I")
        return SimpleGetTagID(TagType(tag_type), tag_id_length, tuple(tag_id_data), ms_to_seconds(last_seen))

    async def simple_get_tag_id(self, index: int) -> SimpleGetTagId:
        """
        Returns the tag type and tag ID from simple mode sorted by last seen time for a given index.

        Up to eight tags are saved.

        Units: last_seen in s.

        This function transfers the complete tag_id stream and calls :func:`simple_get_tag_id_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.

        .. versionadded:: 2.0.6 (Firmware)
        """
        result = await self.simple_get_tag_id_low_level(index)
        return SimpleGetTagId(result.tag_type, result.last_seen, bytes(result.tag_id_data[: result.tag_id_length]))

    async def cardemu_set_tag_id(
        self, tag_id_length: int, tag_id_data: bytes | Sequence[int], response_expected: bool = True
    ) -> None:
        """
        Sets the tag ID for cardemu mode. The tag ID can either have a length of 4 or 7.

        Set a length of 0 for random tag ID (default)

        .. versionadded:: 2.1.0 (Firmware)
        """
        tag_id_length = int(tag_id_length)
        check_range("tag_id_length", tag_id_length, 0, 7)
        check_length("tag_id_data", tag_id_data, 7)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.CARDEMU_SET_TAG_ID,
            data=pack_payload((tag_id_length, list(map(int, tag_id_data))), "B 7B"),
            response_expected=response_expected,
        )

    async def cardemu_get_tag_id(self) -> CardemuGetTagID:
        """
        Returns the tag ID and length as set by :func:`cardemu_set_tag_id`.

        .. versionadded:: 2.1.0 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.CARDEMU_GET_TAG_ID, response_expected=True
        )
        tag_id_length, tag_id_data = unpack_payload(payload, "B 7B")
        return CardemuGetTagID(tag_id_length, tuple(tag_id_data))

    async def set_simple_tag_seen_callback_configuration(
        self, period: Duration = 0, response_expected: bool = True
    ) -> None:
        """
        If you enable this callback by setting a positive period, the
        :attr:`CallbackID.SIMPLE_TAG_SEEN` callback is triggered every time a new tag is seen in
        simple mode. If a tag is constantly seen, the callback will trigger again
        periodically, depending on the period setting. A period of 0 will disable the
        callback.

        .. versionadded:: 2.1.4 (Firmware)
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SIMPLE_TAG_SEEN_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_simple_tag_seen_callback_configuration(self) -> Decimal:
        """
        Returns the configuration as set by :func:`set_simple_tag_seen_callback_configuration`.

        .. versionadded:: 2.1.4 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SIMPLE_TAG_SEEN_CALLBACK_CONFIGURATION, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.READER_STATE_CHANGED:
            state, idle = value
            return 0, ReaderStateChangedEvent(ReaderState(state), idle)
        if callback_id is CallbackID.CARDEMU_STATE_CHANGED:
            state, idle = value
            return 1, CardemuStateChangedEvent(CardemuState(state), idle)
        state, idle = value
        return 2, P2PStateChangedEvent(P2PState(state), idle)

    def _to_events(  # pylint: disable=too-many-locals,too-many-return-statements,too-many-branches
        self, callback_id: CallbackID, value: Any, sids: Sequence[int] | None
    ) -> Iterable[Event]:
        if callback_id is CallbackID.SIMPLE_TAG_SEEN:
            tag_type, tag_id_length, tag_id_data = value
            data = tag_id_data[:tag_id_length]  # A single chunk
            return (Event(self, 3, callback_id, SimpleTagSeenEvent(TagType(tag_type), bytes(data))),)
        return super()._to_events(callback_id, value, sids)
