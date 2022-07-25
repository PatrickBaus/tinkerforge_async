"""
Some helper functions to encode and decode Tinkerforge protocol payloads.
"""
from __future__ import annotations

import math
import struct
from typing import Any

# The following code is taken from the original Tinkerforge ip_connection.py
# noinspection SpellCheckingInspection
BASE58 = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ"


def uid64_to_uid32(uid64: int) -> int:
    value1 = uid64 & 0xFFFFFFFF
    value2 = (uid64 >> 32) & 0xFFFFFFFF

    uid32 = value1 & 0x00000FFF
    uid32 |= (value1 & 0x0F000000) >> 12
    uid32 |= (value2 & 0x0000003F) << 16
    uid32 |= (value2 & 0x000F0000) << 6
    uid32 |= (value2 & 0x3F000000) << 2

    return uid32


def base58encode(value: int) -> str:
    encoded = ""

    while value >= 58:
        div, mod = divmod(value, 58)
        encoded = BASE58[mod] + encoded
        value = div

    return BASE58[value] + encoded


def base58decode(encoded: str) -> int:
    value = 0
    column_multiplier = 1

    for character in encoded[::-1]:
        column = BASE58.index(character)
        value += column * column_multiplier
        column_multiplier *= 58

    return value


def pack_payload(data: tuple[Any, ...], form: str) -> bytes:  # pylint: disable=too-many-branches
    packed = b""

    for format_str, data_unpacked in zip(form.split(" "), data):
        if "!" in format_str:
            if len(format_str) > 1:
                if int(format_str.replace("!", "")) != len(data_unpacked):
                    raise ValueError("Incorrect bool list length")

                packed_bools = [0] * int(math.ceil(len(data_unpacked) / 8.0))

                for i, bool_value in enumerate(data_unpacked):
                    if bool_value:
                        packed_bools[i // 8] |= 1 << (i % 8)

                packed += struct.pack(f"<{len(packed_bools)}B", *packed_bools)
            else:
                packed += struct.pack("<?", data_unpacked)
        elif "c" in format_str:
            if len(format_str) > 1:
                packed += struct.pack("<" + format_str, *list(map(lambda char: bytes([ord(char)]), data_unpacked)))
            else:
                packed += struct.pack("<" + format_str, bytes([ord(data_unpacked)]))
        elif "s" in format_str:
            packed += struct.pack("<" + format_str, data_unpacked)
        elif len(format_str) > 1:
            packed += struct.pack("<" + format_str, *data_unpacked)
        else:
            packed += struct.pack("<" + format_str, data_unpacked)

    return packed


def unpack_payload(data: bytes, form: str) -> Any:  # pylint: disable=too-many-branches
    ret = []
    if not form or len(data) == 0:
        return None

    for format_str in form.split(" "):
        # We need to decode the TF format string to the standard Python format string
        struct_format_str = format_str

        if "!" in struct_format_str:
            if len(struct_format_str) > 1:
                struct_format_str = f"{int(math.ceil(int(struct_format_str.replace('!', '')) / 8.0))}B"
            else:
                struct_format_str = "B"

        struct_format_str = "<" + struct_format_str
        length = struct.calcsize(struct_format_str)
        data_unpacked = struct.unpack(struct_format_str, data[:length])

        if "!" in format_str:
            temp_array = []

            if len(format_str) > 1:
                for i in range(int(format_str.replace("!", ""))):
                    temp_array.append(data_unpacked[i // 8] & (1 << (i % 8)) != 0)
            else:
                temp_array.append(data_unpacked[0] != 0)

            data_unpacked = tuple(temp_array)

        if "c" in struct_format_str:
            if len(data_unpacked) > 1:
                ret.append(tuple(map(lambda item: chr(ord(item)), data_unpacked)))
            else:
                ret.append(chr(ord(data_unpacked[0])))  # type: ignore
        elif "s" in struct_format_str:
            # convert from byte-array to string, removing all null bytes
            ret.append(str(data_unpacked[0], "latin-1").partition("\0")[0])  # type: ignore

        elif len(data_unpacked) > 1:
            ret.append(data_unpacked)
        else:
            ret.append(data_unpacked[0])

        data = data[length:]

    if len(ret) == 1:
        return ret[0]
    return ret
