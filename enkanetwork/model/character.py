import logging

from pydantic import BaseModel, Field
from typing import List, Any

from .equipments import Equipments
from .combats import CharacterCombat
from .assets import (
    CharacterIconAsset
)
from ..assets import Assets
from ..utils import create_ui_path
from ..enum import ElementType

LOGGER = logging.getLogger(__name__)

class ChatacterFriendshipLevel(BaseModel):
    level: int = Field(0, alias="expLevel")

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
    image: CharacterIconAsset = CharacterIconAsset()
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
        character = Assets.character(str(data["avatarId"]))

        # Check if character is founded
        if not character:
            return

        # Load icon
        __pydantic_self__.image = character.images

        # Get element
        __pydantic_self__.element = character.element

        # Load constellation
        LOGGER.debug(f"=== Constellation ===")
        for constellation in character.constellations:
            _constellation = Assets.constellations(constellation)
            if not _constellation:
                continue

            # Get name hash map
            _name = Assets.get_hash_map(str(_constellation.hash_id))

            if _name is None:
                continue

            __pydantic_self__.constellations.append(CharacterConstellations(
                id=int(constellation),
                name=_name,
                icon=_constellation.icon,
                unlocked=int(constellation) in data["talentIdList"] if "talentIdList" in data else False
            ))
        
        # Load skills 
        LOGGER.debug(f"=== Skills ===")
        for skill in character.skills:
            _skill = Assets.skills(skill)

            if not _skill:
                continue

            # Get name hash map
            _name = Assets.get_hash_map(_skill.hash_id)

            if _name is None:
                LOGGER.error(f"Name hash map not found.")
                continue

            __pydantic_self__.skills.append(CharacterSkill(
                id=skill,
                name=_name,
                icon=_skill.icon,
                level=data["skillLevelMap"].get(str(skill), 0)
            ))

        LOGGER.debug(f"=== Character Name ===")
        _name = Assets.get_hash_map(str(character.hash_id))

        if _name is None:
            return

        # Get name from hash map
        __pydantic_self__.name = _name
    
    class Config:
        use_enum_values = True