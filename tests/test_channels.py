"""Tests for the tables of channels, that describe the sids of a device."""

# pylint: disable=protected-access

import asyncio
from decimal import Decimal
from enum import Enum
from unittest.mock import Mock

import pytest

from tinkerforge_async.device_factory import device_factory
from tinkerforge_async.devices import (
    AdvancedCallbackConfiguration,
    Channel,
    ChannelConfiguration,
    Device,
    InvalidSidError,
    SimpleCallbackConfiguration,
    ThresholdOption,
)


def devices_with_channels():
    """All registered devices, that describe their sids in a table of channels."""
    devices = device_factory._DeviceFactory__available_devices.values()
    return sorted((cls for cls in devices if cls.CHANNELS), key=lambda cls: cls.__name__)


DEVICES = devices_with_channels()


def methods(configuration):
    """The names of the methods of a device, that configure the channel."""
    if configuration.split:
        return [
            f"{action}_{configuration.name}_callback_{what}"
            for action in ("set", "get")
            for what in ("period", "threshold")
        ]
    return [f"{action}_{configuration.name}_callback_configuration" for action in ("set", "get")]


def test_the_tables_are_used_by_all_the_devices_with_sids():
    """
    Guard against a device that is not converted. Devices with a bitmask (IO-16, IO-4) have no table. 77 of the
    devices have callbacks and therefore a table.
    """
    assert len(DEVICES) == 18 + 77


@pytest.mark.parametrize("device_class", DEVICES, ids=lambda cls: cls.__name__)
def test_table_is_consistent_with_the_device(device_class):
    """All methods and callbacks, that the table refers to, exist."""
    sids = [channel.sid for channel in device_class.CHANNELS]
    assert len(set(sids)) == len(sids)
    for channel in device_class.CHANNELS:
        assert channel.getter is None or callable(getattr(device_class, channel.getter))
        for callback_id in channel.callbacks:
            assert callback_id in device_class.CALLBACK_FORMATS
        if channel.configuration is not None:
            for name in (
                methods(channel.configuration)
                if channel.configuration.split
                else [
                    f"set_{channel.configuration.name}_callback_configuration",
                    f"get_{channel.configuration.name}_callback_configuration",
                ]
            ):
                assert callable(getattr(device_class, name)), name


@pytest.mark.parametrize("device_class", DEVICES, ids=lambda cls: cls.__name__)
def test_sid_to_callback_is_generated_from_the_table(device_class):
    """The callbacks of a sid are taken from the table and every callback belongs to a sid."""
    assert dict(device_class.SID_TO_CALLBACK) == {channel.sid: channel.callbacks for channel in device_class.CHANNELS}
    assigned = {callback for callbacks in device_class.SID_TO_CALLBACK.values() for callback in callbacks}
    assert assigned == set(device_class.CALLBACK_FORMATS)


class Callback(Enum):
    """The callbacks of the toy device"""

    VALUE = 1


class Toy(Device):
    """A device with all kinds of channels, that records the calls instead of sending requests."""

    CHANNELS = (
        Channel(0, "get_split", (Callback.VALUE,), ChannelConfiguration("split", split=True, default=5)),
        Channel(1, "get_combined", (), ChannelConfiguration("combined")),
        Channel(2, "get_indexed", (), ChannelConfiguration("indexed"), index=7),
        Channel(3, "get_plain", (), ChannelConfiguration("plain", thresholds=False, wrap_advanced=True)),
        Channel(4, None, ()),
        Channel(5, "get_unconfigurable", ()),
    )

    def __init__(self):
        super().__init__("Toy", 1, Mock())
        self.calls = []

    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)

        async def record(*args):
            self.calls.append((name, args))
            if name == "get_plain_callback_configuration":
                return SimpleCallbackConfiguration(Decimal(3), True)
            if name.endswith("_callback_configuration"):
                return AdvancedCallbackConfiguration(Decimal(1), False, ThresholdOption.OFF, Decimal(0), Decimal(0))
            if name.endswith("_callback_period"):
                return Decimal(2)
            if name.endswith("_callback_threshold"):
                return ThresholdOption.OFF, Decimal(0), Decimal(0)
            return name

        return record


def test_sid_to_callback_of_a_class_without_table_is_untouched():
    """Only classes that define CHANNELS get a generated SID_TO_CALLBACK."""

    class Manual(Device):
        """A device with a hand written table"""

        SID_TO_CALLBACK = {0: ("a",)}

    assert Manual.SID_TO_CALLBACK == {0: ("a",)}
    assert Toy.SID_TO_CALLBACK == {0: (Callback.VALUE,), 1: (), 2: (), 3: (), 4: (), 5: ()}


def test_get_value_calls_the_getter_with_the_index():
    """The getter is called, with the index if there is one. Channels without a getter are rejected."""
    toy = Toy()
    assert asyncio.run(toy._get_value(0)) == "get_split"
    assert asyncio.run(toy._get_value(2)) == "get_indexed"
    assert toy.calls == [("get_split", ()), ("get_indexed", (7,))]
    with pytest.raises(InvalidSidError):
        asyncio.run(toy._get_value(4))
    with pytest.raises(InvalidSidError):
        asyncio.run(toy._get_value(6))


def test_split_configuration_sets_period_and_threshold_with_the_default():
    """The default of the channel is used for a missing minimum and maximum."""
    toy = Toy()
    asyncio.run(toy._set_callback_configuration(0, 2, False, ThresholdOption.INSIDE, None, 9, False))
    assert toy.calls == [
        ("set_split_callback_period", (2, False)),
        ("set_split_callback_threshold", (ThresholdOption.INSIDE, 5, 9, False)),
    ]


def test_combined_and_indexed_configuration():
    """A combined configuration is set by one call. The index is the first argument."""
    toy = Toy()
    asyncio.run(toy._set_callback_configuration(1, 2, True, 1, 3, 4, True))
    asyncio.run(toy._set_callback_configuration(2, 2, True))
    assert toy.calls == [
        ("set_combined_callback_configuration", (2, True, 1, 3, 4, True)),
        ("set_indexed_callback_configuration", (7, 2, True, ThresholdOption.OFF, 0, 0, True)),
    ]


def test_configuration_without_thresholds_ignores_them():
    """Only the period and value_has_to_change are set. The result has no thresholds."""
    toy = Toy()
    asyncio.run(toy._set_callback_configuration(3, 2, True, 1, 3, 4, False))
    assert toy.calls == [("set_plain_callback_configuration", (2, True, False))]
    result = asyncio.run(toy._get_callback_configuration(3))
    assert result == AdvancedCallbackConfiguration(Decimal(3), True, None, None, None)


def test_split_configuration_is_returned_as_advanced_configuration():
    """The period and threshold of old devices are combined. They have no value_has_to_change option."""
    toy = Toy()
    result = asyncio.run(toy._get_callback_configuration(0))
    assert result == AdvancedCallbackConfiguration(Decimal(2), True, ThresholdOption.OFF, Decimal(0), Decimal(0))


@pytest.mark.parametrize("sid", [4, 5, 6])
def test_channels_without_configuration_are_rejected(sid):
    """Only channels with a configuration can be configured."""
    toy = Toy()
    with pytest.raises(InvalidSidError):
        asyncio.run(toy._set_callback_configuration(sid))
    with pytest.raises(InvalidSidError):
        asyncio.run(toy._get_callback_configuration(sid))
