# TinkerforgeAsync
This is a reimplementation of the Tinkerforge Python bindings ([original Python Bindings](https://www.tinkerforge.com/en/doc/Software/API_Bindings_Python.html)) using Python 3 asyncio. The original bindings used threads to manage the blocking operations. A much cleaner implementation can be done using the *await* syntax from asyncio. 

# Supported Bricks/Bricklets
|Brick|Supported|Tested|
|--|--|--|
|[Master](https://www.tinkerforge.com/en/doc/Hardware/Bricks/Master_Brick.html)|:x:|  :x:|

|Bricklet|Supported|Tested|
|--|--|--|
|[Humidity](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Humidity.html)|:heavy_check_mark:|  :heavy_check_mark:|
|[Temperature](https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature.html)|:heavy_check_mark:|  :x:|
