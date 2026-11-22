"""
Module for the Tinkerforge DC Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/DC_Brick_Python.html) implemented using
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
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

from .devices import BrickletPort as Port
from .devices import Channel, DeviceIdentifier, DeviceWithMCU, GetSPITFPBaudrateConfig, GetSPITFPErrorCount, _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this brick
    """

    UNDER_VOLTAGE = 21
    EMERGENCY_SHUTDOWN = 22
    VELOCITY_REACHED = 23
    CURRENT_VELOCITY = 24


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """

    SET_VELOCITY = 1
    GET_VELOCITY = 2
    GET_CURRENT_VELOCITY = 3
    SET_ACCELERATION = 4
    GET_ACCELERATION = 5
    SET_PWM_FREQUENCY = 6
    GET_PWM_FREQUENCY = 7
    FULL_BRAKE = 8
    GET_STACK_INPUT_VOLTAGE = 9
    GET_EXTERNAL_INPUT_VOLTAGE = 10
    GET_CURRENT_CONSUMPTION = 11
    ENABLE = 12
    DISABLE = 13
    IS_ENABLED = 14
    SET_MINIMUM_VOLTAGE = 15
    GET_MINIMUM_VOLTAGE = 16
    SET_DRIVE_MODE = 17
    GET_DRIVE_MODE = 18
    SET_CURRENT_VELOCITY_PERIOD = 19
    GET_CURRENT_VELOCITY_PERIOD = 20
    SET_SPITFP_BAUDRATE_CONFIG = 231
    GET_SPITFP_BAUDRATE_CONFIG = 232
    GET_SEND_TIMEOUT_COUNT = 233
    SET_SPITFP_BAUDRATE = 234
    GET_SPITFP_BAUDRATE = 235
    GET_SPITFP_ERROR_COUNT = 237
    ENABLE_STATUS_LED = 238
    DISABLE_STATUS_LED = 239
    IS_STATUS_LED_ENABLED = 240
    GET_PROTOCOL1_BRICKLET_NAME = 241
    GET_CHIP_TEMPERATURE = 242
    WRITE_BRICKLET_PLUGIN = 246
    READ_BRICKLET_PLUGIN = 247


@unique
class DriveMode(Enum):
    """
    The drive mode options
    """

    DRIVE_BRAKE = 0
    DRIVE_COAST = 1


@unique
class CommunicationMethod(Enum):
    """
    The communication method options
    """

    NONE = 0
    USB = 1
    SPI_STACK = 2
    CHIBI = 3
    RS485 = 4
    WIFI = 5
    ETHERNET = 6
    WIFI_V2 = 7


class GetProtocol1BrickletName(NamedTuple):
    protocol_version: int
    firmware_version: tuple[int, ...]
    name: str


DECI_DEGREE_CELSIUS = LinearQuantity(1, 10, CELSIUS_ZERO)  # raw: 1/10 Degree Celsius, returned in K
HERTZ = LinearQuantity(1)  # raw: 1/1 Hertz, returned in Hz
MILLI_AMPERE = LinearQuantity(1, 1000)  # raw: 1/1000 Ampere, returned in A
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V
PERCENT_100_32767 = LinearQuantity(100, 32767)  # raw: 100/32767 Percent, returned in %
PERCENT_PER_SECOND_100_32767 = LinearQuantity(100, 32767)  # raw: 100/32767 Percent Per Second, returned in %/s


class BrickDC(DeviceWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Drives one brushed DC motor with up to 28V and 5A (peak)
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_DC
    DEVICE_DISPLAY_NAME = "DC Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    BrickletPort = Port
    DriveMode: TypeAlias = DriveMode
    CommunicationMethod: TypeAlias = CommunicationMethod

    CALLBACK_FORMATS = {
        CallbackID.UNDER_VOLTAGE: "H",
        CallbackID.EMERGENCY_SHUTDOWN: "",
        CallbackID.VELOCITY_REACHED: "h",
        CallbackID.CURRENT_VELOCITY: "h",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.UNDER_VOLTAGE,)),
        Channel(1, callbacks=(CallbackID.EMERGENCY_SHUTDOWN,)),
        Channel(2, callbacks=(CallbackID.VELOCITY_REACHED,)),
        Channel(3, getter="get_current_velocity", callbacks=(CallbackID.CURRENT_VELOCITY,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 3)

    async def get_value(self, sid: int) -> Any:
        """
        Returns the value of the channel with the secondary id `sid`. See `CHANNELS` for the channels.
        """
        return await self._get_value(sid)

    async def set_velocity(self, velocity: float | Decimal = 0, response_expected: bool = True) -> None:
        """
        Sets the velocity of the motor. Whereas -32767 is full speed backward,
        0 is stop and 32767 is full speed forward. Depending on the
        acceleration (see :func:`set_acceleration`), the motor is not immediately
        brought to the velocity but smoothly accelerated.

        The velocity describes the duty cycle of the PWM with which the motor is
        controlled, e.g. a velocity of 3277 sets a PWM with a 10% duty cycle.
        You can not only control the duty cycle of the PWM but also the frequency,
        see :func:`set_pwm_frequency`.

        Units: velocity in % (-100 to 100 %).
        """
        velocity_raw = PERCENT_100_32767.from_si(velocity)
        check_range("velocity", velocity_raw, -32767, 32767, velocity)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VELOCITY,
            data=pack_payload((velocity_raw,), "h"),
            response_expected=response_expected,
        )

    async def get_velocity(self) -> Decimal:
        """
        Returns the velocity as set by :func:`set_velocity`.

        Units: velocity in % (-100 to 100 %).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VELOCITY, response_expected=True
        )
        return PERCENT_100_32767.to_si(unpack_payload(payload, "h"))

    async def get_current_velocity(self) -> Decimal:
        """
        Returns the *current* velocity of the motor. This value is different
        from :func:`get_velocity` whenever the motor is currently accelerating
        to a goal set by :func:`set_velocity`.

        Units: velocity in % (-100 to 100 %).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_VELOCITY, response_expected=True
        )
        return PERCENT_100_32767.to_si(unpack_payload(payload, "h"))

    async def set_acceleration(
        self, acceleration: float | Decimal = Decimal("30.51850947599719229712820826"), response_expected: bool = True
    ) -> None:
        """
        Sets the acceleration of the motor. It is given in *velocity/s*. An
        acceleration of 10000 means, that every second the velocity is increased
        by 10000 (or about 30% duty cycle).

        For example: If the current velocity is 0 and you want to accelerate to a
        velocity of 16000 (about 50% duty cycle) in 10 seconds, you should set
        an acceleration of 1600.

        If acceleration is set to 0, there is no speed ramping, i.e. a new velocity
        is immediately given to the motor.

        Units: acceleration in %/s.
        """
        acceleration_raw = PERCENT_PER_SECOND_100_32767.from_si(acceleration)
        check_range("acceleration", acceleration_raw, 0, 65535, acceleration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ACCELERATION,
            data=pack_payload((acceleration_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_acceleration(self) -> Decimal:
        """
        Returns the acceleration as set by :func:`set_acceleration`.

        Units: acceleration in %/s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ACCELERATION, response_expected=True
        )
        return PERCENT_PER_SECOND_100_32767.to_si(unpack_payload(payload, "H"))

    async def set_pwm_frequency(self, frequency: float | Decimal = 15000, response_expected: bool = True) -> None:
        """
        Sets the frequency of the PWM with which the motor is driven.
        Often a high frequency
        is less noisy and the motor runs smoother. However, with a low frequency
        there are less switches and therefore fewer switching losses. Also with
        most motors lower frequencies enable higher torque.

        If you have no idea what all this means, just ignore this function and use
        the default frequency, it will very likely work fine.

        Units: frequency in Hz (1 to 20000 Hz).
        """
        frequency_raw = HERTZ.from_si(frequency)
        check_range("frequency", frequency_raw, 1, 20000, frequency)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PWM_FREQUENCY,
            data=pack_payload((frequency_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_pwm_frequency(self) -> Decimal:
        """
        Returns the PWM frequency as set by :func:`set_pwm_frequency`.

        Units: frequency in Hz (1 to 20000 Hz).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_PWM_FREQUENCY, response_expected=True
        )
        return HERTZ.to_si(unpack_payload(payload, "H"))

    async def full_brake(self, response_expected: bool = True) -> None:
        """
        Executes an active full brake.

        .. warning::
         This function is for emergency purposes,
         where an immediate brake is necessary. Depending on the current velocity and
         the strength of the motor, a full brake can be quite violent.

        Call :func:`set_velocity` with 0 if you just want to stop the motor.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.FULL_BRAKE, response_expected=response_expected
        )

    async def get_stack_input_voltage(self) -> Decimal:
        """
        Returns the stack input voltage. The stack input voltage is the
        voltage that is supplied via the stack, i.e. it is given by a
        Step-Down or Step-Up Power Supply.

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_INPUT_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def get_external_input_voltage(self) -> Decimal:
        """
        Returns the external input voltage. The external input voltage is
        given via the black power input connector on the DC Brick.

        If there is an external input voltage and a stack input voltage, the motor
        will be driven by the external input voltage. If there is only a stack
        voltage present, the motor will be driven by this voltage.

        .. warning::
         This means, if you have a high stack voltage and a low external voltage,
         the motor will be driven with the low external voltage. If you then remove
         the external connection, it will immediately be driven by the high
         stack voltage.

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_EXTERNAL_INPUT_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def get_current_consumption(self) -> Decimal:
        """
        Returns the current consumption of the motor.

        Units: voltage in A.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_CONSUMPTION, response_expected=True
        )
        return MILLI_AMPERE.to_si(unpack_payload(payload, "H"))

    async def enable(self, response_expected: bool = True) -> None:
        """
        Enables the driver chip. The driver parameters can be configured (velocity,
        acceleration, etc) before it is enabled.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.ENABLE, response_expected=response_expected)

    async def disable(self, response_expected: bool = True) -> None:
        """
        Disables the driver chip. The configurations are kept (velocity,
        acceleration, etc) but the motor is not driven until it is enabled again.

        .. warning::
         Disabling the driver chip while the motor is still turning can damage the
         driver chip. The motor should be stopped calling :func:`set_velocity` with 0
         before disabling the motor power. The :func:`set_velocity` function will **not**
         wait until the motor is actually stopped. You have to explicitly wait for the
         appropriate time after calling the :func:`set_velocity` function before calling
         the :func:`disable` function.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.DISABLE, response_expected=response_expected)

    async def is_enabled(self) -> bool:
        """
        Returns *true* if the driver chip is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_ENABLED, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def set_minimum_voltage(self, voltage: float | Decimal = 6, response_expected: bool = True) -> None:
        """
        Sets the minimum voltage, below which the :attr:`CallbackID.UNDER_VOLTAGE` callback
        is triggered. The minimum possible value that works with the DC Brick is 6V.
        You can use this function to detect the discharge of a battery that is used
        to drive the motor. If you have a fixed power supply, you likely do not need
        this functionality.

        Units: voltage in V.
        """
        voltage_raw = MILLI_VOLT.from_si(voltage)
        check_range("voltage", voltage_raw, 0, 65535, voltage)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MINIMUM_VOLTAGE,
            data=pack_payload((voltage_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_minimum_voltage(self) -> Decimal:
        """
        Returns the minimum voltage as set by :func:`set_minimum_voltage`

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MINIMUM_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def set_drive_mode(
        self, mode: DriveMode | int = DriveMode.DRIVE_BRAKE, response_expected: bool = True
    ) -> None:
        """
        Sets the drive mode. Possible modes are:

        * 0 = Drive/Brake
        * 1 = Drive/Coast

        These modes are different kinds of motor controls.

        In Drive/Brake mode, the motor is always either driving or braking. There
        is no freewheeling. Advantages are: A more linear correlation between
        PWM and velocity, more exact accelerations and the possibility to drive
        with slower velocities.

        In Drive/Coast mode, the motor is always either driving or freewheeling.
        Advantages are: Less current consumption and less demands on the motor and
        driver chip.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DRIVE_MODE,
            data=pack_payload((DriveMode(mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_drive_mode(self) -> DriveMode:
        """
        Returns the drive mode, as set by :func:`set_drive_mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DRIVE_MODE, response_expected=True
        )
        return DriveMode(unpack_payload(payload, "B"))

    async def set_current_velocity_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets a period with which the :attr:`CallbackID.CURRENT_VELOCITY` callback is triggered.
        A period of 0 turns the callback off.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 65535, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_VELOCITY_PERIOD,
            data=pack_payload((period_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_current_velocity_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_current_velocity_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_VELOCITY_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "H"))

    async def set_spitfp_baudrate_config(
        self,
        enable_dynamic_baudrate: bool = True,
        minimum_dynamic_baudrate: int = 400000,
        response_expected: bool = True,
    ) -> None:
        """
        The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is enabled, the Brick will try
        to adapt the baudrate for the communication between Bricks and Bricklets according to the amount of data that is
        transferred.

        The maximum value of the baudrate can be set per port with the function :func:`set_spitfp_baudrate`. If the
        dynamic baudrate is disabled, the baudrate as set by :func:`set_spitfp_baudrate` will be used statically.
        """
        minimum_dynamic_baudrate = int(minimum_dynamic_baudrate)
        check_range("minimum_dynamic_baudrate", minimum_dynamic_baudrate, 400000, 2000000)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
            data=pack_payload((bool(enable_dynamic_baudrate), minimum_dynamic_baudrate), "! I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate_config(self) -> GetSPITFPBaudrateConfig:
        """
        Returns the baudrate config, see :func:`set_spitfp_baudrate_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPITFP_BAUDRATE_CONFIG, response_expected=True
        )
        enable_dynamic_baudrate, minimum_dynamic_baudrate = unpack_payload(payload, "! I")
        return GetSPITFPBaudrateConfig(enable_dynamic_baudrate, minimum_dynamic_baudrate)

    async def get_send_timeout_count(self, communication_method: CommunicationMethod | int) -> int:
        """
        Returns the timeout count for the different communication methods.

        This function is mostly used for debugging during development, in normal operation the counters should nearly
        always stay at 0.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SEND_TIMEOUT_COUNT,
            data=pack_payload((CommunicationMethod(communication_method).value,), "B"),
            response_expected=True,
        )
        return cast(int, unpack_payload(payload, "I"))

    async def set_spitfp_baudrate(
        self, bricklet_port: Port | str, baudrate: int = 1400000, response_expected: bool = True
    ) -> None:
        """
        Sets the baudrate for a specific Bricklet port. If you want to increase the throughput of Bricklets you can
        increase the baudrate. If you get a high error count because of high interference (see
        :func:`get_spitfp_error_count`) you can decrease the baudrate.
        """
        baudrate = int(baudrate)
        check_range("baudrate", baudrate, 400000, 2000000)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE,
            data=pack_payload((Port(bricklet_port).value, baudrate), "c I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate(self, bricklet_port: Port | str) -> int:
        """
        Returns the baudrate for a given Bricklet port, see :func:`set_spitfp_baudrate`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_BAUDRATE,
            data=pack_payload((Port(bricklet_port).value,), "c"),
            response_expected=True,
        )
        return cast(int, unpack_payload(payload, "I"))

    async def get_spitfp_error_count(self, bricklet_port: Port | str) -> GetSPITFPErrorCount:
        """
        Returns the error count for the communication between Brick and Bricklet. The errors counts are for errors that
        occur on the Brick side.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_ERROR_COUNT,
            data=pack_payload((Port(bricklet_port).value,), "c"),
            response_expected=True,
        )
        error_count_ack_checksum, error_count_message_checksum, error_count_frame, error_count_overflow = (
            unpack_payload(payload, "I I I I")
        )
        return GetSPITFPErrorCount(
            error_count_ack_checksum, error_count_message_checksum, error_count_frame, error_count_overflow
        )

    async def enable_status_led(self, response_expected: bool = True) -> None:
        """
        Enables the status LED. The default state is enabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_STATUS_LED, response_expected=response_expected
        )

    async def disable_status_led(self, response_expected: bool = True) -> None:
        """
        Disables the status LED. The default state is enabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_STATUS_LED, response_expected=response_expected
        )

    async def is_status_led_enabled(self) -> bool:
        """
        Returns *true* if the status LED is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_STATUS_LED_ENABLED, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def get_protocol1_bricklet_name(self, port: Port | str) -> GetProtocol1BrickletName:
        """
        Returns the firmware and protocol version and the name of the Bricklet for a given port.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROTOCOL1_BRICKLET_NAME,
            data=pack_payload((Port(port).value,), "c"),
            response_expected=True,
        )
        protocol_version, firmware_version, name = unpack_payload(payload, "B 3B 40s")
        return GetProtocol1BrickletName(protocol_version, tuple(firmware_version), name)

    @override
    async def get_chip_temperature(self) -> Decimal:
        """
        Returns the temperature as measured inside the microcontroller. The value returned is not the ambient
        temperature!

        The temperature is only proportional to the real temperature and it has an accuracy of ±15%. Practically it is
        only useful as an indicator for temperature changes.

        Units: temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIP_TEMPERATURE, response_expected=True
        )
        return DECI_DEGREE_CELSIUS.to_si(unpack_payload(payload, "h"))

    async def write_bricklet_plugin(
        self, port: Port | str, offset: int, chunk: bytes | Sequence[int], response_expected: bool = True
    ) -> None:
        """
        Writes 32 bytes of firmware to the bricklet attached at the given port. The bytes are written to the position
        offset * 32.

        This function is used by Brick Viewer during flashing. It should not be necessary to call it in a normal user
        program.
        """
        offset = int(offset)
        check_range("offset", offset, 0, 255)
        check_length("chunk", chunk, 32)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.WRITE_BRICKLET_PLUGIN,
            data=pack_payload((Port(port).value, offset, list(map(int, chunk))), "c B 32B"),
            response_expected=response_expected,
        )

    async def read_bricklet_plugin(self, port: Port | str, offset: int) -> tuple[int, ...]:
        """
        Reads 32 bytes of firmware from the bricklet attached at the given port. The bytes are read starting at the
        position offset * 32.

        This function is used by Brick Viewer during flashing. It should not be necessary to call it in a normal user
        program.
        """
        offset = int(offset)
        check_range("offset", offset, 0, 255)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.READ_BRICKLET_PLUGIN,
            data=pack_payload((Port(port).value, offset), "c B"),
            response_expected=True,
        )
        return tuple(unpack_payload(payload, "32B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.UNDER_VOLTAGE:
            return 0, MILLI_VOLT.to_si(value)
        if callback_id is CallbackID.EMERGENCY_SHUTDOWN:
            return 1, None
        if callback_id is CallbackID.VELOCITY_REACHED:
            return 2, PERCENT_100_32767.to_si(value)
        return 3, PERCENT_100_32767.to_si(value)
