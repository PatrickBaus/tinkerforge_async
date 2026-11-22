"""
Module for the Tinkerforge RS485 Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RS485_Bricklet_Python.html) implemented using
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
from .streams import Chunk, StreamAssembler, read_stream, write_stream, write_stream_short

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    READ = 41
    ERROR_COUNT = 42
    MODBUS_SLAVE_READ_COILS_REQUEST = 43
    MODBUS_MASTER_READ_COILS_RESPONSE = 44
    MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST = 45
    MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE = 46
    MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST = 47
    MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE = 48
    MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST = 49
    MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE = 50
    MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST = 51
    MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE = 52
    MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST = 53
    MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE = 54
    MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST = 55
    MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE = 56
    MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST = 57
    MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE = 58
    FRAME_READABLE = 61


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    WRITE_LOW_LEVEL = 1
    READ_LOW_LEVEL = 2
    ENABLE_READ_CALLBACK = 3
    DISABLE_READ_CALLBACK = 4
    IS_READ_CALLBACK_ENABLED = 5
    SET_RS485_CONFIGURATION = 6
    GET_RS485_CONFIGURATION = 7
    SET_MODBUS_CONFIGURATION = 8
    GET_MODBUS_CONFIGURATION = 9
    SET_MODE = 10
    GET_MODE = 11
    SET_COMMUNICATION_LED_CONFIG = 12
    GET_COMMUNICATION_LED_CONFIG = 13
    SET_ERROR_LED_CONFIG = 14
    GET_ERROR_LED_CONFIG = 15
    SET_BUFFER_CONFIG = 16
    GET_BUFFER_CONFIG = 17
    GET_BUFFER_STATUS = 18
    ENABLE_ERROR_COUNT_CALLBACK = 19
    DISABLE_ERROR_COUNT_CALLBACK = 20
    IS_ERROR_COUNT_CALLBACK_ENABLED = 21
    GET_ERROR_COUNT = 22
    GET_MODBUS_COMMON_ERROR_COUNT = 23
    MODBUS_SLAVE_REPORT_EXCEPTION = 24
    MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL = 25
    MODBUS_MASTER_READ_COILS = 26
    MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL = 27
    MODBUS_MASTER_READ_HOLDING_REGISTERS = 28
    MODBUS_SLAVE_ANSWER_WRITE_SINGLE_COIL_REQUEST = 29
    MODBUS_MASTER_WRITE_SINGLE_COIL = 30
    MODBUS_SLAVE_ANSWER_WRITE_SINGLE_REGISTER_REQUEST = 31
    MODBUS_MASTER_WRITE_SINGLE_REGISTER = 32
    MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_COILS_REQUEST = 33
    MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL = 34
    MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_REGISTERS_REQUEST = 35
    MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL = 36
    MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL = 37
    MODBUS_MASTER_READ_DISCRETE_INPUTS = 38
    MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL = 39
    MODBUS_MASTER_READ_INPUT_REGISTERS = 40
    SET_FRAME_READABLE_CALLBACK_CONFIGURATION = 59
    GET_FRAME_READABLE_CALLBACK_CONFIGURATION = 60


@unique
class Parity(Enum):
    """
    The parity options
    """

    NONE = 0
    ODD = 1
    EVEN = 2


@unique
class Stopbits(Enum):
    """
    The stopbits options
    """

    STOPBITS_1 = 1
    STOPBITS_2 = 2


@unique
class Wordlength(Enum):
    """
    The wordlength options
    """

    WORDLENGTH_5 = 5
    WORDLENGTH_6 = 6
    WORDLENGTH_7 = 7
    WORDLENGTH_8 = 8


@unique
class Duplex(Enum):
    """
    The duplex options
    """

    HALF = 0
    FULL = 1


@unique
class Mode(Enum):
    """
    The mode options
    """

    RS485 = 0
    MODBUS_MASTER_RTU = 1
    MODBUS_SLAVE_RTU = 2


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
    SHOW_ERROR = 3


@unique
class ExceptionCode(Enum):
    """
    The exception code options
    """

    TIMEOUT = -1
    SUCCESS = 0
    ILLEGAL_FUNCTION = 1
    ILLEGAL_DATA_ADDRESS = 2
    ILLEGAL_DATA_VALUE = 3
    SLAVE_DEVICE_FAILURE = 4
    ACKNOWLEDGE = 5
    SLAVE_DEVICE_BUSY = 6
    MEMORY_PARITY_ERROR = 8
    GATEWAY_PATH_UNAVAILABLE = 10
    GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND = 11


class Read(NamedTuple):
    message_length: int
    message_chunk_offset: int
    message_chunk_data: tuple[str, ...]


class GetRS485Configuration(NamedTuple):
    baudrate: int
    parity: Parity
    stopbits: Stopbits
    wordlength: Wordlength
    duplex: Duplex


class GetModbusConfiguration(NamedTuple):
    slave_address: int
    master_request_timeout: Decimal


class GetBufferConfig(NamedTuple):
    send_buffer_size: int
    receive_buffer_size: int


class GetBufferStatus(NamedTuple):
    send_buffer_used: int
    receive_buffer_used: int


class GetErrorCount(NamedTuple):
    overrun_error_count: int
    parity_error_count: int


class GetModbusCommonErrorCount(NamedTuple):
    timeout_error_count: int
    checksum_error_count: int
    frame_too_big_error_count: int
    illegal_function_error_count: int
    illegal_data_address_error_count: int
    illegal_data_value_error_count: int
    slave_device_failure_error_count: int


class ModbusSlaveReadCoilsRequestEvent(NamedTuple):
    request_id: int
    starting_address: int
    count_: int


class ModbusSlaveReadHoldingRegistersRequestEvent(NamedTuple):
    request_id: int
    starting_address: int
    count_: int


class ModbusSlaveWriteSingleCoilRequestEvent(NamedTuple):
    request_id: int
    coil_address: int
    coil_value: bool


class ModbusMasterWriteSingleCoilResponseEvent(NamedTuple):
    request_id: int
    exception_code: ExceptionCode


class ModbusSlaveWriteSingleRegisterRequestEvent(NamedTuple):
    request_id: int
    register_address: int
    register_value: int


class ModbusMasterWriteSingleRegisterResponseEvent(NamedTuple):
    request_id: int
    exception_code: ExceptionCode


class ModbusMasterWriteMultipleCoilsResponseEvent(NamedTuple):
    request_id: int
    exception_code: ExceptionCode


class ModbusMasterWriteMultipleRegistersResponseEvent(NamedTuple):
    request_id: int
    exception_code: ExceptionCode


class ModbusSlaveReadDiscreteInputsRequestEvent(NamedTuple):
    request_id: int
    starting_address: int
    count_: int


class ModbusSlaveReadInputRegistersRequestEvent(NamedTuple):
    request_id: int
    starting_address: int
    count_: int


class ModbusMasterReadCoilsResponseEvent(NamedTuple):
    request_id: int
    exception_code: ExceptionCode
    coils: tuple[bool, ...]


class ModbusMasterReadHoldingRegistersResponseEvent(NamedTuple):
    request_id: int
    exception_code: ExceptionCode
    holding_registers: tuple[int, ...]


class ModbusSlaveWriteMultipleCoilsRequestEvent(NamedTuple):
    request_id: int
    starting_address: int
    coils: tuple[bool, ...]


class ModbusSlaveWriteMultipleRegistersRequestEvent(NamedTuple):
    request_id: int
    starting_address: int
    registers: tuple[int, ...]


class ModbusMasterReadDiscreteInputsResponseEvent(NamedTuple):
    request_id: int
    exception_code: ExceptionCode
    discrete_inputs: tuple[bool, ...]


class ModbusMasterReadInputRegistersResponseEvent(NamedTuple):
    request_id: int
    exception_code: ExceptionCode
    input_registers: tuple[int, ...]


class BrickletRS485(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Communicates with RS485/Modbus devices with full- or half-duplex
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_RS485
    DEVICE_DISPLAY_NAME = "RS485 Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    Parity: TypeAlias = Parity
    Stopbits: TypeAlias = Stopbits
    Wordlength: TypeAlias = Wordlength
    Duplex: TypeAlias = Duplex
    Mode: TypeAlias = Mode
    CommunicationLEDConfig: TypeAlias = CommunicationLEDConfig
    ErrorLEDConfig: TypeAlias = ErrorLEDConfig
    ExceptionCode: TypeAlias = ExceptionCode

    CALLBACK_FORMATS = {
        CallbackID.READ: "H H 60c",
        CallbackID.ERROR_COUNT: "I I",
        CallbackID.MODBUS_SLAVE_READ_COILS_REQUEST: "B I H",
        CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE: "B b H H 464!",
        CallbackID.MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST: "B I H",
        CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE: "B b H H 29H",
        CallbackID.MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST: "B I !",
        CallbackID.MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE: "B b",
        CallbackID.MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST: "B I H",
        CallbackID.MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE: "B b",
        CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST: "B I H H 440!",
        CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE: "B b",
        CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST: "B I H H 27H",
        CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE: "B b",
        CallbackID.MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST: "B I H",
        CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE: "B b H H 464!",
        CallbackID.MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST: "B I H",
        CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE: "B b H H 29H",
        CallbackID.FRAME_READABLE: "H",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.ERROR_COUNT,)),
        Channel(1, callbacks=(CallbackID.MODBUS_SLAVE_READ_COILS_REQUEST,)),
        Channel(2, callbacks=(CallbackID.MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST,)),
        Channel(3, callbacks=(CallbackID.MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST,)),
        Channel(4, callbacks=(CallbackID.MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE,)),
        Channel(5, callbacks=(CallbackID.MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST,)),
        Channel(6, callbacks=(CallbackID.MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE,)),
        Channel(7, callbacks=(CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE,)),
        Channel(8, callbacks=(CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE,)),
        Channel(9, callbacks=(CallbackID.MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST,)),
        Channel(10, callbacks=(CallbackID.MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST,)),
        Channel(11, callbacks=(CallbackID.FRAME_READABLE,)),
        Channel(12, callbacks=(CallbackID.READ,)),
        Channel(13, callbacks=(CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE,)),
        Channel(14, callbacks=(CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE,)),
        Channel(15, callbacks=(CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST,)),
        Channel(16, callbacks=(CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST,)),
        Channel(17, callbacks=(CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE,)),
        Channel(18, callbacks=(CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE,)),
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
        self._stream_assemblers = {
            CallbackID.READ: StreamAssembler(),
            CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE: StreamAssembler(),
            CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE: StreamAssembler(),
            CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST: StreamAssembler(),
            CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST: StreamAssembler(),
            CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE: StreamAssembler(),
            CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE: StreamAssembler(),
        }

    async def write_low_level(
        self, message_length: int, message_chunk_offset: int, message_chunk_data: str | Sequence[str]
    ) -> int:
        """
        Writes characters to the RS485 interface. The characters can be binary data,
        ASCII or similar is not necessary.

        The return value is the number of characters that were written.

        See :func:`set_rs485_configuration` for configuration possibilities
        regarding baudrate, parity and so on.
        """
        message_length = int(message_length)
        check_range("message_length", message_length, 0, 65535)
        message_chunk_offset = int(message_chunk_offset)
        check_range("message_chunk_offset", message_chunk_offset, 0, 65535)
        check_length("message_chunk_data", message_chunk_data, 60)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_LOW_LEVEL,
            data=pack_payload((message_length, message_chunk_offset, list(message_chunk_data)), "H H 60c"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def write(self, message: str) -> int:
        """
        Writes characters to the RS485 interface. The characters can be binary data,
        ASCII or similar is not necessary.

        The return value is the number of characters that were written.

        See :func:`set_rs485_configuration` for configuration possibilities
        regarding baudrate, parity and so on.

        This function transfers the complete message stream and calls :func:`write_low_level` as often as necessary.
        Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> tuple[int, Any]:
            result = await self.write_low_level(length, offset, chunk)
            return result, result

        async with self._stream_lock:
            written, _ = await write_stream_short(
                send_chunk, list(message), name="message", chunk_size=60, padding="\0", max_length=65535
            )
        return written

    async def read_low_level(self, length: int) -> Read:
        """
        Returns up to *length* characters from receive buffer.

        Instead of polling with this function, you can also use
        callbacks. But note that this function will return available
        data only when the read callback is disabled.
        See :func:`enable_read_callback` and :attr:`CallbackID.READ` callback.
        """
        length = int(length)
        check_range("length", length, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_LOW_LEVEL,
            data=pack_payload((length,), "H"),
            response_expected=True,
        )
        message_length, message_chunk_offset, message_chunk_data = unpack_payload(payload, "H H 60c")
        return Read(message_length, message_chunk_offset, tuple(message_chunk_data))

    async def read(self, length: int) -> str:
        """
        Returns up to *length* characters from receive buffer.

        Instead of polling with this function, you can also use
        callbacks. But note that this function will return available
        data only when the read callback is disabled.
        See :func:`enable_read_callback` and :attr:`CallbackID.READ` callback.

        This function transfers the complete message stream and calls :func:`read_low_level` as often as necessary.
        Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.read_low_level(length)
            return Chunk(result.message_length, result.message_chunk_offset, result.message_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="message", chunk_size=60)
        return "".join(data)

    async def enable_read_callback(self, response_expected: bool = True) -> None:
        """
        Enables the :attr:`CallbackID.READ` callback. This will disable the :attr:`CallbackID.FRAME_READABLE` callback.

        By default the callback is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_READ_CALLBACK, response_expected=response_expected
        )

    async def disable_read_callback(self, response_expected: bool = True) -> None:
        """
        Disables the :attr:`CallbackID.READ` callback.

        By default the callback is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_READ_CALLBACK, response_expected=response_expected
        )

    async def is_read_callback_enabled(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.READ` callback is enabled,
        *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_READ_CALLBACK_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_rs485_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        baudrate: int = 115200,
        parity: Parity | int = Parity.NONE,
        stopbits: Stopbits | int = Stopbits.STOPBITS_1,
        wordlength: Wordlength | int = Wordlength.WORDLENGTH_8,
        duplex: Duplex | int = Duplex.HALF,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration for the RS485 communication.
        """
        baudrate = int(baudrate)
        check_range("baudrate", baudrate, 100, 2000000)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RS485_CONFIGURATION,
            data=pack_payload(
                (
                    baudrate,
                    Parity(parity).value,
                    Stopbits(stopbits).value,
                    Wordlength(wordlength).value,
                    Duplex(duplex).value,
                ),
                "I B B B B",
            ),
            response_expected=response_expected,
        )

    async def get_rs485_configuration(self) -> GetRS485Configuration:
        """
        Returns the configuration as set by :func:`set_rs485_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RS485_CONFIGURATION, response_expected=True
        )
        baudrate, parity, stopbits, wordlength, duplex = unpack_payload(payload, "I B B B B")
        return GetRS485Configuration(
            baudrate, Parity(parity), Stopbits(stopbits), Wordlength(wordlength), Duplex(duplex)
        )

    async def set_modbus_configuration(
        self, slave_address: int = 1, master_request_timeout: Duration = 1, response_expected: bool = True
    ) -> None:
        """
        Sets the configuration for the RS485 Modbus communication. Available options:

        * Slave Address: Address to be used as the Modbus slave address in Modbus slave mode. Valid Modbus slave address
          range is 1 to 247.
        * Master Request Timeout: Specifies how long the master should wait for a response from a slave when in Modbus
          master mode.

        Units: master_request_timeout in s.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 1, 247)
        master_request_timeout_raw = seconds_to_ms(master_request_timeout)
        check_range("master_request_timeout", master_request_timeout_raw, 0, 4294967295, master_request_timeout)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MODBUS_CONFIGURATION,
            data=pack_payload((slave_address, master_request_timeout_raw), "B I"),
            response_expected=response_expected,
        )

    async def get_modbus_configuration(self) -> GetModbusConfiguration:
        """
        Returns the configuration as set by :func:`set_modbus_configuration`.

        Units: master_request_timeout in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MODBUS_CONFIGURATION, response_expected=True
        )
        slave_address, master_request_timeout = unpack_payload(payload, "B I")
        return GetModbusConfiguration(slave_address, ms_to_seconds(master_request_timeout))

    async def set_mode(self, mode: Mode | int = Mode.RS485, response_expected: bool = True) -> None:
        """
        Sets the mode of the Bricklet in which it operates. Available options are

        * RS485,
        * Modbus Master RTU and
        * Modbus Slave RTU.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MODE,
            data=pack_payload((Mode(mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_mode(self) -> Mode:
        """
        Returns the configuration as set by :func:`set_mode`.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_MODE, response_expected=True)
        return Mode(unpack_payload(payload, "B"))

    async def set_communication_led_config(
        self,
        config: CommunicationLEDConfig | int = CommunicationLEDConfig.SHOW_COMMUNICATION,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the communication LED configuration. By default the LED shows RS485
        communication traffic by flickering.

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
        self, config: ErrorLEDConfig | int = ErrorLEDConfig.SHOW_ERROR, response_expected: bool = True
    ) -> None:
        """
        Sets the error LED configuration.

        By default the error LED turns on if there is any error (see :attr:`CallbackID.ERROR_COUNT`
        callback). If you call this function with the SHOW ERROR option again, the LED
        will turn off until the next error occurs.

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

    async def set_buffer_config(
        self, send_buffer_size: int = 5120, receive_buffer_size: int = 5120, response_expected: bool = True
    ) -> None:
        """
        Sets the send and receive buffer size in byte. In sum there is
        10240 byte (10KiB) buffer available and the minimum buffer size
        is 1024 byte (1KiB) for both.

        The current buffer content is lost if this function is called.

        The send buffer holds data that was given by :func:`write` and
        could not be written yet. The receive buffer holds data that is
        received through RS485 but could not yet be send to the
        user, either by :func:`read` or through :attr:`CallbackID.READ` callback.
        """
        send_buffer_size = int(send_buffer_size)
        check_range("send_buffer_size", send_buffer_size, 1024, 9216)
        receive_buffer_size = int(receive_buffer_size)
        check_range("receive_buffer_size", receive_buffer_size, 1024, 9216)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BUFFER_CONFIG,
            data=pack_payload((send_buffer_size, receive_buffer_size), "H H"),
            response_expected=response_expected,
        )

    async def get_buffer_config(self) -> GetBufferConfig:
        """
        Returns the buffer configuration as set by :func:`set_buffer_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BUFFER_CONFIG, response_expected=True
        )
        send_buffer_size, receive_buffer_size = unpack_payload(payload, "H H")
        return GetBufferConfig(send_buffer_size, receive_buffer_size)

    async def get_buffer_status(self) -> GetBufferStatus:
        """
        Returns the currently used bytes for the send and received buffer.

        See :func:`set_buffer_config` for buffer size configuration.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BUFFER_STATUS, response_expected=True
        )
        send_buffer_used, receive_buffer_used = unpack_payload(payload, "H H")
        return GetBufferStatus(send_buffer_used, receive_buffer_used)

    async def enable_error_count_callback(self, response_expected: bool = True) -> None:
        """
        Enables the :attr:`CallbackID.ERROR_COUNT` callback.

        By default the callback is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_ERROR_COUNT_CALLBACK, response_expected=response_expected
        )

    async def disable_error_count_callback(self, response_expected: bool = True) -> None:
        """
        Disables the :attr:`CallbackID.ERROR_COUNT` callback.

        By default the callback is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_ERROR_COUNT_CALLBACK, response_expected=response_expected
        )

    async def is_error_count_callback_enabled(self) -> bool:
        """
        Returns *true* if the :attr:`CallbackID.ERROR_COUNT` callback is enabled,
        *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_ERROR_COUNT_CALLBACK_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def get_error_count(self) -> GetErrorCount:
        """
        Returns the current number of overrun and parity errors.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_COUNT, response_expected=True
        )
        overrun_error_count, parity_error_count = unpack_payload(payload, "I I")
        return GetErrorCount(overrun_error_count, parity_error_count)

    async def get_modbus_common_error_count(self) -> GetModbusCommonErrorCount:
        """
        Returns the current number of errors occurred in Modbus mode.

        * Timeout Error Count: Number of timeouts occurred.
        * Checksum Error Count: Number of failures due to Modbus frame CRC16 checksum mismatch.
        * Frame Too Big Error Count: Number of times frames were rejected because they exceeded maximum Modbus frame
          size which is 256 bytes.
        * Illegal Function Error Count: Number of errors when an unimplemented or illegal function is requested. This
          corresponds to Modbus exception code 1.
        * Illegal Data Address Error Count: Number of errors due to invalid data address. This corresponds to Modbus
          exception code 2.
        * Illegal Data Value Error Count: Number of errors due to invalid data value. This corresponds to Modbus
          exception code 3.
        * Slave Device Failure Error Count: Number of errors occurred on the slave device which were unrecoverable. This
          corresponds to Modbus exception code 4.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MODBUS_COMMON_ERROR_COUNT, response_expected=True
        )
        (
            timeout_error_count,
            checksum_error_count,
            frame_too_big_error_count,
            illegal_function_error_count,
            illegal_data_address_error_count,
            illegal_data_value_error_count,
            slave_device_failure_error_count,
        ) = unpack_payload(payload, "I I I I I I I")
        return GetModbusCommonErrorCount(
            timeout_error_count,
            checksum_error_count,
            frame_too_big_error_count,
            illegal_function_error_count,
            illegal_data_address_error_count,
            illegal_data_value_error_count,
            slave_device_failure_error_count,
        )

    async def modbus_slave_report_exception(
        self, request_id: int, exception_code: ExceptionCode | int, response_expected: bool = True
    ) -> None:
        """
        In Modbus slave mode this function can be used to report a Modbus exception for
        a Modbus master request.

        * Request ID: Request ID of the request received by the slave.
        * Exception Code: Modbus exception code to report to the Modbus master.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_REPORT_EXCEPTION,
            data=pack_payload((request_id, ExceptionCode(exception_code).value), "B b"),
            response_expected=response_expected,
        )

    async def modbus_slave_answer_read_coils_request_low_level(
        self,
        request_id: int,
        coils_length: int,
        coils_chunk_offset: int,
        coils_chunk_data: Sequence[bool],
        response_expected: bool = True,
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        read coils.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Coils: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_READ_COILS_REQUEST` callback
        with the Request ID as provided by the argument of the callback.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        coils_length = int(coils_length)
        check_range("coils_length", coils_length, 1, 2000)
        coils_chunk_offset = int(coils_chunk_offset)
        check_range("coils_chunk_offset", coils_chunk_offset, 0, 65535)
        check_length("coils_chunk_data", coils_chunk_data, 472)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL,
            data=pack_payload(
                (request_id, coils_length, coils_chunk_offset, [bool(item) for item in coils_chunk_data]), "B H H 472!"
            ),
            response_expected=response_expected,
        )

    async def modbus_slave_answer_read_coils_request(self, request_id: int, coils: Sequence[bool]) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        read coils.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Coils: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_READ_COILS_REQUEST` callback
        with the Request ID as provided by the argument of the callback.

        This function transfers the complete coils stream and calls
        :func:`modbus_slave_answer_read_coils_request_low_level` as often as necessary. Concurrent transfers of the
        stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.modbus_slave_answer_read_coils_request_low_level(request_id, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk,
                [bool(item) for item in coils],
                name="coils",
                chunk_size=472,
                padding=False,
                max_length=65535,
            )

    async def modbus_master_read_coils(self, slave_address: int, starting_address: int, count: int) -> int:
        """
        In Modbus master mode this function can be used to read coils from a slave. This
        function creates a Modbus function code 1 request.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Number of the first coil to read. For backwards compatibility reasons this parameter is
          called Starting Address. It is not an address, but instead a coil number in the range of 1 to 65536.
        * Count: Number of coils to read.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :attr:`CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be
        matched with the Request ID returned from this function to verify that the callback
        is indeed for a particular request.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 0, 247)
        starting_address = int(starting_address)
        check_range("starting_address", starting_address, 1, 65536)
        count = int(count)
        check_range("count", count, 1, 2000)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_MASTER_READ_COILS,
            data=pack_payload((slave_address, starting_address, count), "B I H"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def modbus_slave_answer_read_holding_registers_request_low_level(
        self,
        request_id: int,
        holding_registers_length: int,
        holding_registers_chunk_offset: int,
        holding_registers_chunk_data: Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        read holding registers.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Holding Registers: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST`
        callback with the Request ID as provided by the argument of the callback.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        holding_registers_length = int(holding_registers_length)
        check_range("holding_registers_length", holding_registers_length, 1, 125)
        holding_registers_chunk_offset = int(holding_registers_chunk_offset)
        check_range("holding_registers_chunk_offset", holding_registers_chunk_offset, 0, 65535)
        check_length("holding_registers_chunk_data", holding_registers_chunk_data, 29)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL,
            data=pack_payload(
                (
                    request_id,
                    holding_registers_length,
                    holding_registers_chunk_offset,
                    list(map(int, holding_registers_chunk_data)),
                ),
                "B H H 29H",
            ),
            response_expected=response_expected,
        )

    async def modbus_slave_answer_read_holding_registers_request(
        self, request_id: int, holding_registers: Sequence[int]
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        read holding registers.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Holding Registers: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST`
        callback with the Request ID as provided by the argument of the callback.

        This function transfers the complete holding_registers stream and calls
        :func:`modbus_slave_answer_read_holding_registers_request_low_level` as often as necessary. Concurrent transfers
        of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.modbus_slave_answer_read_holding_registers_request_low_level(request_id, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk,
                [int(item) for item in holding_registers],
                name="holding_registers",
                chunk_size=29,
                padding=0,
                max_length=65535,
            )

    async def modbus_master_read_holding_registers(self, slave_address: int, starting_address: int, count: int) -> int:
        """
        In Modbus master mode this function can be used to read holding registers from a slave.
        This function creates a Modbus function code 3 request.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Number of the first holding register to read. For backwards compatibility reasons this
          parameter is called Starting Address. It is not an address, but instead a holding register number in the range
          of 1 to 65536. The prefix digit 4 (for holding register) is implicit and must be omitted.
        * Count: Number of holding registers to read.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the
        :attr:`CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 0, 247)
        starting_address = int(starting_address)
        check_range("starting_address", starting_address, 1, 65536)
        count = int(count)
        check_range("count", count, 1, 125)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_MASTER_READ_HOLDING_REGISTERS,
            data=pack_payload((slave_address, starting_address, count), "B I H"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def modbus_slave_answer_write_single_coil_request(
        self, request_id: int, response_expected: bool = True
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        write a single coil.

        * Request ID: Request ID of the corresponding request that is being answered.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST`
        callback with the Request ID as provided by the arguments of the callback.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_ANSWER_WRITE_SINGLE_COIL_REQUEST,
            data=pack_payload((request_id,), "B"),
            response_expected=response_expected,
        )

    async def modbus_master_write_single_coil(self, slave_address: int, coil_address: int, coil_value: bool) -> int:
        """
        In Modbus master mode this function can be used to write a single coil of a slave.
        This function creates a Modbus function code 5 request.

        * Slave Address: Address of the target Modbus slave.
        * Coil Address: Number of the coil to be written. For backwards compatibility reasons, this parameter is called
          Starting Address. It is not an address, but instead a coil number in the range of 1 to 65536.
        * Coil Value: Value to be written.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the :attr:`CallbackID.MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 0, 247)
        coil_address = int(coil_address)
        check_range("coil_address", coil_address, 1, 65536)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_MASTER_WRITE_SINGLE_COIL,
            data=pack_payload((slave_address, coil_address, bool(coil_value)), "B I !"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def modbus_slave_answer_write_single_register_request(
        self, request_id: int, response_expected: bool = True
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        write a single register.

        * Request ID: Request ID of the corresponding request that is being answered.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST`
        callback with the Request ID, Register Address and Register Value as provided by
        the arguments of the callback.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_ANSWER_WRITE_SINGLE_REGISTER_REQUEST,
            data=pack_payload((request_id,), "B"),
            response_expected=response_expected,
        )

    async def modbus_master_write_single_register(
        self, slave_address: int, register_address: int, register_value: int
    ) -> int:
        """
        In Modbus master mode this function can be used to write a single holding register of a
        slave. This function creates a Modbus function code 6 request.

        * Slave Address: Address of the target Modbus slave.
        * Register Address: Number of the holding register to be written. For backwards compatibility reasons, this
          parameter is called Starting Address. It is not an address, but instead a holding register number in the range
          of 1 to 65536. The prefix digit 4 (for holding register) is implicit and must be omitted.
        * Register Value: Value to be written.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the
        :attr:`CallbackID.MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 0, 247)
        register_address = int(register_address)
        check_range("register_address", register_address, 1, 65536)
        register_value = int(register_value)
        check_range("register_value", register_value, 0, 65535)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_MASTER_WRITE_SINGLE_REGISTER,
            data=pack_payload((slave_address, register_address, register_value), "B I H"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def modbus_slave_answer_write_multiple_coils_request(
        self, request_id: int, response_expected: bool = True
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        write multiple coils.

        * Request ID: Request ID of the corresponding request that is being answered.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST`
        callback with the Request ID of the callback.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_COILS_REQUEST,
            data=pack_payload((request_id,), "B"),
            response_expected=response_expected,
        )

    async def modbus_master_write_multiple_coils_low_level(
        self,
        slave_address: int,
        starting_address: int,
        coils_length: int,
        coils_chunk_offset: int,
        coils_chunk_data: Sequence[bool],
    ) -> int:
        """
        In Modbus master mode this function can be used to write multiple coils of a slave.
        This function creates a Modbus function code 15 request.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Number of the first coil to write. For backwards compatibility reasons, this parameter is
          called Starting Address.It is not an address, but instead a coil number in the range of 1 to 65536.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the
        :attr:`CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 0, 247)
        starting_address = int(starting_address)
        check_range("starting_address", starting_address, 1, 65536)
        coils_length = int(coils_length)
        check_range("coils_length", coils_length, 1, 1968)
        coils_chunk_offset = int(coils_chunk_offset)
        check_range("coils_chunk_offset", coils_chunk_offset, 0, 65535)
        check_length("coils_chunk_data", coils_chunk_data, 440)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL,
            data=pack_payload(
                (
                    slave_address,
                    starting_address,
                    coils_length,
                    coils_chunk_offset,
                    [bool(item) for item in coils_chunk_data],
                ),
                "B I H H 440!",
            ),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def modbus_master_write_multiple_coils(
        self, slave_address: int, starting_address: int, coils: Sequence[bool]
    ) -> int:
        """
        In Modbus master mode this function can be used to write multiple coils of a slave.
        This function creates a Modbus function code 15 request.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Number of the first coil to write. For backwards compatibility reasons, this parameter is
          called Starting Address.It is not an address, but instead a coil number in the range of 1 to 65536.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the
        :attr:`CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.

        This function transfers the complete coils stream and calls :func:`modbus_master_write_multiple_coils_low_level`
        as often as necessary. Concurrent transfers of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> int:
            return await self.modbus_master_write_multiple_coils_low_level(
                slave_address, starting_address, length, offset, chunk
            )

        async with self._stream_lock:
            result = await write_stream(
                send_chunk,
                [bool(item) for item in coils],
                name="coils",
                chunk_size=440,
                padding=False,
                max_length=65535,
            )
        return result

    async def modbus_slave_answer_write_multiple_registers_request(
        self, request_id: int, response_expected: bool = True
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        write multiple registers.

        * Request ID: Request ID of the corresponding request that is being answered.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST`
        callback with the Request ID of the callback.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_REGISTERS_REQUEST,
            data=pack_payload((request_id,), "B"),
            response_expected=response_expected,
        )

    async def modbus_master_write_multiple_registers_low_level(
        self,
        slave_address: int,
        starting_address: int,
        registers_length: int,
        registers_chunk_offset: int,
        registers_chunk_data: Sequence[int],
    ) -> int:
        """
        In Modbus master mode this function can be used to write multiple registers of a slave.
        This function creates a Modbus function code 16 request.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Number of the first holding register to write. For backwards compatibility reasons, this
          parameter is called Starting Address. It is not an address, but instead a holding register number in the range
          of 1 to 65536. The prefix digit 4 (for holding register) is implicit and must be omitted.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the
        :attr:`CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 0, 247)
        starting_address = int(starting_address)
        check_range("starting_address", starting_address, 1, 65536)
        registers_length = int(registers_length)
        check_range("registers_length", registers_length, 1, 123)
        registers_chunk_offset = int(registers_chunk_offset)
        check_range("registers_chunk_offset", registers_chunk_offset, 0, 65535)
        check_length("registers_chunk_data", registers_chunk_data, 27)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL,
            data=pack_payload(
                (
                    slave_address,
                    starting_address,
                    registers_length,
                    registers_chunk_offset,
                    list(map(int, registers_chunk_data)),
                ),
                "B I H H 27H",
            ),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def modbus_master_write_multiple_registers(
        self, slave_address: int, starting_address: int, registers: Sequence[int]
    ) -> int:
        """
        In Modbus master mode this function can be used to write multiple registers of a slave.
        This function creates a Modbus function code 16 request.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Number of the first holding register to write. For backwards compatibility reasons, this
          parameter is called Starting Address. It is not an address, but instead a holding register number in the range
          of 1 to 65536. The prefix digit 4 (for holding register) is implicit and must be omitted.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the
        :attr:`CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.

        This function transfers the complete registers stream and calls
        :func:`modbus_master_write_multiple_registers_low_level` as often as necessary. Concurrent transfers of the
        stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> int:
            return await self.modbus_master_write_multiple_registers_low_level(
                slave_address, starting_address, length, offset, chunk
            )

        async with self._stream_lock:
            result = await write_stream(
                send_chunk,
                [int(item) for item in registers],
                name="registers",
                chunk_size=27,
                padding=0,
                max_length=65535,
            )
        return result

    async def modbus_slave_answer_read_discrete_inputs_request_low_level(
        self,
        request_id: int,
        discrete_inputs_length: int,
        discrete_inputs_chunk_offset: int,
        discrete_inputs_chunk_data: Sequence[bool],
        response_expected: bool = True,
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        read discrete inputs.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Discrete Inputs: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST`
        callback with the Request ID as provided by the argument of the callback.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        discrete_inputs_length = int(discrete_inputs_length)
        check_range("discrete_inputs_length", discrete_inputs_length, 1, 2000)
        discrete_inputs_chunk_offset = int(discrete_inputs_chunk_offset)
        check_range("discrete_inputs_chunk_offset", discrete_inputs_chunk_offset, 0, 65535)
        check_length("discrete_inputs_chunk_data", discrete_inputs_chunk_data, 472)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL,
            data=pack_payload(
                (
                    request_id,
                    discrete_inputs_length,
                    discrete_inputs_chunk_offset,
                    [bool(item) for item in discrete_inputs_chunk_data],
                ),
                "B H H 472!",
            ),
            response_expected=response_expected,
        )

    async def modbus_slave_answer_read_discrete_inputs_request(
        self, request_id: int, discrete_inputs: Sequence[bool]
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        read discrete inputs.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Discrete Inputs: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST`
        callback with the Request ID as provided by the argument of the callback.

        This function transfers the complete discrete_inputs stream and calls
        :func:`modbus_slave_answer_read_discrete_inputs_request_low_level` as often as necessary. Concurrent transfers
        of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.modbus_slave_answer_read_discrete_inputs_request_low_level(request_id, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk,
                [bool(item) for item in discrete_inputs],
                name="discrete_inputs",
                chunk_size=472,
                padding=False,
                max_length=65535,
            )

    async def modbus_master_read_discrete_inputs(self, slave_address: int, starting_address: int, count: int) -> int:
        """
        In Modbus master mode this function can be used to read discrete inputs from a slave.
        This function creates a Modbus function code 2 request.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Number of the first discrete input to read. For backwards compatibility reasons, this
          parameter is called Starting Address. It is not an address, but instead a discrete input number in the range
          of 1 to 65536. The prefix digit 1 (for discrete input) is implicit and must be omitted.
        * Count: Number of discrete inputs to read.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the
        :attr:`CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 0, 247)
        starting_address = int(starting_address)
        check_range("starting_address", starting_address, 1, 65536)
        count = int(count)
        check_range("count", count, 1, 2000)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_MASTER_READ_DISCRETE_INPUTS,
            data=pack_payload((slave_address, starting_address, count), "B I H"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def modbus_slave_answer_read_input_registers_request_low_level(
        self,
        request_id: int,
        input_registers_length: int,
        input_registers_chunk_offset: int,
        input_registers_chunk_data: Sequence[int],
        response_expected: bool = True,
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        read input registers.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Input Registers: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST` callback
        with the Request ID as provided by the argument of the callback.
        """
        request_id = int(request_id)
        check_range("request_id", request_id, 0, 255)
        input_registers_length = int(input_registers_length)
        check_range("input_registers_length", input_registers_length, 1, 125)
        input_registers_chunk_offset = int(input_registers_chunk_offset)
        check_range("input_registers_chunk_offset", input_registers_chunk_offset, 0, 65535)
        check_length("input_registers_chunk_data", input_registers_chunk_data, 29)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL,
            data=pack_payload(
                (
                    request_id,
                    input_registers_length,
                    input_registers_chunk_offset,
                    list(map(int, input_registers_chunk_data)),
                ),
                "B H H 29H",
            ),
            response_expected=response_expected,
        )

    async def modbus_slave_answer_read_input_registers_request(
        self, request_id: int, input_registers: Sequence[int]
    ) -> None:
        """
        In Modbus slave mode this function can be used to answer a master request to
        read input registers.

        * Request ID: Request ID of the corresponding request that is being answered.
        * Input Registers: Data that is to be sent to the Modbus master for the corresponding request.

        This function must be called from the :attr:`CallbackID.MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST` callback
        with the Request ID as provided by the argument of the callback.

        This function transfers the complete input_registers stream and calls
        :func:`modbus_slave_answer_read_input_registers_request_low_level` as often as necessary. Concurrent transfers
        of the stream are serialized.
        """

        async def send_chunk(length: int, offset: int, chunk: list[Any]) -> None:
            await self.modbus_slave_answer_read_input_registers_request_low_level(request_id, length, offset, chunk)

        async with self._stream_lock:
            await write_stream(
                send_chunk,
                [int(item) for item in input_registers],
                name="input_registers",
                chunk_size=29,
                padding=0,
                max_length=65535,
            )

    async def modbus_master_read_input_registers(self, slave_address: int, starting_address: int, count: int) -> int:
        """
        In Modbus master mode this function can be used to read input registers from a slave.
        This function creates a Modbus function code 4 request.

        * Slave Address: Address of the target Modbus slave.
        * Starting Address: Number of the first input register to read. For backwards compatibility reasons, this
          parameter is called Starting Address. It is not an address, but instead an input register number in the range
          of 1 to 65536. The prefix digit 3 (for input register) is implicit and must be omitted.
        * Count: Number of input registers to read.

        Upon success the function will return a non-zero request ID which will represent
        the current request initiated by the Modbus master. In case of failure the returned
        request ID will be 0.

        When successful this function will also invoke the
        :attr:`CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE`
        callback. In this callback the Request ID provided by the callback argument must be matched
        with the Request ID returned from this function to verify that the callback is indeed for a
        particular request.
        """
        slave_address = int(slave_address)
        check_range("slave_address", slave_address, 0, 247)
        starting_address = int(starting_address)
        check_range("starting_address", starting_address, 1, 65536)
        count = int(count)
        check_range("count", count, 1, 125)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.MODBUS_MASTER_READ_INPUT_REGISTERS,
            data=pack_payload((slave_address, starting_address, count), "B I H"),
            response_expected=True,
        )
        return unpack_payload(payload, "B")

    async def set_frame_readable_callback_configuration(
        self, frame_size: int = 0, response_expected: bool = True
    ) -> None:
        """
        Configures the :attr:`CallbackID.FRAME_READABLE` callback. The frame size is the number of bytes, that have to
        be readable to trigger the callback.
        A frame size of 0 disables the callback. A frame size greater than 0 enables the callback and disables the
        :attr:`CallbackID.READ` callback.

        By default the callback is disabled.

        .. versionadded:: 2.0.5 (Firmware)
        """
        frame_size = int(frame_size)
        check_range("frame_size", frame_size, 0, 9216)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
            data=pack_payload((frame_size,), "H"),
            response_expected=response_expected,
        )

    async def get_frame_readable_callback_configuration(self) -> int:
        """
        Returns the callback configuration as set by :func:`set_frame_readable_callback_configuration`.

        .. versionadded:: 2.0.5 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "H")

    def _convert_callback(  # pylint: disable=too-many-return-statements,too-many-branches,too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.ERROR_COUNT:
            overrun_error_count, parity_error_count = value
            return 0, GetErrorCount(overrun_error_count, parity_error_count)
        if callback_id is CallbackID.MODBUS_SLAVE_READ_COILS_REQUEST:
            request_id, starting_address, count = value
            return 1, ModbusSlaveReadCoilsRequestEvent(request_id, starting_address, count)
        if callback_id is CallbackID.MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST:
            request_id, starting_address, count = value
            return 2, ModbusSlaveReadHoldingRegistersRequestEvent(request_id, starting_address, count)
        if callback_id is CallbackID.MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST:
            request_id, coil_address, coil_value = value
            return 3, ModbusSlaveWriteSingleCoilRequestEvent(request_id, coil_address, coil_value)
        if callback_id is CallbackID.MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE:
            request_id, exception_code = value
            return 4, ModbusMasterWriteSingleCoilResponseEvent(request_id, ExceptionCode(exception_code))
        if callback_id is CallbackID.MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST:
            request_id, register_address, register_value = value
            return 5, ModbusSlaveWriteSingleRegisterRequestEvent(request_id, register_address, register_value)
        if callback_id is CallbackID.MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE:
            request_id, exception_code = value
            return 6, ModbusMasterWriteSingleRegisterResponseEvent(request_id, ExceptionCode(exception_code))
        if callback_id is CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE:
            request_id, exception_code = value
            return 7, ModbusMasterWriteMultipleCoilsResponseEvent(request_id, ExceptionCode(exception_code))
        if callback_id is CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE:
            request_id, exception_code = value
            return 8, ModbusMasterWriteMultipleRegistersResponseEvent(request_id, ExceptionCode(exception_code))
        if callback_id is CallbackID.MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST:
            request_id, starting_address, count = value
            return 9, ModbusSlaveReadDiscreteInputsRequestEvent(request_id, starting_address, count)
        if callback_id is CallbackID.MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST:
            request_id, starting_address, count = value
            return 10, ModbusSlaveReadInputRegistersRequestEvent(request_id, starting_address, count)
        return 11, value

    def _to_events(  # pylint: disable=too-many-locals,too-many-return-statements,too-many-branches
        self, callback_id: CallbackID, value: Any, sids: Sequence[int] | None
    ) -> Iterable[Event]:
        if callback_id is CallbackID.READ:
            message_length, message_chunk_offset, message_chunk_data = value
            data = self._stream_assemblers[CallbackID.READ].add(
                message_length, message_chunk_offset, message_chunk_data
            )
            if data is None:
                return ()
            return (Event(self, 12, callback_id, "".join(data)),)
        if callback_id is CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE:
            request_id, exception_code, coils_length, coils_chunk_offset, coils_chunk_data = value
            data = self._stream_assemblers[CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE].add(
                coils_length, coils_chunk_offset, coils_chunk_data
            )
            if data is None:
                return ()
            return (
                Event(
                    self,
                    13,
                    callback_id,
                    ModbusMasterReadCoilsResponseEvent(request_id, ExceptionCode(exception_code), tuple(data)),
                ),
            )
        if callback_id is CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE:
            (
                request_id,
                exception_code,
                holding_registers_length,
                holding_registers_chunk_offset,
                holding_registers_chunk_data,
            ) = value
            data = self._stream_assemblers[CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE].add(
                holding_registers_length, holding_registers_chunk_offset, holding_registers_chunk_data
            )
            if data is None:
                return ()
            return (
                Event(
                    self,
                    14,
                    callback_id,
                    ModbusMasterReadHoldingRegistersResponseEvent(
                        request_id, ExceptionCode(exception_code), tuple(data)
                    ),
                ),
            )
        if callback_id is CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST:
            request_id, starting_address, coils_length, coils_chunk_offset, coils_chunk_data = value
            data = self._stream_assemblers[CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST].add(
                coils_length, coils_chunk_offset, coils_chunk_data
            )
            if data is None:
                return ()
            return (
                Event(
                    self,
                    15,
                    callback_id,
                    ModbusSlaveWriteMultipleCoilsRequestEvent(request_id, starting_address, tuple(data)),
                ),
            )
        if callback_id is CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST:
            request_id, starting_address, registers_length, registers_chunk_offset, registers_chunk_data = value
            data = self._stream_assemblers[CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST].add(
                registers_length, registers_chunk_offset, registers_chunk_data
            )
            if data is None:
                return ()
            return (
                Event(
                    self,
                    16,
                    callback_id,
                    ModbusSlaveWriteMultipleRegistersRequestEvent(request_id, starting_address, tuple(data)),
                ),
            )
        if callback_id is CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE:
            (
                request_id,
                exception_code,
                discrete_inputs_length,
                discrete_inputs_chunk_offset,
                discrete_inputs_chunk_data,
            ) = value
            data = self._stream_assemblers[CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE].add(
                discrete_inputs_length, discrete_inputs_chunk_offset, discrete_inputs_chunk_data
            )
            if data is None:
                return ()
            return (
                Event(
                    self,
                    17,
                    callback_id,
                    ModbusMasterReadDiscreteInputsResponseEvent(request_id, ExceptionCode(exception_code), tuple(data)),
                ),
            )
        if callback_id is CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE:
            (
                request_id,
                exception_code,
                input_registers_length,
                input_registers_chunk_offset,
                input_registers_chunk_data,
            ) = value
            data = self._stream_assemblers[CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE].add(
                input_registers_length, input_registers_chunk_offset, input_registers_chunk_data
            )
            if data is None:
                return ()
            return (
                Event(
                    self,
                    18,
                    callback_id,
                    ModbusMasterReadInputRegistersResponseEvent(request_id, ExceptionCode(exception_code), tuple(data)),
                ),
            )
        return super()._to_events(callback_id, value, sids)
