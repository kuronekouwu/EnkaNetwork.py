from pydantic import BaseModel, Field
from typing import List, Optional

from .players import PlayerInfo
from .character import CharacterInfo

__all__ = ("EnkaNetworkResponse",)

class EnkaNetworkResponse(BaseModel):
    player: Optional[PlayerInfo] = Field(None, alias="playerInfo")
    characters: Optional[List[CharacterInfo]] = Field(None, alias="avatarInfoList")
    ttl: int = 0