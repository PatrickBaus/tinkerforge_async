"""
Module for the Tinkerforge Barometer Bricklet 2.0
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Barometer_V2.html) implemented using Python asyncio. It does the
low-level communication with the Tinkerforge ip connection and also handles conversion of raw units to SI units.
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

    AIR_PRESSURE = 4
    ALTITUDE = 8
    TEMPERATURE = 12


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_AIR_PRESSURE = 1
    SET_AIR_PRESSURE_CALLBACK_CONFIGURATION = 2
    GET_AIR_PRESSURE_CALLBACK_CONFIGURATION = 3
    GET_ALTITUDE = 5
    SET_ALTITUDE_CALLBACK_CONFIGURATION = 6
    GET_ALTITUDE_CALLBACK_CONFIGURATION = 7
    GET_TEMPERATURE = 9
    SET_TEMPERATURE_CALLBACK_CONFIGURATION = 10
    GET_TEMPERATURE_CALLBACK_CONFIGURATION = 11
    SET_MOVING_AVERAGE_CONFIGURATION = 13
    GET_MOVING_AVERAGE_CONFIGURATION = 14
    SET_REFERENCE_AIR_PRESSURE = 15
    GET_REFERENCE_AIR_PRESSURE = 16
    SET_CALIBRATION = 17
    GET_CALIBRATION = 18
    SET_SENSOR_CONFIGURATION = 19
    GET_SENSOR_CONFIGURATION = 20


@unique
class DataRate(Enum):
    """
    Supported data rates of the air pressure sensor
    """

    OFF = 0
    RATE_1HZ = 1
    RATE_10HZ = 2
    RATE_25HZ = 3
    RATE_50HZ = 4
    RATE_75HZ = 5


_DataRate = DataRate  # We need the alias for MyPy type hinting


@unique
class LowPassFilter(Enum):
    """
    Low pass filter options of the pressure sensor
    """

    FILTER_OFF = 0
    FILTER_9TH = 1
    FILTER_20TH = 2


_LowPassFilter = LowPassFilter  # We need the alias for MyPy type hinting


class GetMovingAverageConfiguration(NamedTuple):
    moving_average_length_air_pressure: int
    moving_average_length_temperature: int


class GetCalibration(NamedTuple):
    measured_air_pressure: Decimal
    actual_air_pressure: Decimal


class GetSensorConfiguration(NamedTuple):
    data_rate: DataRate
    air_pressure_low_pass_filter: LowPassFilter


class BrickletBarometerV2(BrickletWithMCU):  # pylint: disable=too-many-public-methods
    """
    Measures air pressure and altitude changes
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_BAROMETER_V2
    DEVICE_DISPLAY_NAME = "Barometer Bricklet 2.0"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    DataRate = DataRate
    LowPassFilter = LowPassFilter

    CALLBACK_FORMATS = {
        CallbackID.AIR_PRESSURE: "i",
        CallbackID.ALTITUDE: "i",
        CallbackID.TEMPERATURE: "i",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.AIR_PRESSURE,),
        1: (CallbackID.ALTITUDE,),
        2: (CallbackID.TEMPERATURE,),
    }

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to the IP connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_value(self, sid: int) -> Decimal:
        assert sid in (0, 1, 2)

        if sid == 0:
            return await self.get_air_pressure()
        if sid == 1:
            return await self.get_altitude()
        return await self.get_temperature()

    async def set_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        sid: int,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal | None = None,
        maximum: float | Decimal | None = None,
        response_expected: bool = True,
    ):
        minimum = 0 if minimum is None else minimum
        maximum = 0 if maximum is None else maximum

        assert sid in (0, 1, 2)

        if sid == 0:
            await self.set_air_pressure_callback_configuration(
                period, value_has_to_change, option, minimum, maximum, response_expected
            )
        elif sid == 1:
            await self.set_altitude_callback_configuration(
                period, value_has_to_change, option, minimum, maximum, response_expected
            )
        else:
            await self.set_temperature_callback_configuration(
                period, value_has_to_change, option, minimum, maximum, response_expected
            )

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        assert sid in (0, 1, 2)

        if sid == 0:
            return await self.get_air_pressure_callback_configuration()
        if sid == 1:
            return await self.get_altitude_callback_configuration()
        return await self.get_temperature_callback_configuration()

    async def get_air_pressure(self) -> Decimal:
        """
        Returns the measured air pressure.


        If you want to get the value periodically, it is recommended to use the :cb:`Air Pressure` callback. You can set
        the callback configuration with :func:`Set Air Pressure Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AIR_PRESSURE, response_expected=True
        )
        return self.__air_pressure_sensor_to_si(unpack_payload(payload, "i"))

    async def set_air_pressure_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :cb:`Air Pressure` callback is triggered periodically. A value of 0
        turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only triggered after the value has
        changed. If the value didn't change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period, independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Air Pressure` callback.

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
        option = Threshold(option)
        assert period >= 0
        assert minimum >= 0
        assert maximum >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AIR_PRESSURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    self.__si_to_air_pressure_sensor(minimum),
                    self.__si_to_air_pressure_sensor(maximum),
                ),
                "I ! c i i",
            ),
            response_expected=response_expected,
        )

    async def get_air_pressure_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Air Pressure Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_AIR_PRESSURE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        option = Threshold(option)
        minimum, maximum = self.__air_pressure_sensor_to_si(minimum), self.__air_pressure_sensor_to_si(maximum)
        return AdvancedCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def get_altitude(self) -> Decimal:
        """
        Returns the relative altitude of the air pressure sensor. The value is calculated based on the difference
        between the current air pressure and the reference air pressure that can be set with
        :func:`Set Reference Air Pressure`.


        If you want to get the value periodically, it is recommended to use the :cb:`Altitude` callback. You can set the
        callback configuration with :func:`Set Altitude Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALTITUDE, response_expected=True
        )
        return self.__altitude_sensor_to_si(unpack_payload(payload, "i"))

    async def set_altitude_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :cb:`Altitude` callback is triggered periodically. A value of 0 turns
        the callback off.

        If the `value has to change`-parameter is set to true, the callback is only triggered after the value has
        changed. If the value didn't change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period, independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Altitude` callback.

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
        option = Threshold(option)
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALTITUDE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    self.__si_to_altitude_sensor(minimum),
                    self.__si_to_altitude_sensor(maximum),
                ),
                "I ! c i i",
            ),
            response_expected=response_expected,
        )

    async def get_altitude_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Altitude Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALTITUDE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        option = Threshold(option)
        minimum, maximum = self.__altitude_sensor_to_si(minimum), self.__altitude_sensor_to_si(maximum)
        return AdvancedCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def get_temperature(self) -> Decimal:
        """
        Returns the temperature of the air pressure sensor.

        This temperature is used internally for temperature compensation of the air pressure measurement. It is not as
        accurate as the temperature measured by the :ref:`temperature_v2_bricklet` or the
        :ref:`temperature_ir_v2_bricklet`.


        If you want to get the value periodically, it is recommended to use the :cb:`Temperature` callback. You can set
        the callback configuration with :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TEMPERATURE, response_expected=True
        )
        return self.__temperature_sensor_to_si(unpack_payload(payload, "i"))

    async def set_temperature_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        period: int = 0,
        value_has_to_change: bool = False,
        option: Threshold | int = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :cb:`Temperature` callback is triggered periodically. A value of 0 turns
        the callback off.

        If the `value has to change`-parameter is set to true, the callback is only triggered after the value has
        changed. If the value didn't change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period, independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Temperature` callback.

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
        option = Threshold(option)
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(period),
                    bool(value_has_to_change),
                    option.value.encode("ascii"),
                    self.__si_to_temperature_sensor(minimum),
                    self.__si_to_temperature_sensor(maximum),
                ),
                "I ! c i i",
            ),
            response_expected=response_expected,
        )

    async def get_temperature_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ALTITUDE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c i i")
        option = Threshold(option)
        minimum, maximum = self.__temperature_sensor_to_si(minimum), self.__temperature_sensor_to_si(maximum)
        return AdvancedCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def set_moving_average_configuration(
        self,
        moving_average_length_air_pressure: int = 100,
        moving_average_length_temperature: int = 100,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the air pressure and temperature measurements.

        Setting the length to 1 will turn the averaging off. With less averaging, there is more noise on the data.

        If you want to do long term measurements the longest moving average will give the cleanest results.
        """
        assert moving_average_length_air_pressure >= 1
        assert moving_average_length_temperature >= 1

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_MOVING_AVERAGE_CONFIGURATION,
            data=pack_payload(
                (
                    int(moving_average_length_air_pressure),
                    int(moving_average_length_temperature),
                ),
                "H H",
            ),
            response_expected=response_expected,
        )

    async def get_moving_average_configuration(self) -> GetMovingAverageConfiguration:
        """
        Returns the moving average configuration as set by :func:`Set Moving Average Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_MOVING_AVERAGE_CONFIGURATION, response_expected=True
        )

        return GetMovingAverageConfiguration(*unpack_payload(payload, "H H"))

    async def set_reference_air_pressure(
        self, air_pressure: float | Decimal = Decimal("1013.250"), response_expected: bool = True
    ) -> None:
        """
        Sets the reference air pressure for the altitude calculation. Setting the reference to the current air pressure
        results in a calculated altitude of 0mm. Passing 0 is a shortcut for passing the current air pressure as
        reference.

        Well known reference values are the Q codes `QNH <https://en.wikipedia.org/wiki/QNH>`__ and
        `QFE <https://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__ used in aviation.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_REFERENCE_AIR_PRESSURE,
            data=pack_payload((self.__si_to_air_pressure_sensor(air_pressure),), "i"),
            response_expected=response_expected,
        )

    async def get_reference_air_pressure(self) -> Decimal:
        """
        Returns the reference air pressure as set by :func:`Set Reference Air Pressure`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_REFERENCE_AIR_PRESSURE, response_expected=True
        )

        return self.__air_pressure_sensor_to_si(unpack_payload(payload, "i"))

    async def set_calibration(
        self,
        measured_air_pressure: float | Decimal,
        actual_air_pressure: float | Decimal,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the one point calibration (OPC) values for the air pressure measurement.

        Before the Bricklet can be calibrated any previous calibration has to be removed by setting
        ``measured air pressure`` and ``actual air pressure`` to 0.

        Then the current air pressure has to be measured using the Bricklet (``measured air pressure``) and with an
        accurate reference barometer (``actual air pressure``) at the same time and passed to this function.

        After proper calibration the air pressure measurement can achieve an accuracy up to 0.2 hPa.

        The calibration is saved in the EEPROM of the Bricklet and only needs to be configured once.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CALIBRATION,
            data=pack_payload(
                (
                    self.__si_to_air_pressure_sensor(measured_air_pressure),
                    self.__si_to_air_pressure_sensor(actual_air_pressure),
                ),
                "i i",
            ),
            response_expected=response_expected,
        )

    async def get_calibration(self) -> GetCalibration:
        """
        Returns the air pressure one point calibration values as set by :func:`Set Calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CALIBRATION, response_expected=True
        )
        measured_air_pressure, actual_air_pressure = unpack_payload(payload, "i i")
        measured_air_pressure, actual_air_pressure = self.__air_pressure_sensor_to_si(
            measured_air_pressure
        ), self.__air_pressure_sensor_to_si(actual_air_pressure)

        return GetCalibration(measured_air_pressure, actual_air_pressure)

    async def set_sensor_configuration(
        self,
        data_rate: _DataRate | int = DataRate.RATE_50HZ,
        air_pressure_low_pass_filter: _LowPassFilter | int = LowPassFilter.FILTER_9TH,
        response_expected: bool = True,
    ):
        """
        Configures the data rate and air pressure low pass filter. The low pass filter cut-off frequency (if enabled)
        can be set to 1/9th or 1/20th of the configured data rate to decrease the noise on the air pressure data.

        The low pass filter configuration only applies to the air pressure measurement. There is no low pass filter for
        the temperature measurement.

        A higher data rate will result in a less precise temperature because of self-heating of the sensor. If the
        accuracy of the temperature reading is important to you, we would recommend the 1Hz data rate.
        """
        if not isinstance(data_rate, DataRate):
            data_rate = DataRate(data_rate)
        if not isinstance(air_pressure_low_pass_filter, LowPassFilter):
            air_pressure_low_pass_filter = LowPassFilter(air_pressure_low_pass_filter)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSOR_CONFIGURATION,
            data=pack_payload(
                (
                    data_rate.value,
                    air_pressure_low_pass_filter.value,
                ),
                "B B",
            ),
            response_expected=response_expected,
        )

    async def get_sensor_configuration(self) -> GetSensorConfiguration:
        """
        Returns the sensor configuration as set by :func:`Set Sensor Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SENSOR_CONFIGURATION, response_expected=True
        )
        data_rate, air_pressure_low_pass_filter = unpack_payload(payload, "B B")
        data_rate, air_pressure_low_pass_filter = DataRate(data_rate), LowPassFilter(air_pressure_low_pass_filter)

        return GetSensorConfiguration(data_rate, air_pressure_low_pass_filter)

    @staticmethod
    def __air_pressure_sensor_to_si(value: int) -> Decimal:
        """
        Convert the sensor value to SI units
        """
        return Decimal(value) / 10

    @staticmethod
    def __si_to_air_pressure_sensor(value: float | Decimal) -> int:
        """
        Convert SI units to raw values
        """
        return int(value * 10)

    @staticmethod
    def __altitude_sensor_to_si(value: int) -> Decimal:
        """
        Convert the sensor value to SI units
        """
        return Decimal(value) / 1000

    @staticmethod
    def __si_to_altitude_sensor(value: float | Decimal) -> int:
        """
        Convert SI units to raw values
        """
        return int(value * 1000)

    @staticmethod
    def __temperature_sensor_to_si(value: int) -> Decimal:
        """
        Convert the sensor value to SI units
        """
        return Decimal(value) / 100

    @staticmethod
    def __si_to_temperature_sensor(value: float | Decimal) -> int:
        """
        Convert SI units to raw values
        """
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
                if function_id is CallbackID.AIR_PRESSURE:
                    yield Event(self, 0, function_id, self.__air_pressure_sensor_to_si(value))
                elif function_id is CallbackID.ALTITUDE:
                    yield Event(self, 1, function_id, self.__altitude_sensor_to_si(value))
                else:
                    yield Event(self, 2, function_id, self.__temperature_sensor_to_si(value))
