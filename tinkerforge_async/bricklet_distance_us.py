"""
Module for the Tinkerforge Distance US Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DistanceUS_Bricklet_Python.html) implemented using
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

from .devices import BasicCallbackConfiguration, Channel, Device, DeviceIdentifier
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

    DISTANCE = 8
    DISTANCE_REACHED = 9


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_DISTANCE_VALUE = 1
    SET_DISTANCE_CALLBACK_PERIOD = 2
    GET_DISTANCE_CALLBACK_PERIOD = 3
    SET_DISTANCE_CALLBACK_THRESHOLD = 4
    GET_DISTANCE_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_MOVING_AVERAGE = 10
    GET_MOVING_AVERAGE = 11


class BrickletDistanceUS(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures distance between 0.02 m and 4 m with ultrasound
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DISTANCE_US
    DEVICE_DISPLAY_NAME = "Distance US Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.DISTANCE: "H",
        CallbackID.DISTANCE_REACHED: "H",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.DISTANCE,)),
        Channel(1, callbacks=(CallbackID.DISTANCE_REACHED,)),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_distance_value(self) -> int:
        """
        Returns the current distance value measured by the sensor.
        A small value corresponds to a small distance, a big
        value corresponds to a big distance. The relation between the measured distance
        value and the actual distance is affected by the 5V supply voltage (deviations
        in the supply voltage result in deviations in the distance values) and is
        non-linear (resolution is bigger at close range).

        If you want to get the distance value periodically, it is recommended to
        use the :attr:`CallbackID.DISTANCE` callback and set the period with
        :func:`set_distance_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_VALUE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_distance_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.DISTANCE` callback is triggered
        periodically. A value of 0 turns the callback off.

        Der :attr:`CallbackID.DISTANCE` callback is only triggered if the distance value has changed
        since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_distance_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_distance_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_distance_callback_threshold(
        self, option: Threshold | str, minimum: int, maximum: int, response_expected: bool = True
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.DISTANCE_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the distance value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the distance value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the distance value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the distance value is greater than the min value (max is ignored)"
        """
        minimum = int(minimum)
        check_range("minimum", minimum, 0, 4095)
        maximum = int(maximum)
        check_range("maximum", maximum, 0, 4095)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum, maximum), "c H H"),
            response_expected=response_expected,
        )

    async def get_distance_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_distance_callback_threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(Threshold(option), Decimal(minimum), Decimal(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callbacks

        * :attr:`CallbackID.DISTANCE_REACHED`,

        are triggered, if the thresholds

        * :func:`set_distance_callback_threshold`,

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

    async def set_moving_average(self, average: int = 20, response_expected: bool = True) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the distance value.

        Setting the length to 0 will turn the averaging completely off. With less
        averaging, there is more noise on the data.
        """
        average = int(average)
        check_range("average", average, 0, 100)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE,
            data=pack_payload((average,), "B"),
            response_expected=response_expected,
        )

    async def get_moving_average(self) -> int:
        """
        Returns the length moving average as set by :func:`set_moving_average`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOVING_AVERAGE, response_expected=True
        )
        return unpack_payload(payload, "B")

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.DISTANCE:
            return 0, value
        return 1, value
