#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
Motion Detector Bricklet 2.0.
"""
import asyncio
import logging
import warnings

from tinkerforge_async.ip_connection import IPConnectionAsync
from tinkerforge_async.device_factory import device_factory
from tinkerforge_async.bricklet_motion_detector_v2 import BrickletMotionDetectorV2

ipcon = IPConnectionAsync()
running_tasks = []


async def process_callbacks(queue):
    """
    This infinite loop will print all callbacks.
    It waits for packets from the callback queue,
    which the ip connection will push.
    """
    try:
        while 'queue not canceled':
            packet = await queue.get()
            print('Callback received', packet)
    except asyncio.CancelledError:
        print('Callback queue canceled')


async def process_enumerations(callback_queue):
    """
    This infinite loop pulls events from the internal enumeration queue
    of the ip connection and waits for an enumeration event with a
    certain device id, then it will run the example code.
    """
    try:
        while 'queue not canceled':
            packet = await ipcon.enumeration_queue.get()
            if packet['device_id'] is BrickletMotionDetectorV2.DEVICE_IDENTIFIER:
                await run_example(packet, callback_queue)
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

    print('Get Chip temperature:', await bricklet.get_chip_temperature(), '°C')

    print('Reset Bricklet')
    await bricklet.reset()


async def run_example(packet, callback_queue):
    """
    This is the actual demo. If the bricklet is found, this code will be run.
    """
    print('Registering bricklet')
    bricklet = device_factory.get(packet['device_id'], packet['uid'], ipcon)    # Create device object
    print('Identity:', await bricklet.get_identity())

    # Register the callback queue used by process_callbacks()
    # We can register the same queue for multiple callbacks.
    bricklet.register_event_queue(bricklet.CallbackID.MOTION_DETECTED, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.DETECTION_CYCLE_ENDED, callback_queue)

    # Query the value
    print('Motion detected?:', await bricklet.get_motion_detected())
    print('Set sensitivity to maximum and wait for callbacks')
    await bricklet.set_sensitivity(100)
    print('Sensitivity set to {value}.'.format(value=await bricklet.get_sensitivity()))
    print('Enabling lights.')
    await bricklet.set_indicator(top_left=255, top_right=255, bottom=255)
    print('Indicator status:', await bricklet.get_indicator())
    print('Waiting 10 seconds for callbacks')
    await asyncio.sleep(10)    # Wait for callbacks
    print('Done waiting.')

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
    await asyncio.gather(*running_tasks)
    await ipcon.disconnect()    # Disconnect the ip connection last to allow cleanup of the sensors


def error_handler(task):
    """
    The main error handler. It will shutdown on any uncaught exception
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
        await ipcon.connect(host='127.0.0.1', port=4223)
        callback_queue = asyncio.Queue()
        running_tasks.append(asyncio.create_task(process_callbacks(callback_queue)))
        running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions
        running_tasks.append(asyncio.create_task(process_enumerations(callback_queue)))
        running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions
        print('Enumerating brick and waiting for bricklets to reply')
        await ipcon.enumerate()

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
