"""
Module for the Tinkerforge Analog In Bricklet (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Analog_In.html)
implemented using Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

import asyncio
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple

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

    VOLTAGE = 13
    ANALOG_VALUE = 14
    VOLTAGE_REACHED = 15
    ANALOG_VALUE_REACHED = 16


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_VOLTAGE = 1
    GET_ANALOG_VALUE = 2
    SET_VOLTAGE_CALLBACK_PERIOD = 3
    GET_VOLTAGE_CALLBACK_PERIOD = 4
    SET_ANALOG_VALUE_CALLBACK_PERIOD = 5
    GET_ANALOG_VALUE_CALLBACK_PERIOD = 6
    SET_VOLTAGE_CALLBACK_THRESHOLD = 7
    GET_VOLTAGE_CALLBACK_THRESHOLD = 8
    SET_ANALOG_VALUE_CALLBACK_THRESHOLD = 9
    GET_ANALOG_VALUE_CALLBACK_THRESHOLD = 10
    SET_DEBOUNCE_PERIOD = 11
    GET_DEBOUNCE_PERIOD = 12
    SET_RANGE = 17
    GET_RANGE = 18
    SET_AVERAGING = 19
    GET_AVERAGING = 20


@unique
class Range(Enum):
    """
    These ranges define the maximum voltage before the sensor goes out of range.
    """

    AUTOMATIC = 0
    UP_TO_6V = 1
    UP_TO_10V = 2
    UP_TO_36V = 3
    UP_TO_45V = 4
    UP_TO_3V = 5


_Range = Range  # We need the alias for MyPy type hinting


class GetAnalogValueCallbackThreshold(NamedTuple):
    option: Threshold
    minimum: int
    maximum: int


class BrickletAnalogIn(Device):
    """
    Measures DC voltage between 0V and 45V
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ANALOG_IN
    DEVICE_DISPLAY_NAME = "Analog In Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    Range = Range
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.VOLTAGE: "H",
        CallbackID.ANALOG_VALUE: "H",
        CallbackID.VOLTAGE_REACHED: "H",
        CallbackID.ANALOG_VALUE_REACHED: "H",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.VOLTAGE, CallbackID.VOLTAGE_REACHED),
        1: (CallbackID.ANALOG_VALUE, CallbackID.ANALOG_VALUE_REACHED),
    }

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 3)

    async def get_value(self, sid: int) -> int | Decimal:
        assert sid in (0, 1)

        if sid == 0:
            return await self.get_voltage()
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
                self.set_voltage_callback_period(period, response_expected),
                self.set_voltage_callback_threshold(option, minimum, maximum, response_expected),
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
                self.get_voltage_callback_period(), self.get_voltage_callback_threshold()
            )
        else:
            period, config = await asyncio.gather(
                self.get_analog_value_callback_period(), self.get_analog_value_callback_threshold()
            )
        return AdvancedCallbackConfiguration(period, True, *config)

    async def get_voltage(self) -> Decimal:
        """
        Returns the voltage of the sensor. The resolution between 0 and 6V is about 2mV. Between 6 and 45V the
        resolution is about 10mV.

        If you want to get the voltage periodically, it is recommended to use the :cb:`Voltage` callback and set the
        period with :func:`Set Voltage Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE, response_expected=True
        )
        return self.__value_to_si(unpack_payload(payload, "H"))

    async def get_analog_value(self) -> int:
        """
        Returns the value as read by a 12-bit analog-to-digital converter.

        .. note::
         The value returned by :func:`Get Voltage` is averaged over several samples to yield less noise, while
         :func:`Get Analog Value` gives back raw unfiltered analog values. The only reason to use
         :func:`Get Analog Value` is, if you need the full resolution of the analog-to-digital converter.

        If you want the analog value periodically, it is recommended to use the :cb:`Analog Value` callback and set the
        period with :func:`Set Analog Value Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_voltage_callback_period(self, period: int = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :cb:`Voltage` callback is triggered periodically. A value of 0 turns the callback
        off.

        The :cb:`Voltage` callback is only triggered if the voltage has changed since the last triggering.
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), "I"),
            response_expected=response_expected,
        )

    async def get_voltage_callback_period(self) -> int:
        """
        Returns the period as set by :func:`Set Voltage Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE_CALLBACK_PERIOD, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_analog_value_callback_period(self, period: int = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :cb:`Analog Value` callback is triggered periodically. A value of 0 turns the
        callback off.

        The :cb:`Analog Value` callback is only triggered if the analog value has changed since the last triggering.
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

    async def set_voltage_callback_threshold(
        self,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Voltage Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
         "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
         "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (option.value.encode("ascii"), self.__si_to_value(minimum), self.__si_to_value(maximum)), "c H H"
            ),
            response_expected=response_expected,
        )

    async def get_voltage_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Voltage Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        option = Threshold(option)
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_analog_value_callback_threshold(
        self,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
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
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ANALOG_VALUE_CALLBACK_THRESHOLD,
            data=pack_payload((option.value.encode("ascii"), minimum, maximum), "c H H"),
            response_expected=response_expected,
        )

    async def get_analog_value_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Analog Value Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c H H")
        option = Threshold(option)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_debounce_period(self, debounce_period: int = 100, response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callbacks

        * :cb:`Voltage Reached`,
        * :cb:`Analog Value Reached`

        are triggered, if the thresholds

        * :func:`Set Voltage Callback Threshold`,
        * :func:`Set Analog Value Callback Threshold`

        keep being reached.
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

    async def set_range(self, value: _Range | int = Range.AUTOMATIC, response_expected: bool = True):
        """
        Sets the measurement range. Possible ranges:

        * 0: Automatically switched
        * 1: 0V - 6.05V, ~1.48mV resolution
        * 2: 0V - 10.32V, ~2.52mV resolution
        * 3: 0V - 36.30V, ~8.86mV resolution
        * 4: 0V - 45.00V, ~11.25mV resolution
        * 5: 0V - 3.3V, ~0.81mV resolution, new in version 2.0.3$nbsp;(Plugin)

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        if not isinstance(value, Range):
            value = Range(value)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RANGE,
            data=pack_payload((value.value,), "B"),
            response_expected=response_expected,
        )

    async def get_range(self) -> _Range:
        """
        Returns the measurement range as set by :func:`Set Range`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RANGE, response_expected=True
        )
        return Range(unpack_payload(payload, "B"))

    async def set_averaging(self, average: int = 50, response_expected: bool = True) -> None:
        """
        Set the length of a averaging for the voltage value.

        Setting the length to 0 will turn the averaging completely off. If the averaging is off, there is more noise on
        the data, but the data is without delay.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        assert average >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AVERAGING,
            data=pack_payload((int(average),), "B"),
            response_expected=response_expected,
        )

    async def get_averaging(self) -> int:
        """
        Returns the averaging configuration as set by :func:`Set Averaging`.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AVERAGING, response_expected=True
        )
        return unpack_payload(payload, "B")

    @staticmethod
    def __value_to_si(value: int) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 1000

    @staticmethod
    def __si_to_value(value):
        return int(value * 1000)

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
                if function_id in (CallbackID.VOLTAGE, CallbackID.VOLTAGE_REACHED):
                    yield Event(self, 0, function_id, self.__value_to_si(value))
                else:
                    # If it is not a voltage callback there is no need for conversion
                    yield Event(self, 1, function_id, value)
