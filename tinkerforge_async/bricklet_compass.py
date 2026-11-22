"""
Module for the Tinkerforge Compass Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/Compass_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

from collections.abc import Sequence
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    SimpleCallbackConfiguration,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, check_length, check_range, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import LinearQuantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    HEADING = 4
    MAGNETIC_FLUX_DENSITY = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_HEADING = 1
    SET_HEADING_CALLBACK_CONFIGURATION = 2
    GET_HEADING_CALLBACK_CONFIGURATION = 3
    GET_MAGNETIC_FLUX_DENSITY = 5
    SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION = 6
    GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION = 7
    SET_CONFIGURATION = 9
    GET_CONFIGURATION = 10
    SET_CALIBRATION = 11
    GET_CALIBRATION = 12


@unique
class DataRate(Enum):
    """
    The data rate options
    """

    DATA_RATE_100HZ = 0
    DATA_RATE_200HZ = 1
    DATA_RATE_400HZ = 2
    DATA_RATE_600HZ = 3


class GetMagneticFluxDensity(NamedTuple):
    x: Decimal
    y: Decimal
    z: Decimal


class GetConfiguration(NamedTuple):
    data_rate: DataRate
    background_calibration: bool


class GetCalibration(NamedTuple):
    offset: tuple[int, ...]
    gain: tuple[int, ...]


ANGLE = LinearQuantity(1, 10)  # raw: 1/10 Degree, returned in °
HEADING = LinearQuantity(1, 10)  # raw: 1/10 Degree, returned in °
X = LinearQuantity(1, 100000000)  # raw: 1/100000000 Tesla, returned in T
Y = LinearQuantity(1, 100000000)  # raw: 1/100000000 Tesla, returned in T
Z = LinearQuantity(1, 100000000)  # raw: 1/100000000 Tesla, returned in T


class BrickletCompass(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    3-axis compass with 10 nanotesla and 0.1° resolution
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_COMPASS
    DEVICE_DISPLAY_NAME = "Compass Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    DataRate: TypeAlias = DataRate

    CALLBACK_FORMATS = {
        CallbackID.HEADING: "h",
        CallbackID.MAGNETIC_FLUX_DENSITY: "i i i",
    }

    CHANNELS = (
        Channel(
            0, getter="get_heading", callbacks=(CallbackID.HEADING,), configuration=ChannelConfiguration("heading")
        ),
        Channel(
            1,
            callbacks=(CallbackID.MAGNETIC_FLUX_DENSITY,),
            configuration=ChannelConfiguration("magnetic_flux_density", thresholds=False, wrap_advanced=True),
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
        option: Threshold | int = Threshold.OFF,
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

    async def get_heading(self) -> Decimal:
        """
        Returns the heading (north = 0 degree, east = 90 degree).

        Alternatively you can use :func:`get_magnetic_flux_density` and calculate the
        heading with ``heading = atan2(y, x) * 180 / PI``.

        Units: heading in ° (0 to 360 °).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HEADING, response_expected=True
        )
        return HEADING.to_si(unpack_payload(payload, "h"))

    async def set_heading_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.HEADING` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.HEADING` callback.

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

        Units: minimum in °, maximum in °.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = ANGLE.from_si(minimum)
        check_range("minimum", minimum_raw, -32768, 32767, minimum)
        maximum_raw = ANGLE.from_si(maximum)
        check_range("maximum", maximum_raw, -32768, 32767, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_HEADING_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c h h"
            ),
            response_expected=response_expected,
        )

    async def get_heading_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_heading_callback_configuration`.

        Units: minimum in °, maximum in °.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_HEADING_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c h h")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), ANGLE.to_si(minimum), ANGLE.to_si(maximum)
        )

    async def get_magnetic_flux_density(self) -> GetMagneticFluxDensity:
        """
        Returns the `magnetic flux density (magnetic induction) <https://en.wikipedia.org/wiki/Magnetic_flux>`__
        for all three axis.

        If you want to get the value periodically, it is recommended to use the
        :attr:`CallbackID.MAGNETIC_FLUX_DENSITY` callback. You can set the callback configuration
        with :func:`set_magnetic_flux_density_callback_configuration`.

        Units: x in T (-0.0008 to 0.0008 T), y in T (-0.0008 to 0.0008 T), z in T (-0.0008 to 0.0008 T).
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETIC_FLUX_DENSITY, response_expected=True
        )
        x, y, z = unpack_payload(payload, "i i i")
        return GetMagneticFluxDensity(X.to_si(x), Y.to_si(y), Z.to_si(z))

    async def set_magnetic_flux_density_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.MAGNETIC_FLUX_DENSITY` callback
        is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_magnetic_flux_density_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_magnetic_flux_density_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MAGNETIC_FLUX_DENSITY_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_configuration(
        self,
        data_rate: DataRate | int = DataRate.DATA_RATE_100HZ,
        background_calibration: bool = True,
        response_expected: bool = True,
    ) -> None:
        """
        Configures the data rate and background calibration.

        * Data Rate: Sets the data rate that is used by the magnetometer.
          The lower the data rate, the lower is the noise on the data.
        * Background Calibration: Set to *true* to enable the background
          calibration and *false* to turn it off. If the background calibration
          is enabled the sensing polarity is flipped once per second to automatically
          calculate and remove offset that is caused by temperature changes.
          This polarity flipping takes about 20ms. This means that once a second
          you will not get new data for a period of 20ms. We highly recommend that
          you keep the background calibration enabled and only disable it if the 20ms
          off-time is a problem in your application.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((DataRate(data_rate).value, bool(background_calibration)), "B !"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        data_rate, background_calibration = unpack_payload(payload, "B !")
        return GetConfiguration(DataRate(data_rate), background_calibration)

    async def set_calibration(self, offset: Sequence[int], gain: Sequence[int], response_expected: bool = True) -> None:
        """
        Sets offset and gain for each of the three axes.

        The Bricklet is factory calibrated. If you want to re-calibrate the
        Bricklet we recommend that you do the calibration through Brick Viewer.

        The calibration is saved in non-volatile memory and only has to be
        done once.
        """
        check_length("offset", offset, 3)
        check_length("gain", gain, 3)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload((list(map(int, offset)), list(map(int, gain))), "3h 3h"),
            response_expected=response_expected,
        )

    async def get_calibration(self) -> GetCalibration:
        """
        Returns the calibration parameters as set by :func:`set_calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CALIBRATION, response_expected=True
        )
        offset, gain = unpack_payload(payload, "3h 3h")
        return GetCalibration(tuple(offset), tuple(gain))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.HEADING:
            return 0, HEADING.to_si(value)
        x, y, z = value
        return 1, GetMagneticFluxDensity(X.to_si(x), Y.to_si(y), Z.to_si(z))
