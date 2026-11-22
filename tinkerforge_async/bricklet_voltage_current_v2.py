"""
Module for the Tinkerforge Voltage/Current Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/VoltageCurrentV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, Channel, ChannelConfiguration, DeviceIdentifier
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

    CURRENT = 4
    VOLTAGE = 8
    POWER = 12


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_CURRENT = 1
    SET_CURRENT_CALLBACK_CONFIGURATION = 2
    GET_CURRENT_CALLBACK_CONFIGURATION = 3
    GET_VOLTAGE = 5
    SET_VOLTAGE_CALLBACK_CONFIGURATION = 6
    GET_VOLTAGE_CALLBACK_CONFIGURATION = 7
    GET_POWER = 9
    SET_POWER_CALLBACK_CONFIGURATION = 10
    GET_POWER_CALLBACK_CONFIGURATION = 11
    SET_CONFIGURATION = 13
    GET_CONFIGURATION = 14
    SET_CALIBRATION = 15
    GET_CALIBRATION = 16


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
    voltage_multiplier: int
    voltage_divisor: int
    current_multiplier: int
    current_divisor: int


MILLI_AMPERE = LinearQuantity(1, 1000)  # raw: 1/1000 Ampere, returned in A
MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V
MILLI_WATT = LinearQuantity(1, 1000)  # raw: 1/1000 Watt, returned in W


class BrickletVoltageCurrentV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures power, DC voltage and DC current up to 720W/36V/20A
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_VOLTAGE_CURRENT_V2
    DEVICE_DISPLAY_NAME = "Voltage/Current Bricklet 2.0"

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
    }

    CHANNELS = (
        Channel(
            0, getter="get_current", callbacks=(CallbackID.CURRENT,), configuration=ChannelConfiguration("current")
        ),
        Channel(
            1, getter="get_voltage", callbacks=(CallbackID.VOLTAGE,), configuration=ChannelConfiguration("voltage")
        ),
        Channel(2, getter="get_power", callbacks=(CallbackID.POWER,), configuration=ChannelConfiguration("power")),
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

    async def get_current(self) -> Decimal:
        """
        Returns the current.

        Units: current in A (-20 to 20 A).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT, response_expected=True
        )
        return MILLI_AMPERE.to_si(unpack_payload(payload, "i"))

    async def set_current_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.CURRENT` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.CURRENT` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in A, maximum in A.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = MILLI_AMPERE.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = MILLI_AMPERE.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CURRENT_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
            ),
            response_expected=response_expected,
        )

    async def get_current_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_current_callback_configuration`.

        Units: minimum in A, maximum in A.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CURRENT_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            MILLI_AMPERE.to_si(minimum),
            MILLI_AMPERE.to_si(maximum),
        )

    async def get_voltage(self) -> Decimal:
        """
        Returns the voltage.

        Units: voltage in V (0 to 36 V).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "i"))

    async def set_voltage_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.VOLTAGE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.VOLTAGE` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in V, maximum in V.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = MILLI_VOLT.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = MILLI_VOLT.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
            ),
            response_expected=response_expected,
        )

    async def get_voltage_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_voltage_callback_configuration`.

        Units: minimum in V, maximum in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            MILLI_VOLT.to_si(minimum),
            MILLI_VOLT.to_si(maximum),
        )

    async def get_power(self) -> Decimal:
        """
        Returns the power.

        Units: power in W (0 to 720 W).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POWER, response_expected=True
        )
        return MILLI_WATT.to_si(unpack_payload(payload, "i"))

    async def set_power_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.POWER` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.POWER` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        Units: minimum in W, maximum in W.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = MILLI_WATT.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = MILLI_WATT.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_POWER_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
            ),
            response_expected=response_expected,
        )

    async def get_power_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_power_callback_configuration`.

        Units: minimum in W, maximum in W.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_POWER_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            MILLI_WATT.to_si(minimum),
            MILLI_WATT.to_si(maximum),
        )

    async def set_configuration(
        self,
        averaging: Averaging | int = Averaging.AVERAGING_64,
        voltage_conversion_time: ConversionTime | int = ConversionTime.CONVERSION_TIME_1_1MS,
        current_conversion_time: ConversionTime | int = ConversionTime.CONVERSION_TIME_1_1MS,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration of the Voltage/Current Bricklet 2.0. It is
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

    async def set_calibration(
        self,
        voltage_multiplier: int,
        voltage_divisor: int,
        current_multiplier: int,
        current_divisor: int,
        response_expected: bool = True,
    ) -> None:
        """
        Since the ADC and the shunt resistor used for the measurements
        are not perfect they need to be calibrated by a multiplier and
        a divisor if a very precise reading is needed.

        For example, if you are expecting a current of 1000mA and you
        are measuring 1023mA, you can calibrate the Voltage/Current Bricklet
        by setting the current multiplier to 1000 and the divisor to 1023.
        The same applies for the voltage.

        The calibration will be saved on the EEPROM of the Voltage/Current
        Bricklet and only needs to be done once.
        """
        voltage_multiplier = int(voltage_multiplier)
        check_range("voltage_multiplier", voltage_multiplier, 0, 65535)
        voltage_divisor = int(voltage_divisor)
        check_range("voltage_divisor", voltage_divisor, 0, 65535)
        current_multiplier = int(current_multiplier)
        check_range("current_multiplier", current_multiplier, 0, 65535)
        current_divisor = int(current_divisor)
        check_range("current_divisor", current_divisor, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload((voltage_multiplier, voltage_divisor, current_multiplier, current_divisor), "H H H H"),
            response_expected=response_expected,
        )

    async def get_calibration(self) -> GetCalibration:
        """
        Returns the calibration as set by :func:`set_calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CALIBRATION, response_expected=True
        )
        voltage_multiplier, voltage_divisor, current_multiplier, current_divisor = unpack_payload(payload, "H H H H")
        return GetCalibration(voltage_multiplier, voltage_divisor, current_multiplier, current_divisor)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.CURRENT:
            return 0, MILLI_AMPERE.to_si(value)
        if callback_id is CallbackID.VOLTAGE:
            return 1, MILLI_VOLT.to_si(value)
        return 2, MILLI_WATT.to_si(value)
