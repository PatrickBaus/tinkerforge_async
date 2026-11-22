"""
Module for the Tinkerforge Barometer Bricklet (https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Barometer.html)
implemented using Python AsyncIO. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from .devices import (
    AdvancedCallbackConfiguration,
    BasicCallbackConfiguration,
    Channel,
    ChannelConfiguration,
    Device,
    DeviceIdentifier,
)
from .devices import ThresholdOption as Threshold
from .devices import _FunctionID
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import pack_payload, unpack_payload
from .quantities import TEMPERATURE, Quantity

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    AIR_PRESSURE = 15
    ALTITUDE = 16
    AIR_PRESSURE_REACHED = 17
    ALTITUDE_REACHED = 18


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_AIR_PRESSURE = 1
    GET_ALTITUDE = 2
    SET_AIR_PRESSURE_CALLBACK_PERIOD = 3
    GET_AIR_PRESSURE_CALLBACK_PERIOD = 4
    SET_ALTITUDE_CALLBACK_PERIOD = 5
    GET_ALTITUDE_CALLBACK_PERIOD = 6
    SET_AIR_PRESSURE_CALLBACK_THRESHOLD = 7
    GET_AIR_PRESSURE_CALLBACK_THRESHOLD = 8
    SET_ALTITUDE_CALLBACK_THRESHOLD = 9
    GET_ALTITUDE_CALLBACK_THRESHOLD = 10
    SET_DEBOUNCE_PERIOD = 11
    GET_DEBOUNCE_PERIOD = 12
    SET_REFERENCE_AIR_PRESSURE = 13
    GET_CHIP_TEMPERATURE = 14
    GET_REFERENCE_AIR_PRESSURE = 19
    SET_AVERAGING = 20
    GET_AVERAGING = 21
    SET_I2C_MODE = 22
    GET_I2C_MODE = 23


@unique
class I2CMode(Enum):
    """
    The speed of the I2C bus between the Bricklet and its sensor
    """

    FAST = 0  # 400 kHz
    SLOW = 1  # 100 kHz


class GetAveraging(NamedTuple):
    moving_average_pressure: int
    average_pressure: int
    average_temperature: int


ALTITUDE = Quantity(100)  # raw: cm
AIR_PRESSURE = Quantity(10)  # raw: 1/10 Pa


class BrickletBarometer(Device):  # pylint: disable=too-many-public-methods
    """
    Measures air pressure and altitude changes
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_BAROMETER
    DEVICE_DISPLAY_NAME = "Barometer Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    I2CMode: TypeAlias = I2CMode

    CALLBACK_FORMATS = {
        CallbackID.AIR_PRESSURE: "i",
        CallbackID.ALTITUDE: "i",
        CallbackID.AIR_PRESSURE_REACHED: "i",
        CallbackID.ALTITUDE_REACHED: "i",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_air_pressure",
            callbacks=(CallbackID.AIR_PRESSURE, CallbackID.AIR_PRESSURE_REACHED),
            configuration=ChannelConfiguration("air_pressure", split=True),
        ),
        Channel(
            1,
            getter="get_altitude",
            callbacks=(CallbackID.ALTITUDE, CallbackID.ALTITUDE_REACHED),
            configuration=ChannelConfiguration("altitude", split=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> Decimal:
        return await self._get_value(sid)

    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ):
        await self._set_callback_configuration(
            sid, period, value_has_to_change, option, minimum, maximum, response_expected
        )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        return await self._get_callback_configuration(sid)

    async def get_air_pressure(self) -> Decimal:
        """
        Returns the air pressure of the air pressure sensor in Pa.

        If you want to get the air pressure periodically, it is recommended to use the :cb:`Air Pressure` callback and
        set the period with :func:`Set Air Pressure Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AIR_PRESSURE, response_expected=True
        )
        return AIR_PRESSURE.to_si(unpack_payload(payload, "i"))

    async def get_altitude(self) -> Decimal:
        """
        Returns the relative altitude of the air pressure sensor in m. The value is calculated based on the difference
        between the current air pressure and the reference air pressure that can be set with
        :func:`Set Reference Air Pressure`.

        If you want to get the altitude periodically, it is recommended to use the :cb:`Altitude` callback and set the
        period with :func:`Set Altitude Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALTITUDE, response_expected=True
        )
        return ALTITUDE.to_si(unpack_payload(payload, "i"))

    async def set_air_pressure_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :cb:`Air Pressure` callback is triggered periodically. A value of 0 turns the
        callback off.

        The :cb:`Air Pressure` callback is only triggered if the air pressure has
        changed since the last triggering.
        """
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AIR_PRESSURE_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_air_pressure_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set Air Pressure Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AIR_PRESSURE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_altitude_callback_period(self, period: Duration = 0, response_expected: bool = True) -> None:
        """
        Sets the period with which the :cb:`Altitude` callback is triggered periodically. A value of 0 turns the
        callback off.

        The :cb:`Altitude` callback is only triggered if the altitude has changed since
        the last triggering.
        """
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALTITUDE_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_altitude_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set Altitude Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALTITUDE_CALLBACK_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_air_pressure_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Air Pressure Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the air pressure is *outside* the min and max values"
         "'i'",    "Callback is triggered when the air pressure is *inside* the min and max values"
         "'<'",    "Callback is triggered when the air pressure is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the air pressure is greater than the min value (max is ignored)"
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AIR_PRESSURE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value.encode("ascii"),
                    AIR_PRESSURE.from_si(minimum),
                    AIR_PRESSURE.from_si(maximum),
                ),
                "c i i",
            ),
            response_expected=response_expected,
        )

    async def get_air_pressure_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Air Pressure Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AIR_PRESSURE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        option = Threshold(option)
        minimum, maximum = AIR_PRESSURE.to_si(minimum), AIR_PRESSURE.to_si(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_altitude_callback_threshold(
        self,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected=True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Altitude Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the altitude is *outside* the min and max values"
         "'i'",    "Callback is triggered when the altitude is *inside* the min and max values"
         "'<'",    "Callback is triggered when the altitude is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the altitude is greater than the min value (max is ignored)"
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALTITUDE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value.encode("ascii"),
                    ALTITUDE.from_si(minimum),
                    ALTITUDE.from_si(maximum),
                ),
                "c i i",
            ),
            response_expected=response_expected,
        )

    async def get_altitude_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Altitude Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALTITUDE_CALLBACK_THRESHOLD, response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, "c i i")
        option = Threshold(option)
        minimum, maximum = ALTITUDE.to_si(minimum), ALTITUDE.to_si(maximum)
        return BasicCallbackConfiguration(option, minimum, maximum)

    async def set_debounce_period(
        self, debounce_period: Duration = Decimal("0.1"), response_expected: bool = True
    ) -> None:
        """
        Sets the period with which the threshold callbacks

        * :cb:`Air Pressure Reached`,
        * :cb:`Altitude Reached`

        are triggered, if the thresholds

        * :func:`Set Air Pressure Callback Threshold`,
        * :func:`Set Altitude Callback Threshold`

        keep being reached.
        """
        if debounce_period < 0:
            raise ValueError(
                f"Invalid argument: expected debounce_period >= 0, got debounce_period={debounce_period!r}"
            )

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((seconds_to_ms(debounce_period),), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> Decimal:
        """
        Returns the debounce-period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )
        return ms_to_seconds(unpack_payload(payload, "I"))

    async def get_chip_temperature(self) -> Decimal:
        """
        Returns the temperature of the air pressure sensor in K.

        This temperature is used internally for temperature compensation of the air pressure measurement. It is not as
        accurate as the temperature measured by the :ref:`temperature_bricklet` or the :ref:`temperature_ir_bricklet`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIP_TEMPERATURE, response_expected=True
        )
        return TEMPERATURE.to_si(unpack_payload(payload, "h"))

    async def set_reference_air_pressure(
        self, air_pressure: float | Decimal = 101325, response_expected: bool = True
    ) -> None:
        """
        Sets the reference air pressure for the altitude calculation. Setting the reference to the current air pressure
        results in a calculated altitude of 0 m. Passing 0 is a shortcut for passing the current air pressure as
        reference.

        Well known reference values are the Q codes
        `QNH <https://en.wikipedia.org/wiki/QNH>`__ and
        `QFE <https://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__
        used in aviation.
        """
        if not ((air_pressure == 0) or (1000 <= air_pressure <= 120000)):
            raise ValueError(
                "Invalid argument: expected (air_pressure == 0) or (1000 <= air_pressure <= 120000), "
                f"got air_pressure={air_pressure!r}"
            )

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_REFERENCE_AIR_PRESSURE,
            data=pack_payload((AIR_PRESSURE.from_si(air_pressure),), "i"),
            response_expected=response_expected,
        )

    async def get_reference_air_pressure(self) -> Decimal:
        """
        Returns the reference air pressure as set by :func:`Set Reference Air Pressure`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_REFERENCE_AIR_PRESSURE, response_expected=True
        )
        return AIR_PRESSURE.to_si(unpack_payload(payload, "i"))

    async def set_averaging(
        self,
        moving_average_pressure: int = 25,
        average_pressure: int = 10,
        average_temperature: int = 10,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the different averaging parameters. It is possible to set the length of a normal averaging for the
        temperature and pressure, as well as an additional length of a
        `moving average <https://en.wikipedia.org/wiki/Moving_average>`__ for the pressure. The moving average is
        calculated from the normal averages.  There is no moving average for the temperature.

        Setting the all three parameters to 0 will turn the averaging completely off. If the averaging is off, there is
        lots of noise on the data, but the data is returned without delay. Thus, we recommend to turn the averaging off
        if the Barometer Bricklet data is to be used for sensor fusion with other sensors.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        if not 0 <= moving_average_pressure <= 25:
            raise ValueError(
                "Invalid argument: expected 0 <= moving_average_pressure <= 25, "
                f"got moving_average_pressure={moving_average_pressure!r}"
            )
        if not 0 <= average_pressure <= 10:
            raise ValueError(
                f"Invalid argument: expected 0 <= average_pressure <= 10, got average_pressure={average_pressure!r}"
            )
        if not 0 <= average_temperature <= 255:
            raise ValueError(
                "Invalid argument: expected 0 <= average_temperature <= 255, "
                f"got average_temperature={average_temperature!r}"
            )

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AVERAGING,
            data=pack_payload(
                (
                    int(moving_average_pressure),
                    int(average_pressure),
                    int(average_temperature),
                ),
                "B B B",
            ),
            response_expected=response_expected,
        )

    async def get_averaging(self) -> GetAveraging:
        """
        Returns the averaging configuration as set by :func:`Set Averaging`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AVERAGING, response_expected=True
        )
        return GetAveraging(*unpack_payload(payload, "B B B"))

    async def set_i2c_mode(self, mode: I2CMode | int = I2CMode.FAST, response_expected: bool = True) -> None:
        """
        Sets the I2C mode. Possible modes are:

        * 0: Fast (400kHz)
        * 1: Slow (100kHz)

        If you have problems with obvious outliers in the
        Barometer Bricklet measurements, they may be caused by EMI issues.
        In this case it may be helpful to lower the I2C speed.

        It is however not recommended to lower the I2C speed in applications where
        a high throughput needs to be achieved.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        if not isinstance(mode, I2CMode):
            mode = I2CMode(mode)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_I2C_MODE,
            data=pack_payload((mode.value,), "B"),
            response_expected=response_expected,
        )

    async def get_i2c_mode(self) -> I2CMode:
        """
        Returns the I2C mode as set by :func:`Set I2C Mode`.

        .. versionadded:: 2.0.3$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_I2C_MODE, response_expected=True
        )
        return I2CMode(unpack_payload(payload, "B"))

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id in (CallbackID.AIR_PRESSURE, CallbackID.AIR_PRESSURE_REACHED):
            return 0, AIR_PRESSURE.to_si(value)
        return 1, ALTITUDE.to_si(value)
