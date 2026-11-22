"""
Module for the Tinkerforge Analog In Bricklet 3.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/AnalogInV3_Bricklet_Python.html) implemented using
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

    VOLTAGE = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_VOLTAGE = 1
    SET_VOLTAGE_CALLBACK_CONFIGURATION = 2
    GET_VOLTAGE_CALLBACK_CONFIGURATION = 3
    SET_OVERSAMPLING = 5
    GET_OVERSAMPLING = 6
    SET_CALIBRATION = 7
    GET_CALIBRATION = 8


@unique
class Oversampling(Enum):
    """
    The oversampling options
    """

    OVERSAMPLING_32 = 0
    OVERSAMPLING_64 = 1
    OVERSAMPLING_128 = 2
    OVERSAMPLING_256 = 3
    OVERSAMPLING_512 = 4
    OVERSAMPLING_1024 = 5
    OVERSAMPLING_2048 = 6
    OVERSAMPLING_4096 = 7
    OVERSAMPLING_8192 = 8
    OVERSAMPLING_16384 = 9


class GetCalibration(NamedTuple):
    offset: Decimal
    multiplier: int
    divisor: int


MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickletAnalogInV3(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures DC voltage between 0V and 42V
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ANALOG_IN_V3
    DEVICE_DISPLAY_NAME = "Analog In Bricklet 3.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Oversampling: TypeAlias = Oversampling

    CALLBACK_FORMATS = {
        CallbackID.VOLTAGE: "H",
    }

    CHANNELS = (
        Channel(
            0, getter="get_voltage", callbacks=(CallbackID.VOLTAGE,), configuration=ChannelConfiguration("voltage")
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

    async def get_voltage(self) -> Decimal:
        """
        Returns the measured voltage. The resolution is approximately 10mV to 1mV
        depending on the oversampling configuration (:func:`set_oversampling`).

        Units: voltage in V (0 to 42 V).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

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
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = MILLI_VOLT.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c H H"
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
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            MILLI_VOLT.to_si(minimum),
            MILLI_VOLT.to_si(maximum),
        )

    async def set_oversampling(
        self, oversampling: Oversampling | int = Oversampling.OVERSAMPLING_4096, response_expected: bool = True
    ) -> None:
        """
        Sets the oversampling between 32x and 16384x. The Bricklet
        takes one 12bit sample every 17.5µs. Thus an oversampling
        of 32x is equivalent to an integration time of 0.56ms and
        a oversampling of 16384x is equivalent to an integration
        time of 286ms.

        The oversampling uses the moving average principle. A
        new value is always calculated once per millisecond.

        With increased oversampling the noise decreases. With decreased
        oversampling the reaction time increases (changes in voltage will be
        measured faster).
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_OVERSAMPLING,
            data=pack_payload((Oversampling(oversampling).value,), "B"),
            response_expected=response_expected,
        )

    async def get_oversampling(self) -> Oversampling:
        """
        Returns the oversampling value as set by :func:`set_oversampling`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_OVERSAMPLING, response_expected=True
        )
        return Oversampling(unpack_payload(payload, "B"))

    async def set_calibration(
        self, offset: float | Decimal, multiplier: int, divisor: int, response_expected: bool = True
    ) -> None:
        """
        Sets a calibration for the measured voltage value.
        The formula for the calibration is as follows::

         Calibrated Value = (Value + Offset) * Multiplier / Divisor

        We recommend that you use the Brick Viewer to calibrate
        the Bricklet. The calibration will be saved internally and only
        has to be done once.

        Units: offset in V.
        """
        offset_raw = MILLI_VOLT.from_si(offset)
        check_range("offset", offset_raw, -32768, 32767, offset)
        multiplier = int(multiplier)
        check_range("multiplier", multiplier, 0, 65535)
        divisor = int(divisor)
        check_range("divisor", divisor, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload((offset_raw, multiplier, divisor), "h H H"),
            response_expected=response_expected,
        )

    async def get_calibration(self) -> GetCalibration:
        """
        Returns the calibration as set by :func:`set_calibration`.

        Units: offset in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CALIBRATION, response_expected=True
        )
        offset, multiplier, divisor = unpack_payload(payload, "h H H")
        return GetCalibration(MILLI_VOLT.to_si(offset), multiplier, divisor)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, MILLI_VOLT.to_si(value)
