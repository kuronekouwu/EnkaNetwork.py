from pydantic import BaseModel, Field
from typing import List, Any

from ..enum import ElementType


class NamecardAsset(BaseModel):
    id: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    icon: str = Field("", alias="icon")
    banner: str = ""
    navbar: str = ""


class CharacterIconAsset(BaseModel):
    icon: str = ""
    side: str = ""
    banner: str = ""


class CharacterSkillAsset(BaseModel):
    id: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    icon: str = Field(None, alias="skillIcon")


class CharacterConstellationsAsset(BaseModel):
    id: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    icon: str = Field(None, alias="icon")


class CharacterAsset(BaseModel):
    id: int = 0
    hash_id: str = Field("", alias="nameTextMapHash")
    element: ElementType = ElementType.Unknown
    images: CharacterIconAsset = None
    skills: List[int] = []
    constellations: List[int] = Field([], alias="talents")

    class Config:
        use_enum_values = True

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        __pydantic_self__.element = ElementType(data["costElemType"]) if data["costElemType"] != "" else ElementType.Unknown.name  # noqa: E501
