#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge Humidity Bricklet 2.0.
"""
import asyncio
import warnings
from decimal import Decimal

from tinkerforge_async.bricklet_humidity_v2 import BrickletHumidityV2
from tinkerforge_async.devices import BrickletWithMCU
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletHumidityV2) -> None:
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


async def run_example(bricklet: BrickletHumidityV2) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        print("Moving average configuration:", await bricklet.get_moving_average_configuration())
        print("Setting moving average to 20 samples -> 50 ms/sample * 20 samples = 1 s")
        await bricklet.set_moving_average_configuration(20, 20)
        print("Moving average configuration:", await bricklet.get_moving_average_configuration())

        # Query a value
        print("Get humidity:", await bricklet.get_humidity(), "%rH")
        # Use a humidity callback
        print("Set callback period to", 1000, "ms")
        print("Set threshold to >10 %rH and wait for callbacks")
        # We use a low humidity value on purpose, so that the callback will be triggered
        await bricklet.set_humidity_callback_configuration(
            period=1000, value_has_to_change=False, option=bricklet.ThresholdOption.GREATER_THAN, minimum=10, maximum=0
        )
        print("Humidity callback configuration:", await bricklet.get_humidity_callback_configuration())
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disable threshold callback")
        await bricklet.set_humidity_callback_configuration()
        print("Humidity callback configuration:", await bricklet.get_humidity_callback_configuration())

        # Use a temperature value callback
        print("Get temperature:", await bricklet.get_temperature(), "K")
        print("Set callback period to", 1000, "ms")
        print("Set threshold to >10 °C and wait for callbacks")
        await bricklet.set_temperature_callback_configuration(
            1000, False, bricklet.ThresholdOption.GREATER_THAN, 10 + 273.15
        )
        print("Temperature callback configuration:", await bricklet.get_temperature_callback_configuration())
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disable threshold callback")
        await bricklet.set_temperature_callback_configuration()
        print("Temperature callback configuration:", await bricklet.get_temperature_callback_configuration())

        print("Enable both callbacks at once")
        await bricklet.set_temperature_callback_configuration(1000, False)
        await bricklet.set_humidity_callback_configuration(1000, False)
        print("Enabling heater")
        await bricklet.set_heater_configuration(bricklet.HeaterConfig.ENABLED)
        print("Heater config:", await bricklet.get_heater_configuration())
        await asyncio.sleep(5)  # Wait for 2-3 callbacks
        print("Disable both callbacks and heater")
        await asyncio.gather(
            bricklet.set_temperature_callback_configuration(),
            bricklet.set_humidity_callback_configuration(),
            bricklet.set_heater_configuration(),
        )
        print("Heater config:", await bricklet.get_heater_configuration())

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
        async with IPConnectionAsync(host="10.0.0.05", port=4223) as connection:
            await connection.enumerate()
            # Read all enumeration replies, then start the example if we find the correct device
            async for enumeration_type, device in connection.read_enumeration():  # pylint: disable=unused-variable
                if isinstance(device, BrickletHumidityV2):
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
