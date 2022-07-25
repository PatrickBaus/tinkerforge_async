#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge RS232 Bricklet 2.0.
"""
import asyncio
import warnings
from decimal import Decimal

from tinkerforge_async.bricklet_rs232_v2 import BrickletRS232V2
from tinkerforge_async.devices import BrickletWithMCU
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_frame_readable_callback(device: BrickletRS232V2) -> None:
    """
    This callback will be triggered if at least one dataframe is available. The frame size can be configured via
    set_frame_readable_callback_configuration().
    """
    async for event in device.read_events((device.CallbackID.FRAME_READABLE,)):
        print(f"Frame readable callback received. Reading frames. Frames in buffer: {event.payload}")
        # We will receive one callback for each frame, so we only read one
        # frame at a time.
        # Read 3 bytes as set by run_example() with frame_size parameter of
        # the set_frame_readable_callback_configuration() call.
        print(await device.read(3))


async def process_callbacks(device: BrickletRS232V2) -> None:
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


async def run_example(bricklet: BrickletRS232V2) -> None:
    """
    This is the actual demo. If the bricklet is found, this code will be run.
    """
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    frame_callback_task = asyncio.create_task(process_frame_readable_callback(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        config = await bricklet.get_configuration()
        print("Configuration:", config)
        config_dict = config._asdict()
        config_dict["baudrate"] = 2000000
        await bricklet.set_configuration(**config_dict)

        buffer_config = await bricklet.get_buffer_config()
        print("Buffer configuration:", buffer_config)
        await bricklet.set_buffer_config(**buffer_config._asdict())

        print("Buffer status:", await bricklet.get_buffer_status())
        print("Errors:", await bricklet.get_error_count())

        frame_size = await bricklet.get_frame_readable_callback_configuration()
        print("Trigger callback if number of bytes available:", frame_size)
        await bricklet.set_frame_readable_callback_configuration(frame_size)

        # Disable read callback to buffer a multi chunk message
        await bricklet.set_read_callback(False)
        await bricklet.set_frame_readable_callback_configuration(0)
        print("Sending message, then enable the read callback.")
        msg = b"foo" * 30
        await bricklet.write(msg)
        await bricklet.set_read_callback(True)
        print("Read callback enabled?", await bricklet.is_read_callback_enabled())

        await asyncio.sleep(0.1)
        print("Disabling read callback")
        await bricklet.set_read_callback()

        # Use a frame readable callback
        print("Enabling Frame readable callback")
        await bricklet.set_frame_readable_callback_configuration(frame_size=3)
        await bricklet.write(b"foo" * 3)
        await asyncio.sleep(0.1)
        print("Disabling Frame readable callback")
        await bricklet.set_frame_readable_callback_configuration()

        print("Polling the rs232 port")
        await bricklet.write(b"foo" * 3)
        result = await bricklet.read(len(msg))
        print("Result:", result, "number of bytes:", len(result))

        # Test the generic features of the bricklet. These are available with all new bricklets that have a
        # microcontroller
        await run_example_generic(bricklet)
    finally:
        callback_task.cancel()
        frame_callback_task.cancel()


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
                if isinstance(device, BrickletRS232V2):
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
