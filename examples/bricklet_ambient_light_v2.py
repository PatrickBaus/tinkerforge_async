#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import warnings

from source.ip_connection import IPConnectionAsync
from source.device_factory import device_factory
from source.bricklet_ambient_light_v2 import BrickletAmbientLightV2

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
            if packet['device_id'] is BrickletAmbientLightV2.DEVICE_IDENTIFIER:
                await run_example(packet, callback_queue)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')

async def run_example(packet, callback_queue):
    print('Registering bricklet')
    bricklet = device_factory.get(packet['device_id'], packet['uid'], ipcon) # Create device object
    print('Identity:', await bricklet.get_identity())
    # Register the callback queue used by process_callbacks()
    bricklet.register_event_queue(bricklet.CallbackID.ILLUMINANCE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.ILLUMINANCE_REACHED, callback_queue)

    config = await bricklet.get_configuration()
    print('Configuration:', config)
    new_config = config._asdict()
    new_config['illuminance_range'] = bricklet.IlluminanceRange.RANGE_600LUX
    await bricklet.set_configuration(**new_config)

    print('Set callback period to', 1000, 'ms')
    await bricklet.set_illuminance_callback_period(1000)
    print('Get callback period:', await bricklet.get_illuminance_callback_period())
    print('Set bricklet debounce period to', 1000, 'ms')
    await bricklet.set_debounce_period(1000)
    print('Get bricklet debounce period:', await bricklet.get_debounce_period())
    print('Set threshold to >1 lux and wait for callbacks')
    # We use a low illuminance on purpose, so that the callback will be triggered
    await bricklet.set_illuminance_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 1, 0)
    print('Illuminance threshold:', await bricklet.get_illuminance_callback_threshold())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disabling threshold callback')
    await bricklet.set_illuminance_callback_threshold()
    print('Illumiance threshold:', await bricklet.get_illuminance_callback_threshold())
    print('Get illumiance:', await bricklet.get_illuminance())

    # Terminate the loop
    asyncio.create_task(shutdown())

async def shutdown():
    # Clean up: Disconnect ip connection and stop the consumers
    for task in running_tasks:
        task.cancel()
    await asyncio.gather(*running_tasks)
    await ipcon.disconnect()    # Disconnect the ip connection last to allow cleanup of the sensors

def error_handler(task):
    try:
        task.result()
    except Exception:
        asyncio.create_task(shutdown())

async def main():
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
asyncio.run(main(),debug=True)
