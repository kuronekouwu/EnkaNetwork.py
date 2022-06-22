from pydantic import BaseModel, Field, validator
from typing import List, Dict
from enum import Enum

from .artifact import Artifacts
from .combats import CharacterCombat

class CharacterPropertieType(int, Enum):
    UNKNOW = -1
    XP = 1001
    ASENCSION = 1002
    LEVEL = 4001

class ChatacterFriendshipLevel(BaseModel):
    level: int = Field(0, alias="expLevel")

class CharacterPropertie(BaseModel):
    type: CharacterPropertieType
    ival: str = Field("", alias="ival")
    value: str = Field("", alias="val")

    @validator('type', pre=True)
    def check_type(cls, val: int):
        if val not in [1001,1002,4001]:
            val = -1

        return val

    class Config:
        use_enum_values = True

class CharacterInfo(BaseModel):
    id: int = Field(0, alias="avatarId")
    friendship: ChatacterFriendshipLevel = Field({},alias="fetterInfo")
    propertie: Dict[str, CharacterPropertie] = Field({}, alias="propMap")
    # Artifacts
    artifacts: List[Artifacts] = Field([], alias="equipList")
    combat: CharacterCombat = Field({}, alias="fightPropMap")
    skill_data: List[int] = Field([], alias="inherentProudSkillList")
    skill_id: int = Field(0, alias="skillDepotId")

    skill_level: Dict[str, int] = Field({}, alias="skillLevelMap")