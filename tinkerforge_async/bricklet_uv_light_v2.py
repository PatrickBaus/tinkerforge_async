"""
Module for the Tinkerforge UV Light Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/UVLightV2_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias

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

    UVA = 4
    UVB = 8
    UVI = 12


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_UVA = 1
    SET_UVA_CALLBACK_CONFIGURATION = 2
    GET_UVA_CALLBACK_CONFIGURATION = 3
    GET_UVB = 5
    SET_UVB_CALLBACK_CONFIGURATION = 6
    GET_UVB_CALLBACK_CONFIGURATION = 7
    GET_UVI = 9
    SET_UVI_CALLBACK_CONFIGURATION = 10
    GET_UVI_CALLBACK_CONFIGURATION = 11
    SET_CONFIGURATION = 13
    GET_CONFIGURATION = 14


@unique
class IntegrationTime(Enum):
    """
    The integration time options
    """

    INTEGRATION_TIME_50MS = 0
    INTEGRATION_TIME_100MS = 1
    INTEGRATION_TIME_200MS = 2
    INTEGRATION_TIME_400MS = 3
    INTEGRATION_TIME_800MS = 4


UVA = LinearQuantity(1, 10000)  # raw: 1/10000 Watt Per Square Meter, returned in W/m²
UVB = LinearQuantity(1, 10000)  # raw: 1/10000 Watt Per Square Meter, returned in W/m²
UVI = LinearQuantity(1, 10)  # raw: 1/10 UV Index, returned in UVI
VALUE = LinearQuantity(1, 10000)  # raw: 1/10000 Watt Per Square Meter, returned in W/m²
VALUE_2 = LinearQuantity(1, 10)  # raw: 1/10 UV Index, returned in UVI


class BrickletUVLightV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures UV-A, UV-B and UV index
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_UV_LIGHT_V2
    DEVICE_DISPLAY_NAME = "UV Light Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    IntegrationTime: TypeAlias = IntegrationTime

    CALLBACK_FORMATS = {
        CallbackID.UVA: "i",
        CallbackID.UVB: "i",
        CallbackID.UVI: "i",
    }

    CHANNELS = (
        Channel(0, getter="get_uva", callbacks=(CallbackID.UVA,), configuration=ChannelConfiguration("uva")),
        Channel(1, getter="get_uvb", callbacks=(CallbackID.UVB,), configuration=ChannelConfiguration("uvb")),
        Channel(2, getter="get_uvi", callbacks=(CallbackID.UVI,), configuration=ChannelConfiguration("uvi")),
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

    async def get_uva(self) -> Decimal:
        """
        Returns the UVA intensity of the sensor.
        The sensor has not weighted the intensity with the erythemal
        action spectrum to get the skin-affecting irradiation. Therefore, you cannot
        just divide the value by 250 to get the UVA index. To get the UV index use
        :func:`get_uvi`.

        If the sensor is saturated, then -1 is returned, see :func:`set_configuration`.

        If you want to get the intensity periodically, it is recommended to use the
        :attr:`CallbackID.UVA` callback and set the period with
        :func:`set_uva_callback_configuration`.

        Units: uva in W/m².
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_UVA, response_expected=True)
        return UVA.to_si(unpack_payload(payload, "i"))

    async def set_uva_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.UVA` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.UVA` callback.

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

        Units: minimum in W/m², maximum in W/m².
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = VALUE.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = VALUE.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_UVA_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
            ),
            response_expected=response_expected,
        )

    async def get_uva_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_uva_callback_configuration`.

        Units: minimum in W/m², maximum in W/m².
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_UVA_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), VALUE.to_si(minimum), VALUE.to_si(maximum)
        )

    async def get_uvb(self) -> Decimal:
        """
        Returns the UVB intensity of the sensor.
        The sensor has not weighted the intensity with the erythemal
        action spectrum to get the skin-affecting irradiation. Therefore, you cannot
        just divide the value by 250 to get the UVB index. To get the UV index use
        :func:`get_uvi`.

        If the sensor is saturated, then -1 is returned, see :func:`set_configuration`.

        If you want to get the intensity periodically, it is recommended to use the
        :attr:`CallbackID.UVB` callback and set the period with
        :func:`set_uvb_callback_configuration`.

        Units: uvb in W/m².
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_UVB, response_expected=True)
        return UVB.to_si(unpack_payload(payload, "i"))

    async def set_uvb_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.UVB` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.UVB` callback.

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

        Units: minimum in W/m², maximum in W/m².
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = VALUE.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = VALUE.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_UVB_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
            ),
            response_expected=response_expected,
        )

    async def get_uvb_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_uvb_callback_configuration`.

        Units: minimum in W/m², maximum in W/m².
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_UVB_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), VALUE.to_si(minimum), VALUE.to_si(maximum)
        )

    async def get_uvi(self) -> Decimal:
        """
        Returns the UV index of the sensor, the index is given in 1/10.

        If the sensor is saturated, then -1 is returned, see :func:`set_configuration`.

        If you want to get the intensity periodically, it is recommended to use the
        :attr:`CallbackID.UVI` callback and set the period with
        :func:`set_uvi_callback_configuration`.

        Units: uvi in UVI.
        """
        _, payload = await self.ipcon.send_request(device=self, function_id=FunctionID.GET_UVI, response_expected=True)
        return UVI.to_si(unpack_payload(payload, "i"))

    async def set_uvi_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.UVI` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.UVI` callback.

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

        Units: minimum in UVI, maximum in UVI.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = VALUE_2.from_si(minimum)
        check_range("minimum", minimum_raw, -2147483648, 2147483647, minimum)
        maximum_raw = VALUE_2.from_si(maximum)
        check_range("maximum", maximum_raw, -2147483648, 2147483647, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_UVI_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c i i"
            ),
            response_expected=response_expected,
        )

    async def get_uvi_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_uvi_callback_configuration`.

        Units: minimum in UVI, maximum in UVI.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_UVI_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            VALUE_2.to_si(minimum),
            VALUE_2.to_si(maximum),
        )

    async def set_configuration(
        self,
        integration_time: IntegrationTime | int = IntegrationTime.INTEGRATION_TIME_400MS,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration of the sensor. The integration time can be configured
        between 50 and 800 ms. With a shorter integration time the sensor reading updates
        more often but contains more noise. With a longer integration the sensor reading
        contains less noise but updates less often.

        With a longer integration time (especially 800 ms) and a higher UV intensity the
        sensor can be saturated. If this happens the UVA/UVB/UVI readings are all -1.
        In this case you need to choose a shorter integration time.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((IntegrationTime(integration_time).value,), "B"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> IntegrationTime:
        """
        Returns the configuration as set by :func:`set_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        return IntegrationTime(unpack_payload(payload, "B"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.UVA:
            return 0, UVA.to_si(value)
        if callback_id is CallbackID.UVB:
            return 1, UVB.to_si(value)
        return 2, UVI.to_si(value)
