import json

from typing import Any, Dict, Optional
from cachetools import TTLCache

__all__ = ('StaticCache','Cache')

class Cache:
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        pass

    async def set(self, key: str, value: Dict[str, Any]) -> None:
        pass

class StaticCache:
    def __init__(self, maxsize: int, ttl: int) -> None:
        self.cache = TTLCache(maxsize, ttl)

    async def get(self, key) -> Dict[str, Any]:
        data = self.cache.get(key)
        return json.loads(data) if data is not None else data

    async def set(self, key, value) -> None:
        self.cache[key] = json.dumps(value)
