#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge IO-4 Bricklet 2.0.
"""
import asyncio
import warnings
from decimal import Decimal

from tinkerforge_async.bricklet_io4_v2 import BrickletIO4V2
from tinkerforge_async.devices import BrickletWithMCU
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletIO4V2) -> None:
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


async def run_example(bricklet: BrickletIO4V2) -> None:  # pylint: disable=too-many-statements
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        print("Setting all channels to INPUT and floating them")
        await asyncio.gather(
            *[
                bricklet.set_configuration(channel=channel, direction=bricklet.Direction.IN, value=False)
                for channel in range(4)
            ]
        )  # Set all pins to "input with pull-up"
        await asyncio.sleep(0.01)
        print("Input values:", await bricklet.get_value())
        channel_configs = await asyncio.gather(*[bricklet.get_configuration(channel=channel) for channel in range(4)])
        print("Channel configs:\n", *[f"{i}: {channel}\n" for i, channel in enumerate(channel_configs)])
        print("Setting all channels to OUTPUT and driving them HIGH")
        await asyncio.gather(
            *[
                bricklet.set_configuration(channel=channel, direction=bricklet.Direction.OUT, value=True)
                for channel in range(4)
            ]
        )  # Set all pins to "input with pull-up"
        await asyncio.sleep(0.01)
        print("Output values:", await bricklet.get_value())
        channel_configs = await asyncio.gather(*[bricklet.get_configuration(channel=channel) for channel in range(4)])
        print("Channel configs:\n", *[f"{i}: {channel}\n" for i, channel in enumerate(channel_configs)])

        print("Driving all channels LOW")
        await bricklet.set_value((False, False, False, False))
        print("Output values:", await bricklet.get_value())
        print("Driving all channel 1 HIGH")
        await bricklet.set_selected_value(1, True)
        print("Output values:", await bricklet.get_value())

        print("Enabling monoflop, going HIGH for 1 second")
        await bricklet.set_monoflop(0, True, 1000)
        print("Monoflop status:", await bricklet.get_monoflop(0))
        await asyncio.sleep(1)

        print("Triggering an error, because we want to enable edge counting on an output")
        try:
            await bricklet.set_edge_count_configuration(channel=2, edge_type=bricklet.EdgeType.RISING, debounce=1)
        except ValueError:
            print("Got a ValueError.")

        print("Enabling input callbacks on channel 2")
        await asyncio.gather(
            *[
                bricklet.set_configuration(channel=channel, direction=bricklet.Direction.IN, value=False)
                for channel in range(4)
            ]
        )  # Set all pins to "input with pull-up"
        await bricklet.set_input_value_callback_configuration(channel=2, period=100, value_has_to_change=False)
        print("Callback configuration for channel 2:", await bricklet.get_input_value_callback_configuration(2))
        await bricklet.set_all_input_value_callback_configuration(period=100, value_has_to_change=False)
        print("Callback configuration for all inputs:", await bricklet.get_all_input_value_callback_configuration())
        await asyncio.sleep(0.5)
        await bricklet.set_input_value_callback_configuration(channel=2, period=100, value_has_to_change=True)
        await bricklet.set_all_input_value_callback_configuration(period=100, value_has_to_change=True)

        print("Enabling edge counting on channel 2")
        await bricklet.set_edge_count_configuration(channel=2, edge_type=bricklet.EdgeType.BOTH, debounce=1)
        print("Edge counting config:", await bricklet.get_edge_count_configuration(2))
        print("Toggling channel 2")
        await bricklet.set_configuration(channel=2, direction=bricklet.Direction.IN, value=True)
        await bricklet.set_configuration(channel=2, direction=bricklet.Direction.IN, value=False)
        await asyncio.sleep(0.1)
        print("Edges:", await bricklet.get_edge_count(2))

        print("Enabling PWM on channel 3")
        await bricklet.set_configuration(channel=3, direction=bricklet.Direction.OUT, value=False)
        await bricklet.set_pwm_configuration(channel=3, frequency=10, duty_cycle=0.5)
        print("PWM configuration:", await bricklet.get_pwm_configuration(3))
        await asyncio.sleep(1)

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
                if isinstance(device, BrickletIO4V2):
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
