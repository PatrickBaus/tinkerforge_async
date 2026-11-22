#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate the Tinkerforge Silent Stepper Bricklet 2.0.

It reads all values, that can be read without parameters, and prints the callbacks, that are already enabled.
"""

import asyncio
import warnings

from tinkerforge_async.bricklet_silent_stepper_v2 import BrickletSilentStepperV2
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletSilentStepperV2) -> None:
    """Prints the callbacks of the bricklet."""
    async for event in device.read_events():
        print("Callback received", event)


async def run_example(bricklet: BrickletSilentStepperV2) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())
        print("get_max_velocity:", await bricklet.get_max_velocity())
        print("get_current_velocity:", await bricklet.get_current_velocity())
        print("get_speed_ramping:", await bricklet.get_speed_ramping())
        print("get_current_position:", await bricklet.get_current_position())
        print("get_target_position:", await bricklet.get_target_position())
        print("get_steps:", await bricklet.get_steps())
        print("get_remaining_steps:", await bricklet.get_remaining_steps())
        print("get_step_configuration:", await bricklet.get_step_configuration())
        print("get_input_voltage:", await bricklet.get_input_voltage())
        print("get_motor_current:", await bricklet.get_motor_current())
        print("get_enabled:", await bricklet.get_enabled())
        print("get_basic_configuration:", await bricklet.get_basic_configuration())
        print("get_spreadcycle_configuration:", await bricklet.get_spreadcycle_configuration())
        print("get_stealth_configuration:", await bricklet.get_stealth_configuration())
        print("get_coolstep_configuration:", await bricklet.get_coolstep_configuration())
        print("get_misc_configuration:", await bricklet.get_misc_configuration())
        print("get_error_led_config:", await bricklet.get_error_led_config())
        print("get_driver_status:", await bricklet.get_driver_status())
        print("get_minimum_voltage:", await bricklet.get_minimum_voltage())
        print("get_time_base:", await bricklet.get_time_base())
        print("get_all_data:", await bricklet.get_all_data())
        print("get_all_data_callback_configuraton:", await bricklet.get_all_data_callback_configuraton())
        print("get_gpio_state:", await bricklet.get_gpio_state())
        print("get_motor_stalled_callback_configuraton:", await bricklet.get_motor_stalled_callback_configuraton())
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
                if isinstance(device, BrickletSilentStepperV2):
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
