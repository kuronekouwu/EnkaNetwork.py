import json
import os

from typing import Dict, List
from io import TextIOWrapper

PATH = os.path.dirname(os.path.abspath(__file__))
def _load(path: str) -> TextIOWrapper:
    return open(path, "r", encoding="utf-8")

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

        cls.LANGS = lang.upper()

    @classmethod
    def load_json_lang(cls) -> None:
        _PATH = os.path.join(PATH, "json", "lang")
        FILE_LANG = os.listdir(_PATH)
        for FILENAME in FILE_LANG:
            cls.HASH_MAP[FILENAME.split(".")[0]] = json.load(_load(os.path.join(_PATH, FILENAME)))

    @classmethod
    def load_json_data(cls) -> None:
        _PATH = os.path.join(PATH, "json", "data")
        FILE_DATA = os.listdir(_PATH)
        for FILENAME in FILE_DATA:
            cls.DATA[FILENAME.split(".")[0]] = json.load(_load(os.path.join(_PATH, FILENAME)))
