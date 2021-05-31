#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
PTC Bricklet.
"""
import asyncio
import logging
import warnings

from TinkerforgeAsync.ip_connection import IPConnectionAsync
from TinkerforgeAsync.device_factory import device_factory
from TinkerforgeAsync.bricklet_ptc import BrickletPtc

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
            if packet['device_id'] is BrickletPtc.DEVICE_IDENTIFIER:
                await run_example(packet, callback_queue)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')


async def run_example(packet, callback_queue):
    """
    This is the actual demo. If the bricklet is found, this code will be run.
    """
    print('Registering bricklet')
    bricklet = device_factory.get(packet['device_id'], packet['uid'], ipcon)    # Create device object
    print('Identity:', await bricklet.get_identity())

    # Register the callback queue used by process_callbacks()
    # We can register the same queue for multiple callbacks.
    bricklet.register_event_queue(bricklet.CallbackID.TEMPERATURE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.TEMPERATURE_REACHED, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.RESISTANCE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.RESISTANCE_REACHED, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.SENSOR_CONNECTED, callback_queue)

    filter_settings = await bricklet.get_noise_rejection_filter()
    print('Noise rejection filter settings:', filter_settings)
    await bricklet.set_noise_rejection_filter(filter_settings)

    print('Is a sensor connected?', await bricklet.is_sensor_connected())

    print('Sensor type:', bricklet.sensor_type)
    bricklet.sensor_type = bricklet.SensorType.PT_100

    wire_mode = await bricklet.get_wire_mode()
    print('Wire mode:', wire_mode)
    await bricklet.set_wire_mode(wire_mode)

    print('PTC temperature:', await bricklet.get_temperature(), '°C')
    print('PTC resistance:', await bricklet.get_resistance(), 'Ω')

    # Use a temperature and resistance value callback
    print('Set callback period to', 1000, 'ms and wait for callbacks')
    await asyncio.gather(bricklet.set_temperature_callback_period(1000), bricklet.set_resistance_callback_period(1000), bricklet.set_sensor_connected_callback_configuration(True), bricklet.set_temperature_callback_threshold(option=bricklet.ThresholdOption.GREATER_THAN, minimum=0, maximum=0), bricklet.set_resistance_callback_threshold(option=bricklet.ThresholdOption.GREATER_THAN, minimum=10, maximum=0))

    print('Get temperature callback period:', await bricklet.get_temperature_callback_period())
    print('Get resistance callback period:', await bricklet.get_resistance_callback_period())
    print('Get sensor connected callback configuration:', await bricklet.get_sensor_connected_callback_configuration())

    debounce_period = await bricklet.get_debounce_period()
    print('Set bricklet debounce period to', debounce_period, 'ms')
    await bricklet.set_debounce_period(debounce_period)
    print('Get bricklet debounce period:', await bricklet.get_debounce_period())

    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disable callbacks')
    await asyncio.gather(bricklet.set_temperature_callback_period(), bricklet.set_resistance_callback_period(), bricklet.set_sensor_connected_callback_configuration(False), bricklet.set_temperature_callback_threshold(), bricklet.set_resistance_callback_threshold())

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
