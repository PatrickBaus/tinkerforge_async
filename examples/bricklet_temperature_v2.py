#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import warnings

from source.ip_connection import IPConnectionAsync
from source.devices import DeviceIdentifier
from source.bricklet_temperature_v2 import BrickletTemperatureV2

loop = asyncio.get_event_loop()
ipcon = IPConnectionAsync(loop=loop)
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
            if packet['device_id'] is DeviceIdentifier.BrickletTemperatureV2:
                await run_example(packet)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')

def error_handler(task):
    try:
      task.result()
    except Exception:
      asyncio.ensure_future(stop_loop())

async def run_example(packet):
    print('Registering temperature bricklet 2.0')
    bricklet = BrickletTemperatureV2(packet['uid'], ipcon) # Create device object
    print('Identity:', await bricklet.get_identity())

    uid = await bricklet.read_uid()
    print('Device uid:', uid)
    await bricklet.write_uid(uid)

    # Register the callback queue used by process_callbacks()
    # We can register the same queue for multiple callbacks.
    bricklet.register_event_queue(BrickletTemperatureV2.CallbackID.temperature, callback_queue)

    # Query the value
    print('Get temperature:', await bricklet.get_temperature())
    print('Set callback period to', 1000, 'ms')
    print('Set threshold to >10 °C and wait for callbacks')
    # We use a low temperature value on purpose, so that the callback will be triggered
    await bricklet.set_temperature_callback_configuration(1000, False, bricklet.ThresholdOption.greater_than, 10, 0)
    print('Temperature callback configuration:', await bricklet.get_temperature_callback_configuration())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disable threshold callback')
    await bricklet.set_temperature_callback_configuration()
    print('Temperature callback configuration:', await bricklet.get_temperature_callback_configuration())

    print('Enabling heater')
    await bricklet.set_heater_configuration(bricklet.HeaterConfig.enabled)
    print('Heater config:', await bricklet.get_heater_configuration())
    print('Disabling heater')
    await bricklet.set_heater_configuration()
    print('Heater config:', await bricklet.get_heater_configuration())

    print('SPI error count:', await bricklet.get_spitfp_error_count())
    
    print('Current bootloader mode:', await bricklet.get_bootloader_mode())
    bootloader_mode = bricklet.BootloaderMode.firmware
    print('Setting bootloader mode to', bootloader_mode, ':', await bricklet.set_bootloader_mode(bootloader_mode))

    print('Disable status LED')
    await bricklet.set_status_led_config(bricklet.LedConfig.off)
    print('Current status:', await bricklet.get_status_led_config())
    await asyncio.sleep(1)
    print('Enable status LED')
    await bricklet.set_status_led_config(bricklet.LedConfig.show_status)
    print('Current status:', await bricklet.get_status_led_config())

    print('Get Chip temperature:', await bricklet.get_chip_temperature())

    print('Reset Bricklet')
    await bricklet.reset()

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
