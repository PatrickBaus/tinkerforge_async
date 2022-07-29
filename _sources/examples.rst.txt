Examples
========
All tinkerforge connections require a brick daemon connection. This ip connection can either be a brick daemon running
on a computer or a one the `Master Extensions <https://www.tinkerforge.com/en/doc/Hardware/Master_Extensions/Master_Extensions.html>`_ available:
`Ethernet Master Extension <https://www.tinkerforge.com/en/doc/Hardware/Master_Extensions/Ethernet_Extension.html>`_,
`WIFI Master Extension <https://www.tinkerforge.com/en/doc/Hardware/Master_Extensions/WIFI_Extension.html>`_,
or `WIFI Master Extension 2.0 <https://www.tinkerforge.com/en/doc/Hardware/Master_Extensions/WIFI_V2_Extension.html>`_.

Below is a vers simple example, that reads a value from a
`Temperature Bricklet 2.0 <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Temperature_V2.html>`_. In this case,
the user needs to provide the ip and the unique id of the bricklet. If you are using the
`Brick Viewer <https://www.tinkerforge.com/en/doc/Software/Brickv.html>`_ software or the original Tinkerforge API, the
uids are Base58 encoded and need to be decoded first.

Basic Example
-------------

.. literalinclude:: ../../examples/simple.py
    :language: python

More Examples
-------------
More examples, that also use the autodiscovery capability of the ip connection can be found in the
`examples folder <https://github.com/PatrickBaus/tinkerforge_async/tree/master/examples/>`_.
