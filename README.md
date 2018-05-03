# TinkerforgeAsync
This is a reimplementation of the Tinkerforge Python bindings ([original Python bindings](https://www.tinkerforge.com/en/doc/Software/API_Bindings_Python.html)) using Python 3 asyncio. The original bindings used threads to manage the blocking operations. A much cleaner implementation can be done using the *await* syntax from asyncio. 

# Supported Bricks/Bricklets
|Brick|Supported|Tested|Comments|
|--|--|--|--|
|[Master](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html)|:x:|  :x:|  |

|Bricklet|Supported|Tested|
|--|--|--|
|[Humidity](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Humidity.html)|:heavy_check_mark:|:heavy_check_mark:|
|[Temperature](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature.html)|:heavy_check_mark:|:heavy_check_mark:|

# Changes made to the API
Some of the design choices of the original Tinkerforge API are overly complex. I therefore replaced them with a simpler and more intuitive approach. A list of things that were changed can be found below:
### Design Changes
- Only Python 3 is supported (3.5+)
 - Replaced threads with an async event loop
 - Completely rewritten how responses from bricks/bricklets work. All setters now have a response_expected parameter, which when set to true will make the function call either return *True* or raise an error. There are no set_response_expected() functions any more.
 Old Style:
   ```python
   bricklet = BrickletHumidity(UID, ipcon)
   bricklet.set_response_expected(BrickletHumidity.FUNCTION_SET_HUMIDITY_CALLBACK_PERIOD, False)
   bricklet.set_humidity_callback_period(1000)
   ```
   New Style:
   ```python
   bricklet = BrickletHumidity(UID, ipcon)
   result = await bricklet.set_humidity_callback_period(1000, response_expected=False)    # True if successful
   ```
 - Replaced all constants with Enums and enforced their use using assertions. This will allow beginners to spot their mistakes earlier and make the code more readable, including any debug output statements.
 - Moved from base58 encoded uids to integers
 - Moved from callbacks to queues in an attempt to keep users out of the callback hell. It makes the code style more readable when using the *await* syntax anyway.
 - Payloads will now be decoded by the Device object and not by the ip_connection any more. This makes the code a lot more readable. To do so, the payload and decoded header will be handed to the device. It will then decode it if possible and pass it on the queue.
 - If physical quantities are measured we will now return standard SI units, not some unexpected stuff like centi°C (Temperature Bricklet). To preserve the precision the Decimal package is used. The only exception to this rule is the use of °C for temperature. This is for convenience.
 - All callbacks now contain a timestamp (Unix timestamp) and the device uid

### [IP Connection](https://www.tinkerforge.com/de/doc/Software/IPConnection_Python.html#api)

 - IPConnection.authenticate(_secret_): removed. This can now be done through connect()
 - IPConnection.set_timeout/IPConnection.get_timeout: Replaced by a property
 - IPConnection.register_callback(_callback_id_, _function_): Replaced by register_queue()

