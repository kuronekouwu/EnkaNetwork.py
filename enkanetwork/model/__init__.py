from pydantic import BaseModel, Field
from typing import List

from .players import *
from .character import *
from .equipments import *
from .players import *
from .stats import *
# from .base import *

class EnkaNetworkResponse(BaseModel):
    player: PlayerInfo = Field(None, alias="playerInfo")
    characters: List[CharacterInfo] = Field(None, alias="avatarInfoList")
    ttl: int = 0