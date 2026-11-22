"""
Module for the Tinkerforge Joystick Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/Joystick_Bricklet_Python.html) implemented using
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

from .devices import Channel, Device, DeviceIdentifier
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

    POSITION = 15
    ANALOG_VALUE = 16
    POSITION_REACHED = 17
    ANALOG_VALUE_REACHED = 18
    PRESSED = 19
    RELEASED = 20


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_POSITION = 1
    IS_PRESSED = 2
    GET_ANALOG_VALUE = 3
    CALIBRATE = 4
    SET_POSITION_CALLBACK_PERIOD = 5
    GET_POSITION_CALLBACK_PERIOD = 6
    SET_ANALOG_VALUE_CALLBACK_PERIOD = 7
    GET_ANALOG_VALUE_CALLBACK_PERIOD = 8
    SET_POSITION_CALLBACK_THRESHOLD = 9
    GET_POSITION_CALLBACK_THRESHOLD = 10
    SET_ANALOG_VALUE_CALLBACK_THRESHOLD = 11
    GET_ANALOG_VALUE_CALLBACK_THRESHOLD = 12
    SET_DEBOUNCE_PERIOD = 13
    GET_DEBOUNCE_PERIOD = 14


class GetPosition(NamedTuple):
    x: int
    y: int


class GetAnalogValue(NamedTuple):
    x: int
    y: int


class GetPositionCallbackThreshold(NamedTuple):
    option: Threshold
    min_x: int
    max_x: int
    min_y: int
    max_y: int


class GetAnalogValueCallbackThreshold(NamedTuple):
    option: Threshold
    min_x: int
    max_x: int
    min_y: int
    max_y: int


class BrickletJoystick(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    2-axis joystick with push-button
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_JOYSTICK
    DEVICE_DISPLAY_NAME = "Joystick Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.POSITION: "h h",
        CallbackID.ANALOG_VALUE: "H H",
        CallbackID.POSITION_REACHED: "h h",
        CallbackID.ANALOG_VALUE_REACHED: "H H",
        CallbackID.PRESSED: "",
        CallbackID.RELEASED: "",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.POSITION,)),
        Channel(1, callbacks=(CallbackID.ANALOG_VALUE,)),
        Channel(2, callbacks=(CallbackID.POSITION_REACHED,)),
        Channel(3, callbacks=(CallbackID.ANALOG_VALUE_REACHED,)),
        Channel(4, callbacks=(CallbackID.PRESSED,)),
        Channel(5, callbacks=(CallbackID.RELEASED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_position(self) -> GetPosition:
        """
        Returns the position of the joystick. The middle position of the joystick is x=0, y=0.
        The returned values are averaged and calibrated (see :func:`calibrate`).

        If you want to get the position periodically, it is recommended to use the
        :attr:`CallbackID.POSITION` callback and set the period with
        :func:`set_position_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POSITION, response_expected=True
        )
        x, y = unpack_payload(payload, "h h")
        return GetPosition(x, y)

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

    async def get_analog_value(self) -> GetAnalogValue:
        """
        Returns the values as read by a 12-bit analog-to-digital converter.

        .. note::
         The values returned by :func:`get_position` are averaged over several samples
         to yield less noise, while :func:`get_analog_value` gives back raw
         unfiltered analog values. The only reason to use :func:`get_analog_value` is,
         if you need the full resolution of the analog-to-digital converter.

        If you want the analog values periodically, it is recommended to use the
        :attr:`CallbackID.ANALOG_VALUE` callback and set the period with
        :func:`set_analog_value_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE, response_expected=True
        )
        x, y = unpack_payload(payload, "H H")
        return GetAnalogValue(x, y)

    async def calibrate(self, response_expected: bool = True) -> None:
        """
        Calibrates the middle position of the joystick. If your Joystick Bricklet
        does not return x=0 and y=0 in the middle position, call this function
        while the joystick is standing still in the middle position.

        The resulting calibration will be saved on the EEPROM of the Joystick
        Bricklet, thus you only have to calibrate it once.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.CALIBRATE, response_expected=response_expected
        )

    async def set_position_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.POSITION` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.POSITION` callback is only triggered if the position has changed since the
        last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POSITION_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_position_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_position_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POSITION_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_analog_value_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ANALOG_VALUE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.ANALOG_VALUE` callback is only triggered if the analog values have
        changed since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_analog_value_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_analog_value_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_position_callback_threshold(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        option: Threshold | str = Threshold.OFF,
        min_x: int = 0,
        max_x: int = 0,
        min_y: int = 0,
        max_y: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.POSITION_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the position is *outside* the min and max values"
         "'i'",    "Callback is triggered when the position is *inside* the min and max values"
         "'<'",    "Callback is triggered when the position is smaller than the min values (max is ignored)"
         "'>'",    "Callback is triggered when the position is greater than the min values (max is ignored)"
        """
        min_x = int(min_x)
        check_range("min_x", min_x, -32768, 32767)
        max_x = int(max_x)
        check_range("max_x", max_x, -32768, 32767)
        min_y = int(min_y)
        check_range("min_y", min_y, -32768, 32767)
        max_y = int(max_y)
        check_range("max_y", max_y, -32768, 32767)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POSITION_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, min_x, max_x, min_y, max_y), "c h h h h"),
            response_expected=response_expected,
        )

    async def get_position_callback_threshold(self) -> GetPositionCallbackThreshold:
        """
        Returns the threshold as set by :func:`set_position_callback_threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POSITION_CALLBACK_THRESHOLD, response_expected=True
        )
        option, min_x, max_x, min_y, max_y = unpack_payload(payload, "c h h h h")
        return GetPositionCallbackThreshold(Threshold(option), min_x, max_x, min_y, max_y)

    async def set_analog_value_callback_threshold(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        option: Threshold | str = Threshold.OFF,
        min_x: int = 0,
        max_x: int = 0,
        min_y: int = 0,
        max_y: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.ANALOG_VALUE_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the analog values are *outside* the min and max values"
         "'i'",    "Callback is triggered when the analog values are *inside* the min and max values"
         "'<'",    "Callback is triggered when the analog values are smaller than the min values (max is ignored)"
         "'>'",    "Callback is triggered when the analog values are greater than the min values (max is ignored)"
        """
        min_x = int(min_x)
        check_range("min_x", min_x, 0, 65535)
        max_x = int(max_x)
        check_range("max_x", max_x, 0, 65535)
        min_y = int(min_y)
        check_range("min_y", min_y, 0, 65535)
        max_y = int(max_y)
        check_range("max_y", max_y, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, min_x, max_x, min_y, max_y), "c H H H H"),
            response_expected=response_expected,
        )

    async def get_analog_value_callback_threshold(self) -> GetAnalogValueCallbackThreshold:
        """
        Returns the threshold as set by :func:`set_analog_value_callback_threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, min_x, max_x, min_y, max_y = unpack_payload(payload, "c H H H H")
        return GetAnalogValueCallbackThreshold(Threshold(option), min_x, max_x, min_y, max_y)

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callbacks

        * :attr:`CallbackID.POSITION_REACHED`,
        * :attr:`CallbackID.ANALOG_VALUE_REACHED`

        are triggered, if the thresholds

        * :func:`set_position_callback_threshold`,
        * :func:`set_analog_value_callback_threshold`

        keep being reached.

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

    @override
    def _convert_callback(  # pylint: disable=too-many-return-statements,too-many-branches,too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.POSITION:
            x, y = value
            return 0, GetPosition(x, y)
        if callback_id is CallbackID.ANALOG_VALUE:
            x, y = value
            return 1, GetAnalogValue(x, y)
        if callback_id is CallbackID.POSITION_REACHED:
            x, y = value
            return 2, GetPosition(x, y)
        if callback_id is CallbackID.ANALOG_VALUE_REACHED:
            x, y = value
            return 3, GetAnalogValue(x, y)
        if callback_id is CallbackID.PRESSED:
            return 4, None
        return 5, None
