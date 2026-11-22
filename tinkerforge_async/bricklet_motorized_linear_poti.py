"""
Module for the Tinkerforge Motorized Linear Poti Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/MotorizedLinearPoti_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, Channel, ChannelConfiguration, DeviceIdentifier
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    POSITION = 4
    POSITION_REACHED = 10


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_POSITION = 1
    SET_POSITION_CALLBACK_CONFIGURATION = 2
    GET_POSITION_CALLBACK_CONFIGURATION = 3
    SET_MOTOR_POSITION = 5
    GET_MOTOR_POSITION = 6
    CALIBRATE = 7
    SET_POSITION_REACHED_CALLBACK_CONFIGURATION = 8
    GET_POSITION_REACHED_CALLBACK_CONFIGURATION = 9


@unique
class DriveMode(Enum):
    """
    The drive mode options
    """

    FAST = 0
    SMOOTH = 1


class GetMotorPosition(NamedTuple):
    position: int
    drive_mode: DriveMode
    hold_position: bool
    position_reached: bool


class BrickletMotorizedLinearPoti(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Motorized Linear Potentiometer
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_MOTORIZED_LINEAR_POTI
    DEVICE_DISPLAY_NAME = "Motorized Linear Poti Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    DriveMode: TypeAlias = DriveMode

    CALLBACK_FORMATS = {
        CallbackID.POSITION: "H",
        CallbackID.POSITION_REACHED: "H",
    }

    CHANNELS = (
        Channel(
            0, getter="get_position", callbacks=(CallbackID.POSITION,), configuration=ChannelConfiguration("position")
        ),
        Channel(1, callbacks=(CallbackID.POSITION_REACHED,)),
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
        option: Threshold | int = Threshold.OFF,
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

    async def get_position(self) -> int:
        """
        Returns the position of the linear potentiometer. The value is
        between 0 (slider down) and 100 (slider up).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POSITION, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_position_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: int = 0,
        maximum: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.POSITION` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.POSITION` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum = int(minimum)
        check_range("minimum", minimum, 0, 65535)
        maximum = int(maximum)
        check_range("maximum", maximum, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum, maximum), "I ! c H H"
            ),
            response_expected=response_expected,
        )

    async def get_position_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_position_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POSITION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), Decimal(minimum), Decimal(maximum)
        )

    async def set_motor_position(
        self, position: int, drive_mode: DriveMode | int, hold_position: bool, response_expected: bool = True
    ) -> None:
        """
        Sets the position of the potentiometer. The motorized potentiometer will
        immediately start to approach the position. Depending on the chosen drive mode,
        the position will either be reached as fast as possible or in a slow but smooth
        motion.

        The position has to be between 0 (slider down) and 100 (slider up).

        If you set the hold position parameter to true, the position will automatically
        be retained. If a user changes the position of the potentiometer, it will
        automatically drive back to the original set point.

        If the hold position parameter is set to false, the potentiometer can be changed
        again by the user as soon as the set point was reached once.
        """
        position = int(position)
        check_range("position", position, 0, 100)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOTOR_POSITION,
            data=pack_payload((position, DriveMode(drive_mode).value, bool(hold_position)), "H B !"),
            response_expected=response_expected,
        )

    async def get_motor_position(self) -> GetMotorPosition:
        """
        Returns the last motor position as set by :func:`set_motor_position`. This is not
        the current position (use :func:`get_position` to get the current position). This
        is the last used set point and configuration.

        The position reached parameter is true if the position has been reached at one point.
        The position may have been changed again in the meantime by the user.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOTOR_POSITION, response_expected=True
        )
        position, drive_mode, hold_position, position_reached = unpack_payload(payload, "H B ! !")
        return GetMotorPosition(position, DriveMode(drive_mode), hold_position, position_reached)

    async def calibrate(self, response_expected: bool = True) -> None:
        """
        Starts a calibration procedure. The potentiometer will be driven to the extreme
        points to calibrate the potentiometer.

        The calibration is saved in flash, it does not have to be called on every start up.

        The Motorized Linear Poti Bricklet is already factory-calibrated during
        testing at Tinkerforge.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.CALIBRATE, response_expected=response_expected
        )

    async def set_position_reached_callback_configuration(
        self, enabled: bool = True, response_expected: bool = True
    ) -> None:
        """
        Enables/Disables :attr:`CallbackID.POSITION_REACHED` callback.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POSITION_REACHED_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), "!"),
            response_expected=response_expected,
        )

    async def get_position_reached_callback_configuration(self) -> bool:
        """
        Returns the :attr:`CallbackID.POSITION_REACHED` callback configuration
        as set by :func:`set_position_reached_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POSITION_REACHED_CALLBACK_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "!")

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.POSITION:
            return 0, value
        return 1, value
