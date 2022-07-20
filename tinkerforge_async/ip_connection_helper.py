"""
Some helper functions to encode and decode Tinkerforge protocol payloads.
"""
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

    for c in encoded[::-1]:
        column = BASE58.index(c)
        value += column * column_multiplier
        column_multiplier *= 58

    return value


def pack_payload(data: tuple[Any, ...], form: str) -> bytes:
    packed = b""

    for f, d in zip(form.split(" "), data):
        if "!" in f:
            if len(f) > 1:
                if int(f.replace("!", "")) != len(d):
                    raise ValueError("Incorrect bool list length")

                p = [0] * int(math.ceil(len(d) / 8.0))

                for i, b in enumerate(d):
                    if b:
                        p[i // 8] |= 1 << (i % 8)

                packed += struct.pack("<{0}B".format(len(p)), *p)
            else:
                packed += struct.pack("<?", d)
        elif "c" in f:
            if len(f) > 1:
                packed += struct.pack("<" + f, *list(map(lambda char: bytes([ord(char)]), d)))
            else:
                packed += struct.pack("<" + f, bytes([ord(d)]))
        elif "s" in f:
            packed += struct.pack("<" + f, d)
        elif len(f) > 1:
            packed += struct.pack("<" + f, *d)
        else:
            packed += struct.pack("<" + f, d)

    return packed


def unpack_payload(data: bytes, form: str) -> Any:
    ret = []
    if not form or len(data) == 0:
        return None

    for f in form.split(" "):
        o = f

        if "!" in f:
            if len(f) > 1:
                f = "{0}B".format(int(math.ceil(int(f.replace("!", "")) / 8.0)))
            else:
                f = "B"

        f = "<" + f
        length = struct.calcsize(f)
        x = struct.unpack(f, data[:length])

        if "!" in o:
            y = []

            if len(o) > 1:
                for i in range(int(o.replace("!", ""))):
                    y.append(x[i // 8] & (1 << (i % 8)) != 0)
            else:
                y.append(x[0] != 0)

            x = tuple(y)

        if "c" in f:
            if len(x) > 1:
                ret.append(tuple(map(lambda item: chr(ord(item)), x)))
            else:
                ret.append(chr(ord(x[0])))
        elif "s" in f:
            # convert from byte-array to string, removing all null bytes
            # Note: This works only in Python 3
            s = str(x[0], "latin-1").partition("\0")[0]

            # strip null bytes
            ret.append(s)

        elif len(x) > 1:
            ret.append(x)
        else:
            ret.append(x[0])

        data = data[length:]

    if len(ret) == 1:
        return ret[0]
    else:
        return ret
