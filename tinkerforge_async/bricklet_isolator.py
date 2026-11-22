"""
Module for the Tinkerforge Isolator Bricklet
(https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Isolator.html) implemented using Python asyncio. It does
the low-level communication with the Tinkerforge ip connection.
"""

# pylint: disable=duplicate-code  # Many sensors of different generations have a similar API
from __future__ import annotations

from enum import Enum, unique
from typing import TYPE_CHECKING, Any, NamedTuple, TypeAlias, override

from .devices import (
    BrickletWithMCU,
    Channel,
    ChannelConfiguration,
    DeviceIdentifier,
    GetSPITFPBaudrateConfig,
    GetSPITFPErrorCount,
    SimpleCallbackConfiguration,
    _FunctionID,
)
from .helper import Duration, ms_to_seconds, seconds_to_ms
from .ip_connection_helper import base58decode, pack_payload, unpack_payload

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    STATISTICS = 9


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
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID

    CALLBACK_FORMATS = {
        CallbackID.STATISTICS: "I I H 8s",
    }

    CHANNELS = (
        Channel(
            0,
            getter="get_statistics",
            callbacks=(CallbackID.STATISTICS,),
            configuration=ChannelConfiguration("statistics", thresholds=False),
        ),
    )

    def __init__(self, uid, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 1)

    async def get_value(self, sid: int) -> GetStatistics:
        return await self._get_value(sid)

    async def set_callback_configuration(  # pylint: disable=too-many-arguments
        self,
        sid: int,
        period: Duration = 0,
        value_has_to_change: bool = False,
        response_expected: bool = True,
    ) -> None:
        await self._set_callback_configuration(sid, period, value_has_to_change, response_expected=response_expected)

    async def get_callback_configuration(self, sid: int) -> SimpleCallbackConfiguration:
        return await self._get_callback_configuration(sid)

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
        period: Duration = 0,
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
        if period < 0:
            raise ValueError(f"Invalid argument: expected period >= 0, got period={period!r}")

        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_STATISTICS_CALLBACK_CONFIGURATION,
            data=pack_payload(
                (
                    seconds_to_ms(period),
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
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        messages_from_brick, messages_from_bricklet, device_identifier, uid = value
        return 0, GetStatistics(messages_from_brick, messages_from_bricklet, device_identifier, base58decode(uid))
