"""
Module for the Tinkerforge Isolator Bricklet
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Isolator.html) implemented using Python asyncio. It does
the low-level communication with the Tinkerforge ip connection.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, AsyncGenerator, NamedTuple

from .devices import (
    BrickletWithMCU,
    DeviceIdentifier,
    Event,
    GetSPITFPBaudrateConfig,
    GetSPITFPErrorCount,
    SimpleCallbackConfiguration,
    _FunctionID,
)
from .ip_connection_helper import base58decode, pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    STATISTICS = 9


_CallbackID = CallbackID


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_STATISTICS = 1
    SET_SPITFP_BAUDRATE_CONFIG = 2
    GET_SPITFP_BAUDRATE_CONFIG = 3
    SET_SPITFP_BAUDRATE = 4
    GET_SPITFP_BAUDRATE = 5
    GET_ISOLATOR_SPITFP_ERROR_COUNT = 6
    SET_STATISTICS_CALLBACK_CONFIGURATION = 7
    GET_STATISTICS_CALLBACK_CONFIGURATION = 8


class GetStatistics(NamedTuple):
    messages_from_brick: int
    messages_from_bricklet: int
    connected_bricklet_device_identifier: int
    connected_bricklet_uid: int


class BrickletIsolator(BrickletWithMCU):
    """
    Galvanically isolates the power and data lines of a Bricklet and its Master Brick.
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ISOLATOR
    DEVICE_DISPLAY_NAME = "Isolator Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.STATISTICS: "I I H 8s",
    }

    SID_TO_CALLBACK = {
        0: (CallbackID.STATISTICS,),
    }

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> GetStatistics:
        assert sid == 0

        return await self.get_statistics()

    async def set_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        sid: int,
        period: int = 0,
        value_has_to_change: bool = False,
        response_expected: bool = True,
    ) -> None:
        assert sid == 0

        await self.set_statistics_callback_configuration(period, value_has_to_change, response_expected)

    async def get_callback_configuration(self, sid: int) -> SimpleCallbackConfiguration:
        assert sid == 0

        return await self.get_statistics_callback_configuration()

    async def get_statistics(self) -> GetStatistics:
        """
        Returns statistics for the Isolator Bricklet.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATISTICS, response_expected=True
        )
        (
            messages_from_brick,
            messages_from_bricklet,
            connected_bricklet_device_identifier,
            connected_bricklet_uid,
        ) = unpack_payload(payload, "I I H 8s")

        return GetStatistics(
            messages_from_brick,
            messages_from_bricklet,
            connected_bricklet_device_identifier,
            base58decode(connected_bricklet_uid),
        )

    async def set_spitfp_baudrate_config(
        self,
        enable_dynamic_baudrate: bool = True,
        minimum_dynamic_baudrate: int = 400000,
        response_expected: bool = True,
    ) -> None:
        """
        The SPITF protocol can be used with a dynamic baudrate. If the dynamic baudrate is
        enabled, the Isolator Bricklet will try to adapt the baudrate for the communication
        between Bricks and Bricklets according to the amount of data that is transferred.

        The baudrate for communication config between
        Brick and Isolator Bricklet can be set through the API of the Brick.

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
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_SPITFP_BAUDRATE_CONFIG, response_expected=True
        )
        return GetSPITFPBaudrateConfig(*unpack_payload(payload, "! I"))

    async def set_spitfp_baudrate(self, baudrate: int = 1400000, response_expected: bool = True) -> None:
        """
        Sets the baudrate for the communication between Isolator Bricklet
        and the connected Bricklet. The baudrate for communication between
        Brick and Isolator Bricklet can be set through the API of the Brick.

        If you want to increase the throughput of Bricklets you can increase
        the baudrate. If you get a high error count because of high
        interference (see :func:`Get SPITFP Error Count`) you can decrease the
        baudrate.

        If the dynamic baudrate feature is enabled, the baudrate set by this
        function corresponds to the maximum baudrate (see :func:`Set SPITFP Baudrate Config`).

        Regulatory testing is done with the default baudrate. If CE compatibility
        or similar is necessary in your applications we recommend to not change
        the baudrate.
        """
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_SPITFP_BAUDRATE,
            data=pack_payload((int(baudrate),), "I"),
            response_expected=response_expected,
        )

    async def get_spitfp_baudrate(self) -> int:
        """
        Returns the baudrate, see :func:`Set SPITFP Baudrate`.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_SPITFP_BAUDRATE,
            data=pack_payload((), ""),
            response_expected=True,
        )
        return unpack_payload(payload, "I")

    async def get_isolator_spitfp_error_count(self) -> GetSPITFPErrorCount:
        """
        Returns the error count for the communication between Isolator Bricklet and
        the connected Bricklet. Call :func:`Get SPITFP Error Count` to get the
        error count between Isolator Bricklet and Brick.

        The errors are divided into

        * ACK checksum errors,
        * message checksum errors,
        * framing errors and
        * overflow errors.
        """
        _, payload = await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.GET_ISOLATOR_SPITFP_ERROR_COUNT,
            data=pack_payload((), ""),
            response_expected=True,
        )
        return GetSPITFPErrorCount(*unpack_payload(payload, "I I I I"))

    async def set_statistics_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        period: int = 0,
        value_has_to_change: bool = False,
        response_expected=True,
    ) -> None:
        """
        The period is the period with which the :cb:`Statistics`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        .. versionadded:: 2.0.2$nbsp;(Plugin)
        """
        assert period >= 0

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STATISTICS_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    int(period),
                    bool(value_has_to_change),
                ),
                "I !",
            ),
            response_expected=response_expected,
        )

    async def get_statistics_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`Set Statistics Callback Configuration`.

        .. versionadded:: 2.0.2$nbsp;(Plugin)
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_STATISTICS_CALLBACK_CONFIGURATION, response_expected=True
        )
        return SimpleCallbackConfiguration(*unpack_payload(payload, "I !"))

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

        if events is None and sids is None:
            registered_events = set(self.CALLBACK_FORMATS.keys())

        async for header, payload in super()._read_events():
            try:
                function_id = CallbackID(header.function_id)
            except ValueError:
                # Invalid header. Drop the packet.
                continue
            if function_id in registered_events:
                values = unpack_payload(payload, self.CALLBACK_FORMATS[function_id])
                yield Event(self, 0, function_id, GetStatistics(*values))
