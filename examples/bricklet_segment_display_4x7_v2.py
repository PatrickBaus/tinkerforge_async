#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge Segment Display 4x7 Bricklet 2.0.
"""
import asyncio
import warnings
from decimal import Decimal

from tinkerforge_async.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
from tinkerforge_async.devices import BrickletWithMCU
from tinkerforge_async.ip_connection import IPConnectionAsync

DIGITS = [
    0x3F,
    0x06,
    0x5B,
    0x4F,
    0x66,
    0x6D,
    0x7D,
    0x07,
    0x7F,
    0x6F,
    0x77,
    0x7C,
    0x39,
    0x5E,
    0x79,
    0x71,
]  # // 0~9,A,b,C,d,E,F


async def process_callbacks(device: BrickletSegmentDisplay4x7V2) -> None:
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


async def run_example(bricklet: BrickletSegmentDisplay4x7V2) -> None:
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        print('Setting segments to "00:00"')
        await bricklet.set_segments(
            segments=(DIGITS[0], DIGITS[0], DIGITS[0], DIGITS[0]), colon=(True, True), tick=False
        )
        print("Get segments:", await bricklet.get_segments())
        # await asyncio.sleep(3)

        print('Setting segments to "10.00"')
        await bricklet.set_segments(
            segments=(DIGITS[1], DIGITS[0] | 128, DIGITS[0], DIGITS[0]), colon=(False, False), tick=False
        )
        print("Get segments:", await bricklet.get_segments())
        # await asyncio.sleep(3)

        print('Setting segments to "10°C"')
        await bricklet.set_segments(segments=(0, DIGITS[1], DIGITS[0], DIGITS[12]), colon=(False, False), tick=True)
        print("Get segments:", await bricklet.get_segments())
        # await asyncio.sleep(3)

        print("Flashing the display")
        await bricklet.set_brightness(0)
        print("Display brightness:", await bricklet.get_brightness())
        await asyncio.sleep(0.5)
        await bricklet.set_brightness(7)
        print("Display brightness:", await bricklet.get_brightness())

        print('Setting segments to "- 42"')
        await asyncio.gather(bricklet.set_segments(), bricklet.set_numeric_value((-2, -1, 4, 2)))
        # await asyncio.sleep(3)

        print("Toggle the tick")
        is_set = await bricklet.get_selected_segment(34)
        for _ in range(5):
            await bricklet.set_selected_segment(34, not is_set)
            await asyncio.sleep(0.5)
            await bricklet.set_selected_segment(34, is_set)
            await asyncio.sleep(0.5)

        print("Counting from 0 to 5 and back again")
        await bricklet.start_counter(value_from=0, value_to=5, increment=1, length=1000)
        for _ in range(6):
            print("Counter value:", await bricklet.get_counter_value())
            await asyncio.sleep(1)  # Wait for 1 second

        await bricklet.start_counter(value_from=5, value_to=0, increment=-1, length=1000)
        for _ in range(5):
            await asyncio.sleep(1)  # Wait for 1 second
            print("Counter value:", await bricklet.get_counter_value())

        # Test the generic features of the bricklet. These are available with all new bricklets that have a
        # microcontroller
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
                if isinstance(device, BrickletSegmentDisplay4x7V2):
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
