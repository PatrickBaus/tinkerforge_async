#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge Humidity Bricklet.
"""
import asyncio
import warnings

from tinkerforge_async.bricklet_humidity import BrickletHumidity
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletHumidity) -> None:
    """Prints the callbacks (filtered by id) of the bricklet."""
    async for packet in device.read_events():
        print("Callback received", packet)


async def run_example(bricklet: BrickletHumidity) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        print("Set callback period to", 1000, "ms")
        await bricklet.set_humidity_callback_period(1000)
        print("Get callback period:", await bricklet.get_humidity_callback_period())
        print("Set bricklet debounce period to", 1000, "ms")
        await bricklet.set_debounce_period(1000)
        print("Get bricklet debounce period:", await bricklet.get_debounce_period())

        # Use a humidity callback
        print("Get humidity:", await bricklet.get_humidity())
        print("Set threshold to >10 %rH and wait for callbacks")
        # We use a low humidity on purpose, so that the callback will be triggered
        await bricklet.set_humidity_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 10, 0)
        print("Humidity threshold:", await bricklet.get_humidity_callback_threshold())
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disabling threshold callback")
        await bricklet.set_humidity_callback_threshold()
        print("Humidity threshold:", await bricklet.get_humidity_callback_threshold())

        # Use an analog value callback
        print("Get analog value:", await bricklet.get_analog_value())
        print("Set threshold to >10 and wait for callbacks")
        await bricklet.set_analog_value_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 10, 0)
        print("Analog value threshold:", await bricklet.get_analog_value_callback_threshold())
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disabling threshold callback")
        await bricklet.set_analog_value_callback_threshold()
        print("Analog value threshold:", await bricklet.get_analog_value_callback_threshold())
    finally:
        callback_task.cancel()


async def shutdown(tasks: set[asyncio.Task]) -> None:
    """Clean up by stopping all consumers"""
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks)


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
                if isinstance(device, BrickletHumidity):
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
    finally:
        await shutdown(tasks)


# Report all mistakes managing asynchronous resources.
warnings.simplefilter("always", ResourceWarning)

# Start the main loop and run the async loop forever
asyncio.run(main(), debug=True)
