from __future__ import annotations

import os
import json
import logging
import warnings

from .http import HTTPClient
from .model.base import EnkaNetworkResponse
from .assets import Assets
from .enum import Language
from .cache import Cache

from typing import Union, Optional, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self
    from types import TracebackType

__all__ = ("EnkaNetworkAPI",)

class EnkaNetworkAPI:

    LOGGER = logging.getLogger(__name__)

    def __init__(self, lang: str = "en", *, debug: bool = False, key: str = "", cache: bool = True, agent: str = "", timeout: int = 10) -> None:  # noqa: E501
        # Logging
        logging.basicConfig()
        logging.getLogger("enkanetwork").setLevel(logging.DEBUG if debug else logging.ERROR)  # noqa: E501

        # Set language and load config
        self.assets = Assets(lang)

        # Cache
        self._enable_cache = cache
        self.cache = Cache(1024, 60 * 3)

        # http client
        self.__http = HTTPClient(key=key, agent=agent, timeout=timeout)
        self._closed = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_value: Optional[BaseException],
            traceback: Optional[TracebackType],
    ) -> None:
        self._close = True
        if self._close:
            await self.__http.close()

    def is_closed(self) -> bool:
        return self._closed

    @property
    def http(self) -> HTTPClient:
        return self.__http

    @http.setter
    def http(self, http: HTTPClient) -> None:
        self.__http = http

    @property
    def lang(self) -> Language:
        return self.assets.LANGS

    @lang.setter
    def lang(self, lang: Language) -> None:
        self.assets._set_language(lang)

    def set_cache(self, cache: Cache) -> None:
        self.cache = cache

    async def set_language(self, lang: Language) -> None:
        self.lang = lang

    async def fetch_user(self, uid: Union[str, int]) -> EnkaNetworkResponse:
        self.LOGGER.debug(f"Validating with UID {uid}...")

        if self._enable_cache:
            self.LOGGER.warning("Getting data from cache...")
            data = await self.cache.get(uid)

            if data is not None:
                # Return data
                self.LOGGER.debug("Parsing data...")
                return EnkaNetworkResponse.parse_obj(data)

        user = await self.__http.fetch_user(uid)

        data = user["content"]
        data = json.loads(data)

        self.LOGGER.debug(f"Fetching user with UID {uid}...")

        if self._enable_cache:
            self.LOGGER.debug("Caching data...")
            await self.cache.set(uid, data)

        # Return data
        self.LOGGER.debug("Parsing data...")
        return EnkaNetworkResponse.parse_obj(data)

    async def update_assets(self) -> None:
        warnings.warn("enkanetwork.py-data will be public archived and will not update util found new source. Please read reason in https://github.com/mrwan200/enkanetwork.py-data#attemption")
        print("Updating assets...")
        self.LOGGER.debug("Downloading new content...")

        path = Assets._get_path_assets()
        for folder in path:
            for filename in os.listdir(path[folder]):
                self.LOGGER.debug(f"Downloading {folder} file {filename}...")

                data = await self.__http.fetch_asset(folder, filename)

                self.LOGGER.debug(f"Writing {folder} file {filename}...")

                # dumps to json file
                with open(os.path.join(path[folder], filename), "w", encoding="utf-8") as f:
                    json.dump(json.loads(data["content"]), f, ensure_ascii=False, indent=4)

        # Reload config
        self.assets.reload_assets()
