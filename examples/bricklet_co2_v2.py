#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate the Tinkerforge CO2 Bricklet 2.0.

It reads all values, that can be read without parameters, enables the callbacks for a few seconds and prints them.
"""

import asyncio
import warnings

from tinkerforge_async.bricklet_co2_v2 import BrickletCO2V2
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletCO2V2) -> None:
    """Prints the callbacks of the bricklet."""
    async for event in device.read_events():
        print("Callback received", event)


async def run_example(bricklet: BrickletCO2V2) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())
        print("get_all_values:", await bricklet.get_all_values())
        print("get_air_pressure:", await bricklet.get_air_pressure())
        print("get_temperature_offset:", await bricklet.get_temperature_offset())
        print("get_all_values_callback_configuration:", await bricklet.get_all_values_callback_configuration())
        print("get_co2_concentration:", await bricklet.get_co2_concentration())
        print(
            "get_co2_concentration_callback_configuration:",
            await bricklet.get_co2_concentration_callback_configuration(),
        )
        print("get_temperature:", await bricklet.get_temperature())
        print("get_temperature_callback_configuration:", await bricklet.get_temperature_callback_configuration())
        print("get_humidity:", await bricklet.get_humidity())
        print("get_humidity_callback_configuration:", await bricklet.get_humidity_callback_configuration())
        print("get_automatic_self_calibration:", await bricklet.get_automatic_self_calibration())
        print("get_forced_recalibration:", await bricklet.get_forced_recalibration())

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
                if isinstance(device, BrickletCO2V2):
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
