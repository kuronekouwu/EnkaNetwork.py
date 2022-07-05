from pydantic import BaseModel, Field
from typing import List, Any

from ..json import Config
from ..utils import create_ui_path

class ProfilePicture(BaseModel):
    """
        API Response data
    """
    id: int = Field(0, alias="avatarId")

    """
        Custom add data
    """
    icon: str = ""

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        # Get character
        character = Config.DATA["characters"].get(str(data["avatarId"]))
        if character:
            __pydantic_self__.icon = create_ui_path(character["SideIconName"].replace("_Side", ""))

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
    icon:  str = ""

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        # Get character
        character = Config.DATA["characters"].get(str(data["avatarId"]))
        if character:
            # Get name hash map
            name = Config.HASH_MAP["characters"].get(str(character["NameTextMapHash"]))

            __pydantic_self__.name = name[Config.LANGS]
            __pydantic_self__.icon = create_ui_path(character["SideIconName"].replace("_Side", ""))

class Namecard(BaseModel):
    id: int = 0
    icon: str = ""
    banner: str = ""
    navbar: str = ""
    name: str = ""

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        if __pydantic_self__.id > 0:
            # Get name card
            namecard = Config.DATA["namecards"].get(str(__pydantic_self__.id))

            if namecard:
                __pydantic_self__.name = Config.HASH_MAP["namecards"].get(str(namecard["nameTextMapHash"]))[Config.LANGS]
                __pydantic_self__.icon = create_ui_path(namecard["icon"])
                __pydantic_self__.banner = create_ui_path(namecard["banner"])
                __pydantic_self__.navbar = create_ui_path(namecard["navbar"])

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
    profile_picture: ProfilePicture = Field(None, alias="profilePicture")
    # Avatars
    characters_preview: List[showAvatar] = Field([], alias="showAvatarInfoList")
    # Abyss floor
    abyss_floor: int = Field(0, alias="towerFloorIndex")
    abyss_room: int = Field(0, alias="towerLevelIndex")

    """
        Custom data
    """
    namecard: Namecard = Namecard() # Profile namecard
    list_namecard: List[Namecard] = [] # List namecard preview in profile

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        
        __pydantic_self__.namecard = Namecard(id=data["nameCardId"])
        __pydantic_self__.list_namecard = [Namecard(id=namecard) for namecard in data["showNameCardIdList"]]