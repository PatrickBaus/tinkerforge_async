#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge Barometer Bricklet.
"""
import asyncio
import warnings

from tinkerforge_async.bricklet_barometer import BrickletBarometer
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletBarometer) -> None:
    """Prints the callbacks (filtered by id) of the bricklet."""
    async for packet in device.read_events():
        print("Callback received", packet)


async def run_example(bricklet: BrickletBarometer) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        print("Get chip temperature:", await bricklet.get_chip_temperature(), "°C")

        print("Air pressure:", await bricklet.get_air_pressure(), "Pa")
        print("Altitude:", await bricklet.get_altitude(), "m")

        reference_pressure = await bricklet.get_reference_air_pressure()
        print("Reference air pressure:", reference_pressure, "Pa")
        await bricklet.set_reference_air_pressure()

        averaging_config = await bricklet.get_averaging()
        print("Averaging config:", averaging_config)
        await bricklet.set_averaging(**averaging_config._asdict())

        print("Set callback period to", 1000, "ms")
        await asyncio.gather(
            bricklet.set_air_pressure_callback_period(1000), bricklet.set_altitude_callback_period(1000)
        )
        print("Air pressure callback period:", await bricklet.get_air_pressure_callback_period())
        print("Altitude callback period:", await bricklet.get_altitude_callback_period())
        print("Set bricklet debounce period to", 1000, "ms")
        await bricklet.set_debounce_period(1000)
        print("Get bricklet debounce period:", await bricklet.get_debounce_period())

        # Use an air pressure and altitude callback
        print("Set air pressure threshold to >10 Pa and altitude to > 1m and wait for callbacks")
        # We use a low humidity on purpose, so that the callback will be triggered
        await asyncio.gather(
            bricklet.set_air_pressure_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 10, 0),
            bricklet.set_altitude_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 1, 0),
        )
        print("Air pressure threshold:", await bricklet.get_air_pressure_callback_threshold())
        print("Altitude threshold:", await bricklet.get_altitude_callback_threshold())
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disabling threshold callback")
        await asyncio.gather(bricklet.set_air_pressure_callback_threshold(), bricklet.set_altitude_callback_threshold())
        print("Air pressure threshold:", await bricklet.get_air_pressure_callback_threshold())
        print("Altitude threshold:", await bricklet.get_altitude_callback_threshold())
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
                if isinstance(device, BrickletBarometer):
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
        await shutdown(tasks)


# Report all mistakes managing asynchronous resources.
warnings.simplefilter("always", ResourceWarning)

# Start the main loop and run the async loop forever. Turn off the debug parameter for production code.
try:
    asyncio.run(main(), debug=True)
except KeyboardInterrupt:
    print("Shutting down gracefully.")
