"""
Module for the Tinkerforge Ambient Light Bricklet 3.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V3.html) implemented using Python asyncio. It does
the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple

from .devices import AdvancedCallbackConfiguration, BrickletWithMCU, DeviceIdentifier, Event
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .ip_connection_helper import pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ILLUMINANCE = 4


_CallbackID = CallbackID


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


_IlluminanceRange = IlluminanceRange  # We need the alias for MyPy type hinting


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


_IntegrationTime = IntegrationTime  # We need the alias for MyPy type hinting


class GetConfiguration(NamedTuple):
    illuminance_range: IlluminanceRange
    integration_time: IntegrationTime


class BrickletAmbientLightV3(BrickletWithMCU):
    """
    Measures ambient light up to 64000lux
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_AMBIENT_LIGHT_V3
    DEVICE_DISPLAY_NAME = "Ambient Light Bricklet 3.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    IlluminanceRange = IlluminanceRange
    IntegrationTime = IntegrationTime

    CALLBACK_FORMATS = {
        CallbackID.ILLUMINANCE: "I",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.ILLUMINANCE,),
    }

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> Decimal:
        assert sid == 0

        return await self.get_illuminance()

    async def set_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        sid: int,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ) -> None:
        minimum = 0 if minimum is None else minimum
        maximum = 0 if maximum is None else maximum

        assert sid == 0

        await self.set_illuminance_callback_configuration(
            period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        assert sid == 0

        return await self.get_illuminance_callback_configuration()

    async def get_illuminance(self) -> Decimal:
        """
        Returns the illuminance of the ambient light sensor. The measurement range goes up to about 100000lux, but
        above 64000lux the precision starts to drop. The illuminance is given in lux/100, i.e. a value of 450000 means
        that an illuminance of 4500lux is measured.

        An illuminance of 0lux indicates that the sensor is saturated and the configuration should be modified, see
        :func:`Set Configuration`.


        If you want to get the value periodically, it is recommended to use the :cb:`Illuminance` callback. You can set
        the callback configuration with :func:`Set Illuminance Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE, response_expected=True
        )
        print(unpack_payload(payload, "I"))
        return self.__value_to_si(unpack_payload(payload, "I"))

    async def set_illuminance_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        period: int = 0,
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
        assert period >= 0
        assert minimum >= 0
        assert maximum >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    self.__si_to_value(minimum),
                    self.__si_to_value(maximum),
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
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return AdvancedCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def set_configuration(
        self,
        illuminance_range: _IlluminanceRange | int = IlluminanceRange.LUX8000,
        integration_time: _IntegrationTime | int = IntegrationTime.T150MS,
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
        reported by :func:`Get Illuminance` and the :cb:`Illuminance` callback. For example, 800001 for the 0-8000lux
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

    @staticmethod
    def __value_to_si(value) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 100

    @staticmethod
    def __si_to_value(value: float | Decimal) -> int:
        return int(value * 100)

    async def read_events(
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        registered_events = set()
        if events:
            for event in events:
                registered_events.add(self.CallbackID(event))
        if sids is not None:
            for sid in sids:
                for callback in self.SID_TO_CALLBACK.get(sid, []):
                    registered_events.add(callback)

        if not events and not sids:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                yield Event(self, 0, function_id, self.__value_to_si(value))
