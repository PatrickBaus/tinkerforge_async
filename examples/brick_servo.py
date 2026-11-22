#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate the Tinkerforge Servo Brick.

It reads all values, that can be read without parameters, and prints the callbacks, that are already enabled.
"""

import asyncio
import warnings

from tinkerforge_async.brick_servo import BrickServo
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickServo) -> None:
    """Prints the callbacks of the brick."""
    async for event in device.read_events():
        print("Callback received", event)


async def run_example(brick: BrickServo) -> None:
    """This is the actual demo. If the brick is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(brick))
    try:
        print("Identity:", await brick.get_identity())
        print("get_output_voltage:", await brick.get_output_voltage())
        print("get_overall_current:", await brick.get_overall_current())
        print("get_stack_input_voltage:", await brick.get_stack_input_voltage())
        print("get_external_input_voltage:", await brick.get_external_input_voltage())
        print("get_minimum_voltage:", await brick.get_minimum_voltage())
        print("is_position_reached_callback_enabled:", await brick.is_position_reached_callback_enabled())
        print("is_velocity_reached_callback_enabled:", await brick.is_velocity_reached_callback_enabled())
        print("get_spitfp_baudrate_config:", await brick.get_spitfp_baudrate_config())
        print("is_status_led_enabled:", await brick.is_status_led_enabled())
        print("get_chip_temperature:", await brick.get_chip_temperature())
        await asyncio.sleep(2)  # Print the callbacks, that are already enabled
    finally:
        callback_task.cancel()


async def main() -> None:
    """
    The main loop, that will spawn all callback handlers and wait until they are done. There are two callback handlers,
    one waits for the brick to connect and runs the demo, the other handles messages sent by the brick.
    """
    tasks = set()
    try:
        # Use the context manager of the ip connection. It will automatically do the cleanup.
        async with IPConnectionAsync(host="127.0.0.1", port=4223) as connection:
            await connection.enumerate()
            # Read all enumeration replies, then start the example if we find the correct device
            async for enumeration_type, device in connection.read_enumeration():  # pylint: disable=unused-variable
                if isinstance(device, BrickServo):
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
