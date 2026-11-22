"""
Hand-written checks of the unit conversions of some generated devices. The expected values are worked out from the raw
units documented by Tinkerforge, independent of the generator.
"""

from collections.abc import Callable
from decimal import Decimal

from tinkerforge_async.bricklet_accelerometer_v2 import BrickletAccelerometerV2
from tinkerforge_async.bricklet_air_quality import BrickletAirQuality
from tinkerforge_async.bricklet_co2_v2 import BrickletCO2V2
from tinkerforge_async.bricklet_energy_monitor import BrickletEnergyMonitor
from tinkerforge_async.bricklet_gps_v2 import BrickletGPSV2
from tinkerforge_async.bricklet_hall_effect_v2 import BrickletHallEffectV2
from tinkerforge_async.bricklet_load_cell_v2 import BrickletLoadCellV2
from tinkerforge_async.bricklet_temperature_ir_v2 import BrickletTemperatureIRV2
from tinkerforge_async.bricklet_voltage_current_v2 import BrickletVoltageCurrentV2
from tinkerforge_async.devices import Device
from tinkerforge_async.ip_connection import IPConnectionAsync

from .fake_connection import UID, FakeConnection, run


def reply[T: Device](
    device_class: Callable[[int, IPConnectionAsync], T], function: str, form: str, *values: int | str
) -> tuple[T, FakeConnection]:
    """Create the device, let the function reply with the raw values and return the device and the connection."""
    connection = FakeConnection()
    device = device_class(UID, connection.ipcon)
    connection.reply(getattr(device, "FunctionID")[function], form, *values)
    return device, connection


def test_voltage_current_v2() -> None:
    """The raw values are in mV, mA and mW."""
    device, _ = reply(BrickletVoltageCurrentV2, "GET_VOLTAGE", "i", 12345)
    assert run(device.get_voltage()) == Decimal("12.345")
    device, _ = reply(BrickletVoltageCurrentV2, "GET_CURRENT", "i", -1500)
    assert run(device.get_current()) == Decimal("-1.5")
    device, _ = reply(BrickletVoltageCurrentV2, "GET_POWER", "i", 18517)
    assert run(device.get_power()) == Decimal("18.517")


def test_temperature_ir_v2() -> None:
    """The raw temperatures are in 1/10 °C."""
    device, _ = reply(BrickletTemperatureIRV2, "GET_OBJECT_TEMPERATURE", "h", 1000)
    assert run(device.get_object_temperature()) == Decimal("373.15")
    device, _ = reply(BrickletTemperatureIRV2, "GET_AMBIENT_TEMPERATURE", "h", -400)
    assert run(device.get_ambient_temperature()) == Decimal("233.15")


def test_temperature_ir_v2_thresholds_are_sent_in_raw_units() -> None:
    """A threshold of 300 K to 310 K is sent as 26.85 °C to 36.85 °C in 1/10 °C, rounded."""
    connection = FakeConnection()
    device = BrickletTemperatureIRV2(UID, connection.ipcon)
    run(device.set_object_temperature_callback_configuration(0.5, False, "i", 300, Decimal("310")))
    function_id, payload, _ = connection.requests[0]
    assert function_id is BrickletTemperatureIRV2.FunctionID.SET_OBJECT_TEMPERATURE_CALLBACK_CONFIGURATION
    assert payload == (500).to_bytes(4, "little") + b"\x00i" + (268).to_bytes(2, "little") + (368).to_bytes(2, "little")


def test_air_quality() -> None:
    """The air pressure is in 1/100 hPa (= Pa), the temperature in 1/100 °C and the humidity in 1/100 %RH."""
    device, _ = reply(BrickletAirQuality, "GET_ALL_VALUES", "i B i i i", 50, 1, 2500, 4512, 101325)
    values = run(device.get_all_values())
    assert values.iaq_index == 50
    assert values.temperature == Decimal("298.15")
    assert values.humidity == Decimal("45.12")
    assert values.air_pressure == Decimal(101325)
    assert isinstance(values.air_pressure, Decimal)


def test_co2_v2() -> None:
    """The air pressure of the CO2 Bricklet 2.0 is in hPa, so it is multiplied by 100."""
    device, _ = reply(BrickletCO2V2, "GET_AIR_PRESSURE", "H", 1013)
    assert run(device.get_air_pressure()) == Decimal(101300)
    device, _ = reply(BrickletCO2V2, "GET_CO2_CONCENTRATION", "H", 415)
    assert run(device.get_co2_concentration()) == Decimal(415)  # ppm


def test_load_cell_v2() -> None:
    """The weight is in g and returned in kg."""
    device, _ = reply(BrickletLoadCellV2, "GET_WEIGHT", "i", 1250)
    assert run(device.get_weight()) == Decimal("1.25")


def test_accelerometer_v2() -> None:
    """The acceleration is in 1/10000 g and returned in m/s² (1 g = 9.80665 m/s²)."""
    device, _ = reply(BrickletAccelerometerV2, "GET_ACCELERATION", "i i i", 10000, -5000, 0)
    assert tuple(run(device.get_acceleration())) == (Decimal("9.80665"), Decimal("-4.903325"), Decimal(0))


def test_hall_effect_v2() -> None:
    """The magnetic flux density is in µT and returned in T."""
    device, _ = reply(BrickletHallEffectV2, "GET_MAGNETIC_FLUX_DENSITY", "h", -2500)
    assert run(device.get_magnetic_flux_density()) == Decimal("-0.0025")


def test_gps_v2_speed_and_altitude() -> None:
    """The course is in 1/100 °, the speed in 1/100 km/h (returned in m/s) and the altitude in cm."""
    device, _ = reply(BrickletGPSV2, "GET_MOTION", "I I", 18000, 3600)
    motion = run(device.get_motion())
    assert motion.course == 180
    assert motion.speed == 10  # 36 km/h
    device, _ = reply(BrickletGPSV2, "GET_ALTITUDE", "i i", 12345, -100)
    altitude = run(device.get_altitude())
    assert altitude.altitude == Decimal("123.45")
    assert altitude.geoidal_separation == -1


def test_energy_monitor() -> None:
    """The energy is in 1/100 Wh and returned in J."""
    # voltage, current, energy, real power, apparent power, reactive power, power factor, frequency
    raw = (23012, 512, 1, 11782, 11782, 0, 1000, 5000)
    device, _ = reply(BrickletEnergyMonitor, "GET_ENERGY_DATA", "i i i i i i H H", *raw)
    data = run(device.get_energy_data())
    assert data.voltage == Decimal("230.12")
    assert data.current == Decimal("5.12")
    assert data.energy == 36  # 1/100 Wh = 36 J
    assert data.real_power == Decimal("117.82")
    assert data.power_factor == 1  # 1/1000
    assert data.frequency == 50


def test_a_temperature_offset_is_a_difference() -> None:
    """An offset of 1 K is 1 °C, not -272.15 °C. The raw offset is in 1/100 K."""
    for device_class in (BrickletAirQuality, BrickletCO2V2):
        connection = FakeConnection()
        device = device_class(UID, connection.ipcon)
        run(device.set_temperature_offset(Decimal("1.5")))
        assert connection.requests[-1].function_id is device_class.FunctionID.SET_TEMPERATURE_OFFSET
        assert int.from_bytes(connection.requests[-1].data, "little", signed=True) == 150
    device, _ = reply(BrickletAirQuality, "GET_TEMPERATURE_OFFSET", "i", -250)
    assert run(device.get_temperature_offset()) == Decimal("-2.5")
    device, _ = reply(BrickletCO2V2, "GET_TEMPERATURE_OFFSET", "H", 0)
    assert run(device.get_temperature_offset()) == 0
