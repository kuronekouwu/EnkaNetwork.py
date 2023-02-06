from __future__ import annotations

import os
import json
import logging

from .http import HTTPClient
from .model.base import (
    EnkaNetworkResponse,
    EnkaNetworkProfileResponse
)
from .model.hoyos import PlayerHoyos
from .model.build import Builds

from .assets import Assets
from .enum import Language
from .cache import Cache
from .config import Config

from typing import Union, Optional, Type, TYPE_CHECKING, List, Any

if TYPE_CHECKING:
    from typing_extensions import Self
    from types import TracebackType

__all__ = ("EnkaNetworkAPI",)


class EnkaNetworkAPI:
    LOGGER = logging.getLogger(__name__)

    def __init__(self, lang: str = "en", *, debug: bool = False, key: str = "", cache: bool = True, user_agent: str = "", timeout: int = 10) -> None:  # noqa: E501
        # Logging
        logging.basicConfig()
        logging.getLogger("enkanetwork").setLevel(logging.DEBUG if debug else logging.ERROR)  # noqa: E501

        # Set language and load config
        self.assets = Assets(lang)

        # Cache
        self._enable_cache = cache
        if self._enable_cache:
            Config.init_cache(Cache(1024, 60 * 3))

        # http client
        self.__http = HTTPClient(key=key, agent=user_agent, timeout=timeout)
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
        Config.init_cache(cache)

    async def set_language(self, lang: Language) -> None:
        self.lang = lang

    async def fetch_user_by_uid(
        self,
        uid: Union[str, int],
        *,
        info: bool = False
    ) -> EnkaNetworkResponse:
        if self._enable_cache:
            self.LOGGER.warning("Getting data from cache...")
            data = await Config.CACHE.get(uid)

            if data is not None:
                # Return data
                self.LOGGER.debug("Parsing data...")
                return EnkaNetworkResponse.parse_obj(data)

        self.LOGGER.debug(f"Fetching user with UID {uid}...")
        user = await self.__http.fetch_user_by_uid(uid, info=info)

        data = user["content"]
        data = json.loads(data)

        if self._enable_cache:
            self.LOGGER.debug("Caching data...")
            await Config.CACHE.set(uid, data)

        # Return data
        self.LOGGER.debug("Parsing data...")
        if "owner" in data:
            data["owner"] = {
                **data["owner"],
                "builds": await self.fetch_builds(
                    profile_id=data["owner"]["username"], 
                    metaname=data["owner"]["hash"]
                )
            }

        return EnkaNetworkResponse.parse_obj(data)

    async def fetch_user_by_username(
        self,
        profile_id: Union[str, int]
    ) -> EnkaNetworkProfileResponse:
        if self._enable_cache:
            self.LOGGER.warning("Getting data from cache...")
            data = await Config.CACHE.get(profile_id)

            if data is not None:
                # Return data
                self.LOGGER.debug("Parsing data...")
                return EnkaNetworkProfileResponse.parse_obj(data)

        self.LOGGER.debug(f"Fetching user with profile {profile_id}...")

        user = await self.__http.fetch_user_by_username(profile_id)
        data = user["content"]
        data = json.loads(data)

        if self._enable_cache:
            self.LOGGER.debug("Caching data...")
            await Config.CACHE.set(profile_id, data)

        # Return data
        self.LOGGER.debug("Parsing data...")
        return EnkaNetworkProfileResponse.parse_obj({
            **data,
            "hoyos": await self.fetch_hoyos_by_username(profile_id)
        })

    async def fetch_hoyos_by_username(
        self,
        profile_id: Union[str, int]
    ) -> List[PlayerHoyos]:
        key = profile_id + ":hoyos"
        # Check config
        if Config.CACHE_ENABLED:
            self.LOGGER.warning("Getting data from cache...")
            data = await Config.CACHE.get(key)

            if data is not None:
                self.LOGGER.debug("Parsing data...")
                return await self.__format_hoyos(profile_id, data)

        self.LOGGER.debug(f"Fetching user hoyos with profile {profile_id}...")
        user = await self.__http.fetch_hoyos_by_username(profile_id)
        data = user["content"]
        data = json.loads(data)

        if Config.CACHE_ENABLED:
            self.LOGGER.debug("Caching data...")
            await Config.CACHE.set(key, data)

        self.LOGGER.debug("Parsing data...")
        return await self.__format_hoyos(profile_id, data)

    async def fetch_builds(
        self,
        *,
        profile_id: Union[str, int],
        metaname: Union[str, int]
    ) -> PlayerHoyos:
        key = profile_id + ":hoyos:" + metaname + ":builds"
        # Check config
        if Config.CACHE_ENABLED:
            self.LOGGER.warning("Getting data from cache...")
            data = await Config.CACHE.get(key)

            if data is not None:
                self.LOGGER.debug("Parsing data...")
                return await self.__format_hoyos(profile_id, data)

        # Request data first
        user = await self.__http.fetch_hoyos_by_username(profile_id,metaname,True)
        data = user["content"]
        data = json.loads(data)

        if Config.CACHE_ENABLED:
            self.LOGGER.debug("Caching data...")
            await Config.CACHE.set(key, data)

        self.LOGGER.debug("Parsing data...")
        return Builds.parse_obj(data)

    async def request_enka():
        pass

    async def update_assets(self) -> None:
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
                    json.dump(json.loads(data["content"]),
                              f, ensure_ascii=False, indent=4)

        # Reload config
        self.assets.reload_assets()
    
    async def __format_hoyos(self, username: str, data: List[Any]) -> List[PlayerHoyos]:
        return [PlayerHoyos.parse_obj({
            "builds": await self.fetch_builds(profile_id=username, metaname=data[key]["hash"]),
            **data[key]
        }) for key in data]

    # Concept by genshin.py python library
    fetch_user = fetch_user_by_uid
    fetch_profile = fetch_user_by_username
