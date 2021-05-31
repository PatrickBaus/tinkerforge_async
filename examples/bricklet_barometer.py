#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
Barometer Bricklet.
"""
import asyncio
import logging
import warnings

from TinkerforgeAsync.ip_connection import IPConnectionAsync
from TinkerforgeAsync.device_factory import device_factory
from TinkerforgeAsync.bricklet_barometer import BrickletBarometer

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
            if packet['device_id'] is BrickletBarometer.DEVICE_IDENTIFIER:
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

    print('Get chip temperature:', await bricklet.get_chip_temperature(), '°C')

    # Register the callback queue used by process_callbacks()
    # We can register the same queue for multiple callbacks.
    bricklet.register_event_queue(bricklet.CallbackID.AIR_PRESSURE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.ALTITUDE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.AIR_PRESSURE_REACHED, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.ALTITUDE_REACHED, callback_queue)

    print('Air pressure:', await bricklet.get_air_pressure(), 'Pa')
    print('Altidtude:', await bricklet.get_altitude(), 'm')

    reference_pressure = await bricklet.get_reference_air_pressure()
    print('Reference air pressure:', reference_pressure, 'Pa')
    await bricklet.set_reference_air_pressure()

    averageing_config = await bricklet.get_averaging()
    print('Averageing config:', averageing_config)
    await bricklet.set_averaging(**averageing_config._asdict())

    print('Set callback period to', 1000, 'ms')
    await asyncio.gather(bricklet.set_air_pressure_callback_period(1000), bricklet.set_altitude_callback_period(1000))
    print('Air pressure callback period:', await bricklet.get_air_pressure_callback_period())
    print('Altidtude callback period:', await bricklet.get_altitude_callback_period())
    print('Set bricklet debounce period to', 1000, 'ms')
    await bricklet.set_debounce_period(1000)
    print('Get bricklet debounce period:', await bricklet.get_debounce_period())

    # Use an air pressure and altitude callback
    print('Set air pressure threshold to >10 Pa and altitude to > 1m and wait for callbacks')
    # We use a low humidity on purpose, so that the callback will be triggered
    await asyncio.gather(bricklet.set_air_pressure_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 10, 0), bricklet.set_altitude_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 1, 0))
    print('Air pressure threshold:', await bricklet.get_air_pressure_callback_threshold())
    print('Altidtude threshold:', await bricklet.get_altitude_callback_threshold())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disabling threshold callback')
    await asyncio.gather(bricklet.set_air_pressure_callback_threshold(), bricklet.set_altitude_callback_threshold())
    print('Air pressure threshold:', await bricklet.get_air_pressure_callback_threshold())
    print('Altidtude threshold:', await bricklet.get_altitude_callback_threshold())

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
