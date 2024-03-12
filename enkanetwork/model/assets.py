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
    """ Namecards (Assets)

    Attributes
    ------------
    id: :class:`int`
        Namecard ID
    hash_id: :class:`int | str`
        Namecard hash id
    icon: :class:`IconAsset`
        A icon assets. Please refers in `IconAsset` class
    banner: :class:`IconAsset`
        A banner assets. Please refers in `IconAsset` class
    navbar: :class:`IconAsset`
        A navbar assets. Please refers in `IconAsset` class
    """

    id: int = 0
    hash_id: int | str = Field("", alias="nameTextMapHash")
    icon: IconAsset
    banner: IconAsset
    navbar: IconAsset


class CharacterIconAsset(BaseModel):
    """ Character Icon (Assets)

    Attributes
    ------------
    icon: :class:`IconAsset`
        A icon assets. Please refers in `IconAsset` class
    side: :class:`IconAsset`
        A navbar assets. Please refers in `IconAsset` class
    banner: :class:`IconAsset`
        A banner assets. Please refers in `IconAsset` class
    card: :class:`IconAsset`
        A navbar assets. Please refers in `IconAsset` class
    """
    icon: IconAsset
    side: IconAsset
    banner: IconAsset
    card: IconAsset


class CharacterSkillAsset(BaseModel):
    """ Character Skill(s) (Assets)

    Attributes
    ------------
    id: :class:`int`
        Character skill(s) ID
    pround_map: :class:`int`
        pround map for a booest skill by constellation
    hash_id: :class:`int | str`
        Skill(s) hash id
    icon: :class:`IconAsset`
        A icon assets. Please refers in `IconAsset` class
    """
    id: int = 0,
    pround_map: int = 0,
    hash_id: int | str = Field("", alias="nameTextMapHash")
    icon: IconAsset = None


class CharacterConstellationsAsset(BaseModel):
    """ Character Constellations (Assets)

    Attributes
    ------------
    id: :class:`int`
        Character constellations ID
    hash_id: :class:`int | str`
        Constellations hash id
    icon: :class:`IconAsset`
        A icon assets. Please refers in `IconAsset` class
    """
    id: int = 0
    hash_id: int | str = Field("", alias="nameTextMapHash")
    icon: IconAsset = None


class CharacterCostume(BaseModel):
    """ Character Costume (Assets)

    Attributes
    ------------
    id: :class:`int`
        Costume ID
    hash_id: :class:`int`
        Costume hash id
    icon: :class:`IconAsset`
        A icon assets. Please refers in `IconAsset` class
    """
    id: int = 0
    images: CharacterIconAsset = None

class AritfactProps(BaseModel):
    id: int = 0
    type: str = Field('', alias='propType')
    digit: str = Field('DIGIT', alias='propDigit')
    value: int | float = Field(0, alias='propValue')


class CharacterAsset(BaseModel):
    """ Character (Assets)

    Attributes
    ------------
    id: :class:`int`
        Avatar ID
    rarity: :class:`int`
        Character rarity (5 stars or 4stars)
    hash_id: :class:`int`
        Character hash id
    element: :class:`ElementType`
        Character element type
    images: :class:`CharacterIconAsset`
        Character image data. Please refers in `CharacterIconAsset`
    skill_id: :class:`int`
        Character skill ID
    skills: List[:class:`int`]
        Character skill data list
    constellations:  List[:class:`int`]
        Character constellations data list
    """
    id: int = 0
    rarity: int = 0
    hash_id: int | str = Field("", alias="nameTextMapHash")
    element: ElementType = ElementType.Unknown
    images: CharacterIconAsset = None
    skill_id: int = 0
    skills: List[int] = []
    constellations: List[int] = Field([], alias="talents")

    class Config:
        use_enum_values = True

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.element = ElementType(
            data["costElemType"]) if data["costElemType"] != "" else ElementType.Unknown
        self.rarity = 5 if data["qualityType"].endswith("_ORANGE") else 4
