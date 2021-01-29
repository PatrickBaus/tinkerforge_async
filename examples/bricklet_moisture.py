#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import warnings

from source.ip_connection import IPConnectionAsync
from source.devices import DeviceIdentifier
from source.bricklet_moisture import BrickletMoisture

ipcon = IPConnectionAsync()
callback_queue = asyncio.Queue()

running_tasks = []

async def process_callbacks():
    """
    This infinite loop will print all callbacks.
    It waits for packets from the callback queue,
    which the ip connection will push.
    """
    try:
        while 'queue not canceled':
            packet = await callback_queue.get()
            print('Callback received', packet)
    except asyncio.CancelledError:
        print('Callback queue canceled')

async def process_enumerations():
    """
    This infinite loop pulls events from the internal enumeration queue
    of the ip connection and waits for an enumeration event with a
    certain device id, then it will run the example code.
    """
    try:
        while 'queue not canceled':
            packet = await ipcon.enumeration_queue.get()
            if packet['device_id'] is BrickletMoisture.DEVICE_IDENTIFIER:
                await run_example(packet)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')

async def run_example(packet):
    print('Registering bricklet')
    bricklet = BrickletMoisture(packet['uid'], ipcon) # Create device object
    print('Identity:', await bricklet.get_identity())
    # Register the callback queue used by process_callbacks()
    bricklet.register_event_queue(BrickletMoisture.CallbackID.moisture_reached, callback_queue)

    print('Setting moving average to 20 samples')
    await bricklet.set_moving_average(20)
    print('Moving average configuration:', await bricklet.get_moving_average())
    print('Resetting moving average')
    await bricklet.set_moving_average()

    print('Set callback period to', 1000, 'ms')
    await bricklet.set_moisture_callback_period(1000)
    print('Get callback period:', await bricklet.get_moisture_callback_period())
    print('Set bricklet debounce period to', 1000, 'ms')
    await bricklet.set_debounce_period(1000)
    print('Get bricklet debounce period:', await bricklet.get_debounce_period())
    print('Set threshold to >10 and wait for callbacks')
    # We use a low 'moisture value' on purpose, so that the callback will be triggered
    await bricklet.set_moisture_callback_threshold(bricklet.ThresholdOption.greater_than, 10, 0)
    print('Moisture threshold:', await bricklet.get_moisture_callback_threshold())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disabling threshold callback')
    await bricklet.set_moisture_callback_threshold()
    print('Moisture threshold:', await bricklet.get_moisture_callback_threshold())
    print('Get Moisture:', await bricklet.get_moisture_value())


    # Terminate the loop
    asyncio.ensure_future(stop_loop())

async def stop_loop():
    # Clean up: Disconnect ip connection and stop the consumers
    await ipcon.disconnect()
    for task in running_tasks:
        task.cancel()
    await asyncio.gather(*running_tasks)
    asyncio.get_running_loop().stop()

def error_handler(task):
    try:
        task.result()
    except Exception:
        asyncio.ensure_future(stop_loop())

async def main():
    try: 
        await ipcon.connect(host='127.0.0.1', port=4223)
        running_tasks.append(asyncio.ensure_future(process_callbacks()))
        running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions
        running_tasks.append(asyncio.ensure_future(process_enumerations()))
        running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions
        print('Enumerating brick and waiting for bricklets to reply')
        await ipcon.enumerate()
    except ConnectionRefusedError:
        print('Could not connect to server. Connection refused. Is the brick daemon up?')
    except asyncio.CancelledError:
        print('Stopped the main loop')

# Report all mistakes managing asynchronous resources.
warnings.simplefilter('always', ResourceWarning)
logging.basicConfig(level=logging.INFO)    # Enable logs from the ip connection. Set to debug for even more info

# Start the main loop, the run the async loop forever
running_tasks.append(asyncio.ensure_future(main()))
running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions
loop = asyncio.get_event_loop()
loop.set_debug(enabled=True)    # Raise all execption and log all callbacks taking longer than 100 ms
loop.run_forever()
loop.close()
