from pydantic import BaseModel, Field
from typing import List

from .players import PlayerInfo
from .character import CharacterInfo


class EnkaNetworkResponse(BaseModel):
    player: PlayerInfo = Field(None, alias="playerInfo")
    characters: List[CharacterInfo] = Field(None, alias="avatarInfoList")
    ttl: int = 0
