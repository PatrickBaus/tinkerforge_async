#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
Barometer Bricklet 2.0.
"""
import asyncio
import logging
import warnings

from tinkerforge_async.ip_connection import IPConnectionAsync
from tinkerforge_async.device_factory import device_factory
from tinkerforge_async.brick_master import BrickMaster

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
            if packet['device_id'] is BrickMaster.DEVICE_IDENTIFIER:
                await run_example(packet, callback_queue)
    except asyncio.CancelledError:
        print('Enumeration queue canceled')


async def run_master_extension_chibi(brick):
    """
    This is the demo for the chibi extension
    """
    chibi_address = await brick.get_chibi_address()
    print('Chibi address:', chibi_address)
    await brick.set_chibi_address(chibi_address)

    chibi_address = await brick.get_chibi_master_address()
    print('Chibi master address:', chibi_address)
    await brick.set_chibi_master_address(chibi_address)

    chibi_addresses = await brick.get_slave_addresses()
    print('Chibi slave address:', chibi_addresses)
    await brick.set_chibi_slave_addresses(chibi_addresses)

    print('Chibi signal strength:', await brick.get_chibi_signal_strength())
    print('Chibi error log:', await brick.get_chibi_error_log())

    chibi_freq = await brick.get_chibi_frequency()
    print('Chibi frequency:', chibi_freq)
    await brick.set_chibi_frequency(chibi_freq)

    chibi_channel = await brick.get_chibi_channel()
    print('Chibi channel:', chibi_channel)
    await brick.set_chibi_channel(chibi_channel)


async def run_master_extension_rs485(brick):
    """
    This is the demo for the RS485 extension
    """
    config = await brick.get_rs485_configuration()
    print('RS-485 configuration:', config)
    new_config = config._asdict()
    new_config['speed'] = 1000000
    #await brick.set_rs485_configuration(**new_config)

    #await brick.set_rs485_address(0)   # 0 = brick
    print('RS-485 address:', await brick.get_rs485_address())

    #await brick.set_rs485_slave_addresses([42,])
    print('RS-485 slave addresses:', await brick.get_rs485_slave_addresses())

    print('RS-485 CRC error count:', await brick.get_rs485_error_log())


async def run_master_extension_wifi(brick):
    """
    This is the demo for the WIFI extension
    """
    config = await brick.get_wifi_configuration()
    print('WIFI config:', config)
    await brick.set_wifi_configuration(**config._asdict())

    wifi_encryption = await brick.get_wifi_encryption()
    print('WIFI encryption:', wifi_encryption)
    await brick.set_wifi_encryption(**wifi_encryption._asdict())
    #await master.set_long_wifi_key('foobar')

    print('WIFI Key (only FW <2.4.4): "{}"'.format(await brick.get_long_wifi_key()))

    wifi_power_mode = await brick.get_wifi_power_mode()
    print('WIFI power mode:', wifi_power_mode)
    await brick.set_wifi_power_mode(wifi_power_mode)

    print('WIFI buffer:', await brick.get_wifi_buffer_info())

    reg_domain = await brick.get_wifi_regulatory_domain()
    print('WIFI regulatory domain:', reg_domain)
    await brick.set_wifi_regulatory_domain(reg_domain)

    await brick.refresh_wifi_status()
    await asyncio.sleep(0.1)   # sleep a few ms to give the stack some time to update the wifi status
    wifi_status = await brick.get_wifi_status()
    new_status = wifi_status._asdict()
    # The mac and bssid are stored as tuples of int. We will replace them with the more common hex notation for
    # better readability, then we will recreate the named tuple.
    new_status['mac_address'] = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(*new_status['mac_address'])
    new_status['bssid'] = '{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}'.format(*new_status['bssid'])
    print('WIFI status:', type(wifi_status)(**new_status))

    hostname = await brick.get_wifi_hostname()
    print('WIFI Hostname:', hostname)
    await brick.set_wifi_hostname('hostname')

    #await brick.set_wifi_authentication_secret('')
    print('WIFI authentication secret: "{secret}"'.format(secret=await brick.get_wifi_authentication_secret()))

    #await brick.set_wpa_enterprise_username('user')
    #await brick.set_wpa_enterprise_password('password')
    print('WPA Enterprise username: "{user}"'.format(user=await brick.get_wpa_enterprise_username()))
    print('WPA Enterprise password: "{passwd}"'.format(passwd=await brick.get_wpa_enterprise_password()))


async def run_master_extension_ethernet(brick):
    """
    This is the demo for the ethernet extension
    """
    config = await brick.get_ethernet_configuration()
    print('Ethernet config:', config)
    await brick.set_ethernet_configuration(**config._asdict())

    await brick.set_ethernet_hostname('tinkerforge-testing')
    status = await brick.get_ethernet_status()
    print('Ethernet status:', status)

    await brick.set_ethernet_mac_address(status._asdict()['mac_address'])

    await brick.set_ethernet_websocket_configuration(sockets=3, port=4280)
    config_websocket = await brick.get_ethernet_websocket_configuration()
    print('Websocket config:', config_websocket)

    #await brick.set_ethernet_authentication_secret('')
    print('Ethernet authentication secret: "{secret}"'.format(secret=await brick.get_ethernet_authentication_secret()))


async def run_master_extension_wifi2(brick):
    """
    This is the demo for the WIFI 2.0 extension
    """
    print('WIFI 2.0 firmware version:', await brick.get_wifi2_firmware_version())
    led_status = await brick.is_wifi2_status_led_enabled()
    print('WIFI 2.0 status led enabled?', led_status)
    print('Flashing WIFI 2.0 status led')
    await brick.set_wifi2_status_led(not led_status)
    await asyncio.sleep(1)
    await brick.set_wifi2_status_led(led_status)
    print('WIFI 2.0 status led enabled?', await brick.is_wifi2_status_led_enabled())

    config = await brick.get_wifi2_configuration()
    print('WIFI 2.0 config:', config)
    new_config = config._asdict()
    #new_config["website"] = True
    await brick.set_wifi2_configuration(**new_config)
    print('New WIFI 2.0 config:', await brick.get_wifi2_configuration())

    print('WIFI 2.0 status:', await brick.get_wifi2_status())
    config = await brick.get_wifi2_client_configuration()
    print('WIFI 2.0 client configuration:', config)
    new_config = config._asdict()
    #new_config["ip"] = (0,0,0,0)    # Set to DHCP
    await brick.set_wifi2_client_configuration(**new_config)
    print('New WIFI 2.0 client configuration:', await brick.get_wifi2_client_configuration())

    client_hostname = await brick.get_wifi2_client_hostname()
    print('WIFI 2.0 client hostname:', client_hostname)
    #await brick.set_wifi2_client_hostname()    # Reset hostname

    #await brick.set_wifi2_client_password('foo')
    print('WIFI 2.0 client password:', await brick.get_wifi2_client_password())

    config = await brick.get_wifi2_ap_configuration()
    print('WIFI 2.0 AP configuration:', config)
    new_config = config._asdict()
    #new_config["enable"] = False
    await brick.set_wifi2_ap_configuration(**new_config)

    #await brick.set_wifi2_ap_password('foobar')
    print('WIFI 2.0 AP password:', await brick.get_wifi2_ap_password())

    config = await brick.get_wifi2_mesh_configuration()
    print('WIFI 2.0 Mesh configuration:', config)
    new_config = config._asdict()
    #new_config['group_id'] = (26, 254, 52, 0, 0, 0)
    await brick.set_wifi2_mesh_configuration(**new_config)

    print('WIFI 2.0 Mesh SSID:', await brick.get_wifi2_mesh_router_ssid())
    #await brick.set_wifi2_mesh_router_ssid('Your Access Point')

    print('WIFI 2.0 mesh router password:', await brick.get_wifi2_mesh_router_password())
    #await brick.set_wifi2_mesh_router_password('foo')

    print('WIFI 2.0 mesh common status:', await brick.get_wifi2_mesh_common_status())
    print('WIFI 2.0 mesh client status:', await brick.get_wifi2_mesh_client_status())
    print('WIFI 2.0 mesh AP status:', await brick.get_wifi2_mesh_ap_status())

    #await brick.set_wifi2_authentication_secret('')    # disable authentication
    print('WIFI 2.0 authentication secret:', await brick.get_wifi2_authentication_secret())

    #await brick.save_wifi2_configuration()

async def run_example(packet, callback_queue):
    """
    This is the actual demo. If the brick is found, this code will be run.
    """
    print('Registering master brick')
    master = device_factory.get(packet['device_id'], packet['uid'], ipcon)
    print('Identity:', await master.get_identity())

    debounce_period = await master.get_debounce_period()
    print('Debounce period:', debounce_period, 'ms')
    await master.set_debounce_period(debounce_period)

    print('Connection type used to control Brick:', await master.get_connection_type())

    print('USB voltage:  ', await master.get_usb_voltage(), 'V')
    print('Stack voltage:', await master.get_stack_voltage(), 'V')
    print('Stack current:', await master.get_stack_current(), 'A')
    print('Chip temperature:', await master.get_chip_temperature(), '°C')

    print('##################\nCallbacks:')
    master.register_event_queue(master.CallbackID.STACK_CURRENT, callback_queue)
    master.register_event_queue(master.CallbackID.STACK_VOLTAGE, callback_queue)
    master.register_event_queue(master.CallbackID.USB_VOLTAGE, callback_queue)
    await asyncio.gather(
        master.set_usb_voltage_callback_period(100),
        master.set_stack_voltage_callback_period(110),
        master.set_stack_current_callback_period(120),
        master.set_usb_voltage_callback_threshold(master.ThresholdOption.OFF, 0, 0),
        master.set_stack_voltage_callback_threshold(master.ThresholdOption.OFF, 0, 0),
        master.set_stack_current_callback_threshold(master.ThresholdOption.OFF, 0, 0),
    )
    print('USB voltage callback period:  ', await master.get_usb_voltage_callback_period(), 'ms')
    print('Stack voltage callback period:', await master.get_stack_voltage_callback_period(), 'ms')
    print('Stack current callback period:', await master.get_stack_current_callback_period(), 'ms')
    print('USB voltage callback threshold:  ', await master.get_usb_voltage_callback_threshold())
    print('Stack voltage callback threshold:', await master.get_stack_voltage_callback_threshold())
    print('Stack current callback threshold:', await master.get_stack_current_callback_threshold())
    print('Waiting 1 second for callbacks...')
    await asyncio.sleep(1)
    await asyncio.gather(
        master.set_usb_voltage_callback_period(0),
        master.set_stack_voltage_callback_period(0),
        master.set_stack_current_callback_period(0)
    )
    print('##################\nExtensions:')
    if await master.is_chibi_present():
        await run_master_extension_chibi(master)

    if await master.is_rs485_present():
        await run_master_extension_rs485(master)

    if await master.is_wifi_present():
        await run_master_extension_wifi(master)

    if await master.is_ethernet_present():
        await run_master_extension_ethernet(master)

    if await master.is_wifi2_present():
        await run_master_extension_wifi2(master)

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
