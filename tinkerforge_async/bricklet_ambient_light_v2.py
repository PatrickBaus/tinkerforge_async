"""
Module for the Tinkerforge Ambient Light Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Ambient_Light_V2.html) implemented using Python asyncio. It does
the low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""
# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

import asyncio
from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple

from .devices import AdvancedCallbackConfiguration, BasicCallbackConfiguration, Device, DeviceIdentifier, Event
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

    ILLUMINANCE = 10
    ILLUMINANCE_REACHED = 11


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ILLUMINANCE = 1
    SET_ILLUMINANCE_CALLBACK_PERIOD = 2
    GET_ILLUMINANCE_CALLBACK_PERIOD = 3
    SET_ILLUMINANCE_CALLBACK_THRESHOLD = 4
    GET_ILLUMINANCE_CALLBACK_THRESHOLD = 5
    SET_DEBOUNCE_PERIOD = 6
    GET_DEBOUNCE_PERIOD = 7
    SET_CONFIGURATION = 8
    GET_CONFIGURATION = 9


@unique
class IlluminanceRange(Enum):
    """
    These ranges define the maximum illuminance before the sensor goes out of
    range.
    """

    RANGE_UNLIMITED = 6
    RANGE_64000LUX = 0
    RANGE_32000LUX = 1
    RANGE_16000LUX = 2
    RANGE_8000LUX = 3
    RANGE_1300LUX = 4
    RANGE_600LUX = 5


_IlluminanceRange = IlluminanceRange  # We need the alias for MyPy type hinting


@unique
class IntegrationTime(Enum):
    """
    The illuminance sensor integration time. A longer integration time decreases noise while sacrificing speed.
    """

    TIME_50MS = 0
    TIME_100MS = 1
    TIME_150MS = 2
    TIME_200MS = 3
    TIME_250MS = 4
    TIME_300MS = 5
    TIME_350MS = 6
    TIME_400MS = 7


_IntegrationTime = IntegrationTime  # We need the alias for MyPy type hinting


class GetConfiguration(NamedTuple):
    illuminance_range: IlluminanceRange
    integration_time: IntegrationTime


class BrickletAmbientLightV2(Device):
    """
    Measures ambient light up to 64000lux
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_AMBIENT_LIGHT_V2
    DEVICE_DISPLAY_NAME = "Ambient Light Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    IlluminanceRange = IlluminanceRange
    IntegrationTime = IntegrationTime
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.ILLUMINANCE: "I",
        CallbackID.ILLUMINANCE_REACHED: "I",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.ILLUMINANCE, CallbackID.ILLUMINANCE_REACHED),
    }

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> Decimal:
        assert sid == 0

        return await self.get_illuminance()

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,unused-argument
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

        await asyncio.gather(
            self.set_illuminance_callback_period(period, response_expected),
            self.set_illuminance_callback_threshold(option, minimum, maximum, response_expected),
        )

    async def get_callback_configuration(self, sid) -> AdvancedCallbackConfiguration:
        assert sid == 0

        period, config = await asyncio.gather(
            self.get_illuminance_callback_period(), self.get_illuminance_callback_threshold()
        )
        return AdvancedCallbackConfiguration(period, True, *config)

    async def get_illuminance(self) -> Decimal:
        """
        Returns the illuminance of the ambient light sensor. The measurement range goes up to about 100000lux, but above
         64000lux the precision starts to drop.

        .. versionchanged:: 2.0.2$nbsp;(Plugin)
          An illuminance of 0lux indicates that the sensor is saturated and the configuration should be modified, see
          :func:`Set Configuration`.

        If you want to get the illuminance periodically, it is recommended to use the :cb:`Illuminance` callback and set
        the period with :func:`Set Illuminance Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE, response_expected=True
        )
        return self.__value_to_si(unpack_payload(payload, "I"))

    async def set_illuminance_callback_period(self, period: int = 0, response_expected=True) -> None:
        """
        Sets the period with which the :cb:`Illuminance` callback is triggered periodically. A value of 0 turns the
        callback off.

        The :cb:`Illuminance` callback is only triggered if the illuminance has changed since the last triggering.
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), "I"),
            response_expected=response_expected,
        )

    async def get_illuminance_callback_period(self) -> int:
        """
        Returns the period as set by :func:`Set Illuminance Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_PERIOD, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_illuminance_callback_threshold(
        self,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Illuminance Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the illuminance is *outside* the min and max values"
         "'i'",    "Callback is triggered when the illuminance is *inside* the min and max values"
         "'<'",    "Callback is triggered when the illuminance is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the illuminance is greater than the min value (max is ignored)"
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)
        assert minimum >= 0
        assert maximum >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (option.value.encode("ascii"), self.__si_to_value(minimum), self.__si_to_value(maximum)), "c I I"
            ),
            response_expected=response_expected,
        )

    async def get_illuminance_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Illuminance Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c I I")
        option = Threshold(option)
        minimum, maximum = self.__value_to_si(minimum), self.__value_to_si(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_debounce_period(self, debounce_period: int = 100, response_expected: bool = True) -> None:
        """
        Sets the period with which the threshold callbacks

        * :cb:`Illuminance Reached`,

        are triggered, if the thresholds

        * :func:`Set Illuminance Callback Threshold`,

        keep being reached.
        """
        assert debounce_period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((int(debounce_period),), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> int:
        """
        Returns the debounce-period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return unpack_payload(payload, "I")

    async def set_configuration(
        self,
        illuminance_range: _IlluminanceRange | int,
        integration_time: _IntegrationTime | int,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the configuration. It is possible to configure an illuminance range between 0-600lux and 0-64000lux and an
        integration time between 50ms and 400ms.

        .. versionadded:: 2.0.2$nbsp;(Plugin)
          The unlimited illuminance range allows to measure up to about 100000lux, but above 64000lux the precision
          starts to drop.

        A smaller illuminance range increases the resolution of the data. A longer integration time will result in less
        noise on the data.

        .. versionchanged:: 2.0.2$nbsp;(Plugin)
          If the actual measure illuminance is out-of-range then the current illuminance range maximum +0.01lux is
          reported by :func:`Get Illuminance` and the :cb:`Illuminance` callback. For example, 800001 for the 0-8000lux
          range.

        .. versionchanged:: 2.0.2$nbsp;(Plugin)
          With a long integration time the sensor might be saturated before the measured value reaches the maximum of
          the selected illuminance range. In this case 0lux is reported by :func:`Get Illuminance` and the
          :cb:`Illuminance` callback.

        If the measurement is out-of-range or the sensor is saturated then you should configure the next higher
        illuminance range. If the highest range is already in use, then start to reduce the integration time.
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
        return GetConfiguration(IlluminanceRange(illuminance_range), IntegrationTime(integration_time))

    @staticmethod
    def __value_to_si(value) -> Decimal:
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 100

    @staticmethod
    def __si_to_value(value) -> int:
        return int(value * 100)

    async def read_events(
        self,
        events: tuple[int | _CallbackID, ...] | list[int | _CallbackID] | None = None,
        sids: tuple[int, ...] | list[int] | None = None,
    ) -> AsyncGenerator[Event, None]:
        registered_events = set()
        if events:
            for event in events:
                registered_events.add(CallbackID(event))
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
