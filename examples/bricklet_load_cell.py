#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate the Tinkerforge Load Cell Bricklet.

It reads all values, that can be read without parameters, enables the callbacks for a few seconds and prints them.
"""

import asyncio
import warnings

from tinkerforge_async.bricklet_load_cell import BrickletLoadCell
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletLoadCell) -> None:
    """Prints the callbacks of the bricklet."""
    async for event in device.read_events():
        print("Callback received", event)


async def run_example(bricklet: BrickletLoadCell) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())
        print("get_weight:", await bricklet.get_weight())
        print("get_weight_callback_period:", await bricklet.get_weight_callback_period())
        print("get_weight_callback_threshold:", await bricklet.get_weight_callback_threshold())
        print("get_debounce_period:", await bricklet.get_debounce_period())
        print("get_moving_average:", await bricklet.get_moving_average())
        print("is_led_on:", await bricklet.is_led_on())
        print("get_configuration:", await bricklet.get_configuration())

        # Enable the callbacks of the sids [0] with a period of 1 s
        for sid in [0]:
            await bricklet.set_callback_configuration(sid, period=1)
            print(f"Callback configuration of sid {sid}:", await bricklet.get_callback_configuration(sid))
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        # Disable the callbacks
        for sid in [0]:
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
                if isinstance(device, BrickletLoadCell):
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
