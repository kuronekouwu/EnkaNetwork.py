from pydantic import BaseModel, Field
from typing import List, Any

from ..enum import ElementType
from .utils import IconAsset

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
    id: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    icon: IconAsset = Field(None, alias="skillIcon")


class CharacterConstellationsAsset(BaseModel):
    id: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    icon: IconAsset = Field(None, alias="icon")


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

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        __pydantic_self__.element = ElementType(data["costElemType"]) if data["costElemType"] != "" else ElementType.Unknown  # noqa: E501
        __pydantic_self__.rarity = 5 if data["qualityType"].endswith("_ORANGE") else 4  # noqa: E501
