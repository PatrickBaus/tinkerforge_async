"""
Module for the Tinkerforge Voltage/Current Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/VoltageCurrent_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

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

    CURRENT = 22
    VOLTAGE = 23
    POWER = 24
    CURRENT_REACHED = 25
    VOLTAGE_REACHED = 26
    POWER_REACHED = 27


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_CURRENT = 1
    GET_VOLTAGE = 2
    GET_POWER = 3
    SET_CONFIGURATION = 4
    GET_CONFIGURATION = 5
    SET_CALIBRATION = 6
    GET_CALIBRATION = 7
    SET_CURRENT_CALLBACK_PERIOD = 8
    GET_CURRENT_CALLBACK_PERIOD = 9
    SET_VOLTAGE_CALLBACK_PERIOD = 10
    GET_VOLTAGE_CALLBACK_PERIOD = 11
    SET_POWER_CALLBACK_PERIOD = 12
    GET_POWER_CALLBACK_PERIOD = 13
    SET_CURRENT_CALLBACK_THRESHOLD = 14
    GET_CURRENT_CALLBACK_THRESHOLD = 15
    SET_VOLTAGE_CALLBACK_THRESHOLD = 16
    GET_VOLTAGE_CALLBACK_THRESHOLD = 17
    SET_POWER_CALLBACK_THRESHOLD = 18
    GET_POWER_CALLBACK_THRESHOLD = 19
    SET_DEBOUNCE_PERIOD = 20
    GET_DEBOUNCE_PERIOD = 21


@unique
class Averaging(Enum):
    """
    The averaging options
    """

    AVERAGING_1 = 0
    AVERAGING_4 = 1
    AVERAGING_16 = 2
    AVERAGING_64 = 3
    AVERAGING_128 = 4
    AVERAGING_256 = 5
    AVERAGING_512 = 6
    AVERAGING_1024 = 7


@unique
class ConversionTime(Enum):
    """
    The conversion time options
    """

    CONVERSION_TIME_140US = 0
    CONVERSION_TIME_204US = 1
    CONVERSION_TIME_332US = 2
    CONVERSION_TIME_588US = 3
    CONVERSION_TIME_1_1MS = 4
    CONVERSION_TIME_2_116MS = 5
    CONVERSION_TIME_4_156MS = 6
    CONVERSION_TIME_8_244MS = 7


class GetConfiguration(NamedTuple):
    averaging: Averaging
    voltage_conversion_time: ConversionTime
    current_conversion_time: ConversionTime


class GetCalibration(NamedTuple):
    gain_multiplier: int
    gain_divisor: int


MILLI_AMPERE = LinearQuantity(1, 1000)  # raw: 1/1000 Ampere, returned in A
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V
MILLI_WATT = LinearQuantity(1, 1000)  # raw: 1/1000 Watt, returned in W


class BrickletVoltageCurrent(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures power, DC voltage and DC current up to 720W/36V/20A
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_VOLTAGE_CURRENT
    DEVICE_DISPLAY_NAME = "Voltage/Current Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Averaging: TypeAlias = Averaging
    ConversionTime: TypeAlias = ConversionTime

    CALLBACK_FORMATS = {
        CallbackID.CURRENT: "i",
        CallbackID.VOLTAGE: "i",
        CallbackID.POWER: "i",
        CallbackID.CURRENT_REACHED: "i",
        CallbackID.VOLTAGE_REACHED: "i",
        CallbackID.POWER_REACHED: "i",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_current",
            callbacks=(
                CallbackID.CURRENT,
                CallbackID.CURRENT_REACHED,
            ),
            configuration=ChannelConfiguration("current", split=True),
        ),
        Channel(
            1,
            getter="get_voltage",
            callbacks=(
                CallbackID.VOLTAGE,
                CallbackID.VOLTAGE_REACHED,
            ),
            configuration=ChannelConfiguration("voltage", split=True),
        ),
        Channel(
            2,
            getter="get_power",
            callbacks=(
                CallbackID.POWER,
                CallbackID.POWER_REACHED,
            ),
            configuration=ChannelConfiguration("power", split=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

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

    async def get_current(self) -> Decimal:
        """
        Returns the current.

        If you want to get the current periodically, it is recommended to use the
        :attr:`CallbackID.CURRENT` callback and set the period with
        :func:`set_current_callback_period`.

        Units: current in A (-20 to 20 A).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT, response_expected=True
        )
        return MILLI_AMPERE.to_si(unpack_payload(payload, "i"))

    async def get_voltage(self) -> Decimal:
        """
        Returns the voltage.

        If you want to get the voltage periodically, it is recommended to use the
        :attr:`CallbackID.VOLTAGE` callback and set the period with
        :func:`set_voltage_callback_period`.

        Units: voltage in V (0 to 36 V).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "i"))

    async def get_power(self) -> Decimal:
        """
        Returns the power.

        If you want to get the power periodically, it is recommended to use the
        :attr:`CallbackID.POWER` callback and set the period with
        :func:`set_power_callback_period`.

        Units: power in W (0 to 720 W).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POWER, response_expected=True
        )
        return MILLI_WATT.to_si(unpack_payload(payload, "i"))

    async def set_configuration(
        self,
        averaging: Averaging | int = Averaging.AVERAGING_64,
        voltage_conversion_time: ConversionTime | int = ConversionTime.CONVERSION_TIME_1_1MS,
        current_conversion_time: ConversionTime | int = ConversionTime.CONVERSION_TIME_1_1MS,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration of the Voltage/Current Bricklet. It is
        possible to configure number of averages as well as
        voltage and current conversion time.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload(
                (
                    Averaging(averaging).value,
                    ConversionTime(voltage_conversion_time).value,
                    ConversionTime(current_conversion_time).value,
                ),
                "B B B",
            ),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        averaging, voltage_conversion_time, current_conversion_time = unpack_payload(payload, "B B B")
        return GetConfiguration(
            Averaging(averaging), ConversionTime(voltage_conversion_time), ConversionTime(current_conversion_time)
        )

    async def set_calibration(self, gain_multiplier: int, gain_divisor: int, response_expected: bool = True) -> None:
        """
        Since the shunt resistor that is used to measure the current is not
        perfectly precise, it needs to be calibrated by a multiplier and
        divisor if a very precise reading is needed.

        For example, if you are expecting a measurement of 1000mA and you
        are measuring 1023mA, you can calibrate the Voltage/Current Bricklet
        by setting the multiplier to 1000 and the divisor to 1023.
        """
        gain_multiplier = int(gain_multiplier)
        check_range("gain_multiplier", gain_multiplier, 0, 65535)
        gain_divisor = int(gain_divisor)
        check_range("gain_divisor", gain_divisor, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload((gain_multiplier, gain_divisor), "H H"),
            response_expected=response_expected,
        )

    async def get_calibration(self) -> GetCalibration:
        """
        Returns the calibration as set by :func:`set_calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CALIBRATION, response_expected=True
        )
        gain_multiplier, gain_divisor = unpack_payload(payload, "H H")
        return GetCalibration(gain_multiplier, gain_divisor)

    async def set_current_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.CURRENT` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.CURRENT` callback is only triggered if the current has changed since
        the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_current_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_current_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_voltage_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.VOLTAGE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.VOLTAGE` callback is only triggered if the voltage has changed since
        the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_voltage_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_voltage_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_power_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.POWER` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.POWER` callback is only triggered if the power has changed since the
        last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POWER_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_power_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`get_power_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POWER_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_current_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.CURRENT_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the current is *outside* the min and max values"
         "'i'",    "Callback is triggered when the current is *inside* the min and max values"
         "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"

        Units: minimum in A, maximum in A.
        """
        minimum_raw = MILLI_AMPERE.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = MILLI_AMPERE.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c i i"),
            response_expected=response_expected,
        )

    async def get_current_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_current_callback_threshold`.

        Units: minimum in A, maximum in A.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        return BasicCallbackConfiguration(Threshold(option), MILLI_AMPERE.to_si(minimum), MILLI_AMPERE.to_si(maximum))

    async def set_voltage_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.VOLTAGE_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
         "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
         "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

        Units: minimum in V, maximum in V.
        """
        minimum_raw = MILLI_VOLT.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = MILLI_VOLT.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c i i"),
            response_expected=response_expected,
        )

    async def get_voltage_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_voltage_callback_threshold`.

        Units: minimum in V, maximum in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        return BasicCallbackConfiguration(Threshold(option), MILLI_VOLT.to_si(minimum), MILLI_VOLT.to_si(maximum))

    async def set_power_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.POWER_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the power is *outside* the min and max values"
         "'i'",    "Callback is triggered when the power is *inside* the min and max values"
         "'<'",    "Callback is triggered when the power is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the power is greater than the min value (max is ignored)"

        Units: minimum in W, maximum in W.
        """
        minimum_raw = MILLI_WATT.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = MILLI_WATT.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POWER_CALLBACK_THRESHOLD,
            data=pack_payload((Threshold(option).value, minimum_raw, maximum_raw), "c i i"),
            response_expected=response_expected,
        )

    async def get_power_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`set_power_callback_threshold`.

        Units: minimum in W, maximum in W.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POWER_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        return BasicCallbackConfiguration(Threshold(option), MILLI_WATT.to_si(minimum), MILLI_WATT.to_si(maximum))

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callbacks

        * :attr:`CallbackID.CURRENT_REACHED`,
        * :attr:`CallbackID.VOLTAGE_REACHED`,
        * :attr:`CallbackID.POWER_REACHED`

        are triggered, if the thresholds

        * :func:`set_current_callback_threshold`,
        * :func:`set_voltage_callback_threshold`,
        * :func:`set_power_callback_threshold`

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

    def _convert_callback(  # pylint: disable=too-many-return-statements,too-many-branches,too-many-locals
        self, callback_id: CallbackID, value: Any
    ) -> tuple[int, Any]:
        if callback_id is CallbackID.CURRENT:
            return 0, MILLI_AMPERE.to_si(value)
        if callback_id is CallbackID.VOLTAGE:
            return 1, MILLI_VOLT.to_si(value)
        if callback_id is CallbackID.POWER:
            return 2, MILLI_WATT.to_si(value)
        if callback_id is CallbackID.CURRENT_REACHED:
            return 0, MILLI_AMPERE.to_si(value)
        if callback_id is CallbackID.VOLTAGE_REACHED:
            return 1, MILLI_VOLT.to_si(value)
        return 2, MILLI_AMPERE.to_si(value)
