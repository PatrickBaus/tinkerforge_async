#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
A simple example, that reads a value from a temperature bricklet
"""
import asyncio

from tinkerforge_async.bricklet_temperature_v2 import BrickletTemperatureV2
from tinkerforge_async.ip_connection import IPConnectionAsync


async def main() -> None:
    """Connect to the bricklet and query the temperature value"""
    try:
        uid = 123456  # alternatively use base58decode("XXX")
        # Use the context manager of the ip connection. It will automatically do the cleanup.
        async with IPConnectionAsync(host="127.0.0.1", port=4223) as connection:
            bricklet = BrickletTemperatureV2(uid, connection)
            # The temperature is in Kelvin. Convert to float and subtract 273.15 to get Celsius.
            print(f"Bricklet: {bricklet}\nTemperature: {await bricklet.get_temperature()} K")
    except ConnectionRefusedError:
        print("Could not connect to server. Connection refused. Is the brick daemon up?")


# Start the main loop and run the async loop forever. Turn off the debug parameter for production code.
try:
    asyncio.run(main(), debug=True)
except KeyboardInterrupt:
    print("Shutting down gracefully.")
