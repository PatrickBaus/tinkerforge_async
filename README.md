# TinkerforgeAsync
This is a reimplementation of the Tinkerforge Python bindings ([Original Python Bindings](https://www.tinkerforge.com/en/doc/Software/API_Bindings_Python.html)) using Python 3 asyncio. The original bindings used threads to manage the blocking operations. A much cleaner implementation can be done using the *await* syntax from asyncio. 

# Supported Bricks/Bricklets
|Bricklet|Supported|Tested|
|--|--|--|
|Humidity|![supported](/images/light_green_check.png)|![tested](/images/light_green_check.png)

