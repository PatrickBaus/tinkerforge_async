# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, unique

from .devices import DeviceIdentifier, Device, ThresholdOption
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetAirPressureCallbackThreshold = namedtuple('AirPressureCallbackThreshold', ['option', 'min', 'max'])
GetAltitudeCallbackThreshold = namedtuple('AltitudeCallbackThreshold', ['option', 'min', 'max'])
GetAveraging = namedtuple('Averaging', ['moving_average_pressure', 'average_pressure', 'average_temperature'])

@unique
class CallbackID(Enum):
    AIR_PRESSURE = 15
    ALTITUDE = 16
    AIR_PRESSURE_REACHED = 17
    ALTITUDE_REACHED = 18

@unique
class FunctionID(Enum):
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

class BrickletBarometer(Device):
    """
    Measures air pressure and altitude changes
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletBarometer
    DEVICE_DISPLAY_NAME = 'Barometer Bricklet'
    DEVICE_URL_PART = 'barometer' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption

    CALLBACK_FORMATS = {
        CallbackID.AIR_PRESSURE: 'i',
        CallbackID.ALTITUDE: 'i',
        CallbackID.AIR_PRESSURE_REACHED: 'i',
        CallbackID.ALTITUDE_REACHED: 'i',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_air_pressure(self):
        """
        Returns the air pressure of the air pressure sensor.

        If you want to get the air pressure periodically, it is recommended to use the
        :cb:`Air Pressure` callback and set the period with
        :func:`Set Air Pressure Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_AIR_PRESSURE,
            response_expected=True
        )
        return self.__value_to_SI_pressure(unpack_payload(payload, 'i'))

    async def get_altitude(self):
        """
        Returns the relative altitude of the air pressure sensor. The value is
        calculated based on the difference between the current air pressure
        and the reference air pressure that can be set with :func:`Set Reference Air Pressure`.

        If you want to get the altitude periodically, it is recommended to use the
        :cb:`Altitude` callback and set the period with
        :func:`Set Altitude Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ALTITUDE,
            response_expected=True
        )
        return self.__value_to_SI_altitude(unpack_payload(payload, 'i'))

    async def set_air_pressure_callback_period(self, period=0, response_expected=True):
        """
        Sets the period with which the :cb:`Air Pressure` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Air Pressure` callback is only triggered if the air pressure has
        changed since the last triggering.
        """
        assert type(period) is int and period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AIR_PRESSURE_CALLBACK_PERIOD,
            data=pack_payload((period,), 'I'),
            response_expected = response_expected,
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_air_pressure_callback_period(self):
        """
        Returns the period as set by :func:`Set Air Pressure Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_AIR_PRESSURE_CALLBACK_PERIOD,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_altitude_callback_period(self, period=0, response_expected=True):
        """
        Sets the period with which the :cb:`Altitude` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Altitude` callback is only triggered if the altitude has changed since
        the last triggering.
        """
        assert type(period) is int and period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALTITUDE_CALLBACK_PERIOD,
            data=pack_payload((period,), 'I'),
            response_expected = response_expected,
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_altitude_callback_period(self):
        """
        Returns the period as set by :func:`Set Altitude Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_GET_ALTITUDE_CALLBACK_PERIOD,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_air_pressure_callback_threshold(self, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
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
        assert type(option) is ThresholdOption
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_AIR_PRESSURE_CALLBACK_THRESHOLD,
            data=pack_payload((option.value.encode('ascii'), self.__SI_pressure_to_value(minimum), self.__SI_pressure_to_value(maximum)), 'c i i'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_air_pressure_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Air Pressure Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_AIR_PRESSURE_CALLBACK_THRESHOLD,
            response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, 'c i i')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_SI_pressure(minimum), self.__value_to_SI_pressure(maximum)
        return GetAirPressureCallbackThreshold(option, minimum, maximum)

    async def set_altitude_callback_threshold(self, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
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
        assert type(option) is ThresholdOption
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ALTITUDE_CALLBACK_THRESHOLD,
            data=pack_payload((option.value.encode('ascii'), self.__SI_altitude_to_value(minimum), self.__SI_altitude_to_value(maximum)), 'c i i'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_altitude_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Altitude Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ALTITUDE_CALLBACK_THRESHOLD,
            response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, 'c i i')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_SI_altitude(minimum), self.__value_to_SI_altitude(maximum)
        return GetAltitudeCallbackThreshold(option, minimum, maximum)

    async def set_debounce_period(self, debounce_period=100, response_expected=True):
        """
        Sets the period with which the threshold callbacks

        * :cb:`Air Pressure Reached`,
        * :cb:`Altitude Reached`

        are triggered, if the thresholds

        * :func:`Set Air Pressure Callback Threshold`,
        * :func:`Set Altitude Callback Threshold`

        keep being reached.
        """
        assert type(debounce_period) is int and debounce_period >= 0
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((debounce_period,), 'I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_DEBOUNCE_PERIOD,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def get_chip_temperature(self):
        """
        Returns the temperature of the air pressure sensor.

        This temperature is used internally for temperature compensation of the air
        pressure measurement. It is not as accurate as the temperature measured by the
        :ref:`temperature_bricklet` or the :ref:`temperature_ir_bricklet`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CHIP_TEMPERATURE,
            response_expected=True
        )
        return unpack_payload(payload, 'h')

    async def set_reference_air_pressure(self, air_pressure=101.3250, response_expected=False):
        """
        Sets the reference air pressure for the altitude calculation.
        Setting the reference to the current air pressure results in a calculated
        altitude of 0cm. Passing 0 is a shortcut for passing the current air pressure as
        reference.

        Well known reference values are the Q codes
        `QNH <https://en.wikipedia.org/wiki/QNH>`__ and
        `QFE <https://en.wikipedia.org/wiki/Mean_sea_level_pressure#Mean_sea_level_pressure>`__
        used in aviation.
        """
        assert air_pressure == 0 or (1 <= air_pressure <= 120)
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.FUNCTION_SET_REFERENCE_AIR_PRESSURE,
            data=pack_payload((self.__SI_pressure_to_value(air_pressure),), 'i'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_reference_air_pressure(self):
        """
        Returns the reference air pressure as set by :func:`Set Reference Air Pressure`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_REFERENCE_AIR_PRESSURE,
            response_expected=True
        )
        return self.__value_to_SI_pressure(unpack_payload(payload, 'i'))

    async def set_averaging(self, moving_average_pressure=25, average_pressure=10, average_temperature=10, response_expected=False):
        """
        Sets the different averaging parameters. It is possible to set
        the length of a normal averaging for the temperature and pressure,
        as well as an additional length of a
        `moving average <https://en.wikipedia.org/wiki/Moving_average>`__
        for the pressure. The moving average is calculated from the normal
        averages.  There is no moving average for the temperature.

        Setting the all three parameters to 0 will turn the averaging
        completely off. If the averaging is off, there is lots of noise
        on the data, but the data is without delay. Thus we recommend
        to turn the averaging off if the Barometer Bricklet data is
        to be used for sensor fusion with other sensors.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        assert type(moving_average_pressure) is int and 0 <= moving_average_pressure <= 25
        assert type(average_pressure) is int and 0 <= average_pressure <= 10
        assert type(average_temperature) is int and 0 <= moving_average_pressure <= 255
        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.FUNCTION_SET_AVERAGING,
            data=pack_payload((moving_average_pressure, average_pressure, average_temperature), 'B B B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_averaging(self):
        """
        Returns the averaging configuration as set by :func:`Set Averaging`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_AVERAGING,
            response_expected=True
        )
        return GetAveraging(unpack_payload(payload, 'B B B'))

    def __value_to_SI_altitude(self, value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 100

    def __SI_altitude_to_value(self, value):
        return int(value * 100)

    def __value_to_SI_pressure(self, value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 10000

    def __SI_pressure_to_value(self, value):
        return int(value * 10000)

    def _process_callback(self, header, payload):
        try:
            header['function_id'] = self.CallbackID(header['function_id'])
        except ValueError:
            # ValueError: raised if the callbackID is unknown
            raise UnknownFunctionError from None
        else:
            payload = self.__value_to_SI_pressure(
                unpack_payload(payload, self.CALLBACK_FORMATS[header['function_id']])
            )
            super()._process_callback(header, payload)

