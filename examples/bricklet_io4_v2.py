#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
IO-4 Bricklet 2.0.
"""
import asyncio
import logging
import warnings

from TinkerforgeAsync.ip_connection import IPConnectionAsync
from TinkerforgeAsync.device_factory import device_factory
from TinkerforgeAsync.bricklet_io4_v2 import BrickletIO4V2

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
            if packet['device_id'] is BrickletIO4V2.DEVICE_IDENTIFIER:
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
    bricklet.register_event_queue(bricklet.CallbackID.INPUT_VALUE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.ALL_INPUT_VALUE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.MONOFLOP_DONE, callback_queue)

    print('Setting all channels to INPUT and floating them')
    await asyncio.gather(*[bricklet.set_configuration(channel=channel, direction=bricklet.Direction.IN, value=False) for channel in range(4)])  # Set all pins to inputs with pull ups
    await asyncio.sleep(0.01)
    print('Input values:', await bricklet.get_value())
    channel_configs = await asyncio.gather(*[bricklet.get_configuration(channel=channel) for channel in range(4)])
    print('Channel configs:\n', *[f"{i}: {channel}\n" for i, channel in enumerate(channel_configs)])
    print('Setting all channels to OUTPUT and driving them HIGH')
    await asyncio.gather(*[bricklet.set_configuration(channel=channel, direction=bricklet.Direction.OUT, value=True) for channel in range(4)])  # Set all pins to inputs with pull ups
    await asyncio.sleep(0.01)
    print('Output values:', await bricklet.get_value())
    channel_configs = await asyncio.gather(*[bricklet.get_configuration(channel=channel) for channel in range(4)])
    print('Channel configs:\n', *[f"{i}: {channel}\n" for i, channel in enumerate(channel_configs)])

    print('Driving all channels LOW')
    await bricklet.set_value((False, False, False, False))
    print('Output values:', await bricklet.get_value())
    print('Driving all channel 1 HIGH')
    await bricklet.set_selected_value(1, True)
    print('Output values:', await bricklet.get_value())

    print('Enabling monoflop, going HIGH for 1 second')
    await bricklet.set_monoflop(0, True, 1000)
    print('Monoflop status:', await bricklet.get_monoflop(0))
    await asyncio.sleep(1)

    print('Triggering error, because we want to enable Edgecount on an output')
    try:
        await bricklet.set_edge_count_configuration(channel=2, edge_type=bricklet.EdgeType.RISING, debounce=1)
    except ValueError:
        print('Got a ValueError.')

    print('Enabling input callbacks on channel 2')
    await asyncio.gather(*[bricklet.set_configuration(channel=channel, direction=bricklet.Direction.IN, value=False) for channel in range(4)])  # Set all pins to inputs with pull ups
    await bricklet.set_input_value_callback_configuration(channel=2, period=100, value_has_to_change=False)
    print('Callback configuration for channel 2:', await bricklet.get_input_value_callback_configuration(2))
    await bricklet.set_all_input_value_callback_configuration(period=100, value_has_to_change=False)
    print('Callback configuration for all inputs:', await bricklet.get_all_input_value_callback_configuration())
    await asyncio.sleep(0.5)
    await bricklet.set_input_value_callback_configuration(channel=2, period=100, value_has_to_change=True)
    await bricklet.set_all_input_value_callback_configuration(period=100, value_has_to_change=True)

    print('Enabling edgecount on channel 2')
    await bricklet.set_edge_count_configuration(channel=2, edge_type=bricklet.EdgeType.BOTH, debounce=1)
    print('Edgecount config:', await bricklet.get_edge_count_configuration(2))
    print('Toggling channel 2')
    await bricklet.set_configuration(channel=2, direction=bricklet.Direction.IN, value=True)
    await bricklet.set_configuration(channel=2, direction=bricklet.Direction.IN, value=False)
    await asyncio.sleep(0.1)
    print('Edges:', await bricklet.get_edge_count(2))

    print('Enabling PWM on channel 3')
    await bricklet.set_configuration(channel=3, direction=bricklet.Direction.OUT, value=False)
    await bricklet.set_pwm_configuration(channel=3, frequency=10, duty_cycle=0.5)
    print('PWM configuration:', await bricklet.get_pwm_configuration(3))
    await asyncio.sleep(1)

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
