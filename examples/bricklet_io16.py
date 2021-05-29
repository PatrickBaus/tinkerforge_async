#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
import warnings

from source.ip_connection import IPConnectionAsync
from source.device_factory import device_factory
from source.bricklet_io16 import BrickletIO16

sys.path.append("..")   # Adds higher directory to python modules path.

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
            if packet['device_id'] is BrickletIO16.DEVICE_IDENTIFIER:
                await run_example(packet, callback_queue)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')


async def run_example(packet, callback_queue):
    print('Registering bricklet')
    bricklet = device_factory.get(packet['device_id'], packet['uid'], ipcon)    # Create device object
    print('Identity:', await bricklet.get_identity())
    # Register the callback queue used by process_callbacks()
    # We can register the same queue for multiple callbacks.
    bricklet.register_event_queue(bricklet.CallbackID.INTERRUPT, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.MONOFLOP_DONE, callback_queue)

    port_a = await bricklet.get_port(bricklet.Port.A)   # or 'a' or 'A'
    port_b = await bricklet.get_port('b')
    print('Port A:', '{0:08b}'.format(port_a))
    print('Port B:', '{0:08b}'.format(port_b))
    await asyncio.gather(bricklet.set_port('A', port_a), bricklet.set_port('B', port_b))

    print('Port A configuration:', await bricklet.get_port_configuration('A'))
    print('Port B configuration:', await bricklet.get_port_configuration('B'))
    await bricklet.set_port_configuration('A', 0b11111111, bricklet.Direction.IN, bricklet.InputConfiguration.PULL_UP)    # Set all pins to inputs with pull ups
    await bricklet.set_port_configuration('B', 0b11111111, bricklet.Direction.OUT, bricklet.OutputConfiguration.LOW)    # Set all pins to outputs with LOW values

    print('Set bricklet debounce period to', 10, 'ms')
    await bricklet.set_debounce_period(10)
    print('Get bricklet debounce period:', await bricklet.get_debounce_period())

    port_a = await bricklet.get_port_interrupt('A')
    port_b = await bricklet.get_port_interrupt('B')
    print('Port A interrupts:', '{0:08b}'.format(port_a))
    print('Port B interrupts:', '{0:08b}'.format(port_b))

    print('Enable interrupts on port A')
    await bricklet.set_port_interrupt('A', 0b11111111)
    print('Port interrupts:', '{0:08b}'.format(await bricklet.get_port_interrupt('A')))
    print('Wait for interrupts. Connect a few outputs from port B to port A.')
    await asyncio.sleep(5)

    print('Enabling monoflop on B0 and B3. A0 will be high and B3 low until the time runs out, then B0 will go low and B3 high. Like a dead man\'s switch')
    await bricklet.set_port_monoflop('B', 0b00001001, 0b00000001, 3000)
    print('Monoflop state:')
    for i in range(3):
        print('B0: {0}, B3: {1}'.format(*(await asyncio.gather(bricklet.get_port_monoflop('B', 0), bricklet.get_port_monoflop('B', 3)))))
        await asyncio.sleep(1)

    print('Setting B3 low.')
    await bricklet.set_selected_values('B', 0b00001000, 0b00000000)
    await asyncio.sleep(0.1)

    print('Enabling edge counting on A0. Connect pin B7 to A0.')
    await bricklet.set_selected_values('B', 0b10000000, 0b10000000)   # Set B7 to high, because toggling starts by going low.
    await bricklet.set_edge_count_config(0, bricklet.EdgeType.BOTH, debounce=5)
    print('Edge count config A0:', await bricklet.get_edge_count_config(0))
    print('Edge count config A1:', await bricklet.get_edge_count_config(1))

    print('Toggling pin B7.')
    for i in range(10):
        print('Setting pin', 'HIGH.' if (i % 2) else 'LOW.')
        await bricklet.set_selected_values('B', 0b10000000, 0b10000000 & ((i % 2) << 7))
        print('Edge count of A0:', await bricklet.get_edge_count(0))
        await asyncio.sleep(0.01)

    print('Disabling interrupts.')
    await bricklet.set_port_interrupt('A', 0b00000000)

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
        # Normally we should log these
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
asyncio.run(main(), debug=True)
