"""
Module for the Tinkerforge Ambient Light Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/AmbientLight_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias, cast, override

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
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ILLUMINANCE = 13
    ANALOG_VALUE = 14
    ILLUMINANCE_REACHED = 15
    ANALOG_VALUE_REACHED = 16


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ILLUMINANCE = 1
    GET_ANALOG_VALUE = 2
    SET_ILLUMINANCE_CALLBACK_PERIOD = 3
    GET_ILLUMINANCE_CALLBACK_PERIOD = 4
    SET_ANALOG_VALUE_CALLBACK_PERIOD = 5
    GET_ANALOG_VALUE_CALLBACK_PERIOD = 6
    SET_ILLUMINANCE_CALLBACK_THRESHOLD = 7
    GET_ILLUMINANCE_CALLBACK_THRESHOLD = 8
    SET_ANALOG_VALUE_CALLBACK_THRESHOLD = 9
    GET_ANALOG_VALUE_CALLBACK_THRESHOLD = 10
    SET_DEBOUNCE_PERIOD = 11
    GET_DEBOUNCE_PERIOD = 12


DECI_LUX = LinearQuantity(1, 10)  # raw: 1/10 Lux, returned in lx


class BrickletAmbientLight(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures ambient light up to 900lux
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_AMBIENT_LIGHT
    DEVICE_DISPLAY_NAME = "Ambient Light Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.ILLUMINANCE: "H",
        CallbackID.ANALOG_VALUE: "H",
        CallbackID.ILLUMINANCE_REACHED: "H",
        CallbackID.ANALOG_VALUE_REACHED: "H",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_illuminance",
            callbacks=(
                CallbackID.ILLUMINANCE,
                CallbackID.ILLUMINANCE_REACHED,
            ),
            configuration=ChannelConfiguration("illuminance", split=True),
        ),
        Channel(
            1,
            getter="get_analog_value",
            callbacks=(
                CallbackID.ANALOG_VALUE,
                CallbackID.ANALOG_VALUE_REACHED,
            ),
            configuration=ChannelConfiguration("analog_value", split=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> Any:
        """
        Returns the value of the channel with the secondary id `sid`. See `CHANNELS` for the channels.
        """
        return await self._get_value(sid)

    @override
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

    @override
    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_illuminance(self) -> Decimal:
        """
        Returns the illuminance of the ambient light sensor.

        If you want to get the illuminance periodically, it is recommended to use the
        :attr:`CallbackID.ILLUMINANCE` callback and set the period with
        :func:`set_illuminance_callback_period`.

        Units: illuminance in lx (0 to 900 lx).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE, response_expected=True
        )
        return DECI_LUX.to_si(unpack_payload(payload, "H"))

    async def get_analog_value(self) -> int:
        """
        Returns the value as read by a 12-bit analog-to-digital converter.

        .. note::
         The value returned by :func:`get_illuminance` is averaged over several samples
         to yield less noise, while :func:`get_analog_value` gives back raw
         unfiltered analog values. The only reason to use :func:`get_analog_value` is,
         if you need the full resolution of the analog-to-digital converter.

         Also, the analog-to-digital converter covers three different ranges that are
         set dynamically depending on the light intensity. It is impossible to
         distinguish between these ranges with the analog value.

        If you want the analog value periodically, it is recommended to use the
        :attr:`CallbackID.ANALOG_VALUE` callback and set the period with
        :func:`set_analog_value_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE, response_expected=True
        )
        return cast(int, unpack_payload(payload, "H"))

    async def set_illuminance_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ILLUMINANCE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.ILLUMINANCE` callback is only triggered if the illuminance has changed
        since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_illuminance_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_illuminance_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_analog_value_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ANALOG_VALUE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.ANALOG_VALUE` callback is only triggered if the analog value has
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

    async def set_illuminance_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.ILLUMINANCE_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the illuminance is *outside* the min and max values"
         "'i'",    "Callback is triggered when the illuminance is *inside* the min and max values"
         "'<'",    "Callback is triggered when the illuminance is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the illuminance is greater than the min value (max is ignored)"

        Units: minimum in lx, maximum in lx.
        """
        minimum_raw = DECI_LUX.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = DECI_LUX.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c H H"),
            response_expected=response_expected,
        )

    async def get_illuminance_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_illuminance_callback_threshold`.

        Units: minimum in lx, maximum in lx.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(Threshold(option), DECI_LUX.to_si(minimum), DECI_LUX.to_si(maximum))

    async def set_analog_value_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: int = 0,
        maximum: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.ANALOG_VALUE_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the analog value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the analog value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the analog value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the analog value is greater than the min value (max is ignored)"
        """
        minimum = int(minimum)
        check_range("minimum", minimum, 0, 65535)
        maximum = int(maximum)
        check_range("maximum", maximum, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum, maximum), "c H H"),
            response_expected=response_expected,
        )

    async def get_analog_value_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_analog_value_callback_threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(Threshold(option), Decimal(minimum), Decimal(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callbacks

        * :attr:`CallbackID.ILLUMINANCE_REACHED`,
        * :attr:`CallbackID.ANALOG_VALUE_REACHED`

        are triggered, if the thresholds

        * :func:`set_illuminance_callback_threshold`,
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
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.ILLUMINANCE:
            return 0, DECI_LUX.to_si(value)
        if callback_id is CallbackID.ANALOG_VALUE:
            return 1, value
        if callback_id is CallbackID.ILLUMINANCE_REACHED:
            return 0, DECI_LUX.to_si(value)
        return 1, value
