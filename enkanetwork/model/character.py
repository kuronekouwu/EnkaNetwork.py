import logging

from pydantic import BaseModel, Field
from typing import List, Any

from .equipments import Equipments
from .combats import CharacterCombat
from ..json import Config
from ..utils import create_ui_path
from ..enum import ElementType

LOGGER = logging.getLogger(__name__)

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
    element: ElementType = ElementType.Unknown
    image: CharacterImages = CharacterImages()
    skills: List[CharacterSkill] = []
    constellations: List[CharacterConstellations] = []

    # Prop Maps
    xp: int = 0 # AKA. propMap 1001
    ascension: int = 0 # AKA. propMap 4001
    level: int = 0 # AKA. propMap 1002

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        # Get prop map
        __pydantic_self__.xp = int(data["propMap"]["1001"]["ival"]) if "1001" in data["propMap"] else 0
        __pydantic_self__.ascension = int(data["propMap"]["1002"]["ival"]) if "1002" in data["propMap"] else 0
        __pydantic_self__.level = int(data["propMap"]["4001"]["ival"]) if "4001" in data["propMap"] else 0

        # Get character
        LOGGER.debug(f"=== Character Data ===")
        LOGGER.debug(f"Getting character wtih id: {__pydantic_self__.id}")
        character = Config.DATA["characters"].get(str(data["avatarId"]))

        # Check if character is founded
        if not character:
            LOGGER.debug(f"Character not found with id: {__pydantic_self__.id}")
            return

        # Load icon
        __pydantic_self__.image = CharacterImages(
            icon=create_ui_path(character["sideIconName"].replace("_Side", "")),
            side=create_ui_path(character["sideIconName"]),
            gacha=create_ui_path(character["sideIconName"].replace("AvatarIcon_Side", "Gacha_AvatarImg"))
        )

        # Get element
        __pydantic_self__.element = ElementType[character["costElemType"]]

        # Load constellation
        LOGGER.debug(f"=== Constellation ===")
        for constellation in character["talents"]:
            LOGGER.debug(f"Getting constellation icon ID: {constellation}")
            _constellation = Config.DATA["constellations"].get(str(constellation))

            if not _constellation:
                LOGGER.debug(f"Constellation icon ID: {__pydantic_self__.id} not found.")
                continue

            # Get name hash map
            LOGGER.debug(f"Getting name hash map ID: {_constellation['nameTextMapHash']}")
            _name = Config.HASH_MAP["constellations"].get(str(_constellation["nameTextMapHash"]))

            if _name is None:
                LOGGER.error(f"Name hash map not found.")
                continue

            __pydantic_self__.constellations.append(CharacterConstellations(
                id=int(constellation),
                name=_name[Config.LANGS],
                icon=create_ui_path(_constellation["icon"]),
                unlocked=int(constellation) in data["talentIdList"] if "talentIdList" in data else False
            ))
        
        # Load skills 
        LOGGER.debug(f"=== Skills ===")
        for skill in character["skills"]:
            LOGGER.debug(f"Getting skill ID: {skill}")
            _skill = Config.DATA["skills"].get(str(skill))

            if not _skill:
                LOGGER.error(f"Skill ID: {__pydantic_self__.id} not found")
                continue

            # Get name hash map
            LOGGER.debug(f"Getting name hash map ID: {_skill['nameTextMapHash']}")
            _name = Config.HASH_MAP["skills"].get(str(_skill["nameTextMapHash"]))

            if _name is None:
                LOGGER.error(f"Name hash map not found.")
                continue

            __pydantic_self__.skills.append(CharacterSkill(
                id=skill,
                name=_name[Config.LANGS],
                icon=create_ui_path(_skill["skillIcon"]),
                level=data["skillLevelMap"].get(str(skill), 0)
            ))

        LOGGER.debug(f"=== Character Name ===")
        LOGGER.debug(f"Getting name hash map ID: {character['nameTextMapHash']}")
        _name = Config.HASH_MAP["characters"].get(str(character["nameTextMapHash"]))

        if _name is None:
            LOGGER.error(f"Name hash map not found.")
            return

        # Get name from hash map
        __pydantic_self__.name = _name[Config.LANGS]
    
    class Config:
        use_enum_values = True