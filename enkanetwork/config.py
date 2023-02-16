from typing import (
    ClassVar
)
from .utils import get_user_agent
from .cache import Cache, StaticCache

class Config:
    # HTTP Config
    ENKA_PROTOCOL: ClassVar[str] = "https"
    ENKA_URL: ClassVar[str] = "enka.network"
    # Assets
    ASSETS_PROTOCOL: ClassVar[str] = "https"
    ASSETS_URL: ClassVar[str] = "raw.githubusercontent.com"
    # Header Config
    USER_AGENT: ClassVar[str] = get_user_agent()
    # Client config
    CACHE_ENABLED: ClassVar[bool] = True
    CACHE: ClassVar[Cache] = StaticCache(1024, 60 * 3)

    @classmethod
    def init_cache(
        cls, 
        cache: Cache,
        enabled: bool = True
    ):
        cls.CACHE = cache
        cls.CACHE_ENABLED = enabled
    
    @classmethod
    def init_user_agent(cls, agent: str):
        cls.USER_AGENT = agent