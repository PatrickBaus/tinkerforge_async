"""
Module for the Tinkerforge Distance IR Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Software/Bricklets/DistanceIRV2_Bricklet_Python.html) implemented using
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

    DISTANCE = 4
    ANALOG_VALUE = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_DISTANCE = 1
    SET_DISTANCE_CALLBACK_CONFIGURATION = 2
    GET_DISTANCE_CALLBACK_CONFIGURATION = 3
    GET_ANALOG_VALUE = 5
    SET_ANALOG_VALUE_CALLBACK_CONFIGURATION = 6
    GET_ANALOG_VALUE_CALLBACK_CONFIGURATION = 7
    SET_MOVING_AVERAGE_CONFIGURATION = 9
    GET_MOVING_AVERAGE_CONFIGURATION = 10
    SET_DISTANCE_LED_CONFIG = 11
    GET_DISTANCE_LED_CONFIG = 12
    SET_SENSOR_TYPE = 13
    GET_SENSOR_TYPE = 14


@unique
class DistanceLEDConfig(Enum):
    """
    The distance led config options
    """

    OFF = 0
    ON = 1
    SHOW_HEARTBEAT = 2
    SHOW_DISTANCE = 3


@unique
class SensorType(Enum):
    """
    The sensor type options
    """

    SENSOR_TYPE_2Y0A41 = 0
    SENSOR_TYPE_2Y0A21 = 1
    SENSOR_TYPE_2Y0A02 = 2


DISTANCE = LinearQuantity(1, 1000)  # raw: 1/1000 Meter, returned in m


class BrickletDistanceIRV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures distance up to 1.5 m with infrared light
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_DISTANCE_IR_V2
    DEVICE_DISPLAY_NAME = "Distance IR Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    DistanceLEDConfig: TypeAlias = DistanceLEDConfig
    SensorType: TypeAlias = SensorType

    CALLBACK_FORMATS = {
        CallbackID.DISTANCE: "H",
        CallbackID.ANALOG_VALUE: "I",
    }

    CHANNELS = (
        Channel(
            0, getter="get_distance", callbacks=(CallbackID.DISTANCE,), configuration=ChannelConfiguration("distance")
        ),
        Channel(
            1,
            getter="get_analog_value",
            callbacks=(CallbackID.ANALOG_VALUE,),
            configuration=ChannelConfiguration("analog_value"),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

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

    async def get_distance(self) -> Decimal:
        """
        Returns the distance measured by the sensor. Possible
        distance ranges are 40 to 300, 100 to 800 and 200 to 1500, depending on the
        selected IR sensor.

        Units: distance in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE, response_expected=True
        )
        return DISTANCE.to_si(unpack_payload(payload, "H"))

    async def set_distance_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.DISTANCE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.DISTANCE` callback.

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

        Units: minimum in m, maximum in m.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = DISTANCE.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = DISTANCE.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c H H"
            ),
            response_expected=response_expected,
        )

    async def get_distance_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_distance_callback_configuration`.

        Units: minimum in m, maximum in m.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            DISTANCE.to_si(minimum),
            DISTANCE.to_si(maximum),
        )

    async def get_analog_value(self) -> int:
        """
        Returns the analog value as read by a analog-to-digital converter.

        This is unfiltered raw data. We made sure that the integration time
        of the ADC is shorter then the measurement interval of the sensor
        (10ms vs 16.5ms). So there is no information lost.

        If you want to do your own calibration or create your own lookup table
        you can use this value.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_analog_value_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: int = 0,
        maximum: int = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ANALOG_VALUE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.ANALOG_VALUE` callback.

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
            function_id=FunctionID.SET_ANALOG_VALUE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum, maximum), "I ! c I I"
            ),
            response_expected=response_expected,
        )

    async def get_analog_value_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_analog_value_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ANALOG_VALUE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c I I")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period), value_has_to_change, Threshold(option), Decimal(minimum), Decimal(maximum)
        )

    async def set_moving_average_configuration(
        self, moving_average_length: int = 25, response_expected: bool = True
    ) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the distance.

        Setting the length to 1 will turn the averaging off. With less averaging, there
        is more noise on the data.

        New data is gathered every ~10ms. With a moving average of length 1000 the
        resulting averaging window has a length of approximately 10s. If you want to do
        long term measurements the longest moving average will give the cleanest results.
        """
        moving_average_length = int(moving_average_length)
        check_range("moving_average_length", moving_average_length, 1, 1000)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE_CONFIGURATION,
            data=pack_payload((moving_average_length,), "H"),
            response_expected=response_expected,
        )

    async def get_moving_average_configuration(self) -> int:
        """
        Returns the moving average configuration as set by :func:`set_moving_average_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOVING_AVERAGE_CONFIGURATION, response_expected=True
        )
        return unpack_payload(payload, "H")

    async def set_distance_led_config(
        self, config: DistanceLEDConfig | int = DistanceLEDConfig.SHOW_DISTANCE, response_expected: bool = True
    ) -> None:
        """
        Configures the distance LED to be either turned off, turned on, blink in
        heartbeat mode or show the distance (brighter = object is nearer).
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DISTANCE_LED_CONFIG,
            data=pack_payload((DistanceLEDConfig(config).value,), "B"),
            response_expected=response_expected,
        )

    async def get_distance_led_config(self) -> DistanceLEDConfig:
        """
        Returns the LED configuration as set by :func:`set_distance_led_config`
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DISTANCE_LED_CONFIG, response_expected=True
        )
        return DistanceLEDConfig(unpack_payload(payload, "B"))

    async def set_sensor_type(self, sensor: SensorType | int, response_expected: bool = True) -> None:
        """
        Sets the sensor type.

        The Bricklet comes configured with the correct sensor type
        and the type is saved in flash (i.e. the Bricklet retains the information if
        power is lost).

        If you want to change the sensor you can set the type in Brick Viewer,
        you will likely never need to call this function from your program.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSOR_TYPE,
            data=pack_payload((SensorType(sensor).value,), "B"),
            response_expected=response_expected,
        )

    async def get_sensor_type(self) -> SensorType:
        """
        Returns the sensor type as set by :func:`set_sensor_type`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_TYPE, response_expected=True
        )
        return SensorType(unpack_payload(payload, "B"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id is CallbackID.DISTANCE:
            return 0, DISTANCE.to_si(value)
        return 1, value
