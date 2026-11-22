"""
Module for the Tinkerforge Color Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/ColorV2_Bricklet_Python.html) implemented using
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

    COLOR = 4
    ILLUMINANCE = 8
    COLOR_TEMPERATURE = 12


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_COLOR = 1
    SET_COLOR_CALLBACK_CONFIGURATION = 2
    GET_COLOR_CALLBACK_CONFIGURATION = 3
    GET_ILLUMINANCE = 5
    SET_ILLUMINANCE_CALLBACK_CONFIGURATION = 6
    GET_ILLUMINANCE_CALLBACK_CONFIGURATION = 7
    GET_COLOR_TEMPERATURE = 9
    SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION = 10
    GET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION = 11
    SET_LIGHT = 13
    GET_LIGHT = 14
    SET_CONFIGURATION = 15
    GET_CONFIGURATION = 16


@unique
class Gain(Enum):
    """
    The gain options
    """

    GAIN_1X = 0
    GAIN_4X = 1
    GAIN_16X = 2
    GAIN_60X = 3


@unique
class IntegrationTime(Enum):
    """
    The integration time options
    """

    INTEGRATION_TIME_2MS = 0
    INTEGRATION_TIME_24MS = 1
    INTEGRATION_TIME_101MS = 2
    INTEGRATION_TIME_154MS = 3
    INTEGRATION_TIME_700MS = 4


class GetColor(NamedTuple):
    r: int
    g: int
    b: int
    c: int


class GetConfiguration(NamedTuple):
    gain: Gain
    integration_time: IntegrationTime


KELVIN = LinearQuantity(1)  # raw: 1/1 Kelvin, returned in K


class BrickletColorV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures color (RGB value), illuminance and color temperature
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_COLOR_V2
    DEVICE_DISPLAY_NAME = "Color Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Gain: TypeAlias = Gain
    IntegrationTime: TypeAlias = IntegrationTime

    CALLBACK_FORMATS = {
        CallbackID.COLOR: "H H H H",
        CallbackID.ILLUMINANCE: "I",
        CallbackID.COLOR_TEMPERATURE: "H",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.COLOR,),
            configuration=ChannelConfiguration("color", thresholds=False, wrap_advanced=True),
        ),
        Channel(
            1,
            getter="get_illuminance",
            callbacks=(CallbackID.ILLUMINANCE,),
            configuration=ChannelConfiguration("illuminance"),
        ),
        Channel(
            2,
            getter="get_color_temperature",
            callbacks=(CallbackID.COLOR_TEMPERATURE,),
            configuration=ChannelConfiguration("color_temperature"),
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

    async def get_color(self) -> GetColor:
        """
        Returns the measured color of the sensor.

        The red (r), green (g), blue (b) and clear (c) colors are measured
        with four different photodiodes that are responsive at different
        wavelengths:

        .. image:: /Images/Bricklets/bricklet_color_wavelength_chart_600.jpg
           :scale: 100 %
           :alt: Chart Responsivity / Wavelength
           :align: center
           :target: ../../_images/Bricklets/bricklet_color_wavelength_chart_600.jpg

        If you want to get the color periodically, it is recommended
        to use the :attr:`CallbackID.COLOR` callback and set the period with
        :func:`set_color_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR, response_expected=True
        )
        r, g, b, c = unpack_payload(payload, "H H H H")
        return GetColor(r, g, b, c)

    async def set_color_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.COLOR`
        callback is triggered periodically. A value of 0 turns the callback off.

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
            function_id=FunctionID.SET_COLOR_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_color_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_color_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def get_illuminance(self) -> int:
        """
        Returns the illuminance affected by the gain and integration time as
        set by :func:`set_configuration`. To get the illuminance in Lux apply this formula::

         lux = illuminance * 700 / gain / integration_time

        To get a correct illuminance measurement make sure that the color
        values themselves are not saturated. The color value (R, G or B)
        is saturated if it is equal to the maximum value of 65535.
        In that case you have to reduce the gain, see :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE, response_expected=True
        )
        return cast(int, unpack_payload(payload, "I"))

    async def set_illuminance_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: int = 0,
        maximum: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ILLUMINANCE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.ILLUMINANCE` callback.

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
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum = int(minimum)
        check_range("minimum", minimum, 0, 4294967295)
        maximum = int(maximum)
        check_range("maximum", maximum, 0, 4294967295)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum, maximum), "I ! c I I"
            ),
            response_expected=response_expected,
        )

    async def get_illuminance_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_illuminance_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c I I")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), Decimal(minimum), Decimal(maximum)
        )

    async def get_color_temperature(self) -> Decimal:
        """
        Returns the color temperature.

        To get a correct color temperature measurement make sure that the color
        values themselves are not saturated. The color value (R, G or B)
        is saturated if it is equal to the maximum value of 65535.
        In that case you have to reduce the gain, see :func:`set_configuration`.

        Units: color_temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR_TEMPERATURE, response_expected=True
        )
        return KELVIN.to_si(unpack_payload(payload, "H"))

    async def set_color_temperature_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.COLOR_TEMPERATURE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.COLOR_TEMPERATURE`
        callback.

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

        Units: minimum in K, maximum in K.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = KELVIN.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = KELVIN.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c H H"
            ),
            response_expected=response_expected,
        )

    async def get_color_temperature_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_color_temperature_callback_configuration`.

        Units: minimum in K, maximum in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), KELVIN.to_si(minimum), KELVIN.to_si(maximum)
        )

    async def set_light(self, enable: bool = False, response_expected: bool = True) -> None:
        """
        Turns the white LED on the Bricklet on/off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_LIGHT,
            data=pack_payload((bool(enable),), "!"),
            response_expected=response_expected,
        )

    async def get_light(self) -> bool:
        """
        Returns the value as set by :func:`set_light`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_LIGHT, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def set_configuration(
        self,
        gain: Gain | int = Gain.GAIN_60X,
        integration_time: IntegrationTime | int = IntegrationTime.INTEGRATION_TIME_154MS,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration of the sensor. Gain and integration time
        can be configured this way.

        For configuring the gain:

        * 0: 1x Gain
        * 1: 4x Gain
        * 2: 16x Gain
        * 3: 60x Gain

        For configuring the integration time:

        * 0: 2.4ms
        * 1: 24ms
        * 2: 101ms
        * 3: 154ms
        * 4: 700ms

        Increasing the gain enables the sensor to detect a
        color from a higher distance.

        The integration time provides a trade-off between conversion time
        and accuracy. With a longer integration time the values read will
        be more accurate but it will take longer to get the conversion
        results.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((Gain(gain).value, IntegrationTime(integration_time).value), "B B"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        gain, integration_time = unpack_payload(payload, "B B")
        return GetConfiguration(Gain(gain), IntegrationTime(integration_time))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.COLOR:
            r, g, b, c = value
            return 0, GetColor(r, g, b, c)
        if callback_id is CallbackID.ILLUMINANCE:
            return 1, value
        return 2, KELVIN.to_si(value)
