# -*- coding: utf-8 -*-
"""
Module for the Tinkerforge PTC Bricklet
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/PTC.html)
implemented using Python AsyncIO. It does the low-lvel communication with the
Tinkerforge ip connection and also handles conversion of raw units to SI units.
"""
import asyncio
from collections import namedtuple
from decimal import Decimal
from enum import Enum, unique

from .devices import DeviceIdentifier, Device, ThresholdOption, GetCallbackConfiguration
from .ip_connection_helper import pack_payload, unpack_payload

GetTemperatureCallbackThreshold = namedtuple('TemperatureCallbackThreshold', ['option', 'minimum', 'maximum'])
GetResistanceCallbackThreshold = namedtuple('ResistanceCallbackThreshold', ['option', 'minimum', 'maximum'])


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """
    TEMPERATURE = 13
    TEMPERATURE_REACHED = 14
    RESISTANCE = 15
    RESISTANCE_REACHED = 16
    SENSOR_CONNECTED = 24


@unique
class FunctionID(Enum):
    """
    The function calls available to this bricklet
    """
    GET_TEMPERATURE = 1
    GET_RESISTANCE = 2
    SET_TEMPERATURE_CALLBACK_PERIOD = 3
    GET_TEMPERATURE_CALLBACK_PERIOD = 4
    SET_RESISTANCE_CALLBACK_PERIOD = 5
    GET_RESISTANCE_CALLBACK_PERIOD = 6
    SET_TEMPERATURE_CALLBACK_THRESHOLD = 7
    GET_TEMPERATURE_CALLBACK_THRESHOLD = 8
    SET_RESISTANCE_CALLBACK_THRESHOLD = 9
    GET_RESISTANCE_CALLBACK_THRESHOLD = 10
    SET_DEBOUNCE_PERIOD = 11
    GET_DEBOUNCE_PERIOD = 12
    SET_NOISE_REJECTION_FILTER = 17
    GET_NOISE_REJECTION_FILTER = 18
    IS_SENSOR_CONNECTED = 19
    SET_WIRE_MODE = 20
    GET_WIRE_MODE = 21
    SET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION = 22
    GET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION = 23


@unique
class LineFilter(Enum):
    """
    Selects the notch filter to filter out the mains frequency hum
    """
    FREQUENCY_50HZ = 0
    FREQUENCY_60HZ = 1


@unique
class WireMode(Enum):
    """
    Select the measurement setup. Use 3 or wires to eliminate most/all of the
    resistance of the wire. Use 3 or 4 wire setups when using PT100 and long
    cables.
    """
    WIRE_2 = 2
    WIRE_3 = 3
    WIRE_4 = 4


@unique
class SensorType(Enum):
    """
    The type of sensor used
    """
    PT_100 = 0
    PT_1000 = 1


class BrickletPtc(Device):
    """
    Reads temperatures from Pt100 und Pt1000 sensors
    """
    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_PTC
    DEVICE_DISPLAY_NAME = 'PTC Bricklet'

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption
    LineFilter = LineFilter
    WireMode = WireMode
    SensorType = SensorType

    CALLBACK_FORMATS = {
        CallbackID.TEMPERATURE: 'i',
        CallbackID.TEMPERATURE_REACHED: 'i',
        CallbackID.RESISTANCE: 'i',
        CallbackID.RESISTANCE_REACHED: 'i',
        CallbackID.SENSOR_CONNECTED: '!',
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.TEMPERATURE, CallbackID.TEMPERATURE_REACHED),
        1: (CallbackID.RESISTANCE, CallbackID.RESISTANCE_REACHED),
        2: (CallbackID.SENSOR_CONNECTED, ),
    }

    @property
    def sensor_type(self):
        """
        Return the type of sensor. Either PT100 oder PT1000 as a SensorType
        enum.
        """
        return self.__sensor_type

    @sensor_type.setter
    def sensor_type(self, value):
        if not isinstance(value, SensorType):
            self.__sensor_type = SensorType(value)
        else:
            self.__sensor_type = value

    def __init__(self, uid, ipcon, sensor_type=SensorType.PT_100):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)
        self.sensor_type = sensor_type    # Use the setter to automatically convert to enum

    def __repr__(self):
        return f'{self.__class__.__module__}.{self.__class__.__qualname__}(uid={self.uid}, ipcon={self.ipcon!r}, sensor_type={self.sensor_type})'

    async def get_value(self, sid):
        assert sid in (0, 1, 2)

        if sid == 0:
            return await self.get_temperature()
        elif sid == 1:
            return await self.get_resistance()
        else:
            return await self.is_sensor_connected()

    async def set_callback_configuration(self, sid, period=0, value_has_to_change=False, option=ThresholdOption.OFF, minimum=None, maximum=None, response_expected=True):  # pylint: disable=too-many-arguments
        assert sid in (0, 1, 2)

        if sid == 0:
            minimum = Decimal('273.15') if minimum is None else minimum
            maximum = Decimal('273.15') if maximum is None else maximum
            await asyncio.gather(
                self.set_temperature_callback_period(period, response_expected),
                self.set_temperature_callback_threshold(option, minimum, maximum, response_expected)
            )
        elif sid == 1:
            minimum = 0 if minimum is None else minimum
            maximum = 0 if maximum is None else maximum
            await asyncio.gather(
                self.set_resistance_callback_period(period, response_expected),
                self.set_resistance_callback_threshold(option, minimum, maximum, response_expected)
            )
        else:
            raise AttributeError("Configuration of the 'connected callback' is not supported.")

    async def get_callback_configuration(self, sid):
        assert sid in (0, 1, 2)

        if sid == 0:
            period, config = await asyncio.gather(
                self.get_temperature_callback_period(),
                self.get_temperature_callback_threshold()
            )
        elif sid == 1:
            period, config = await asyncio.gather(
                self.get_resistance_callback_period(),
                self.get_resistance_callback_threshold()
            )
        else:
            raise AttributeError("Configuration of the 'connected callback' is not supported.")

        return GetCallbackConfiguration(period, True, *config)

    async def get_temperature(self):
        """
        Returns the temperature of the sensor. The value
        has a range of -246 to 849 °C and is given in °C/100,
        e.g. a value of 4223 means that a temperature of 42.23 °C is measured.

        If you want to get the temperature periodically, it is recommended
        to use the :cb:`Temperature` callback and set the period with
        :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_TEMPERATURE,
            response_expected=True
        )
        return self.__value_to_si_temperature(unpack_payload(payload, 'i'))

    async def get_resistance(self):
        """
        Returns the value as measured by the MAX31865 precision delta-sigma ADC.

        The value can be converted with the following formulas:

        * Pt100:  resistance = (value * 390) / 32768
        * Pt1000: resistance = (value * 3900) / 32768

        If you want to get the resistance periodically, it is recommended
        to use the :cb:`Resistance` callback and set the period with
        :func:`Set Resistance Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RESISTANCE,
            response_expected=True
        )
        return self.__value_to_si_resistance(unpack_payload(payload, 'i'))

    async def set_temperature_callback_period(self, period=0, response_expected=True):
        """
        Sets the period in ms with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Temperature` callback is only triggered if the temperature has changed
        since the last triggering.

        The default value is 0.
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), 'I'),
            response_expected=response_expected,
        )

    async def get_temperature_callback_period(self):
        """
        Returns the period as set by :func:`Set Temperature Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_TEMPERATURE_CALLBACK_PERIOD,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_resistance_callback_period(self, period=0, response_expected=True):
        """
        Sets the period with which the :cb:`Resistance` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Resistance` callback is only triggered if the resistance has changed
        since the last triggering.
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RESISTANCE_CALLBACK_PERIOD,
            data=pack_payload((int(period),), 'I'),
            response_expected=response_expected,
        )

    async def get_resistance_callback_period(self):
        """
        Returns the period as set by :func:`Set Resistance Callback Period`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RESISTANCE_CALLBACK_PERIOD,
            response_expected=True
        )
        return unpack_payload(payload, 'I')

    async def set_temperature_callback_threshold(self, option=ThresholdOption.OFF, minimum=Decimal('273.15'), maximum=Decimal('273.15'), response_expected=True):
        """
        Sets the thresholds for the :cb:`Temperature Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        if not isinstance(option, ThresholdOption):
            option = ThresholdOption(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TEMPERATURE_CALLBACK_THRESHOLD,
            data=pack_payload(
              (
                option.value.encode('ascii'),
                self.__si_temperature_to_value(minimum),
                self.__si_temperature_to_value(maximum)
              ), 'c i i'),
            response_expected=response_expected
        )

    async def get_temperature_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_TEMPERATURE_CALLBACK_THRESHOLD,
            response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, 'c i i')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_si_temperature(minimum), self.__value_to_si_temperature(maximum)
        return GetTemperatureCallbackThreshold(option, minimum, maximum)

    async def set_resistance_callback_threshold(self, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
        """
        Sets the thresholds for the :cb:`Temperature Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the temperature is *outside* the min and max values"
         "'i'",    "Callback is triggered when the temperature is *inside* the min and max values"
         "'<'",    "Callback is triggered when the temperature is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the temperature is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).
        """
        if not isinstance(option, ThresholdOption):
            option = ThresholdOption(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RESISTANCE_CALLBACK_THRESHOLD,
            data=pack_payload(
              (
                option.value.encode('ascii'),
                self.__si_resistance_to_value(minimum),
                self.__si_resistance_to_value(maximum)
              ), 'c i i'),
            response_expected=response_expected
        )

    async def get_resistance_callback_threshold(self):
        """
        Returns the threshold as set by :func:`Set Temperature Callback Threshold`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_RESISTANCE_CALLBACK_THRESHOLD,
            response_expected=True
        )
        option, minimum, maximum = unpack_payload(payload, 'c i i')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_si_resistance(minimum), self.__value_to_si_resistance(maximum)
        return GetResistanceCallbackThreshold(option, minimum, maximum)

    async def set_debounce_period(self, debounce_period=100, response_expected=True):
        """
        Sets the period in ms with which the threshold callback

        * :cb:`Temperature Reached`

        is triggered, if the threshold

        * :func:`Set Temperature Callback Threshold`

        keeps being reached.

        The default value is 100.
        """
        assert debounce_period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((int(debounce_period),), 'I'),
            response_expected=response_expected
        )

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

    async def set_noise_rejection_filter(self, line_filter=LineFilter.FREQUENCY_50HZ, response_expected=True):
        """
        Sets the noise rejection filter to either 50Hz (0) or 60Hz (1).
        Noise from 50Hz or 60Hz power sources (including
        harmonics of the AC power's fundamental frequency) is
        attenuated by 82dB.

        Default value is 0 = 50Hz.
        """
        if not isinstance(line_filter, LineFilter):
            line_filter = LineFilter(line_filter)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_NOISE_REJECTION_FILTER,
            data=pack_payload((line_filter.value,), 'B'),
            response_expected=response_expected
        )

    async def get_noise_rejection_filter(self):
        """
        Returns the noise rejection filter option as set by
        :func:`Set Noise Rejection Filter`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_NOISE_REJECTION_FILTER,
            response_expected=True
        )
        return LineFilter(unpack_payload(payload, 'B'))

    async def is_sensor_connected(self):
        """
        Returns *true* if the sensor is connected correctly.

        If this function
        returns *false*, there is either no Pt100 or Pt1000 sensor connected,
        the sensor is connected incorrectly or the sensor itself is faulty.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.IS_SENSOR_CONNECTED,
            response_expected=True
        )
        return unpack_payload(payload, '!')

    async def set_wire_mode(self, mode=WireMode.WIRE_2, response_expected=True):
        """
        Sets the wire mode of the sensor. Possible values are 2, 3 and 4 which
        correspond to 2-, 3- and 4-wire sensors. The value has to match the jumper
        configuration on the Bricklet.

        The default value is 2 = 2-wire.
        """
        if not isinstance(mode, WireMode):
            mode = WireMode(mode)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_WIRE_MODE,
            data=pack_payload((mode.value,), 'B'),
            response_expected=response_expected
        )

    async def get_wire_mode(self):
        """
        Returns the wire mode as set by :func:`Set Wire Mode`
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_WIRE_MODE,
            response_expected=True
        )
        return WireMode(unpack_payload(payload, 'B'))

    async def set_sensor_connected_callback_configuration(self, enabled, response_expected=True):
        """
        If you enable this callback, the :cb:`Sensor Connected` callback is triggered
        every time a Pt sensor is connected/disconnected.

        By default this callback is disabled.

        .. versionadded:: 2.0.2$nbsp;(Plugin)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION,
            data=pack_payload((bool(enabled),), '!'),
            response_expected=response_expected
        )

    async def get_sensor_connected_callback_configuration(self):
        """
        Returns the configuration as set by :func:`Set Sensor Connected Callback Configuration`.
set_sensor_connected_callback_configuration
        .. versionadded:: 2.0.2$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SENSOR_CONNECTED_CALLBACK_CONFIGURATION,
            response_expected=True
        )
        return unpack_payload(payload, '!')

    @staticmethod
    def __value_to_si_temperature(value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value + 27315) / 100

    @staticmethod
    def __si_temperature_to_value(value):
        return int(value * 100) - 27315

    def __value_to_si_resistance(self, value):
        """
        Convert to the sensor value to SI units
        """
        value = Decimal(value) * 390 / 32768
        if self.__sensor_type is SensorType.PT_1000:
            value *= 10
        return value

    def __si_resistance_to_value(self, value):
        if self.__sensor_type is SensorType.PT_1000:
            value /= 10
        return int(value * 32768 / 390)

    async def read_events(self, events=None, sids=None):
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

        async for header, payload in super().read_events():
            try:
                function_id = CallbackID(header['function_id'])
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                value = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                if function_id in (CallbackID.TEMPERATURE, CallbackID.TEMPERATURE_REACHED):
                    yield self.build_event(0, function_id, self.__value_to_si_temperature(value))
                elif function_id in (CallbackID.RESISTANCE, CallbackID.RESISTANCE_REACHED):
                    yield self.build_event(1, function_id, self.__value_to_si_resistance(value))
                else:
                    yield self.build_event(2, function_id, value)
