#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
Segment Display 4x7 Bricklet 2.0.
"""
import asyncio
import logging
import warnings

from tinkerforge_async.ip_connection import IPConnectionAsync
from tinkerforge_async.device_factory import device_factory
from tinkerforge_async.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2


ipcon = IPConnectionAsync()
running_tasks = []

DIGITS = [0x3f, 0x06, 0x5b, 0x4f,
          0x66, 0x6d, 0x7d, 0x07,
          0x7f, 0x6f, 0x77, 0x7c,
          0x39, 0x5e, 0x79, 0x71]   # // 0~9,A,b,C,d,E,F


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
            if packet['device_id'] is BrickletSegmentDisplay4x7V2.DEVICE_IDENTIFIER:
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
    bricklet.register_event_queue(bricklet.CallbackID.COUNTER_FINISHED, callback_queue)

    print('Setting segments to "00:00"')
    await bricklet.set_segments(segments=(DIGITS[0], DIGITS[0], DIGITS[0], DIGITS[0]), colon=(True, True), tick=False)
    print('Get segments:', await bricklet.get_segments())
    #await asyncio.sleep(3)

    print('Setting segments to "10.00"')
    await bricklet.set_segments(segments=(DIGITS[1], DIGITS[0] | 128, DIGITS[0], DIGITS[0]), colon=(False, False), tick=False)
    print('Get segments:', await bricklet.get_segments())
    #await asyncio.sleep(3)

    print('Setting segments to "10°C"')
    await bricklet.set_segments(segments=(0, DIGITS[1], DIGITS[0], DIGITS[12]), colon=(False, False), tick=True)
    print('Get segments:', await bricklet.get_segments())
    #await asyncio.sleep(3)

    print('Flashing the display')
    await bricklet.set_brightness(0)
    print('Display brightness:', await bricklet.get_brightness())
    await asyncio.sleep(0.5)
    await bricklet.set_brightness(7)
    print('Display brightness:', await bricklet.get_brightness())

    print('Setting segments to "- 42"')
    await asyncio.gather(bricklet.set_segments(), bricklet.set_numeric_value((-2, -1, 4, 2)))
    #await asyncio.sleep(3)

    print("Toggle the tick")
    is_set = await bricklet.get_selected_segment(34)
    for _ in range(5):
        await bricklet.set_selected_segment(34, not is_set)
        await asyncio.sleep(0.5)
        await bricklet.set_selected_segment(34, is_set)
        await asyncio.sleep(0.5)

    print('Counting from 0 to 5 and back again')
    await bricklet.start_counter(value_from=0, value_to=5, increment=1, length=1000)
    for _ in range(6):
        print('Counter value:', await bricklet.get_counter_value())
        await asyncio.sleep(1)    # Wait for 1 second

    await bricklet.start_counter(value_from=5, value_to=0, increment=-1, length=1000)
    for _ in range(5):
        await asyncio.sleep(1)    # Wait for 1 second
        print('Counter value:', await bricklet.get_counter_value())

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
