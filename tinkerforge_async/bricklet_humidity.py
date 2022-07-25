"""
Module for the Tinkerforge Humidity Bricklet (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Humidity.html)
implemented using Python AsyncIO. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

import asyncio
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator

from .devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration, Device, DeviceIdentifier, Event
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    HUMIDITY = 13
    ANALOG_VALUE = 14
    HUMIDITY_REACHED = 15
    ANALOG_VALUE_REACHED = 16


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_HUMIDITY = 1
    GET_ANALOG_VALUE = 2
    SET_HUMIDITY_CALLBACK_PERIOD = 3
    GET_HUMIDITY_CALLBACK_PERIOD = 4
    SET_ANALOG_VALUE_CALLBACK_PERIOD = 5
    GET_ANALOG_VALUE_CALLBACK_PERIOD = 6
    SET_HUMIDITY_CALLBACK_THRESHOLD = 7
    GET_HUMIDITY_CALLBACK_THRESHOLD = 8
    SET_ANALOG_VALUE_CALLBACK_THRESHOLD = 9
    GET_ANALOG_VALUE_CALLBACK_THRESHOLD = 10
    SET_DEBOUNCE_PERIOD = 11
    GET_DEBOUNCE_PERIOD = 12


class BrickletHumidity(Device):
    """
    Measures relative humidity
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_HUMIDITY
    DEVICE_DISPLAY_NAME = "Humidity Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.HUMIDITY: "H",
        CallbackID.ANALOG_VALUE: "H",
        CallbackID.HUMIDITY_REACHED: "H",
        CallbackID.ANALOG_VALUE_REACHED: "H",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.HUMIDITY, CallbackID.HUMIDITY_REACHED),
        1: (CallbackID.ANALOG_VALUE, CallbackID.ANALOG_VALUE_REACHED),
    }

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> int | Decimal:
        assert sid in (0, 1)

        if sid == 0:
            return await self.get_humidity()
        return await self.get_analog_value()

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,unused-argument
        self,
        sid: int,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        minimum = 0 if minimum is None else minimum
        maximum = 0 if maximum is None else maximum

        assert sid in (0, 1)

        if sid == 0:
            await asyncio.gather(
                self.set_humidity_callback_period(period, response_expected),
                self.set_humidity_callback_threshold(option, minimum, maximum, response_expected),
            )
        else:
            await asyncio.gather(
                self.set_analog_value_callback_period(period, response_expected),
                self.set_analog_value_callback_threshold(option, minimum, maximum, response_expected),
            )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        assert sid in (0, 1)

        if sid == 0:
            period, config = await asyncio.gather(
                self.get_humidity_callback_period(), self.get_humidity_callback_threshold()
            )
        else:
            period, config = await asyncio.gather(
                self.get_analog_value_callback_period(), self.get_analog_value_callback_threshold()
            )
        return AdvancedCallbackConfiguration(period, True, *config)

    async def get_humidity(self) -> Decimal:
        """
        Returns the humidity of the sensor. The value
        has a range of 0 to 1000 and is given in %RH/10 (Relative Humidity),
        i.e. a value of 421 means that a humidity of 42.1 %RH is measured.

        If you want to get the humidity periodically, it is recommended to use the
        :cb:`Humidity` callback and set the period with
        :func:`Set Humidity Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HUMIDITY, response_expected=True
        )
        return self.__value_to_si(unpack_payload(payload, "H"))

    async def get_analog_value(self) -> int:
        """
        Returns the value as read by a 12-bit analog-to-digital converter.
        The value is between 0 and 4095.

        .. note::
         The value returned by :func:`Get Humidity` is averaged over several samples
         to yield less noise, while :func:`Get Analog Value` gives back raw
         unfiltered analog values. The returned humidity value is calibrated for
         room temperatures, if you use the sensor in extremely cold or extremely
         warm environments, you might want to calculate the humidity from
         the analog value yourself. See the `HIH 5030 datasheet
         <https://github.com/Tinkerforge/humidity-bricklet/raw/master/datasheets/hih-5030.pdf>`__.

        If you want the analog value periodically, it is recommended to use the
        :cb:`Analog Value` callback and set the period with
        :func:`Set Analog Value Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_humidity_callback_period(self, period: int = 0, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the :cb:`Humidity` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Humidity` callback is only triggered if the humidity has changed
        since the last triggering.

        The default value is 0.
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HUMIDITY_CALLBACK_PERIOD,
            data=pack_payload((int(period),), "I"),
            response_expected=response_expected,
        )

    async def get_humidity_callback_period(self) -> int:
        """
        Returns the period as set by :func:`Set Humidity Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HUMIDITY_CALLBACK_PERIOD, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_analog_value_callback_period(self, period: int = 0, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the :cb:`Analog Value` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Analog Value` callback is only triggered if the analog value has
        changed since the last triggering.

        The default value is 0.
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ANALOG_VALUE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), "I"),
            response_expected=response_expected,
        )

    async def get_analog_value_callback_period(self) -> int:
        """
        Returns the period as set by :func:`Set Analog Value Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE_CALLBACK_PERIOD, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_humidity_callback_threshold(
        self,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Humidity Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the humidity is *outside* the min and max values"
         "'i'",    "Callback is triggered when the humidity is *inside* the min and max values"
         "'<'",    "Callback is triggered when the humidity is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the humidity is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HUMIDITY_CALLBACK_THRESHOLD,
            data=pack_payload(
                (option.value.encode("ascii"), self.__si_to_value(minimum), self.__si_to_value(maximum)), "c H H"
            ),
            response_expected=response_expected,
        )

    async def get_humidity_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Humidity Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HUMIDITY_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c h h")
        option = Threshold(option)
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_analog_value_callback_threshold(
        self,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ):
        """
        Sets the thresholds for the :cb:`Analog Value Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the analog value is *outside* the min and max values"
         "'i'",    "Callback is triggered when the analog value is *inside* the min and max values"
         "'<'",    "Callback is triggered when the analog value is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the analog value is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
            data=pack_payload((option.value.encode("ascii"), int(minimum), int(maximum)), "c H H"),
            response_expected=response_expected,
        )

    async def get_analog_value_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Analog Value Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD, response_expected=True
        )
        payload = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(Threshold(payload[0]), Decimal(payload[1]), Decimal(payload[2]))

    async def set_debounce_period(self, debounce_period: int = 100, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the threshold callbacks

        * :cb:`Humidity Reached`,
        * :cb:`Analog Value Reached`

        are triggered, if the thresholds

        * :func:`Set Humidity Callback Threshold`,
        * :func:`Set Analog Value Callback Threshold`

        keep being reached.

        The default value is 100.
        """
        assert debounce_period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((int(debounce_period),), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> int:
        """
        Returns the debounce-period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return unpack_payload(payload, "I")

    @staticmethod
    def __value_to_si(value: int) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 10

    @staticmethod
    def __si_to_value(value: float | Decimal) -> int:
        return int(value * 10)

    async def read_events(
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        registered_events = set()
        if events:
            for event in events:
                registered_events.add(self.CallbackID(event))
        if sids is not None:
            for sid in sids:
                for callback in self.SID_TO_CALLBACK.get(sid, []):
                    registered_events.add(callback)

        if not events and not sids:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                if function_id in (CallbackID.HUMIDITY, CallbackID.HUMIDITY_REACHED):
                    yield Event(self, 0, function_id, self.__value_to_si(value))
                else:
                    yield Event(self, 1, function_id, value)
