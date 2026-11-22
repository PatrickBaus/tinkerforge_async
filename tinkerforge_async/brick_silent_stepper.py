"""
Module for the Tinkerforge Silent Stepper Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/SilentStepper_Brick_Python.html) implemented using
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

    UNDER_VOLTAGE = 40
    POSITION_REACHED = 41
    ALL_DATA = 47
    NEW_STATE = 48


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
    SET_STEP_CONFIGURATION = 14
    GET_STEP_CONFIGURATION = 15
    DRIVE_FORWARD = 16
    DRIVE_BACKWARD = 17
    STOP = 18
    GET_STACK_INPUT_VOLTAGE = 19
    GET_EXTERNAL_INPUT_VOLTAGE = 20
    SET_MOTOR_CURRENT = 22
    GET_MOTOR_CURRENT = 23
    ENABLE = 24
    DISABLE = 25
    IS_ENABLED = 26
    SET_BASIC_CONFIGURATION = 27
    GET_BASIC_CONFIGURATION = 28
    SET_SPREADCYCLE_CONFIGURATION = 29
    GET_SPREADCYCLE_CONFIGURATION = 30
    SET_STEALTH_CONFIGURATION = 31
    GET_STEALTH_CONFIGURATION = 32
    SET_COOLSTEP_CONFIGURATION = 33
    GET_COOLSTEP_CONFIGURATION = 34
    SET_MISC_CONFIGURATION = 35
    GET_MISC_CONFIGURATION = 36
    GET_DRIVER_STATUS = 37
    SET_MINIMUM_VOLTAGE = 38
    GET_MINIMUM_VOLTAGE = 39
    SET_TIME_BASE = 42
    GET_TIME_BASE = 43
    GET_ALL_DATA = 44
    SET_ALL_DATA_PERIOD = 45
    GET_ALL_DATA_PERIOD = 46
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
class StepResolution(Enum):
    """
    The step resolution options
    """

    STEP_RESOLUTION_1 = 8
    STEP_RESOLUTION_2 = 7
    STEP_RESOLUTION_4 = 6
    STEP_RESOLUTION_8 = 5
    STEP_RESOLUTION_16 = 4
    STEP_RESOLUTION_32 = 3
    STEP_RESOLUTION_64 = 2
    STEP_RESOLUTION_128 = 1
    STEP_RESOLUTION_256 = 0


@unique
class ChopperMode(Enum):
    """
    The chopper mode options
    """

    SPREAD_CYCLE = 0
    FAST_DECAY = 1


@unique
class FreewheelMode(Enum):
    """
    The freewheel mode options
    """

    NORMAL = 0
    FREEWHEELING = 1
    COIL_SHORT_LS = 2
    COIL_SHORT_HS = 3


@unique
class CurrentUpStepIncrement(Enum):
    """
    The current up step increment options
    """

    CURRENT_UP_STEP_INCREMENT_1 = 0
    CURRENT_UP_STEP_INCREMENT_2 = 1
    CURRENT_UP_STEP_INCREMENT_4 = 2
    CURRENT_UP_STEP_INCREMENT_8 = 3


@unique
class CurrentDownStepDecrement(Enum):
    """
    The current down step decrement options
    """

    CURRENT_DOWN_STEP_DECREMENT_1 = 0
    CURRENT_DOWN_STEP_DECREMENT_2 = 1
    CURRENT_DOWN_STEP_DECREMENT_8 = 2
    CURRENT_DOWN_STEP_DECREMENT_32 = 3


@unique
class MinimumCurrent(Enum):
    """
    The minimum current options
    """

    HALF = 0
    QUARTER = 1


@unique
class StallguardMode(Enum):
    """
    The stallguard mode options
    """

    STANDARD = 0
    FILTERED = 1


@unique
class OpenLoad(Enum):
    """
    The open load options
    """

    NONE = 0
    PHASE_A = 1
    PHASE_B = 2
    PHASE_AB = 3


@unique
class ShortToGround(Enum):
    """
    The short to ground options
    """

    NONE = 0
    PHASE_A = 1
    PHASE_B = 2
    PHASE_AB = 3


@unique
class OverTemperature(Enum):
    """
    The over temperature options
    """

    NONE = 0
    WARNING = 1
    LIMIT = 2


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


class GetStepConfiguration(NamedTuple):
    step_resolution: StepResolution
    interpolation: bool


class GetBasicConfiguration(NamedTuple):
    standstill_current: Decimal
    motor_run_current: Decimal
    standstill_delay_time: Decimal
    power_down_time: Decimal
    stealth_threshold: int
    coolstep_threshold: int
    classic_threshold: int
    high_velocity_chopper_mode: bool


class GetSpreadcycleConfiguration(NamedTuple):
    slow_decay_duration: int
    enable_random_slow_decay: bool
    fast_decay_duration: int
    hysteresis_start_value: int
    hysteresis_end_value: int
    sine_wave_offset: int
    chopper_mode: ChopperMode
    comparator_blank_time: int
    fast_decay_without_comparator: bool


class GetStealthConfiguration(NamedTuple):
    enable_stealth: bool
    amplitude: int
    gradient: int
    enable_autoscale: bool
    force_symmetric: bool
    freewheel_mode: FreewheelMode


class GetCoolstepConfiguration(NamedTuple):
    minimum_stallguard_value: int
    maximum_stallguard_value: int
    current_up_step_width: CurrentUpStepIncrement
    current_down_step_width: CurrentDownStepDecrement
    minimum_current: MinimumCurrent
    stallguard_threshold_value: int
    stallguard_mode: StallguardMode


class GetMiscConfiguration(NamedTuple):
    disable_short_to_ground_protection: bool
    synchronize_phase_frequency: int


class GetDriverStatus(NamedTuple):
    open_load: OpenLoad
    short_to_ground: ShortToGround
    over_temperature: OverTemperature
    motor_stalled: bool
    actual_motor_current: int
    full_step_active: bool
    stallguard_result: int
    stealth_voltage_amplitude: int


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


class BrickSilentStepper(DeviceWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Silently drives one bipolar stepper motor with up to 46V and 1.6A per phase
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_SILENT_STEPPER
    DEVICE_DISPLAY_NAME = "Silent Stepper Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    BrickletPort = Port
    StepResolution: TypeAlias = StepResolution
    ChopperMode: TypeAlias = ChopperMode
    FreewheelMode: TypeAlias = FreewheelMode
    CurrentUpStepIncrement: TypeAlias = CurrentUpStepIncrement
    CurrentDownStepDecrement: TypeAlias = CurrentDownStepDecrement
    MinimumCurrent: TypeAlias = MinimumCurrent
    StallguardMode: TypeAlias = StallguardMode
    OpenLoad: TypeAlias = OpenLoad
    ShortToGround: TypeAlias = ShortToGround
    OverTemperature: TypeAlias = OverTemperature
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

        self.api_version = (2, 0, 1)

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

    async def set_step_configuration(
        self,
        step_resolution: StepResolution | int = StepResolution.STEP_RESOLUTION_256,
        interpolation: bool = True,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the step resolution from full-step up to 1/256-step.

        If interpolation is turned on, the Silent Stepper Brick will always interpolate
        your step inputs as 1/256-step. If you use full-step mode with interpolation, each
        step will generate 256 1/256 steps.

        For maximum torque use full-step without interpolation. For maximum resolution use
        1/256-step. Turn interpolation on to make the Stepper driving less noisy.

        If you often change the speed with high acceleration you should turn the
        interpolation off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STEP_CONFIGURATION,
            data=pack_payload((StepResolution(step_resolution).value, bool(interpolation)), "B !"),
            response_expected=response_expected,
        )

    async def get_step_configuration(self) -> GetStepConfiguration:
        """
        Returns the step mode as set by :func:`set_step_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STEP_CONFIGURATION, response_expected=True
        )
        step_resolution, interpolation = unpack_payload(payload, "B !")
        return GetStepConfiguration(StepResolution(step_resolution), interpolation)

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
        given via the black power input connector on the Silent Stepper Brick.

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

    async def set_motor_current(
        self, current: float | Decimal = Decimal("0.8"), response_expected: bool = True
    ) -> None:
        """
        Sets the current with which the motor will be driven.

        .. warning::
         Do not set this value above the specifications of your stepper motor.
         Otherwise it may damage your motor.

        Units: current in A (0.36 to 1.64 A).
        """
        current_raw = MILLI_AMPERE.from_si(current)
        check_range("current", current_raw, 360, 1640, current)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOTOR_CURRENT,
            data=pack_payload((current_raw,), "H"),
            response_expected=response_expected,
        )

    async def get_motor_current(self) -> Decimal:
        """
        Returns the current as set by :func:`set_motor_current`.

        Units: current in A (0.36 to 1.64 A).
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

    async def set_basic_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        standstill_current: float | Decimal = Decimal("0.2"),
        motor_run_current: float | Decimal = Decimal("0.8"),
        standstill_delay_time: Duration = 0,
        power_down_time: Duration = 1,
        stealth_threshold: int = 500,
        coolstep_threshold: int = 500,
        classic_threshold: int = 1000,
        high_velocity_chopper_mode: bool = False,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the basic configuration parameters for the different modes (Stealth, Coolstep, Classic).

        * Standstill Current: This value can be used to lower the current during stand still. This might
          be reasonable to reduce the heating of the motor and the Brick. When the motor is in standstill
          the configured motor phase current will be driven until the configured
          Power Down Time is elapsed. After that the phase current will be reduced to the standstill
          current. The elapsed time for this reduction can be configured with the Standstill Delay Time.
          The maximum allowed value is the configured maximum motor current
          (see :func:`set_motor_current`).

        * Motor Run Current: The value sets the motor current when the motor is running.
          Use a value of at least one half of the global maximum motor current for a good
          microstep performance. The maximum allowed value is the current
          motor current. The API maps the entered value to 1/32 ... 32/32 of the maximum
          motor current. This value should be used to change the motor current during motor movement,
          whereas the global maximum motor current should not be changed while the motor is moving
          (see :func:`set_motor_current`).

        * Standstill Delay Time: Controls the duration for motor power down after a motion
          as soon as standstill is detected and the Power Down Time is expired. A high Standstill Delay
          Time results in a smooth transition that avoids motor jerk during power down.

        * Power Down Time: Sets the delay time after a stand still.

        * Stealth Threshold: Sets the upper threshold for Stealth mode.
          If the velocity of the motor goes above this value, Stealth mode is turned
          off. Otherwise it is turned on. In Stealth mode the torque declines with high speed.

        * Coolstep Threshold: Sets the lower threshold for Coolstep mode.
          The Coolstep Threshold needs to be above the Stealth Threshold.

        * Classic Threshold: Sets the lower threshold for classic mode.
          In classic mode the stepper becomes more noisy, but the torque is maximized.

        * High Velocity Chopper Mode: If High Velocity Chopper Mode is enabled, the stepper control
          is optimized to run the stepper motors at high velocities.

        If you want to use all three thresholds make sure that
        Stealth Threshold < Coolstep Threshold < Classic Threshold.

        Units: standstill_current in A, motor_run_current in A, standstill_delay_time in s (0 to 0.307 s),
        power_down_time in s (0 to 5.222 s).
        """
        standstill_current_raw = MILLI_AMPERE.from_si(standstill_current)
        check_range("standstill_current", standstill_current_raw, 0, 65535, standstill_current)
        motor_run_current_raw = MILLI_AMPERE.from_si(motor_run_current)
        check_range("motor_run_current", motor_run_current_raw, 0, 65535, motor_run_current)
        standstill_delay_time_raw = seconds_to_ms(standstill_delay_time)
        check_range("standstill_delay_time", standstill_delay_time_raw, 0, 307, standstill_delay_time)
        power_down_time_raw = seconds_to_ms(power_down_time)
        check_range("power_down_time", power_down_time_raw, 0, 5222, power_down_time)
        stealth_threshold = int(stealth_threshold)
        check_range("stealth_threshold", stealth_threshold, 0, 65535)
        coolstep_threshold = int(coolstep_threshold)
        check_range("coolstep_threshold", coolstep_threshold, 0, 65535)
        classic_threshold = int(classic_threshold)
        check_range("classic_threshold", classic_threshold, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BASIC_CONFIGURATION,
            data=pack_payload(
                (
                    standstill_current_raw,
                    motor_run_current_raw,
                    standstill_delay_time_raw,
                    power_down_time_raw,
                    stealth_threshold,
                    coolstep_threshold,
                    classic_threshold,
                    bool(high_velocity_chopper_mode),
                ),
                "H H H H H H H !",
            ),
            response_expected=response_expected,
        )

    async def get_basic_configuration(self) -> GetBasicConfiguration:
        """
        Returns the configuration as set by :func:`set_basic_configuration`.

        Units: standstill_current in A, motor_run_current in A, standstill_delay_time in s (0 to 0.307 s),
        power_down_time in s (0 to 5.222 s).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BASIC_CONFIGURATION, response_expected=True
        )
        (
            standstill_current,
            motor_run_current,
            standstill_delay_time,
            power_down_time,
            stealth_threshold,
            coolstep_threshold,
            classic_threshold,
            high_velocity_chopper_mode,
        ) = unpack_payload(payload, "H H H H H H H !")
        return GetBasicConfiguration(
            MILLI_AMPERE.to_si(standstill_current),
            MILLI_AMPERE.to_si(motor_run_current),
            ms_to_seconds(standstill_delay_time),
            ms_to_seconds(power_down_time),
            stealth_threshold,
            coolstep_threshold,
            classic_threshold,
            high_velocity_chopper_mode,
        )

    async def set_spreadcycle_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        slow_decay_duration: int = 4,
        enable_random_slow_decay: bool = False,
        fast_decay_duration: int = 0,
        hysteresis_start_value: int = 0,
        hysteresis_end_value: int = 0,
        sine_wave_offset: int = 0,
        chopper_mode: ChopperMode | int = ChopperMode.SPREAD_CYCLE,
        comparator_blank_time: int = 1,
        fast_decay_without_comparator: bool = False,
        response_expected: bool = True,
    ) -> None:
        """
        Note: If you don't know what any of this means you can very likely keep all of
        the values as default!

        Sets the Spreadcycle configuration parameters. Spreadcycle is a chopper algorithm which actively
        controls the motor current flow. More information can be found in the TMC2130 datasheet on page
        47 (7 spreadCycle and Classic Chopper).

        * Slow Decay Duration: Controls duration of off time setting of slow decay phase.
          0 = driver disabled, all bridges off. Use 1 only with Comparator Blank time >= 2.

        * Enable Random Slow Decay: Set to false to fix chopper off time as set by Slow Decay Duration.
          If you set it to true, Decay Duration is randomly modulated.

        * Fast Decay Duration: Sets the fast decay duration. This parameters is
          only used if the Chopper Mode is set to Fast Decay.

        * Hysteresis Start Value: Sets the hysteresis start value. This parameter is
          only used if the Chopper Mode is set to Spread Cycle.

        * Hysteresis End Value: Sets the hysteresis end value. This parameter is
          only used if the Chopper Mode is set to Spread Cycle.

        * Sine Wave Offset: Sets the sine wave offset. This parameters is
          only used if the Chopper Mode is set to Fast Decay. 1/512 of the value becomes added to the absolute
          value of the sine wave.

        * Chopper Mode: 0 = Spread Cycle, 1 = Fast Decay.

        * Comparator Blank Time: Sets the blank time of the comparator. Available values are

          * 0 = 16 clocks,
          * 1 = 24 clocks,
          * 2 = 36 clocks and
          * 3 = 54 clocks.

          A value of 1 or 2 is recommended for most applications.

        * Fast Decay Without Comparator: If set to true the current comparator usage for termination of the
          fast decay cycle is disabled.
        """
        slow_decay_duration = int(slow_decay_duration)
        check_range("slow_decay_duration", slow_decay_duration, 0, 15)
        fast_decay_duration = int(fast_decay_duration)
        check_range("fast_decay_duration", fast_decay_duration, 0, 15)
        hysteresis_start_value = int(hysteresis_start_value)
        check_range("hysteresis_start_value", hysteresis_start_value, 0, 7)
        hysteresis_end_value = int(hysteresis_end_value)
        check_range("hysteresis_end_value", hysteresis_end_value, -3, 12)
        sine_wave_offset = int(sine_wave_offset)
        check_range("sine_wave_offset", sine_wave_offset, -3, 12)
        comparator_blank_time = int(comparator_blank_time)
        check_range("comparator_blank_time", comparator_blank_time, 0, 3)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPREADCYCLE_CONFIGURATION,
            data=pack_payload(
                (
                    slow_decay_duration,
                    bool(enable_random_slow_decay),
                    fast_decay_duration,
                    hysteresis_start_value,
                    hysteresis_end_value,
                    sine_wave_offset,
                    ChopperMode(chopper_mode).value,
                    comparator_blank_time,
                    bool(fast_decay_without_comparator),
                ),
                "B ! B B b b B B !",
            ),
            response_expected=response_expected,
        )

    async def get_spreadcycle_configuration(self) -> GetSpreadcycleConfiguration:
        """
        Returns the configuration as set by :func:`set_basic_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPREADCYCLE_CONFIGURATION, response_expected=True
        )
        (
            slow_decay_duration,
            enable_random_slow_decay,
            fast_decay_duration,
            hysteresis_start_value,
            hysteresis_end_value,
            sine_wave_offset,
            chopper_mode,
            comparator_blank_time,
            fast_decay_without_comparator,
        ) = unpack_payload(payload, "B ! B B b b B B !")
        return GetSpreadcycleConfiguration(
            slow_decay_duration,
            enable_random_slow_decay,
            fast_decay_duration,
            hysteresis_start_value,
            hysteresis_end_value,
            sine_wave_offset,
            ChopperMode(chopper_mode),
            comparator_blank_time,
            fast_decay_without_comparator,
        )

    async def set_stealth_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        enable_stealth: bool = True,
        amplitude: int = 128,
        gradient: int = 4,
        enable_autoscale: bool = True,
        force_symmetric: bool = False,
        freewheel_mode: FreewheelMode | int = FreewheelMode.NORMAL,
        response_expected: bool = True,
    ) -> None:
        """
        Note: If you don't know what any of this means you can very likely keep all of
        the values as default!

        Sets the configuration relevant for Stealth mode.

        * Enable Stealth: If set to true the stealth mode is enabled, if set to false the
          stealth mode is disabled, even if the speed is below the threshold set in :func:`set_basic_configuration`.

        * Amplitude: If autoscale is disabled, the PWM amplitude is scaled by this value. If autoscale is enabled,
          this value defines the maximum PWM amplitude change per half wave.

        * Gradient: If autoscale is disabled, the PWM gradient is scaled by this value. If autoscale is enabled,
          this value defines the maximum PWM gradient. With autoscale a value above 64 is recommended,
          otherwise the regulation might not be able to measure the current.

        * Enable Autoscale: If set to true, automatic current control is used. Otherwise the user defined
          amplitude and gradient are used.

        * Force Symmetric: If true, A symmetric PWM cycle is enforced. Otherwise the PWM value may change within each
          PWM cycle.

        * Freewheel Mode: The freewheel mode defines the behavior in stand still if the Standstill Current
          (see :func:`set_basic_configuration`) is set to 0.
        """
        amplitude = int(amplitude)
        check_range("amplitude", amplitude, 0, 255)
        gradient = int(gradient)
        check_range("gradient", gradient, 0, 255)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STEALTH_CONFIGURATION,
            data=pack_payload(
                (
                    bool(enable_stealth),
                    amplitude,
                    gradient,
                    bool(enable_autoscale),
                    bool(force_symmetric),
                    FreewheelMode(freewheel_mode).value,
                ),
                "! B B ! ! B",
            ),
            response_expected=response_expected,
        )

    async def get_stealth_configuration(self) -> GetStealthConfiguration:
        """
        Returns the configuration as set by :func:`set_stealth_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STEALTH_CONFIGURATION, response_expected=True
        )
        enable_stealth, amplitude, gradient, enable_autoscale, force_symmetric, freewheel_mode = unpack_payload(
            payload, "! B B ! ! B"
        )
        return GetStealthConfiguration(
            enable_stealth, amplitude, gradient, enable_autoscale, force_symmetric, FreewheelMode(freewheel_mode)
        )

    async def set_coolstep_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        minimum_stallguard_value: int = 2,
        maximum_stallguard_value: int = 10,
        current_up_step_width: CurrentUpStepIncrement | int = CurrentUpStepIncrement.CURRENT_UP_STEP_INCREMENT_1,
        current_down_step_width: (
            CurrentDownStepDecrement | int
        ) = CurrentDownStepDecrement.CURRENT_DOWN_STEP_DECREMENT_1,
        minimum_current: MinimumCurrent | int = MinimumCurrent.HALF,
        stallguard_threshold_value: int = 0,
        stallguard_mode: StallguardMode | int = StallguardMode.STANDARD,
        response_expected: bool = True,
    ) -> None:
        """
        Note: If you don't know what any of this means you can very likely keep all of
        the values as default!

        Sets the configuration relevant for Coolstep.

        * Minimum Stallguard Value: If the Stallguard result falls below this value*32, the motor current
          is increased to reduce motor load angle. A value of 0 turns Coolstep off.

        * Maximum Stallguard Value: If the Stallguard result goes above
          (Min Stallguard Value + Max Stallguard Value + 1) * 32, the motor current is decreased to save
          energy.

        * Current Up Step Width: Sets the up step increment per Stallguard value. The value range is 0-3,
          corresponding to the increments 1, 2, 4 and 8.

        * Current Down Step Width: Sets the down step decrement per Stallguard value. The value range is 0-3,
          corresponding to the decrements 1, 2, 8 and 16.

        * Minimum Current: Sets the minimum current for Coolstep current control. You can choose between
          half and quarter of the run current.

        * Stallguard Threshold Value: Sets the level for stall output (see :func:`get_driver_status`).
          A lower value gives a higher sensitivity. You have to find a suitable value for your
          motor by trial and error, 0 works for most motors.

        * Stallguard Mode: Set to 0 for standard resolution or 1 for filtered mode. In filtered mode the Stallguard
          signal will be updated every four full-steps.
        """
        minimum_stallguard_value = int(minimum_stallguard_value)
        check_range("minimum_stallguard_value", minimum_stallguard_value, 0, 15)
        maximum_stallguard_value = int(maximum_stallguard_value)
        check_range("maximum_stallguard_value", maximum_stallguard_value, 0, 15)
        stallguard_threshold_value = int(stallguard_threshold_value)
        check_range("stallguard_threshold_value", stallguard_threshold_value, -64, 63)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COOLSTEP_CONFIGURATION,
            data=pack_payload(
                (
                    minimum_stallguard_value,
                    maximum_stallguard_value,
                    CurrentUpStepIncrement(current_up_step_width).value,
                    CurrentDownStepDecrement(current_down_step_width).value,
                    MinimumCurrent(minimum_current).value,
                    stallguard_threshold_value,
                    StallguardMode(stallguard_mode).value,
                ),
                "B B B B B b B",
            ),
            response_expected=response_expected,
        )

    async def get_coolstep_configuration(self) -> GetCoolstepConfiguration:
        """
        Returns the configuration as set by :func:`set_coolstep_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COOLSTEP_CONFIGURATION, response_expected=True
        )
        (
            minimum_stallguard_value,
            maximum_stallguard_value,
            current_up_step_width,
            current_down_step_width,
            minimum_current,
            stallguard_threshold_value,
            stallguard_mode,
        ) = unpack_payload(payload, "B B B B B b B")
        return GetCoolstepConfiguration(
            minimum_stallguard_value,
            maximum_stallguard_value,
            CurrentUpStepIncrement(current_up_step_width),
            CurrentDownStepDecrement(current_down_step_width),
            MinimumCurrent(minimum_current),
            stallguard_threshold_value,
            StallguardMode(stallguard_mode),
        )

    async def set_misc_configuration(
        self,
        disable_short_to_ground_protection: bool = False,
        synchronize_phase_frequency: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Note: If you don't know what any of this means you can very likely keep all of
        the values as default!

        Sets miscellaneous configuration parameters.

        * Disable Short To Ground Protection: Set to false to enable short to ground protection, otherwise
          it is disabled.

        * Synchronize Phase Frequency: With this parameter you can synchronize the chopper for both phases
          of a two phase motor to avoid the occurrence of a beat. The value range is 0-15. If set to 0,
          the synchronization is turned off. Otherwise the synchronization is done through the formula
          f_sync = f_clk/(value*64). In Classic Mode the synchronization is automatically switched off.
          f_clk is 12.8MHz.
        """
        synchronize_phase_frequency = int(synchronize_phase_frequency)
        check_range("synchronize_phase_frequency", synchronize_phase_frequency, 0, 15)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MISC_CONFIGURATION,
            data=pack_payload((bool(disable_short_to_ground_protection), synchronize_phase_frequency), "! B"),
            response_expected=response_expected,
        )

    async def get_misc_configuration(self) -> GetMiscConfiguration:
        """
        Returns the configuration as set by :func:`set_misc_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MISC_CONFIGURATION, response_expected=True
        )
        disable_short_to_ground_protection, synchronize_phase_frequency = unpack_payload(payload, "! B")
        return GetMiscConfiguration(disable_short_to_ground_protection, synchronize_phase_frequency)

    async def get_driver_status(self) -> GetDriverStatus:
        """
        Returns the current driver status.

        * Open Load: Indicates if an open load is present on phase A, B or both. This could mean that there is a problem
          with the wiring of the motor. False detection can occur in fast motion as well as during stand still.

        * Short To Ground: Indicates if a short to ground is present on phase A, B or both. If this is detected the
          driver
          automatically becomes disabled and stays disabled until it is enabled again manually.

        * Over Temperature: The over temperature indicator switches to "Warning" if the driver IC warms up. The warning
          flag
          is expected during long duration stepper uses. If the temperature limit is reached the indicator switches
          to "Limit". In this case the driver becomes disabled until it cools down again.

        * Motor Stalled: Is true if a motor stall was detected.

        * Actual Motor Current: Indicates the actual current control scaling as used in Coolstep mode.
          It represents a multiplier of 1/32 to 32/32 of the
          ``Motor Run Current`` as set by :func:`set_basic_configuration`. Example: If a ``Motor Run Current``
          of 1000mA was set and the returned value is 15, the ``Actual Motor Current`` is 16/32*1000mA = 500mA.

        * Stallguard Result: Indicates the load of the motor. A lower value signals a higher load. Per trial and error
          you can find out which value corresponds to a suitable torque for the velocity used in your application.
          After that you can use this threshold value to find out if a motor stall becomes probable and react on it
          (e.g.
          decrease velocity).
          During stand still this value can not be used for stall detection, it shows the chopper on-time for motor coil
          A.

        * Stealth Voltage Amplitude: Shows the actual PWM scaling. In Stealth mode it can be used to detect motor load
          and
          stall if autoscale is enabled (see :func:`set_stealth_configuration`).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DRIVER_STATUS, response_expected=True
        )
        (
            open_load,
            short_to_ground,
            over_temperature,
            motor_stalled,
            actual_motor_current,
            full_step_active,
            stallguard_result,
            stealth_voltage_amplitude,
        ) = unpack_payload(payload, "B B B ! B ! B B")
        return GetDriverStatus(
            OpenLoad(open_load),
            ShortToGround(short_to_ground),
            OverTemperature(over_temperature),
            motor_stalled,
            actual_motor_current,
            full_step_active,
            stallguard_result,
            stealth_voltage_amplitude,
        )

    async def set_minimum_voltage(self, voltage: float | Decimal = 8, response_expected: bool = True) -> None:
        """
        Sets the minimum voltage, below which the :attr:`CallbackID.UNDER_VOLTAGE` callback
        is triggered. The minimum possible value that works with the Silent Stepper
        Brick is 8V.
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

    async def set_time_base(self, time_base: float | Decimal = 1, response_expected: bool = True) -> None:
        """
        Sets the time base of the velocity and the acceleration of the Silent Stepper
        Brick.

        For example, if you want to make one step every 1.5 seconds, you can set
        the time base to 15 and the velocity to 10. Now the velocity is
        10steps/15s = 1steps/1.5s.

        Units: time_base in s.
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

        The current consumption is calculated by multiplying the ``Actual Motor Current``
        value (see :func:`set_basic_configuration`) with the ``Motor Run Current``
        (see :func:`get_driver_status`). This is an internal calculation of the
        driver, not an independent external measurement.

        The current consumption calculation was broken up to firmware 2.0.1, it is fixed
        since firmware 2.0.2.

        There is also a callback for this function, see :attr:`CallbackID.ALL_DATA` callback.

        Units: stack_voltage in V, external_voltage in V, current_consumption in A.
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
