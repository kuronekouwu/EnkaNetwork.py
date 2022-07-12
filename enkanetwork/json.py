import json
import os
import logging

from typing import Dict, List
from io import TextIOWrapper

from .utils import request, get_default_header

PATH = os.path.dirname(os.path.abspath(__file__))

LOGGER = logging.getLogger(__name__)

class Config:
    # Characters & Skills
    DATA: Dict[str, dict] = {}

    # Hash Map
    HASH_MAP: Dict[str, dict] = {}

    # Language
    LANGS: str = "EN"
    LANGS_SUPPORTS: List[str] = ["en", "ru", "vi", "th", "pt", "kr", "jp", "id", "fr", "es", "de", "cht", "chs"]

    @classmethod
    def set_languege(cls, lang: str) -> None:
        # Check language
        if not lang.split("-")[0].lower() in cls.LANGS_SUPPORTS:
            raise ValueError("Language not supported. Please check your language.")

        LOGGER.debug(f"Set language to {lang}.")
        cls.LANGS = lang.upper()

    @classmethod
    def get_path_json(cls) -> Dict[str, str]:
        return {
            "data": os.path.join(PATH, "json", "data"),
            "langs": os.path.join(PATH, "json", "langs")
        }

    @classmethod
    def load_json_lang(cls) -> None:
        _PATH = cls.get_path_json()["langs"]
        FILE_LANG = os.listdir(_PATH)
        for FILENAME in FILE_LANG:
            LOGGER.debug(f"Loading language file {FILENAME}...")
            cls.HASH_MAP[FILENAME.split(".")[0]] = json.load(cls._load(os.path.join(_PATH, FILENAME)))

    @classmethod
    def load_json_data(cls) -> None:
        _PATH = cls.get_path_json()["data"]
        FILE_DATA = os.listdir(_PATH)
        for FILENAME in FILE_DATA:
            LOGGER.debug(f"Loading data file {FILENAME}...")
            cls.DATA[FILENAME.split(".")[0]] = json.load(cls._load(os.path.join(_PATH, FILENAME)))
    
    def _load(path: str) -> TextIOWrapper:
        return open(path, "r", encoding="utf-8")
