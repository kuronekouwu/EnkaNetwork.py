from __future__ import annotations

from typing import Any, Dict, List, TypedDict, Union

__all__ = ('EnkaNetwork', 'Default')

class profile_picture(TypedDict):
    avatarId: int

class avatar_info(profile_picture):
    level: int

class player_info(TypedDict):
    nickname: str
    level: int
    signature: str
    worldLevel: int
    nameCardId: int
    finishAchievementNum: int
    towerFloorIndex: int
    towerLevelIndex: int
    showAvatarInfoList: List[avatar_info]
    showNameCardIdList: List[int]
    profilePicture: profile_picture

class avatar_info_full(TypedDict):
    avatarId: int
    propMap: Dict[Dict, Dict[str, Any]]
    talentIdList: List[int]
    fightPropMap: Dict[str, Union[int, float]]
    skillDepotId: int
    inherentProudSkillList: List[int]
    skillLevelMap: Dict[str, int]
    equipList: List[Dict[str, Any]]  # TODO: check if this is correct
    fetterInfo: Dict[str, int]

class EnkaNetworkResponse(TypedDict):
    playerInfo: player_info
    avatarInfoList: avatar_info_full
    ttl: int

class EnkaNetwork(TypedDict):
    status: int
    content: EnkaNetworkResponse

class Default:
    status: int
    content: Any
