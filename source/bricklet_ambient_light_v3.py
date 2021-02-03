# -*- coding: utf-8 -*-
from collections import namedtuple
from decimal import Decimal
from enum import Enum, unique

from .devices import DeviceIdentifier, BrickletWithMCU, ThresholdOption
from .ip_connection import Flags, UnknownFunctionError
from .ip_connection_helper import pack_payload, unpack_payload

GetIlluminanceCallbackConfiguration = namedtuple('IlluminanceCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'minimum', 'maximum'])
GetConfiguration = namedtuple('Configuration', ['illuminance_range', 'integration_time'])

@unique
class CallbackID(Enum):
    ILLUMINANCE = 4

@unique
class FunctionID(Enum):
    GET_ILLUMINANCE = 1
    SET_ILLUMINANCE_CALLBACK_CONFIGURATION = 2
    GET_ILLUMINANCE_CALLBACK_CONFIGURATION = 3
    SET_CONFIGURATION = 5
    GET_CONFIGURATION = 6

@unique
class IlluminanceRange(Enum):
    UNLIMITED = 6
    LUX64000 = 0
    LUX32000 = 1
    LUX16000 = 2
    LUX8000 = 3
    LUX1300 = 4
    LUX600 = 5

@unique
class IntegrationTime(Enum):
    T50MS = 0
    T100MS = 1
    T150MS = 2
    T200MS = 3
    T250MS = 4
    T300MS = 5
    T350MS = 6
    T400MS = 7


class BrickletAmbientLightV3(BrickletWithMCU):
    """
    Measures ambient temperature with 0.2 K accuracy
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BrickletAmbientLight_V3
    DEVICE_DISPLAY_NAME = 'Ambient Light Bricklet 3.0'
    DEVICE_URL_PART = 'ambient_light_v3' # internal

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID
    ThresholdOption = ThresholdOption
    IlluminanceRange = IlluminanceRange
    IntegrationTime = IntegrationTime

    CALLBACK_FORMATS = {
        CallbackID.ILLUMINANCE: 'I',
    }

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(uid, ipcon)

        self.api_version = (2, 0, 0)

    async def get_illuminance(self):
        """
        Returns the illuminance of the ambient light sensor. The measurement range goes
        up to about 100000lux, but above 64000lux the precision starts to drop.
        The illuminance is given in lux/100, i.e. a value of 450000 means that an
        illuminance of 4500lux is measured.

        An illuminance of 0lux indicates that the sensor is saturated and the
        configuration should be modified, see :func:`Set Configuration`.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Illuminance` callback. You can set the callback configuration
        with :func:`Set Illuminance Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ILLUMINANCE,
            response_expected=True
        )
        print(unpack_payload(payload, 'I'))
        return self.__value_to_SI(unpack_payload(payload, 'I'))

    async def set_illuminance_callback_configuration(self, period=0, value_has_to_change=False, option=ThresholdOption.OFF, minimum=0, maximum=0, response_expected=True):
        """
        The period is the period with which the :cb:`Illuminance` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

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
        if not type(option) is ThresholdOption:
            option = ThresholdOption(option)
        assert period >= 0
        assert minimum >= 0
        assert maximum >= 0

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_ILLUMINANCE_CALLBACK_CONFIGURATION,
            data=pack_payload(
              (
                int(period),
                bool(value_has_to_change),
                option.value.encode('ascii'),
                self.__SI_to_value(minimum),
                self.__SI_to_value(maximum)
              ), 'I ! c I I'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            # TODO raise errors
            return header['flags'] == Flags.OK

    async def get_illuminance_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ILLUMINANCE_CALLBACK_CONFIGURATION,
            response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, 'I ! c I I')
        option = ThresholdOption(option)
        minimum, maximum = self.__value_to_SI(minimum), self.__value_to_SI(maximum)
        return GetIlluminanceCallbackConfiguration(period, value_has_to_change, option, minimum, maximum)

    async def set_configuration(self, illuminance_range=IlluminanceRange.LUX8000, integration_time=IntegrationTime.T150MS, response_expected=True):
        """
        Sets the configuration. It is possible to configure an illuminance range
        between 0-600lux and 0-64000lux and an integration time between 50ms and 400ms.

        The unlimited illuminance range allows to measure up to about 100000lux, but
        above 64000lux the precision starts to drop.

        A smaller illuminance range increases the resolution of the data. A longer
        integration time will result in less noise on the data.

        If the actual measure illuminance is out-of-range then the current illuminance
        range maximum +0.01lux is reported by :func:`Get Illuminance` and the
        :cb:`Illuminance` callback. For example, 800001 for the 0-8000lux range.

        With a long integration time the sensor might be saturated before the measured
        value reaches the maximum of the selected illuminance range. In this case 0lux
        is reported by :func:`Get Illuminance` and the :cb:`Illuminance` callback.

        If the measurement is out-of-range or the sensor is saturated then you should
        configure the next higher illuminance range. If the highest range is already
        in use, then start to reduce the integration time.

        The default values are 0-8000lux illuminance range and 150ms integration time.
        """
        if not type(illuminance_range) is IlluminanceRange:
            illuminance_range = IlluminanceRange(illuminance_range)
        if not type(integration_time) is IntegrationTime:
            integration_time = IntegrationTime(integration_time)

        result = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_CONFIGURATION,
            data=pack_payload((illuminance_range.value,integration_time.value), 'B B'),
            response_expected=response_expected
        )
        if response_expected:
            header, _ = result
            return header['flags'] == Flags.OK

    async def get_configuration(self):
        """
        Returns the configuration as set by :func:`Set Configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_CONFIGURATION,
            response_expected=True
        )
        illuminance_range, integration_time = unpack_payload(payload, 'B B')
        illuminance_range, integration_time = IlluminanceRange(illuminance_range), IntegrationTime(integration_time)
        return GetConfiguration(illuminance_range, integration_time)

    def __value_to_SI(self, value):
        """
        Convert to the sensor value to SI units
        """
        return Decimal(value) / 100

    def __SI_to_value(self, value):
        return int(value * 100)

