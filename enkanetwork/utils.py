"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz
Copyright (c) 2022-present M-307

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

import re
import logging
import sys

from typing import Any, Dict, TYPE_CHECKING

from . import __version__

if TYPE_CHECKING:
    from aiohttp import ClientResponse

LOGGER = logging.getLogger(__name__)

# Base URL
BASE_URL = "https://enka.network/{PATH}"

# Request
CHUNK_SIZE = 5 * 2**20
RETRY_MAX = 10


def create_path(path: str) -> str:
    return BASE_URL.format(PATH=path)


def create_ui_path(filename: str) -> str:
    return create_path(f"ui/{filename}.png")


def validate_uid(uid: str) -> bool:
    """
        Validate UID
    """
    return len(uid) == 9 and uid.isdigit() and re.match(r"([1,2,5-9])\d{8}", uid)


def get_default_header():
    # Get python version
    python_version = sys.version_info

    return {
        "User-Agent": "EnkaNetwork.py/{version} (Python {major}.{minor}.{micro})".format(
            version=__version__,
            major=python_version.major,
            minor=python_version.minor,
            micro=python_version.micro
        ),
    }

class _MissingSentinel:
    __slots__ = ()

    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __hash__(self):
        return 0

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()

async def to_data(response: ClientResponse) -> Dict[str, Any]:

    data = bytearray()
    data_to_read = True
    while data_to_read:
        red = 0
        while red < CHUNK_SIZE:
            chunk = await response.content.read(CHUNK_SIZE - red)

            if not chunk:
                data_to_read = False
                break

            data.extend(chunk)
            red += len(chunk)

    content = {
        "status": response.status,
        "content": data
    }
    return content

