#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ##### BEGIN GPL LICENSE BLOCK #####
#
# Copyright (C) 2021  Patrick Baus
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####
"""
The lab temperature controller uses a PID controller and the Tinkerforge sensors to regulate
the room temperature.
"""

import argparse

from tinkerforge_async.ip_connection_helper import base58decode, base58encode


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [UID]...",
        description="Convert Tinkerforge base58 encoded uids to ints"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('uids', nargs='+')
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
