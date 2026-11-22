"""Tests for the IO-4 Bricklet 2.0."""

# pylint: disable=duplicate-code  # The devices of a family have a similar API, and so have their tests

import asyncio
from contextlib import aclosing
from decimal import Decimal

import pytest

from tinkerforge_async.bricklet_io4_v2 import (
    BrickletIO4V2,
    GetCaptureInputCallbackConfiguration,
    GetConfiguration,
    GetEdgeCountConfiguration,
    GetMonoflop,
    GetPWMConfiguration,
)
from tinkerforge_async.devices import AdvancedCallbackConfiguration, SimpleCallbackConfiguration

from .device_tests import DeviceTests
from .fake_connection import Call, read_events, request, run, summary, take

DEVICE = BrickletIO4V2
FunctionID = BrickletIO4V2.FunctionID
CallbackID = BrickletIO4V2.CallbackID
Direction = BrickletIO4V2.Direction
EdgeType = BrickletIO4V2.EdgeType

CALLS = [
    Call("set_value", FunctionID.SET_VALUE, ((True, False, 1, 0),), sent=("4!", ((True, False, True, False),))),
    Call(
        "set_value",
        FunctionID.SET_VALUE,
        ([False, False, False, True], False),
        sent=("4!", ((False, False, False, True),)),
        response_expected=False,
    ),
    Call(
        "get_value",
        FunctionID.GET_VALUE,
        reply=("4!", ((True, False, False, True),)),
        result=(True, False, False, True),
    ),
    Call("set_selected_value", FunctionID.SET_SELECTED_VALUE, (3, True), sent=("B !", (3, True))),
    Call("set_selected_value", FunctionID.SET_SELECTED_VALUE, (0, 0), sent=("B !", (0, False))),
    # The default is an input with pull-up
    Call("set_configuration", FunctionID.SET_CONFIGURATION, (0,), sent=("B c !", (0, b"i", True))),
    Call(
        "set_configuration",
        FunctionID.SET_CONFIGURATION,
        (3, Direction.OUT, False),
        sent=("B c !", (3, b"o", False)),
    ),
    Call("set_configuration", FunctionID.SET_CONFIGURATION, (1, "o"), sent=("B c !", (1, b"o", True))),
    Call(
        "get_configuration",
        FunctionID.GET_CONFIGURATION,
        (2,),
        sent=("B", (2,)),
        reply=("c !", ("o", True)),
        result=GetConfiguration(Direction.OUT, True),
    ),
    Call(
        "set_input_value_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (0,),
        sent=("B I !", (0, 0, False)),
    ),
    Call(
        "set_input_value_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (3, Decimal("0.5"), True),
        sent=("B I !", (3, 500, True)),
    ),
    Call(
        "set_callback_configuration",
        FunctionID.SET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (2, 1, True),
        sent=("B I !", (2, 1000, True)),
    ),
    Call(
        "get_input_value_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
        reply=("I !", (500, True)),
        result=SimpleCallbackConfiguration(Decimal("0.5"), True),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (2,),
        sent=("B", (2,)),
        reply=("I !", (500, True)),
        result=AdvancedCallbackConfiguration(Decimal("0.5"), True, None, None, None),
    ),
    Call(
        "set_all_input_value_callback_configuration",
        FunctionID.SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        sent=("I !", (0, False)),
    ),
    Call(
        "set_all_input_value_callback_configuration",
        FunctionID.SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (Decimal("0.5"), True),
        sent=("I !", (500, True)),
    ),
    # The sid 4 are all inputs
    Call(
        "set_callback_configuration",
        FunctionID.SET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (4, 1, True),
        sent=("I !", (1000, True)),
    ),
    Call(
        "get_all_input_value_callback_configuration",
        FunctionID.GET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        reply=("I !", (500, True)),
        result=SimpleCallbackConfiguration(Decimal("0.5"), True),
    ),
    Call(
        "get_callback_configuration",
        FunctionID.GET_ALL_INPUT_VALUE_CALLBACK_CONFIGURATION,
        (4,),
        reply=("I !", (500, True)),
        result=AdvancedCallbackConfiguration(Decimal("0.5"), True, None, None, None),
    ),
    Call("set_monoflop", FunctionID.SET_MONOFLOP, (0, True, Decimal("1.5")), sent=("B ! I", (0, True, 1500))),
    Call("set_monoflop", FunctionID.SET_MONOFLOP, (3, False, 0), sent=("B ! I", (3, False, 0))),
    Call(
        "get_monoflop",
        FunctionID.GET_MONOFLOP,
        (3,),
        sent=("B", (3,)),
        reply=("! I I", (True, 1500, 500)),
        result=GetMonoflop(True, Decimal("1.5"), Decimal("0.5")),
    ),
    Call("get_edge_count", FunctionID.GET_EDGE_COUNT, (0,), sent=("B !", (0, False)), reply=("I", (42,)), result=42),
    Call("get_edge_count", FunctionID.GET_EDGE_COUNT, (3, True), sent=("B !", (3, True)), reply=("I", (0,)), result=0),
    Call("set_edge_count_configuration", FunctionID.SET_EDGE_COUNT_CONFIGURATION, (0,), sent=("B B B", (0, 0, 100))),
    Call(
        "set_edge_count_configuration",
        FunctionID.SET_EDGE_COUNT_CONFIGURATION,
        (3, EdgeType.BOTH, Decimal("0.255")),
        sent=("B B B", (3, 2, 255)),
    ),
    Call("set_edge_count_configuration", FunctionID.SET_EDGE_COUNT_CONFIGURATION, (1, 1, 0), sent=("B B B", (1, 1, 0))),
    Call(
        "get_edge_count_configuration",
        FunctionID.GET_EDGE_COUNT_CONFIGURATION,
        (1,),
        sent=("B", (1,)),
        reply=("B B", (1, 100)),
        result=GetEdgeCountConfiguration(EdgeType.FALLING, Decimal("0.1")),
    ),
    # The frequency is transferred in 1/10 Hz, the duty cycle in 1/100 %
    Call("set_pwm_configuration", FunctionID.SET_PWM_CONFIGURATION, (0,), sent=("B I H", (0, 0, 0))),
    Call(
        "set_pwm_configuration",
        FunctionID.SET_PWM_CONFIGURATION,
        (3, Decimal("1000.5"), 0.5),
        sent=("B I H", (3, 10005, 5000)),
    ),
    Call(
        "get_pwm_configuration",
        FunctionID.GET_PWM_CONFIGURATION,
        (3,),
        sent=("B", (3,)),
        reply=("I H", (10005, 10000)),
        result=GetPWMConfiguration(Decimal("1000.5"), Decimal(1)),
    ),
]

CALLS += [
    Call(
        "set_capture_input_callback_configuration",
        FunctionID.SET_CAPTURE_INPUT_CALLBACK_CONFIGURATION,
        (True,),
        sent=("! H", (True, 50)),
    ),
    Call(
        "set_capture_input_callback_configuration",
        FunctionID.SET_CAPTURE_INPUT_CALLBACK_CONFIGURATION,
        (False, 0.00002, False),
        sent=("! H", (False, 20)),
        response_expected=False,
    ),
    Call(
        "get_capture_input_callback_configuration",
        FunctionID.GET_CAPTURE_INPUT_CALLBACK_CONFIGURATION,
        reply=("! H", (True, 50)),
        result=GetCaptureInputCallbackConfiguration(True, Decimal("0.00005")),
    ),
]

REJECTED = [
    ("set_selected_value", (4, True)),
    ("set_configuration", (4,)),
    ("set_configuration", (0, "x")),
    ("get_configuration", (4,)),
    ("set_input_value_callback_configuration", (4,)),
    ("get_input_value_callback_configuration", (4,)),
    ("set_edge_count_callback_configuration", (4,)),
    ("set_monoflop", (4, True, 1)),
    ("get_monoflop", (4,)),
    ("get_edge_count", (4,)),
    ("set_edge_count_configuration", (4,)),
    ("set_edge_count_configuration", (0, 3)),
    ("get_edge_count_configuration", (4,)),
    ("set_pwm_configuration", (4,)),
    ("get_pwm_configuration", (4,)),
    ("get_edge_count_callback_configuration", (4,)),
    # The time between two captures is 20 µs to 65535 µs
    ("set_capture_input_callback_configuration", (True, Decimal("0.000019"))),
    ("set_capture_input_callback_configuration", (True, Decimal("0.065536"))),
    # The sids are the channels 0 to 3, 4 for all channels, and 5 to 8 for the edge counters of the channels. The
    # captured inputs (sid 9) are not configured by a period.
    ("set_callback_configuration", (9,)),
    ("get_callback_configuration", (9,)),
]


def test_identity(bricklet):
    """The Bricklet knows who it is."""
    assert bricklet.DEVICE_IDENTIFIER.value == 2111
    assert bricklet.get_api_version() == (2, 0, 0)
    assert str(bricklet).startswith("IO-4 Bricklet 2.0 with uid 12345")


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def callbacks(connection):
    """Register one callback of each kind, and one unknown callback, that must be dropped."""
    connection.callback(CallbackID.INPUT_VALUE, "B ! !", 1, True, False)
    connection.callback(99)
    connection.callback(CallbackID.MONOFLOP_DONE, "B !", 3, True)
    connection.callback(CallbackID.ALL_INPUT_VALUE, "4! 4!", (False, True, False, False), (True, False, True, False))


def test_events_filtered_by_callback(bricklet, connection):
    """The channel is the sid. The callback of all inputs is sid 4, its payload are the values of all channels."""
    callbacks(connection)
    assert summary(read_events(bricklet, events=(CallbackID.INPUT_VALUE,))) == [(1, CallbackID.INPUT_VALUE, False)]
    assert summary(read_events(bricklet, events=(CallbackID.MONOFLOP_DONE.value,))) == [
        (3, CallbackID.MONOFLOP_DONE, True)
    ]
    events = read_events(bricklet, events=(CallbackID.ALL_INPUT_VALUE,))
    assert summary(events) == [(4, CallbackID.ALL_INPUT_VALUE, (True, False, True, False))]
    assert events[0].additional == (False, True, False, False)  # The channels that changed


def test_events_filtered_by_sid(bricklet, connection):
    """The callback of all inputs is split into the channels, unless the sid 4 is requested."""
    callbacks(connection)
    events = read_events(bricklet, sids=(1,))
    assert summary(events) == [(1, CallbackID.INPUT_VALUE, False), (1, CallbackID.ALL_INPUT_VALUE, False)]
    assert [event.additional for event in events] == [True, True]  # The value has changed

    assert summary(read_events(bricklet, sids=(0, 3))) == [
        (3, CallbackID.MONOFLOP_DONE, True),
        (0, CallbackID.ALL_INPUT_VALUE, True),
        (3, CallbackID.ALL_INPUT_VALUE, False),
    ]
    assert summary(read_events(bricklet, sids=(4,))) == [(4, CallbackID.ALL_INPUT_VALUE, (True, False, True, False))]


def test_captured_inputs_are_events_of_sid_9(bricklet, connection):
    """The captured inputs are a stream of bitmasks. They are not split into the channels."""
    callbacks(connection)
    connection.callback(CallbackID.CAPTURE_INPUT, "64B", list(range(64)))
    connection.callback(CallbackID.EDGE_COUNT)  # Emulated by the library, so a packet with this id is dropped
    expected = [(9, CallbackID.CAPTURE_INPUT, bytes(range(64)))]
    assert summary(read_events(bricklet, sids=(9,))) == expected
    assert summary(read_events(bricklet, events=(CallbackID.CAPTURE_INPUT,))) == expected
    assert (9, CallbackID.CAPTURE_INPUT, bytes(range(64))) not in summary(read_events(bricklet, sids=(0, 4)))
    # The callback of all inputs is still split into the channels, if both are read
    assert summary(read_events(bricklet, sids=(2, 9))) == [(2, CallbackID.ALL_INPUT_VALUE, True)] + expected


def test_invalid_event_filters_are_rejected(bricklet):
    """The events are either filtered by callback or by sid. Unknown callbacks are rejected."""
    with pytest.raises(ValueError):
        read_events(bricklet, events=(CallbackID.INPUT_VALUE,), sids=(0,))
    with pytest.raises(ValueError):
        read_events(bricklet, events=(99,))


def test_all_events_are_read_without_a_filter(bricklet, connection):
    """Without a filter the callbacks and the edge counters are read."""
    callbacks(connection)
    connection.reply(FunctionID.GET_EDGE_COUNT, "I", 7)

    async def scenario():
        await bricklet.set_edge_count_callback_configuration(2, period=Decimal("0.001"))
        return await take(bricklet.read_events(), 4)

    assert sorted(summary(run(scenario())), key=lambda event: event[1].value) == [
        (1, CallbackID.INPUT_VALUE, False),
        (4, CallbackID.ALL_INPUT_VALUE, (True, False, True, False)),
        (3, CallbackID.MONOFLOP_DONE, True),
        (7, CallbackID.EDGE_COUNT, 7),
    ]


async def requests_sent(connection, count):
    """Wait until the library has sent a number of requests."""
    async with asyncio.timeout(5):
        while len(connection.requests) < count:
            await asyncio.sleep(0.001)


async def read_until(bricklet, payload, **filters):
    """
    Read the events of the edge counters until an event with the given payload is read. The number of events depends
    on the timing, because a reading replaces the previous reading, if it has not been read yet.
    """
    events = []
    async with asyncio.timeout(5):
        async with aclosing(bricklet.read_events(**filters)) as stream:
            async for event in stream:
                events.append(event)
                if event.payload == payload:
                    break
    return events


def test_edge_count_events_are_polled(bricklet, connection):
    """
    The Bricklet has no callback for the edge counters, so the library polls them. The sid is the channel + 5. The
    counter is reset with every reading, so the payload is the number of edges per period.
    """
    for count in (0, 3, 3, 5):  # The first reading only resets the counter
        connection.reply(FunctionID.GET_EDGE_COUNT, "I", count)

    async def scenario():
        await bricklet.set_callback_configuration(6, period=Decimal("0.001"))
        return await read_until(bricklet, 5, sids=(6,))

    events = run(scenario())
    assert {(event.sid, event.function_id) for event in events} == {(6, CallbackID.EDGE_COUNT)}
    assert [event.payload for event in events] in ([3, 3, 5], [3, 5], [5])
    assert set(connection.requests) == {request(FunctionID.GET_EDGE_COUNT, "B !", 1, True)}
    assert run(bricklet.get_edge_count_callback_configuration(1)) == SimpleCallbackConfiguration(
        Decimal("0.001"), False
    )
    assert run(bricklet.get_callback_configuration(6)) == AdvancedCallbackConfiguration(
        Decimal("0.001"), False, None, None, None
    )


def test_edge_count_events_if_the_value_has_to_change(bricklet, connection):
    """A reading, that is equal to the previous reading, is dropped."""
    for count in (0, 3, 3, 3, 5):
        connection.reply(FunctionID.GET_EDGE_COUNT, "I", count)

    async def scenario():
        await bricklet.set_edge_count_callback_configuration(0, Decimal("0.001"), value_has_to_change=True)
        events = await read_until(bricklet, 5, events=(CallbackID.EDGE_COUNT,))
        # The reading stays 5 from now on, so there are no more events
        with pytest.raises(TimeoutError):
            async with asyncio.timeout(0.02):
                await take(bricklet.read_events(sids=(5,)), 1)
        return events

    assert summary(run(scenario())) in (
        [(5, CallbackID.EDGE_COUNT, 3), (5, CallbackID.EDGE_COUNT, 5)],
        [(5, CallbackID.EDGE_COUNT, 5)],
    )
    assert run(bricklet.get_edge_count_callback_configuration(0)) == SimpleCallbackConfiguration(Decimal("0.001"), True)


def test_only_the_latest_edge_count_is_kept(bricklet, connection):
    """If nobody reads the events, the old reading is replaced, so the reader does not get outdated events."""
    for count in range(100):
        connection.reply(FunctionID.GET_EDGE_COUNT, "I", count)

    async def scenario():
        await bricklet.set_edge_count_callback_configuration(0, Decimal("0.001"))
        await requests_sent(connection, 5)
        return (await take(bricklet.read_events(sids=(5,)), 1))[0]

    assert run(scenario()).payload >= 2


def test_edge_count_polling_is_stopped(bricklet, connection):
    """A period of 0 stops the polling, and drops the event, that has not been read."""
    connection.reply(FunctionID.GET_EDGE_COUNT, "I", 1)

    async def scenario():
        await bricklet.set_edge_count_callback_configuration(0, 0)  # It is not running, there is nothing to stop
        await bricklet.set_edge_count_callback_configuration(0, Decimal("0.001"))
        await requests_sent(connection, 3)  # The second reading creates the first event
        await bricklet.set_edge_count_callback_configuration(0, 0)
        requests = len(connection.requests)
        with pytest.raises(TimeoutError):
            async with asyncio.timeout(0.02):
                await take(bricklet.read_events(sids=(5,)), 1)
        assert len(connection.requests) == requests
        return await bricklet.get_edge_count_callback_configuration(0)

    assert run(scenario()) == SimpleCallbackConfiguration(Decimal(0), False)


def test_edge_count_polling_ends_if_the_bricklet_rejects_the_request(bricklet, connection):
    """The polling ends silently, and can be configured again."""
    connection.fail(FunctionID.GET_EDGE_COUNT, ValueError("Invalid parameter."))

    async def scenario():
        await bricklet.set_edge_count_callback_configuration(0, Decimal("0.001"))
        await requests_sent(connection, 1)
        await asyncio.sleep(0.02)
        assert len(connection.requests) == 1  # It does not try again
        await bricklet.set_edge_count_callback_configuration(0, Decimal("0.001"))
        await requests_sent(connection, 2)

    run(scenario())
