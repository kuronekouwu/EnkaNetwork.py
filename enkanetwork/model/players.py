import logging

from pydantic import BaseModel, Field
from typing import List, Any, Union

from ..assets import Assets
from ..enum import ElementType

LOGGER = logging.getLogger(__name__)


class ProfilePicture(BaseModel):
    """
        API Response data
    """
    id: int = Field(0, alias="avatarId")

    """
        Custom add data
    """
    url: Union[str, None] = None

    def __init__(__pydantic_self__, **data: Any) -> None:
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

            __pydantic_self__.url = icon.icon


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
    icon: str = ""
    element: ElementType = ElementType.Unknown

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        # Get character
        LOGGER.debug("=== Character preview ===")

        # Find tarveler
        character_preview = Assets.character(str(data["avatarId"]))

        if not character_preview:
            return

        __pydantic_self__.element = character_preview.element

        if "costumeId" in data:
            _data = Assets.character_costume(str(data["costumeId"]))
            if _data:
                __pydantic_self__.icon = _data.images.icon
        else:
            __pydantic_self__.icon = character_preview.images.icon

        # Get name hash map
        _name = Assets.get_hash_map(str(character_preview.hash_id))

        if _name is None:
            return

        __pydantic_self__.name = _name


class Namecard(BaseModel):
    id: int = 0
    icon: str = ""
    banner: str = ""
    navbar: str = ""
    name: str = ""

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        if __pydantic_self__.id > 0:
            LOGGER.debug("=== Namecard ===")
            # Get name card
            namecard = Assets.namecards(str(__pydantic_self__.id))

            if not namecard:
                return

            __pydantic_self__.icon = namecard.icon
            __pydantic_self__.banner = namecard.banner
            __pydantic_self__.navbar = namecard.navbar

            _name = Assets.get_hash_map(str(namecard.hash_id))
            if _name is None:
                return

            __pydantic_self__.name = _name


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
    icon: ProfilePicture = Field(None, alias="profilePicture")
    # Avatars
    characters_preview: List[showAvatar] = Field(
        [], alias="showAvatarInfoList")
    # Abyss floor
    abyss_floor: int = Field(0, alias="towerFloorIndex")
    abyss_room: int = Field(0, alias="towerLevelIndex")

    """
        Custom data
    """
    namecard: Namecard = Namecard()  # Profile namecard
    namecards: List[Namecard] = []  # List namecard preview in profile

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        __pydantic_self__.namecard = Namecard(id=data["nameCardId"])
        __pydantic_self__.namecards = [Namecard(id=namecard) for namecard in (
            data["showNameCardIdList"])] if "showNameCardIdList" in data else []  # noqa: E501
