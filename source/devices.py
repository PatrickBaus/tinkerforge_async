# -*- coding: utf-8 -*-
import asyncio
from collections import namedtuple
from enum import Enum, IntEnum, unique
import time

from .ip_connection_helper import base58decode, pack_payload, unpack_payload

GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])


@unique
class DeviceIdentifier(IntEnum):
    BrickMaster = 13
    BrickletAmbientLight = 21
    BrickletHumidity = 27
    BrickletTemperature = 216
    BrickletSegmentDisplay4x7 = 237
    BrickletAmbientLightV2 = 259
    BrickletHumidityV2 = 283
    BrickletTemperatureV2 = 2113

@unique
class FunctionID(IntEnum):
    enumerate = 254
    adc_calibrate = 251
    get_adc_calibration = 250
    read_bricklet_uid = 249
    write_bricklet_uid = 248
    read_bricklet_plugin = 247
    write_bricklet_plugin = 246
    disconnect_probe = 128

    callback_enumerate = 253
    # Available only on bricklets with MCUs (aka the new 7p bricklets)
    get_spitfp_error_count = 234
    set_bootloader_mode = 235
    get_bootloader_mode = 236
    set_status_led_config = 239
    get_status_led_config = 240
    get_chip_temperature = 242
    reset = 243
    # Available on all bricklets
    get_identity = 255

@unique
class BrickletPort(Enum):
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'

class Device(object):
    RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0
    RESPONSE_EXPECTED_ALWAYS_TRUE = 1 # getter
    RESPONSE_EXPECTED_TRUE = 2 # setter
    RESPONSE_EXPECTED_FALSE = 3 # setter, default

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
        This function will only push the payload to the output queue. The payload still needs to be unpacked.
        This is to be done by the bricklet and then the payload is to be handed down to this function via super().
        """
        try:
            # Try to push it to the output queue. If the queue is full, drop the oldest packet and insert it again
            self.__registered_queues[header['function_id']].put_nowait({
                'timestamp': int(time.time()),
                'uid': self.uid,
                'device_id': self.DEVICE_IDENTIFIER,
                'function_id': header['function_id'],
                'payload': payload,
            })
        except asyncio.QueueFull:
            # TODO: log a warning, that we are dropping packets
            self.__registered_queues[header['function_id']].get_nowait()
            self.__registered_queues[header['function_id']].put_nowait(payload)

    def register_event_queue(self, event_id, queue):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if queue is None:
            self.__registered_queues.pop(event_id, None)
        else:
            self.__registered_queues[event_id] = queue

    async def set_debounce_period(self, debounce_period=100, response_expected=True):
        """
        Sets the period in ms with which the threshold callbacks

        * :cb:`Humidity Reached`,
        * :cb:`Analog Value Reached`

        are triggered, if the thresholds

        * :func:`Set Humidity Callback Threshold`,
        * :func:`Set Analog Value Callback Threshold`

        keep being reached.

        The default value is 100.
        """
        assert debounce_period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.set_debounce_period,
            data=pack_payload((int(debounce_period),), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

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
            function_id=FunctionID.get_identity,
            response_expected=True
        )
        uid, connected_uid, position, hw_version, fw_version, device_id = unpack_payload(payload, '8s 8s c 3B 3B H')
        return GetIdentity(
            base58decode(uid),
            base58decode(connected_uid),
            BrickletPort(position),
            hw_version,
            fw_version,
            DeviceIdentifier(device_id)
        )

@unique
class BootloaderMode(IntEnum):
    bootloader = 0
    firmware = 1
    bootloader_wait_for_reboot = 2
    firmware_wait_for_reboot = 3
    firmware_wait_for_erase_and_reboot = 4

@unique
class BootloaderStatus(IntEnum):
    ok = 0
    invalid_mode = 1
    no_change = 2
    entry_function_not_present = 3
    device_identifier_incorrect = 4
    crc_mismatch = 5

@unique
class LedConfig(IntEnum):
    off = 0
    on = 1
    show_heartbeat = 2
    show_status = 3

class DeviceWithMCU(Device):
    # Convenience imports, so that the user does not need to additionally import them
    BootloaderMode = BootloaderMode
    BootloaderStatus = BootloaderStatus
    LedConfig = LedConfig

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
            function_id=FunctionID.get_spitfp_error_count,
            response_expected=True
        )

        return GetSPITFPErrorCount(*unpack_payload(payload, 'I I I I'))

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
        assert type(mode) is BootloaderMode

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.set_bootloader_mode,
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
            function_id=FunctionID.get_bootloader_mode,
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
        assert type(pointer) is int and pointer >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.set_write_firmware_pointer,
            data=pack_payload((pointer,), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

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
            function_id=FunctionID.write_firmware,
            data=pack_payload((list(map(int, data)),), '64B'),
            response_expected=True
        )
        return unpack_payload(payload, 'B')

    async def set_status_led_config(self, config=LedConfig.show_status, response_expected=False):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        assert type(config) is LedConfig

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.set_status_led_config,
            data=pack_payload((config.value,), 'B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.get_status_led_config,
            response_expected=True
        )
        return LedConfig(unpack_payload(payload, 'B'))

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
            function_id=FunctionID.get_chip_temperature,
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
            function_id=FunctionID.reset,
            response_expected=False
        )

    async def write_uid(self, uid, response_expected=False):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        assert type(uid) is int and uid >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.write_bricklet_uid,
            data=pack_payload((uid,), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.ok

    async def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.read_bricklet_uid,
            response_expected=True
        )
        return unpack_payload(payload, 'I')
