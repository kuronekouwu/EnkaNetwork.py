from __future__ import annotations

import os
import json
import logging

from typing import Union, Optional, Type, TYPE_CHECKING, List, Any, Dict

from .http import HTTPClient
from .model.base import (
    EnkaNetworkResponse,
    EnkaNetworkProfileResponse
)
from .model.hoyos import PlayerHoyos
from .model.build import Builds

from .assets import Assets
from .enum import Language
from .cache import Cache, StaticCache
from .config import Config
from .tools import (
    merge_raw_data
)

if TYPE_CHECKING:
    from typing_extensions import Self
    from types import TracebackType

__all__ = ("EnkaNetworkAPI",)


class EnkaNetworkAPI:
    """

    A library for API wrapper player by UID / Username
    from https://enka.network

    Parameters
    ------------
    lang: :class:`str`
        Init default language
    debug: :class:`bool`
        If set to `True`. In request data or get assets.
        It's will be shown log processing
    key: :class:`str`
        Depercated
    cache: :class:`bool`
        If set to `True`. In response data will be cache data
    user_agent: :class:`str`
        User-Agent for speical to request Enka.Network
    timeout: :class:`int`
        Request timeout to Enka.Network

    Attributes
    ------------
    assets: :class:`Assets`
        Assets character / artifact / namecards / language / etc. data
    http: :class:`HTTPClient`
        HTTP for request and handle data
    lang: :class:`Language`
        A default language

    Example
    ------------
    ```py
    import asyncio

    from enkanetwork import EnkaNetworkAPI

    client = EnkaNetworkAPI(lang="th",user_agent="SpeicalAgent/1.0")

    async def main():
        async with client:
            data = await client.fetch_user(843715177)
            print(data.player.nickname)

    asyncio.run(main())
    ```
    """
    LOGGER = logging.getLogger(__name__)

    def __init__(
        self,
        *,
        lang: str = "en",
        debug: bool = False,
        key: str = "",
        cache: bool = True,
        user_agent: str = "",
        timeout: int = 10
    ) -> None:  # noqa: E501
        # Logging
        logging.basicConfig()
        logging.getLogger("enkanetwork").setLevel(logging.DEBUG if debug else logging.ERROR)  # noqa: E501

        # Set language and load config
        self.assets = Assets(lang)

        # Cache
        self._enable_cache = cache
        if self._enable_cache:
            Config.init_cache(StaticCache(1024, 60 * 1))

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
        self._closed = True
        if self._closed:
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
        """ Fetch user profile by UID

        Parameters
        ------------
        uid: Union[:class:`str`,:class:`int`]
            UID player in-game
        info: :class:`bool`
            If set to `True`. It's will response player info only

        Raises
        ------------
        VaildateUIDError
            Player UID empty/format has incorrect.
        EnkaPlayerNotFound
            Player UID doesn't not exists in-game
        EnkaServerRateLimit
            Enka.Network has been rate limit
        EnkaServerMaintanance
            Enka.Network has maintenance server
        EnkaServerError
            Enka.Network has server error (The reason normal is `general`)
        EnkaServerUnknown
            Enka.Network has error another

        Returns
        ------------
        :class:`EnkaNetworkResponse`
            The response player data
        """

        # Loda cache
        cache = await self.__get_cache(uid)
        if cache:
            return EnkaNetworkResponse.model_validate(cache)

        data = await self.__http.fetch_user_by_uid(uid, info=info)
        data = self.__format_json(data)

        # Return data
        self.LOGGER.debug("Parsing data...")

        # Store cache
        await self.__store_cache(uid, data)

        if "owner" in data:
            data["owner"] = {
                **data["owner"],
                "builds": await self.fetch_builds(
                    profile_id=data["owner"]["username"],
                    metaname=data["owner"]["hash"]
                )
            }

        return EnkaNetworkResponse.model_validate(data)

    async def fetch_user_by_username(
        self,
        profile_id: Optional[str]
    ) -> EnkaNetworkProfileResponse:
        """ Fetch user profile by Username / patreon ID

        Parameters
        ------------
        profile_id: Optional[:class:`str`]
            Username / patreon ID has subscriptions in Enka.Network

        Raises
        ------------
        EnkaPlayerNotFound
            Player UID doesn't not exists in-game
        EnkaServerRateLimit
            Enka.Network has been rate limit
        EnkaServerMaintanance
            Enka.Network has maintenance server
        EnkaServerError
            Enka.Network has server error (The reason normal is `general`)
        EnkaServerUnknown
            Enka.Network has error another

        Returns
        ------------
        :class:`EnkaNetworkProfileResponse`
            The response profile / hoyos and builds data
        """
        # Loda cache
        cache = await self.__get_cache(profile_id)
        if cache:
            return EnkaNetworkProfileResponse.model_validate(cache)

        data = await self.__http.fetch_user_by_username(profile_id)
        data = self.__format_json(data)

        self.LOGGER.debug("Parsing data...")

        # Store cache
        await self.__store_cache(profile_id, data)

        # Fetch hoyos and build(s)
        data = {
            **data,
            "hoyos": await self.fetch_hoyos_by_username(profile_id)
        }

        return EnkaNetworkProfileResponse.model_validate(data)

    async def fetch_hoyos_by_username(
        self,
        profile_id: Optional[str]
    ) -> List[PlayerHoyos]:
        """ Fetch hoyos user data by Username / patreon ID

        Parameters
        ------------
        profile_id: Optional[:class:`str`]
            Username / patreon ID has subscriptions in Enka.Network

        Raises
        ------------
        EnkaPlayerNotFound
            Player UID doesn't not exists in-game
        EnkaServerRateLimit
            Enka.Network has been rate limit
        EnkaServerMaintanance
            Enka.Network has maintenance server
        EnkaServerError
            Enka.Network has server error (The reason normal is `general`)
        EnkaServerUnknown
            Enka.Network has error another

        Returns
        ------------
        List[:class:`PlayerHoyos`]
            A response hoyos player data
        """
        key = profile_id + ":hoyos"

        # Loda cache
        cache = await self.__get_cache(key)
        if cache:
            return self.__format_hoyos(profile_id, cache)

        data = await self.__http.fetch_hoyos_by_username(profile_id)
        data = self.__format_json(data)
        self.LOGGER.debug("Parsing data...")

        # Store cache
        await self.__store_cache(key, data)

        return await self.__format_hoyos(profile_id, data)

    async def fetch_builds(
        self,
        *,
        profile_id: Optional[str],
        metaname: Optional[str]
    ) -> Builds:
        """ Fetch hoyos build(s) data

        Parameters
        ------------
        profile_id: Optional[:class:`str`]
            Username / patreon ID has subscriptions in Enka.Network
        metaname: Optional[:class:`str`]
            Metaname from hoyos data or owner tag in hash field

        Raises
        ------------
        EnkaPlayerNotFound
            Player UID doesn't not exists in-game
        EnkaServerRateLimit
            Enka.Network has been rate limit
        EnkaServerMaintanance
            Enka.Network has maintenance server
        EnkaServerError
            Enka.Network has server error (The reason normal is `general`)
        EnkaServerUnknown
            Enka.Network has error another

        Returns
        ------------
        :class:`Builds`
            A response builds data
        """
        key = profile_id + ":hoyos:" + metaname + ":builds"
        # Loda cache
        cache = await self.__get_cache(key)
        if cache:
            return Builds.model_validate(cache)

        data = await self.__http.fetch_hoyos_by_username(
            profile_id, metaname, True)
        data = self.__format_json(data)
        self.LOGGER.debug("Parsing data...")

        # Store cache
        await self.__store_cache(key, data)

        return Builds.model_validate(data)

    async def fetch_raw_data(self, uid: Union[str, int], *, info: bool = False) -> Dict[str, Any]:  # noqa
        """Fetches raw data for a user with the given UID. """

        # Loda cache
        cache = await self.__get_cache(uid)
        if cache:
            return cache

        data = await self.__http.fetch_user_by_uid(uid, info=info)
        data = self.__format_json(data)

        # Store cache
        await self.__store_cache(uid, data, cache=cache)

        return data

    async def sync_build(self, uid: Union[str, int], old_data: Dict[str, Any]) -> Dict[str, Any]:  # noqa
        """ Sync build data

        Parameters
        ----------
            uid: Union[:class:`str`,:class:`int`]
                The UID of the user to fetch data for.
            old_data: Dict[:class:`str`, Any]
                The build old data.

        Returns
        ------
            A dictionary containing the merged data.
        """

        new_data = await self.fetch_raw_data(uid)
        return await merge_raw_data(new_data, old_data)

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
                with open(os.path.join(path[folder], filename), "w",
                          encoding="utf-8") as f:
                    json.dump(json.loads(data["content"]),
                              f, ensure_ascii=False, indent=4)

        # Reload config
        self.assets.reload_assets()

    async def __format_hoyos(self, username: str, data: List[Any]) -> List[PlayerHoyos]:  # noqa
        return [PlayerHoyos.model_validate({
            "builds": await self.fetch_builds(profile_id=username,
                                              metaname=data[key]["hash"]),
            **data[key]
        }) for key in data]

    def __format_json(self, data: Any):
        data = data["content"]
        return json.loads(data)

    async def __get_cache(
        self,
        cache_key: str,
    ):
        key = cache_key
        # Check config
        if Config.CACHE_ENABLED:
            self.LOGGER.warning(f"Getting data {key} from cache...")
            data = await Config.CACHE.get(key)

            if data is not None:
                self.LOGGER.debug("Parsing data...")
                return data

        return data

    async def __store_cache(self, key: str, data: Any, *, cache: Any = None):
        if Config.CACHE_ENABLED:
            self.LOGGER.debug(f"Caching data {key}...")
            if cache is None:
                await Config.CACHE.set(key, data)
            else:
                await Config.CACHE.set(key, await self.merge_raw_data(data,
                                                                      cache_data=cache))  # noqa

    # Concept by genshin.py python library
    fetch_user = fetch_user_by_uid
    fetch_profile = fetch_user_by_username
    merge_raw_data = merge_raw_data
