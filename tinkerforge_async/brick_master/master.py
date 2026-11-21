"""
Module for the Tinkerforge Master Brick (https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html)
implemented using Python AsyncIO. It does the low-level communication with the Tinkerforge ip connection and also
handles conversion of raw units to SI units.
"""

# pylint: disable=too-many-lines,duplicate-code
from __future__ import annotations

from decimal import Decimal
from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias

from ..devices import BasicCallbackConfiguration
from ..devices import BrickletPort as Port
from ..devices import DeviceIdentifier, DeviceWithMCU, GetSPITFPBaudrateConfig, GetSPITFPErrorCount
from ..devices import ThresholdOption as Threshold
from ..helper import Duration, ms_to_seconds, seconds_to_ms
from ..ip_connection_helper import pack_payload, unpack_payload
from ..quantities import CELSIUS_ZERO, Quantity
from .chibi import ChibiExtension, ChibiFrequency
from .common import ConnectionType, FunctionID
from .ethernet import EthernetConnection, EthernetExtension, PhyMode
from .rs485 import Rs485Extension, Rs485Parity
from .wifi import WifiConnection, WifiExtension
from .wifi2 import Wifi2Extension, WifiApEncryption, WifiClientStatus, WifiMeshStatus

if TYPE_CHECKING:
    from ..ip_connection import IPConnectionAsync


class GetProtocol1BrickletName(NamedTuple):
    protocol_version: int
    firmware_version: tuple[int, int, int]
    name: str


@unique
class CallbackID(Enum):
    """
    The callbacks available to this brick
    """

    STACK_CURRENT = 59
    STACK_VOLTAGE = 60
    USB_VOLTAGE = 61
    STACK_CURRENT_REACHED = 62
    STACK_VOLTAGE_REACHED = 63
    USB_VOLTAGE_REACHED = 64


@unique
class ExtensionPosition(Enum):
    """
    The position of the master extension in the stack.
    """

    BOTTOM = 0
    TOP = 1


@unique
class ExtensionType(Enum):
    """
    The types of master extensions available.
    """

    CHIBI = 1
    RS485 = 2
    WIFI = 3
    ETHERNET = 4
    WIFI2 = 5


VOLTAGE = Quantity(1000)  # raw: mV
CURRENT = Quantity(1000)  # raw: mA


class BrickMaster(
    ChibiExtension, Rs485Extension, WifiExtension, EthernetExtension, Wifi2Extension, DeviceWithMCU
):  # pylint: disable=too-many-ancestors,too-many-public-methods
    """
    Basis to build stacks and has 4 Bricklet ports
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICK_MASTER

    DEVICE_DISPLAY_NAME = "Master Brick"

    CallbackID: TypeAlias = CallbackID

    FunctionID = FunctionID

    ExtensionPosition: TypeAlias = ExtensionPosition

    ExtensionType: TypeAlias = ExtensionType

    BrickletPort = Port

    ConnectionType: TypeAlias = ConnectionType

    ChibiFrequency: TypeAlias = ChibiFrequency

    Rs485Parity: TypeAlias = Rs485Parity

    WifiConnection: TypeAlias = WifiConnection

    EthernetConnection: TypeAlias = EthernetConnection

    PhyMode: TypeAlias = PhyMode

    WifiClientStatus = WifiClientStatus

    WifiApEncryption: TypeAlias = WifiApEncryption

    WifiMeshStatus = WifiMeshStatus

    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.STACK_CURRENT: "H",
        CallbackID.STACK_VOLTAGE: "H",
        CallbackID.USB_VOLTAGE: "H",
        CallbackID.STACK_CURRENT_REACHED: "H",
        CallbackID.STACK_VOLTAGE_REACHED: "H",
        CallbackID.USB_VOLTAGE_REACHED: "H",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.USB_VOLTAGE, CallbackID.USB_VOLTAGE_REACHED),
        1: (CallbackID.STACK_VOLTAGE, CallbackID.STACK_VOLTAGE_REACHED),
        2: (CallbackID.STACK_CURRENT, CallbackID.STACK_CURRENT_REACHED),
    }

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 4)

    async def get_stack_voltage(self) -> Decimal:
        """
        Returns the stack voltage in V. The stack voltage is the
        voltage that is supplied via the stack, i.e. it is given by a
        Step-Down or Step-Up Power Supply.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_VOLTAGE, response_expected=True
        )
        return VOLTAGE.to_si(unpack_payload(payload, "H"))

    async def get_stack_current(self) -> Decimal:
        """
        Returns the stack current in A. The stack current is the
        current that is drawn via the stack, i.e. it is given by a
        Step-Down or Step-Up Power Supply.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_CURRENT, response_expected=True
        )
        return CURRENT.to_si(unpack_payload(payload, "H"))

    async def set_extension_type(
        self, extension: ExtensionPosition, exttype: ExtensionType | int, response_expected: bool = True
    ) -> None:
        """
        Writes the extension type to the EEPROM of a specified extension.
        The extension is either 0 or 1 (0 is the on the bottom, 1 is the one on top,
        if only one extension is present use 0).

        Possible extension types:

        .. csv-table::
         :header: "Type", "Description"
         :widths: 10, 100

         "1",    "Chibi"
         "2",    "RS485"
         "3",    "Wi-Fi"
         "4",    "Ethernet"
         "5",    "Wi-Fi 2.0"

        The extension type is already set when bought, and it can be set with the
        Brick Viewer, it is unlikely that you need this function.
        """
        if not isinstance(extension, ExtensionPosition):
            extension = ExtensionPosition(extension)
        if not isinstance(exttype, ExtensionType):
            exttype = ExtensionType(exttype)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_EXTENSION_TYPE,
            data=pack_payload((extension.value, exttype.value), "B I"),
            response_expected=response_expected,
        )

    async def get_extension_type(self, extension: int) -> ExtensionType:
        """
        Returns the type for a given extension as set by :func:`Set Extension Type`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_EXTENSION_TYPE,
            data=pack_payload((int(extension),), "B"),
            response_expected=True,
        )
        return ExtensionType(unpack_payload(payload, "I"))

    async def get_usb_voltage(self) -> Decimal:
        """
        Returns the USB voltage in V. Does not work with hardware version 2.1.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_USB_VOLTAGE, response_expected=True
        )

        return VOLTAGE.to_si(unpack_payload(payload, "H"))

    async def set_stack_current_callback_period(self, period: Duration, response_expected: bool = True) -> None:
        """
        Sets the period in s with which the :cb:`Stack Current` callback is triggered periodically. A value of 0 turns
        the callback off.

        The :cb:`Stack Current` callback is only triggered if the current has changed since the last triggering.

        The default value is 0.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STACK_CURRENT_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_stack_current_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set Stack Current Callback Period`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_CURRENT_CALLBACK_PERIOD, response_expected=True
        )

        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_stack_voltage_callback_period(self, period: Duration, response_expected: bool = True) -> None:
        """
        Sets the period in s with which the :cb:`Stack Voltage` callback is triggered periodically. A value of 0 turns
        the callback off.

        The :cb:`Stack Voltage` callback is only triggered if the voltage has changed
        since the last triggering.

        The default value is 0.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STACK_VOLTAGE_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_stack_voltage_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set Stack Voltage Callback Period`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_VOLTAGE_CALLBACK_PERIOD, response_expected=True
        )

        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_usb_voltage_callback_period(self, period: Duration, response_expected: bool = True) -> None:
        """
        Sets the period in s with which the :cb:`USB Voltage` callback is triggered periodically. A value of 0 turns
        the callback off.

        The :cb:`USB Voltage` callback is only triggered if the voltage has changed since the last triggering.

        The default value is 0.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_USB_VOLTAGE_CALLBACK_PERIOD,
            data=pack_payload((seconds_to_ms(period),), "I"),
            response_expected=response_expected,
        )

    async def get_usb_voltage_callback_period(self) -> Decimal:
        """
        Returns the period as set by :func:`Set USB Voltage Callback Period`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_USB_VOLTAGE_CALLBACK_PERIOD, response_expected=True
        )

        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_stack_current_callback_threshold(
        self,
        option: Threshold | int,
        minimum: float | Decimal,
        maximum: float | Decimal,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Stack Current Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the current is *outside* the min and max values"
         "'i'",    "Callback is triggered when the current is *inside* the min and max values"
         "'<'",    "Callback is triggered when the current is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the current is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STACK_CURRENT_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value,
                    CURRENT.from_si(minimum),
                    CURRENT.from_si(maximum),
                ),
                "c H H",
            ),
            response_expected=response_expected,
        )

    async def get_stack_current_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Stack Current Callback Threshold`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_CURRENT_CALLBACK_THRESHOLD, response_expected=True
        )

        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(
            Threshold(option),
            CURRENT.to_si(minimum),
            CURRENT.to_si(maximum),
        )

    async def set_stack_voltage_callback_threshold(
        self,
        option: Threshold | int,
        minimum: float | Decimal,
        maximum: float | Decimal,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`Stack Voltage Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
         "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
         "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STACK_VOLTAGE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value,
                    VOLTAGE.from_si(minimum),
                    VOLTAGE.from_si(maximum),
                ),
                "c H H",
            ),
            response_expected=response_expected,
        )

    async def get_stack_voltage_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set Stack Voltage Callback Threshold`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STACK_VOLTAGE_CALLBACK_THRESHOLD, response_expected=True
        )

        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(
            Threshold(option),
            VOLTAGE.to_si(minimum),
            VOLTAGE.to_si(maximum),
        )

    async def set_usb_voltage_callback_threshold(
        self,
        option: Threshold | int,
        minimum: float | Decimal,
        maximum: float | Decimal,
        response_expected: bool = True,
    ) -> None:
        """
        Sets the thresholds for the :cb:`USB Voltage Reached` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the voltage is *outside* the min and max values"
         "'i'",    "Callback is triggered when the voltage is *inside* the min and max values"
         "'<'",    "Callback is triggered when the voltage is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the voltage is greater than the min value (max is ignored)"

        The default value is ('x', 0, 0).

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        if not isinstance(option, Threshold):
            option = Threshold(option)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_USB_VOLTAGE_CALLBACK_THRESHOLD,
            data=pack_payload(
                (
                    option.value,
                    VOLTAGE.from_si(minimum),
                    VOLTAGE.from_si(maximum),
                ),
                "c H H",
            ),
            response_expected=response_expected,
        )

    async def get_usb_voltage_callback_threshold(self) -> BasicCallbackConfiguration:
        """
        Returns the threshold as set by :func:`Set USB Voltage Callback Threshold`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_USB_VOLTAGE_CALLBACK_THRESHOLD, response_expected=True
        )

        option, minimum, maximum = unpack_payload(payload, "c H H")
        return BasicCallbackConfiguration(
            Threshold(option),
            VOLTAGE.to_si(minimum),
            VOLTAGE.to_si(maximum),
        )

    async def set_debounce_period(self, debounce: Duration = Decimal("0.1"), response_expected: bool = True) -> None:
        """
        Sets the period in s with which the threshold callbacks

        * :cb:`Stack Current Reached`,
        * :cb:`Stack Voltage Reached`,
        * :cb:`USB Voltage Reached`

        are triggered, if the thresholds

        * :func:`Set Stack Current Callback Threshold`,
        * :func:`Set Stack Voltage Callback Threshold`,
        * :func:`Set USB Voltage Callback Threshold`

        keep being reached.

        The default value is 0.1.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_DEBOUNCE_PERIOD,
            data=pack_payload((seconds_to_ms(debounce),), "I"),
            response_expected=response_expected,
        )

    async def get_debounce_period(self) -> Decimal:
        """
        Returns the debounce period as set by :func:`Set Debounce Period`.

        .. versionadded:: 2.0.5$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_DEBOUNCE_PERIOD, response_expected=True
        )

        return ms_to_seconds(unpack_payload(payload, "I"))

    async def set_spitfp_baudrate_config(
        self,
        enable_dynamic_baudrate: bool = True,
        minimum_dynamic_baudrate: int = 400000,
        response_expected: bool = True,
    ) -> None:
        """
        The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is
        enabled, the Brick will try to adapt the baudrate for the communication
        between Bricks and Bricklets according to the amount of data that is transferred.

        The baudrate will be increased exponentially if lots of data is sent/received and
        decreased linearly if little data is sent/received.

        This lowers the baudrate in applications where little data is transferred (e.g.
        a weather station) and increases the robustness. If there is lots of data to transfer
        (e.g. Thermal Imaging Bricklet) it automatically increases the baudrate as needed.

        In cases where some data has to transferred as fast as possible every few seconds
        (e.g. RS485 Bricklet with a high baudrate but small payload) you may want to turn
        the dynamic baudrate off to get the highest possible performance.

        The maximum value of the baudrate can be set per port with the function
        :func:`Set SPITFP Baudrate`. If the dynamic baudrate is disabled, the baudrate
        as set by :func:`Set SPITFP Baudrate` will be used statically.

        The minimum dynamic baudrate has a value range of 400000 to 2000000 baud.

        By default, dynamic baudrate is enabled and the minimum dynamic baudrate is 400000.

        .. versionadded:: 2.4.6$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE_CONFIG,
            data=pack_payload((bool(enable_dynamic_baudrate), int(minimum_dynamic_baudrate)), "! I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate_config(self) -> GetSPITFPBaudrateConfig:
        """
        Returns the baudrate config, see :func:`Set SPITFP Baudrate Config`.

        .. versionadded:: 2.4.6$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPITFP_BAUDRATE_CONFIG, response_expected=True
        )
        return GetSPITFPBaudrateConfig(*unpack_payload(payload, "! I"))

    async def get_send_timeout_count(self, communication_method: ConnectionType | int) -> int:
        """
        Returns the timeout count for the different communication methods.

        The methods 0-2 are available for all Bricks, 3-7 only for Master Bricks.

        This function is mostly used for debugging during development, in normal operation
        the counters should nearly always stay at 0.

        .. versionadded:: 2.4.3$nbsp;(Firmware)
        """
        if not isinstance(communication_method, ConnectionType):
            communication_method = ConnectionType(communication_method)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SEND_TIMEOUT_COUNT,
            data=pack_payload((communication_method.value,), "B"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def set_spitfp_baudrate(
        self, bricklet_port: Port, baudrate: int = 1400000, response_expected: bool = True
    ) -> None:
        """
        Sets the baudrate for a specific Bricklet port ('a' - 'd'). The
        baudrate can be in the range 400000 to 2000000.

        If you want to increase the throughput of Bricklets you can increase
        the baudrate. If you get a high error count because of high
        interference (see :func:`Get SPITFP Error Count`) you can decrease the
        baudrate.

        If the dynamic baudrate feature is enabled, the baudrate set by this
        function corresponds to the maximum baudrate (see :func:`Set SPITFP Baudrate Config`).

        Regulatory testing is done with the default baudrate. If CE compatability
        or similar is necessary in you applications we recommend to not change
        the baudrate.

        The default baudrate for all ports is 1400000.

        .. versionadded:: 2.4.3$nbsp;(Firmware)
        """
        if not isinstance(bricklet_port, Port):
            bricklet_port = Port(bricklet_port)

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE,
            data=pack_payload((bricklet_port.value.encode(), int(baudrate)), "c I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate(self, bricklet_port: Port) -> int:
        """
        Returns the baudrate for a given Bricklet port, see :func:`Set SPITFP Baudrate`.

        .. versionadded:: 2.4.3$nbsp;(Firmware)
        """
        if not isinstance(bricklet_port, Port):
            bricklet_port = Port(bricklet_port)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_BAUDRATE,
            data=pack_payload((bricklet_port.value.encode(),), "c"),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def get_spitfp_error_count(self, bricklet_port: Port) -> GetSPITFPErrorCount:
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ACK checksum errors,
        * message checksum errors,
        * framing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Brick side. All
        Bricklets have a similar function that returns the errors on the Bricklet side.

        .. versionadded:: 2.4.3$nbsp;(Firmware)
        """
        # TODO: Are these values reset after some time? I see varying error rates
        if not isinstance(bricklet_port, Port):
            bricklet_port = Port(bricklet_port)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_ERROR_COUNT,
            data=pack_payload((bricklet_port.value.encode(),), "c"),
            response_expected=True,
        )
        return GetSPITFPErrorCount(*unpack_payload(payload, "I I I I"))

    async def enable_status_led(self, response_expected: bool = True) -> None:
        """
        Enables the status LED.

        The status LED is the blue LED next to the USB connector. If enabled is is
        on and it flickers if data is transfered. If disabled it is always off.

        The default state is enabled.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.ENABLE_STATUS_LED, response_expected=response_expected
        )

    async def disable_status_led(self, response_expected: bool = True) -> None:
        """
        Disables the status LED.

        The status LED is the blue LED next to the USB connector. If enabled is is
        on and it flickers if data is transfered. If disabled it is always off.

        The default state is enabled.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.DISABLE_STATUS_LED, response_expected=response_expected
        )

    async def is_status_led_enabled(self) -> bool:
        """
        Returns *true* if the status LED is enabled, *false* otherwise.

        .. versionadded:: 2.3.2$nbsp;(Firmware)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.IS_STATUS_LED_ENABLED, response_expected=True
        )
        return unpack_payload(payload, "!")

    async def get_protocol1_bricklet_name(self, bricklet_port: Port) -> GetProtocol1BrickletName:
        """
        Returns the firmware and protocol version and the name of the Bricklet for a
        given port.

        This functions sole purpose is to allow automatic flashing of v1.x.y Bricklet
        plugins.
        """
        if not isinstance(bricklet_port, Port):
            bricklet_port = Port(bricklet_port)

        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_PROTOCOL1_BRICKLET_NAME,
            data=pack_payload((bricklet_port.value.encode(),), "c"),
            response_expected=True,
        )
        return GetProtocol1BrickletName(*unpack_payload(payload, "B 3B 40s"))

    async def get_chip_temperature(self) -> Decimal:
        """
        Returns the temperature in K as measured inside the microcontroller. The value returned is not the ambient
        temperature!

        The temperature is only proportional to the real temperature, and it has an accuracy of +-15%. Practically it is
        only useful as an indicator for temperature changes.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_CHIP_TEMPERATURE, response_expected=True
        )
        result = unpack_payload(payload, "h")
        return Decimal(result) / 10 + CELSIUS_ZERO

    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        if callback_id in (CallbackID.USB_VOLTAGE, CallbackID.USB_VOLTAGE_REACHED):
            return 0, VOLTAGE.to_si(value)
        if callback_id in (CallbackID.STACK_VOLTAGE, CallbackID.STACK_VOLTAGE_REACHED):
            return 1, VOLTAGE.to_si(value)
        return 2, CURRENT.to_si(value)
