"""
Module for the Tinkerforge HAT Zero Brick
(https://www.tinkerforge.com/en/doc/Software/Bricks/HATZero_Brick_Python.html) implemented using
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
from typing import TYPE_CHECKING, Any, TypeAlias, cast, override

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
    The callbacks available to this brick
    """

    USB_VOLTAGE = 4


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this brick
    """

    GET_USB_VOLTAGE = 1
    SET_USB_VOLTAGE_CALLBACK_CONFIGURATION = 2
    GET_USB_VOLTAGE_CALLBACK_CONFIGURATION = 3


MILLI_VOLT = LinearQuantity(1, 1000)  # raw: 1/1000 Volt, returned in V


class BrickHATZero(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    HAT for Raspberry Pi Zero with 4 Bricklets ports
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_HAT_ZERO
    DEVICE_DISPLAY_NAME = "HAT Zero Brick"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.USB_VOLTAGE: "H",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_usb_voltage",
            callbacks=(CallbackID.USB_VOLTAGE,),
            configuration=ChannelConfiguration("usb_voltage"),
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

    async def get_callback_configuration(self, sid: int) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration of the channel with the secondary id `sid`.
        """
        return cast(AdvancedCallbackConfiguration, await self._get_callback_configuration(sid))

    async def get_usb_voltage(self) -> Decimal:
        """
        Returns the USB supply voltage of the Raspberry Pi.

        Units: voltage in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_USB_VOLTAGE, response_expected=True
        )
        return MILLI_VOLT.to_si(unpack_payload(payload, "H"))

    async def set_usb_voltage_callback_configuration(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        period: Duration = 0,
        value_has_to_change: bool = False,
        option: Threshold | str = Threshold.OFF,
        minimum: float | Decimal = 0,
        maximum: float | Decimal = 0,
        response_expected: bool = True,
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.USB_VOLTAGE` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :attr:`CallbackID.USB_VOLTAGE` callback.

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

        Units: minimum in V, maximum in V.
        """
        period_raw = seconds_to_ms(period)
        check_range("period", period_raw, 0, 4294967295, period)
        minimum_raw = MILLI_VOLT.from_si(minimum)
        check_range("minimum", minimum_raw, 0, 65535, minimum)
        maximum_raw = MILLI_VOLT.from_si(maximum)
        check_range("maximum", maximum_raw, 0, 65535, maximum)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_USB_VOLTAGE_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (period_raw, bool(value_has_to_change), Threshold(option).value, minimum_raw, maximum_raw), "I ! c H H"
            ),
            response_expected=response_expected,
        )

    async def get_usb_voltage_callback_configuration(self) -> AdvancedCallbackConfiguration:
        """
        Returns the callback configuration as set by :func:`set_usb_voltage_callback_configuration`.

        Units: minimum in V, maximum in V.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_USB_VOLTAGE_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change, option, minimum, maximum = unpack_payload(payload, "I ! c H H")
        return AdvancedCallbackConfiguration(
            ms_to_seconds(period),
            value_has_to_change,
            Threshold(option),
            MILLI_VOLT.to_si(minimum),
            MILLI_VOLT.to_si(maximum),
        )

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        return 0, MILLI_VOLT.to_si(value)
