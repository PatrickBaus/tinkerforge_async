"""
Module for the Tinkerforge Rotary Encoder Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/RotaryEncoder_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias

from .devices import (
    AdvancedCallbackConfiguration,
    BasicCallbackConfiguration,
    Channel,
    ChannelConfiguration,
    Device,
    DeviceIdentifier,
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

    COUNT = 8
    COUNT_REACHED = 9
    PRESSED = 11
    RELEASED = 12


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_COUNT = 1
    SET_COUNT_CALLBACK_PERIOD = 2
    GET_COUNT_CALLBACK_PERIOD = 3
    SET_COUNT_CALLBACK_THRESHOLD = 4
    GET_COUNT_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    IS_PRESSED = 10


class BrickletRotaryEncoder(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    360° rotary encoder with push-button
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ROTARY_ENCODER
    DEVICE_DISPLAY_NAME = "Rotary Encoder Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.COUNT: "i",
        CallbackID.COUNT_REACHED: "i",
        CallbackID.PRESSED: "",
        CallbackID.RELEASED: "",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(
                CallbackID.COUNT,
                CallbackID.COUNT_REACHED,
            ),
            configuration=ChannelConfiguration("count", split=True),
        ),
        Channel(1, callbacks=(CallbackID.PRESSED,)),
        Channel(2, callbacks=(CallbackID.RELEASED,)),
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
        return await self._get_callback_configuration(sid)

    async def get_count(self, reset: bool) -> int:
        """
        Returns the current count of the encoder. If you set reset
        to true, the count is set back to 0 directly after the
        current count is read.

        The encoder has 24 steps per rotation

        Turning the encoder to the left decrements the counter,
        so a negative count is possible.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_COUNT,
            data=pack_payload((bool(reset),), "!"),
            response_expected=True,
        )
        return unpack_payload(payload, "i")

    async def set_count_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.COUNT` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.COUNT` callback is only triggered if the count has changed since the
        last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COUNT_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_count_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_count_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COUNT_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_count_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: int = 0,
        maximum: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.COUNT_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the count is *outside* the min and max values"
         "'i'",    "Callback is triggered when the count is *inside* the min and max values"
         "'<'",    "Callback is triggered when the count is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the count is greater than the min value (max is ignored)"
        """
        minimum = int(minimum)
        check_range("minimum", minimum, -2147483648, 2147483647)
        maximum = int(maximum)
        check_range("maximum", maximum, -2147483648, 2147483647)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COUNT_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum, maximum), "c i i"),
            response_expected=response_expected,
        )

    async def get_count_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_count_callback_threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COUNT_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        return BasicCallbackConfiguration(Threshold(option), Decimal(minimum), Decimal(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callback

        * :attr:`CallbackID.COUNT_REACHED`

        is triggered, if the thresholds

        * :func:`set_count_callback_threshold`

        keeps being reached.

        Units: debounce in s.
        """
        debounce_raw = seconds_to_ms(debounce)
        check_range("debounce", debounce_raw, 0, 4294967295, debounce)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((debounce_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> Decimal:
        """
        Returns the debounce period as set by :func:`set_debounce_period`.

        Units: debounce in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def is_pressed(self) -> bool:
        """
        Returns *true* if the button is pressed and *false* otherwise.

        It is recommended to use the :attr:`CallbackID.PRESSED` and :attr:`CallbackID.RELEASED` callbacks
        to handle the button.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_PRESSED, response_expected=True
        )
        return unpack_payload(payload, "!")

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.COUNT:
            return 0, value
        if callback_id is CallbackID.COUNT_REACHED:
            return 0, value
        if callback_id is CallbackID.PRESSED:
            return 1, None
        return 2, None
