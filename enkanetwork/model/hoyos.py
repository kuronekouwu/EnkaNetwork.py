from pydantic import BaseModel

from .players import PlayerInfo
from .build import Builds

class PlayerHoyos(BaseModel):
    uid_public: bool = False
    public: bool = False
    verified: bool = False
    player_info: PlayerInfo
    hash: str
    region: str
    order: str

    builds: Builds = None

    