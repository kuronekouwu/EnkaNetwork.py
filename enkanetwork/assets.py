import json
import os
import logging

from typing import Dict, Union
from io import TextIOWrapper

from .enum import Language
from .model import assets
from .utils import create_ui_path

PATH = os.path.dirname(os.path.abspath(__file__))

LOGGER = logging.getLogger(__name__)


class Assets:
    DATA: Dict[str, dict] = {}
    HASH_MAP: Dict[str, dict] = {}
    LANGS: Language = Language.EN

    def __init__(self, lang: Language = Language.EN) -> None:
        # Set language
        self._set_language(lang)
        self.reload_assets()

    @classmethod
    def reload_assets(cls) -> None:
        # Load assets
        cls.__load_assets_lang()
        cls.__load_assets_data()

    @classmethod
    def character(cls, id: int) -> Union[assets.CharacterAsset, None]:
        LOGGER.debug(f"Getting character assets with id: {id}")
        data = cls.DATA["characters"].get(str(id))
        if not data:
            LOGGER.error(f"Character not found with id: {id}")
            return

        return assets.CharacterAsset.parse_obj({
            "id": id,
            "images": cls.create_character_icon(data["sideIconName"]),
            **data
        })

    @classmethod
    def constellations(cls, id: int) -> Union[assets.CharacterConstellationsAsset, None]:  # noqa: E501
        LOGGER.debug(f"Getting character constellations assets with id: {id}")
        data = cls.DATA["constellations"].get(str(id))
        if not data:
            LOGGER.error(f"Character constellations not found with id: {id}")
            return

        return assets.CharacterConstellationsAsset.parse_obj({
            "id": id,
            **data,
            "icon": cls.create_icon_path(data["icon"])
        })

    @classmethod
    def skills(cls, id: int) -> Union[assets.CharacterSkillAsset, None]:
        LOGGER.debug(f"Getting character skills assets with id: {id}")
        data = cls.DATA["skills"].get(str(id))
        if not data:
            LOGGER.error(f"Character skills not found with id: {id}")
            return

        return assets.CharacterSkillAsset.parse_obj({
            "id": id,
            **data,
            "skillIcon": cls.create_icon_path(data["skillIcon"])
        })

    @classmethod
    def namecards(cls, id: int) -> Union[assets.NamecardAsset, None]:
        LOGGER.debug(f"Getting namecards assets with id: {id}")
        data = cls.DATA["namecards"].get(str(id))
        if not data:
            LOGGER.error(f"Namecards not found with id: {id}")
            return

        return assets.NamecardAsset.parse_obj({
            "id": id,
            **data,
            "icon": cls.create_icon_path(data["icon"]),
            "banner": cls.create_icon_path(data["picPath"][1]),
            "navbar": cls.create_icon_path(data["picPath"][0])
        })

    @classmethod
    def get_hash_map(cls, hash_id: str) -> Union[str, None]:
        LOGGER.debug(f"Getting nameTextMapHash {hash_id} with language: {cls.LANGS}")  # noqa: E501
        for key in cls.HASH_MAP:
            if str(hash_id) in cls.HASH_MAP[key]:
                val = cls.HASH_MAP[key][str(hash_id)][cls.LANGS]
                LOGGER.debug(f"Got nameTextMapHash {hash_id} with language: {key} (Value '{val}')")  # noqa: E501
                return val

        LOGGER.error(f"nameTextMapHash {hash_id} not found with language: {cls.LANGS}")  # noqa: E501
        return

    @classmethod
    def character_icon(cls, id: int) -> Union[assets.CharacterIconAsset, None]:
        data = cls.character(id)
        if not data:
            return

        return data.images

    @staticmethod
    def create_character_icon(path: str) -> assets.CharacterIconAsset:
        return assets.CharacterIconAsset(
            icon=create_ui_path(path.replace("_Side", "")),
            side=create_ui_path(path),
            banner=create_ui_path(path.replace("AvatarIcon_Side", "Gacha_AvatarImg"))  # noqa: E501
        )

    @staticmethod
    def create_icon_path(path: str) -> str:
        return create_ui_path(path)

    @classmethod
    def _set_language(cls, lang: Language) -> None:
        # Check language
        if not lang.split("-")[0].lower() in list(Language):
            raise ValueError("Language not supported. Please check your language.")  # noqa: E501

        LOGGER.debug(f"Set language to {lang}.")
        cls.LANGS = lang.upper()

    @classmethod
    def _get_path_assets(cls) -> Dict[str, str]:
        return {
            "data": os.path.join(PATH, "assets", "data"),
            "langs": os.path.join(PATH, "assets", "langs")
        }

    @classmethod
    def __load_assets_lang(cls) -> None:
        _PATH = cls._get_path_assets()["langs"]
        FILE_LANG = os.listdir(_PATH)
        for FILENAME in FILE_LANG:
            LOGGER.debug(f"Loading language file {FILENAME}...")
            cls.HASH_MAP[FILENAME.split(".")[0]] = json.load(cls.__load(os.path.join(_PATH, FILENAME)))  # noqa: E501

    @classmethod
    def __load_assets_data(cls) -> None:
        _PATH = cls._get_path_assets()["data"]
        FILE_DATA = os.listdir(_PATH)
        for FILENAME in FILE_DATA:
            LOGGER.debug(f"Loading data file {FILENAME}...")
            cls.DATA[FILENAME.split(".")[0]] = json.load(cls.__load(os.path.join(_PATH, FILENAME)))  # noqa: E501

    def __load(path: str) -> TextIOWrapper:
        return open(path, "r", encoding="utf-8")
