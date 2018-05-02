# -*- coding: utf-8 -*-

import asyncio, async_timeout
import async_timeout
from enum import IntEnum, unique
import logging
import struct
import time
import traceback

from .ip_connection_helper import base58decode, unpack_payload
from .devices import DeviceIdentifier

class UnknownFunctionError(Exception):
    pass

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
#    callback_connected = 0
#    callback_disconnected = 1

@unique
class EnumerationType(IntEnum):
    available = 0
    connected = 1
    disconnected = 2

@unique
class MessageType(IntEnum):
    device_connected = 0
    device_disconnected = 1

@unique
class Flags(IntEnum):
    ok = 0
    invalid_parameter = 1
    function_not_supported = 2

DEFAULT_WAIT_TIMEOUT = 2.5 # in seconds
def parse_header(data):
    uid, payload_size, function_id, options, flags = struct.unpack_from(IPConnectionAsync.HEADER_FORMAT, data)
    try:
      function_id = FunctionID(function_id)
    except ValueError:
        # Do not assign an enum, leave the int
        pass
    sequence_number = None if (options >> 4) & 0b1111 == 0 else (options >> 4) & 0b1111   # There is no sequence number if it is a callback (sequence_number == 0)
    response_expected = bool(options >> 3 & 0b1)
    #options = options & 0b111 # Options for future use
    try:
        flags = Flags(flags)
    except ValueError:
        # Do not assign an enum, leave the int
        pass

    return payload_size, \
           {'uid': uid,
            'sequence_number': sequence_number,
            'response_expected': response_expected,
            'function_id': function_id,
            'flags': flags
           }

class Device(object):
    RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0
    RESPONSE_EXPECTED_ALWAYS_TRUE = 1 # getter
    RESPONSE_EXPECTED_TRUE = 2 # setter
    RESPONSE_EXPECTED_FALSE = 3 # setter, default

    def __init__(self, uid, ipcon):
        """
        Creates the device object with the unique device ID *uid* and adds
        it to the IPConnection *ipcon*.
        """

        self.uid = uid if uid <= 0xFFFFFFFF else uid64_to_uid32(uid)
        self.ipcon = ipcon
        self.api_version = (0, 0, 0)
        self.__registered_queues = {}
        self.high_level_callbacks = {}

        self.response_expected = [Device.RESPONSE_EXPECTED_INVALID_FUNCTION_ID] * 256
        self.response_expected[IPConnectionAsync.FUNCTION_ADC_CALIBRATE] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[IPConnectionAsync.FUNCTION_GET_ADC_CALIBRATION] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[IPConnectionAsync.FUNCTION_READ_BRICKLET_UID] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[IPConnectionAsync.FUNCTION_WRITE_BRICKLET_UID] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[IPConnectionAsync.FUNCTION_READ_BRICKLET_PLUGIN] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[IPConnectionAsync.FUNCTION_WRITE_BRICKLET_PLUGIN] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE

        ipcon.add_device(self)

    def get_api_version(self):
        """
        Returns the API version (major, minor, revision) of the bindings for
        this device.
        """
        return self.api_version

    def process_callback(self, header, payload):
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

class IPConnectionAsync(object):
    FUNCTION_ENUMERATE = 254
    FUNCTION_ADC_CALIBRATE = 251
    FUNCTION_GET_ADC_CALIBRATION = 250
    FUNCTION_READ_BRICKLET_UID = 249
    FUNCTION_WRITE_BRICKLET_UID = 248
    FUNCTION_READ_BRICKLET_PLUGIN = 247
    FUNCTION_WRITE_BRICKLET_PLUGIN = 246
    FUNCTION_DISCONNECT_PROBE = 128

    CALLBACK_ENUMERATE = 253
    CALLBACK_CONNECTED = 0
    CALLBACK_DISCONNECTED = 1
    
    BROADCAST_UID = 0

    # See https://www.tinkerforge.com/en/doc/Low_Level_Protocols/TCPIP.html for details
    HEADER_FORMAT = '<IBBBB'  # little endian (<), uid (I, uint32), size (B, uint8), function id, squence number, flags

    @property
    def enumeration_queue(self):
        """
        Sets the timeout for async operations in seconds
        """
        return self.__enumeration_queue

    @property
    def timeout(self):
        """
        Returns the timeout for async operations in seconds
        """
        return self.__timeout
        
    @property
    def logger(self):
        return self.__logger

    @timeout.setter
    def timeout(self, value):
        self.__timeout = abs(int(value))

    def __init__(self, loop):
        self.__loop = loop
        self.__sequence_number = 0
        self.__timeout = DEFAULT_WAIT_TIMEOUT
        self.__pending_requests = {}

        self.__enumeration_queue = asyncio.Queue(maxsize=20, loop=self.__loop)
        self.__reply_queue = asyncio.Queue(maxsize=20, loop=self.__loop)

        self.__devices = {}
        
        self.__logger = logging.getLogger(__name__)

    def __get_sequence_number(self):
        self.__sequence_number = (self.__sequence_number % 15) + 1

        return self.__sequence_number 

    def __create_packet_header(self, payload_size, function_id, uid=None, response_expected=False):
        uid = IPConnectionAsync.BROADCAST_UID if uid is None else uid
        packet_size = payload_size + struct.calcsize(IPConnectionAsync.HEADER_FORMAT)
        sequence_number = self.__get_sequence_number()
        response_expected = bool(response_expected)

        sequence_number_and_options = (sequence_number << 4) | response_expected << 3

        return (struct.pack(IPConnectionAsync.HEADER_FORMAT, uid, packet_size, function_id, sequence_number_and_options, Flags.ok),
                sequence_number)

    def add_device(self, device):
        self.logger.debug('Adding device: %(device)s', {'device': device})
        self.__devices[device.uid] = device

    async def enumerate(self):
        """
        Broadcasts an enumerate request. All devices will respond with an enumerate callback.
        Returns: None, it does not support 'response_expected'
        """
        self.logger.debug('Enumerating Node')
        await self.send_request(
            device=None,
            function_id=FunctionID.enumerate
        )

    async def send_request(self, device, function_id, data=b'', response_expected=False):
        header, sequence_number = self.__create_packet_header(
            payload_size=len(data),
            function_id=function_id,
            uid=0 if device is None else device.uid,
            response_expected=response_expected,
        )
        
        request = header + data

        # If we are waiting for a response, send the request, then pass on the response as a future
        self.logger.debug('Sending request: %(header)s - %(payload)s', {'header': header, 'payload': data})
        self.__writer.write(request)
        if response_expected:
            self.logger.debug('Waiting for reply for request number %(sequence_number)s.', {'sequence_number': sequence_number})
            header, payload = await self.__get_response(sequence_number)
            self.logger.debug('Got reply for request number %(sequence_number)s: %(header)s - %(payload)s', {'sequence_number': sequence_number, 'header': header, 'payload': payload})
            return header, payload

    async def __get_response(self, sequence_number):
        # Create a lock for the sequence number
        self.__pending_requests[sequence_number] = asyncio.Condition()
        async with async_timeout.timeout(self.__timeout) as cm:
            # Aquire the lock
            with await self.__pending_requests[sequence_number]:
                try:
                    # wait for the lock to be released
                    await self.__pending_requests[sequence_number].wait()
                    # Once released the worker (streamreader) will have put the packet in the queue
                    header, payload = await self.__reply_queue.get()
                    return header, payload
                except asyncio.CancelledError:
                    if cm.expired:
                        raise asyncio.TimeoutError() from None
                    else:
                        raise
                finally:
                    # Remove the lock
                    del self.__pending_requests[sequence_number]

    def __parse_enumerate_payload(self, payload):
        uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type \
            = unpack_payload(payload, '8s 8s c 3B 3B H B')

        enumeration_type = EnumerationType(enumeration_type)
        
        try:
            device_identifier = DeviceIdentifier(device_identifier)
        except ValueError:
            # Do not assign an enum, leave the int
            pass

        # See https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html#callbacks for details on the payload
        # We will return None for all 'invalid' fields instead of garbage like the Tinkerforge API
        return {'uid': base58decode(uid),   # Stop the base58 encoded nonsense and use the uint32_t id
                'connected_uid': None if (enumeration_type is EnumerationType.disconnected or connected_uid == '0') else base58decode(connected_uid),
                'position':  None if enumeration_type is EnumerationType.disconnected else position,
                'hardware_version': None if enumeration_type is EnumerationType.disconnected else hardware_version,
                'firmware_version': None if enumeration_type is EnumerationType.disconnected else firmware_version,
                'device_id': None if enumeration_type is EnumerationType.disconnected else device_identifier,
                'enumeration_type': enumeration_type,
        }

    async def __read_packet(self):
        try:
            with async_timeout.timeout(self.__timeout):
                data = await self.__reader.read(struct.calcsize(IPConnectionAsync.HEADER_FORMAT))
                packet_size, header = parse_header(data)

                payload = await self.__reader.read(packet_size - struct.calcsize(IPConnectionAsync.HEADER_FORMAT))

                return header, payload
        except asyncio.TimeoutError:
            return None, None

    async def __process_packet(self, header, payload):
        # There are two types of packets:
        # - Broadcasts/Callbacks
        # - Replies
        # We need to treat them differently
        
        # Callbacks first, because most packets will be callbacks,
        # so it is more efficient to do them first
        if header['sequence_number'] is None:
            try:
                # Try to process the callback by handing it to the device
                self.__devices[header['uid']].process_callback(header, payload)
            except (KeyError, UnknownFunctionError):
                # KeyError: raised if the either device is not registered with us or there is no output queue registered
                # UnknownFunctionError is raised by process_callback if there is no local function to process the callback.
                # maybe it is a global callback like an enumeration callback
                try:
                    header['function_id'] = FunctionID(header['function_id'])
                    # This packet must be processed by the ip connection
                    if header['function_id'] is FunctionID.callback_enumerate:
                        payload = self.__parse_enumerate_payload(payload)
                        try:
                            self.logger.debug('Received enumeration: %(header)s - %(payload)s', {'header': header, 'payload': payload})
                            self.__enumeration_queue.put_nowait(payload)
                        except asyncio.QueueFull:
                            # TODO: log a warning, that we are dropping packets
                            self.__self.__enumeration_queue.get_nowait()
                            self.__self.__enumeration_queue.put_nowait(payload)
                except ValueError:
                    # raised if the functionID is unknown. This can happen if there was no device output queue
                    # registered with the callback.
                    pass

        elif header['response_expected']:
            try:
                with await self.__pending_requests[header['sequence_number']]:
                    self.__pending_requests[header['sequence_number']].notify()
                    self.__reply_queue.put_nowait((header, payload,))
                await asyncio.sleep(0)
            except asyncio.QueueFull:
                # TODO: log a warning, that we are dropping packets
                self.__self.__reply_queue.get_nowait()
                self.__self.__reply_queue.put_nowait(payload)
            except KeyError:
                # Drop the packet, because it is not our sequence number
                pass
        else:
            self.logger.info('Unknown packet: %(header)s - %(payload)s', {'header': header, 'payload': payload})

    async def main_loop(self, host, port):
        try:
            self.logger.info('Tinkerforge IP connection connected')
            while 'loop not canceled':
                # Read packets from the socket and process them.
                header, payload = await self.__read_packet()
                if header is not None:
                    await self.__process_packet(header, payload)
        except asyncio.CancelledError:
            self.logger.info('Tinkerforge IP connection closed')
        except Exception as e:
            self.logger.exception("Error while running main_loop")

    async def connect(self, host, port=4223):
        self.__reader, self.__writer = await asyncio.open_connection(host, port, loop=self.__loop)
        self.__main_loop_task = self.__loop.create_task(self.main_loop(host, port))

    async def cancel(self):
        return await self.disconnect()

    async def disconnect(self):
        self.__main_loop_task.cancel()
        await self.__main_loop_task
        self.__reader = None
        # Flush data
        self.__writer.write_eof()
        await self.__writer.drain()
        self.__writer.close()
        self.__writer = None

