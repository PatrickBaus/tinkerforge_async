"""
Module for the Tinkerforge Distance IR Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DistanceIR_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias, override

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

    DISTANCE = 15
    ANALOG_VALUE = 16
    DISTANCE_REACHED = 17
    ANALOG_VALUE_REACHED = 18


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_DISTANCE = 1
    GET_ANALOG_VALUE = 2
    SET_SAMPLING_POINT = 3
    GET_SAMPLING_POINT = 4
    SET_DISTANCE_CALLBACK_PERIOD = 5
    GET_DISTANCE_CALLBACK_PERIOD = 6
    SET_ANALOG_VALUE_CALLBACK_PERIOD = 7
    GET_ANALOG_VALUE_CALLBACK_PERIOD = 8
    SET_DISTANCE_CALLBACK_THRESHOLD = 9
    GET_DISTANCE_CALLBACK_THRESHOLD = 10
    SET_ANALOG_VALUE_CALLBACK_THRESHOLD = 11
    GET_ANALOG_VALUE_CALLBACK_THRESHOLD = 12
    SET_DEBOUNCE_PERIOD = 13
    GET_DEBOUNCE_PERIOD = 14


METER_1_10000 = LinearQuantity(1, 10000)  # raw: 1/10000 Meter, returned in m
MILLI_METER = LinearQuantity(1, 1000)  # raw: 1/1000 Meter, returned in m


class BrickletDistanceIR(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures distance up to 1.5 m with infrared light
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DISTANCE_IR
    DEVICE_DISPLAY_NAME = "Distance IR Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.DISTANCE: "H",
        CallbackID.ANALOG_VALUE: "H",
        CallbackID.DISTANCE_REACHED: "H",
        CallbackID.ANALOG_VALUE_REACHED: "H",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_distance",
            callbacks=(
                CallbackID.DISTANCE,
                CallbackID.DISTANCE_REACHED,
            ),
            configuration=ChannelConfiguration("distance", split=True),
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

    async def get_distance(self) -> Decimal:
        """
        Returns the distance measured by the sensor. Possible
        distance ranges are 40 to 300, 100 to 800 and 200 to 1500, depending on the
        selected IR sensor.

        If you want to get the distance periodically, it is recommended to use the
        :attr:`CallbackID.DISTANCE` callback and set the period with
        :func:`set_distance_callback_period`.

        Units: distance in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE, response_expected=True
        )
        return MILLI_METER.to_si(unpack_payload(payload, "H"))

    async def get_analog_value(self) -> int:
        """
        Returns the value as read by a 12-bit analog-to-digital converter.

        .. note::
         The value returned by :func:`get_distance` is averaged over several samples
         to yield less noise, while :func:`get_analog_value` gives back raw
         unfiltered analog values. The only reason to use :func:`get_analog_value` is,
         if you need the full resolution of the analog-to-digital converter.

        If you want the analog value periodically, it is recommended to use the
        :attr:`CallbackID.ANALOG_VALUE` callback and set the period with
        :func:`set_analog_value_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_sampling_point(
        self, position: int, distance: float | Decimal, response_expected: bool = True
    ) -> None:
        """
        Sets a sampling point value to a specific position of the lookup table.
        The lookup table comprises 128 equidistant analog values with
        corresponding distances.

        If you measure a distance of 0.5 m at the analog value 2048, you
        should call this function with (64, 5000). The utilized analog-to-digital
        converter has a resolution of 12 bit. With 128 sampling points on the
        whole range, this means that every sampling point has a size of 32
        analog values. Thus the analog value 2048 has the corresponding sampling
        point 64 = 2048/32.

        Sampling points are saved on the EEPROM of the Distance IR Bricklet and
        loaded again on startup.

        .. note::
         An easy way to calibrate the sampling points of the Distance IR Bricklet is
         implemented in the Brick Viewer. If you want to calibrate your Bricklet it is
         highly recommended to use this implementation.

        Units: distance in m.
        """
        position = int(position)
        check_range("position", position, 0, 127)
        distance_raw = METER_1_10000.from_si(distance)
        check_range("distance", distance_raw, 0, 65535, distance)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SAMPLING_POINT,
            data=pack_payload((position, distance_raw), "B H"),
            response_expected=response_expected,
        )

    async def get_sampling_point(self, position: int) -> Decimal:
        """
        Returns the distance to a sampling point position as set by
        :func:`set_sampling_point`.

        Units: distance in m.
        """
        position = int(position)
        check_range("position", position, 0, 127)
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SAMPLING_POINT,
            data=pack_payload((position,), "B"),
            response_expected=True,
        )
        return METER_1_10000.to_si(unpack_payload(payload, "H"))

    async def set_distance_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.DISTANCE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.DISTANCE` callback is only triggered if the distance has changed since the
        last triggering.
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

    async def set_distance_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.DISTANCE_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the distance is *outside* the min and max values"
         "'i'",    "Callback is triggered when the distance is *inside* the min and max values"
         "'<'",    "Callback is triggered when the distance is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the distance is greater than the min value (max is ignored)"

        Units: minimum in m, maximum in m.
        """
        minimum_raw = MILLI_METER.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = MILLI_METER.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c H H"),
            response_expected=response_expected,
        )

    async def get_distance_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_distance_callback_threshold`.

        Units: minimum in m, maximum in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(Threshold(option), MILLI_METER.to_si(minimum), MILLI_METER.to_si(maximum))

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

        * :attr:`CallbackID.DISTANCE_REACHED`,
        * :attr:`CallbackID.ANALOG_VALUE_REACHED`

        are triggered, if the thresholds

        * :func:`set_distance_callback_threshold`,
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
        if callback_id is CallbackID.DISTANCE:
            return 0, MILLI_METER.to_si(value)
        if callback_id is CallbackID.ANALOG_VALUE:
            return 1, value
        if callback_id is CallbackID.DISTANCE_REACHED:
            return 0, MILLI_METER.to_si(value)
        return 1, value
