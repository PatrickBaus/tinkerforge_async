"""
Module for the Tinkerforge NFC/RFID Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/NFCRFID_Bricklet_Python.html) implemented using
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

    STATE_CHANGED = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    REQUEST_TAG_ID = 1
    GET_TAG_ID = 2
    GET_STATE = 3
    AUTHENTICATE_MIFARE_CLASSIC_PAGE = 4
    WRITE_PAGE = 5
    REQUEST_PAGE = 6
    GET_PAGE = 7


@unique
class TagType(Enum):
    """
    The tag type options
    """

    MIFARE_CLASSIC = 0
    TYPE1 = 1
    TYPE2 = 2


@unique
class State(Enum):
    """
    The state options
    """

    INITIALIZATION = 0
    IDLE = 128
    ERROR = 192
    REQUEST_TAG_ID = 2
    REQUEST_TAG_ID_READY = 130
    REQUEST_TAG_ID_ERROR = 194
    AUTHENTICATING_MIFARE_CLASSIC_PAGE = 3
    AUTHENTICATING_MIFARE_CLASSIC_PAGE_READY = 131
    AUTHENTICATING_MIFARE_CLASSIC_PAGE_ERROR = 195
    WRITE_PAGE = 4
    WRITE_PAGE_READY = 132
    WRITE_PAGE_ERROR = 196
    REQUEST_PAGE = 5
    REQUEST_PAGE_READY = 133
    REQUEST_PAGE_ERROR = 197


@unique
class Key(Enum):
    """
    The key options
    """

    A = 0
    B = 1


class GetTagID(NamedTuple):
    tag_type: TagType
    tid_length: int
    tid: tuple[int, ...]


class GetState(NamedTuple):
    state: State
    idle: bool


class StateChangedEvent(NamedTuple):
    state: State
    idle: bool


class BrickletNFCRFID(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Reads and writes NFC and RFID tags
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_NFC_RFID
    DEVICE_DISPLAY_NAME = "NFC/RFID Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    TagType: TypeAlias = TagType
    State: TypeAlias = State
    Key: TypeAlias = Key

    CALLBACK_FORMATS = {
        CallbackID.STATE_CHANGED: "B !",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.STATE_CHANGED,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def request_tag_id(self, tag_type: TagType | int, response_expected: bool = True) -> None:
        """
        To read or write a tag that is in proximity of the NFC/RFID Bricklet you
        first have to call this function with the expected tag type as parameter.
        It is no problem if you don't know the tag type. You can cycle through
        the available tag types until the tag gives an answer to the request.

        Currently the following tag types are supported:

        * Mifare Classic
        * NFC Forum Type 1
        * NFC Forum Type 2

        After you call :func:`request_tag_id` the NFC/RFID Bricklet will try to read
        the tag ID from the tag. After this process is done the state will change.
        You can either register the :attr:`CallbackID.STATE_CHANGED` callback or you can poll
        :func:`get_state` to find out about the state change.

        If the state changes to *RequestTagIDError* it means that either there was
        no tag present or that the tag is of an incompatible type. If the state
        changes to *RequestTagIDReady* it means that a compatible tag was found
        and that the tag ID could be read out. You can now get the tag ID by
        calling :func:`get_tag_id`.

        If two tags are in the proximity of the NFC/RFID Bricklet, this
        function will cycle through the tags. To select a specific tag you have
        to call :func:`request_tag_id` until the correct tag id is found.

        In case of any *Error* state the selection is lost and you have to
        start again by calling :func:`request_tag_id`.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REQUEST_TAG_ID,
            data=pack_payload((TagType(tag_type).value,), "B"),
            response_expected=response_expected,
        )

    async def get_tag_id(self) -> GetTagID:
        """
        Returns the tag type, tag ID and the length of the tag ID
        (4 or 7 bytes are possible length). This function can only be called if the
        NFC/RFID is currently in one of the *Ready* states. The returned ID
        is the ID that was saved through the last call of :func:`request_tag_id`.

        To get the tag ID of a tag the approach is as follows:

        1. Call :func:`request_tag_id`
        2. Wait for state to change to *RequestTagIDReady* (see :func:`get_state` or
           :attr:`CallbackID.STATE_CHANGED` callback)
        3. Call :func:`get_tag_id`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TAG_ID, response_expected=True
        )
        tag_type, tid_length, tid = unpack_payload(payload, "B B 7B")
        return GetTagID(TagType(tag_type), tid_length, tuple(tid))

    async def get_state(self) -> GetState:
        """
        Returns the current state of the NFC/RFID Bricklet.

        On startup the Bricklet will be in the *Initialization* state. The
        initialization will only take about 20ms. After that it changes to *Idle*.

        The functions of this Bricklet can be called in the *Idle* state and all of
        the *Ready* and *Error* states.

        Example: If you call :func:`request_page`, the state will change to
        *RequestPage* until the reading of the page is finished. Then it will change
        to either *RequestPageReady* if it worked or to *RequestPageError* if it
        didn't. If the request worked you can get the page by calling :func:`get_page`.

        The same approach is used analogously for the other API functions.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATE, response_expected=True
        )
        state, idle = unpack_payload(payload, "B !")
        return GetState(State(state), idle)

    async def authenticate_mifare_classic_page(
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

        1. Call :func:`request_tag_id`
        2. Wait for state to change to *RequestTagIDReady* (see :func:`get_state`
           or :attr:`CallbackID.STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`get_tag_id` and check if the
           expected tag was found, if it was not found go back to step 1
        4. Call :func:`authenticate_mifare_classic_page` with page and key for the page
        5. Wait for state to change to *AuthenticatingMifareClassicPageReady* (see
           :func:`get_state` or :attr:`CallbackID.STATE_CHANGED` callback)
        6. Call :func:`request_page` or :func:`write_page` to read/write page
        """
        page = int(page)
        check_range("page", page, 0, 65535)
        check_length("key", key, 6)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.AUTHENTICATE_MIFARE_CLASSIC_PAGE,
            data=pack_payload((page, Key(key_number).value, list(map(int, key))), "H B 6B"),
            response_expected=response_expected,
        )

    async def write_page(self, page: int, data: bytes | Sequence[int], response_expected: bool = True) -> None:
        """
        Writes 16 bytes starting from the given page. How many pages are written
        depends on the tag type. The page sizes are as follows:

        * Mifare Classic page size: 16 byte (one page is written)
        * NFC Forum Type 1 page size: 8 byte (two pages are written)
        * NFC Forum Type 2 page size: 4 byte (four pages are written)

        The general approach for writing to a tag is as follows:

        1. Call :func:`request_tag_id`
        2. Wait for state to change to *RequestTagIDReady* (see :func:`get_state` or
           :attr:`CallbackID.STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`get_tag_id` and check if the
           expected tag was found, if it was not found got back to step 1
        4. Call :func:`write_page` with page number and data
        5. Wait for state to change to *WritePageReady* (see :func:`get_state` or
           :attr:`CallbackID.STATE_CHANGED` callback)

        If you use a Mifare Classic tag you have to authenticate a page before you
        can write to it. See :func:`authenticate_mifare_classic_page`.
        """
        page = int(page)
        check_range("page", page, 0, 65535)
        check_length("data", data, 16)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_PAGE,
            data=pack_payload((page, list(map(int, data))), "H 16B"),
            response_expected=response_expected,
        )

    async def request_page(self, page: int, response_expected: bool = True) -> None:
        """
        Reads 16 bytes starting from the given page and stores them into a buffer.
        The buffer can then be read out with :func:`get_page`.
        How many pages are read depends on the tag type. The page sizes are
        as follows:

        * Mifare Classic page size: 16 byte (one page is read)
        * NFC Forum Type 1 page size: 8 byte (two pages are read)
        * NFC Forum Type 2 page size: 4 byte (four pages are read)

        The general approach for reading a tag is as follows:

        1. Call :func:`request_tag_id`
        2. Wait for state to change to *RequestTagIDReady* (see :func:`get_state`
           or :attr:`CallbackID.STATE_CHANGED` callback)
        3. If looking for a specific tag then call :func:`get_tag_id` and check if the
           expected tag was found, if it was not found got back to step 1
        4. Call :func:`request_page` with page number
        5. Wait for state to change to *RequestPageReady* (see :func:`get_state`
           or :attr:`CallbackID.STATE_CHANGED` callback)
        6. Call :func:`get_page` to retrieve the page from the buffer

        If you use a Mifare Classic tag you have to authenticate a page before you
        can read it. See :func:`authenticate_mifare_classic_page`.
        """
        page = int(page)
        check_range("page", page, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.REQUEST_PAGE,
            data=pack_payload((page,), "H"),
            response_expected=response_expected,
        )

    async def get_page(self) -> tuple[int, ...]:
        """
        Returns 16 bytes of data from an internal buffer. To fill the buffer
        with specific pages you have to call :func:`request_page` beforehand.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_PAGE, response_expected=True)
        return tuple(unpack_payload(payload, "16B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        state, idle = value
        return 0, StateChangedEvent(State(state), idle)
