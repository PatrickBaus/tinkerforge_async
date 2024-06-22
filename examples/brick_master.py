#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge Master brick.
"""
import asyncio
import warnings
from decimal import Decimal

from tinkerforge_async.brick_master import BrickMaster
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickMaster) -> None:
    """Prints the callbacks (filtered by id) of the bricklet"""
    async for packet in device.read_events():
        print("Callback received", packet)


async def run_master_extension_chibi(brick: BrickMaster) -> None:
    """This is the demo for the chibi extension"""
    chibi_address = await brick.get_chibi_address()
    print("Chibi address:", chibi_address)
    await brick.set_chibi_address(chibi_address)

    chibi_address = await brick.get_chibi_master_address()
    print("Chibi master address:", chibi_address)
    await brick.set_chibi_master_address(chibi_address)

    chibi_addresses = await brick.get_slave_addresses()
    print("Chibi slave address:", chibi_addresses)
    await brick.set_chibi_slave_addresses(chibi_addresses)

    print("Chibi signal strength:", await brick.get_chibi_signal_strength())
    print("Chibi error log:", await brick.get_chibi_error_log())

    chibi_freq = await brick.get_chibi_frequency()
    print("Chibi frequency:", chibi_freq)
    await brick.set_chibi_frequency(chibi_freq)

    chibi_channel = await brick.get_chibi_channel()
    print("Chibi channel:", chibi_channel)
    await brick.set_chibi_channel(chibi_channel)


async def run_master_extension_rs485(brick: BrickMaster) -> None:
    """This is the demo for the RS485 extension"""
    config = await brick.get_rs485_configuration()
    print("RS-485 configuration:", config)
    new_config = config._asdict()
    new_config["speed"] = 1000000
    # await brick.set_rs485_configuration(**new_config)

    # await brick.set_rs485_address(0)   # 0 = brick
    print("RS-485 address:", await brick.get_rs485_address())

    # await brick.set_rs485_slave_addresses([42,])
    print("RS-485 slave addresses:", await brick.get_rs485_slave_addresses())

    print("RS-485 CRC error count:", await brick.get_rs485_error_log())


async def run_master_extension_wifi(brick: BrickMaster) -> None:
    """This is the demo for the Wi-Fi extension"""
    config = await brick.get_wifi_configuration()
    print("WIFI config:", config)
    await brick.set_wifi_configuration(**config._asdict())

    wifi_encryption = await brick.get_wifi_encryption()
    print("WIFI encryption:", wifi_encryption)
    await brick.set_wifi_encryption(**wifi_encryption._asdict())
    # await master.set_long_wifi_key('foobar')

    print(f"WIFI Key (only FW <2.4.4): '{await brick.get_long_wifi_key()!r}'")

    wifi_power_mode = await brick.get_wifi_power_mode()
    print("WIFI power mode:", wifi_power_mode)
    await brick.set_wifi_power_mode(wifi_power_mode)

    print("WIFI buffer:", await brick.get_wifi_buffer_info())

    reg_domain = await brick.get_wifi_regulatory_domain()
    print("WIFI regulatory domain:", reg_domain)
    await brick.set_wifi_regulatory_domain(reg_domain)

    await brick.refresh_wifi_status()
    await asyncio.sleep(0.1)  # sleep a few ms to give the stack some time to update the wifi status
    wifi_status = await brick.get_wifi_status()
    new_status = wifi_status._asdict()
    # The mac and bssid are stored as tuples of int. We will replace them with the more common hex notation for
    # better readability, then we will recreate the named tuple.
    new_status["mac_address"] = []
    new_status["mac_address"] = (
        "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(  # pylint: disable=consider-using-f-string
            *new_status["mac_address"]
        )
    )
    new_status["bssid"] = "{:02x}:{:02x}:{:02x}:{:02x}:{:02x}:{:02x}".format(  # pylint: disable=consider-using-f-string
        *new_status["bssid"]
    )
    print("WIFI status:", type(wifi_status)(**new_status))

    hostname = await brick.get_wifi_hostname()
    print("WIFI Hostname:", hostname)
    await brick.set_wifi_hostname("hostname")

    # await brick.set_wifi_authentication_secret('')
    print(f"WIFI authentication secret: '{await brick.get_wifi_authentication_secret()!r}'")

    # await brick.set_wpa_enterprise_username('user')
    # await brick.set_wpa_enterprise_password('password')
    print(f"WPA Enterprise username: '{await brick.get_wpa_enterprise_username()!r}'")
    print(f"WPA Enterprise password: '{await brick.get_wpa_enterprise_password()!r}'")


async def run_master_extension_ethernet(brick: BrickMaster) -> None:
    """This is the demo for the ethernet extension"""
    config = await brick.get_ethernet_configuration()
    print("Ethernet config:", config)
    await brick.set_ethernet_configuration(**config._asdict())

    await brick.set_ethernet_hostname("tinkerforge-testing")
    status = await brick.get_ethernet_status()
    print("Ethernet status:", status)

    await brick.set_ethernet_mac_address(status._asdict()["mac_address"])

    await brick.set_ethernet_websocket_configuration(sockets=3, port=4280)
    config_websocket = await brick.get_ethernet_websocket_configuration()
    print("Websocket config:", config_websocket)

    # await brick.set_ethernet_authentication_secret('')
    print(f"Ethernet authentication secret: '{await brick.get_ethernet_authentication_secret()!r}'")


async def run_master_extension_wifi2(brick: BrickMaster) -> None:
    """This is the demo for the Wi-Fi 2.0 extension"""
    print("WIFI 2.0 firmware version:", await brick.get_wifi2_firmware_version())
    led_status = await brick.is_wifi2_status_led_enabled()
    print("WIFI 2.0 status led enabled?", led_status)
    print("Flashing WIFI 2.0 status led")
    await brick.set_wifi2_status_led(not led_status)
    await asyncio.sleep(1)
    await brick.set_wifi2_status_led(led_status)
    print("WIFI 2.0 status led enabled?", await brick.is_wifi2_status_led_enabled())

    config_wifi = await brick.get_wifi2_configuration()
    print("WIFI 2.0 config:", config_wifi)
    new_config = config_wifi._asdict()
    # new_config["website"] = True
    await brick.set_wifi2_configuration(**new_config)
    print("New WIFI 2.0 config:", await brick.get_wifi2_configuration())

    print("WIFI 2.0 status:", await brick.get_wifi2_status())
    config_client = await brick.get_wifi2_client_configuration()
    print("WIFI 2.0 client configuration:", config_client)
    new_config = config_client._asdict()
    # new_config["ip"] = (0,0,0,0)    # Set to DHCP
    await brick.set_wifi2_client_configuration(**new_config)
    print("New WIFI 2.0 client configuration:", await brick.get_wifi2_client_configuration())

    client_hostname = await brick.get_wifi2_client_hostname()
    print("WIFI 2.0 client hostname:", client_hostname)
    # await brick.set_wifi2_client_hostname()    # Reset hostname

    # await brick.set_wifi2_client_password('foo')
    print("WIFI 2.0 client password:", await brick.get_wifi2_client_password())

    config_ap = await brick.get_wifi2_ap_configuration()
    print("WIFI 2.0 AP configuration:", config_ap)
    new_config = config_ap._asdict()
    # new_config["enable"] = False
    await brick.set_wifi2_ap_configuration(**new_config)

    # await brick.set_wifi2_ap_password('foobar')
    print("WIFI 2.0 AP password:", await brick.get_wifi2_ap_password())

    config_mesh = await brick.get_wifi2_mesh_configuration()
    print("WIFI 2.0 Mesh configuration:", config_mesh)
    new_config = config_mesh._asdict()
    # new_config['group_id'] = (26, 254, 52, 0, 0, 0)
    await brick.set_wifi2_mesh_configuration(**new_config)

    print("WIFI 2.0 Mesh SSID:", await brick.get_wifi2_mesh_router_ssid())
    # await brick.set_wifi2_mesh_router_ssid('Your Access Point')

    print("WIFI 2.0 mesh router password:", await brick.get_wifi2_mesh_router_password())
    # await brick.set_wifi2_mesh_router_password('foo')

    print("WIFI 2.0 mesh common status:", await brick.get_wifi2_mesh_common_status())
    print("WIFI 2.0 mesh client status:", await brick.get_wifi2_mesh_client_status())
    print("WIFI 2.0 mesh AP status:", await brick.get_wifi2_mesh_ap_status())

    # await brick.set_wifi2_authentication_secret('')    # disable authentication
    print("WIFI 2.0 authentication secret:", await brick.get_wifi2_authentication_secret())

    # await brick.save_wifi2_configuration()


async def run_example(master: BrickMaster) -> None:
    """This is the actual demo. If the brick is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(master))
    try:
        print("Identity:", await master.get_identity())

        debounce_period = await master.get_debounce_period()
        print("Debounce period:", debounce_period, "ms")
        await master.set_debounce_period(debounce_period)

        print("Connection type used to control Brick:", await master.get_connection_type())

        print("USB voltage:  ", await master.get_usb_voltage(), "V")
        print("Stack voltage:", await master.get_stack_voltage(), "V")
        print("Stack current:", await master.get_stack_current(), "A")
        print("Chip temperature:", await master.get_chip_temperature() - Decimal("273.15"), "°C")

        print("##################\nCallbacks:")
        await asyncio.gather(
            master.set_usb_voltage_callback_period(100),
            master.set_stack_voltage_callback_period(110),
            master.set_stack_current_callback_period(120),
            master.set_usb_voltage_callback_threshold(master.ThresholdOption.OFF, 0, 0),
            master.set_stack_voltage_callback_threshold(master.ThresholdOption.OFF, 0, 0),
            master.set_stack_current_callback_threshold(master.ThresholdOption.OFF, 0, 0),
        )
        print("USB voltage callback period:  ", await master.get_usb_voltage_callback_period(), "ms")
        print("Stack voltage callback period:", await master.get_stack_voltage_callback_period(), "ms")
        print("Stack current callback period:", await master.get_stack_current_callback_period(), "ms")
        print("USB voltage callback threshold:  ", await master.get_usb_voltage_callback_threshold())
        print("Stack voltage callback threshold:", await master.get_stack_voltage_callback_threshold())
        print("Stack current callback threshold:", await master.get_stack_current_callback_threshold())
        print("Waiting 1 second for callbacks...")
        await asyncio.sleep(1)
        await asyncio.gather(
            master.set_usb_voltage_callback_period(0),
            master.set_stack_voltage_callback_period(0),
            master.set_stack_current_callback_period(0),
        )
        print("##################\nExtensions:")
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

    finally:
        callback_task.cancel()


async def shutdown(tasks: set[asyncio.Task]) -> None:
    """Clean up by stopping all consumers"""
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks)


async def main() -> None:
    """
    The main loop, that will spawn all callback handlers and wait until they are
    done. There are two callback handlers, one waits for the bricklet to connect
    and run the demo, the other handles messages sent by the bricklet.
    """
    tasks = set()
    try:
        # Use the context manager of the ip connection. It will automatically do the cleanup.
        async with IPConnectionAsync(host="10.0.0.5", port=4223) as connection:
            await connection.enumerate()
            # Read all enumeration replies, then start the example if we find the correct device
            async for enumeration_type, device in connection.read_enumeration():  # pylint: disable=unused-variable
                if isinstance(device, BrickMaster):
                    print(f"Found {device}, running example.")
                    tasks.add(asyncio.create_task(run_example(device)))
                    break
                print(f"Found {device}, but not interested.")

            # Wait for run_example() to finish
            await asyncio.gather(*tasks)
    except ConnectionRefusedError:
        print("Could not connect to server. Connection refused. Is the brick daemon up?")
    except asyncio.CancelledError:
        print("Stopped the main loop.")
        raise  # It is good practice to re-raise CancelledErrors
    finally:
        await shutdown(tasks)


# Report all mistakes managing asynchronous resources.
warnings.simplefilter("always", ResourceWarning)

# Start the main loop and run the async loop forever. Turn off the debug parameter for production code.
try:
    asyncio.run(main(), debug=True)
except KeyboardInterrupt:
    print("Shutting down gracefully.")
