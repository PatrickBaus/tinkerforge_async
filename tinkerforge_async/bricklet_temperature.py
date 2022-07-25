"""
Module for the Tinkerforge Temperature Bricklet (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature.html)
implemented using Python asyncIO. It does the low-level communication with the Tinkerforge ip connection and also
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

    TEMPERATURE = 8
    TEMPERATURE_REACHED = 9


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_TEMPERATURE = 1
    SET_TEMPERATURE_CALLBACK_PERIOD = 2
    GET_TEMPERATURE_CALLBACK_PERIOD = 3
    SET_TEMPERATURE_CALLBACK_THRESHOLD = 4
    GET_TEMPERATURE_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_I2C_MODE = 10
    GET_I2C_MODE = 11


@unique
class I2cOption(Enum):
    """
    The options are slow (50 kHz) and fast (400 kHz). The slower mode is useful
    in high EMI environments or with long cables.
    """

    FAST = 0
    SLOW = 1


_I2cOption = I2cOption


class BrickletTemperature(Device):
    """
    Measures ambient temperature with 0.5 K accuracy
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_TEMPERATURE
    DEVICE_DISPLAY_NAME = "Temperature Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    I2cOption = I2cOption

    CALLBACK_FORMATS = {
        CallbackID.TEMPERATURE: "h",
        CallbackID.TEMPERATURE_REACHED: "h",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.TEMPERATURE, CallbackID.TEMPERATURE_REACHED),
    }

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> Decimal:
        assert sid == 0

        return await self.get_temperature()

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
        minimum = Decimal("273.15") if minimum is None else minimum
        maximum = Decimal("273.15") if maximum is None else maximum

        assert sid == 0

        await asyncio.gather(
            self.set_temperature_callback_period(period, response_expected),
            self.set_temperature_callback_threshold(option, minimum, maximum, response_expected),
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        assert sid == 0

        period, config = await asyncio.gather(
            self.get_temperature_callback_period(), self.get_temperature_callback_threshold()
        )
        return AdvancedCallbackConfiguration(period, True, *config)

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the sensor. The value
        has a range of -2500 to 8500 and is given in °C/100,
        e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

        If you want to get the temperature periodically, it is recommended
        to use the :cb:`Temperature` callback and set the period with
        :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return self.__value_to_si(unpack_payload(payload, "h"))

    async def set_temperature_callback_period(self, period: int = 0, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Temperature` callback is only triggered if the temperature has changed
        since the last triggering.

        The default value is 0.
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), "I"),
            response_expected=response_expected,
        )

    async def get_temperature_callback_period(self) -> int:
        """
        Returns the period as set by :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_temperature_callback_threshold(
        self,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = Decimal("273.15"),
        maximum: float | Decimal = Decimal("273.15"),
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Temperature Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (option.value.encode("ascii"), self.__si_to_value(minimum), self.__si_to_value(maximum)), "c h h"
            ),
            response_expected=response_expected,
        )

    async def get_temperature_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c h h")
        option = Threshold(option)
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_debounce_period(self, debounce_period: int = 100, response_expected: bool = True) -> None:
        """
        Sets the period in ms with which the threshold callback

        * :cb:`Temperature Reached`

        is triggered, if the threshold

        * :func:`Set Temperature Callback Threshold`

        keeps being reached.

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

    async def set_i2c_mode(self, mode: _I2cOption | int = I2cOption.FAST, response_expected: bool = True) -> None:
        """
        Sets the I2C mode. Possible modes are:

        * 0: Fast (400kHz, default)
        * 1: Slow (100kHz)

        If you have problems with obvious outliers in the
        Temperature Bricklet measurements, they may be caused by EMI issues.
        In this case it may be helpful to lower the I2C speed.

        It is however not recommended to lower the I2C speed in applications where
        a high throughput needs to be achieved.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        mode = I2cOption(mode)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_I2C_MODE,
            data=pack_payload((mode.value,), "B"),
            response_expected=response_expected,
        )

    async def get_i2c_mode(self) -> _I2cOption:
        """
        Returns the I2C mode as set by :func:`Set I2C Mode`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_I2C_MODE, response_expected=True
        )
        return I2cOption(unpack_payload(payload, "B"))

    # pylint: disable=duplicate-code
    @staticmethod
    def __value_to_si(value: int) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value + 27315) / 100

    @staticmethod
    def __si_to_value(value: float | Decimal) -> int:
        return int(value * 100) - 27315

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
                yield Event(self, 0, function_id, self.__value_to_si(value))
