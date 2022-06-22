from pydantic import BaseModel
from typing import List

class ProfilePicture(BaseModel):
    avatarId: int

class showAvatar(BaseModel):
    avatarId: str
    level: int

class PlayerInfo(BaseModel):
    # Profile info
    finishAchievementNum: int
    level: int
    nameCardId: int
    nickname: str
    signature: str
    worldLevel: int
    profilePicture: ProfilePicture
    # Avatars
    showAvatarInfoList: List[showAvatar]
    # Abyss floor
    towerFloorIndex: int
    towerLevelIndex: int