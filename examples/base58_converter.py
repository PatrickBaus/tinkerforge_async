#!/usr/bin/env python3
"""
An example, that shows how to convert the Tinkerforge UIDs into integers used by the Tinkerforge Async library.
"""

import argparse

from tinkerforge_async.ip_connection_helper import base58decode, base58encode


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [UID]...", description="Convert Tinkerforge base58 encoded uids to ints"
    )
    parser.add_argument("-v", "--version", action="version", version=f"{parser.prog} version 1.0.0")
    parser.add_argument("uids", nargs="+")
    return parser


def main() -> None:
    parser = init_argparse()
    args = parser.parse_args()
    for uid in args.uids:
        try:
            print(base58encode(int(uid)))
        except ValueError:
            print(base58decode(uid))


main()
