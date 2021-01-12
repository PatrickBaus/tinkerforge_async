# -*- coding: utf-8 -*-
import asyncio
import async_timeout
from enum import Enum, Flag
import logging
import struct
import traceback

from .ip_connection_helper import base58decode, pack_payload, unpack_payload
from .devices import DeviceIdentifier, FunctionID

class UnknownFunctionError(Exception):
    pass

class EnumerationType(Enum):
    AVAILABLE = 0
    CONNECTED = 1
    DISCONNECTED = 2

class Flags(Flag):
    OK = 0
    INVALID_PARAMETER = 1
    FUNCTION_NOT_SUPPORTED = 2

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

    @timeout.setter
    def timeout(self, value):
        self.__timeout = abs(int(value))

    @property
    def is_connected(self):
        return self.__writer is not None and not self.__writer.is_closing()

    def __init__(self):
        self.__main_task = None
        self.__reader, self.__writer = None, None
        self.__sequence_number = 0
        self.__timeout = DEFAULT_WAIT_TIMEOUT
        self.__pending_requests = {}

        self.__enumeration_queue = asyncio.Queue(maxsize=20)
        self.__reply_queue = asyncio.Queue(maxsize=20)

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

        return (struct.pack(IPConnectionAsync.HEADER_FORMAT, uid, packet_size, function_id, sequence_number_and_options, Flags.OK.value),
                sequence_number)

    def add_device(self, device):
        self.__logger.debug('Adding device: %(device)s', {'device': device})
        self.__devices[device.uid] = device

    async def enumerate(self):
        """
        Broadcasts an enumerate request. All devices will respond with an enumerate callback.
        Returns: None, it does not support 'response_expected'
        """
        self.__logger.debug('Enumerating Node')
        await self.send_request(
            device=None,
            function_id=FunctionID.ENUMERATE
        )

    async def send_request(self, device, function_id, data=b'', response_expected=False):
        header, sequence_number = self.__create_packet_header(
            payload_size=len(data),
            function_id=function_id.value,
            uid=0 if device is None else device.uid,
            response_expected=response_expected,
        )

        request = header + data

        # If we are waiting for a response, send the request, then pass on the response as a future
        self.__logger.debug('Sending request: %(header)s - %(payload)s', {'header': header, 'payload': data})
        self.__writer.write(request)
        if response_expected:
            self.__logger.debug('Waiting for reply for request number %(sequence_number)s.', {'sequence_number': sequence_number})
            header, payload = await self.__get_response(sequence_number)
            self.__logger.debug('Got reply for request number %(sequence_number)s: %(header)s - %(payload)s', {'sequence_number': sequence_number, 'header': header, 'payload': payload})
            return header, payload

    async def __get_response(self, sequence_number):
        # Create a lock for the sequence number
        self.__pending_requests[sequence_number] = asyncio.Condition()
        async with async_timeout.timeout(self.__timeout) as cm:
            # Aquire the lock
            async with self.__pending_requests[sequence_number]:
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

        try:
            position = int(position)
        except ValueError:
            # It is probably a bricklet, which does have an alphabetic position desciptor
            pass

        # See https://www.tinkerforge.com/en/doc/Software/IPConnection_Python.html#callbacks for details on the payload
        # We will return None for all 'invalid' fields instead of garbage like the Tinkerforge API
        return {'uid': base58decode(uid),   # Stop the base58 encoded nonsense and use the uint32_t id
                'connected_uid': None if (enumeration_type is EnumerationType.DISCONNECTED or connected_uid == '0') else base58decode(connected_uid),
                'position':  None if enumeration_type is EnumerationType.DISCONNECTED else position,
                'hardware_version': None if enumeration_type is EnumerationType.DISCONNECTED else hardware_version,
                'firmware_version': None if enumeration_type is EnumerationType.DISCONNECTED else firmware_version,
                'device_id': None if enumeration_type is EnumerationType.DISCONNECTED else device_identifier,
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
                self.__devices[header['uid']]._process_callback(header, payload)
            except (KeyError, UnknownFunctionError):
                # KeyError: raised if either the device is not registered with us or there is no output queue registered
                # UnknownFunctionError is raised by _process_callback if there is no local function to process the callback.
                # Maybe it is a global callback like an enumeration callback
                try:
                    header['function_id'] = FunctionID(header['function_id'])
                    # This packet must be processed by the ip connection
                    if header['function_id'] is FunctionID.CALLBACK_ENUMERATE:
                        payload = self.__parse_enumerate_payload(payload)
                        self.__logger.debug('Received enumeration: %(header)s - %(payload)s', {'header': header, 'payload': payload})
                        if self.__self.__enumeration_queue.full():
                            # TODO: log a warning, that we are dropping packets
                            self.__self.__enumeration_queue.get_nowait()
                        self.__enumeration_queue.put_nowait(payload)
                except ValueError:
                    # raised if the functionID is unknown. This can happen if there was no device output queue
                    # registered with the callback.
                    pass

        elif header['response_expected']:
            try:
                async with self.__pending_requests[header['sequence_number']]:
                    if self.__reply_queue.full():
                        # TODO: log a warning, that we are dropping packets
                        self.__self.__reply_queue.get_nowait()

                    self.__reply_queue.put_nowait((header, payload,))
                    self.__pending_requests[header['sequence_number']].notify()
                    await asyncio.sleep(0)
            except KeyError:
                # Drop the packet, because it is not our sequence number
                pass
        else:
            self.__logger.info('Unknown packet: %(header)s - %(payload)s', {'header': header, 'payload': payload})

    async def main_loop(self):
        try:
            self.__logger.info('Tinkerforge IP connection connected')
            while 'loop not canceled':
                # Read packets from the socket and process them.
                header, payload = await self.__read_packet()
                if header is not None:
                    await self.__process_packet(header, payload)
        finally:
            self.__main_task = None
            if self.is_connected:
                await self.__close_transport()

    async def connect(self, host, port=4223):
        self.__reader, self.__writer = await asyncio.open_connection(host, port)
        self.__main_task = asyncio.create_task(self.main_loop())

    async def disconnect(self):
       if self.__main_task is not None and not self.__main_task.done():
            self.__main_task.cancel()
            try:
                await self.__main_task
            except asyncio.CancelledError:
                pass

    async def __close_transport(self):
        # Flush data
        try:
            self.__writer.write_eof()
            await self.__writer.drain()
            self.__writer.close()
            await self.__writer.wait_closed()
        except OSError as exc:
            if exc.errno == errno.ENOTCONN:
                pass # Socket is no longer connected, so we can't send the EOF.
            else:
                raise
        finally:
            self.__writer, self.__reader = None, None
            self.__logger.info('Tinkerforge IP connection closed')
