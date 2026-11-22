"""The payloads of the callbacks of the generated devices are named after their callback."""

import sys

import pytest

from tinkerforge_async.device_factory import device_factory

from .fake_connection import UID, FakeConnection, read_events


def generated_devices():
    """All registered devices, that were generated from the Tinkerforge API definitions."""
    devices = device_factory._DeviceFactory__available_devices.values()  # pylint: disable=protected-access
    marker = "generated from the Tinkerforge API definitions"
    return sorted(
        (cls for cls in devices if marker in (sys.modules[cls.__module__].__doc__ or "")), key=lambda cls: cls.__name__
    )


def zeros(form):
    """A payload of zeros for the Tinkerforge format string."""
    values = []
    for item in form.split():
        count = int(item[:-1]) if item[:-1] else 1
        kind = item[-1]
        if kind == "s":
            values.append(b"")
        elif kind == "c":
            values.append(["\0"] * count if count > 1 else "\0")
        elif kind == "!":
            values.append([False] * count if count > 1 else False)
        else:
            values.append([0] * count if count > 1 else 0)
    return values


def callbacks():
    """All callbacks of the generated devices"""
    return [
        (device_class, callback_id)
        for device_class in generated_devices()
        for callback_id, form in device_class.CALLBACK_FORMATS.items()
        if form
    ]


def names(callback_id):
    """The allowed names of the named tuple of a callback, without underscores and in lower case."""
    name = callback_id.name.replace("_", "").lower()
    allowed = {f"get{name}", f"{name}event", f"get{name}result"}
    if name.endswith("reached"):  # The threshold callback of an old style Bricklet uses the result of the getter
        allowed.add(f"get{name.removesuffix('reached')}")
    return allowed


@pytest.mark.parametrize(
    "device_class, callback_id", callbacks(), ids=lambda value: getattr(value, "__name__", None) or value.name
)
def test_the_payload_is_named_after_the_callback(device_class, callback_id):
    """A named tuple of one callback must not be reused for another callback, that happens to have the same fields."""
    connection = FakeConnection()
    form = device_class.CALLBACK_FORMATS[callback_id]
    connection.callback(callback_id, form, *zeros(form))
    try:
        events = read_events(device_class(UID, connection))
    except ValueError:
        pytest.skip("A raw value of 0 is not a valid enum member of this callback")
    assert len(events) <= 1
    for event in events:
        payload_type = type(event.payload)
        if issubclass(payload_type, tuple) and hasattr(payload_type, "_fields"):
            assert payload_type.__name__.lower() in names(callback_id), payload_type.__name__
