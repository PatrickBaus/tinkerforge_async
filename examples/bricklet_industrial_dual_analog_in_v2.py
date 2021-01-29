#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import sys
sys.path.append("..") # Adds higher directory to python modules path.
import warnings

from source.ip_connection import IPConnectionAsync
from source.devices import DeviceIdentifier
from source.device_factory import device_factory
from source.bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2

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
            if packet['device_id'] is BrickletIndustrialDualAnalogInV2.DEVICE_IDENTIFIER:
                await run_example(packet)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')

async def run_example(packet):
    print('Registering Industrial Dual Analog In bricklet 2.0')
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

    print('Get chip temperature:', await bricklet.get_chip_temperature(), '°C')

    # Register the callback queue used by process_callbacks()
    # We can register the same queue for multiple callbacks.
    bricklet.register_event_queue(bricklet.CallbackID.VOLTAGE, callback_queue)
    bricklet.register_event_queue(bricklet.CallbackID.ALL_VOLTAGES, callback_queue)

    await bricklet.set_sample_rate(bricklet.SamplingRate.RATE_1_SPS)
    print('Sampling rate:', await bricklet.get_sample_rate())

    cal_data = await bricklet.get_calibration()
    print('Calibration data:', cal_data)
    await bricklet.set_calibration(**cal_data._asdict())
    print('ADC raw values (with offset subtracted):', await bricklet.get_adc_values())

    # Query LEDs
    print('Channel 0 led config:', await bricklet.get_channel_led_config(0))
    print('Channel 1 led config:', await bricklet.get_channel_led_config(1))
    led_status_config = await bricklet.get_channel_led_status_config(0)
    print('Channel 0 led status config', led_status_config)
    await bricklet.set_channel_led_status_config(0, **led_status_config._asdict())
    led_status_config = await bricklet.get_channel_led_status_config(1)
    print('Channel 1 led status config', led_status_config)
    led_status_config = led_status_config._asdict()
    led_status_config['config'] = led_status_config['config'].value   # convert to int. Both int and enum work
    await bricklet.set_channel_led_status_config(1, **led_status_config)

    print('Setting channel leds to heartbeat')
    await bricklet.set_channel_led_config(0, bricklet.ChannelLedConfig.HEARTBEAT)
    await bricklet.set_channel_led_config(1, bricklet.ChannelLedConfig.HEARTBEAT)

    # Query a value
    print('Get voltage, channel 0:', await bricklet.get_voltage(0), 'V')
    print('Get voltage, channel 1:', await bricklet.get_voltage(1), 'V')

    # Use a voltage value callback
    print('Set callback period to', 1000, 'ms and wait for callbacks')
    await bricklet.set_voltage_callback_configuration(channel=0, period=1000)
    await bricklet.set_voltage_callback_configuration(channel=1, period=500)
    print('Voltage callback config, channel 0:', await bricklet.get_voltage_callback_configuration(0))
    print('Voltage callback config, channel 1:', await bricklet.get_voltage_callback_configuration(1))
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disable callbacks')
    await bricklet.set_voltage_callback_configuration(0)
    await bricklet.set_voltage_callback_configuration(1)
    print('Voltage callback config, channel 0:', await bricklet.get_voltage_callback_configuration(0))
    print('Voltage callback config, channel 1:', await bricklet.get_voltage_callback_configuration(1))

    # Use all voltages callback
    print('Get all voltages:', await bricklet.get_all_voltages())

    await bricklet.set_all_voltages_callback_configuration(period=1000)
    print('All voltages callback config:', await bricklet.get_all_voltages_callback_configuration())
    await asyncio.sleep(2.1)    # Wait for 2-3 callbacks
    print('Disable callback')
    await bricklet.set_all_voltages_callback_configuration()
    print('All voltages callback config:', await bricklet.get_all_voltages_callback_configuration())

    print('Resetting channel leds to status')
    await bricklet.set_channel_led_config(0, bricklet.ChannelLedConfig.CHANNEL_STATUS)
    await bricklet.set_channel_led_config(1, bricklet.ChannelLedConfig.CHANNEL_STATUS)

    print('Reset Bricklet')
    await bricklet.reset()

    # Terminate the loop
    asyncio.create_task(stop_loop())

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
      asyncio.create_task(stop_loop())

async def main():
    try: 
        await ipcon.connect(host='127.0.0.1', port=4223)
        #await ipcon.connect(host='10.0.0.5', port=4223)
        running_tasks.append(asyncio.create_task(process_callbacks()))
        running_tasks[-1].add_done_callback(error_handler)  # Add error handler to catch exceptions
        running_tasks.append(asyncio.create_task(process_enumerations()))
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
