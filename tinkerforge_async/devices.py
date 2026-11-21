"""
This file contains all base classes used by Bricks and bricklets
"""

from __future__ import annotations

import time
from collections.abc import AsyncGenerator, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, TypeAlias

from .ip_connection_helper import base58decode, pack_payload, uid64_to_uid32, unpack_payload
from .quantities import CELSIUS_ZERO

if TYPE_CHECKING:
    from .ip_connection import HeaderPayload, IPConnectionAsync


class UnknownFunctionError(Exception):
    """
    Raised when an unknown callback id was returned and the Brick/Bricklet does
    not know which function it belongs to
    """


class InvalidSidError(ValueError):
    """
    Raised when a secondary id (sid) does not exist on the Brick/Bricklet or does not support the requested
    function, e.g. a sid without a callback configuration. Inherits from ValueError for backwards compatibility.
    """


@unique
class ThresholdOption(Enum):
    """
    These options can be used to configure thresholds for callbacks
    """

    OFF = "x"
    OUTSIDE = "o"
    INSIDE = "i"
    LESS_THAN = "<"
    GREATER_THAN = ">"


@unique
class DeviceIdentifier(Enum):
    """
    The device ids used by the Bricks and bricklets to communicate
    """

    BRICK_MASTER = 13
    BRICKLET_AMBIENT_LIGHT = 21
    BRICKLET_HUMIDITY = 27
    BRICKLET_IO_16 = 28
    BRICKLET_TEMPERATURE = 216
    BRICKLET_ANALOG_IN = 219
    BRICKLET_BAROMETER = 221
    BRICKLET_PTC = 226
    BRICKLET_MOISTURE = 232
    BRICKLET_SEGMENT_DISPLAY_4x7 = 237  # pylint: disable=invalid-name
    BRICKLET_AMBIENT_LIGHT_V2 = 259
    BRICKLET_HUMIDITY_V2 = 283
    BRICKLET_MOTION_DETECTOR_V2 = 292
    BRICKLET_PTC_V2 = 2101
    BRICKLET_RS232_V2 = 2108
    BRICKLET_THERMOCOUPLE_V2 = 2109
    BRICKLET_IO_4_V2 = 2111
    BRICKLET_TEMPERATURE_V2 = 2113
    BRICKLET_BAROMETER_V2 = 2117
    BRICKLET_INDUSTRIAL_DUAL_0_20MA_V2 = 2120
    BRICKLET_INDUSTRIAL_DUAL_ANALOG_IN_V2 = 2121
    BRICKLET_ISOLATOR = 2122
    BRICKLET_AMBIENT_LIGHT_V3 = 2131
    BRICKLET_SEGMENT_DISPLAY_4x7_V2 = 2137  # pylint: disable=invalid-name
    BRICKLET_INDUSTRIAL_PTC = 2164


class _FunctionID(Enum):
    pass


@unique
class FunctionID(_FunctionID):
    """
    General purpose functions supported by most Bricks and Bricklets
    """

    ADC_CALIBRATE = 251
    GET_ADC_CALIBRATION = 250
    READ_BRICKLET_UID = 249
    WRITE_BRICKLET_UID = 248
    READ_BRICKLET_PLUGIN = 247
    WRITE_BRICKLET_PLUGIN = 246
    DISCONNECT_PROBE = 128

    # Available only on bricklets with MCUs (aka the new 7p bricklets)
    GET_SPITFP_ERROR_COUNT = 234
    SET_BOOTLOADER_MODE = 235
    GET_BOOTLOADER_MODE = 236
    SET_WRITE_FIRMWARE_POINTER = 237
    WRITE_FIRMWARE = 238
    SET_STATUS_LED_CONFIG = 239
    GET_STATUS_LED_CONFIG = 240
    GET_CHIP_TEMPERATURE = 242
    RESET = 243
    # Available on all bricklets
    GET_IDENTITY = 255


@unique
class BrickletPort(Enum):
    """
    The port to which a Bricklet is connected on a Master Brick
    """

    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"  # Only available on Bricks/HATs with more than four ports
    F = "f"
    G = "g"
    H = "h"
    Z = "z"  # Bricklets connected to an Isolator Bricklet are always at position 'z'


class GetSPITFPErrorCount(NamedTuple):
    error_count_ack_checksum: int
    error_count_message_checksum: int
    error_count_frame: int
    error_count_overflow: int


class GetIdentity(NamedTuple):
    uid: int
    connected_uid: int | None
    position: int | BrickletPort
    hardware_version: tuple[int, int, int]
    firmware_version: tuple[int, int, int]
    device_identifier: DeviceIdentifier


class Device:
    """
    The base class of all Bricks and Bricklets. Newer Bricks or Bricklets inherit from this class and add their
    features.
    """

    RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0
    RESPONSE_EXPECTED_ALWAYS_TRUE = 1  # getter
    RESPONSE_EXPECTED_TRUE = 2  # setter
    RESPONSE_EXPECTED_FALSE = 3  # setter, default

    # The following attributes are defined by every device with callbacks. See `read_events()`.
    CallbackID: ClassVar[Any]
    CALLBACK_FORMATS: ClassVar[Mapping[Any, str]]
    SID_TO_CALLBACK: ClassVar[Mapping[int, Sequence[Any]]]

    def __str__(self) -> str:
        return f"{self.__display_name} with uid {self.uid} connected at {self.__ipcon}"

    def __repr__(self) -> str:
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}(uid={self.uid}, ipcon={self.ipcon!r})"

    @property
    def ipcon(self) -> IPConnectionAsync:
        """
        Get the ip connection associated with the device
        """
        return self.__ipcon

    @property
    def uid(self) -> int:
        """
        Get the ip connection associated with the device
        """
        return self.__uid

    def __init__(self, display_name: str, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates the device object with the unique device ID *uid* and adds
        it to the IPConnection *ipcon*.
        """

        self.__display_name = display_name
        self.__uid = uid if uid <= 0xFFFFFFFF else uid64_to_uid32(uid)
        self.__ipcon = ipcon
        self.api_version = (0, 0, 0)

    def _validate_sid(self, sid: int, valid_sids: Iterable[int]) -> None:
        """
        Check that the secondary id (sid) is supported by this device. Unlike an assert statement, this check is
        also performed when Python runs with optimizations enabled (-O or -OO).

        Parameters
        ----------
        sid: int
            The secondary id to check
        valid_sids: Iterable of int
            The secondary ids supported by the function called

        Raises
        ------
        InvalidSidError
            If `sid` is not in `valid_sids`
        """
        valid_sids = tuple(valid_sids)
        if sid not in valid_sids:
            raise InvalidSidError(f"Invalid sid {sid!r} for {self}. Valid sids: {valid_sids}.")

    def get_api_version(self) -> tuple[int, int, int]:
        """
        Returns the API version (major, minor, revision) of the bindings for
        this device.
        """
        return self.api_version

    async def get_identity(self) -> GetIdentity:
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a' to 'h' or 'z' (behind an Isolator Bricklet).

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_IDENTITY, response_expected=True
        )
        uid, connected_uid, position, hw_version, fw_version, device_id = unpack_payload(payload, "8s 8s c 3B 3B H")
        try:
            position = BrickletPort(position)
        except ValueError:
            position = int(position)  # It is a Master brick. The position is its position in the stack.

        return GetIdentity(
            base58decode(uid),
            None if connected_uid == "0" else base58decode(connected_uid),
            position,
            hw_version,
            fw_version,
            DeviceIdentifier(device_id),
        )

    async def _read_events(self) -> AsyncGenerator[tuple[HeaderPayload, bytes], None]:
        async for event in self.ipcon.read_events(self.uid):
            yield event

    def _get_registered_events(self, events: Sequence[Any] | None, sids: Sequence[int] | None) -> set[Any]:
        """
        Translate the filters of `read_events()` into the set of callbacks that are forwarded.

        Parameters
        ----------
        events: sequence of CallbackID or int, optional
            The callbacks to register.
        sids: sequence of int, optional
            The secondary ids to register. All callbacks of these sids are registered. Unknown sids are ignored.

        Returns
        -------
        set of CallbackID
            All callbacks if neither `events` nor `sids` are given. Otherwise the union of the callbacks in `events`
            and the callbacks belonging to `sids`.

        Raises
        ------
        ValueError
            If an entry in `events` is not a valid callback id.
        """
        if events is None and sids is None:
            return set(self.CALLBACK_FORMATS)

        registered_events = set()
        for event in events or ():
            registered_events.add(self.CallbackID(event))
        for sid in sids or ():
            registered_events.update(self.SID_TO_CALLBACK.get(sid, ()))
        return registered_events

    def _convert_callback(self, callback_id: Any, value: Any) -> tuple[int, Any]:  # pylint: disable=unused-argument
        """
        Convert the unpacked payload of a callback to the value of an `Event`. The default is a device with a single
        sid 0 that returns the raw value. Devices override this method (or `_to_events()` if a payload does not map to
        exactly one event).

        Parameters
        ----------
        callback_id: CallbackID
            The callback that was received.
        value: Any
            The payload of the callback unpacked with the format in `CALLBACK_FORMATS`.

        Returns
        -------
        tuple of int and Any
            The sid and the payload of the event.
        """
        return 0, value

    def _to_events(  # pylint: disable=unused-argument
        self, callback_id: Any, value: Any, sids: Sequence[int] | None
    ) -> Iterable[Event]:
        """
        Convert the unpacked payload of a callback to events. The default implementation creates one event from
        `_convert_callback()`. Override it if a payload results in no or several events, e.g. because the channel is
        part of the payload or the payload spans several packets.

        Parameters
        ----------
        callback_id: CallbackID
            The callback that was received.
        value: Any
            The payload of the callback unpacked with the format in `CALLBACK_FORMATS`.
        sids: sequence of int, optional
            The sids that were passed to `read_events()`, or `None` if the caller did not filter by sid.

        Returns
        -------
        iterable of Event
            The events to yield.
        """
        sid, payload = self._convert_callback(callback_id, value)
        return (Event(self, sid, callback_id, payload),)

    async def read_events(
        self,
        events: Sequence[Any] | None = None,
        sids: Sequence[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        """
        Get the callback events of the device.

        Parameters
        ----------
        events: sequence of CallbackID, optional
            Only yield events of these callbacks.
        sids: sequence of int, optional
            Only yield events of the callbacks that belong to these sids.

        If both `events` and `sids` are given, events matching either filter are yielded. If neither is given, all
        events are yielded. An empty sequence selects nothing.

        Yields
        ------
        Event
            The events matching the filters.

        Raises
        ------
        ValueError
            If an entry in `events` is not a valid callback id.
        """
        registered_events = self._get_registered_events(events, sids)

        async for header, payload in self._read_events():
            try:
                callback_id = self.CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if callback_id in registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[callback_id])
                for event in self._to_events(callback_id, value, sids):
                    yield event

    async def connect(self) -> None:
        """
        Connect the ip connection if not already connected
        """
        await self.__ipcon.connect()

    async def disconnect(self) -> None:
        """
        Disconnect the ip connection. This will also disconnect all other
        Bricks and Bricklets.
        """
        await self.__ipcon.disconnect()


class DeviceWithMCU(Device):
    """
    The base class for a more advanced Brick or Bricklet with a microcontroller on board.
    """

    async def get_chip_temperature(self) -> Decimal:
        """
        Returns the temperature in K as measured inside the microcontroller. The value returned is not the
        ambient temperature!

        The temperature is only proportional to the real temperature, and it has bad accuracy. Practically it is only
        useful as an indicator for temperature changes.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIP_TEMPERATURE, response_expected=True
        )
        result = unpack_payload(payload, "h")
        return result + CELSIUS_ZERO

    async def reset(self) -> None:
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.RESET, response_expected=False)


@unique
class BootloaderMode(Enum):
    """
    Bricklets with a microcontroller have a bootloader that activated by setting
    the bootloader mode to BOOTLOADER. The Bricklet can then be flashed.
    """

    BOOTLOADER = 0
    FIRMWARE = 1
    BOOTLOADER_WAIT_FOR_REBOOT = 2
    FIRMWARE_WAIT_FOR_REBOOT = 3
    FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4


@unique
class BootloaderStatus(Enum):
    """
    If the bricklet has a microcontroller, this is the status reported by
    the bootloader, when queried.
    """

    OK = 0
    INVALID_MODE = 1
    NO_CHANGE = 2
    ENTRY_FUNCTION_NOT_PRESENT = 3
    DEVICE_IDENTIFIER_INCORRECT = 4
    CRC_MISMATCH = 5


@unique
class LedConfig(Enum):
    """
    All Bricklets with a mcu on board also feature one or more LEDs to signal
    their status. These are the config options.
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_STATUS = 3


class BrickletWithMCU(DeviceWithMCU):
    """
    The new Bricklets feature a microcontroller and this base class implements
    the generic function supported by the microcontroller.
    """

    # Convenience imports, so that the user does not need to additionally import them
    BootloaderStatus: TypeAlias = BootloaderStatus
    LedConfig: TypeAlias = LedConfig
    BootloaderMode: TypeAlias = BootloaderMode

    async def set_bootloader_mode(self, mode: BootloaderMode) -> BootloaderStatus:
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier und crc are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        mode = BootloaderMode(mode)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BOOTLOADER_MODE,
            data=pack_payload((mode.value,), "B"),
            response_expected=True,
        )
        return BootloaderStatus(unpack_payload(payload, "B"))

    async def get_bootloader_mode(self) -> BootloaderMode:
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BOOTLOADER_MODE, response_expected=True
        )
        return BootloaderMode(unpack_payload(payload, "B"))

    async def set_write_firmware_pointer(self, pointer: int, response_expected: bool = False) -> None:
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        if pointer < 0:
            raise ValueError(f"Invalid argument: expected pointer >= 0, got pointer={pointer!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WRITE_FIRMWARE_POINTER,
            data=pack_payload((int(pointer),), "I"),
            response_expected=response_expected,
        )

    async def write_firmware(self, data: Iterable[int]) -> int:
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_FIRMWARE,
            data=pack_payload((list(map(int, data)),), "64B"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def set_status_led_config(
        self, config: LedConfig | int = LedConfig.SHOW_STATUS, response_expected: bool = False
    ) -> None:
        """
        Sets the status LED configuration. By default, the LED shows communication traffic between Brick and Bricklet,
        it flickers once for every 10 data packets received.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = LedConfig(config)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STATUS_LED_CONFIG,
            data=pack_payload((config.value,), "B"),
            response_expected=response_expected,
        )

    async def get_status_led_config(self) -> LedConfig:
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATUS_LED_CONFIG, response_expected=True
        )
        return LedConfig(unpack_payload(payload, "B"))

    async def write_uid(self, uid: int, response_expected: bool = False) -> None:
        """
        Writes a new UID into flash. If you want to set a new UID you have to decode the Base58 encoded UID string into
        an integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        if uid < 0:
            raise ValueError(f"Invalid argument: expected uid >= 0, got uid={uid!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_BRICKLET_UID,
            data=pack_payload((int(uid),), "I"),
            response_expected=response_expected,
        )

    async def read_uid(self) -> int:
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.READ_BRICKLET_UID, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def get_spitfp_error_count(self) -> GetSPITFPErrorCount:
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ack checksum errors,
        * message checksum errors,
        * frameing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Bricklet side. All
        Bricks have a similar function that returns the errors on the Brick side.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPITFP_ERROR_COUNT, response_expected=True
        )

        return GetSPITFPErrorCount(*unpack_payload(payload, "I I I I"))


@dataclass
class Event:
    timestamp: float = field(init=False)
    sender: Device
    sid: int
    function_id: Any
    payload: Any
    additional: Any = None

    def __post_init__(self) -> None:
        self.timestamp = time.time()

    def __str__(self) -> str:
        return (
            f"Event(timestamp={self.timestamp}, sender={self.sender}, sid={self.sid}, "
            f"function_id={self.function_id}, payload={self.payload})"
        )


class BasicCallbackConfiguration(NamedTuple):
    option: ThresholdOption
    minimum: Decimal
    maximum: Decimal


class SimpleCallbackConfiguration(NamedTuple):
    period: Decimal
    value_has_to_change: bool


class AdvancedCallbackConfiguration(NamedTuple):
    period: Decimal
    value_has_to_change: bool
    option: ThresholdOption | None
    minimum: Decimal | None
    maximum: Decimal | None


class GetSPITFPBaudrateConfig(NamedTuple):
    enable_dynamic_baudrate: bool
    minimum_dynamic_baudrate: int
