from pydantic import BaseModel, Field
from typing import List

from .players import PlayerInfo
from .character import CharacterInfo

class EnkaNetworkResponse(BaseModel):
    player: PlayerInfo = Field({}, alias="playerInfo")
    characters: List[CharacterInfo] = Field([], alias="avatarInfoList")
    ttl: int = 0