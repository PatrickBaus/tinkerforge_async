"""
Module for the Tinkerforge Ambient Light Bricklet 3.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V3.html) implemented using Python asyncio. It does
the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, Channel, ChannelConfiguration, DeviceIdentifier
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import Quantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ILLUMINANCE = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ILLUMINANCE = 1
    SET_ILLUMINANCE_CALLBACK_CONFIGURATION = 2
    GET_ILLUMINANCE_CALLBACK_CONFIGURATION = 3
    SET_CONFIGURATION = 5
    GET_CONFIGURATION = 6


@unique
class IlluminanceRange(Enum):
    """
    These ranges define the maximum illuminance before the sensor goes out of
    range.
    """

    UNLIMITED = 6
    LUX64000 = 0
    LUX32000 = 1
    LUX16000 = 2
    LUX8000 = 3
    LUX1300 = 4
    LUX600 = 5


@unique
class IntegrationTime(Enum):
    """
    The illuminance sensor integration time. A longer integration time decreases noise while sacrificing speed.
    """

    T50MS = 0
    T100MS = 1
    T150MS = 2
    T200MS = 3
    T250MS = 4
    T300MS = 5
    T350MS = 6
    T400MS = 7


class GetConfiguration(NamedTuple):
    illuminance_range: IlluminanceRange
    integration_time: IntegrationTime


ILLUMINANCE = Quantity(100)  # raw: 1/100 lux


class BrickletAmbientLightV3(BrickletWithMCU):
    """
    Measures ambient light up to 64000lux
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_AMBIENT_LIGHT_V3
    DEVICE_DISPLAY_NAME = "Ambient Light Bricklet 3.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    IlluminanceRange: TypeAlias = IlluminanceRange
    IntegrationTime: TypeAlias = IntegrationTime

    CALLBACK_FORMATS = {
        CallbackID.ILLUMINANCE: "I",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_illuminance",
            callbacks=(CallbackID.ILLUMINANCE,),
            configuration=ChannelConfiguration("illuminance"),
        ),
    )

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> Decimal:
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
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        return await self._get_callback_configuration(sid)

    async def get_illuminance(self) -> Decimal:
        """
        Returns the illuminance of the ambient light sensor. The measurement range goes up to about 100000lux, but
        above 64000lux the precision starts to drop. The illuminance is given in lux, i.e. a value of 4500 means
        that an illuminance of 4500 lux is measured.

        An illuminance of 0lux indicates that the sensor is saturated and the configuration should be modified, see
        :func:`Set Configuration`.


        If you want to get the value periodically, it is recommended to use the :cb:`Illuminance` callback. You can set
        the callback configuration with :func:`Set Illuminance Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE, response_expected=True
        )
        print(unpack_payload(payload, "I"))
        return ILLUMINANCE.to_si(unpack_payload(payload, "I"))

    async def set_illuminance_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :cb:`Illuminance` callback is triggered periodically. A value of 0 turns
        the callback off.

        If the `value has to change`-parameter is set to true, the callback is only triggered after the value has
        changed. If the value didn't change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period, independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Illuminance` callback.

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
        if not isinstance(option, Threshold):
            option = Threshold(option)
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")
        if minimum < 0:
            raise ValueError(f"Invalid argument: expected minimum >= 0, got minimum={minimum!r}")
        if maximum < 0:
            raise ValueError(f"Invalid argument: expected maximum >= 0, got maximum={maximum!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    seconds_to_ms(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    ILLUMINANCE.from_si(minimum),
                    ILLUMINANCE.from_si(maximum),
                ),
                "I ! c I I",
            ),
            response_expected=response_expected,
        )

    async def get_illuminance_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c I I")
        option = Threshold(option)
        minimum, maximum = ILLUMINANCE.to_si(minimum), ILLUMINANCE.to_si(maximum)
        return AdvancedCallbackConfiguration(ms_to_seconds(period), value_has_to_change, option, minimum, maximum)

    async def set_configuration(
        self,
        illuminance_range: IlluminanceRange | int = IlluminanceRange.LUX8000,
        integration_time: IntegrationTime | int = IntegrationTime.T150MS,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration. It is possible to configure an illuminance range between 0-600lux and 0-64000lux and an
        integration time between 50ms and 400ms.

        The unlimited illuminance range allows to measure up to about 100000lux, but above 64000lux the precision starts
        to drop.

        A smaller illuminance range increases the resolution of the data. A longer integration time will result in less
        noise on the data.

        If the actual measure illuminance is out-of-range then the current illuminance range maximum +0.01lux is
        reported by :func:`Get Illuminance` and the :cb:`Illuminance` callback. For example, 8000.01 for the 0-8000lux
        range.

        With a long integration time the sensor might be saturated before the measured value reaches the maximum of the
        selected illuminance range. In this case 0lux is reported by :func:`Get Illuminance` and the :cb:`Illuminance`
        callback.

        If the measurement is out-of-range or the sensor is saturated then you should configure the next higher
        illuminance range. If the highest range is already in use, then start to reduce the integration time.

        The default values are 0-8000lux illuminance range and 150ms integration time.
        """
        if not isinstance(illuminance_range, IlluminanceRange):
            illuminance_range = IlluminanceRange(illuminance_range)
        if not isinstance(integration_time, IntegrationTime):
            integration_time = IntegrationTime(integration_time)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((illuminance_range.value, integration_time.value), "B B"),
            response_expected=response_expected,
        )

    async def get_configuration(self) -> GetConfiguration:
        """
        Returns the configuration as set by :func:`Set Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CONFIGURATION, response_expected=True
        )
        illuminance_range, integration_time = unpack_payload(payload, "B B")
        illuminance_range, integration_time = IlluminanceRange(illuminance_range), IntegrationTime(integration_time)
        return GetConfiguration(illuminance_range, integration_time)

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, ILLUMINANCE.to_si(value)
