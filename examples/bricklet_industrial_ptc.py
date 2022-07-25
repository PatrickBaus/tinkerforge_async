#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge Industrial PTC Bricklet.
"""
import asyncio
import warnings
from decimal import Decimal

from tinkerforge_async.bricklet_industrial_ptc import BrickletIndustrialPtc
from tinkerforge_async.devices import BrickletWithMCU
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletIndustrialPtc) -> None:
    """Prints the callbacks (filtered by id) of the bricklet."""
    async for packet in device.read_events():
        print("Callback received", packet)


async def run_example_generic(bricklet: BrickletWithMCU) -> None:
    """This is a demo of the generic features of the Tinkerforge bricklets with a microcontroller."""
    uid = await bricklet.read_uid()
    print("Device uid:", uid)
    await bricklet.write_uid(uid)

    print("SPI error count:", await bricklet.get_spitfp_error_count())

    print("Current bootloader mode:", await bricklet.get_bootloader_mode())
    bootloader_mode = bricklet.BootloaderMode.FIRMWARE
    print("Setting bootloader mode to", bootloader_mode, ":", await bricklet.set_bootloader_mode(bootloader_mode))

    print("Disable status LED")
    await bricklet.set_status_led_config(bricklet.LedConfig.OFF)
    print("Current status:", await bricklet.get_status_led_config())
    await asyncio.sleep(1)
    print("Enable status LED")
    await bricklet.set_status_led_config(bricklet.LedConfig.SHOW_STATUS)
    print("Current status:", await bricklet.get_status_led_config())

    print("Get Chip temperature:", await bricklet.get_chip_temperature() - Decimal("273.15"), "°C")

    print("Reset Bricklet")
    await bricklet.reset()


async def run_example(bricklet: BrickletIndustrialPtc) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        filter_settings = await bricklet.get_noise_rejection_filter()
        print("Noise rejection filter settings", filter_settings)
        await bricklet.set_noise_rejection_filter(filter_settings)

        moving_average_config = await bricklet.get_moving_average_configuration()
        print("Moving average config:", moving_average_config)
        await bricklet.set_moving_average_configuration(**moving_average_config._asdict())

        print("Is a sensor connected?", await bricklet.is_sensor_connected())

        wire_mode = await bricklet.get_wire_mode()
        print("Wire mode:", wire_mode)
        await bricklet.set_wire_mode(wire_mode)

        print("PTC temperature:", await bricklet.get_temperature() - Decimal("273.15"), "°C")
        print("PTC resistance:", await bricklet.get_resistance(), "Ω")

        # Use a temperature and resistance value callback
        callback_period = 10000
        print(f"Set callback period to {callback_period} ms and wait for callbacks")
        await asyncio.gather(
            bricklet.set_temperature_callback_configuration(period=callback_period),
            bricklet.set_resistance_callback_configuration(period=callback_period),
            bricklet.set_sensor_connected_callback_configuration(True),
        )
        print("Temperature callback configuration:", await bricklet.get_temperature_callback_configuration())
        print("Resistance callback configuration:", await bricklet.get_resistance_callback_configuration())
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disable callbacks")
        await asyncio.gather(
            bricklet.set_temperature_callback_configuration(),
            bricklet.set_resistance_callback_configuration(),
            bricklet.set_sensor_connected_callback_configuration(),
        )
        print("Temperature callback configuration:", await bricklet.get_temperature_callback_configuration())
        print("Resistance callback configuration:", await bricklet.get_resistance_callback_configuration())

        # Test the generic features of the bricklet. These are available with all
        # new bricklets that have a microcontroller
        await run_example_generic(bricklet)
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
                if isinstance(device, BrickletIndustrialPtc):
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
