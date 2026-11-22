"""
Module for the Tinkerforge Color Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/Color_Bricklet_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import Channel, Device, DeviceIdentifier
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

    COLOR = 8
    COLOR_REACHED = 9
    ILLUMINANCE = 21
    COLOR_TEMPERATURE = 22


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_COLOR = 1
    SET_COLOR_CALLBACK_PERIOD = 2
    GET_COLOR_CALLBACK_PERIOD = 3
    SET_COLOR_CALLBACK_THRESHOLD = 4
    GET_COLOR_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    LIGHT_ON = 10
    LIGHT_OFF = 11
    IS_LIGHT_ON = 12
    SET_CONFIG = 13
    GET_CONFIG = 14
    GET_ILLUMINANCE = 15
    GET_COLOR_TEMPERATURE = 16
    SET_ILLUMINANCE_CALLBACK_PERIOD = 17
    GET_ILLUMINANCE_CALLBACK_PERIOD = 18
    SET_COLOR_TEMPERATURE_CALLBACK_PERIOD = 19
    GET_COLOR_TEMPERATURE_CALLBACK_PERIOD = 20


@unique
class Light(Enum):
    """
    The light options
    """

    ON = 0
    OFF = 1


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


class GetColorCallbackThreshold(NamedTuple):
    option: Threshold
    min_r: int
    max_r: int
    min_g: int
    max_g: int
    min_b: int
    max_b: int
    min_c: int
    max_c: int


class GetConfig(NamedTuple):
    gain: Gain
    integration_time: IntegrationTime


KELVIN = LinearQuantity(1)  # raw: 1/1 Kelvin, returned in K


class BrickletColor(Device):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures color (RGB value), illuminance and color temperature
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_COLOR
    DEVICE_DISPLAY_NAME = "Color Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    Light: TypeAlias = Light
    Gain: TypeAlias = Gain
    IntegrationTime: TypeAlias = IntegrationTime

    CALLBACK_FORMATS = {
        CallbackID.COLOR: "H H H H",
        CallbackID.COLOR_REACHED: "H H H H",
        CallbackID.ILLUMINANCE: "I",
        CallbackID.COLOR_TEMPERATURE: "H",
    }

    CHANNELS = (
        Channel(0, callbacks=(CallbackID.COLOR,)),
        Channel(1, callbacks=(CallbackID.COLOR_REACHED,)),
        Channel(2, getter="get_illuminance", callbacks=(CallbackID.ILLUMINANCE,)),
        Channel(3, getter="get_color_temperature", callbacks=(CallbackID.COLOR_TEMPERATURE,)),
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
        :func:`set_color_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR, response_expected=True
        )
        r, g, b, c = unpack_payload(payload, "H H H H")
        return GetColor(r, g, b, c)

    async def set_color_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.COLOR` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.COLOR` callback is only triggered if the color has changed since the
        last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COLOR_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_color_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_color_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_color_callback_threshold(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        option: Threshold | str = Threshold.OFF,
        min_r: int = 0,
        max_r: int = 0,
        min_g: int = 0,
        max_g: int = 0,
        min_b: int = 0,
        max_b: int = 0,
        min_c: int = 0,
        max_c: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :attr:`CallbackID.COLOR_REACHED` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"
        """
        min_r = int(min_r)
        check_range("min_r", min_r, 0, 65535)
        max_r = int(max_r)
        check_range("max_r", max_r, 0, 65535)
        min_g = int(min_g)
        check_range("min_g", min_g, 0, 65535)
        max_g = int(max_g)
        check_range("max_g", max_g, 0, 65535)
        min_b = int(min_b)
        check_range("min_b", min_b, 0, 65535)
        max_b = int(max_b)
        check_range("max_b", max_b, 0, 65535)
        min_c = int(min_c)
        check_range("min_c", min_c, 0, 65535)
        max_c = int(max_c)
        check_range("max_c", max_c, 0, 65535)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COLOR_CALLBACK_THRESHOLD,
            data=pack_payload(
                (Threshold(option).value, min_r, max_r, min_g, max_g, min_b, max_b, min_c, max_c), "c H H H H H H H H"
            ),
            response_expected=response_expected,
        )

    async def get_color_callback_threshold(self) -> GetColorCallbackThreshold:
        """
        Returns the threshold as set by :func:`set_color_callback_threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR_CALLBACK_THRESHOLD, response_expected=True
        )
        option, min_r, max_r, min_g, max_g, min_b, max_b, min_c, max_c = unpack_payload(payload, "c H H H H H H H H")
        return GetColorCallbackThreshold(Threshold(option), min_r, max_r, min_g, max_g, min_b, max_b, min_c, max_c)

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callback

        * :attr:`CallbackID.COLOR_REACHED`

        is triggered, if the threshold

        * :func:`set_color_callback_threshold`

        keeps being reached.

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

    async def light_on(self, response_expected: bool = True) -> None:
        """
        Turns the LED on.
        """
        await self.ipcon.send_request(device=self, function_id=FunctionID.LIGHT_ON, response_expected=response_expected)

    async def light_off(self, response_expected: bool = True) -> None:
        """
        Turns the LED off.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.LIGHT_OFF, response_expected=response_expected
        )

    async def is_light_on(self) -> Light:
        """
        Returns the state of the LED. Possible values are:

        * 0: On
        * 1: Off
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_LIGHT_ON, response_expected=True
        )
        return Light(unpack_payload(payload, "B"))

    async def set_config(
        self,
        gain: Gain | int = Gain.GAIN_60X,
        integration_time: IntegrationTime | int = IntegrationTime.INTEGRATION_TIME_154MS,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration of the sensor. Gain and integration time
        can be configured in this way.

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
        be more accurate but it will take longer time to get the conversion
        results.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIG,
            data=pack_payload((Gain(gain).value, IntegrationTime(integration_time).value), "B B"),
            response_expected=response_expected,
        )

    async def get_config(self) -> GetConfig:
        """
        Returns the configuration as set by :func:`set_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIG, response_expected=True
        )
        gain, integration_time = unpack_payload(payload, "B B")
        return GetConfig(Gain(gain), IntegrationTime(integration_time))

    async def get_illuminance(self) -> int:
        """
        Returns the illuminance affected by the gain and integration time as
        set by :func:`set_config`. To get the illuminance in Lux apply this formula::

         lux = illuminance * 700 / gain / integration_time

        To get a correct illuminance measurement make sure that the color
        values themselves are not saturated. The color value (R, G or B)
        is saturated if it is equal to the maximum value of 65535.
        In that case you have to reduce the gain, see :func:`set_config`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def get_color_temperature(self) -> Decimal:
        """
        Returns the color temperature.

        To get a correct color temperature measurement make sure that the color
        values themselves are not saturated. The color value (R, G or B)
        is saturated if it is equal to the maximum value of 65535.
        In that case you have to reduce the gain, see :func:`set_config`.

        Units: color_temperature in K.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR_TEMPERATURE, response_expected=True
        )
        return KELVIN.to_si(unpack_payload(payload, "H"))

    async def set_illuminance_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.ILLUMINANCE` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.ILLUMINANCE` callback is only triggered if the illuminance has changed
        since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_illuminance_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_illuminance_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_color_temperature_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :attr:`CallbackID.COLOR_TEMPERATURE` callback is
        triggered periodically. A value of 0 turns the callback off.

        The :attr:`CallbackID.COLOR_TEMPERATURE` callback is only triggered if the color temperature
        has changed since the last triggering.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_COLOR_TEMPERATURE_CALLBACK_PERIOD,
            data=pack_payload((period_raw,), "I"),
            response_expected=response_expected,
        )

    async def get_color_temperature_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`set_color_temperature_callback_period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_COLOR_TEMPERATURE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.COLOR:
            r, g, b, c = value
            return 0, GetColor(r, g, b, c)
        if callback_id is CallbackID.COLOR_REACHED:
            r, g, b, c = value
            return 1, GetColor(r, g, b, c)
        if callback_id is CallbackID.ILLUMINANCE:
            return 2, value
        return 3, KELVIN.to_si(value)
