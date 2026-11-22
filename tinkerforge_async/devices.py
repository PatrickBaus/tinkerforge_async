"""
This file contains all base classes used by Bricks and bricklets
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncGenerator, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, ClassVar, NamedTuple, TypeAlias, cast

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
    BRICK_RED = 17
    BRICK_IMU_V2 = 18
    BRICK_SILENT_STEPPER = 19
    BRICKLET_AMBIENT_LIGHT = 21
    BRICKLET_DISTANCE_IR = 25
    BRICKLET_HUMIDITY = 27
    BRICKLET_IO_16 = 28
    BRICK_HAT = 111
    BRICK_HAT_ZERO = 112
    BRICK_ESP32 = 113
    BRICK_ESP32_ETHERNET = 115
    BRICKLET_JOYSTICK = 210
    BRICKLET_LCD_20X4 = 212
    BRICKLET_LINEAR_POTI = 213
    BRICKLET_ROTARY_POTI = 215
    BRICKLET_TEMPERATURE = 216
    BRICKLET_ANALOG_IN = 219
    BRICKLET_BAROMETER = 221
    BRICKLET_INDUSTRIAL_DIGITAL_OUT_4 = 224
    BRICKLET_PTC = 226
    BRICKLET_INDUSTRIAL_DUAL_0_20MA = 228
    BRICKLET_MOISTURE = 232
    BRICKLET_MULTI_TOUCH = 234
    BRICKLET_SEGMENT_DISPLAY_4x7 = 237  # pylint: disable=invalid-name
    BRICKLET_SOUND_INTENSITY = 238
    BRICKLET_TILT = 239
    BRICKLET_HALL_EFFECT = 240
    BRICKLET_LINE = 241
    BRICKLET_PIEZO_SPEAKER = 242
    BRICKLET_COLOR = 243
    BRICKLET_RS232 = 254
    BRICKLET_AMBIENT_LIGHT_V2 = 259
    BRICKLET_DUST_DETECTOR = 260
    BRICKLET_OLED_64X48 = 264
    BRICKLET_MOTORIZED_LINEAR_POTI = 267
    BRICKLET_REAL_TIME_CLOCK = 268
    BRICKLET_CAN = 270
    BRICKLET_GPS_V2 = 276
    BRICKLET_RS485 = 277
    BRICKLET_THERMAL_IMAGING = 278
    BRICKLET_XMC1400_BREAKOUT = 279
    BRICKLET_RGB_LED_BUTTON = 282
    BRICKLET_HUMIDITY_V2 = 283
    BRICKLET_INDUSTRIAL_DUAL_RELAY = 284
    BRICKLET_DMX = 285
    BRICKLET_NFC = 286
    BRICKLET_OUTDOOR_WEATHER = 288
    BRICKLET_REMOTE_SWITCH_V2 = 289
    BRICKLET_SOUND_PRESSURE_LEVEL = 290
    BRICKLET_TEMPERATURE_IR_V2 = 291
    BRICKLET_MOTION_DETECTOR_V2 = 292
    BRICKLET_INDUSTRIAL_COUNTER = 293
    BRICKLET_ROTARY_ENCODER_V2 = 294
    BRICKLET_ANALOG_IN_V3 = 295
    BRICKLET_SOLID_STATE_RELAY_V2 = 296
    BRICKLET_AIR_QUALITY = 297
    BRICKLET_LCD_128X64 = 298
    BRICKLET_DISTANCE_US_V2 = 299
    BRICKLET_INDUSTRIAL_DIGITAL_IN_4_V2 = 2100
    BRICKLET_PTC_V2 = 2101
    BRICKLET_INDUSTRIAL_QUAD_RELAY_V2 = 2102
    BRICKLET_LED_STRIP_V2 = 2103
    BRICKLET_LOAD_CELL_V2 = 2104
    BRICKLET_VOLTAGE_CURRENT_V2 = 2105
    BRICKLET_REAL_TIME_CLOCK_V2 = 2106
    BRICKLET_CAN_V2 = 2107
    BRICKLET_RS232_V2 = 2108
    BRICKLET_THERMOCOUPLE_V2 = 2109
    BRICKLET_PARTICULATE_MATTER = 2110
    BRICKLET_IO_4_V2 = 2111
    BRICKLET_OLED_128X64_V2 = 2112
    BRICKLET_TEMPERATURE_V2 = 2113
    BRICKLET_IO16_V2 = 2114
    BRICKLET_ANALOG_OUT_V3 = 2115
    BRICKLET_INDUSTRIAL_ANALOG_OUT_V2 = 2116
    BRICKLET_BAROMETER_V2 = 2117
    BRICKLET_UV_LIGHT_V2 = 2118
    BRICKLET_DUAL_BUTTON_V2 = 2119
    BRICKLET_INDUSTRIAL_DUAL_0_20MA_V2 = 2120
    BRICKLET_INDUSTRIAL_DUAL_ANALOG_IN_V2 = 2121
    BRICKLET_ISOLATOR = 2122
    BRICKLET_ONE_WIRE = 2123
    BRICKLET_INDUSTRIAL_DIGITAL_OUT_4_V2 = 2124
    BRICKLET_DISTANCE_IR_V2 = 2125
    BRICKLET_RGB_LED_V2 = 2127
    BRICKLET_COLOR_V2 = 2128
    BRICKLET_MULTI_TOUCH_V2 = 2129
    BRICKLET_ACCELEROMETER_V2 = 2130
    BRICKLET_AMBIENT_LIGHT_V3 = 2131
    BRICKLET_HALL_EFFECT_V2 = 2132
    BRICKLET_SEGMENT_DISPLAY_4x7_V2 = 2137  # pylint: disable=invalid-name
    BRICKLET_JOYSTICK_V2 = 2138
    BRICKLET_LINEAR_POTI_V2 = 2139
    BRICKLET_ROTARY_POTI_V2 = 2140
    BRICKLET_LASER_RANGE_FINDER_V2 = 2144
    BRICKLET_PIEZO_SPEAKER_V2 = 2145
    BRICKLET_E_PAPER_296X128 = 2146
    BRICKLET_CO2_V2 = 2147
    BRICKLET_ENERGY_MONITOR = 2152
    BRICKLET_COMPASS = 2153
    BRICKLET_PERFORMANCE_DC = 2156
    BRICKLET_SERVO_V2 = 2157
    BRICKLET_IMU_V3 = 2161
    BRICKLET_INDUSTRIAL_DUAL_AC_RELAY = 2162
    BRICKLET_INDUSTRIAL_PTC = 2164
    BRICKLET_DC_V2 = 2165
    BRICKLET_SILENT_STEPPER_V2 = 2166
    BRICKLET_GPS_V3 = 2171
    BRICKLET_INDUSTRIAL_DUAL_AC_IN = 2174


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


@dataclass(frozen=True, slots=True)
class ChannelConfiguration:
    """
    Describes how the callbacks of a channel are configured, i.e. which methods of the device are called by
    `Device.set_callback_configuration()` and `Device.get_callback_configuration()`.

    Parameters
    ----------
    name: str
        The name used by the methods. The configuration of a channel called `temperature` is set by
        `set_temperature_callback_configuration()`, or by `set_temperature_callback_period()` and
        `set_temperature_callback_threshold()` if `split` is set.
    split: bool
        The device configures the period and the threshold with separate functions. These are the devices that do not
        have a `value_has_to_change` option.
    thresholds: bool
        The callback has a threshold with an option, a minimum and a maximum. If not, only the period and
        `value_has_to_change` are set.
    default: Decimal or int
        The value of the minimum and maximum, if they are not given. This is the SI value of the raw value 0 of the
        device.
    wrap_advanced: bool
        Return the configuration of a callback without thresholds as an `AdvancedCallbackConfiguration`, where the
        option, minimum and maximum are `None`.
    """

    name: str
    split: bool = False
    thresholds: bool = True
    default: Decimal | int = 0
    wrap_advanced: bool = False


@dataclass(frozen=True, slots=True)
class Channel:
    """
    Describes a value of a Brick or Bricklet, that is addressed by its secondary id (sid). The table of all channels
    of a device (`Device.CHANNELS`) is the source for the validation of the sids, the callbacks of a sid
    (`Device.SID_TO_CALLBACK`) and the generic implementations `Device._get_value()`,
    `Device._set_callback_configuration()` and `Device._get_callback_configuration()`.

    Parameters
    ----------
    sid: int
        The secondary id of the channel.
    getter: str, optional
        The name of the method that returns the value of the channel. `None` if the value cannot be read.
    callbacks: tuple of CallbackID
        The callbacks that belong to the channel.
    configuration: ChannelConfiguration, optional
        How the callbacks are configured. `None` if the callbacks cannot be configured.
    index: int, optional
        If set, it is passed as the first argument to the methods, that read and configure the channel. These are the
        devices that have several identical channels, which are selected by an argument.
    """

    sid: int
    getter: str | None = None
    callbacks: tuple[Any, ...] = ()
    configuration: ChannelConfiguration | None = None
    index: int | None = None


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
    # The channels of the device. If a class defines it, `SID_TO_CALLBACK` is generated from it.
    CHANNELS: ClassVar[Sequence[Channel]] = ()

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if "CHANNELS" in cls.__dict__:
            cls.SID_TO_CALLBACK = {channel.sid: channel.callbacks for channel in cls.CHANNELS}

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

    def _get_channel(self, sid: int, *, configurable: bool = False) -> Channel:
        """
        Get the channel with the secondary id (sid) from the table of channels.

        Parameters
        ----------
        sid: int
            The secondary id of the channel
        configurable: bool
            Only accept channels with a callback configuration. Otherwise, only accept channels with a getter.

        Raises
        ------
        InvalidSidError
            If there is no such channel.
        """
        if configurable:
            channels = [channel for channel in self.CHANNELS if channel.configuration is not None]
        else:
            channels = [channel for channel in self.CHANNELS if channel.getter is not None]
        self._validate_sid(sid, (channel.sid for channel in channels))
        return next(channel for channel in channels if channel.sid == sid)

    async def _get_value(self, sid: int) -> Any:
        """
        Get the current value of a channel. See `Channel`.
        """
        channel = self._get_channel(sid)
        arguments = () if channel.index is None else (channel.index,)
        # _get_channel() only returns channels with a getter
        return await getattr(self, cast(str, channel.getter))(*arguments)

    async def _set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: float | Decimal = 0,
        value_has_to_change: bool = False,
        option: ThresholdOption | int = ThresholdOption.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        """
        Configure the callbacks of a channel. See `Channel`.
        """
        channel = self._get_channel(sid, configurable=True)
        # _get_channel() only returns channels with a configuration
        configuration = cast(ChannelConfiguration, channel.configuration)
        arguments = () if channel.index is None else (channel.index,)

        if not configuration.thresholds:
            await getattr(self, f"set_{configuration.name}_callback_configuration")(
                *arguments, period, value_has_to_change, response_expected
            )
            return

        minimum = configuration.default if minimum is None else minimum
        maximum = configuration.default if maximum is None else maximum
        if configuration.split:
            await asyncio.gather(
                getattr(self, f"set_{configuration.name}_callback_period")(*arguments, period, response_expected),
                getattr(self, f"set_{configuration.name}_callback_threshold")(
                    *arguments, option, minimum, maximum, response_expected
                ),
            )
        else:
            await getattr(self, f"set_{configuration.name}_callback_configuration")(
                *arguments, period, value_has_to_change, option, minimum, maximum, response_expected
            )

    async def _get_callback_configuration(self, sid: int) -> Any:
        """
        Get the configuration of the callbacks of a channel. See `Channel`.
        """
        channel = self._get_channel(sid, configurable=True)
        # _get_channel() only returns channels with a configuration
        configuration = cast(ChannelConfiguration, channel.configuration)
        arguments = () if channel.index is None else (channel.index,)

        if configuration.split:
            period, config = await asyncio.gather(
                getattr(self, f"get_{configuration.name}_callback_period")(*arguments),
                getattr(self, f"get_{configuration.name}_callback_threshold")(*arguments),
            )
            return AdvancedCallbackConfiguration(period, True, *config)

        result = await getattr(self, f"get_{configuration.name}_callback_configuration")(*arguments)
        if configuration.wrap_advanced:
            return AdvancedCallbackConfiguration(result.period, result.value_has_to_change, None, None, None)
        return result

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
