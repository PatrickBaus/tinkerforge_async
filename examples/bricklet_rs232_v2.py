#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import warnings

from source.ip_connection import IPConnectionAsync
from source.device_factory import device_factory
from source.bricklet_rs232_v2 import BrickletRS232V2, Rs232IOError

ipcon = IPConnectionAsync()
running_tasks = []

async def process_frame_readable_callback(queue):
    try:
        while 'queue not canceled':
            packet = await queue.get()
            print('Frame readable callback received. Reading frames. Frames in buffer: {frames}'.format(frames=packet['payload']))
            bricklet = packet['sender']
            # We will receive one callback for each frame, so we only read one frame at a time
            print(await bricklet.read(3))   # Read 3 bytes as set by run_example()
    except asyncio.CancelledError:
        print('Frame readable callback queue canceled')

async def process_callbacks(queue):
    """
    This infinite loop will print all callbacks.
    It waits for packets from the callback queue,
    which the ip connection will push.
    """
    try:
        while 'queue not canceled':
            packet = await queue.get()
            if packet['function_id'] is BrickletRS232V2.CallbackID.FRAME_READABLE:
                pass
            print('Callback received', packet)
    except asyncio.CancelledError:
        print('Callback queue canceled')

async def process_enumerations(callback_queue, frame_readable_callback_queue):
    """
    This infinite loop pulls events from the internal enumeration queue
    of the ip connection and waits for an enumeration event with a
    certain device id, then it will run the example code.
    """
    try:
        while 'queue not canceled':
            packet = await ipcon.enumeration_queue.get()
            if packet['device_id'] is BrickletRS232V2.DEVICE_IDENTIFIER:
                await run_example(packet, callback_queue, frame_readable_callback_queue)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')

async def run_example(packet, callback_queue, frame_readable_callback_queue):
    print('Registering bricklet')
    bricklet = device_factory.get(packet['device_id'], packet['uid'], ipcon) # Create device object
    print('Identity:', await bricklet.get_identity())

    uid = await bricklet.read_uid()
    print('Device uid:', uid)
    await bricklet.write_uid(uid)

    print('Disable status LED')
    await bricklet.set_status_led_config(bricklet.LedConfig.OFF)
    print('Current status:', await bricklet.get_status_led_config())
    await asyncio.sleep(1)
    print('Enable status LED')
    await bricklet.set_status_led_config(bricklet.LedConfig.SHOW_STATUS)
    print('Current status:', await bricklet.get_status_led_config())

    print('Get Chip temperature:', await bricklet.get_chip_temperature(), '°C')

    config = await bricklet.get_configuration()
    print('Configuration:', config)
    config = config._asdict()
    config['baudrate'] = 2000000
    await bricklet.set_configuration(**config)

    config = await bricklet.get_buffer_config()
    print('Buffer configuration:', config)
    await bricklet.set_buffer_config(**config._asdict())

    print('Buffer status:', await bricklet.get_buffer_status())
    print('Errors:', await bricklet.get_error_count())
    
    config = await bricklet.get_frame_readable_callback_configuration()
    print('Trigger callback if number of bytes available:', config)
    await bricklet.set_frame_readable_callback_configuration(config)

    # Register the callback queue used by process_callbacks()
    # We can register the same queue for multiple callbacks.
    bricklet.register_event_queue(bricklet.CallbackID.READ, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.ERROR_COUNT, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.FRAME_READABLE, frame_readable_callback_queue)

    # Disable read callback to buffer a multi chunk message
    await bricklet.set_read_callback(False)
    await bricklet.set_frame_readable_callback_configuration(0)
    print('Sending message, then enable the read callback.')
    msg = b'foo'*30
    await bricklet.write(msg)
    await bricklet.set_read_callback(True)
    print('Read callback enabled?', await bricklet.is_read_callback_enabled())

    await asyncio.sleep(0.1)
    print('Disabling read callback')
    await bricklet.set_read_callback()
    
    # Use a frame readable callback
    print('Enabling Frame readable callback')
    await bricklet.set_frame_readable_callback_configuration(3)
    await bricklet.write(b'foo'*3)
    await asyncio.sleep(0.1)
    print('Disabling Frame readable callback')
    await bricklet.set_frame_readable_callback_configuration()

    print('Polling the rs232 port')
    await bricklet.write(b'foo'*3)
    result = await bricklet.read(len(msg))
    print('Result:', result, 'number of bytes:', len(result))

    print('Reset Bricklet')
    await bricklet.reset()

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
        frame_readable_callback_queue = asyncio.Queue()
        running_tasks.append(asyncio.create_task(process_callbacks(callback_queue)))
        running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions
        running_tasks.append(asyncio.create_task(process_frame_readable_callback(frame_readable_callback_queue)))
        running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions
        running_tasks.append(asyncio.create_task(process_enumerations(callback_queue, frame_readable_callback_queue)))
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
