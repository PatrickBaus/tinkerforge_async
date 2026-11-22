#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate the Tinkerforge Thermal Imaging Bricklet.

It reads all values, that can be read without parameters, and prints the callbacks, that are already enabled.
"""

import asyncio
import warnings

from tinkerforge_async.bricklet_thermal_imaging import BrickletThermalImaging
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletThermalImaging) -> None:
    """Prints the callbacks of the bricklet."""
    async for event in device.read_events():
        print("Callback received", event)


async def run_example(bricklet: BrickletThermalImaging) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())
        print("get_statistics:", await bricklet.get_statistics())
        print("get_resolution:", await bricklet.get_resolution())
        print("get_spotmeter_config:", await bricklet.get_spotmeter_config())
        print("get_high_contrast_config:", await bricklet.get_high_contrast_config())
        print("get_image_transfer_config:", await bricklet.get_image_transfer_config())
        print("get_flux_linear_parameters:", await bricklet.get_flux_linear_parameters())
        print("get_ffc_shutter_mode:", await bricklet.get_ffc_shutter_mode())
        await asyncio.sleep(2)  # Print the callbacks, that are already enabled
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
                if isinstance(device, BrickletThermalImaging):
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
