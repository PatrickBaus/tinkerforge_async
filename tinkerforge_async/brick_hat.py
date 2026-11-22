"""
Module for the Tinkerforge HAT Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/HAT_Brick_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, cast, override

from .devices import (
    AdvancedCallbackConfiguration,
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    SimpleCallbackConfiguration,
)
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
    The callbacks available to this brick
    """

    VOLTAGES = 8


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """

    SET_SLEEP_MODE = 1
    GET_SLEEP_MODE = 2
    SET_BRICKLET_POWER = 3
    GET_BRICKLET_POWER = 4
    GET_VOLTAGES = 5
    SET_VOLTAGES_CALLBACK_CONFIGURATION = 6
    GET_VOLTAGES_CALLBACK_CONFIGURATION = 7
    SET_RTC_DRIVER = 9
    GET_RTC_DRIVER = 10


@unique
class RTCDriver(Enum):
    """
    The rtc driver options
    """

    PCF8523 = 0
    DS1338 = 1


class GetSleepMode(NamedTuple):
    power_off_delay: Decimal
    power_off_duration: Decimal
    raspberry_pi_off: bool
    bricklets_off: bool
    enable_sleep_indicator: bool


class GetVoltages(NamedTuple):
    voltage_usb: Decimal
    voltage_dc: Decimal


MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V
SECOND = LinearQuantity(1)  # raw: 1/1 Second, returned in s


class BrickHAT(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    HAT for Raspberry Pi with 8 Bricklets ports and real-time clock
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_HAT
    DEVICE_DISPLAY_NAME = "HAT Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold
    RTCDriver: TypeAlias = RTCDriver

    CALLBACK_FORMATS = {
        CallbackID.VOLTAGES: "H H",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.VOLTAGES,),
            configuration=ChannelConfiguration("voltages", thresholds=False, wrap_advanced=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 2)

    @override
    async def set_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
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

    @override
    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def set_sleep_mode(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        power_off_delay: float | Decimal,
        power_off_duration: float | Decimal,
        raspberry_pi_off: bool,
        bricklets_off: bool,
        enable_sleep_indicator: bool,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the sleep mode.

        .. note::
         Calling this function will cut the Raspberry Pi's power after Power Off Delay seconds.
         You have to shut down the operating system yourself, e.g. by calling 'sudo shutdown -h now'.

        Parameters:

        * Power Off Delay: Time before the RPi/Bricklets are powered off.
        * Power Off Duration: Duration that the RPi/Bricklets stay powered off.
        * Raspberry Pi Off: RPi is powered off if set to true.
        * Bricklets Off: Bricklets are powered off if set to true.
        * Enable Sleep Indicator: If set to true, the status LED will blink in a 1s interval
          during the whole power off duration. This will draw additional 0.3mA.

        Example: To turn RPi and Bricklets off in 5 seconds for 10 minutes with sleep
        indicator enabled, call (5, 60*10, true, true, true).

        This function can also be used to implement a watchdog. To do this you can
        write a program that calls this function once per second in a loop with
        (10, 2, true, false, false). If the RPi crashes or gets stuck
        the HAT will reset the RPi after 10 seconds.

        Units: power_off_delay in s, power_off_duration in s.
        """
        power_off_delay_raw = SECOND.from_si(power_off_delay)
        check_range("power_off_delay", power_off_delay_raw, 0, 4294967295, power_off_delay)
        power_off_duration_raw = SECOND.from_si(power_off_duration)
        check_range("power_off_duration", power_off_duration_raw, 0, 4294967295, power_off_duration)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SLEEP_MODE,
            data=pack_payload(
                (
                    power_off_delay_raw,
                    power_off_duration_raw,
                    bool(raspberry_pi_off),
                    bool(bricklets_off),
                    bool(enable_sleep_indicator),
                ),
                "I I ! ! !",
            ),
            response_expected=response_expected,
        )

    async def get_sleep_mode(self) -> GetSleepMode:
        """
        Returns the sleep mode settings as set by :func:`set_sleep_mode`.

        Units: power_off_delay in s, power_off_duration in s.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SLEEP_MODE, response_expected=True
        )
        power_off_delay, power_off_duration, raspberry_pi_off, bricklets_off, enable_sleep_indicator = unpack_payload(
            payload, "I I ! ! !"
        )
        return GetSleepMode(
            SECOND.to_si(power_off_delay),
            SECOND.to_si(power_off_duration),
            raspberry_pi_off,
            bricklets_off,
            enable_sleep_indicator,
        )

    async def set_bricklet_power(self, bricklet_power: bool = True, response_expected: bool = True) -> None:
        """
        Set to true/false to turn the power supply of the connected Bricklets on/off.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_BRICKLET_POWER,
            data=pack_payload((bool(bricklet_power),), "!"),
            response_expected=response_expected,
        )

    async def get_bricklet_power(self) -> bool:
        """
        Returns the power status of the connected Bricklets as set by :func:`set_bricklet_power`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_BRICKLET_POWER, response_expected=True
        )
        return cast(bool, unpack_payload(payload, "!"))

    async def get_voltages(self) -> GetVoltages:
        """
        Returns the USB supply voltage and the DC input supply voltage.

        There are three possible combinations:

        * Only USB connected: The USB supply voltage will be fed back to the
          DC input connector. You will read the USB voltage and a slightly lower
          voltage on the DC input.
        * Only DC input connected: The DC voltage will not be fed back to the
          USB connector. You will read the DC input voltage and the USB voltage
          will be 0.
        * USB and DC input connected: You will read both voltages. In this case
          the USB supply will be without load, but it will work as backup if you
          disconnect the DC input (or if the DC input voltage falls below the
          USB voltage).

        Units: voltage_usb in V, voltage_dc in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGES, response_expected=True
        )
        voltage_usb, voltage_dc = unpack_payload(payload, "H H")
        return GetVoltages(MILLI_VOLT.to_si(voltage_usb), MILLI_VOLT.to_si(voltage_dc))

    async def set_voltages_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.VOLTAGES`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_VOLTAGES_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_voltages_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_voltages_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_VOLTAGES_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    async def set_rtc_driver(self, rtc_driver: RTCDriver | int, response_expected: bool = True) -> None:
        """
        Configures the RTC driver that is given to the Raspberry Pi to be used.
        Currently there are two different RTCs used:

        * Hardware version <= 1.5: PCF8523
        * Hardware version 1.6: DS1338

        The correct driver will be set during factory flashing by Tinkerforge.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_RTC_DRIVER,
            data=pack_payload((RTCDriver(rtc_driver).value,), "B"),
            response_expected=response_expected,
        )

    async def get_rtc_driver(self) -> RTCDriver:
        """
        Returns the RTC driver as set by :func:`set_rtc_driver`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_RTC_DRIVER, response_expected=True
        )
        return RTCDriver(unpack_payload(payload, "B"))

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        voltage_usb, voltage_dc = value
        return 0, GetVoltages(MILLI_VOLT.to_si(voltage_usb), MILLI_VOLT.to_si(voltage_dc))
