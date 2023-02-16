from pydantic import BaseModel

from ..enum import ProfileRank
from .build import Builds

class EnkaProfile(BaseModel):
    bio: str = ''
    level: ProfileRank = ProfileRank.TIER_1
    signup_state: int = 0
    image_url: str = ''

class ProfileOwner(BaseModel):
    hash: str
    username: str
    profile: EnkaProfile
    builds: Builds = None