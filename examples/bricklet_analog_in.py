#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
Analog In Bricklet.
"""
import asyncio
import logging
import warnings

from TinkerforgeAsync.ip_connection import IPConnectionAsync
from TinkerforgeAsync.device_factory import device_factory
from TinkerforgeAsync.bricklet_analog_in import BrickletAnalogIn

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
            if packet['device_id'] is BrickletAnalogIn.DEVICE_IDENTIFIER:
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
    bricklet.register_event_queue(bricklet.CallbackID.VOLTAGE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.ANALOG_VALUE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.VOLTAGE_REACHED, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.ANALOG_VALUE_REACHED, callback_queue)

    voltage_range = await bricklet.get_range()
    print('Range:', voltage_range)
    await bricklet.set_range(voltage_range)

    averaging = await bricklet.get_averaging()
    print('Averaging:', averaging)
    await bricklet.set_averaging(averaging)

    # Query a value
    print('Get voltage:', await bricklet.get_voltage(), 'V')
    print('Analog value:', await bricklet.get_analog_value())

    print('Set bricklet debounce period to', 1000, 'ms')
    await bricklet.set_debounce_period(1000)
    print('Get bricklet debounce period:', await bricklet.get_debounce_period())

    # Use a voltage callback
    print('Set voltage callback period to', 1000, 'ms')
    await bricklet.set_voltage_callback_period(1000)
    print('Voltage callback period:', await bricklet.get_voltage_callback_period())

    print('Set voltage threshold to > 1 mV and wait for callbacks')
    # We use a low voltage on purpose, so that the callback will be triggered
    await bricklet.set_voltage_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 0.001, 0)
    print('Voltage threshold:', await bricklet.get_voltage_callback_threshold())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disabling threshold callback')
    await asyncio.gather(bricklet.set_voltage_callback_threshold(), bricklet.set_voltage_callback_period())
    print('Voltage threshold:', await bricklet.get_voltage_callback_threshold())
    print('Voltage callback period:', await bricklet.get_voltage_callback_period())

    # Use an analog value callback
    print('Set analog value callback period to', 1000, 'ms')
    await bricklet.set_analog_value_callback_period(1000)
    print('Analog value callback period:', await bricklet.get_analog_value_callback_period())

    print('Set analog value threshold to > 0 and wait for callbacks')
    await bricklet.set_analog_value_callback_threshold(bricklet.ThresholdOption.GREATER_THAN, 0, 0)
    print('Analog value threshold:', await bricklet.get_analog_value_callback_threshold())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disabling threshold callback')
    await bricklet.set_analog_value_callback_threshold()
    print('Analog value threshold:', await bricklet.get_analog_value_callback_threshold())

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
