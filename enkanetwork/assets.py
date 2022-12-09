import json
import os
import logging

from .enum import Language
from .model import assets, utils
from .utils import create_ui_path

from typing import Dict, List, TextIO, Optional, Union, Callable

PATH = os.path.dirname(os.path.abspath(__file__))

LOGGER = logging.getLogger(__name__)

__all__ = ('Assets',)


def check_assets(f: Callable):
    def decorator(*args):
        if not args[0].DATA or \
           not args[0].HASH_MAP:
           args[0]._set_language("EN")
           args[0].reload_assets()
        
        return f(*args)

    return decorator


class Assets:
    DATA: Dict[str, dict] = {}
    HASH_MAP: Dict[str, dict] = {}
    LANGS: Language = Language.EN

    def __init__(self, lang: Union[str, Language] = Language.EN) -> None:
        # Set language
        self._set_language(lang)
        self.reload_assets()

    @classmethod
    def reload_assets(cls) -> None:
        # Load assets
        cls.__load_assets_lang()
        cls.__load_assets_data()

    @property
    def CHARACTERS_IDS(self) -> List[str]:
        return [x for x in self.DATA["characters"]]

    @property
    def COSTUMES_IDS(self) -> List[str]:
        return [x for x in self.DATA["costumes"]]

    @property
    def NAMECARD_IDS(self) -> List[str]:
        return [x for x in self.DATA["namecards"]]

    @classmethod
    @check_assets
    def character(cls, id: Union[int, str]) -> Optional[assets.CharacterAsset]:
        LOGGER.debug(f"Getting character assets with id: {id}")

        data = cls.DATA["characters"].get(str(id))
        if not data:
            LOGGER.error(f"Character not found with id: {id}")
            return

        return assets.CharacterAsset.parse_obj({
            "id": id if str(id).isdigit() else id.split("-")[0],
            "skill_id": str(id).split("-")[1] if not str(id).isdigit() else 0,
            "images": cls.create_character_icon(data["sideIconName"]),
            **data
        })

    @classmethod
    def character_costume(cls, id: int) -> Optional[assets.CharacterCostume]:
        LOGGER.debug(f"Getting costume assets with id: {id}")
        data = cls.DATA["costumes"].get(str(id))
        if not data:
            LOGGER.error(f"Costume not found with id: {id}")
            return

        return assets.CharacterCostume.parse_obj({
            "id": id,
            "images": cls.create_chractar_costume_icon(data["sideIconName"])
        })

    @classmethod
    def constellations(cls, id: int) -> Optional[assets.CharacterConstellationsAsset]:
        LOGGER.debug(f"Getting character constellations assets with id: {id}")
        data = cls.DATA["constellations"].get(str(id))
        if not data:
            LOGGER.error(f"Character constellations not found with id: {id}")
            return

        return assets.CharacterConstellationsAsset.parse_obj({
            "id": id,
            **data,
            "icon": utils.IconAsset(filename=data["icon"])
        })

    @classmethod
    def skills(cls, id: int) -> Optional[assets.CharacterSkillAsset]:
        LOGGER.debug(f"Getting character skills assets with id: {id}")
        data = cls.DATA["skills"].get(str(id))

        if not data:
            LOGGER.error(f"Character skills not found with id: {id}")
            return


        pround = data.get("proudSkillGroupId", 0)
        return assets.CharacterSkillAsset.parse_obj({
            "id": id,
            **data,
            "pround_map": pround if not pround is None and pround != "" else 0,
            "icon": utils.IconAsset(filename=data["skillIcon"])
        })

    @classmethod
    def namecards(cls, id: int) -> Optional[assets.NamecardAsset]:
        LOGGER.debug(f"Getting namecards assets with id: {id}")
        data = cls.DATA["namecards"].get(str(id))
        if not data:
            LOGGER.error(f"Namecards not found with id: {id}")
            return

        return assets.NamecardAsset.parse_obj({
            "id": id,
            **data,
            "icon": utils.IconAsset(filename=data["icon"]),
            "banner": utils.IconAsset(filename=data["picPath"][1]),
            "navbar": utils.IconAsset(filename=data["picPath"][0]),
        })

    @classmethod
    def get_hash_map(cls, hash_id: str) -> Optional[str]:
        LOGGER.debug(f"Getting nameTextMapHash {hash_id} with language: {cls.LANGS}")  # noqa: E501
        for key in cls.HASH_MAP:
            if str(hash_id) in cls.HASH_MAP[key]:
                val = cls.HASH_MAP[key][str(hash_id)][cls.LANGS]
                LOGGER.debug(f"Got nameTextMapHash {hash_id} with language: {key} (Value '{val}')")  # noqa: E501
                return val

        LOGGER.error(f"nameTextMapHash {hash_id} not found with language: {cls.LANGS}")  # noqa: E501
        return

    @classmethod
    def character_icon(cls, id: int) -> Optional[assets.CharacterIconAsset]:
        data = cls.character(id)
        if not data:
            return

        return data.images

    @staticmethod
    def create_character_icon(path: str) -> assets.CharacterIconAsset:
        return assets.CharacterIconAsset(
            icon=utils.IconAsset(filename=path.replace("_Side", "")),
            side=utils.IconAsset(filename=path),
            banner=utils.IconAsset(filename=path.replace("AvatarIcon_Side", "Gacha_AvatarImg")),  # noqa: E501
            card=utils.IconAsset(filename=path.replace("_Side", "") + "_Card")
        )

    @classmethod
    def create_chractar_costume_icon(cls, path: str) -> assets.CharacterIconAsset:  # noqa: E501
        _data = cls.create_character_icon(path)
        _data.banner = utils.IconAsset(filename=_data.banner.filename.replace("Gacha_AvatarImg", "Costume"))  # noqa: E501
        return _data

    @staticmethod
    def create_icon_path(path: str) -> str:
        return create_ui_path(path)

    @classmethod
    def _set_language(cls, lang: Language) -> None:
        # Check language
        if lang is None or not lang.split("-")[0].lower() in list(Language):
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

    @staticmethod
    def __load(path: str) -> TextIO:
        return open(path, "r", encoding="utf-8")
