"""
Module for the Tinkerforge Multi Touch Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/MultiTouchV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias

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
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    TOUCH_STATE = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_TOUCH_STATE = 1
    SET_TOUCH_STATE_CALLBACK_CONFIGURATION = 2
    GET_TOUCH_STATE_CALLBACK_CONFIGURATION = 3
    RECALIBRATE = 5
    SET_ELECTRODE_CONFIG = 6
    GET_ELECTRODE_CONFIG = 7
    SET_ELECTRODE_SENSITIVITY = 8
    GET_ELECTRODE_SENSITIVITY = 9
    SET_TOUCH_LED_CONFIG = 10
    GET_TOUCH_LED_CONFIG = 11


@unique
class TouchLEDConfig(Enum):
    """
    The touch led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_TOUCH = 3


class BrickletMultiTouchV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Capacitive touch sensor for 12 electrodes
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_MULTI_TOUCH_V2
    DEVICE_DISPLAY_NAME = "Multi Touch Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    TouchLEDConfig: TypeAlias = TouchLEDConfig

    CALLBACK_FORMATS = {
        CallbackID.TOUCH_STATE: "13!",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_touch_state",
            callbacks=(CallbackID.TOUCH_STATE,),
            configuration=ChannelConfiguration("touch_state", thresholds=False, wrap_advanced=True),
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

    async def get_touch_state(self) -> tuple[bool, ...]:
        """
        Returns the current touch state. The state is given as a array of
        bools.

        Element 0 to 11 represent the 12 electrodes and element 12 represents
        the proximity.

        If an electrode is touched, the corresponding element is *true*. If
        a hand or similar is in proximity to the electrodes, element 12 is
        *true*.

        The proximity is activated with a distance of 1-0.02 m. An electrode
        is already counted as touched if a finger is nearly touching the
        electrode. This means that you can put a piece of paper or foil
        or similar on top of a electrode to build a touch panel with
        a professional look.

        If you want to get the value periodically, it is recommended to use the
        :attr:`CallbackID.TOUCH_STATE` callback. You can set the callback configuration
        with :func:`set_touch_state_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_STATE, response_expected=True
        )
        return tuple(unpack_payload(payload, "13!"))

    async def set_touch_state_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.TOUCH_STATE` callback
        is triggered periodically. A value of 0 turns the callback off.

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
            function_id=FunctionID.SET_TOUCH_STATE_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_touch_state_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_touch_state_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_STATE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def recalibrate(self, response_expected: bool = True) -> None:
        """
        Recalibrates the electrodes. Call this function whenever you changed
        or moved you electrodes.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.RECALIBRATE, response_expected=response_expected
        )

    async def set_electrode_config(self, enabled_electrodes: Sequence[bool], response_expected: bool = True) -> None:
        """
        Enables/disables electrodes with a bool array (see :func:`get_touch_state`).

        *True* enables the electrode, *false* disables the electrode. A
        disabled electrode will always return *false* as its state. If you
        don't need all electrodes you can disable the electrodes that are
        not needed.

        It is recommended that you disable the proximity electrode (element 12) if
        the proximity feature is not needed. This will reduce the amount of
        traffic that is produced by the :attr:`CallbackID.TOUCH_STATE` callback.

        Disabling electrodes will also reduce power consumption.
        """
        check_length("enabled_electrodes", enabled_electrodes, 13)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ELECTRODE_CONFIG,
            data=pack_payload(([bool(item) for item in enabled_electrodes],), "13!"),
            response_expected=response_expected,
        )

    async def get_electrode_config(self) -> tuple[bool, ...]:
        """
        Returns the electrode configuration, as set by :func:`set_electrode_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ELECTRODE_CONFIG, response_expected=True
        )
        return tuple(unpack_payload(payload, "13!"))

    async def set_electrode_sensitivity(self, sensitivity: int = 181, response_expected: bool = True) -> None:
        """
        Sets the sensitivity of the electrodes. An electrode with a high sensitivity
        will register a touch earlier then an electrode with a low sensitivity.

        If you build a big electrode you might need to decrease the sensitivity, since
        the area that can be charged will get bigger. If you want to be able to
        activate an electrode from further away you need to increase the sensitivity.

        After a new sensitivity is set, you likely want to call :func:`recalibrate`
        to calibrate the electrodes with the newly defined sensitivity.
        """
        sensitivity = int(sensitivity)
        check_range("sensitivity", sensitivity, 5, 201)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ELECTRODE_SENSITIVITY,
            data=pack_payload((sensitivity,), "B"),
            response_expected=response_expected,
        )

    async def get_electrode_sensitivity(self) -> int:
        """
        Returns the current sensitivity, as set by :func:`set_electrode_sensitivity`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ELECTRODE_SENSITIVITY, response_expected=True
        )
        return unpack_payload(payload, "B")

    async def set_touch_led_config(
        self, config: TouchLEDConfig | int = TouchLEDConfig.SHOW_TOUCH, response_expected: bool = True
    ) -> None:
        """
        Configures the touch LED to be either turned off, turned on, blink in
        heartbeat mode or show the touch state (electrode touched = LED on).
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TOUCH_LED_CONFIG,
            data=pack_payload((TouchLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_touch_led_config(self) -> TouchLEDConfig:
        """
        Returns the LED configuration as set by :func:`set_touch_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TOUCH_LED_CONFIG, response_expected=True
        )
        return TouchLEDConfig(unpack_payload(payload, "B"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, tuple(value)
