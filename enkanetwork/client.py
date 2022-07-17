import logging
import os
import json

from typing import Union

from .model import EnkaNetworkResponse
from .exception import VaildateUIDError, UIDNotFounded
from .assets import Assets
from .utils import create_path, validate_uid, request

class EnkaNetworkAPI:
    LOGGER = logging.getLogger(__name__)

    # JSON Data & Language
    RAWDATA = "https://raw.githubusercontent.com/mrwan200/enkanetwork.py-data/{PATH}"

    def __init__(self, lang: str = "en", debug: bool = False, key: str = "") -> None:
        # Logging
        logging.basicConfig()
        logging.getLogger("enkanetwork").setLevel(logging.DEBUG if debug else logging.ERROR)

        # Set language and load config
        self.assets = Assets(lang)

        # Key
        self.__key = key

    async def fetch_user(self, uid: Union[str, int]) -> EnkaNetworkResponse:
        self.LOGGER.debug(f"Validating with UID {uid}...")
        if not validate_uid(str(uid)):
            raise VaildateUIDError("Validate UID failed. Please check your UID.")
        
        self.LOGGER.debug(f"Fetching user with UID {uid}...")

        resp = await request(url=create_path(f"u/{uid}/__data.json" + ("?key={key}" if self.__key else "")))

        # Check if status code is not 200 (Ex. 500)
        if resp["status"] != 200:
            raise UIDNotFounded(f"UID {uid} not found.")

        # Parse JSON data
        data = resp["content"]
                        
        if not data:
            raise UIDNotFounded(f"UID {uid} not found.")

        self.LOGGER.debug("Got data from EnkaNetwork.")
        self.LOGGER.debug(f"Raw data: {data}")

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
                    url=self.RAWDATA.format(PATH=f"master/exports/{folder}/{filename}")
                )

                self.LOGGER.debug(f"Writing {folder} file {filename}...")
                with open(os.path.join(_PATH[folder], filename), "w", encoding="utf-8") as f:
                    json.dump(_json["content"], f, ensure_ascii=False, indent=4)

        # Reload config
        self.assets.reload_assets()