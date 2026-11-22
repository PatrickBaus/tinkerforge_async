"""
Module for the Tinkerforge Joystick Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/JoystickV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

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

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    POSITION = 6
    PRESSED = 9


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_POSITION = 1
    IS_PRESSED = 2
    CALIBRATE = 3
    SET_POSITION_CALLBACK_CONFIGURATION = 4
    GET_POSITION_CALLBACK_CONFIGURATION = 5
    SET_PRESSED_CALLBACK_CONFIGURATION = 7
    GET_PRESSED_CALLBACK_CONFIGURATION = 8


class GetPosition(NamedTuple):
    x: int
    y: int


class BrickletJoystickV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    2-axis joystick with push-button
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_JOYSTICK_V2
    DEVICE_DISPLAY_NAME = "Joystick Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.POSITION: "h h",
        CallbackID.PRESSED: "!",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.POSITION,),
            configuration=ChannelConfiguration("position", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            1,
            callbacks=(CallbackID.PRESSED,),
            configuration=ChannelConfiguration("pressed", thresholds=False, wrap_advanced=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

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
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_position(self) -> GetPosition:
        """
        Returns the position of the joystick. The middle position of the joystick is x=0, y=0.
        The returned values are averaged and calibrated (see :func:`calibrate`).

        If you want to get the position periodically, it is recommended to use the
        :attr:`CallbackID.POSITION` callback and set the period with
        :func:`set_position_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POSITION, response_expected=True
        )
        x, y = unpack_payload(payload, "h h")
        return GetPosition(x, y)

    async def is_pressed(self) -> bool:
        """
        Returns *true* if the button is pressed and *false* otherwise.

        If you want to get the press-state periodically, it is recommended to use the
        :attr:`CallbackID.PRESSED` callback and set the period with
        :func:`set_pressed_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_PRESSED, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def calibrate(self, response_expected: bool = True) -> None:
        """
        Calibrates the middle position of the joystick. If your Joystick Bricklet 2.0
        does not return x=0 and y=0 in the middle position, call this function
        while the joystick is standing still in the middle position.

        The resulting calibration will be saved in non-volatile memory,
        thus you only have to calibrate it once.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.CALIBRATE, response_expected=response_expected
        )

    async def set_position_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.POSITION`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after at least one of the values has changed. If the values didn't
        change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POSITION_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_position_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_position_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POSITION_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_pressed_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.PRESSED`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after at least one of the values has changed. If the values didn't
        change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_PRESSED_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_pressed_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_pressed_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_PRESSED_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.POSITION:
            x, y = value
            return 0, GetPosition(x, y)
        return 1, value
