"""
Module for the Tinkerforge Moisture Bricklet (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Moisture.html)
implemented using Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

import typing
from decimal import Decimal
from enum import Enum, unique
from typing import TypeAlias

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
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload

if typing.TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    MOISTURE = 8
    MOISTURE_REACHED = 9


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_MOISTURE = 1
    SET_MOISTURE_CALLBACK_PERIOD = 2
    GET_MOISTURE_CALLBACK_PERIOD = 3
    SET_MOISTURE_CALLBACK_THRESHOLD = 4
    GET_MOISTURE_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_MOVING_AVERAGE = 10
    GET_MOVING_AVERAGE = 11


class BrickletMoisture(Device):
    """
    Measures ambient light up to 64000lux
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_MOISTURE
    DEVICE_DISPLAY_NAME = "Moisture Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.MOISTURE: "H",
        CallbackID.MOISTURE_REACHED: "H",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_moisture_value",
            callbacks=(CallbackID.MOISTURE, CallbackID.MOISTURE_REACHED),
            configuration=ChannelConfiguration("moisture", split=True),
        ),
    )

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> int:
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
    ):
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        return await self._get_callback_configuration(sid)

    async def get_moisture_value(self) -> int:
        """
        Returns the current moisture value. A small value corresponds to little moisture, a big value corresponds
        to a high level of moisture.

        If you want to get the moisture value periodically, it is recommended to use the
        :cb:`Moisture` callback and set the period with :func:`Set Moisture Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOISTURE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_moisture_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :cb:`Moisture` callback is triggered periodically. A value of 0 turns the
        callback off.

        The :cb:`Moisture` callback is only triggered if the moisture value has changed since the last triggering.
        """
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOISTURE_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_moisture_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set Moisture Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOISTURE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_moisture_callback_threshold(
        self,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Moisture Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the moisture value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the moisture value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the moisture value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the moisture value is greater than the min value (max is ignored)"
        """
        option = Threshold(option)
        if minimum < 0:
            raise ValueError(f"Invalid argument: expected minimum >= 0, got minimum={minimum!r}")
        if maximum < 0:
            raise ValueError(f"Invalid argument: expected maximum >= 0, got maximum={maximum!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOISTURE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value.encode("ascii"),
                    int(minimum),
                    int(maximum),
                ),
                "c H H",
            ),
            response_expected=response_expected,
        )

    async def get_moisture_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Illuminance Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOISTURE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(Threshold(option), minimum, maximum)

    async def set_debounce_period(
        self, debounce_period: Duration = Decimal("0.1"), response_expected: bool = True
    ) -> None:
        """
        Sets the period with which the threshold callbacks

        * :cb:`Illuminance Reached`,

        are triggered, if the thresholds

        * :func:`Set Illuminance Callback Threshold`,

        keep being reached.
        """
        if debounce_period < 0:
            raise ValueError(
                f"Invalid argument: expected debounce_period >= 0, got debounce_period={debounce_period!r}"
            )

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((seconds_to_ms(debounce_period),), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> Decimal:
        """
        Returns the debounce-period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_moving_average(self, average: int = 100, response_expected: bool = True) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__ for the moisture value.

        Setting the length to 0 will turn the averaging completely off. With less averaging, there is more noise on the
        data.
        """
        if average < 0:
            raise ValueError(f"Invalid argument: expected average >= 0, got average={average!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE,
            data=pack_payload((int(average),), "B"),
            response_expected=response_expected,
        )

    async def get_moving_average(self) -> int:
        """
        Returns the length moving average as set by :func:`Set Moving Average`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOVING_AVERAGE, response_expected=True
        )
        return unpack_payload(payload, "B")
