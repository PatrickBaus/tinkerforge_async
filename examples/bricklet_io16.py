#!/usr/bin/env python3
# pylint: disable=duplicate-code
"""
An example to demonstrate most of the capabilities of the Tinkerforge IO-16 Bricklet.
"""
import asyncio
import warnings

from tinkerforge_async.bricklet_io16 import BrickletIO16
from tinkerforge_async.ip_connection import IPConnectionAsync


async def process_callbacks(device: BrickletIO16) -> None:
    """Prints the callbacks (filtered by id) of the bricklet."""
    async for packet in device.read_events():
        print("Callback received", packet)


async def run_example(bricklet: BrickletIO16) -> None:  # pylint: disable=too-many-statements
    """This is the actual demo. If the bricklet is found, this code will be run."""
    callback_task = asyncio.create_task(process_callbacks(bricklet))
    try:
        print("Identity:", await bricklet.get_identity())

        port_a = await bricklet.get_port(bricklet.Port.A)  # or 'a' or 'A'
        port_b = await bricklet.get_port("b")
        print(f"Port A: {port_a:08b}")
        print(f"Port B: {port_b:08b}")
        await asyncio.gather(bricklet.set_port("A", port_a), bricklet.set_port("B", port_b))

        print("Port A configuration:", await bricklet.get_port_configuration("A"))
        print("Port B configuration:", await bricklet.get_port_configuration("B"))
        await bricklet.set_port_configuration(
            "A", 0b11111111, bricklet.Direction.IN, bricklet.InputConfiguration.PULL_UP
        )  # Set all pins to "input with pull-up"
        await bricklet.set_port_configuration(
            "B", 0b11111111, bricklet.Direction.OUT, bricklet.OutputConfiguration.LOW
        )  # Set all pins to output LOW

        print("Set bricklet debounce period to", 10, "ms")
        await bricklet.set_debounce_period(10)
        print("Get bricklet debounce period:", await bricklet.get_debounce_period())

        port_a = await bricklet.get_port_interrupt("A")
        port_b = await bricklet.get_port_interrupt("B")
        print(f"Port A interrupts: {port_a:08b}")
        print(f"Port B interrupts: {port_b:08b}")

        print("Enable interrupts on port A")
        await bricklet.set_port_interrupt("A", 0b11111111)
        print(f"Port interrupts: {await bricklet.get_port_interrupt('A'):08b}")
        print("Wait for interrupts. Connect a few outputs from port B to port A.")
        await asyncio.sleep(5)

        print(
            "Enabling monoflop on B0 and B3. A0 will be high and B3 low until the time runs out, then B0 will go low"
            " and B3 high. Like a dead man's switch."
        )
        await bricklet.set_port_monoflop("B", 0b00001001, 0b00000001, 3000)
        print("Monoflop state:")
        for i in range(3):
            print(f"B0: {await bricklet.get_port_monoflop('B', 0)}, B3: {bricklet.get_port_monoflop('B', 3)}")
            await asyncio.sleep(1)

        print("Setting B3 low.")
        await bricklet.set_selected_values("B", 0b00001000, 0b00000000)
        await asyncio.sleep(0.1)

        print("Enabling edge counting on A0. Connect pin B7 to A0.")
        await bricklet.set_selected_values(
            "B", 0b10000000, 0b10000000
        )  # Set B7 to high, because toggling starts by going low.
        await bricklet.set_edge_count_config(0, bricklet.EdgeType.BOTH, debounce=5)
        print("Edge count config A0:", await bricklet.get_edge_count_config(0))
        print("Edge count config A1:", await bricklet.get_edge_count_config(1))

        print("Toggling pin B7.")
        for i in range(10):
            print("Setting pin", "HIGH." if (i % 2) else "LOW.")
            await bricklet.set_selected_values("B", 0b10000000, 0b10000000 & ((i % 2) << 7))
            print("Edge count of A0:", await bricklet.get_edge_count(0))
            await asyncio.sleep(0.01)

        print("Disabling interrupts.")
        await bricklet.set_port_interrupt("A", 0b00000000)
    finally:
        callback_task.cancel()


async def shutdown(tasks: set[asyncio.Task]) -> None:
    """Clean up by stopping all consumers"""
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks)


async def main() -> None:
    """
    The main loop, that will spawn all callback handlers and wait until they are done. There are two callback handlers,
    one waits for the bricklet to connect and runs the demo, the other handles messages sent by the bricklet.
    """
    tasks = set()
    try:
        # Use the context manager of the ip connection. It will automatically do the cleanup.
        async with IPConnectionAsync(host="127.0.0.1", port=4223) as connection:
            await connection.enumerate()
            # Read all enumeration replies, then start the example if we find the correct device
            async for enumeration_type, device in connection.read_enumeration():  # pylint: disable=unused-variable
                if isinstance(device, BrickletIO16):
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
    finally:
        await shutdown(tasks)


# Report all mistakes managing asynchronous resources.
warnings.simplefilter("always", ResourceWarning)

# Start the main loop and run the async loop forever
asyncio.run(main(), debug=True)
