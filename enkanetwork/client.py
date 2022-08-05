from __future__ import annotations

import logging
from .http import HTTPClient
from .model import EnkaNetworkResponse
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

    def __init__(self, lang: str = "en", *, debug: bool = False, key: str = "", cache: bool = True, agent: str = "") -> None:  # noqa: E501
        # Logging
        logging.basicConfig()
        logging.getLogger("enkanetwork").setLevel(logging.DEBUG if debug else logging.ERROR)  # noqa: E501

        # Set language and load config
        self.assets = Assets(lang)

        # Cache
        self._enable_cache = cache
        self.cache = Cache(1024, 60 * 3)

        # http client
        self.__http = HTTPClient(key=key, agent=agent)
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
            self.LOGGER.warn("Getting data from cache...")
            data = await self.cache.get(uid)

            if data is not None:
                # Return data
                self.LOGGER.debug("Parsing data...")
                return EnkaNetworkResponse.parse_obj(data)

        user = await self.__http.fetch_user(uid)

        data = user["content"]

        self.LOGGER.debug(f"Fetching user with UID {uid}...")

        if self._enable_cache:
            self.LOGGER.debug("Caching data...")
            await self.cache.set(uid, data)

        # Return data
        self.LOGGER.debug("Parsing data...")
        return EnkaNetworkResponse.parse_obj(data)

    async def update_assets(self) -> None:
        print("Updating assets...")
        self.LOGGER.debug("Downloading new content...")

        # get path
        path = Assets._get_path_assets()

        # update assets
        await self.__http.update_asset(path)

        # Reload config
        self.assets.reload_assets()
