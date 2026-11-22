"""
Module for the Tinkerforge Energy Monitor Bricklet
(https://www.tinkerforge.com/en/doc/Software/Bricklets/EnergyMonitor_Bricklet_Python.html) implemented using
Python asyncio. It does the low-level communication with the Tinkerforge ip connection and also handles
conversion of raw units to SI units.

This module was generated from the Tinkerforge API definitions (https://github.com/Tinkerforge/generators).
The descriptions of the functions are taken from the official documentation. Numbers in them can refer to the
raw values of the device. The library converts all values to the units given in the "Units" line of each
function.
"""

# pylint: disable=duplicate-code,too-many-lines
from __future__ import annotations

import asyncio
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
from .streams import Chunk, read_stream

if TYPE_CHECKING:
    from .ip_connection import IPConnectionAsync


@unique
class CallbackID(Enum):
    """
    The callbacks available to this bricklet
    """

    ENERGY_DATA = 10


@unique
class FunctionID(_FunctionID):
    """
    The function calls available to this bricklet
    """

    GET_ENERGY_DATA = 1
    RESET_ENERGY = 2
    GET_WAVEFORM_LOW_LEVEL = 3
    GET_TRANSFORMER_STATUS = 4
    SET_TRANSFORMER_CALIBRATION = 5
    GET_TRANSFORMER_CALIBRATION = 6
    CALIBRATE_OFFSET = 7
    SET_ENERGY_DATA_CALLBACK_CONFIGURATION = 8
    GET_ENERGY_DATA_CALLBACK_CONFIGURATION = 9


class GetEnergyData(NamedTuple):
    voltage: Decimal
    current: Decimal
    energy: Decimal
    real_power: Decimal
    apparent_power: Decimal
    reactive_power: Decimal
    power_factor: Decimal
    frequency: Decimal


class GetWaveform(NamedTuple):
    waveform_chunk_offset: int
    waveform_chunk_data: tuple[int, ...]


class GetTransformerStatus(NamedTuple):
    voltage_transformer_connected: bool
    current_transformer_connected: bool


class GetTransformerCalibration(NamedTuple):
    voltage_ratio: int
    current_ratio: int
    phase_shift: int


CENTI_AMPERE = LinearQuantity(1, 100)  # raw: 1/100 Ampere, returned in A
CENTI_HERTZ = LinearQuantity(1, 100)  # raw: 1/100 Hertz, returned in Hz
CENTI_VOLT = LinearQuantity(1, 100)  # raw: 1/100 Volt, returned in V
CENTI_VOLT_AMPERE = LinearQuantity(1, 100)  # raw: 1/100 Volt Ampere, returned in VA
CENTI_VOLT_AMPERE_REACTIVE = LinearQuantity(1, 100)  # raw: 1/100 Volt Ampere Reactive, returned in var
CENTI_WATT = LinearQuantity(1, 100)  # raw: 1/100 Watt, returned in W
CENTI_WATT_HOUR = LinearQuantity(36)  # raw: 1/100 Watt Hour, returned in J
RATIO_1_1000 = LinearQuantity(1, 1000)  # raw: 1/1000, dimensionless


class BrickletEnergyMonitor(BrickletWithMCU):  # pylint: disable=too-many-public-methods,too-few-public-methods
    """
    Measures Voltage, Current, Energy, Real/Apparent/Reactive Power, Power Factor and Frequency
    """

    DEVICE_IDENTIFIER = DeviceIdentifier.BRICKLET_ENERGY_MONITOR
    DEVICE_DISPLAY_NAME = "Energy Monitor Bricklet"

    # Convenience imports, so that the user does not need to additionally import them
    CallbackID: TypeAlias = CallbackID
    FunctionID = FunctionID
    ThresholdOption = Threshold

    CALLBACK_FORMATS = {
        CallbackID.ENERGY_DATA: "i i i i i i H H",
    }

    CHANNELS = (
        Channel(
            0,
            callbacks=(CallbackID.ENERGY_DATA,),
            configuration=ChannelConfiguration("energy_data", thresholds=False, wrap_advanced=True),
        ),
    )

    def __init__(self, uid: int, ipcon: IPConnectionAsync) -> None:
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        super().__init__(self.DEVICE_DISPLAY_NAME, uid, ipcon)

        self.api_version = (2, 0, 0)
        # Only one transfer of a stream at a time. The chunks of concurrent transfers would mix.
        self._stream_lock = asyncio.Lock()

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

    async def get_energy_data(self) -> GetEnergyData:
        """
        Returns all of the measurements that are done by the Energy Monitor Bricklet.

        * Voltage RMS
        * Current RMS
        * Energy (integrated over time)
        * Real Power
        * Apparent Power
        * Reactive Power
        * Power Factor
        * Frequency (AC Frequency of the mains voltage)

        The frequency is recalculated every 6 seconds.

        All other values are integrated over 10 zero-crossings of the voltage sine wave.
        With a standard AC mains voltage frequency of 50Hz this results in a 5 measurements
        per second (or an integration time of 200ms per measurement).

        If no voltage transformer is connected, the Bricklet will use the current waveform
        to calculate the frequency and it will use an integration time of
        10 zero-crossings of the current waveform.

        Units: voltage in V, current in A, energy in J, real_power in W, apparent_power in VA, reactive_power in var,
        frequency in Hz.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ENERGY_DATA, response_expected=True
        )
        voltage, current, energy, real_power, apparent_power, reactive_power, power_factor, frequency = unpack_payload(
            payload, "i i i i i i H H"
        )
        return GetEnergyData(
            CENTI_VOLT.to_si(voltage),
            CENTI_AMPERE.to_si(current),
            CENTI_WATT_HOUR.to_si(energy),
            CENTI_WATT.to_si(real_power),
            CENTI_VOLT_AMPERE.to_si(apparent_power),
            CENTI_VOLT_AMPERE_REACTIVE.to_si(reactive_power),
            RATIO_1_1000.to_si(power_factor),
            CENTI_HERTZ.to_si(frequency),
        )

    async def reset_energy(self, response_expected: bool = True) -> None:
        """
        Sets the energy value (see :func:`get_energy_data`) back to 0Wh.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.RESET_ENERGY, response_expected=response_expected
        )

    async def get_waveform_low_level(self) -> GetWaveform:
        """
        Returns a snapshot of the voltage and current waveform. The values
        in the returned array alternate between voltage and current. The data from
        one getter call contains 768 data points for voltage and current, which
        correspond to about 3 full sine waves.

        The voltage is given with a resolution of 100mV and the current is given
        with a resolution of 10mA.

        This data is meant to be used for a non-realtime graphical representation of
        the voltage and current waveforms.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_WAVEFORM_LOW_LEVEL, response_expected=True
        )
        waveform_chunk_offset, waveform_chunk_data = unpack_payload(payload, "H 30h")
        return GetWaveform(waveform_chunk_offset, tuple(waveform_chunk_data))

    async def get_waveform(self) -> tuple[int, ...]:
        """
        Returns a snapshot of the voltage and current waveform. The values
        in the returned array alternate between voltage and current. The data from
        one getter call contains 768 data points for voltage and current, which
        correspond to about 3 full sine waves.

        The voltage is given with a resolution of 100mV and the current is given
        with a resolution of 10mA.

        This data is meant to be used for a non-realtime graphical representation of
        the voltage and current waveforms.

        This function transfers the complete waveform stream and calls :func:`get_waveform_low_level` as often as
        necessary. Concurrent transfers of the stream are serialized.
        """

        async def read_chunk() -> Chunk:
            result = await self.get_waveform_low_level()
            return Chunk(1536, result.waveform_chunk_offset, result.waveform_chunk_data, result)

        async with self._stream_lock:
            data, _ = await read_stream(read_chunk, name="waveform", chunk_size=30, empty_offset=65535)
        return tuple(data)

    async def get_transformer_status(self) -> GetTransformerStatus:
        """
        Returns *true* if a voltage/current transformer is connected to the Bricklet.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TRANSFORMER_STATUS, response_expected=True
        )
        voltage_transformer_connected, current_transformer_connected = unpack_payload(payload, "! !")
        return GetTransformerStatus(voltage_transformer_connected, current_transformer_connected)

    async def set_transformer_calibration(
        self, voltage_ratio: int = 1923, current_ratio: int = 3000, phase_shift: int = 0, response_expected: bool = True
    ) -> None:
        """
        Sets the transformer ratio for the voltage and current transformer in 1/100 form.

        Example: If your mains voltage is 230V, you use 9V voltage transformer and a
        1V:30A current clamp your voltage ratio is 230/9 = 25.56 and your current ratio
        is 30/1 = 30.

        In this case you have to set the values 2556 and 3000 for voltage ratio and current
        ratio.

        The calibration is saved in non-volatile memory, you only have to set it once.

        Set the phase shift to 0. It is for future use and currently not supported by the Bricklet.
        """
        voltage_ratio = int(voltage_ratio)
        check_range("voltage_ratio", voltage_ratio, 0, 65535)
        current_ratio = int(current_ratio)
        check_range("current_ratio", current_ratio, 0, 65535)
        phase_shift = int(phase_shift)
        check_range("phase_shift", phase_shift, 0, 0)
        await self.ipcon.send_request(
            device=self,
            function_id=FunctionID.SET_TRANSFORMER_CALIBRATION,
            data=pack_payload((voltage_ratio, current_ratio, phase_shift), "H H h"),
            response_expected=response_expected,
        )

    async def get_transformer_calibration(self) -> GetTransformerCalibration:
        """
        Returns the transformer calibration as set by :func:`set_transformer_calibration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_TRANSFORMER_CALIBRATION, response_expected=True
        )
        voltage_ratio, current_ratio, phase_shift = unpack_payload(payload, "H H h")
        return GetTransformerCalibration(voltage_ratio, current_ratio, phase_shift)

    async def calibrate_offset(self, response_expected: bool = True) -> None:
        """
        Calling this function will start an offset calibration. The offset calibration will
        integrate the voltage and current waveform over a longer time period to find the 0
        transition point in the sine wave.

        The Bricklet comes with a factory-calibrated offset value, you should not have to
        call this function.

        If you want to re-calibrate the offset we recommend that you connect a load that
        has a smooth sinusoidal voltage and current waveform. Alternatively you can also
        short both inputs.

        The calibration is saved in non-volatile memory, you only have to set it once.
        """
        await self.ipcon.send_request(
            device=self, function_id=FunctionID.CALIBRATE_OFFSET, response_expected=response_expected
        )

    async def set_energy_data_callback_configuration(
        self, period: Duration = 0, value_has_to_change: bool = False, response_expected: bool = True
    ) -> None:
        """
        The period is the period with which the :attr:`CallbackID.ENERGY_DATA`
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
            function_id=FunctionID.SET_ENERGY_DATA_CALLBACK_CONFIGURATION,
            data=pack_payload((period_raw, bool(value_has_to_change)), "I !"),
            response_expected=response_expected,
        )

    async def get_energy_data_callback_configuration(self) -> SimpleCallbackConfiguration:
        """
        Returns the callback configuration as set by
        :func:`set_energy_data_callback_configuration`.
        """
        _, payload = await self.ipcon.send_request(
            device=self, function_id=FunctionID.GET_ENERGY_DATA_CALLBACK_CONFIGURATION, response_expected=True
        )
        period, value_has_to_change = unpack_payload(payload, "I !")
        return SimpleCallbackConfiguration(ms_to_seconds(period), value_has_to_change)

    @override
    def _convert_callback(self, callback_id: CallbackID, value: Any) -> tuple[int, Any]:
        voltage, current, energy, real_power, apparent_power, reactive_power, power_factor, frequency = value
        return 0, GetEnergyData(
            CENTI_VOLT.to_si(voltage),
            CENTI_AMPERE.to_si(current),
            CENTI_WATT_HOUR.to_si(energy),
            CENTI_WATT.to_si(real_power),
            CENTI_VOLT_AMPERE.to_si(apparent_power),
            CENTI_VOLT_AMPERE_REACTIVE.to_si(reactive_power),
            RATIO_1_1000.to_si(power_factor),
            CENTI_HERTZ.to_si(frequency),
        )
