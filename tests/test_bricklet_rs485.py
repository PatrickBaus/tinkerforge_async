"""Tests for the RS485 Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_rs485 import (
    BrickletRS485,
    GetBufferConfig,
    GetBufferStatus,
    GetErrorCount,
    GetModbusCommonErrorCount,
    GetModbusConfiguration,
    GetRS485Configuration,
    ModbusMasterWriteMultipleCoilsResponseEvent,
    ModbusMasterWriteMultipleRegistersResponseEvent,
    ModbusMasterWriteSingleCoilResponseEvent,
    ModbusMasterWriteSingleRegisterResponseEvent,
    ModbusSlaveReadCoilsRequestEvent,
    ModbusSlaveReadDiscreteInputsRequestEvent,
    ModbusSlaveReadHoldingRegistersRequestEvent,
    ModbusSlaveReadInputRegistersRequestEvent,
    ModbusSlaveWriteSingleCoilRequestEvent,
    ModbusSlaveWriteSingleRegisterRequestEvent,
    Read,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletRS485
FunctionID = BrickletRS485.FunctionID
CallbackID = BrickletRS485.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "WRITE_LOW_LEVEL": 1,
    "READ_LOW_LEVEL": 2,
    "ENABLE_READ_CALLBACK": 3,
    "DISABLE_READ_CALLBACK": 4,
    "IS_READ_CALLBACK_ENABLED": 5,
    "SET_RS485_CONFIGURATION": 6,
    "GET_RS485_CONFIGURATION": 7,
    "SET_MODBUS_CONFIGURATION": 8,
    "GET_MODBUS_CONFIGURATION": 9,
    "SET_MODE": 10,
    "GET_MODE": 11,
    "SET_COMMUNICATION_LED_CONFIG": 12,
    "GET_COMMUNICATION_LED_CONFIG": 13,
    "SET_ERROR_LED_CONFIG": 14,
    "GET_ERROR_LED_CONFIG": 15,
    "SET_BUFFER_CONFIG": 16,
    "GET_BUFFER_CONFIG": 17,
    "GET_BUFFER_STATUS": 18,
    "ENABLE_ERROR_COUNT_CALLBACK": 19,
    "DISABLE_ERROR_COUNT_CALLBACK": 20,
    "IS_ERROR_COUNT_CALLBACK_ENABLED": 21,
    "GET_ERROR_COUNT": 22,
    "GET_MODBUS_COMMON_ERROR_COUNT": 23,
    "MODBUS_SLAVE_REPORT_EXCEPTION": 24,
    "MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL": 25,
    "MODBUS_MASTER_READ_COILS": 26,
    "MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL": 27,
    "MODBUS_MASTER_READ_HOLDING_REGISTERS": 28,
    "MODBUS_SLAVE_ANSWER_WRITE_SINGLE_COIL_REQUEST": 29,
    "MODBUS_MASTER_WRITE_SINGLE_COIL": 30,
    "MODBUS_SLAVE_ANSWER_WRITE_SINGLE_REGISTER_REQUEST": 31,
    "MODBUS_MASTER_WRITE_SINGLE_REGISTER": 32,
    "MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_COILS_REQUEST": 33,
    "MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL": 34,
    "MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_REGISTERS_REQUEST": 35,
    "MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL": 36,
    "MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL": 37,
    "MODBUS_MASTER_READ_DISCRETE_INPUTS": 38,
    "MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL": 39,
    "MODBUS_MASTER_READ_INPUT_REGISTERS": 40,
    "SET_FRAME_READABLE_CALLBACK_CONFIGURATION": 59,
    "GET_FRAME_READABLE_CALLBACK_CONFIGURATION": 60,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {
    "READ_LOW_LEVEL": 41,
    "ERROR_COUNT": 42,
    "MODBUS_SLAVE_READ_COILS_REQUEST": 43,
    "MODBUS_MASTER_READ_COILS_RESPONSE_LOW_LEVEL": 44,
    "MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST": 45,
    "MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE_LOW_LEVEL": 46,
    "MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST": 47,
    "MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE": 48,
    "MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST": 49,
    "MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE": 50,
    "MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST_LOW_LEVEL": 51,
    "MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE": 52,
    "MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST_LOW_LEVEL": 53,
    "MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE": 54,
    "MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST": 55,
    "MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE_LOW_LEVEL": 56,
    "MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST": 57,
    "MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE_LOW_LEVEL": 58,
    "FRAME_READABLE": 61,
}

CALLS: list[Call] = [
    Call(
        "write_low_level",
        FunctionID.WRITE_LOW_LEVEL,
        (3, 3, ("abcdefgh" * 60)[:60]),
        sent=("H H 60c", (3, 3, list(("abcdefgh" * 60)[:60]))),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "read_low_level",
        FunctionID.READ_LOW_LEVEL,
        (3,),
        sent=("H", (3,)),
        reply=("H H 60c", (3, 4, list(("abcdefgh" * 60)[:60]))),
        result=Read(3, 4, tuple(("abcdefgh" * 60)[:60])),
    ),
    Call("enable_read_callback", FunctionID.ENABLE_READ_CALLBACK, ()),
    Call("enable_read_callback", FunctionID.ENABLE_READ_CALLBACK, (False,), response_expected=False),
    Call("disable_read_callback", FunctionID.DISABLE_READ_CALLBACK, ()),
    Call("disable_read_callback", FunctionID.DISABLE_READ_CALLBACK, (False,), response_expected=False),
    Call("is_read_callback_enabled", FunctionID.IS_READ_CALLBACK_ENABLED, (), reply=("!", (True,)), result=True),
    Call(
        "set_rs485_configuration",
        FunctionID.SET_RS485_CONFIGURATION,
        (100, DEVICE.Parity.EVEN, DEVICE.Stopbits.STOPBITS_2, DEVICE.Wordlength.WORDLENGTH_8, DEVICE.Duplex.FULL),
        sent=("I B B B B", (100, 2, 2, 8, 1)),
    ),
    Call(
        "set_rs485_configuration",
        FunctionID.SET_RS485_CONFIGURATION,
        (
            100,
            DEVICE.Parity.EVEN,
            DEVICE.Stopbits.STOPBITS_2,
            DEVICE.Wordlength.WORDLENGTH_8,
            DEVICE.Duplex.FULL,
            False,
        ),
        sent=("I B B B B", (100, 2, 2, 8, 1)),
        response_expected=False,
    ),
    Call(
        "get_rs485_configuration",
        FunctionID.GET_RS485_CONFIGURATION,
        (),
        reply=("I B B B B", (100, 2, 2, 8, 1)),
        result=GetRS485Configuration(
            100, DEVICE.Parity.EVEN, DEVICE.Stopbits.STOPBITS_2, DEVICE.Wordlength.WORDLENGTH_8, DEVICE.Duplex.FULL
        ),
    ),
    Call("set_modbus_configuration", FunctionID.SET_MODBUS_CONFIGURATION, (3, Decimal("0.003")), sent=("B I", (3, 3))),
    Call(
        "set_modbus_configuration",
        FunctionID.SET_MODBUS_CONFIGURATION,
        (3, Decimal("0.003"), False),
        sent=("B I", (3, 3)),
        response_expected=False,
    ),
    Call(
        "get_modbus_configuration",
        FunctionID.GET_MODBUS_CONFIGURATION,
        (),
        reply=("B I", (3, 4)),
        result=GetModbusConfiguration(3, Decimal("0.004")),
    ),
    Call("set_mode", FunctionID.SET_MODE, (DEVICE.Mode.MODBUS_SLAVE_RTU,), sent=("B", (2,))),
    Call(
        "set_mode",
        FunctionID.SET_MODE,
        (DEVICE.Mode.MODBUS_SLAVE_RTU, False),
        sent=("B", (2,)),
        response_expected=False,
    ),
    Call("get_mode", FunctionID.GET_MODE, (), reply=("B", (2,)), result=DEVICE.Mode.MODBUS_SLAVE_RTU),
    Call(
        "set_communication_led_config",
        FunctionID.SET_COMMUNICATION_LED_CONFIG,
        (DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION,),
        sent=("B", (3,)),
    ),
    Call(
        "set_communication_led_config",
        FunctionID.SET_COMMUNICATION_LED_CONFIG,
        (DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_communication_led_config",
        FunctionID.GET_COMMUNICATION_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.CommunicationLEDConfig.SHOW_COMMUNICATION,
    ),
    Call(
        "set_error_led_config", FunctionID.SET_ERROR_LED_CONFIG, (DEVICE.ErrorLEDConfig.SHOW_ERROR,), sent=("B", (3,))
    ),
    Call(
        "set_error_led_config",
        FunctionID.SET_ERROR_LED_CONFIG,
        (DEVICE.ErrorLEDConfig.SHOW_ERROR, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_error_led_config",
        FunctionID.GET_ERROR_LED_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.ErrorLEDConfig.SHOW_ERROR,
    ),
    Call("set_buffer_config", FunctionID.SET_BUFFER_CONFIG, (1024, 1024), sent=("H H", (1024, 1024))),
    Call(
        "set_buffer_config",
        FunctionID.SET_BUFFER_CONFIG,
        (1024, 1024, False),
        sent=("H H", (1024, 1024)),
        response_expected=False,
    ),
    Call(
        "get_buffer_config",
        FunctionID.GET_BUFFER_CONFIG,
        (),
        reply=("H H", (1024, 1024)),
        result=GetBufferConfig(1024, 1024),
    ),
    Call("get_buffer_status", FunctionID.GET_BUFFER_STATUS, (), reply=("H H", (3, 4)), result=GetBufferStatus(3, 4)),
    Call("enable_error_count_callback", FunctionID.ENABLE_ERROR_COUNT_CALLBACK, ()),
    Call("enable_error_count_callback", FunctionID.ENABLE_ERROR_COUNT_CALLBACK, (False,), response_expected=False),
    Call("disable_error_count_callback", FunctionID.DISABLE_ERROR_COUNT_CALLBACK, ()),
    Call("disable_error_count_callback", FunctionID.DISABLE_ERROR_COUNT_CALLBACK, (False,), response_expected=False),
    Call(
        "is_error_count_callback_enabled",
        FunctionID.IS_ERROR_COUNT_CALLBACK_ENABLED,
        (),
        reply=("!", (True,)),
        result=True,
    ),
    Call("get_error_count", FunctionID.GET_ERROR_COUNT, (), reply=("I I", (3, 4)), result=GetErrorCount(3, 4)),
    Call(
        "get_modbus_common_error_count",
        FunctionID.GET_MODBUS_COMMON_ERROR_COUNT,
        (),
        reply=("I I I I I I I", (3, 4, 5, 6, 7, 8, 9)),
        result=GetModbusCommonErrorCount(3, 4, 5, 6, 7, 8, 9),
    ),
    Call(
        "modbus_slave_report_exception",
        FunctionID.MODBUS_SLAVE_REPORT_EXCEPTION,
        (3, DEVICE.ExceptionCode.GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND),
        sent=("B b", (3, 11)),
    ),
    Call(
        "modbus_slave_report_exception",
        FunctionID.MODBUS_SLAVE_REPORT_EXCEPTION,
        (3, DEVICE.ExceptionCode.GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND, False),
        sent=("B b", (3, 11)),
        response_expected=False,
    ),
    Call(
        "modbus_slave_answer_read_coils_request_low_level",
        FunctionID.MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL,
        (3, 3, 3, [i % 2 == 0 for i in range(472)]),
        sent=("B H H 472!", (3, 3, 3, [i % 2 == 0 for i in range(472)])),
    ),
    Call(
        "modbus_slave_answer_read_coils_request_low_level",
        FunctionID.MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL,
        (3, 3, 3, [i % 2 == 0 for i in range(472)], False),
        sent=("B H H 472!", (3, 3, 3, [i % 2 == 0 for i in range(472)])),
        response_expected=False,
    ),
    Call(
        "modbus_master_read_coils",
        FunctionID.MODBUS_MASTER_READ_COILS,
        (3, 3, 3),
        sent=("B I H", (3, 3, 3)),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "modbus_slave_answer_read_holding_registers_request_low_level",
        FunctionID.MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL,
        (3, 3, 3, [3] * 29),
        sent=("B H H 29H", (3, 3, 3, [3] * 29)),
    ),
    Call(
        "modbus_slave_answer_read_holding_registers_request_low_level",
        FunctionID.MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL,
        (3, 3, 3, [3] * 29, False),
        sent=("B H H 29H", (3, 3, 3, [3] * 29)),
        response_expected=False,
    ),
    Call(
        "modbus_master_read_holding_registers",
        FunctionID.MODBUS_MASTER_READ_HOLDING_REGISTERS,
        (3, 3, 3),
        sent=("B I H", (3, 3, 3)),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "modbus_slave_answer_write_single_coil_request",
        FunctionID.MODBUS_SLAVE_ANSWER_WRITE_SINGLE_COIL_REQUEST,
        (3,),
        sent=("B", (3,)),
    ),
    Call(
        "modbus_slave_answer_write_single_coil_request",
        FunctionID.MODBUS_SLAVE_ANSWER_WRITE_SINGLE_COIL_REQUEST,
        (3, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "modbus_master_write_single_coil",
        FunctionID.MODBUS_MASTER_WRITE_SINGLE_COIL,
        (3, 3, True),
        sent=("B I !", (3, 3, True)),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "modbus_slave_answer_write_single_register_request",
        FunctionID.MODBUS_SLAVE_ANSWER_WRITE_SINGLE_REGISTER_REQUEST,
        (3,),
        sent=("B", (3,)),
    ),
    Call(
        "modbus_slave_answer_write_single_register_request",
        FunctionID.MODBUS_SLAVE_ANSWER_WRITE_SINGLE_REGISTER_REQUEST,
        (3, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "modbus_master_write_single_register",
        FunctionID.MODBUS_MASTER_WRITE_SINGLE_REGISTER,
        (3, 3, 3),
        sent=("B I H", (3, 3, 3)),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "modbus_slave_answer_write_multiple_coils_request",
        FunctionID.MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_COILS_REQUEST,
        (3,),
        sent=("B", (3,)),
    ),
    Call(
        "modbus_slave_answer_write_multiple_coils_request",
        FunctionID.MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_COILS_REQUEST,
        (3, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "modbus_master_write_multiple_coils_low_level",
        FunctionID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL,
        (3, 3, 3, 3, [i % 2 == 0 for i in range(440)]),
        sent=("B I H H 440!", (3, 3, 3, 3, [i % 2 == 0 for i in range(440)])),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "modbus_slave_answer_write_multiple_registers_request",
        FunctionID.MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_REGISTERS_REQUEST,
        (3,),
        sent=("B", (3,)),
    ),
    Call(
        "modbus_slave_answer_write_multiple_registers_request",
        FunctionID.MODBUS_SLAVE_ANSWER_WRITE_MULTIPLE_REGISTERS_REQUEST,
        (3, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "modbus_master_write_multiple_registers_low_level",
        FunctionID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL,
        (3, 3, 3, 3, [3] * 27),
        sent=("B I H H 27H", (3, 3, 3, 3, [3] * 27)),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "modbus_slave_answer_read_discrete_inputs_request_low_level",
        FunctionID.MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL,
        (3, 3, 3, [i % 2 == 0 for i in range(472)]),
        sent=("B H H 472!", (3, 3, 3, [i % 2 == 0 for i in range(472)])),
    ),
    Call(
        "modbus_slave_answer_read_discrete_inputs_request_low_level",
        FunctionID.MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL,
        (3, 3, 3, [i % 2 == 0 for i in range(472)], False),
        sent=("B H H 472!", (3, 3, 3, [i % 2 == 0 for i in range(472)])),
        response_expected=False,
    ),
    Call(
        "modbus_master_read_discrete_inputs",
        FunctionID.MODBUS_MASTER_READ_DISCRETE_INPUTS,
        (3, 3, 3),
        sent=("B I H", (3, 3, 3)),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "modbus_slave_answer_read_input_registers_request_low_level",
        FunctionID.MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL,
        (3, 3, 3, [3] * 29),
        sent=("B H H 29H", (3, 3, 3, [3] * 29)),
    ),
    Call(
        "modbus_slave_answer_read_input_registers_request_low_level",
        FunctionID.MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL,
        (3, 3, 3, [3] * 29, False),
        sent=("B H H 29H", (3, 3, 3, [3] * 29)),
        response_expected=False,
    ),
    Call(
        "modbus_master_read_input_registers",
        FunctionID.MODBUS_MASTER_READ_INPUT_REGISTERS,
        (3, 3, 3),
        sent=("B I H", (3, 3, 3)),
        reply=("B", (3,)),
        result=3,
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (3,),
        sent=("H", (3,)),
    ),
    Call(
        "set_frame_readable_callback_configuration",
        FunctionID.SET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (3, False),
        sent=("H", (3,)),
        response_expected=False,
    ),
    Call(
        "get_frame_readable_callback_configuration",
        FunctionID.GET_FRAME_READABLE_CALLBACK_CONFIGURATION,
        (),
        reply=("H", (3,)),
        result=3,
    ),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("write_low_level", (65536, 3, ("abcdefgh" * 60)[:60])),
    ("write_low_level", (3, 65536, ("abcdefgh" * 60)[:60])),
    ("write_low_level", (3, 3, (("abcdefgh" * 60)[:60])[:-1])),
    ("write", ("a" * 65536,)),
    ("read_low_level", (65536,)),
    (
        "set_rs485_configuration",
        (2000001, DEVICE.Parity.EVEN, DEVICE.Stopbits.STOPBITS_2, DEVICE.Wordlength.WORDLENGTH_8, DEVICE.Duplex.FULL),
    ),
    (
        "set_rs485_configuration",
        (100, 12345, DEVICE.Stopbits.STOPBITS_2, DEVICE.Wordlength.WORDLENGTH_8, DEVICE.Duplex.FULL),
    ),
    ("set_rs485_configuration", (100, DEVICE.Parity.EVEN, 12345, DEVICE.Wordlength.WORDLENGTH_8, DEVICE.Duplex.FULL)),
    ("set_rs485_configuration", (100, DEVICE.Parity.EVEN, DEVICE.Stopbits.STOPBITS_2, 12345, DEVICE.Duplex.FULL)),
    (
        "set_rs485_configuration",
        (100, DEVICE.Parity.EVEN, DEVICE.Stopbits.STOPBITS_2, DEVICE.Wordlength.WORDLENGTH_8, 12345),
    ),
    ("set_modbus_configuration", (248, Decimal("0.003"))),
    ("set_modbus_configuration", (3, Decimal("4294967.296"))),
    ("set_mode", (12345,)),
    ("set_communication_led_config", (12345,)),
    ("set_error_led_config", (12345,)),
    ("set_buffer_config", (9217, 1024)),
    ("set_buffer_config", (1024, 9217)),
    ("modbus_slave_report_exception", (256, DEVICE.ExceptionCode.GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND)),
    ("modbus_slave_report_exception", (3, 12345)),
    ("modbus_slave_answer_read_coils_request_low_level", (256, 3, 3, [i % 2 == 0 for i in range(472)])),
    ("modbus_slave_answer_read_coils_request_low_level", (3, 2001, 3, [i % 2 == 0 for i in range(472)])),
    ("modbus_slave_answer_read_coils_request_low_level", (3, 3, 65536, [i % 2 == 0 for i in range(472)])),
    ("modbus_slave_answer_read_coils_request_low_level", (3, 3, 3, ([i % 2 == 0 for i in range(472)])[:-1])),
    ("modbus_slave_answer_read_coils_request", (3, [True] * 65536)),
    ("modbus_master_read_coils", (248, 3, 3)),
    ("modbus_master_read_coils", (3, 65537, 3)),
    ("modbus_master_read_coils", (3, 3, 2001)),
    ("modbus_slave_answer_read_holding_registers_request_low_level", (256, 3, 3, [3] * 29)),
    ("modbus_slave_answer_read_holding_registers_request_low_level", (3, 126, 3, [3] * 29)),
    ("modbus_slave_answer_read_holding_registers_request_low_level", (3, 3, 65536, [3] * 29)),
    ("modbus_slave_answer_read_holding_registers_request_low_level", (3, 3, 3, ([3] * 29)[:-1])),
    ("modbus_slave_answer_read_holding_registers_request", (3, [1] * 65536)),
    ("modbus_master_read_holding_registers", (248, 3, 3)),
    ("modbus_master_read_holding_registers", (3, 65537, 3)),
    ("modbus_master_read_holding_registers", (3, 3, 126)),
    ("modbus_slave_answer_write_single_coil_request", (256,)),
    ("modbus_master_write_single_coil", (248, 3, True)),
    ("modbus_master_write_single_coil", (3, 65537, True)),
    ("modbus_slave_answer_write_single_register_request", (256,)),
    ("modbus_master_write_single_register", (248, 3, 3)),
    ("modbus_master_write_single_register", (3, 65537, 3)),
    ("modbus_master_write_single_register", (3, 3, 65536)),
    ("modbus_slave_answer_write_multiple_coils_request", (256,)),
    ("modbus_master_write_multiple_coils_low_level", (248, 3, 3, 3, [i % 2 == 0 for i in range(440)])),
    ("modbus_master_write_multiple_coils_low_level", (3, 65537, 3, 3, [i % 2 == 0 for i in range(440)])),
    ("modbus_master_write_multiple_coils_low_level", (3, 3, 1969, 3, [i % 2 == 0 for i in range(440)])),
    ("modbus_master_write_multiple_coils_low_level", (3, 3, 3, 65536, [i % 2 == 0 for i in range(440)])),
    ("modbus_master_write_multiple_coils_low_level", (3, 3, 3, 3, ([i % 2 == 0 for i in range(440)])[:-1])),
    ("modbus_master_write_multiple_coils", (3, 3, [True] * 65536)),
    ("modbus_slave_answer_write_multiple_registers_request", (256,)),
    ("modbus_master_write_multiple_registers_low_level", (248, 3, 3, 3, [3] * 27)),
    ("modbus_master_write_multiple_registers_low_level", (3, 65537, 3, 3, [3] * 27)),
    ("modbus_master_write_multiple_registers_low_level", (3, 3, 124, 3, [3] * 27)),
    ("modbus_master_write_multiple_registers_low_level", (3, 3, 3, 65536, [3] * 27)),
    ("modbus_master_write_multiple_registers_low_level", (3, 3, 3, 3, ([3] * 27)[:-1])),
    ("modbus_master_write_multiple_registers", (3, 3, [1] * 65536)),
    ("modbus_slave_answer_read_discrete_inputs_request_low_level", (256, 3, 3, [i % 2 == 0 for i in range(472)])),
    ("modbus_slave_answer_read_discrete_inputs_request_low_level", (3, 2001, 3, [i % 2 == 0 for i in range(472)])),
    ("modbus_slave_answer_read_discrete_inputs_request_low_level", (3, 3, 65536, [i % 2 == 0 for i in range(472)])),
    ("modbus_slave_answer_read_discrete_inputs_request_low_level", (3, 3, 3, ([i % 2 == 0 for i in range(472)])[:-1])),
    ("modbus_slave_answer_read_discrete_inputs_request", (3, [True] * 65536)),
    ("modbus_master_read_discrete_inputs", (248, 3, 3)),
    ("modbus_master_read_discrete_inputs", (3, 65537, 3)),
    ("modbus_master_read_discrete_inputs", (3, 3, 2001)),
    ("modbus_slave_answer_read_input_registers_request_low_level", (256, 3, 3, [3] * 29)),
    ("modbus_slave_answer_read_input_registers_request_low_level", (3, 126, 3, [3] * 29)),
    ("modbus_slave_answer_read_input_registers_request_low_level", (3, 3, 65536, [3] * 29)),
    ("modbus_slave_answer_read_input_registers_request_low_level", (3, 3, 3, ([3] * 29)[:-1])),
    ("modbus_slave_answer_read_input_registers_request", (3, [1] * 65536)),
    ("modbus_master_read_input_registers", (248, 3, 3)),
    ("modbus_master_read_input_registers", (3, 65537, 3)),
    ("modbus_master_read_input_registers", (3, 3, 126)),
    ("set_frame_readable_callback_configuration", (9217,)),
]


def test_identity(device: BrickletRS485) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 277
    assert device.get_api_version() == (2, 0, 1)
    assert str(device).startswith("RS485 Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_write_transfers_the_stream(device: BrickletRS485, connection: FakeConnection) -> None:
    """The high-level function write() uses write_low_level()."""
    data = ("abc" * 3)[:3]
    connection.reply(FunctionID.WRITE_LOW_LEVEL, "B", *(3,))
    result = run(device.write(*(data,)))
    assert connection.requests == [
        request(FunctionID.WRITE_LOW_LEVEL, "H H 60c", *(3, offset, chunk(list(("abc" * 3)[:3]), offset, 60, "\x00")))
        for offset in range(0, 1, 60)
    ]
    assert result == 3


def test_read_transfers_the_stream(device: BrickletRS485, connection: FakeConnection) -> None:
    """The high-level function read() uses read_low_level()."""
    data = list(("abc" * 3)[:3])
    for offset in range(0, 1, 60):
        connection.reply(FunctionID.READ_LOW_LEVEL, "H H 60c", *(3, offset, chunk(data, offset, 60, "\x00")))
    result = run(device.read(*(3,)))
    assert connection.requests == [request(FunctionID.READ_LOW_LEVEL, "H", *(3,))] * 1
    assert result == ("abc" * 3)[:3]


def test_modbus_slave_answer_read_coils_request_transfers_the_stream(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The high-level function modbus_slave_answer_read_coils_request() uses modbus_slave_answer_read_coils_request_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    result = run(device.modbus_slave_answer_read_coils_request(*(3, data)))
    assert connection.requests == [
        request(
            FunctionID.MODBUS_SLAVE_ANSWER_READ_COILS_REQUEST_LOW_LEVEL,
            "B H H 472!",
            *(3, 3, offset, chunk([i % 2 == 0 for i in range(3)], offset, 472, False)),
        )
        for offset in range(0, 1, 472)
    ]
    assert result is None


def test_modbus_slave_answer_read_holding_registers_request_transfers_the_stream(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The high-level function modbus_slave_answer_read_holding_registers_request() uses modbus_slave_answer_read_holding_registers_request_low_level()."""
    data = [3] * 3
    result = run(device.modbus_slave_answer_read_holding_registers_request(*(3, data)))
    assert connection.requests == [
        request(
            FunctionID.MODBUS_SLAVE_ANSWER_READ_HOLDING_REGISTERS_REQUEST_LOW_LEVEL,
            "B H H 29H",
            *(3, 3, offset, chunk([3] * 3, offset, 29, 0)),
        )
        for offset in range(0, 1, 29)
    ]
    assert result is None


def test_modbus_master_write_multiple_coils_transfers_the_stream(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The high-level function modbus_master_write_multiple_coils() uses modbus_master_write_multiple_coils_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    connection.reply(FunctionID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL, "B", *(3,))
    result = run(device.modbus_master_write_multiple_coils(*(3, 3, data)))
    assert connection.requests == [
        request(
            FunctionID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_LOW_LEVEL,
            "B I H H 440!",
            *(3, 3, 3, offset, chunk([i % 2 == 0 for i in range(3)], offset, 440, False)),
        )
        for offset in range(0, 1, 440)
    ]
    assert result is not None


def test_modbus_master_write_multiple_registers_transfers_the_stream(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The high-level function modbus_master_write_multiple_registers() uses modbus_master_write_multiple_registers_low_level()."""
    data = [3] * 3
    connection.reply(FunctionID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL, "B", *(3,))
    result = run(device.modbus_master_write_multiple_registers(*(3, 3, data)))
    assert connection.requests == [
        request(
            FunctionID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_LOW_LEVEL,
            "B I H H 27H",
            *(3, 3, 3, offset, chunk([3] * 3, offset, 27, 0)),
        )
        for offset in range(0, 1, 27)
    ]
    assert result is not None


def test_modbus_slave_answer_read_discrete_inputs_request_transfers_the_stream(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The high-level function modbus_slave_answer_read_discrete_inputs_request() uses modbus_slave_answer_read_discrete_inputs_request_low_level()."""
    data = [i % 2 == 0 for i in range(3)]
    result = run(device.modbus_slave_answer_read_discrete_inputs_request(*(3, data)))
    assert connection.requests == [
        request(
            FunctionID.MODBUS_SLAVE_ANSWER_READ_DISCRETE_INPUTS_REQUEST_LOW_LEVEL,
            "B H H 472!",
            *(3, 3, offset, chunk([i % 2 == 0 for i in range(3)], offset, 472, False)),
        )
        for offset in range(0, 1, 472)
    ]
    assert result is None


def test_modbus_slave_answer_read_input_registers_request_transfers_the_stream(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The high-level function modbus_slave_answer_read_input_registers_request() uses modbus_slave_answer_read_input_registers_request_low_level()."""
    data = [3] * 3
    result = run(device.modbus_slave_answer_read_input_registers_request(*(3, data)))
    assert connection.requests == [
        request(
            FunctionID.MODBUS_SLAVE_ANSWER_READ_INPUT_REGISTERS_REQUEST_LOW_LEVEL,
            "B H H 29H",
            *(3, 3, offset, chunk([3] * 3, offset, 29, 0)),
        )
        for offset in range(0, 1, 29)
    ]
    assert result is None


def test_callback_read(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback READ is converted to an event."""
    data = list(("abc" * 3)[:3])
    for offset in range(0, 1, 60):
        connection.callback(CallbackID.READ, "H H 60c", *(3, offset, chunk(data, offset, 60, "\x00")))
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [(12, CallbackID.READ)]
    assert events[0].payload == ("abc" * 3)[:3]
    connection_2 = FakeConnection()
    connection_2.callback(CallbackID.READ, "H H 60c", *(63, 60, chunk(data, 0, 60, "\x00")))
    assert not read_events(DEVICE(UID, connection_2.ipcon))


def test_callback_error_count(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback ERROR_COUNT is converted to an event."""
    connection.callback(CallbackID.ERROR_COUNT, "I I", *(3, 4))
    assert summary(read_events(device)) == [(0, CallbackID.ERROR_COUNT, GetErrorCount(3, 4))]


def test_callback_modbus_slave_read_coils_request(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback MODBUS_SLAVE_READ_COILS_REQUEST is converted to an event."""
    connection.callback(CallbackID.MODBUS_SLAVE_READ_COILS_REQUEST, "B I H", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (1, CallbackID.MODBUS_SLAVE_READ_COILS_REQUEST, ModbusSlaveReadCoilsRequestEvent(3, 4, 5))
    ]


def test_callback_modbus_master_read_coils_response(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback MODBUS_MASTER_READ_COILS_RESPONSE is converted to an event."""
    data = [i % 2 == 0 for i in range(3)]
    for offset in range(0, 1, 464):
        connection.callback(
            CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE,
            "B b H H 464!",
            *(3, 11, 3, offset, chunk(data, offset, 464, False)),
        )
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [(13, CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE)]
    assert events[0].payload.coils == tuple(i % 2 == 0 for i in range(3))
    connection_2 = FakeConnection()
    connection_2.callback(
        CallbackID.MODBUS_MASTER_READ_COILS_RESPONSE, "B b H H 464!", *(3, 11, 467, 464, chunk(data, 0, 464, False))
    )
    assert not read_events(DEVICE(UID, connection_2.ipcon))


def test_callback_modbus_slave_read_holding_registers_request(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The callback MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST is converted to an event."""
    connection.callback(CallbackID.MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST, "B I H", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (
            2,
            CallbackID.MODBUS_SLAVE_READ_HOLDING_REGISTERS_REQUEST,
            ModbusSlaveReadHoldingRegistersRequestEvent(3, 4, 5),
        )
    ]


def test_callback_modbus_master_read_holding_registers_response(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The callback MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE is converted to an event."""
    data = [3] * 3
    for offset in range(0, 1, 29):
        connection.callback(
            CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE,
            "B b H H 29H",
            *(3, 11, 3, offset, chunk(data, offset, 29, 0)),
        )
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [
        (14, CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE)
    ]
    assert events[0].payload.holding_registers == (3,) * 3
    connection_2 = FakeConnection()
    connection_2.callback(
        CallbackID.MODBUS_MASTER_READ_HOLDING_REGISTERS_RESPONSE, "B b H H 29H", *(3, 11, 32, 29, chunk(data, 0, 29, 0))
    )
    assert not read_events(DEVICE(UID, connection_2.ipcon))


def test_callback_modbus_slave_write_single_coil_request(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST is converted to an event."""
    connection.callback(CallbackID.MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST, "B I !", *(3, 4, True))
    assert summary(read_events(device)) == [
        (3, CallbackID.MODBUS_SLAVE_WRITE_SINGLE_COIL_REQUEST, ModbusSlaveWriteSingleCoilRequestEvent(3, 4, True))
    ]


def test_callback_modbus_master_write_single_coil_response(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE is converted to an event."""
    connection.callback(CallbackID.MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE, "B b", *(3, 11))
    assert summary(read_events(device)) == [
        (
            4,
            CallbackID.MODBUS_MASTER_WRITE_SINGLE_COIL_RESPONSE,
            ModbusMasterWriteSingleCoilResponseEvent(3, DEVICE.ExceptionCode.GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND),
        )
    ]


def test_callback_modbus_slave_write_single_register_request(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST is converted to an event."""
    connection.callback(CallbackID.MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST, "B I H", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (5, CallbackID.MODBUS_SLAVE_WRITE_SINGLE_REGISTER_REQUEST, ModbusSlaveWriteSingleRegisterRequestEvent(3, 4, 5))
    ]


def test_callback_modbus_master_write_single_register_response(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The callback MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE is converted to an event."""
    connection.callback(CallbackID.MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE, "B b", *(3, 11))
    assert summary(read_events(device)) == [
        (
            6,
            CallbackID.MODBUS_MASTER_WRITE_SINGLE_REGISTER_RESPONSE,
            ModbusMasterWriteSingleRegisterResponseEvent(
                3, DEVICE.ExceptionCode.GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND
            ),
        )
    ]


def test_callback_modbus_slave_write_multiple_coils_request(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST is converted to an event."""
    data = [i % 2 == 0 for i in range(3)]
    for offset in range(0, 1, 440):
        connection.callback(
            CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST,
            "B I H H 440!",
            *(3, 4, 3, offset, chunk(data, offset, 440, False)),
        )
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [
        (15, CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST)
    ]
    assert events[0].payload.coils == tuple(i % 2 == 0 for i in range(3))
    connection_2 = FakeConnection()
    connection_2.callback(
        CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_COILS_REQUEST,
        "B I H H 440!",
        *(3, 4, 443, 440, chunk(data, 0, 440, False)),
    )
    assert not read_events(DEVICE(UID, connection_2.ipcon))


def test_callback_modbus_master_write_multiple_coils_response(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The callback MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE is converted to an event."""
    connection.callback(CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE, "B b", *(3, 11))
    assert summary(read_events(device)) == [
        (
            7,
            CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_COILS_RESPONSE,
            ModbusMasterWriteMultipleCoilsResponseEvent(
                3, DEVICE.ExceptionCode.GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND
            ),
        )
    ]


def test_callback_modbus_slave_write_multiple_registers_request(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The callback MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST is converted to an event."""
    data = [3] * 3
    for offset in range(0, 1, 27):
        connection.callback(
            CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST,
            "B I H H 27H",
            *(3, 4, 3, offset, chunk(data, offset, 27, 0)),
        )
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [
        (16, CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST)
    ]
    assert events[0].payload.registers == (3,) * 3
    connection_2 = FakeConnection()
    connection_2.callback(
        CallbackID.MODBUS_SLAVE_WRITE_MULTIPLE_REGISTERS_REQUEST, "B I H H 27H", *(3, 4, 30, 27, chunk(data, 0, 27, 0))
    )
    assert not read_events(DEVICE(UID, connection_2.ipcon))


def test_callback_modbus_master_write_multiple_registers_response(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The callback MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE is converted to an event."""
    connection.callback(CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE, "B b", *(3, 11))
    assert summary(read_events(device)) == [
        (
            8,
            CallbackID.MODBUS_MASTER_WRITE_MULTIPLE_REGISTERS_RESPONSE,
            ModbusMasterWriteMultipleRegistersResponseEvent(
                3, DEVICE.ExceptionCode.GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND
            ),
        )
    ]


def test_callback_modbus_slave_read_discrete_inputs_request(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST is converted to an event."""
    connection.callback(CallbackID.MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST, "B I H", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (9, CallbackID.MODBUS_SLAVE_READ_DISCRETE_INPUTS_REQUEST, ModbusSlaveReadDiscreteInputsRequestEvent(3, 4, 5))
    ]


def test_callback_modbus_master_read_discrete_inputs_response(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The callback MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE is converted to an event."""
    data = [i % 2 == 0 for i in range(3)]
    for offset in range(0, 1, 464):
        connection.callback(
            CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE,
            "B b H H 464!",
            *(3, 11, 3, offset, chunk(data, offset, 464, False)),
        )
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [
        (17, CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE)
    ]
    assert events[0].payload.discrete_inputs == tuple(i % 2 == 0 for i in range(3))
    connection_2 = FakeConnection()
    connection_2.callback(
        CallbackID.MODBUS_MASTER_READ_DISCRETE_INPUTS_RESPONSE,
        "B b H H 464!",
        *(3, 11, 467, 464, chunk(data, 0, 464, False)),
    )
    assert not read_events(DEVICE(UID, connection_2.ipcon))


def test_callback_modbus_slave_read_input_registers_request(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST is converted to an event."""
    connection.callback(CallbackID.MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST, "B I H", *(3, 4, 5))
    assert summary(read_events(device)) == [
        (10, CallbackID.MODBUS_SLAVE_READ_INPUT_REGISTERS_REQUEST, ModbusSlaveReadInputRegistersRequestEvent(3, 4, 5))
    ]


def test_callback_modbus_master_read_input_registers_response(
    device: BrickletRS485, connection: FakeConnection
) -> None:
    """The callback MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE is converted to an event."""
    data = [3] * 3
    for offset in range(0, 1, 29):
        connection.callback(
            CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE,
            "B b H H 29H",
            *(3, 11, 3, offset, chunk(data, offset, 29, 0)),
        )
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [
        (18, CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE)
    ]
    assert events[0].payload.input_registers == (3,) * 3
    connection_2 = FakeConnection()
    connection_2.callback(
        CallbackID.MODBUS_MASTER_READ_INPUT_REGISTERS_RESPONSE, "B b H H 29H", *(3, 11, 32, 29, chunk(data, 0, 29, 0))
    )
    assert not read_events(DEVICE(UID, connection_2.ipcon))


def test_callback_frame_readable(device: BrickletRS485, connection: FakeConnection) -> None:
    """The callback FRAME_READABLE is converted to an event."""
    connection.callback(CallbackID.FRAME_READABLE, "H", *(3,))
    assert summary(read_events(device)) == [(11, CallbackID.FRAME_READABLE, 3)]
