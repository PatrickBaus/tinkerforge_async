#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An example to demonstrate most of the capabilities of the Tinkerforge
IP connection. It will connect to the remote host and enumerate it and
list all sensors.
"""
import asyncio
import warnings

from tinkerforge_async import IPConnectionAsync


async def main():
    """
    The main loop, that will spawn all callback handlers and wait until they are
    done. There are two callback handlers, one waits for the bricklet to connect
    and run the demo, the other handles messages sent by the bricklet.
    """
    try:
        async with IPConnectionAsync(host='127.0.0.1', port=4223) as ipcon:
            print('Enumerating brick and waiting for bricklets to reply')
            await ipcon.enumerate()
            async for packet in ipcon.read_enumeration():
                print(packet)

    except ConnectionRefusedError:
        print('Could not connect to server. Connection refused. Is the brick daemon up?')
    except asyncio.CancelledError:
        print('Stopped the main loop')
        raise

# Report all mistakes managing asynchronous resources.
warnings.simplefilter('always', ResourceWarning)

# Start the main loop and run the async loop forever
asyncio.run(main(), debug=True)