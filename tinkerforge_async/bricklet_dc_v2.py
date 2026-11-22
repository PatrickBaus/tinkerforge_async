"""
Module for the Tinkerforge DC Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DCV2_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    SimpleCallbackConfiguration,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    EMERGENCY_SHUTDOWN = 22
    VELOCITY_REACHED = 23
    CURRENT_VELOCITY = 24


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    SET_ENABLED = 1
    GET_ENABLED = 2
    SET_VELOCITY = 3
    GET_VELOCITY = 4
    GET_CURRENT_VELOCITY = 5
    SET_MOTION = 6
    GET_MOTION = 7
    FULL_BRAKE = 8
    SET_DRIVE_MODE = 9
    GET_DRIVE_MODE = 10
    SET_PWM_FREQUENCY = 11
    GET_PWM_FREQUENCY = 12
    GET_POWER_STATISTICS = 13
    SET_ERROR_LED_CONFIG = 14
    GET_ERROR_LED_CONFIG = 15
    SET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION = 16
    GET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION = 17
    SET_VELOCITY_REACHED_CALLBACK_CONFIGURATION = 18
    GET_VELOCITY_REACHED_CALLBACK_CONFIGURATION = 19
    SET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION = 20
    GET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION = 21


@unique
class DriveMode(Enum):
    """
    The drive mode options
    """

    DRIVE_BRAKE = 0
    DRIVE_COAST = 1


@unique
class ErrorLEDConfig(Enum):
    """
    The error led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_ERROR = 3


class GetMotion(NamedTuple):
    acceleration: Decimal
    deceleration: Decimal


class GetPowerStatistics(NamedTuple):
    voltage: Decimal
    current: Decimal


HERTZ = LinearQuantity(1)  # raw: 1/1 Hertz, returned in Hz
MILLI_AMPERE = LinearQuantity(1, 1000)  # raw: 1/1000 Ampere, returned in A
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V
PERCENT_100_32767 = LinearQuantity(100, 32767)  # raw: 100/32767 Percent, returned in %
PERCENT_PER_SECOND_100_32767 = LinearQuantity(100, 32767)  # raw: 100/32767 Percent Per Second, returned in %/s


class BrickletDCV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Drives one brushed DC motor with up to 28V and 5A (peak)
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DC_V2
    DEVICE_DISPLAY_NAME = "DC Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    DriveMode: TypeAlias = DriveMode
    ErrorLEDConfig: TypeAlias = ErrorLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.EMERGENCY_SHUTDOWN: "",
        CallbackID.VELOCITY_REACHED: "h",
        CallbackID.CURRENT_VELOCITY: "h",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.EMERGENCY_SHUTDOWN,)),
        Channel(1, callbacks=(CallbackID.VELOCITY_REACHED,)),
        Channel(
            2,
            getter="get_current_velocity",
            callbacks=(CallbackID.CURRENT_VELOCITY,),
            configuration=ChannelConfiguration("current_velocity", thresholds=False, wrap_advanced=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> Any:
        """
        Returns the value of the channel with the secondary id `sid`. See `CHANNELS` for the channels.
        """
        return await self._get_value(sid)

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the callbacks of the channel with the secondary id `sid`. The thresholds are ignored by
        channels without thresholds.
        """
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return await self._get_callback_configuration(sid)

    async def set_enabled(self, enabled: bool, response_expected: bool = True) -> None:
        """
        Enables/Disables the driver chip. The driver parameters can be configured
        (velocity, acceleration, etc) before it is enabled.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ENABLED,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_enabled(self) -> bool:
        """
        Returns *true* if the driver chip is enabled, *false* otherwise.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_velocity(self, velocity: float | Decimal = 0, response_expected: bool = True) -> None:
        """
        Sets the velocity of the motor. Whereas -32767 is full speed backward,
        0 is stop and 32767 is full speed forward. Depending on the
        acceleration (see :func:`set_motion`), the motor is not immediately
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

    async def set_motion(
        self,
        acceleration: float | Decimal = Decimal("30.51850947599719229712820826"),
        deceleration: float | Decimal = Decimal("30.51850947599719229712820826"),
        response_expected: bool = True,
    ) -> None:
        """
        Sets the acceleration and deceleration of the motor. It is given in *velocity/s*.
        An acceleration of 10000 means, that every second the velocity is increased
        by 10000 (or about 30% duty cycle).

        For example: If the current velocity is 0 and you want to accelerate to a
        velocity of 16000 (about 50% duty cycle) in 10 seconds, you should set
        an acceleration of 1600.

        If acceleration and deceleration is set to 0, there is no speed ramping, i.e. a
        new velocity is immediately given to the motor.

        Units: acceleration in %/s, deceleration in %/s.
        """
        acceleration_raw = PERCENT_PER_SECOND_100_32767.from_si(acceleration)
        check_range("acceleration", acceleration_raw, 0, 65535, acceleration)
        deceleration_raw = PERCENT_PER_SECOND_100_32767.from_si(deceleration)
        check_range("deceleration", deceleration_raw, 0, 65535, deceleration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOTION,
            data=pack_payload((acceleration_raw, deceleration_raw), "H H"),
            response_expected=response_expected,
        )

    async def get_motion(self) -> GetMotion:
        """
        Returns the acceleration/deceleration as set by :func:`set_motion`.

        Units: acceleration in %/s, deceleration in %/s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOTION, response_expected=True
        )
        acceleration, deceleration = unpack_payload(payload, "H H")
        return GetMotion(
            PERCENT_PER_SECOND_100_32767.to_si(acceleration), PERCENT_PER_SECOND_100_32767.to_si(deceleration)
        )

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

    async def get_power_statistics(self) -> GetPowerStatistics:
        """
        Returns input voltage and current usage of the driver.

        Units: voltage in V, current in A.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POWER_STATISTICS, response_expected=True
        )
        voltage, current = unpack_payload(payload, "H H")
        return GetPowerStatistics(MILLI_VOLT.to_si(voltage), MILLI_AMPERE.to_si(current))

    async def set_error_led_config(
        self, config: ErrorLEDConfig | int = ErrorLEDConfig.SHOW_ERROR, response_expected: bool = True
    ) -> None:
        """
        Configures the error LED to be either turned off, turned on, blink in
        heartbeat mode or show an error.

        If the LED is configured to show errors it has three different states:

        * Off: No error present.
        * 1s interval blinking: Input voltage too low (below 6V).
        * 250ms interval blinking: Overtemperature or overcurrent.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ERROR_LED_CONFIG,
            data=pack_payload((ErrorLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_error_led_config(self) -> ErrorLEDConfig:
        """
        Returns the LED configuration as set by :func:`set_error_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ERROR_LED_CONFIG, response_expected=True
        )
        return ErrorLEDConfig(unpack_payload(payload, "B"))

    async def set_emergency_shutdown_callback_configuration(
        self, enabled: bool = False, response_expected: bool = True
    ) -> None:
        """
        Enable/Disable :attr:`CallbackID.EMERGENCY_SHUTDOWN` callback.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_emergency_shutdown_callback_configuration(self) -> bool:
        """
        Returns the callback configuration as set by
        :func:`set_emergency_shutdown_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_EMERGENCY_SHUTDOWN_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_velocity_reached_callback_configuration(
        self, enabled: bool = False, response_expected: bool = True
    ) -> None:
        """
        Enable/Disable :attr:`CallbackID.VELOCITY_REACHED` callback.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VELOCITY_REACHED_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_velocity_reached_callback_configuration(self) -> bool:
        """
        Returns the callback configuration as set by
        :func:`set_velocity_reached_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VELOCITY_REACHED_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def set_current_velocity_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.CURRENT_VELOCITY`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_current_velocity_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_current_velocity_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_VELOCITY_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.EMERGENCY_SHUTDOWN:
            return 0, None
        if callback_id is CallbackID.VELOCITY_REACHED:
            return 1, PERCENT_100_32767.to_si(value)
        return 2, PERCENT_100_32767.to_si(value)
