"""
Module for the Tinkerforge Servo Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/ServoV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import BrickletWithMCU, Channel, DeviceIdentifier, _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    POSITION_REACHED = 27


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_STATUS = 1
    SET_ENABLE = 2
    GET_ENABLED = 3
    SET_POSITION = 4
    GET_POSITION = 5
    GET_CURRENT_POSITION = 6
    GET_CURRENT_VELOCITY = 7
    SET_MOTION_CONFIGURATION = 8
    GET_MOTION_CONFIGURATION = 9
    SET_PULSE_WIDTH = 10
    GET_PULSE_WIDTH = 11
    SET_DEGREE = 12
    GET_DEGREE = 13
    SET_PERIOD = 14
    GET_PERIOD = 15
    GET_SERVO_CURRENT = 16
    SET_SERVO_CURRENT_CONFIGURATION = 17
    GET_SERVO_CURRENT_CONFIGURATION = 18
    SET_INPUT_VOLTAGE_CONFIGURATION = 19
    GET_INPUT_VOLTAGE_CONFIGURATION = 20
    GET_OVERALL_CURRENT = 21
    GET_INPUT_VOLTAGE = 22
    SET_CURRENT_CALIBRATION = 23
    GET_CURRENT_CALIBRATION = 24
    SET_POSITION_REACHED_CALLBACK_CONFIGURATION = 25
    GET_POSITION_REACHED_CALLBACK_CONFIGURATION = 26


class GetStatus(NamedTuple):
    enabled: tuple[bool, ...]
    current_position: tuple[Decimal, ...]
    current_velocity: tuple[Decimal, ...]
    current: tuple[Decimal, ...]
    input_voltage: Decimal


class GetMotionConfiguration(NamedTuple):
    velocity: Decimal
    acceleration: Decimal
    deceleration: Decimal


class GetPulseWidth(NamedTuple):
    minimum: Decimal
    maximum: Decimal


class GetDegree(NamedTuple):
    minimum: Decimal
    maximum: Decimal


class PositionReachedEvent(NamedTuple):
    servo_channel: int
    position: Decimal


ACCELERATION = LinearQuantity(1, 100)  # raw: 1/100 Degree Per Second Squared, returned in °/s²
ANGLE = LinearQuantity(1, 100)  # raw: 1/100 Degree, returned in °
CURRENT = LinearQuantity(1, 1000)  # raw: 1/1000 Ampere, returned in A
CURRENT_POSITION = LinearQuantity(1, 100)  # raw: 1/100 Degree, returned in °
CURRENT_VELOCITY = LinearQuantity(1, 100)  # raw: 1/100 Degree Per Second, returned in °/s
DECELERATION = LinearQuantity(1, 100)  # raw: 1/100 Degree Per Second Squared, returned in °/s²
INPUT_VOLTAGE = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V
OFFSET = LinearQuantity(1, 1000)  # raw: 1/1000 Ampere, returned in A
PERIOD = LinearQuantity(1, 1000000)  # raw: 1/1000000 Second, returned in s
POSITION = LinearQuantity(1, 100)  # raw: 1/100 Degree, returned in °
TIME = LinearQuantity(1, 1000000)  # raw: 1/1000000 Second, returned in s
VELOCITY = LinearQuantity(1, 100)  # raw: 1/100 Degree Per Second, returned in °/s
VOLTAGE = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletServoV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Drives up to 10 RC Servos
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_SERVO_V2
    DEVICE_DISPLAY_NAME = "Servo Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.POSITION_REACHED: "H h",
    }

    CHANNELS = (Channel(0, callbacks=(CallbackID.POSITION_REACHED,)),)

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_status(self) -> GetStatus:
        """
        Returns the status information of the Servo Bricklet 2.0.

        The status includes

        * for each channel if it is enabled or disabled,
        * for each channel the current position,
        * for each channel the current velocity,
        * for each channel the current usage and
        * the input voltage.

        Please note that the position and the velocity is a snapshot of the
        current position and velocity of the servo in motion.

        Units: current_position in °, current_velocity in °/s (0 to 5000 °/s), current in A, input_voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATUS, response_expected=True
        )
        enabled, current_position, current_velocity, current, input_voltage = unpack_payload(
            payload, "10! 10h 10h 10H H"
        )
        return GetStatus(
            tuple(enabled),
            tuple(CURRENT_POSITION.to_si(item) for item in current_position),
            tuple(CURRENT_VELOCITY.to_si(item) for item in current_velocity),
            tuple(CURRENT.to_si(item) for item in current),
            INPUT_VOLTAGE.to_si(input_voltage),
        )

    async def set_enable(self, servo_channel: int, enable: bool = False, response_expected: bool = True) -> None:
        """
        Enables a servo channel (0 to 9). If a servo is enabled, the configured position,
        velocity, acceleration, etc. are applied immediately.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ENABLE,
            data=pack_payload((servo_channel, bool(enable)), "H !"),
            response_expected=response_expected,
        )

    async def get_enabled(self, servo_channel: int) -> bool:
        """
        Returns *true* if the specified servo channel is enabled, *false* otherwise.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ENABLED,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        return unpack_payload(payload, "!")

    async def set_position(self, servo_channel: int, position: float | Decimal, response_expected: bool = True) -> None:
        """
        Sets the position in °/100 for the specified servo channel.

        The default range of the position is -9000 to 9000, but it can be specified
        according to your servo with :func:`set_degree`.

        If you want to control a linear servo or RC brushless motor controller or
        similar with the Servo Brick, you can also define lengths or speeds with
        :func:`set_degree`.

        Units: position in °.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 65535)
        position_raw = POSITION.from_si(position)
        check_range("position", position_raw, -32768, 32767, position)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POSITION,
            data=pack_payload((servo_channel, position_raw), "H h"),
            response_expected=response_expected,
        )

    async def get_position(self, servo_channel: int) -> Decimal:
        """
        Returns the position of the specified servo channel as set by :func:`set_position`.

        Units: position in °.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_POSITION,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        return POSITION.to_si(unpack_payload(payload, "h"))

    async def get_current_position(self, servo_channel: int) -> Decimal:
        """
        Returns the *current* position of the specified servo channel. This may not be the
        value of :func:`set_position` if the servo is currently approaching a
        position goal.

        Units: position in °.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CURRENT_POSITION,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        return POSITION.to_si(unpack_payload(payload, "h"))

    async def get_current_velocity(self, servo_channel: int) -> Decimal:
        """
        Returns the *current* velocity of the specified servo channel. This may not be the
        velocity specified by :func:`set_motion_configuration`. if the servo is
        currently approaching a velocity goal.

        Units: velocity in °/s (0 to 5000 °/s).
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CURRENT_VELOCITY,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        return VELOCITY.to_si(unpack_payload(payload, "H"))

    async def set_motion_configuration(
        self,
        servo_channel: int,
        velocity: float | Decimal = 1000,
        acceleration: float | Decimal = 500,
        deceleration: float | Decimal = 500,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the maximum velocity of the specified servo channel in °/100s as well as
        the acceleration and deceleration in °/100s²

        With a velocity of 0 °/100s the position will be set immediately (no velocity).

        With an acc-/deceleration of 0 °/100s² the velocity will be set immediately
        (no acc-/deceleration).

        Units: velocity in °/s (0 to 5000 °/s), acceleration in °/s² (0 to 5000 °/s²), deceleration in °/s² (0 to 5000
        °/s²).
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 65535)
        velocity_raw = VELOCITY.from_si(velocity)
        check_range("velocity", velocity_raw, 0, 500000, velocity)
        acceleration_raw = ACCELERATION.from_si(acceleration)
        check_range("acceleration", acceleration_raw, 0, 500000, acceleration)
        deceleration_raw = DECELERATION.from_si(deceleration)
        check_range("deceleration", deceleration_raw, 0, 500000, deceleration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOTION_CONFIGURATION,
            data=pack_payload((servo_channel, velocity_raw, acceleration_raw, deceleration_raw), "H I I I"),
            response_expected=response_expected,
        )

    async def get_motion_configuration(self, servo_channel: int) -> GetMotionConfiguration:
        """
        Returns the motion configuration as set by :func:`set_motion_configuration`.

        Units: velocity in °/s (0 to 5000 °/s), acceleration in °/s² (0 to 5000 °/s²), deceleration in °/s² (0 to 5000
        °/s²).
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_MOTION_CONFIGURATION,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        velocity, acceleration, deceleration = unpack_payload(payload, "I I I")
        return GetMotionConfiguration(
            VELOCITY.to_si(velocity), ACCELERATION.to_si(acceleration), DECELERATION.to_si(deceleration)
        )

    async def set_pulse_width(
        self,
        servo_channel: int,
        minimum: float | Decimal = Decimal("0.001"),
        maximum: float | Decimal = Decimal("0.002"),
        response_expected: bool = True,
    ) -> None:
        """
        Sets the minimum and maximum pulse width of the specified servo channel in µs.

        Usually, servos are controlled with a
        `PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__, whereby the
        length of the pulse controls the position of the servo. Every servo has
        different minimum and maximum pulse widths, these can be specified with
        this function.

        If you have a datasheet for your servo that specifies the minimum and
        maximum pulse width, you should set the values accordingly. If your servo
        comes without any datasheet you have to find the values via trial and error.

        Both values have a range from 1 to 65535 (unsigned 16-bit integer). The
        minimum must be smaller than the maximum.

        The default values are 1000µs (1ms) and 2000µs (2ms) for minimum and
        maximum pulse width.

        Units: minimum in s, maximum in s.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 65535)
        minimum_raw = TIME.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 4294967295, minimum)
        maximum_raw = TIME.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 4294967295, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PULSE_WIDTH,
            data=pack_payload((servo_channel, minimum_raw, maximum_raw), "H I I"),
            response_expected=response_expected,
        )

    async def get_pulse_width(self, servo_channel: int) -> GetPulseWidth:
        """
        Returns the minimum and maximum pulse width for the specified servo channel as set by
        :func:`set_pulse_width`.

        Units: minimum in s, maximum in s.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PULSE_WIDTH,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        minimum, maximum = unpack_payload(payload, "I I")
        return GetPulseWidth(TIME.to_si(minimum), TIME.to_si(maximum))

    async def set_degree(
        self,
        servo_channel: int,
        minimum: float | Decimal = -90,
        maximum: float | Decimal = 90,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the minimum and maximum degree for the specified servo channel (by default
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

        Both values have a possible range from -32767 to 32767
        (signed 16-bit integer). The minimum must be smaller than the maximum.

        The default values are -9000 and 9000 for the minimum and maximum degree.

        Units: minimum in °, maximum in °.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 65535)
        minimum_raw = ANGLE.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = ANGLE.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEGREE,
            data=pack_payload((servo_channel, minimum_raw, maximum_raw), "H h h"),
            response_expected=response_expected,
        )

    async def get_degree(self, servo_channel: int) -> GetDegree:
        """
        Returns the minimum and maximum degree for the specified servo channel as set by
        :func:`set_degree`.

        Units: minimum in °, maximum in °.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_DEGREE,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        minimum, maximum = unpack_payload(payload, "h h")
        return GetDegree(ANGLE.to_si(minimum), ANGLE.to_si(maximum))

    async def set_period(
        self, servo_channel: int, period: float | Decimal = Decimal("0.0195"), response_expected: bool = True
    ) -> None:
        """
        Sets the period of the specified servo channel in µs.

        Usually, servos are controlled with a
        `PWM <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__. Different
        servos expect PWMs with different periods. Most servos run well with a
        period of about 20ms.

        If your servo comes with a datasheet that specifies a period, you should
        set it accordingly. If you don't have a datasheet and you have no idea
        what the correct period is, the default value (19.5ms) will most likely
        work fine.

        The minimum possible period is 1µs and the maximum is 1000000µs.

        The default value is 19.5ms (19500µs).
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 65535)
        period_raw = PERIOD.from_si(period)
        check_range("period", period_raw, 1, 1000000, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PERIOD,
            data=pack_payload((servo_channel, period_raw), "H I"),
            response_expected=response_expected,
        )

    async def get_period(self, servo_channel: int) -> Decimal:
        """
        Returns the period for the specified servo channel as set by :func:`set_period`.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PERIOD,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        return PERIOD.to_si(unpack_payload(payload, "I"))

    async def get_servo_current(self, servo_channel: int) -> Decimal:
        """
        Returns the current consumption of the specified servo channel in A.

        Units: current in A.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SERVO_CURRENT,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        return CURRENT.to_si(unpack_payload(payload, "H"))

    async def set_servo_current_configuration(
        self, servo_channel: int, averaging_duration: Duration = Decimal("0.255"), response_expected: bool = True
    ) -> None:
        """
        Sets the averaging duration of the current measurement for the specified servo channel in ms.

        Units: averaging_duration in s (0.001 to 0.255 s).
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 65535)
        averaging_duration_raw = seconds_to_ms(averaging_duration)
        check_range("averaging_duration", averaging_duration_raw, 1, 255, averaging_duration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SERVO_CURRENT_CONFIGURATION,
            data=pack_payload((servo_channel, averaging_duration_raw), "H B"),
            response_expected=response_expected,
        )

    async def get_servo_current_configuration(self, servo_channel: int) -> Decimal:
        """
        Returns the servo current configuration for the specified servo channel as set
        by :func:`set_servo_current_configuration`.

        Units: averaging_duration in s (0.001 to 0.255 s).
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SERVO_CURRENT_CONFIGURATION,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        return ms_to_seconds(unpack_payload(payload, "B"))

    async def set_input_voltage_configuration(
        self, averaging_duration: Duration = Decimal("0.255"), response_expected: bool = True
    ) -> None:
        """
        Sets the averaging duration of the input voltage measurement for the specified servo channel in ms.

        Units: averaging_duration in s (0.001 to 0.255 s).
        """
        averaging_duration_raw = seconds_to_ms(averaging_duration)
        check_range("averaging_duration", averaging_duration_raw, 1, 255, averaging_duration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_INPUT_VOLTAGE_CONFIGURATION,
            data=pack_payload((averaging_duration_raw,), "B"),
            response_expected=response_expected,
        )

    async def get_input_voltage_configuration(self) -> Decimal:
        """
        Returns the input voltage configuration as set by :func:`set_input_voltage_configuration`.

        Units: averaging_duration in s (0.001 to 0.255 s).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_INPUT_VOLTAGE_CONFIGURATION, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "B"))

    async def get_overall_current(self) -> Decimal:
        """
        Returns the current consumption of all servos together in A.

        Units: current in A.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OVERALL_CURRENT, response_expected=True
        )
        return CURRENT.to_si(unpack_payload(payload, "H"))

    async def get_input_voltage(self) -> Decimal:
        """
        Returns the input voltage in V. The input voltage is
        given via the black power input connector on the Servo Brick.

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_INPUT_VOLTAGE, response_expected=True
        )
        return VOLTAGE.to_si(unpack_payload(payload, "H"))

    async def set_current_calibration(self, offset: Sequence[float | Decimal], response_expected: bool = True) -> None:
        """
        Sets an offset value (in A) for each channel.

        Note: On delivery the Servo Bricklet 2.0 is already calibrated.

        Units: offset in A.
        """
        check_length("offset", offset, 10)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_CALIBRATION,
            data=pack_payload(([OFFSET.from_si(item) for item in offset],), "10h"),
            response_expected=response_expected,
        )

    async def get_current_calibration(self) -> tuple[Decimal, ...]:
        """
        Returns the current calibration as set by :func:`set_current_calibration`.

        Units: offset in A.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_CALIBRATION, response_expected=True
        )
        return tuple(OFFSET.to_si(item) for item in unpack_payload(payload, "10h"))

    async def set_position_reached_callback_configuration(
        self, servo_channel: int, enabled: bool = False, response_expected: bool = True
    ) -> None:
        """
        Enable/Disable :attr:`CallbackID.POSITION_REACHED` callback.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POSITION_REACHED_CALLBACK_CONFIGURATION,
            data=pack_payload((servo_channel, bool(enabled)), "H !"),
            response_expected=response_expected,
        )

    async def get_position_reached_callback_configuration(self, servo_channel: int) -> bool:
        """
        Returns the callback configuration as set by
        :func:`set_position_reached_callback_configuration`.
        """
        servo_channel = int(servo_channel)
        check_range("servo_channel", servo_channel, 0, 9)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_POSITION_REACHED_CALLBACK_CONFIGURATION,
            data=pack_payload((servo_channel,), "H"),
            response_expected=True,
        )
        return unpack_payload(payload, "!")

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        servo_channel, position = value
        return 0, PositionReachedEvent(servo_channel, POSITION.to_si(position))
