"""Tests for the encoding and decoding of the payloads of the Tinkerforge protocol."""

import struct
from typing import Any

import pytest

from tinkerforge_async.ip_connection_helper import (
    base58decode,
    base58encode,
    pack_payload,
    uid64_to_uid32,
    unpack_payload,
)


@pytest.mark.parametrize(
    "uid64, uid32",
    [
        (0, 0),
        (0x0000_0000_0000_0FFF, 0x0000_0FFF),  # The lower 12 bits are kept
        (0x0000_0000_0F00_0000, 0x0000_F000),
        (0x0000_003F_0000_0000, 0x003F_0000),
        (0x000F_0000_0000_0000, 0x03C0_0000),
        (0x3F00_0000_0000_0000, 0xFC00_0000),
        (0x3F0F_003F_0F00_0FFF, 0xFFFF_FFFF),
        (0xC0F0_FFC0_F0FF_F000, 0),  # These bits are dropped
    ],
)
def test_uid64_to_uid32(uid64: int, uid32: int) -> None:
    """The uids of the newer devices have 64 bits. The protocol uses 32 bits of them."""
    assert uid64_to_uid32(uid64) == uid32


@pytest.mark.parametrize(
    "value, encoded",
    [(0, "1"), (1, "2"), (57, "Z"), (58, "21"), (58 * 58 - 1, "ZZ"), (58 * 58, "211"), (12345, "4ER")],
)
def test_base58(value: int, encoded: str) -> None:
    """The uids are printed on the devices in base58. The alphabet has no 0, O, I and l, because they look alike."""
    assert base58encode(value) == encoded
    assert base58decode(encoded) == value


def test_base58_rejects_characters_that_are_not_in_the_alphabet() -> None:
    """A typo in a uid must not result in another uid."""
    with pytest.raises(ValueError):
        base58decode("0")


@pytest.mark.parametrize(
    "form, values, packed",
    [
        ("B", (255,), b"\xff"),
        ("b", (-1,), b"\xff"),
        ("H", (0x1234,), b"\x34\x12"),  # little endian
        ("h", (-2,), b"\xfe\xff"),
        ("I", (0x12345678,), b"\x78\x56\x34\x12"),
        ("i", (-2,), b"\xfe\xff\xff\xff"),
        ("B H", (1, 2), b"\x01\x02\x00"),  # There is no padding
        ("3B", ((1, 2, 3),), b"\x01\x02\x03"),  # A list
        ("2H B", ((1, 2), 3), b"\x01\x00\x02\x00\x03"),
        ("!", (True,), b"\x01"),
        ("!", (False,), b"\x00"),
        ("4!", ((True, False, True, True),), b"\x0d"),  # A list of bools is packed into a bitmask
        ("10!", ((True,) + (False,) * 8 + (True,),), b"\x01\x02"),
        ("c", ("a",), b"a"),
        ("c", (b"a",), b"a"),
        ("3c", (("a", "b", "c"),), b"abc"),
        ("4s", (b"ab",), b"ab\x00\x00"),  # Strings are padded with null bytes
        ("c B !", ("x", 1, True), b"x\x01\x01"),
    ],
)
def test_pack_payload(form: str, values: tuple[Any, ...], packed: bytes) -> None:
    """The values are packed without padding in little endian."""
    assert pack_payload(values, form) == packed


def test_pack_payload_rejects_a_list_of_bools_of_the_wrong_length() -> None:
    """The length of the list is part of the format."""
    with pytest.raises(ValueError, match="bool list length"):
        pack_payload(((True, False),), "4!")


def test_pack_payload_rejects_values_that_do_not_fit() -> None:
    """The errors of the struct module are passed on."""
    with pytest.raises(struct.error):
        pack_payload((256,), "B")


@pytest.mark.parametrize(
    "form, packed, values",
    [
        ("B", b"\xff", 255),  # A single value is not wrapped in a list
        ("b", b"\xff", -1),
        ("H", b"\x34\x12", 0x1234),
        ("i", b"\xfe\xff\xff\xff", -2),
        ("B H", b"\x01\x02\x00", [1, 2]),
        ("3B", b"\x01\x02\x03", (1, 2, 3)),
        ("2H B", b"\x01\x00\x02\x00\x03", [(1, 2), 3]),
        ("!", b"\x01", True),
        ("!", b"\x00", False),
        ("!", b"\x02", True),  # Any value other than 0 is true
        ("4!", b"\x0d", (True, False, True, True)),
        ("10!", b"\x01\x02", (True,) + (False,) * 8 + (True,)),
        ("c", b"a", "a"),
        ("3c", b"abc", ("a", "b", "c")),
        ("4s", b"ab\x00\x00", "ab"),  # The string ends at the first null byte
        ("4s", b"abcd", "abcd"),
        ("4s", b"\x00bcd", ""),
        ("2s", b"\xfc\xff", "üÿ"),  # Strings are decoded as latin-1
        ("c B !", b"x\x01\x01", ["x", 1, True]),
        ("B", b"\x01\x02\x03", 1),  # Extra bytes are ignored
    ],
)
def test_unpack_payload(form: str, packed: bytes, values: Any) -> None:
    """The payload is unpacked to a single value, or a list of values."""
    assert unpack_payload(packed, form) == values


@pytest.mark.parametrize("form, packed", [("", b"\x01"), ("B", b"")])
def test_unpack_payload_without_data(form: str, packed: bytes) -> None:
    """There is nothing to unpack, if the format or the payload is empty."""
    assert unpack_payload(packed, form) is None


def test_unpack_payload_rejects_a_payload_that_is_too_short() -> None:
    """The errors of the struct module are passed on."""
    with pytest.raises(struct.error):
        unpack_payload(b"\x01", "H")


@pytest.mark.parametrize(
    "form, packed, unpacked",
    [
        ("I ! c h h", (1500, True, "x", -100, 200), [1500, True, "x", -100, 200]),
        (
            "8s 8s c 3B 3B H",
            (b"6CRh", b"0", "a", (1, 0, 0), (2, 0, 1), 2113),
            ["6CRh", "0", "a", (1, 0, 0), (2, 0, 1), 2113],
        ),
        (
            "4! 4!",
            ((True, False, False, True), (False, True, True, False)),
            [(True, False, False, True), (False, True, True, False)],
        ),
        ("H H 60B", (5, 0, tuple(range(60))), [5, 0, tuple(range(60))]),
    ],
)
def test_pack_and_unpack_are_inverse(form: str, packed: tuple[Any, ...], unpacked: Any) -> None:
    """What was packed is unpacked to the same values. Strings are packed from bytes."""
    assert unpack_payload(pack_payload(packed, form), form) == unpacked
