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
DEALINGS IN THE SOFTWARE."""

from __future__ import annotations

import asyncio
import aiohttp
import logging

from typing import (
    Any,
    ClassVar,
    Optional,
    TypeVar,
    Coroutine,
    Dict,
    Union,
    TYPE_CHECKING
)
from . import utils
from .utils import MISSING, RETRY_MAX
from .exception import (
    VaildateUIDError,
    UIDNotFounded,
    HTTPException,
    Forbidden,
    EnkaServerError
)

if TYPE_CHECKING:
    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]
    from .types.enkanetwork import (
        EnkaNetwork as EnkaNetworkPayload,
        Default as DefaultPayload,
    )


class Route:

    BASE_URL: ClassVar[str] = "https://enka.network{PATH}"
    RAW_DATA_URL: ClassVar[str] = "https://raw.githubusercontent.com/mrwan200/enkanetwork.py-data/{PATH}"

    def __init__(
        self,
        method: str,
        path: str,
        endpoint: str = 'enka',
        uid: Optional[str] = None,
    ) -> None:
        self.method = method
        self.uid = uid
        self.url = ''
        
        if endpoint == 'enka':
            self.url: str = self.BASE_URL.format(PATH=path)
        else:
            self.url: str = self.RAW_DATA_URL.format(PATH=path)

class HTTPClient:

    LOGGER = logging.getLogger(__name__)

    def __init__(self, *, key: str = '', agent: str = '', timeout: int = 5) -> None:
        self.__session: aiohttp.ClientSession = MISSING
        self.__headers: Dict = {}
        self.__agent: str = agent
        self.__key: str = key
        self.__timeout = timeout or 10

    async def close(self) -> None:
        if self.__session is not MISSING:
            await self.__session.close()
            self.__session = MISSING
            self.LOGGER.debug('Session closed')
        else:
            self.LOGGER.debug('Session already closed')

    async def request(self, route: Route, **kwargs: Any) -> Any:
        method = route.method
        url = route.url
        uid = route.uid

        self.__headers.clear()
        if self.__agent != '':
            self.__headers['User-Agent'] = self.__agent

        kwargs['headers'] = {**utils.get_default_header(), **self.__headers}

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None

        if self.__session is MISSING:
            self.__session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.__timeout))

        for tries in range(RETRY_MAX):
            try:
                async with self.__session.request(method, url, **kwargs) as response:
                    if 300 > response.status >= 200:
                        data = await utils.to_data(response)

                        if not data['content'] or response.status != 200:
                            raise UIDNotFounded(f"UID {uid} not found.")

                        self.LOGGER.debug('%s %s has received %s', method, url, data)
                        return data

                    if response.status == 500:
                        raise UIDNotFounded(f"UID {uid} not found or Genshin server broken.")

                    # we are being rate limited
                    # if response.status == 429:
                    # Banned by Cloudflare more than likely.

                    if response.status >= 400:
                        self.LOGGER.warning(f"Failure to fetch {url} ({response.status}) Retry {tries} / {RETRY_MAX}")
                        if tries > RETRY_MAX:
                            raise HTTPException(f"Failed to download {url}")
                        await asyncio.sleep(1)  # 1 + tries * 2
                        continue

                    if response.status == 403:
                        raise Forbidden("Forbidden 403")  # TODO: คิดไม่ออกจะพิมพ์อะไร

                    raise HTTPException("Unknown error")

            except OSError as e:
                # Connection reset by peer
                if tries < 4 and e.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise

        if response is not None:
            # We've run out of retries, raise.
            if response.status >= 500:
                raise EnkaServerError("Server error")

            raise HTTPException("Unknown error")

        raise RuntimeError('Unreachable code in HTTP handling')

    def fetch_user(self, uid: Union[str, int]) -> Response[EnkaNetworkPayload]:
        if not utils.validate_uid(str(uid)):
            raise VaildateUIDError("Validate UID failed. Please check your UID.")
        r = Route(
            'GET',
            f'/u/{uid}/__data.json' + (f"?key={self.__key}" if self.__key else ""),
            endpoint='enka',
            uid=uid
        )
        return self.request(r)

    def fetch_asset(self, folder: str, filename: str) -> Response[DefaultPayload]:
        r = Route(
            'GET',
            f'/master/exports/{folder}/{filename}',
            endpoint='assets'
        )
        return self.request(r)

    async def read_from_url(self, url: str) -> bytes:
        async with self.__session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            elif resp.status == 404:
                raise HTTPException(resp, 'asset not found')
            elif resp.status == 403:
                raise Forbidden(resp, 'cannot retrieve asset')
            else:
                raise HTTPException(resp, 'failed to get asset')