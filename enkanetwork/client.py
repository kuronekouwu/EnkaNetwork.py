import logging
import os
import json

from typing import Union

from .model import EnkaNetworkResponse
from .exception import VaildateUIDError, UIDNotFounded
from .assets import Assets
from .utils import create_path, validate_uid, request
from .enum import Language
from .cache import Cache


class EnkaNetworkAPI:
    LOGGER = logging.getLogger(__name__)
    RAWDATA = "https://raw.githubusercontent.com/mrwan200/enkanetwork.py-data/{PATH}"  # noqa: E501

    def __init__(self, lang: str = "en", debug: bool = False, key: str = "", cache: bool = True, agent: str = "") -> None:  # noqa: E501
        # Logging
        logging.basicConfig()
        logging.getLogger("enkanetwork").setLevel(logging.DEBUG if debug else logging.ERROR)  # noqa: E501

        # Set language and load config
        self.assets = Assets(lang)

        # Cache
        self._enable_cache = cache
        self.cache = Cache(1024, 60 * 3)

        # Custom User-Agent
        self.__agent = agent

        # Key
        self.__key = key

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
        if not validate_uid(str(uid)):
            raise VaildateUIDError("Validate UID failed. Please check your UID.")  # noqa: E501

        self.LOGGER.debug(f"Fetching user with UID {uid}...")

        if self._enable_cache:
            self.LOGGER.warn("Getting data from cache...")
            data = await self.cache.get(uid)

            if data is not None:
                # Return data
                self.LOGGER.debug("Parsing data...")
                return EnkaNetworkResponse.parse_obj(data)

        headers = {}
        if self.__agent != "":
            headers["User-Agent"] = self.__agent

        resp = await request(url=create_path(f"u/{uid}/__data.json" + ("?key={key}" if self.__key else "")), headers=headers)  # noqa: E501

        # Check if status code is not 200 (Ex. 500)
        if resp["status"] != 200:
            raise UIDNotFounded(f"UID {uid} not found.")

        # Parse JSON data
        data = resp["content"]

        if not data:
            raise UIDNotFounded(f"UID {uid} not found.")

        self.LOGGER.debug("Got data from EnkaNetwork.")
        self.LOGGER.debug(f"Raw data: {data}")

        if self._enable_cache:
            self.LOGGER.debug("Caching data...")
            await self.cache.set(uid, data)

        # Return data
        self.LOGGER.debug("Parsing data...")
        return EnkaNetworkResponse.parse_obj(data)

    async def update_assets(self) -> None:
        self.LOGGER.debug("Downloading new content...")
        _PATH = Assets._get_path_assets()
        for folder in _PATH:
            for filename in os.listdir(_PATH[folder]):
                self.LOGGER.debug(f"Downloading {folder} file {filename}...")
                _json = await request(
                    url=self.RAWDATA.format(PATH=f"master/exports/{folder}/{filename}")  # noqa: E501
                )

                self.LOGGER.debug(f"Writing {folder} file {filename}...")
                with open(os.path.join(_PATH[folder], filename), "w", encoding="utf-8") as f:  # noqa: E501
                    json.dump(_json["content"], f, ensure_ascii=False, indent=4)  # noqa: E501

        # Reload config
        self.assets.reload_assets()
