import re
import aiohttp
import logging
import asyncio
import json
import sys

from .info import VERSION

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


async def request(url: str, headers: dict = None) -> dict:
    _url = url.strip(" ")
    if headers is None:
        headers = {}

    retry = 0
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
        """
            From https://gist.github.com/foobarna/19c132304e140bf5031c273f6dc27ece   # noqa: E501
        """

        while True:
            response = await session.request("GET", _url, headers={**get_default_header(), **headers})  # noqa: E501

            if response.status >= 400:
                LOGGER.warning(f"Failure to fetch {_url} ({response.status}) Retry {retry} / {RETRY_MAX}")  # noqa: E501
                retry += 1
                if retry > RETRY_MAX:
                    raise Exception(f"Failed to download {url}")

                await asyncio.sleep(1)
                continue

            break

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

        return {
            "status": response.status,
            "content": json.loads(data)
        }
