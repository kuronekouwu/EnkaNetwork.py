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
import warnings

from typing import (
    Any,
    Optional,
    TypeVar,
    Coroutine,
    Dict,
    Union,
    TYPE_CHECKING
)
from . import utils
from .config import Config
from .utils import MISSING, RETRY_MAX
from .exception import (
    VaildateUIDError,
    HTTPException,
    EnkaServerError,
    EnkaServerUnknown,
    TimedOut,
    ERROR_ENKA
)

if TYPE_CHECKING:
    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]
    from .types.enkanetwork import (
        EnkaNetwork as EnkaNetworkPayload,
        Default as DefaultPayload,
    )


class Route:
    def __init__(
        self,
        method: str,
        path: str,
        endpoint: str = 'enka',
        username: Optional[str] = None
    ) -> None:
        self.method = method
        self.url = ''
        self.username = username

        if endpoint == 'enka':
            self.url: str = Config.ENKA_PROTOCOL + "://" + Config.ENKA_URL + path
        else:
            self.url: str = Config.ASSETS_PROTOCOL + "://" + Config.ASSETS_URL + path


class HTTPClient:
    LOGGER = logging.getLogger(__name__)

    def __init__(self, *, key: str = '', agent: str = '', timeout: int = 5) -> None:  # noqa
        self.__session: aiohttp.ClientSession = MISSING
        self.__headers: Dict = {}
        self.__timeout = timeout or 10

        # Init User Agent
        if agent != '':
            Config.init_user_agent(agent)

        if key != '':
            warnings.warn("'key' has depercated.")

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
        username = route.username

        self.__headers.clear()
        if Config.USER_AGENT != '':
            self.__headers['User-Agent'] = Config.USER_AGENT

        kwargs['headers'] = self.__headers

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None

        if self.__session is MISSING:
            self.__session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.__timeout))

        for tries in range(RETRY_MAX):
            try:
                async with self.__session.request(method, url, **kwargs) as response: # noqa

                    _host = response.host
                    if 300 > response.status >= 200:
                        data = await utils.to_data(response)

                        self.LOGGER.debug(
                            '%s %s has received %s', method, url, data)
                        return data

                    if _host == Config.ENKA_URL:
                        err = ERROR_ENKA.get(response.status, None)
                        if err:
                            raise err[0](err[1].format(uid=username))

                        raise EnkaServerUnknown(
                            f"Unknow error HTTP status: {response.status}")

                    if response.status >= 400:
                        self.LOGGER.warning(
                            f"Failure to fetch {url} ({response.status}) Retry {tries} / {RETRY_MAX}") # noqa
                        if tries > RETRY_MAX:
                            raise HTTPException(f"Failed to download {url}")
                        await asyncio.sleep(1)  # 1 + tries * 2
                        continue

                    raise HTTPException("Unknown error")

            except OSError as e:
                # Connection reset by peer
                if tries < 4 and e.errno in (54, 10054):
                    await asyncio.sleep(1 + tries * 2)
                    continue
                raise TimedOut("Timeout from enka.network")

        if response is not None:
            # We've run out of retries, raise.
            if response.status >= 500:
                raise EnkaServerError("Server error")

            raise HTTPException("Unknown error")

        raise RuntimeError('Unreachable code in HTTP handling')

    def fetch_user_by_uid(
        self,
        uid: Union[str, int],
        *,
        info: bool = False
    ) -> Response[EnkaNetworkPayload]:
        if not utils.validate_uid(str(uid)):
            raise VaildateUIDError(
                "Validate UID failed. Please check your UID.")

        r = Route(
            'GET',
            f'/api/uid/{uid}' + ("?info" if info else ""),
            endpoint='enka',
            username=uid
        )
        return self.request(r)

    def fetch_user_by_username(
        self,
        username: Union[str, int]
    ) -> Response[EnkaNetworkPayload]:
        r = Route(
            'GET',
            f'/api/profile/{username}',
            endpoint='enka',
            username=username
        )
        return self.request(r)

    def fetch_hoyos_by_username(
        self,
        username: Union[str, int],
        metaname: str = "",
        show_build: bool = False
    ):
        r = Route(
            'GET',
            f'/api/profile/{username}/hoyos'
            + (f"/{metaname}" if metaname != '' else '')
            + ('/builds' if (show_build and metaname != '') else ''),
            endpoint='enka',
            username=username
        )
        return self.request(r)

    def fetch_asset(self, folder: str, filename: str) -> Response[DefaultPayload]: # noqa
        r = Route(
            'GET',
            f'/mrwan200/enkanetwork.py-data/master/exports/{folder}/{filename}', # noqa
            endpoint='assets'
        )
        return self.request(r)

    async def read_from_url(self, url: str) -> bytes:
        async with self.__session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
            elif resp.status == 404:
                raise HTTPException(resp, 'asset not found')
            else:
                raise HTTPException(resp, 'failed to get asset')
