#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge Industrial Dual 0-20mA Bricklet 2.0.
"""

import asyncio
import warnings
from decimal import Decimal

from tinkerforge_async.bricklet_industrial_dual_0_20ma_v2 import BrickletIndustrialDual020mAV2
from tinkerforge_async.devices import BrickletWithMCU
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletIndustrialDual020mAV2) -> None:
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

    print("Get Chip temperature:", await bricklet.get_chip_temperature(), "K")

    print("Reset Bricklet")
    await bricklet.reset()


async def run_example(bricklet: BrickletIndustrialDual020mAV2) -> None:
    """This is a demo of the features of the Tinkerforge Industrial Dual 0-20mA Bricklet 2.0."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        # Sample rate and gain. A lower sample rate increases the resolution and reduces the noise.
        await bricklet.set_sample_rate(bricklet.SamplingRate.RATE_4_SPS)
        print("Sampling rate:", await bricklet.get_sample_rate())
        await bricklet.set_gain(bricklet.Gain.GAIN_1X)
        print("Gain:", await bricklet.get_gain())

        # Query LEDs
        print("Channel 0 led configuration:", await bricklet.get_channel_led_config(0))
        print("Channel 1 led config:", await bricklet.get_channel_led_config(1))
        led_status_config = await bricklet.get_channel_led_status_config(0)
        print("Channel 0 led status config", led_status_config)
        await bricklet.set_channel_led_status_config(0, **led_status_config._asdict())
        led_status_config = await bricklet.get_channel_led_status_config(1)
        print("Channel 1 led status config", led_status_config)
        conf = led_status_config._asdict()
        conf["config"] = conf["config"].value  # convert to int. Both int and enum work
        await bricklet.set_channel_led_status_config(1, **conf)

        print("Setting channel leds to heartbeat")
        await bricklet.set_channel_led_config(0, bricklet.ChannelLedConfig.SHOW_HEARTBEAT)
        await bricklet.set_channel_led_config(1, bricklet.ChannelLedConfig.SHOW_HEARTBEAT)
        await asyncio.sleep(1)
        print("Setting channel leds to intensity mode, scaled between 0.004 A and 0.02 A")
        await bricklet.set_channel_led_status_config(
            0, Decimal("0.004"), Decimal("0.02"), bricklet.ChannelLedStatusConfig.INTENSITY
        )
        await bricklet.set_channel_led_status_config(
            1, Decimal("0.004"), Decimal("0.02"), bricklet.ChannelLedStatusConfig.INTENSITY
        )

        # Query a value. All currents are returned in A.
        print("Get current, channel 0:", await bricklet.get_current(0), "A")
        print("Get current, channel 1:", await bricklet.get_current(1), "A")

        # Use a current value callback
        print("Set callback period to", 1, "s and wait for callbacks")
        await bricklet.set_current_callback_configuration(channel=0, period=1)
        await bricklet.set_current_callback_configuration(channel=1, period=0.5)
        print("Current callback configuration, channel 0:", await bricklet.get_current_callback_configuration(0))
        print("Current callback configuration, channel 1:", await bricklet.get_current_callback_configuration(1))
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disable callbacks")
        await bricklet.set_current_callback_configuration(0)
        await bricklet.set_current_callback_configuration(1)

        # Use a callback with a threshold: only fire when the current of channel 0 is greater than 0.01 A, with a
        # period of 1 s. Thresholds are given in A.
        print("Set threshold callback on channel 0 (> 0.01 A)")
        await bricklet.set_current_callback_configuration(
            channel=0, period=1, option=bricklet.ThresholdOption.GREATER_THAN, minimum=Decimal("0.01")
        )
        print("Current callback configuration, channel 0:", await bricklet.get_current_callback_configuration(0))
        await asyncio.sleep(2.1)
        print("Disable callback")
        await bricklet.set_current_callback_configuration(0)

        print("Resetting channel leds to status")
        await bricklet.set_channel_led_config(0, bricklet.ChannelLedConfig.SHOW_STATUS)
        await bricklet.set_channel_led_config(1, bricklet.ChannelLedConfig.SHOW_STATUS)

        # Test the generic features of the bricklet. These are available with all new bricklets that have a
        # microcontroller
        await run_example_generic(bricklet)
    finally:
        callback_task.cancel()


async def shutdown(tasks: set[asyncio.Task[None]]) -> None:
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
                if isinstance(device, BrickletIndustrialDual020mAV2):
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
