from pydantic import BaseModel, Field
from typing import List, Any

from .equipments import Equipments
from .combats import CharacterCombat
from ..json import Config
from ..utils import create_ui_path

class ChatacterFriendshipLevel(BaseModel):
    level: int = Field(0, alias="expLevel")

class CharacterImages(BaseModel):
    icon: str = ""
    side: str = ""
    gacha: str = ""

class CharacterSkill(BaseModel):
    id: int = 0
    name: str = ""
    icon: str = ""
    level: int = 0

class CharacterConstellations(BaseModel):
    id: int = 0
    name: str  = ""
    icon: str = ""
    unlocked: bool = False # If character has this constellation.

class CharacterInfo(BaseModel):
    """
        API Response data
    """
    id: int = Field(0, alias="avatarId")
    friendship: ChatacterFriendshipLevel = Field({},alias="fetterInfo")
    equipments: List[Equipments] = Field([], alias="equipList")
    combat: CharacterCombat = Field({}, alias="fightPropMap")
    skill_data: List[int] = Field([], alias="inherentProudSkillList")
    skill_id: int = Field(0, alias="skillDepotId")

    """
        Custom data
    """
    name: str = "" # Get from name hash map 
    image: CharacterImages = CharacterImages()
    skills: List[CharacterSkill] = []
    constellations: List[CharacterConstellations] = []

    # Prop Maps
    xp: int = 0 # AKA. propMap 1001
    ascension: int = 0 # AKA. propMap 4001
    level: int = 0 # AKA. propMap 1002

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        # Get character
        character = Config.DATA["characters"].get(str(data["avatarId"]))

        # Check if character is 
        if not character:
            return
        # Get name hash map
        name = Config.HASH_MAP["characters"].get(str(character["NameTextMapHash"]))

        # Get name from hash map and icon
        __pydantic_self__.name = name[Config.LANGS]
        __pydantic_self__.image = CharacterImages(
            icon=create_ui_path(character["SideIconName"].replace("_Side", "")),
            side=create_ui_path(character["SideIconName"]),
            gacha=create_ui_path(character["SideIconName"].replace("AvatarIcon_Side", "Gacha_AvatarImg"))
        )

        # Get prop map
        __pydantic_self__.xp = int(data["propMap"]["1001"]["ival"]) if "1001" in data["propMap"] else 0
        __pydantic_self__.ascension = int(data["propMap"]["1002"]["ival"]) if "1002" in data["propMap"] else 0
        __pydantic_self__.level = int(data["propMap"]["4001"]["ival"]) if "4001" in data["propMap"] else 0

        # Load constellation
        for constellation in character["Consts"]:
            _constellation = Config.DATA["constellations"].get(str(constellation))
            if _constellation:
                __pydantic_self__.constellations.append(CharacterConstellations(
                    id=_constellation["talentId"],
                    name=Config.HASH_MAP["constellations"].get(str(_constellation["nameTextMapHash"]))[Config.LANGS],
                    icon=create_ui_path(constellation),
                    unlocked=_constellation["talentId"] in data["talentIdList"] if "talentIdList" in data else False
                ))
        
        # Load skills 
        for skill in character["SkillOrder"]:
            _skill = Config.DATA["skills"].get(str(skill))
            if _skill:
                __pydantic_self__.skills.append(CharacterSkill(
                    id=skill,
                    name=Config.HASH_MAP["skills"].get(str(_skill["nameTextMapHash"]))[Config.LANGS],
                    icon=create_ui_path(_skill["skillIcon"]),
                    level=data["skillLevelMap"].get(str(skill), 0)
                ))