"""
Module for the Tinkerforge Temperature Bricklet (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature.html)
implemented using Python asyncIO. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
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
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import CELSIUS_ZERO, TEMPERATURE

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    TEMPERATURE = 8
    TEMPERATURE_REACHED = 9


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


class BrickletTemperature(Device):
    """
    Measures ambient temperature with 0.5 K accuracy
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_TEMPERATURE
    DEVICE_DISPLAY_NAME = "Temperature Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    I2cOption: TypeAlias = I2cOption

    CALLBACK_FORMATS = {
        CallbackID.TEMPERATURE: "h",
        CallbackID.TEMPERATURE_REACHED: "h",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_temperature",
            callbacks=(CallbackID.TEMPERATURE, CallbackID.TEMPERATURE_REACHED),
            configuration=ChannelConfiguration("temperature", split=True, default=CELSIUS_ZERO),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> Decimal:
        return cast(Decimal, await self._get_value(sid))

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
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the sensor in K. The value has a range of 248.15 to 358.15 K,
        e.g. a value of 315.38 K means that a temperature of 315.38 K is measured.

        If you want to get the temperature periodically, it is recommended
        to use the :cb:`Temperature` callback and set the period with
        :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "h"))

    async def set_temperature_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period in s with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Temperature` callback is only triggered if the temperature has changed
        since the last triggering.

        The default value is 0.
        """
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_temperature_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_temperature_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = CELSIUS_ZERO,
        maximum: float | Decimal = CELSIUS_ZERO,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Temperature Reached` callback. The thresholds are given in K.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

        The default value is ('x', 273.15, 273.15).
        """
        option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (option.value.encode("ascii"), TEMPERATURE.from_si(minimum), TEMPERATURE.from_si(maximum)), "c h h"
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
        minimum, maximum = TEMPERATURE.to_si(minimum), TEMPERATURE.to_si(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_debounce_period(
        self, debounce_period: Duration = Decimal("0.1"), response_expected: bool = True
    ) -> None:
        """
        Sets the period in s with which the threshold callback

        * :cb:`Temperature Reached`

        is triggered, if the threshold

        * :func:`Set Temperature Callback Threshold`

        keeps being reached.

        The default value is 0.1.
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

    async def set_i2c_mode(self, mode: I2cOption | int = I2cOption.FAST, response_expected: bool = True) -> None:
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

    async def get_i2c_mode(self) -> I2cOption:
        """
        Returns the I2C mode as set by :func:`Set I2C Mode`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_I2C_MODE, response_expected=True
        )
        return I2cOption(unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, TEMPERATURE.to_si(value)
