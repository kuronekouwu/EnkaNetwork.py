import logging

from pydantic import BaseModel, Field
from typing import List, Any, Dict

from .equipments import Equipments
from .stats import CharacterStats
from .assets import (
    CharacterIconAsset,
)
from .utils import IconAsset

from ..assets import Assets
from ..enum import ElementType

LOGGER = logging.getLogger(__name__)

__all__ = (
    'CharacterSkill',
    'CharacterConstellations',
    'CharacterInfo'
)

class CharacterSkill(BaseModel):
    id: int = 0
    name: str = ""
    icon: IconAsset = None
    is_boosted: bool = False
    level: int = 0


class CharacterConstellations(BaseModel):
    id: int = 0
    name: str = ""
    icon: IconAsset = None
    unlocked: bool = False  # If character has this constellation.


class CharacterInfo(BaseModel):
    """
        API Response data
    """
    id: int = Field(0, alias="avatarId")
    equipments: List[Equipments] = Field([], alias="equipList")
    stats: CharacterStats = Field({}, alias="fightPropMap")
    skill_data: List[int] = Field([], alias="inherentProudSkillList")
    skill_id: int = Field(0, alias="skillDepotId")

    """
        Custom data
    """
    name: str = ""  # Get from name hash map
    friendship_level: int = 1
    element: ElementType = ElementType.Unknown
    rarity: int = 0
    image: CharacterIconAsset = None
    skills: List[CharacterSkill] = []
    constellations: List[CharacterConstellations] = []

    # Prop Maps
    xp: int = 0  # AKA. propMap 1001
    ascension: int = 0  # AKA. propMap 4001
    level: int = 0  # AKA. propMap 1002

    # Other
    max_level: int = 20
    constellations_unlocked: int = 0  # Constellation is unlocked count

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        # Friendship level
        self.friendship_level = data["fetterInfo"]["expLevel"]

        # Get prop map
        self.xp = int(data["propMap"]["1001"]["ival"]) if "1001" in data["propMap"] else 0
        self.ascension = int(data["propMap"]["1002"]["ival"]) if "1002" in data["propMap"] else 0
        self.level = int(data["propMap"]["4001"]["ival"]) if "4001" in data["propMap"] else 0

        # Constellation unlocked count
        self.constellations_unlocked = len(data["talentIdList"]) if "talentIdList" in data else 0

        # Get max character level
        self.max_level = (self.ascension * 10) + (10 if self.ascension > 0 else 0) + 20

        # Get character
        LOGGER.debug("=== Character Data ===")
        avatarId = str(data["avatarId"])
        avatarId += f"-{data['skillDepotId']}" if data["avatarId"] in [10000005, 10000007] else ""
        character = Assets.character(avatarId)

        # Check if character is founded
        if not character:
            return

        # Load icon
        if "costumeId" in data:
            _data = Assets.character_costume(str(data["costumeId"]))
            if _data:
                self.image = _data.images
            else:
                self.image = character.images
        else:
            self.image = character.images

        # Get element
        self.element = ElementType(character.element)

        # Check calculate rarity
        self.rarity = character.rarity

        # Load constellation
        LOGGER.debug("=== Constellation ===")
        for constellation in character.constellations:
            _constellation = Assets.constellations(constellation)
            if not _constellation:
                continue

            # Get name hash map
            _name = Assets.get_hash_map(str(_constellation.hash_id))

            if _name is None:
                continue

            self.constellations.append(CharacterConstellations(
                id=int(constellation),
                name=_name,
                icon=_constellation.icon,
                unlocked=int(
                    constellation) in data["talentIdList"] if "talentIdList" in data else False
            ))

        # Load skills
        LOGGER.debug("=== Skills ===")
        for skill in character.skills:
            _lvl = data["skillLevelMap"].get(str(skill), 0)
            _is_boosted = False
            _skill = Assets.skills(skill)

            if not _skill:
                continue

            # Get name hash map
            _name = Assets.get_hash_map(_skill.hash_id)

            if _name is None:
                continue

            if "proudSkillExtraLevelMap" in data:
                boost_level = data["proudSkillExtraLevelMap"].get(str(_skill.pround_map), None)
                if not boost_level is None:
                    _is_boosted = True 
                    _lvl += boost_level

            self.skills.append(CharacterSkill(
                id=skill,
                name=_name,
                icon=_skill.icon,
                is_boosted=_is_boosted,
                level=_lvl
            ))

        LOGGER.debug("=== Character Name ===")
        _name = Assets.get_hash_map(str(character.hash_id))

        if _name is None:
            return

        # Get name from hash map
        self.name = _name

    class Config:
        use_enum_values = True
