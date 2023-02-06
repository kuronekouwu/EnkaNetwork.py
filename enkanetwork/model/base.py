from pydantic import BaseModel, Field
from typing import List

from .players import PlayerInfo
from .character import CharacterInfo
from .profile import ProfilePatreon, ProfileOwner
from .hoyos import PlayerHoyos

from ..utils import BASE_URL
from typing import Any

__all__ = ("EnkaNetworkResponse",)

class EnkaNetworkInfo(BaseModel):
    uid: str = ""
    url: str = ""
    path: str = ""

class EnkaNetworkResponse(BaseModel):
    player: PlayerInfo = Field(None, alias="playerInfo")
    characters: List[CharacterInfo] = Field(None, alias="avatarInfoList")
    profile: EnkaNetworkInfo = EnkaNetworkInfo()
    owner: ProfileOwner = None
    ttl: int = 0

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.profile.path = f"/u/{data.get('uid')}"
        self.profile.url = BASE_URL.format(PATH=self.profile.path[1:])
        self.profile.uid = data.get("uid") or ""

class EnkaNetworkProfileResponse(BaseModel):
    username: str
    profile: ProfilePatreon
    hoyos: List[PlayerHoyos] = []