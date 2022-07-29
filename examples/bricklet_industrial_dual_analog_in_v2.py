#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge Industrial Dual Analog In Bricklet 2.0.
"""
import asyncio
import warnings
from decimal import Decimal

from tinkerforge_async.bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2
from tinkerforge_async.devices import BrickletWithMCU
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletIndustrialDualAnalogInV2) -> None:
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


async def run_example(bricklet: BrickletIndustrialDualAnalogInV2) -> None:
    """This is a demo of the generic features of the Tinkerforge bricklets with a microcontroller."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        await bricklet.set_sample_rate(bricklet.SamplingRate.RATE_1_SPS)
        print("Sampling rate:", await bricklet.get_sample_rate())

        cal_data = await bricklet.get_calibration()
        print("Calibration data:", cal_data)
        await bricklet.set_calibration(**cal_data._asdict())
        print("ADC raw values (with offset subtracted):", await bricklet.get_adc_values())

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

        # Query a value
        print("Get voltage, channel 0:", await bricklet.get_voltage(0), "V")
        print("Get voltage, channel 1:", await bricklet.get_voltage(1), "V")

        # Use a voltage value callback
        print("Set callback period to", 1000, "ms and wait for callbacks")
        await bricklet.set_voltage_callback_configuration(channel=0, period=1000)
        await bricklet.set_voltage_callback_configuration(channel=1, period=500)
        print("Voltage callback configuration, channel 0:", await bricklet.get_voltage_callback_configuration(0))
        print("Voltage callback configuration, channel 1:", await bricklet.get_voltage_callback_configuration(1))
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disable callbacks")
        await bricklet.set_voltage_callback_configuration(0)
        await bricklet.set_voltage_callback_configuration(1)
        print("Voltage callback configuration, channel 0:", await bricklet.get_voltage_callback_configuration(0))
        print("Voltage callback configuration, channel 1:", await bricklet.get_voltage_callback_configuration(1))

        # Use all voltages callback
        print("Get all voltages:", await bricklet.get_all_voltages())

        await bricklet.set_all_voltages_callback_configuration(period=1000)
        print("All voltages callback configuration:", await bricklet.get_all_voltages_callback_configuration())
        await asyncio.sleep(2.1)  # Wait for 2-3 callbacks
        print("Disable callback")
        await bricklet.set_all_voltages_callback_configuration()
        print("All voltages callback configuration:", await bricklet.get_all_voltages_callback_configuration())

        print("Resetting channel leds to status")
        await bricklet.set_channel_led_config(0, bricklet.ChannelLedConfig.SHOW_STATUS)
        await bricklet.set_channel_led_config(1, bricklet.ChannelLedConfig.SHOW_STATUS)

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
                if isinstance(device, BrickletIndustrialDualAnalogInV2):
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
