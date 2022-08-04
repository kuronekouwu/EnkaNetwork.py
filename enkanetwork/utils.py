from __future__ import annotations

import re
import aiohttp
import logging
import asyncio
import json
import sys

from typing import Any, Dict, TYPE_CHECKING

from .info import VERSION

if TYPE_CHECKING:
    from aiohttp import ClientResponse

LOGGER = logging.getLogger(__name__)

# Base URL
BASE_URL = "https://enka.network/{PATH}"

# Request
CHUNK_SIZE = 1024 * 1024 * 1
RETRY_MAX = 10


def create_path(path: str) -> str:
    return BASE_URL.format(PATH=path)


def create_ui_path(filename: str) -> str:
    return create_path(f"ui/{filename}.png")


def validate_uid(uid: str) -> bool:
    """
        Validate UID
    """
    return len(uid) == 9 and uid.isdigit() and re.match(r"([1,2,5-9])\d{8}", uid)  # noqa: E501


def get_default_header():
    # Get python version
    python_version = sys.version_info

    return {
        "User-Agent": "EnkaNetwork.py/{version} (Python {major}.{minor}.{micro})".format(  # noqa: E501
            version=VERSION,
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
        "content": json.loads(data)
    }
    return content

