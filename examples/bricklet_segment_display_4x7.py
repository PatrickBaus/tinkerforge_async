#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import warnings

from source.ip_connection import IPConnectionAsync
from source.devices import DeviceIdentifier
from source.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7

loop = asyncio.get_event_loop()
ipcon = IPConnectionAsync(loop=loop)
callback_queue = asyncio.Queue()

running_tasks = []

DIGITS = [0x3f,0x06,0x5b,0x4f,
          0x66,0x6d,0x7d,0x07,
          0x7f,0x6f,0x77,0x7c,
          0x39,0x5e,0x79,0x71] # // 0~9,A,b,C,d,E,F

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
            if packet['device_id'] is DeviceIdentifier.BrickletSegmentDisplay4x7:
                await run_example(packet)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')

async def run_example(packet):
    print('Registering BrickletSegmentDisplay4x7 bricklet')
    bricklet = BrickletSegmentDisplay4x7(packet['uid'], ipcon) # Create device object
    print('Identity:', await bricklet.get_identity())
    # Register the callback queue used by process_callbacks()
    bricklet.register_event_queue(BrickletSegmentDisplay4x7.CallbackID.counter_finished, callback_queue)

    print('Setting segments to "00:00"')
    await bricklet.set_segments(segments=[DIGITS[0],DIGITS[0],DIGITS[0],DIGITS[0]], brightness=3, colon=True)
    print('Get segments:', await bricklet.get_segments())
    print('Counting from 0 to 5 and back again')
    await bricklet.start_counter(value_from=0, value_to=5, increment=1, length=1000)
    for i in range(6):
        print('Counter value: ', await bricklet.get_counter_value())
        await asyncio.sleep(1)    # Wait for 1 second

    await bricklet.start_counter(value_from=5, value_to=0, increment=-1, length=1000)
    for i in range(5):
        await asyncio.sleep(1)    # Wait for 1 second
        print('Counter value: ', await bricklet.get_counter_value())

#    print('Turning off segments')
#    await bricklet.set_segments(segments=[0,0,0,0], brightness=0, colon=True)

    # Terminate the loop
    asyncio.ensure_future(stop_loop())

async def stop_loop():
    # Clean up: Disconnect ip connection and stop the consumers
    await ipcon.disconnect()
    for task in running_tasks:
        task.cancel()
    await asyncio.gather(*running_tasks)
    loop.stop()    

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
        print("Enumerating brick and waiting for bricklets to reply")
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
loop.set_debug(enabled=True)    # Raise all execption and log all callbacks taking longer than 100 ms
loop.run_forever()
loop.close()
