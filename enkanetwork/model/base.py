from pydantic import BaseModel, Field
from typing import List

from .players import PlayerInfo
from .character import CharacterInfo
from .profile import EnkaProfile, ProfileOwner
from .hoyos import PlayerHoyos

from ..utils import BASE_URL
from typing import Any

__all__ = ("EnkaNetworkResponse",)

class EnkaNetworkInfo(BaseModel):
    """ Enka.Network response data

    Attributes
    ------------
    uid: :class:`str`
        UID Player
    url: :class:`str`
        URL to Enka.Network profile
    path: :class:`str`
        Path to enter Enka.network profile
    """
    uid: str = ""
    url: str = ""
    path: str = ""

class EnkaNetworkResponse(BaseModel):
    """ Enka.Network response data

    Attributes
    ------------
    player: :class:`PlayerInfo`
        Player info data. Please refers in `PlayerInfo` class (key: "playerInfo")
    characters: List[:class:`CharacterInfo`]
        List character. Please refers in `CharacterInfo` class (key: "avatarInfoList")
    profile: :class:`EnkaNetworkInfo`
        profile enka.network. Please refers in `EnkaNetworkInfo` class
    owner: :class:`ProfileOwner`
        Owner UID data. **subscriptions in Enka.Network**. Please refers in `ProfileOwner` class 
    ttl: :class:`int`
        Cache timeout
    uid: :class:`int`
        UID Player
    """
    player: PlayerInfo = Field(None, alias="playerInfo")
    characters: List[CharacterInfo] = Field(None, alias="avatarInfoList")
    profile: EnkaNetworkInfo = EnkaNetworkInfo()
    owner: ProfileOwner = None
    ttl: int = 0
    uid: int = 0

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.profile.path = f"/u/{data.get('uid')}"
        self.profile.url = BASE_URL.format(PATH=self.profile.path[1:])
        self.profile.uid = data.get("uid") or ""

class EnkaNetworkProfileResponse(BaseModel):
    username: str
    profile: EnkaProfile
    hoyos: List[PlayerHoyos] = []