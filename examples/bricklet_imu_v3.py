#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate the Tinkerforge IMU Bricklet 3.0.

It reads all values, that can be read without parameters, enables the callbacks for a few seconds and prints them.
"""

import asyncio
import warnings

from tinkerforge_async.bricklet_imu_v3 import BrickletIMUV3
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletIMUV3) -> None:
    """Prints the callbacks of the bricklet."""
    async for event in device.read_events():
        print("Callback received", event)


async def run_example(bricklet: BrickletIMUV3) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())
        print("get_acceleration:", await bricklet.get_acceleration())
        print("get_magnetic_field:", await bricklet.get_magnetic_field())
        print("get_angular_velocity:", await bricklet.get_angular_velocity())
        print("get_temperature:", await bricklet.get_temperature())
        print("get_orientation:", await bricklet.get_orientation())
        print("get_linear_acceleration:", await bricklet.get_linear_acceleration())
        print("get_gravity_vector:", await bricklet.get_gravity_vector())
        print("get_quaternion:", await bricklet.get_quaternion())
        print("get_all_data:", await bricklet.get_all_data())
        print("get_sensor_configuration:", await bricklet.get_sensor_configuration())
        print("get_sensor_fusion_mode:", await bricklet.get_sensor_fusion_mode())
        print("get_acceleration_callback_configuration:", await bricklet.get_acceleration_callback_configuration())
        print("get_magnetic_field_callback_configuration:", await bricklet.get_magnetic_field_callback_configuration())
        print(
            "get_angular_velocity_callback_configuration:", await bricklet.get_angular_velocity_callback_configuration()
        )
        print("get_temperature_callback_configuration:", await bricklet.get_temperature_callback_configuration())
        print("get_orientation_callback_configuration:", await bricklet.get_orientation_callback_configuration())
        print(
            "get_linear_acceleration_callback_configuration:",
            await bricklet.get_linear_acceleration_callback_configuration(),
        )
        print("get_gravity_vector_callback_configuration:", await bricklet.get_gravity_vector_callback_configuration())
        print("get_quaternion_callback_configuration:", await bricklet.get_quaternion_callback_configuration())
        print("get_all_data_callback_configuration:", await bricklet.get_all_data_callback_configuration())

        # Enable the callbacks of the sids [0, 1, 2, 3] with a period of 1 s
        for sid in [0, 1, 2, 3]:
            await bricklet.set_callback_configuration(sid, period=1)
            print(f"Callback configuration of sid {sid}:", await bricklet.get_callback_configuration(sid))
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        # Disable the callbacks
        for sid in [0, 1, 2, 3]:
            await bricklet.set_callback_configuration(sid)
    finally:
        callback_task.cancel()


async def main() -> None:
    """
    The main loop, that will spawn all callback handlers and wait until they are done. There are two callback handlers,
    one waits for the bricklet to connect and runs the demo, the other handles messages sent by the bricklet.
    """
    tasks = set()
    try:
        # Use the context manager of the ip connection. It will automatically do the cleanup.
        async with IPConnectionAsync(host="127.0.0.1", port=4223) as connection:
            await connection.enumerate()
            # Read all enumeration replies, then start the example if we find the correct device
            async for enumeration_type, device in connection.read_enumeration():  # pylint: disable=unused-variable
                if isinstance(device, BrickletIMUV3):
                    print(f"Found {device}, running example.")
                    tasks.add(asyncio.create_task(run_example(device)))
                    break
                print(f"Found {device}, but not interested.")

            # Wait for run_example() to finish
            await asyncio.gather(*tasks)
    except ConnectionRefusedError:
        print("Could not connect to server. Connection refused. Is the brick daemon up?")
    except asyncio.CancelledError:
        print("Stopped the main loop.")
        raise  # It is good practice to re-raise CancelledErrors
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


# Report all mistakes managing asynchronous resources.
warnings.simplefilter("always", ResourceWarning)

# Start the main loop and run the async loop forever. Turn off the debug parameter for production code.
try:
    asyncio.run(main(), debug=True)
except KeyboardInterrupt:
    print("Shutting down gracefully.")
