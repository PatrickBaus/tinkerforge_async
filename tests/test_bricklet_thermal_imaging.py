"""Tests for the Thermal Imaging Bricklet. Generated from the Tinkerforge API definitions."""

# pylint: disable=duplicate-code,too-many-lines,line-too-long,unused-import

from decimal import Decimal
from typing import Any

from tinkerforge_async.bricklet_thermal_imaging import (
    BrickletThermalImaging,
    GetFFCShutterMode,
    GetFluxLinearParameters,
    GetHighContrastConfig,
    GetHighContrastImage,
    GetStatistics,
    GetTemperatureImage,
)
from tinkerforge_async.devices import ThresholdOption as Threshold

from .device_tests import DeviceTests
from .fake_connection import UID, Call, FakeConnection, chunk, read_events, request, run, summary

DEVICE = BrickletThermalImaging
FunctionID = BrickletThermalImaging.FunctionID
CallbackID = BrickletThermalImaging.CallbackID

# The function and callback ids of the official Tinkerforge Python bindings 2.1.32
OFFICIAL_FUNCTION_IDS: dict[str, int] = {
    "GET_HIGH_CONTRAST_IMAGE_LOW_LEVEL": 1,
    "GET_TEMPERATURE_IMAGE_LOW_LEVEL": 2,
    "GET_STATISTICS": 3,
    "SET_RESOLUTION": 4,
    "GET_RESOLUTION": 5,
    "SET_SPOTMETER_CONFIG": 6,
    "GET_SPOTMETER_CONFIG": 7,
    "SET_HIGH_CONTRAST_CONFIG": 8,
    "GET_HIGH_CONTRAST_CONFIG": 9,
    "SET_IMAGE_TRANSFER_CONFIG": 10,
    "GET_IMAGE_TRANSFER_CONFIG": 11,
    "SET_FLUX_LINEAR_PARAMETERS": 14,
    "GET_FLUX_LINEAR_PARAMETERS": 15,
    "SET_FFC_SHUTTER_MODE": 16,
    "GET_FFC_SHUTTER_MODE": 17,
    "RUN_FFC_NORMALIZATION": 18,
}
OFFICIAL_CALLBACK_IDS: dict[str, int] = {"HIGH_CONTRAST_IMAGE_LOW_LEVEL": 12, "TEMPERATURE_IMAGE_LOW_LEVEL": 13}

CALLS: list[Call] = [
    Call(
        "get_high_contrast_image_low_level",
        FunctionID.GET_HIGH_CONTRAST_IMAGE_LOW_LEVEL,
        (),
        reply=("H 62B", (3, [i % 256 for i in range(62)])),
        result=GetHighContrastImage(3, tuple(i % 256 for i in range(62))),
    ),
    Call(
        "get_temperature_image_low_level",
        FunctionID.GET_TEMPERATURE_IMAGE_LOW_LEVEL,
        (),
        reply=("H 31H", (3, [4] * 31)),
        result=GetTemperatureImage(3, (4,) * 31),
    ),
    Call(
        "get_statistics",
        FunctionID.GET_STATISTICS,
        (),
        reply=("4H 4H B B 2!", ([3] * 4, [4] * 4, 1, 3, [i % 2 == 0 for i in range(2)])),
        result=GetStatistics(
            (3,) * 4,
            (4,) * 4,
            DEVICE.Resolution.RESOLUTION_0_TO_655_KELVIN,
            DEVICE.FFCStatus.COMPLETE,
            tuple(i % 2 == 0 for i in range(2)),
        ),
    ),
    Call(
        "set_resolution", FunctionID.SET_RESOLUTION, (DEVICE.Resolution.RESOLUTION_0_TO_655_KELVIN,), sent=("B", (1,))
    ),
    Call(
        "set_resolution",
        FunctionID.SET_RESOLUTION,
        (DEVICE.Resolution.RESOLUTION_0_TO_655_KELVIN, False),
        sent=("B", (1,)),
        response_expected=False,
    ),
    Call(
        "get_resolution",
        FunctionID.GET_RESOLUTION,
        (),
        reply=("B", (1,)),
        result=DEVICE.Resolution.RESOLUTION_0_TO_655_KELVIN,
    ),
    Call(
        "set_spotmeter_config",
        FunctionID.SET_SPOTMETER_CONFIG,
        ([i % 256 for i in range(4)],),
        sent=("4B", ([i % 256 for i in range(4)],)),
    ),
    Call(
        "set_spotmeter_config",
        FunctionID.SET_SPOTMETER_CONFIG,
        ([i % 256 for i in range(4)], False),
        sent=("4B", ([i % 256 for i in range(4)],)),
        response_expected=False,
    ),
    Call(
        "get_spotmeter_config",
        FunctionID.GET_SPOTMETER_CONFIG,
        (),
        reply=("4B", ([i % 256 for i in range(4)],)),
        result=tuple(i % 256 for i in range(4)),
    ),
    Call(
        "set_high_contrast_config",
        FunctionID.SET_HIGH_CONTRAST_CONFIG,
        ([i % 256 for i in range(4)], 3, [3] * 2, 3),
        sent=("4B H 2H H", ([i % 256 for i in range(4)], 3, [3] * 2, 3)),
    ),
    Call(
        "set_high_contrast_config",
        FunctionID.SET_HIGH_CONTRAST_CONFIG,
        ([i % 256 for i in range(4)], 3, [3] * 2, 3, False),
        sent=("4B H 2H H", ([i % 256 for i in range(4)], 3, [3] * 2, 3)),
        response_expected=False,
    ),
    Call(
        "get_high_contrast_config",
        FunctionID.GET_HIGH_CONTRAST_CONFIG,
        (),
        reply=("4B H 2H H", ([i % 256 for i in range(4)], 4, [5] * 2, 6)),
        result=GetHighContrastConfig(tuple(i % 256 for i in range(4)), 4, (5,) * 2, 6),
    ),
    Call(
        "set_image_transfer_config",
        FunctionID.SET_IMAGE_TRANSFER_CONFIG,
        (DEVICE.ImageTransfer.CALLBACK_TEMPERATURE_IMAGE,),
        sent=("B", (3,)),
    ),
    Call(
        "set_image_transfer_config",
        FunctionID.SET_IMAGE_TRANSFER_CONFIG,
        (DEVICE.ImageTransfer.CALLBACK_TEMPERATURE_IMAGE, False),
        sent=("B", (3,)),
        response_expected=False,
    ),
    Call(
        "get_image_transfer_config",
        FunctionID.GET_IMAGE_TRANSFER_CONFIG,
        (),
        reply=("B", (3,)),
        result=DEVICE.ImageTransfer.CALLBACK_TEMPERATURE_IMAGE,
    ),
    Call(
        "set_flux_linear_parameters",
        FunctionID.SET_FLUX_LINEAR_PARAMETERS,
        (
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("0.03662109375"),
            Decimal("0.03"),
        ),
        sent=("H H H H H H H H", (82, 3, 82, 3, 82, 3, 3, 3)),
    ),
    Call(
        "set_flux_linear_parameters",
        FunctionID.SET_FLUX_LINEAR_PARAMETERS,
        (
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("0.03662109375"),
            Decimal("0.03"),
            False,
        ),
        sent=("H H H H H H H H", (82, 3, 82, 3, 82, 3, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_flux_linear_parameters",
        FunctionID.GET_FLUX_LINEAR_PARAMETERS,
        (),
        reply=("H H H H H H H H", (82, 4, 82, 6, 82, 8, 9, 10)),
        result=GetFluxLinearParameters(
            Decimal("1.0009765625"),
            Decimal("0.04"),
            Decimal("1.0009765625"),
            Decimal("0.06"),
            Decimal("1.0009765625"),
            Decimal("0.08"),
            Decimal("0.10986328125"),
            Decimal("0.1"),
        ),
    ),
    Call(
        "set_ffc_shutter_mode",
        FunctionID.SET_FFC_SHUTTER_MODE,
        (
            DEVICE.ShutterMode.EXTERNAL,
            DEVICE.ShutterLockout.LOW,
            True,
            True,
            Decimal("0.003"),
            Decimal("0.003"),
            True,
            Decimal("0.03"),
            3,
        ),
        sent=("B B ! ! I I ! H H", (2, 2, True, True, 3, 3, True, 3, 3)),
    ),
    Call(
        "set_ffc_shutter_mode",
        FunctionID.SET_FFC_SHUTTER_MODE,
        (
            DEVICE.ShutterMode.EXTERNAL,
            DEVICE.ShutterLockout.LOW,
            True,
            True,
            Decimal("0.003"),
            Decimal("0.003"),
            True,
            Decimal("0.03"),
            3,
            False,
        ),
        sent=("B B ! ! I I ! H H", (2, 2, True, True, 3, 3, True, 3, 3)),
        response_expected=False,
    ),
    Call(
        "get_ffc_shutter_mode",
        FunctionID.GET_FFC_SHUTTER_MODE,
        (),
        reply=("B B ! ! I I ! H H", (2, 2, True, True, 7, 8, True, 10, 11)),
        result=GetFFCShutterMode(
            DEVICE.ShutterMode.EXTERNAL,
            DEVICE.ShutterLockout.LOW,
            True,
            True,
            Decimal("0.007"),
            Decimal("0.008"),
            True,
            Decimal("0.1"),
            11,
        ),
    ),
    Call("run_ffc_normalization", FunctionID.RUN_FFC_NORMALIZATION, ()),
    Call("run_ffc_normalization", FunctionID.RUN_FFC_NORMALIZATION, (False,), response_expected=False),
]

REJECTED: list[tuple[str, tuple[Any, ...]]] = [
    ("set_resolution", (12345,)),
    ("set_spotmeter_config", (([i % 256 for i in range(4)])[:-1],)),
    ("set_high_contrast_config", (([i % 256 for i in range(4)])[:-1], 3, [3] * 2, 3)),
    ("set_high_contrast_config", ([i % 256 for i in range(4)], 257, [3] * 2, 3)),
    ("set_high_contrast_config", ([i % 256 for i in range(4)], 3, ([3] * 2)[:-1], 3)),
    ("set_high_contrast_config", ([i % 256 for i in range(4)], 3, [3] * 2, 16384)),
    ("set_image_transfer_config", (12345,)),
    (
        "set_flux_linear_parameters",
        (
            Decimal("100.01220703125"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("0.03662109375"),
            Decimal("0.03"),
        ),
    ),
    (
        "set_flux_linear_parameters",
        (
            Decimal("1.0009765625"),
            Decimal("655.36"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("0.03662109375"),
            Decimal("0.03"),
        ),
    ),
    (
        "set_flux_linear_parameters",
        (
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("100.01220703125"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("0.03662109375"),
            Decimal("0.03"),
        ),
    ),
    (
        "set_flux_linear_parameters",
        (
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("655.36"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("0.03662109375"),
            Decimal("0.03"),
        ),
    ),
    (
        "set_flux_linear_parameters",
        (
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("100.01220703125"),
            Decimal("0.03"),
            Decimal("0.03662109375"),
            Decimal("0.03"),
        ),
    ),
    (
        "set_flux_linear_parameters",
        (
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("655.36"),
            Decimal("0.03662109375"),
            Decimal("0.03"),
        ),
    ),
    (
        "set_flux_linear_parameters",
        (
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("100.01220703125"),
            Decimal("0.03"),
        ),
    ),
    (
        "set_flux_linear_parameters",
        (
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("1.0009765625"),
            Decimal("0.03"),
            Decimal("0.03662109375"),
            Decimal("655.36"),
        ),
    ),
    (
        "set_ffc_shutter_mode",
        (12345, DEVICE.ShutterLockout.LOW, True, True, Decimal("0.003"), Decimal("0.003"), True, Decimal("0.03"), 3),
    ),
    (
        "set_ffc_shutter_mode",
        (DEVICE.ShutterMode.EXTERNAL, 12345, True, True, Decimal("0.003"), Decimal("0.003"), True, Decimal("0.03"), 3),
    ),
    (
        "set_ffc_shutter_mode",
        (
            DEVICE.ShutterMode.EXTERNAL,
            DEVICE.ShutterLockout.LOW,
            True,
            True,
            Decimal("4294967.296"),
            Decimal("0.003"),
            True,
            Decimal("0.03"),
            3,
        ),
    ),
    (
        "set_ffc_shutter_mode",
        (
            DEVICE.ShutterMode.EXTERNAL,
            DEVICE.ShutterLockout.LOW,
            True,
            True,
            Decimal("0.003"),
            Decimal("4294967.296"),
            True,
            Decimal("0.03"),
            3,
        ),
    ),
    (
        "set_ffc_shutter_mode",
        (
            DEVICE.ShutterMode.EXTERNAL,
            DEVICE.ShutterLockout.LOW,
            True,
            True,
            Decimal("0.003"),
            Decimal("0.003"),
            True,
            Decimal("655.36"),
            3,
        ),
    ),
    (
        "set_ffc_shutter_mode",
        (
            DEVICE.ShutterMode.EXTERNAL,
            DEVICE.ShutterLockout.LOW,
            True,
            True,
            Decimal("0.003"),
            Decimal("0.003"),
            True,
            Decimal("0.03"),
            65536,
        ),
    ),
]


def test_identity(device: BrickletThermalImaging) -> None:
    """The device knows who it is."""
    assert device.DEVICE_IDENTIFIER.value == 278
    assert device.get_api_version() == (2, 0, 2)
    assert str(device).startswith("Thermal Imaging Bricklet with uid 12345")


def test_ids_match_the_official_bindings() -> None:
    """The ids of all functions and callbacks, that the official bindings know, are the same."""
    for name, value in OFFICIAL_FUNCTION_IDS.items():
        assert FunctionID.__members__[name].value == value, name
    for name, value in OFFICIAL_CALLBACK_IDS.items():
        name = name.removesuffix("_LOW_LEVEL") if name not in CallbackID.__members__ else name
        assert CallbackID.__members__[name].value == value, name


class TestRequests(DeviceTests):
    """The requests of the table `CALLS` and the invalid arguments of the table `REJECTED`."""


def test_get_high_contrast_image_transfers_the_stream(
    device: BrickletThermalImaging, connection: FakeConnection
) -> None:
    """The high-level function get_high_contrast_image() uses get_high_contrast_image_low_level()."""
    data = [i % 256 for i in range(4800)]
    for offset in range(0, 4800, 62):
        connection.reply(FunctionID.GET_HIGH_CONTRAST_IMAGE_LOW_LEVEL, "H 62B", *(offset, chunk(data, offset, 62, 0)))
    result = run(device.get_high_contrast_image())
    assert connection.requests == [request(FunctionID.GET_HIGH_CONTRAST_IMAGE_LOW_LEVEL)] * 78
    assert result == bytes([i % 256 for i in range(4800)])


def test_get_temperature_image_transfers_the_stream(device: BrickletThermalImaging, connection: FakeConnection) -> None:
    """The high-level function get_temperature_image() uses get_temperature_image_low_level()."""
    data = [3] * 4800
    for offset in range(0, 4800, 31):
        connection.reply(FunctionID.GET_TEMPERATURE_IMAGE_LOW_LEVEL, "H 31H", *(offset, chunk(data, offset, 31, 0)))
    result = run(device.get_temperature_image())
    assert connection.requests == [request(FunctionID.GET_TEMPERATURE_IMAGE_LOW_LEVEL)] * 155
    assert result == (3,) * 4800


def test_callback_high_contrast_image(device: BrickletThermalImaging, connection: FakeConnection) -> None:
    """The callback HIGH_CONTRAST_IMAGE is converted to an event."""
    data = [i % 256 for i in range(4800)]
    for offset in range(0, 4800, 62):
        connection.callback(CallbackID.HIGH_CONTRAST_IMAGE, "H 62B", *(offset, chunk(data, offset, 62, 0)))
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [(0, CallbackID.HIGH_CONTRAST_IMAGE)]
    assert events[0].payload == bytes([i % 256 for i in range(4800)])
    connection_2 = FakeConnection()
    connection_2.callback(CallbackID.HIGH_CONTRAST_IMAGE, "H 62B", *(62, chunk(data, 0, 62, 0)))
    assert not read_events(DEVICE(UID, connection_2.ipcon))


def test_callback_temperature_image(device: BrickletThermalImaging, connection: FakeConnection) -> None:
    """The callback TEMPERATURE_IMAGE is converted to an event."""
    data = [3] * 4800
    for offset in range(0, 4800, 31):
        connection.callback(CallbackID.TEMPERATURE_IMAGE, "H 31H", *(offset, chunk(data, offset, 31, 0)))
    events = read_events(device)
    assert [(event.sid, event.function_id) for event in events] == [(1, CallbackID.TEMPERATURE_IMAGE)]
    assert events[0].payload == (3,) * 4800
    connection_2 = FakeConnection()
    connection_2.callback(CallbackID.TEMPERATURE_IMAGE, "H 31H", *(31, chunk(data, 0, 31, 0)))
    assert not read_events(DEVICE(UID, connection_2.ipcon))
