"""
Hand-written checks of some generated discontinued devices. The expected values are worked out from the raw units
documented by Tinkerforge, independent of the generator.
"""

import struct
from collections.abc import Callable
from decimal import Decimal
from typing import Any

import pytest

from tinkerforge_async.brick_imu import BrickIMU
from tinkerforge_async.brick_stepper import BrickStepper
from tinkerforge_async.bricklet_accelerometer import BrickletAccelerometer
from tinkerforge_async.bricklet_gps import BrickletGPS
from tinkerforge_async.bricklet_temperature_ir import BrickletTemperatureIR
from tinkerforge_async.bricklet_thermocouple import G8_GAIN, G32_GAIN, BrickletThermocouple
from tinkerforge_async.bricklet_voltage_current import BrickletVoltageCurrent
from tinkerforge_async.devices import Device, Event
from tinkerforge_async.ip_connection import IPConnectionAsync

from .fake_connection import UID, FakeConnection, run

SensorType = BrickletThermocouple.SensorType
FunctionID = BrickletThermocouple.FunctionID
CallbackID = BrickletThermocouple.CallbackID


def reply[T: Device](
    device_class: Callable[[int, IPConnectionAsync], T], function: str, form: str, *values: int | str
) -> tuple[T, FakeConnection]:
    """Create the device, let the function reply with the raw values and return the device and the connection."""
    connection = FakeConnection()
    device = device_class(UID, connection.ipcon)
    connection.reply(getattr(device, "FunctionID")[function], form, *values)
    return device, connection


def test_voltage_current() -> None:
    """The raw values are in mV, mA and mW."""
    device, _ = reply(BrickletVoltageCurrent, "GET_VOLTAGE", "i", 12000)
    assert run(device.get_voltage()) == 12
    device, _ = reply(BrickletVoltageCurrent, "GET_CURRENT", "i", -250)
    assert run(device.get_current()) == Decimal("-0.25")


def test_accelerometer() -> None:
    """The acceleration is in 1/1000 g and returned in m/s², the chip temperature in °C and returned in K."""
    device, _ = reply(BrickletAccelerometer, "GET_ACCELERATION", "h h h", 1000, -500, 0)
    assert tuple(run(device.get_acceleration())) == (Decimal("9.80665"), Decimal("-4.903325"), Decimal(0))
    device, _ = reply(BrickletAccelerometer, "GET_TEMPERATURE", "h", 25)
    assert run(device.get_temperature()) == Decimal("298.15")


def test_temperature_ir() -> None:
    """The temperatures are in 1/10 °C."""
    device, _ = reply(BrickletTemperatureIR, "GET_OBJECT_TEMPERATURE", "h", 1000)
    assert run(device.get_object_temperature()) == Decimal("373.15")


def test_imu_brick() -> None:
    """The angular velocity is in 1/14.375 °/s, the magnetic field in 0.1 µT and the chip temperature in 1/10 °C."""
    device, _ = reply(BrickIMU, "GET_ANGULAR_VELOCITY", "h h h", 115, -1150, 0)
    assert tuple(run(device.get_angular_velocity())) == (Decimal(8), Decimal(-80), Decimal(0))
    device, _ = reply(BrickIMU, "GET_MAGNETIC_FIELD", "h h h", 500, 0, -10)
    assert tuple(run(device.get_magnetic_field())) == (Decimal("0.00005"), Decimal(0), Decimal("-0.000001"))
    device, _ = reply(BrickIMU, "GET_CHIP_TEMPERATURE", "h", 315)
    assert run(device.get_chip_temperature()) == Decimal("304.65")


def test_stepper_brick_motor_current() -> None:
    """The motor current is set in mA and passed in A."""
    connection = FakeConnection()
    run(BrickStepper(UID, connection.ipcon).set_motor_current(Decimal("1.5")))
    assert connection.requests[0].data == struct.pack("<H", 1500)


def test_gps_coordinates() -> None:
    """The GPS Bricklet sends the coordinates in the format DD.dddddd° times 1000000, HDOP and EPE in 1/100."""
    device, _ = reply(
        BrickletGPS, "GET_COORDINATES", "I c I c H H H H", 52518611, "N", 13376111, "E", 150, 100, 120, 500
    )
    coordinates = run(device.get_coordinates())
    assert coordinates.latitude == Decimal("52.518611")
    assert coordinates.ns == "N"
    assert coordinates.longitude == Decimal("13.376111")
    assert coordinates.hdop == Decimal("1")
    assert coordinates.epe == 5  # m


@pytest.mark.parametrize(
    "sensor_type, gain", [(SensorType.TYPE_G8, 8 * 1.6 * 2**17), (SensorType.TYPE_G32, 32 * 1.6 * 2**17)]
)
def test_thermocouple_returns_the_input_voltage_for_the_types_g8_and_g32(sensor_type: SensorType, gain: float) -> None:
    """The raw value is gain * 1.6 * 2^17 * Vin. The library returns Vin in V."""
    assert float({SensorType.TYPE_G8: G8_GAIN, SensorType.TYPE_G32: G32_GAIN}[sensor_type]) == gain
    connection = FakeConnection()
    bricklet = BrickletThermocouple(UID, connection.ipcon, sensor_type)
    assert bricklet.sensor_type is sensor_type
    connection.reply(FunctionID.GET_TEMPERATURE, "i", round(gain * 0.01))
    assert run(bricklet.get_temperature()) == pytest.approx(Decimal("0.01"), abs=Decimal(1) / Decimal(gain))
    # The thresholds are passed in V
    run(bricklet.set_temperature_callback_threshold("o", Decimal("0.01"), Decimal("0.02")))
    assert connection.requests[-1].data == struct.pack("<cii", b"o", round(gain * 0.01), round(gain * 0.02))
    # And so are the callbacks
    connection.callback(CallbackID.TEMPERATURE, "i", round(gain * 0.02))
    [event] = run(take_events(bricklet))
    assert event.payload == pytest.approx(Decimal("0.02"), abs=Decimal(1) / Decimal(gain))


async def take_events(device: Any) -> list[Event]:
    """All events of the device"""
    return [event async for event in device.read_events()]


def test_thermocouple_follows_the_configuration() -> None:
    """Setting or reading the configuration changes the conversion of the values. The default is type K."""
    connection = FakeConnection()
    bricklet = BrickletThermocouple(UID, connection.ipcon)
    default = bricklet.sensor_type
    assert default is SensorType.TYPE_K
    connection.reply(FunctionID.GET_TEMPERATURE, "i", 2500)
    assert run(bricklet.get_temperature()) == Decimal("298.15")

    run(bricklet.set_configuration(thermocouple_type=SensorType.TYPE_G8))
    configured = bricklet.sensor_type
    assert configured is SensorType.TYPE_G8
    assert run(bricklet.get_temperature()) == Decimal(2500) / G8_GAIN

    connection.reply(FunctionID.GET_CONFIGURATION, "B B B", 4, 3, 0)  # 16 samples, type K, 50 Hz
    assert run(bricklet.get_configuration()).thermocouple_type is SensorType.TYPE_K
    assert bricklet.sensor_type is SensorType.TYPE_K

    bricklet.sensor_type = 9  # The setter accepts the raw value
    assert bricklet.sensor_type is SensorType.TYPE_G32
    with pytest.raises(ValueError):
        bricklet.sensor_type = 10
