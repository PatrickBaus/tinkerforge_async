# -*- coding: utf-8 -*-
import asyncio
from collections import namedtuple
from enum import Enum, unique
import time

from .ip_connection_helper import base58decode, pack_payload, unpack_payload

GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])


class UnknownFunctionError(Exception):
    pass


@unique
class ThresholdOption(Enum):
    OFF = 'x'
    OUTSIDE = 'o'
    INSIDE = 'i'
    LESS_THAN = '<'
    GREATER_THAN = '>'


@unique
class DeviceIdentifier(Enum):
    BrickMaster = 13
    BrickletAmbientLight = 21
    BrickletHumidity = 27
    BrickletIO16 = 28
    BrickletTemperature = 216
    BrickletAnalogIn = 219
    BrickletBarometer = 221
    BrickletPtc = 226
    BrickletMoisture = 232
    BrickletSegmentDisplay4x7 = 237
    BrickletAmbientLight_V2 = 259
    BrickletHumidity_V2 = 283
    BrickletMotionDetector_V2 = 292
    BrickletPtc_V2 = 2101
    BrickletRs232_V2 = 2108
    BrickletIO4V2 = 2111
    BrickletTemperature_V2 = 2113
    BrickletIndustrialDualAnalogIn_V2 = 2121
    BrickletAmbientLight_V3 = 2131
    BrickletSegmentDisplay4x7_V2 = 2137


@unique
class FunctionID(Enum):
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
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'


class Device(object):
    RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0
    RESPONSE_EXPECTED_ALWAYS_TRUE = 1   # getter
    RESPONSE_EXPECTED_TRUE = 2          # setter
    RESPONSE_EXPECTED_FALSE = 3         # setter, default

    def __repr__(self):
        return self.DEVICE_DISPLAY_NAME

    @property
    def ipcon(self):
        """
        Get the ip connection associated with the device
        """
        return self.__ipcon

    def __init__(self, uid, ipcon):
        """
        Creates the device object with the unique device ID *uid* and adds
        it to the IPConnection *ipcon*.
        """

        self.uid = uid if uid <= 0xFFFFFFFF else uid64_to_uid32(uid)
        self.__ipcon = ipcon
        self.api_version = (0, 0, 0)
        self.__registered_queues = {}
        self.high_level_callbacks = {}

        self.ipcon.add_device(self)

    def get_api_version(self):
        """
        Returns the API version (major, minor, revision) of the bindings for
        this device.
        """
        return self.api_version

    def _process_callback(self, header, payload):
        """
        This function will push the payload to the output queue. If the payload is None, no callback will be triggered.
        """
        self.__process_callback_header(header)
        payload, done = self._process_callback_payload(header, payload)

        if done:
            # Try to push it to the output queue. If the queue is full, drop the oldest packet and insert it again
            try:
                self.__registered_queues[header['function_id']].put_nowait({
                    'timestamp': int(time.time()),
                    'sender': self,
                    'function_id': header['function_id'],
                    'sid': header.get('sid', 0),
                    'payload': payload,
                })
            except asyncio.QueueFull:
                # TODO: log a warning, that we are dropping packets
                self.__registered_queues[header['function_id']].get_nowait()
                self.__registered_queues[header['function_id']].put_nowait(payload)

    def __process_callback_header(self, header):
        # CallbackID is defined by the brick/bricklet
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the function_id is unknown
            raise UnknownFunctionError from None

    def _process_callback_payload(self, header, payload):
        """
        Process the callback using the bricklet callback format. This function shall be
        overwritten, if processing of the payload is required.
        """
        return unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']]), True    # payload, done

    def register_event_queue(self, event_id, queue):
        """
        Registers the given *function* with the given *callback_id*.
        """
        # CallbackID is defined by the brick/bricklet
        if not type(event_id) is self.CallbackID:
            event_id = event_id(CallbackID)

        if queue is None:
            self.__registered_queues.pop(event_id, None)
        else:
            self.__registered_queues[event_id] = queue

    async def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_IDENTITY,
            response_expected=True
        )
        uid, connected_uid, position, hw_version, fw_version, device_id = unpack_payload(payload, '8s 8s c 3B 3B H')
        try:
            position = BrickletPort(position)
        except ValueError:
            position = int(position)    # It is a Master brick. The position is its position in the stack.

        return GetIdentity(
            base58decode(uid),
            None if connected_uid == '0' else base58decode(connected_uid),
            position,
            hw_version,
            fw_version,
            DeviceIdentifier(device_id)
        )

    async def connect(self):
        await self.__ipcon.connect()

    async def disconnect(self):
        await self.__ipcon.disconnect()


class DeviceWithMCU(Device):
    async def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHIP_TEMPERATURE,
            response_expected=True
        )
        return unpack_payload(payload, 'h')

    async def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.RESET,
            response_expected=False
        )


@unique
class BootloaderMode(Enum):
    BOOTLOADER = 0
    FIRMWARE = 1
    BOOTLOADER_WAIT_FOR_REBOOT = 2
    FIRMWARE_WAIT_FOR_REBOOT = 3
    FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4


@unique
class BootloaderStatus(Enum):
    OK = 0
    INVALID_MODE = 1
    NO_CHANGE = 2
    ENTRY_FUNCTION_NOT_PRESENT = 3
    DEVICE_IDENTIFIER_INCORRECT = 4
    CRC_MISMATCH = 5


@unique
class LedConfig(Enum):
    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_STATUS = 3


class BrickletWithMCU(DeviceWithMCU):
    # Convenience imports, so that the user does not need to additionally import them
    BootloaderStatus = BootloaderStatus
    LedConfig = LedConfig
    BootloaderMode = BootloaderMode

    async def set_bootloader_mode(self, mode):
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier und crc are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        if not type(mode) is BootloaderMode:
            mode = BootloaderMode(mode)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BOOTLOADER_MODE,
            data=pack_payload((mode.value,), 'B'),
            response_expected=True
        )
        return BootloaderStatus(unpack_payload(payload, 'B'))

    async def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_BOOTLOADER_MODE,
            response_expected=True
        )
        return BootloaderMode(unpack_payload(payload, 'B'))

    async def set_write_firmware_pointer(self, pointer, response_expected=False):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        assert pointer >= 0

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WRITE_FIRMWARE_POINTER,
            data=pack_payload((int(pointer),), 'I'),
            response_expected=response_expected
        )

    async def write_firmware(self, data):
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
            data=pack_payload((list(map(int, data)),), '64B'),
            response_expected=True
        )
        return unpack_payload(payload, 'B')

    async def set_status_led_config(self, config=LedConfig.SHOW_STATUS, response_expected=False):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        if not type(config) is LedConfig:
            config = LedConfig(config)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STATUS_LED_CONFIG,
            data=pack_payload((config.value,), 'B'),
            response_expected=response_expected
        )

    async def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_STATUS_LED_CONFIG,
            response_expected=True
        )
        return LedConfig(unpack_payload(payload, 'B'))

    async def write_uid(self, uid, response_expected=False):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        assert uid >= 0

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_BRICKLET_UID,
            data=pack_payload((int(uid),), 'I'),
            response_expected=response_expected
        )

    async def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_BRICKLET_UID,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def get_spitfp_error_count(self):
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
            device=self,
            function_id=FunctionID.GET_SPITFP_ERROR_COUNT,
            response_expected=True
        )

        return GetSPITFPErrorCount(*unpack_payload(payload, 'I I I I'))
