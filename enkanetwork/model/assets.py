from pydantic import BaseModel, Field
from typing import List, Any

from ..enum import ElementType
from .utils import IconAsset

__all__ = (
    'NamecardAsset',
    'CharacterIconAsset',
    'CharacterSkillAsset',
    'CharacterConstellationsAsset',
    'CharacterCostume',
    'CharacterAsset'
)

class NamecardAsset(BaseModel):
    id: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    icon: IconAsset
    banner: IconAsset
    navbar: IconAsset


class CharacterIconAsset(BaseModel):
    icon: IconAsset
    side: IconAsset 
    banner: IconAsset
    card: IconAsset


class CharacterSkillAsset(BaseModel):
    id: int = 0,
    pround_map: int = 0,
    hash_id: str = Field("", alias="nameTextMapHash")
    icon: IconAsset = None


class CharacterConstellationsAsset(BaseModel):
    id: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    icon: IconAsset = None

class CharacterCostume(BaseModel):
    id: int = 0
    images: CharacterIconAsset = None


class CharacterAsset(BaseModel):
    id: int = 0
    rarity: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    element: ElementType = ElementType.Unknown
    images: CharacterIconAsset = None
    skill_id: int = 0
    skills: List[int] = []
    constellations: List[int] = Field([], alias="talents")

    class Config:
        use_enum_values = True

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.element = ElementType(data["costElemType"]) if data["costElemType"] != "" else ElementType.Unknown
        self.rarity = 5 if data["qualityType"].endswith("_ORANGE") else 4
