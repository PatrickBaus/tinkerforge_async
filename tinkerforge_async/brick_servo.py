"""
Module for the Tinkerforge Servo Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/Servo_Brick_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import BrickletPort as Port
from .devices import Channel, DeviceIdentifier, DeviceWithMCU, GetSPITFPBaudrateConfig, GetSPITFPErrorCount, _FunctionID
from .helper import check_length, check_range
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this brick
    """

    UNDER_VOLTAGE = 26
    POSITION_REACHED = 27
    VELOCITY_REACHED = 28


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """

    ENABLE = 1
    DISABLE = 2
    IS_ENABLED = 3
    SET_POSITION = 4
    GET_POSITION = 5
    GET_CURRENT_POSITION = 6
    SET_VELOCITY = 7
    GET_VELOCITY = 8
    GET_CURRENT_VELOCITY = 9
    SET_ACCELERATION = 10
    GET_ACCELERATION = 11
    SET_OUTPUT_VOLTAGE = 12
    GET_OUTPUT_VOLTAGE = 13
    SET_PULSE_WIDTH = 14
    GET_PULSE_WIDTH = 15
    SET_DEGREE = 16
    GET_DEGREE = 17
    SET_PERIOD = 18
    GET_PERIOD = 19
    GET_SERVO_CURRENT = 20
    GET_OVERALL_CURRENT = 21
    GET_STACK_INPUT_VOLTAGE = 22
    GET_EXTERNAL_INPUT_VOLTAGE = 23
    SET_MINIMUM_VOLTAGE = 24
    GET_MINIMUM_VOLTAGE = 25
    ENABLE_POSITION_REACHED_CALLBACK = 29
    DISABLE_POSITION_REACHED_CALLBACK = 30
    IS_POSITION_REACHED_CALLBACK_ENABLED = 31
    ENABLE_VELOCITY_REACHED_CALLBACK = 32
    DISABLE_VELOCITY_REACHED_CALLBACK = 33
    IS_VELOCITY_REACHED_CALLBACK_ENABLED = 34
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


class GetPulseWidth(NamedTuple):
    minimum: Decimal
    maximum: Decimal


class GetDegree(NamedTuple):
    minimum: Decimal
    maximum: Decimal


class GetProtocol1BrickletName(NamedTuple):
    protocol_version: int
    firmware_version: tuple[int, ...]
    name: str


class PositionReachedEvent(NamedTuple):
    servo_num: int
    position: Decimal


class VelocityReachedEvent(NamedTuple):
    servo_num: int
    velocity: Decimal


CENTI_DEGREE = LinearQuantity(1, 100)  # raw: 1/100 Degree, returned in °
CENTI_DEGREE_PER_SECOND = LinearQuantity(1, 100)  # raw: 1/100 Degree Per Second, returned in °/s
CENTI_DEGREE_PER_SECOND_SQUARED = LinearQuantity(1, 100)  # raw: 1/100 Degree Per Second Squared, returned in °/s²
DECI_DEGREE_CELSIUS = LinearQuantity(1, 10, CELSIUS_ZERO)  # raw: 1/10 Degree Celsius, returned in K
MICRO_SECOND = LinearQuantity(1, 1000000)  # raw: 1/1000000 Second, returned in s
MILLI_AMPERE = LinearQuantity(1, 1000)  # raw: 1/1000 Ampere, returned in A
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickServo(DeviceWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Drives up to 7 RC Servos with up to 3A
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_SERVO
    DEVICE_DISPLAY_NAME = "Servo Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    BrickletPort = Port
    CommunicationMethod: TypeAlias = CommunicationMethod

    CALLBACK_FORMATS = {
        CallbackID.UNDER_VOLTAGE: "H",
        CallbackID.POSITION_REACHED: "B h",
        CallbackID.VELOCITY_REACHED: "B h",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.UNDER_VOLTAGE,)),
        Channel(1, callbacks=(CallbackID.POSITION_REACHED,)),
        Channel(2, callbacks=(CallbackID.VELOCITY_REACHED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 4)

    async def enable(self, servo_num: int, response_expected: bool = True) -> None:
        """
        Enables a servo (0 to 6). If a servo is enabled, the configured position,
        velocity, acceleration, etc. are applied immediately.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.ENABLE,
            data=pack_payload((servo_num,), "B"),
            response_expected=response_expected,
        )

    async def disable(self, servo_num: int, response_expected: bool = True) -> None:
        """
        Disables a servo (0 to 6). Disabled servos are not driven at all, i.e. a
        disabled servo will not hold its position if a load is applied.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.DISABLE,
            data=pack_payload((servo_num,), "B"),
            response_expected=response_expected,
        )

    async def is_enabled(self, servo_num: int) -> bool:
        """
        Returns *true* if the specified servo is enabled, *false* otherwise.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_ENABLED, data=pack_payload((servo_num,), "B"), response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_position(self, servo_num: int, position: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets the position for the specified servo.

        The default range of the position is -9000 to 9000, but it can be specified
        according to your servo with :func:`set_degree`.

        If you want to control a linear servo or RC brushless motor controller or
        similar with the Servo Brick, you can also define lengths or speeds with
        :func:`set_degree`.

        Units: position in °.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 255)
        position_raw = CENTI_DEGREE.from_si(position)
        check_range("position", position_raw, -32768, 32767, position)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POSITION,
            data=pack_payload((servo_num, position_raw), "B h"),
            response_expected=response_expected,
        )

    async def get_position(self, servo_num: int) -> Decimal:
        """
        Returns the position of the specified servo as set by :func:`set_position`.

        Units: position in °.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_POSITION,
            data=pack_payload((servo_num,), "B"),
            response_expected=True,
        )
        return CENTI_DEGREE.to_si(unpack_payload(payload, "h"))

    async def get_current_position(self, servo_num: int) -> Decimal:
        """
        Returns the *current* position of the specified servo. This may not be the
        value of :func:`set_position` if the servo is currently approaching a
        position goal.

        Units: position in °.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CURRENT_POSITION,
            data=pack_payload((servo_num,), "B"),
            response_expected=True,
        )
        return CENTI_DEGREE.to_si(unpack_payload(payload, "h"))

    async def set_velocity(
        self, servo_num: int, velocity: float | Decimal = Decimal("655.35"), response_expected: bool = True
    ) -> None:
        """
        Sets the maximum velocity of the specified servo. The velocity
        is accelerated according to the value set by :func:`set_acceleration`.

        The minimum velocity is 0 (no movement) and the maximum velocity is 65535.
        With a value of 65535 the position will be set immediately (no velocity).

        Units: velocity in °/s.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 255)
        velocity_raw = CENTI_DEGREE_PER_SECOND.from_si(velocity)
        check_range("velocity", velocity_raw, 0, 65535, velocity)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VELOCITY,
            data=pack_payload((servo_num, velocity_raw), "B H"),
            response_expected=response_expected,
        )

    async def get_velocity(self, servo_num: int) -> Decimal:
        """
        Returns the velocity of the specified servo as set by :func:`set_velocity`.

        Units: velocity in °/s.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_VELOCITY,
            data=pack_payload((servo_num,), "B"),
            response_expected=True,
        )
        return CENTI_DEGREE_PER_SECOND.to_si(unpack_payload(payload, "H"))

    async def get_current_velocity(self, servo_num: int) -> Decimal:
        """
        Returns the *current* velocity of the specified servo. This may not be the
        value of :func:`set_velocity` if the servo is currently approaching a
        velocity goal.

        Units: velocity in °/s.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CURRENT_VELOCITY,
            data=pack_payload((servo_num,), "B"),
            response_expected=True,
        )
        return CENTI_DEGREE_PER_SECOND.to_si(unpack_payload(payload, "H"))

    async def set_acceleration(
        self, servo_num: int, acceleration: float | Decimal = Decimal("655.35"), response_expected: bool = True
    ) -> None:
        """
        Sets the acceleration of the specified servo.

        The minimum acceleration is 1 and the maximum acceleration is 65535.
        With a value of 65535 the velocity will be set immediately (no acceleration).

        Units: acceleration in °/s².
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 255)
        acceleration_raw = CENTI_DEGREE_PER_SECOND_SQUARED.from_si(acceleration)
        check_range("acceleration", acceleration_raw, 0, 65535, acceleration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ACCELERATION,
            data=pack_payload((servo_num, acceleration_raw), "B H"),
            response_expected=response_expected,
        )

    async def get_acceleration(self, servo_num: int) -> Decimal:
        """
        Returns the acceleration for the specified servo as set by
        :func:`set_acceleration`.

        Units: acceleration in °/s².
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ACCELERATION,
            data=pack_payload((servo_num,), "B"),
            response_expected=True,
        )
        return CENTI_DEGREE_PER_SECOND_SQUARED.to_si(unpack_payload(payload, "H"))

    async def set_output_voltage(self, voltage: float | Decimal = 5, response_expected: bool = True) -> None:
        """
        Sets the output voltages with which the servos are driven.

        .. note::
         We recommend that you set this value to the maximum voltage that is
         specified for your servo, most servos achieve their maximum force only
         with high voltages.

        Units: voltage in V (2 to 9 V).
        """
        voltage_raw = MILLI_VOLT.from_si(voltage)
        check_range("voltage", voltage_raw, 2000, 9000, voltage)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_OUTPUT_VOLTAGE,
            data=pack_payload((voltage_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_output_voltage(self) -> Decimal:
        """
        Returns the output voltage as specified by :func:`set_output_voltage`.

        Units: voltage in V (2 to 9 V).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OUTPUT_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def set_pulse_width(
        self,
        servo_num: int,
        minimum: float | Decimal = Decimal("0.001"),
        maximum: float | Decimal = Decimal("0.002"),
        response_expected: bool = True,
    ) -> None:
        """
        Sets the minimum and maximum pulse width of the specified servo.

        Usually, servos are controlled with a
        `PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__, whereby the
        length of the pulse controls the position of the servo. Every servo has
        different minimum and maximum pulse widths, these can be specified with
        this function.

        If you have a datasheet for your servo that specifies the minimum and
        maximum pulse width, you should set the values accordingly. If your servo
        comes without any datasheet you have to find the values via trial and error.

        The minimum must be smaller than the maximum.

        Units: minimum in s, maximum in s.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 255)
        minimum_raw = MICRO_SECOND.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = MICRO_SECOND.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PULSE_WIDTH,
            data=pack_payload((servo_num, minimum_raw, maximum_raw), "B H H"),
            response_expected=response_expected,
        )

    async def get_pulse_width(self, servo_num: int) -> GetPulseWidth:
        """
        Returns the minimum and maximum pulse width for the specified servo as set by
        :func:`set_pulse_width`.

        Units: minimum in s, maximum in s.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PULSE_WIDTH,
            data=pack_payload((servo_num,), "B"),
            response_expected=True,
        )
        minimum, maximum = unpack_payload(payload, "H H")
        return GetPulseWidth(MICRO_SECOND.to_si(minimum), MICRO_SECOND.to_si(maximum))

    async def set_degree(
        self,
        servo_num: int,
        minimum: float | Decimal = -90,
        maximum: float | Decimal = 90,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the minimum and maximum degree for the specified servo (by default
        given as °/100).

        This only specifies the abstract values between which the minimum and maximum
        pulse width is scaled. For example: If you specify a pulse width of 1000µs
        to 2000µs and a degree range of -90° to 90°, a call of :func:`set_position`
        with 0 will result in a pulse width of 1500µs
        (-90° = 1000µs, 90° = 2000µs, etc.).

        Possible usage:

        * The datasheet of your servo specifies a range of 200° with the middle position
          at 110°. In this case you can set the minimum to -9000 and the maximum to 11000.
        * You measure a range of 220° on your servo and you don't have or need a middle
          position. In this case you can set the minimum to 0 and the maximum to 22000.
        * You have a linear servo with a drive length of 0.2 m, In this case you could
          set the minimum to 0 and the maximum to 20000. Now you can set the Position
          with :func:`set_position` with a resolution of cm/100. Also the velocity will
          have a resolution of cm/100s and the acceleration will have a resolution of
          cm/100s².
        * You don't care about units and just want the highest possible resolution. In
          this case you should set the minimum to -32767 and the maximum to 32767.
        * You have a brushless motor with a maximum speed of 10000 rpm and want to
          control it with a RC brushless motor controller. In this case you can set the
          minimum to 0 and the maximum to 10000. :func:`set_position` now controls the rpm.

        The minimum must be smaller than the maximum.

        Units: minimum in °, maximum in °.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 255)
        minimum_raw = CENTI_DEGREE.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = CENTI_DEGREE.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEGREE,
            data=pack_payload((servo_num, minimum_raw, maximum_raw), "B h h"),
            response_expected=response_expected,
        )

    async def get_degree(self, servo_num: int) -> GetDegree:
        """
        Returns the minimum and maximum degree for the specified servo as set by
        :func:`set_degree`.

        Units: minimum in °, maximum in °.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEGREE, data=pack_payload((servo_num,), "B"), response_expected=True
        )
        minimum, maximum = unpack_payload(payload, "h h")
        return GetDegree(CENTI_DEGREE.to_si(minimum), CENTI_DEGREE.to_si(maximum))

    async def set_period(
        self, servo_num: int, period: float | Decimal = Decimal("0.0195"), response_expected: bool = True
    ) -> None:
        """
        Sets the period of the specified servo.

        Usually, servos are controlled with a
        `PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__. Different
        servos expect PWMs with different periods. Most servos run well with a
        period of about 20ms.

        If your servo comes with a datasheet that specifies a period, you should
        set it accordingly. If you don't have a datasheet and you have no idea
        what the correct period is, the default value will most likely
        work fine.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 255)
        period_raw = MICRO_SECOND.from_si(period)
        check_range("period", period_raw, 0, 65535, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PERIOD,
            data=pack_payload((servo_num, period_raw), "B H"),
            response_expected=response_expected,
        )

    async def get_period(self, servo_num: int) -> Decimal:
        """
        Returns the period for the specified servo as set by :func:`set_period`.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_PERIOD, data=pack_payload((servo_num,), "B"), response_expected=True
        )
        return MICRO_SECOND.to_si(unpack_payload(payload, "H"))

    async def get_servo_current(self, servo_num: int) -> Decimal:
        """
        Returns the current consumption of the specified servo.

        Units: current in A.
        """
        servo_num = int(servo_num)
        check_range("servo_num", servo_num, 0, 6)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SERVO_CURRENT,
            data=pack_payload((servo_num,), "B"),
            response_expected=True,
        )
        return MILLI_AMPERE.to_si(unpack_payload(payload, "H"))

    async def get_overall_current(self) -> Decimal:
        """
        Returns the current consumption of all servos together.

        Units: current in A.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OVERALL_CURRENT, response_expected=True
        )
        return MILLI_AMPERE.to_si(unpack_payload(payload, "H"))

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
        given via the black power input connector on the Servo Brick.

        If there is an external input voltage and a stack input voltage, the motors
        will be driven by the external input voltage. If there is only a stack
        voltage present, the motors will be driven by this voltage.

        .. warning::
         This means, if you have a high stack voltage and a low external voltage,
         the motors will be driven with the low external voltage. If you then remove
         the external connection, it will immediately be driven by the high
         stack voltage

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_EXTERNAL_INPUT_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def set_minimum_voltage(self, voltage: float | Decimal = 5, response_expected: bool = True) -> None:
        """
        Sets the minimum voltage, below which the :attr:`CallbackID.UNDER_VOLTAGE` callback
        is triggered. The minimum possible value that works with the Servo Brick is 5V.
        You can use this function to detect the discharge of a battery that is used
        to drive the stepper motor. If you have a fixed power supply, you likely do
        not need this functionality.

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

    async def enable_position_reached_callback(self, response_expected: bool = True) -> None:
        """
        Enables the :attr:`CallbackID.POSITION_REACHED` callback.

        Default is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_POSITION_REACHED_CALLBACK, response_expected=response_expected
        )

    async def disable_position_reached_callback(self, response_expected: bool = True) -> None:
        """
        Disables the :attr:`CallbackID.POSITION_REACHED` callback.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_POSITION_REACHED_CALLBACK, response_expected=response_expected
        )

    async def is_position_reached_callback_enabled(self) -> bool:
        """
        Returns *true* if :attr:`CallbackID.POSITION_REACHED` callback is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_POSITION_REACHED_CALLBACK_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def enable_velocity_reached_callback(self, response_expected: bool = True) -> None:
        """
        Enables the :attr:`CallbackID.VELOCITY_REACHED` callback.

        Default is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_VELOCITY_REACHED_CALLBACK, response_expected=response_expected
        )

    async def disable_velocity_reached_callback(self, response_expected: bool = True) -> None:
        """
        Disables the :attr:`CallbackID.VELOCITY_REACHED` callback.

        Default is disabled.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_VELOCITY_REACHED_CALLBACK, response_expected=response_expected
        )

    async def is_velocity_reached_callback_enabled(self) -> bool:
        """
        Returns *true* if :attr:`CallbackID.VELOCITY_REACHED` callback is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_VELOCITY_REACHED_CALLBACK_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

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
        return unpack_payload(payload, "I")

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
        return unpack_payload(payload, "I")

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
        return unpack_payload(payload, "!")

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
        if callback_id is CallbackID.POSITION_REACHED:
            servo_num, position = value
            return 1, PositionReachedEvent(servo_num, CENTI_DEGREE.to_si(position))
        servo_num, velocity = value
        return 2, VelocityReachedEvent(servo_num, CENTI_DEGREE_PER_SECOND.to_si(velocity))
