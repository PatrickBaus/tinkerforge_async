"""
Module for the Tinkerforge Stepper Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/Stepper_Brick_Python.html) implemented using
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

    UNDER_VOLTAGE = 31
    POSITION_REACHED = 32
    ALL_DATA = 40
    NEW_STATE = 41


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """

    SET_MAX_VELOCITY = 1
    GET_MAX_VELOCITY = 2
    GET_CURRENT_VELOCITY = 3
    SET_SPEED_RAMPING = 4
    GET_SPEED_RAMPING = 5
    FULL_BRAKE = 6
    SET_CURRENT_POSITION = 7
    GET_CURRENT_POSITION = 8
    SET_TARGET_POSITION = 9
    GET_TARGET_POSITION = 10
    SET_STEPS = 11
    GET_STEPS = 12
    GET_REMAINING_STEPS = 13
    SET_STEP_MODE = 14
    GET_STEP_MODE = 15
    DRIVE_FORWARD = 16
    DRIVE_BACKWARD = 17
    STOP = 18
    GET_STACK_INPUT_VOLTAGE = 19
    GET_EXTERNAL_INPUT_VOLTAGE = 20
    GET_CURRENT_CONSUMPTION = 21
    SET_MOTOR_CURRENT = 22
    GET_MOTOR_CURRENT = 23
    ENABLE = 24
    DISABLE = 25
    IS_ENABLED = 26
    SET_DECAY = 27
    GET_DECAY = 28
    SET_MINIMUM_VOLTAGE = 29
    GET_MINIMUM_VOLTAGE = 30
    SET_SYNC_RECT = 33
    IS_SYNC_RECT = 34
    SET_TIME_BASE = 35
    GET_TIME_BASE = 36
    GET_ALL_DATA = 37
    SET_ALL_DATA_PERIOD = 38
    GET_ALL_DATA_PERIOD = 39
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
class StepMode(Enum):
    """
    The step mode options
    """

    FULL_STEP = 1
    HALF_STEP = 2
    QUARTER_STEP = 4
    EIGHTH_STEP = 8


@unique
class State(Enum):
    """
    The state options
    """

    STOP = 1
    ACCELERATION = 2
    RUN = 3
    DEACCELERATION = 4
    DIRECTION_CHANGE_TO_FORWARD = 5
    DIRECTION_CHANGE_TO_BACKWARD = 6


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


class GetSpeedRamping(NamedTuple):
    acceleration: int
    deacceleration: int


class GetAllData(NamedTuple):
    current_velocity: int
    current_position: int
    remaining_steps: int
    stack_voltage: Decimal
    external_voltage: Decimal
    current_consumption: Decimal


class GetProtocol1BrickletName(NamedTuple):
    protocol_version: int
    firmware_version: tuple[int, ...]
    name: str


class NewStateEvent(NamedTuple):
    state_new: State
    state_previous: State


DECI_DEGREE_CELSIUS = LinearQuantity(1, 10, CELSIUS_ZERO)  # raw: 1/10 Degree Celsius, returned in K
MILLI_AMPERE = LinearQuantity(1, 1000)  # raw: 1/1000 Ampere, returned in A
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V
SECOND = LinearQuantity(1)  # raw: 1/1 Second, returned in s


class BrickStepper(DeviceWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Drives one bipolar stepper motor with up to 38V and 2.5A per phase
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_STEPPER
    DEVICE_DISPLAY_NAME = "Stepper Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    BrickletPort = Port
    StepMode: TypeAlias = StepMode
    State: TypeAlias = State
    CommunicationMethod: TypeAlias = CommunicationMethod

    CALLBACK_FORMATS = {
        CallbackID.UNDER_VOLTAGE: "H",
        CallbackID.POSITION_REACHED: "i",
        CallbackID.ALL_DATA: "H i i H H H",
        CallbackID.NEW_STATE: "B B",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.UNDER_VOLTAGE,)),
        Channel(1, callbacks=(CallbackID.POSITION_REACHED,)),
        Channel(2, callbacks=(CallbackID.ALL_DATA,)),
        Channel(3, callbacks=(CallbackID.NEW_STATE,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 4)

    async def set_max_velocity(self, velocity: int, response_expected: bool = True) -> None:
        """
        Sets the maximum velocity of the stepper motor.
        This function does *not* start the motor, it merely sets the maximum
        velocity the stepper motor is accelerated to. To get the motor running use
        either :func:`set_target_position`, :func:`set_steps`, :func:`drive_forward` or
        :func:`drive_backward`.
        """
        velocity = int(velocity)
        check_range("velocity", velocity, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MAX_VELOCITY,
            data=pack_payload((velocity,), "H"),
            response_expected=response_expected,
        )

    async def get_max_velocity(self) -> int:
        """
        Returns the velocity as set by :func:`set_max_velocity`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAX_VELOCITY, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def get_current_velocity(self) -> int:
        """
        Returns the *current* velocity of the stepper motor.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_VELOCITY, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_speed_ramping(
        self, acceleration: int = 1000, deacceleration: int = 1000, response_expected: bool = True
    ) -> None:
        """
        Sets the acceleration and deacceleration of the stepper motor.
        An acceleration of 1000 means, that
        every second the velocity is increased by 1000 *steps/s*.

        For example: If the current velocity is 0 and you want to accelerate to a
        velocity of 8000 *steps/s* in 10 seconds, you should set an acceleration
        of 800 *steps/s²*.

        An acceleration/deacceleration of 0 means instantaneous
        acceleration/deacceleration (not recommended)
        """
        acceleration = int(acceleration)
        check_range("acceleration", acceleration, 0, 65535)
        deacceleration = int(deacceleration)
        check_range("deacceleration", deacceleration, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPEED_RAMPING,
            data=pack_payload((acceleration, deacceleration), "H H"),
            response_expected=response_expected,
        )

    async def get_speed_ramping(self) -> GetSpeedRamping:
        """
        Returns the acceleration and deacceleration as set by
        :func:`set_speed_ramping`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPEED_RAMPING, response_expected=True
        )
        acceleration, deacceleration = unpack_payload(payload, "H H")
        return GetSpeedRamping(acceleration, deacceleration)

    async def full_brake(self, response_expected: bool = True) -> None:
        """
        Executes an active full brake.

        .. warning::
         This function is for emergency purposes,
         where an immediate brake is necessary. Depending on the current velocity and
         the strength of the motor, a full brake can be quite violent.

        Call :func:`stop` if you just want to stop the motor.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.FULL_BRAKE, response_expected=response_expected
        )

    async def set_current_position(self, position: int, response_expected: bool = True) -> None:
        """
        Sets the current steps of the internal step counter. This can be used to
        set the current position to 0 when some kind of starting position
        is reached (e.g. when a CNC machine reaches a corner).
        """
        position = int(position)
        check_range("position", position, -2147483648, 2147483647)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_POSITION,
            data=pack_payload((position,), "i"),
            response_expected=response_expected,
        )

    async def get_current_position(self) -> int:
        """
        Returns the current position of the stepper motor in steps. On startup
        the position is 0. The steps are counted with all possible driving
        functions (:func:`set_target_position`, :func:`set_steps`, :func:`drive_forward` or
        :func:`drive_backward`). It also is possible to reset the steps to 0 or
        set them to any other desired value with :func:`set_current_position`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_POSITION, response_expected=True
        )
        return unpack_payload(payload, "i")

    async def set_target_position(self, position: int, response_expected: bool = True) -> None:
        """
        Sets the target position of the stepper motor in steps. For example,
        if the current position of the motor is 500 and :func:`set_target_position` is
        called with 1000, the stepper motor will drive 500 steps forward. It will
        use the velocity, acceleration and deacceleration as set by
        :func:`set_max_velocity` and :func:`set_speed_ramping`.

        A call of :func:`set_target_position` with the parameter *x* is equivalent to
        a call of :func:`set_steps` with the parameter
        (*x* - :func:`get_current_position`).
        """
        position = int(position)
        check_range("position", position, -2147483648, 2147483647)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TARGET_POSITION,
            data=pack_payload((position,), "i"),
            response_expected=response_expected,
        )

    async def get_target_position(self) -> int:
        """
        Returns the last target position as set by :func:`set_target_position`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TARGET_POSITION, response_expected=True
        )
        return unpack_payload(payload, "i")

    async def set_steps(self, steps: int, response_expected: bool = True) -> None:
        """
        Sets the number of steps the stepper motor should run. Positive values
        will drive the motor forward and negative values backward.
        The velocity, acceleration and deacceleration as set by
        :func:`set_max_velocity` and :func:`set_speed_ramping` will be used.
        """
        steps = int(steps)
        check_range("steps", steps, -2147483648, 2147483647)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STEPS,
            data=pack_payload((steps,), "i"),
            response_expected=response_expected,
        )

    async def get_steps(self) -> int:
        """
        Returns the last steps as set by :func:`set_steps`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STEPS, response_expected=True
        )
        return unpack_payload(payload, "i")

    async def get_remaining_steps(self) -> int:
        """
        Returns the remaining steps of the last call of :func:`set_steps`.
        For example, if :func:`set_steps` is called with 2000 and
        :func:`get_remaining_steps` is called after the motor has run for 500 steps,
        it will return 1500.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_REMAINING_STEPS, response_expected=True
        )
        return unpack_payload(payload, "i")

    async def set_step_mode(self, mode: StepMode | int = StepMode.EIGHTH_STEP, response_expected: bool = True) -> None:
        """
        Sets the step mode of the stepper motor. Possible values are:

        * Full Step = 1
        * Half Step = 2
        * Quarter Step = 4
        * Eighth Step = 8

        A higher value will increase the resolution and
        decrease the torque of the stepper motor.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STEP_MODE,
            data=pack_payload((StepMode(mode).value,), "B"),
            response_expected=response_expected,
        )

    async def get_step_mode(self) -> StepMode:
        """
        Returns the step mode as set by :func:`set_step_mode`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STEP_MODE, response_expected=True
        )
        return StepMode(unpack_payload(payload, "B"))

    async def drive_forward(self, response_expected: bool = True) -> None:
        """
        Drives the stepper motor forward until :func:`drive_backward` or
        :func:`stop` is called. The velocity, acceleration and deacceleration as
        set by :func:`set_max_velocity` and :func:`set_speed_ramping` will be used.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DRIVE_FORWARD, response_expected=response_expected
        )

    async def drive_backward(self, response_expected: bool = True) -> None:
        """
        Drives the stepper motor backward until :func:`drive_forward` or
        :func:`stop` is triggered. The velocity, acceleration and deacceleration as
        set by :func:`set_max_velocity` and :func:`set_speed_ramping` will be used.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DRIVE_BACKWARD, response_expected=response_expected
        )

    async def stop(self, response_expected: bool = True) -> None:
        """
        Stops the stepper motor with the deacceleration as set by
        :func:`set_speed_ramping`.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.STOP, response_expected=response_expected)

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
        given via the black power input connector on the Stepper Brick.

        If there is an external input voltage and a stack input voltage, the motor
        will be driven by the external input voltage. If there is only a stack
        voltage present, the motor will be driven by this voltage.

        .. warning::
         This means, if you have a high stack voltage and a low external voltage,
         the motor will be driven with the low external voltage. If you then remove
         the external connection, it will immediately be driven by the high
         stack voltage

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_EXTERNAL_INPUT_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def get_current_consumption(self) -> Decimal:
        """
        Returns the current consumption of the motor.

        Units: current in A.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_CONSUMPTION, response_expected=True
        )
        return MILLI_AMPERE.to_si(unpack_payload(payload, "H"))

    async def set_motor_current(
        self, current: float | Decimal = Decimal("0.8"), response_expected: bool = True
    ) -> None:
        """
        Sets the current with which the motor will be driven.

        .. warning::
         Do not set this value above the specifications of your stepper motor.
         Otherwise it may damage your motor.

        Units: current in A (0.1 to 2.291 A).
        """
        current_raw = MILLI_AMPERE.from_si(current)
        check_range("current", current_raw, 100, 2291, current)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOTOR_CURRENT,
            data=pack_payload((current_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_motor_current(self) -> Decimal:
        """
        Returns the current as set by :func:`set_motor_current`.

        Units: current in A (0.1 to 2.291 A).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOTOR_CURRENT, response_expected=True
        )
        return MILLI_AMPERE.to_si(unpack_payload(payload, "H"))

    async def enable(self, response_expected: bool = True) -> None:
        """
        Enables the driver chip. The driver parameters can be configured (maximum velocity,
        acceleration, etc) before it is enabled.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.ENABLE, response_expected=response_expected)

    async def disable(self, response_expected: bool = True) -> None:
        """
        Disables the driver chip. The configurations are kept (maximum velocity,
        acceleration, etc) but the motor is not driven until it is enabled again.

        .. warning::
         Disabling the driver chip while the motor is still turning can damage the
         driver chip. The motor should be stopped calling :func:`stop` function
         before disabling the motor power. The :func:`stop` function will **not**
         wait until the motor is actually stopped. You have to explicitly wait for the
         appropriate time after calling the :func:`stop` function before calling
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
        return unpack_payload(payload, "!")

    async def set_decay(self, decay: int = 10000, response_expected: bool = True) -> None:
        """
        Sets the decay mode of the stepper motor.
        A value of 0 sets the fast decay mode, a value of
        65535 sets the slow decay mode and a value in between sets the mixed
        decay mode.

        Changing the decay mode is only possible if synchronous rectification
        is enabled (see :func:`set_sync_rect`).

        For a good explanation of the different decay modes see
        `this <https://ebldc.com/?p=86/>`__ blog post by Avayan.

        A good decay mode is unfortunately different for every motor. The best
        way to work out a good decay mode for your stepper motor, if you can't
        measure the current with an oscilloscope, is to listen to the sound of
        the motor. If the value is too low, you often hear a high pitched
        sound and if it is too high you can often hear a humming sound.

        Generally, fast decay mode (small value) will be noisier but also
        allow higher motor speeds.

        .. note::
         There is unfortunately no formula to calculate a perfect decay
         mode for a given stepper motor. If you have problems with loud noises
         or the maximum motor speed is too slow, you should try to tinker with
         the decay value
        """
        decay = int(decay)
        check_range("decay", decay, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DECAY,
            data=pack_payload((decay,), "H"),
            response_expected=response_expected,
        )

    async def get_decay(self) -> int:
        """
        Returns the decay mode as set by :func:`set_decay`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DECAY, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_minimum_voltage(self, voltage: float | Decimal = 8, response_expected: bool = True) -> None:
        """
        Sets the minimum voltage, below which the :attr:`CallbackID.UNDER_VOLTAGE` callback
        is triggered. The minimum possible value that works with the Stepper Brick is 8V.
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
        Returns the minimum voltage as set by :func:`set_minimum_voltage`.

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MINIMUM_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def set_sync_rect(self, sync_rect: bool = False, response_expected: bool = True) -> None:
        """
        Turns synchronous rectification on or off (*true* or *false*).

        With synchronous rectification on, the decay can be changed
        (see :func:`set_decay`). Without synchronous rectification fast
        decay is used.

        For an explanation of synchronous rectification see
        `here <https://en.wikipedia.org/wiki/Active_rectification>`__.

        .. warning::
         If you want to use high speeds (> 10000 steps/s) for a large
         stepper motor with a large inductivity we strongly
         suggest that you disable synchronous rectification. Otherwise the
         Brick may not be able to cope with the load and overheat.

        .. versionadded:: 1.1.4 (Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SYNC_RECT,
            data=pack_payload((bool(sync_rect),), "!"),
            response_expected=response_expected,
        )

    async def is_sync_rect(self) -> bool:
        """
        Returns *true* if synchronous rectification is enabled, *false* otherwise.

        .. versionadded:: 1.1.4 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_SYNC_RECT, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_time_base(self, time_base: float | Decimal = 1, response_expected: bool = True) -> None:
        """
        Sets the time base of the velocity and the acceleration of the stepper brick.

        For example, if you want to make one step every 1.5 seconds, you can set
        the time base to 15 and the velocity to 10. Now the velocity is
        10steps/15s = 1steps/1.5s.

        Units: time_base in s.

        .. versionadded:: 1.1.6 (Firmware)
        """
        time_base_raw = SECOND.from_si(time_base)
        check_range("time_base", time_base_raw, 0, 4294967295, time_base)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TIME_BASE,
            data=pack_payload((time_base_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_time_base(self) -> Decimal:
        """
        Returns the time base as set by :func:`set_time_base`.

        Units: time_base in s.

        .. versionadded:: 1.1.6 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TIME_BASE, response_expected=True
        )
        return SECOND.to_si(unpack_payload(payload, "I"))

    async def get_all_data(self) -> GetAllData:
        """
        Returns the following parameters: The current velocity,
        the current position, the remaining steps, the stack voltage, the external
        voltage and the current consumption of the stepper motor.

        There is also a callback for this function, see :attr:`CallbackID.ALL_DATA` callback.

        Units: stack_voltage in V, external_voltage in V, current_consumption in A.

        .. versionadded:: 1.1.6 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_DATA, response_expected=True
        )
        current_velocity, current_position, remaining_steps, stack_voltage, external_voltage, current_consumption = (
            unpack_payload(payload, "H i i H H H")
        )
        return GetAllData(
            current_velocity,
            current_position,
            remaining_steps,
            MILLI_VOLT.to_si(stack_voltage),
            MILLI_VOLT.to_si(external_voltage),
            MILLI_AMPERE.to_si(current_consumption),
        )

    async def set_all_data_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ALL_DATA` callback is triggered
        periodically. A value of 0 turns the callback off.

        .. versionadded:: 1.1.6 (Firmware)
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALL_DATA_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_all_data_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_all_data_period`.

        .. versionadded:: 1.1.6 (Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALL_DATA_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

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

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.UNDER_VOLTAGE:
            return 0, MILLI_VOLT.to_si(value)
        if callback_id is CallbackID.POSITION_REACHED:
            return 1, value
        if callback_id is CallbackID.ALL_DATA:
            (
                current_velocity,
                current_position,
                remaining_steps,
                stack_voltage,
                external_voltage,
                current_consumption,
            ) = value
            return 2, GetAllData(
                current_velocity,
                current_position,
                remaining_steps,
                MILLI_VOLT.to_si(stack_voltage),
                MILLI_VOLT.to_si(external_voltage),
                MILLI_AMPERE.to_si(current_consumption),
            )
        state_new, state_previous = value
        return 3, NewStateEvent(State(state_new), State(state_previous))
