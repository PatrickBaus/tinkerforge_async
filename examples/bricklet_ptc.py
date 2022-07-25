#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge PTC Bricklet.
"""
import asyncio
import warnings

from tinkerforge_async.bricklet_ptc import BrickletPtc
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletPtc) -> None:
    """Prints the callbacks (filtered by id) of the bricklet."""
    async for packet in device.read_events():
        print("Callback received", packet)


async def run_example(bricklet: BrickletPtc) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        filter_settings = await bricklet.get_noise_rejection_filter()
        print("Noise rejection filter settings:", filter_settings)
        await bricklet.set_noise_rejection_filter(filter_settings)

        print("Is a sensor connected?", await bricklet.is_sensor_connected())

        print("Sensor type:", bricklet.sensor_type)
        bricklet.sensor_type = bricklet.SensorType.PT_100

        wire_mode = await bricklet.get_wire_mode()
        print("Wire mode:", wire_mode)
        await bricklet.set_wire_mode(wire_mode)

        print("PTC temperature:", await bricklet.get_temperature(), "°C")
        print("PTC resistance:", await bricklet.get_resistance(), "Ω")

        # Use a temperature and resistance value callback
        print("Set callback period to", 1000, "ms and wait for callbacks")
        await asyncio.gather(
            bricklet.set_temperature_callback_period(1000),
            bricklet.set_resistance_callback_period(1000),
            bricklet.set_sensor_connected_callback_configuration(True),
            bricklet.set_temperature_callback_threshold(
                option=bricklet.ThresholdOption.GREATER_THAN, minimum=0, maximum=0
            ),
            bricklet.set_resistance_callback_threshold(
                option=bricklet.ThresholdOption.GREATER_THAN, minimum=10, maximum=0
            ),
        )

        print("Get temperature callback period:", await bricklet.get_temperature_callback_period())
        print("Get resistance callback period:", await bricklet.get_resistance_callback_period())
        print(
            "Get sensor connected callback configuration:", await bricklet.get_sensor_connected_callback_configuration()
        )

        debounce_period = await bricklet.get_debounce_period()
        print("Set bricklet debounce period to", debounce_period, "ms")
        await bricklet.set_debounce_period(debounce_period)
        print("Get bricklet debounce period:", await bricklet.get_debounce_period())

        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disable callbacks")
        await asyncio.gather(
            bricklet.set_temperature_callback_period(),
            bricklet.set_resistance_callback_period(),
            bricklet.set_sensor_connected_callback_configuration(False),
            bricklet.set_temperature_callback_threshold(),
            bricklet.set_resistance_callback_threshold(),
        )
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
                if isinstance(device, BrickletPtc):
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
