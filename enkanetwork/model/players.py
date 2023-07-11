import logging

from pydantic import BaseModel, Field
from typing import List, Any, Union

from .utils import IconAsset

from ..assets import Assets
from ..enum import ElementType

LOGGER = logging.getLogger(__name__)

__all__ = (
    'ProfilePicture',
    'showAvatar',
    'Namecard',
    'PlayerInfo'
)

class ProfilePicture(BaseModel):
    """
        API Response data
    """
    id: int = Field(0, alias="avatarId")

    """
        Custom add data
    """
    icon: IconAsset = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        # Get character
        LOGGER.debug("=== Avatar ===")
        if "avatarId" in data:
            if "costumeId" in data:
                _data = Assets.character_costume(str(data["costumeId"]))
                icon = _data.images if _data is not None else _data
            else:
                icon = Assets.character_icon(str(data["avatarId"]))

            if not icon:
                return

            self.icon = icon.icon


class showAvatar(BaseModel):
    """
        API Response data
    """
    id: str = Field(0, alias="avatarId")
    level: int = 1

    """
        Custom data
    """
    name: str = ""
    icon: IconAsset = None
    element: ElementType = ElementType.Unknown

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        # Get character
        LOGGER.debug("=== Character preview ===")

        # Find traveler
        character_preview = Assets.character(str(data["avatarId"]))

        if not character_preview:
            return

        self.element = character_preview.element

        if "costumeId" in data:
            _data = Assets.character_costume(str(data["costumeId"]))
            if _data:
                self.icon = _data.images.icon
        else:
            self.icon = character_preview.images.icon

        # Get name hash map
        _name = Assets.get_hash_map(str(character_preview.hash_id))

        if _name is None:
            return

        self.name = _name


class Namecard(BaseModel):
    id: int = 0
    name: str = ""
    icon: IconAsset = None
    banner: IconAsset = None
    navbar: IconAsset = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        if self.id > 0:
            LOGGER.debug("=== Namecard ===")
            # Get name card
            namecard = Assets.namecards(str(self.id))

            if not namecard:
                return

            self.icon = namecard.icon
            self.banner = namecard.banner
            self.navbar = namecard.navbar

            _name = Assets.get_hash_map(str(namecard.hash_id))
            if _name is None:
                return

            self.name = _name


class PlayerInfo(BaseModel):
    """
        API Response data
    """
    # Profile info
    achievement: int = Field(0, alias="finishAchievementNum")
    level: int = 0
    nickname: str = ""
    signature: str = ""
    world_level: int = Field(1, alias="worldLevel")
    avatar: ProfilePicture = Field(None, alias="profilePicture")
    # Avatars
    characters_preview: List[showAvatar] = Field([], alias="showAvatarInfoList")
    # Abyss floor
    abyss_floor: int = Field(0, alias="towerFloorIndex")
    abyss_room: int = Field(0, alias="towerLevelIndex")

    """
        Custom data
    """
    namecard: Namecard = Namecard()  # Profile name-card
    namecards: List[Namecard] = []  # List name-card preview in profile

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.namecard = Namecard(id=data["nameCardId"])
        self.namecards = [Namecard(id=namecard) for namecard in (data["showNameCardIdList"])] if "showNameCardIdList" in data else []  # noqa: E501
