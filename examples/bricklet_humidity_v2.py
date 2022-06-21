#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
Humidity Bricklet 2.0.
"""
import asyncio
import logging
import warnings

from tinkerforge_async.ip_connection import IPConnectionAsync
from tinkerforge_async.bricklet_humidity_v2 import BrickletHumidityV2

running_tasks = []


async def process_callbacks(bricklet, registered_events):
    """
    This infinite loop will print all callbacks.
    It waits for packets from the callback queue,
    which the ip connection will push.
    """
    try:
        async for event in bricklet.read_events(events=registered_events):
            print('Callback received', event)
    except asyncio.CancelledError:
        print('Callback queue canceled')


async def process_enumerations(ipcon):
    """
    This infinite loop pulls events from the internal enumeration queue
    of the ip connection and waits for an enumeration event with a
    certain device id, then it will run the example code.
    """
    try:
        print('Enumerating brick and waiting for bricklets to reply')
        await ipcon.enumerate()
        async for enumeration_type, bricklet in ipcon.read_enumeration():
            if type(bricklet) is BrickletHumidityV2:
                await run_example(bricklet)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')


async def run_example_generic(bricklet):
    """
    This is a demo of the generic features of the Tinkerforge bricklets with a
    microcontroller.
    """
    uid = await bricklet.read_uid()
    print('Device uid:', uid)
    await bricklet.write_uid(uid)

    print('SPI error count:', await bricklet.get_spitfp_error_count())

    print('Current bootloader mode:', await bricklet.get_bootloader_mode())
    bootloader_mode = bricklet.BootloaderMode.FIRMWARE
    print('Setting bootloader mode to', bootloader_mode, ':', await bricklet.set_bootloader_mode(bootloader_mode))

    print('Disable status LED')
    await bricklet.set_status_led_config(bricklet.LedConfig.OFF)
    print('Current status:', await bricklet.get_status_led_config())
    await asyncio.sleep(1)
    print('Enable status LED')
    await bricklet.set_status_led_config(bricklet.LedConfig.SHOW_STATUS)
    print('Current status:', await bricklet.get_status_led_config())

    print('Get Chip temperature:', await bricklet.get_chip_temperature(), 'K')

    print('Reset Bricklet')
    await bricklet.reset()


async def run_example(bricklet):
    """
    This is the actual demo. If the bricklet is found, this code will be run.
    """
    print('Identity:', await bricklet.get_identity())

    # Start reading callbacks
    running_tasks.append(asyncio.create_task(
        process_callbacks(bricklet, [bricklet.CallbackID.HUMIDITY, bricklet.CallbackID.TEMPERATURE]))
    )
    running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions

    print('Moving average configuration:', await bricklet.get_moving_average_configuration())
    print('Setting moving average to 20 samples -> 50 ms/sample * 20 samples = 1 s')
    await bricklet.set_moving_average_configuration(20, 20)
    print('Moving average configuration:', await bricklet.get_moving_average_configuration())

    # Query a value
    print('Get humidity:', await bricklet.get_humidity(), '%rH')
    # Use a humidity callback
    print('Set callback period to', 1000, 'ms')
    print('Set threshold to >10 %rH and wait for callbacks')
    # We use a low humidity value on purpose, so that the callback will be triggered
    await bricklet.set_humidity_callback_configuration(
        period=1000, value_has_to_change=False, option=bricklet.ThresholdOption.GREATER_THAN, minimum=10, maximum=0
    )
    print('Humidity callback configuration:', await bricklet.get_humidity_callback_configuration())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disable threshold callback')
    await bricklet.set_humidity_callback_configuration()
    print('Humidity callback configuration:', await bricklet.get_humidity_callback_configuration())

    # Use a temperature value callback
    print('Get temperature:', await bricklet.get_temperature(), 'K')
    print('Set callback period to', 1000, 'ms')
    print('Set threshold to >10 °C and wait for callbacks')
    #await bricklet.set_temperature_callback_configuration(1000, False, bricklet.ThresholdOption.GREATER_THAN, 10+273.15)
    print('Temperature callback configuration:', await bricklet.get_temperature_callback_configuration())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disable threshold callback')
    await bricklet.set_temperature_callback_configuration()
    print('Temperature callback configuration:', await bricklet.get_temperature_callback_configuration())

    print('Enable both callbacks at once')
    await bricklet.set_temperature_callback_configuration(1000, False)
    await bricklet.set_humidity_callback_configuration(1000, False)
    print('Enabling heater')
    await bricklet.set_heater_configuration(bricklet.HeaterConfig.ENABLED)
    print('Heater config:', await bricklet.get_heater_configuration())
    await asyncio.sleep(5)    # Wait for 2-3 callbacks
    print('Disable both callbacks and heater')
    await asyncio.gather(
        bricklet.set_temperature_callback_configuration(),
        bricklet.set_humidity_callback_configuration(),
        bricklet.set_heater_configuration()
    )
    print('Heater config:', await bricklet.get_heater_configuration())

    # Test the generic features of the bricklet. These are available with all
    # new bricklets that have a microcontroller
    await run_example_generic(bricklet)

    # Terminate the loop
    asyncio.create_task(shutdown())


async def shutdown():
    """
    Clean up: Disconnect ip connection and stop the consumers
    """
    for task in running_tasks:
        task.cancel()
    try:
        await asyncio.gather(*running_tasks)
    except asyncio.CancelledError:
        pass


def error_handler(task):
    """
    The main error handler. It will shut down on any uncaught exception
    """
    try:
        task.result()
    except Exception:  # pylint: disable=broad-except
        # Normally we should log these errors
        asyncio.create_task(shutdown())


async def main():
    """
    The main loop, that will spawn all callback handlers and wait until they are
    done. There are two callback handlers, one waits for the bricklet to connect
    and run the demo, the other handles messages sent by the bricklet.
    """
    try:
        async with IPConnectionAsync(host='10.0.0.5', port=4223) as ipcon:
            running_tasks.append(asyncio.create_task(process_enumerations(ipcon)))
            running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions

            # Wait for run_example() to finish
            await asyncio.gather(*running_tasks)
    except ConnectionRefusedError:
        print('Could not connect to server. Connection refused. Is the brick daemon up?')
    except asyncio.CancelledError:
        print('Stopped the main loop')

# Report all mistakes managing asynchronous resources.
warnings.simplefilter('always', ResourceWarning)
logging.basicConfig(level=logging.INFO)    # Enable logs from the ip connection. Set to debug for even more info

# Start the main loop and run the async loop forever
asyncio.run(main(), debug=True)
