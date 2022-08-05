import json

from typing import Any, Dict
from cachetools import TTLCache

__all__ = ('Cache',)

class Cache:
    def __init__(self, maxsize: int, ttl: int) -> None:
        self.cache = TTLCache(maxsize, ttl)

    async def get(self, key) -> Dict[str, Any]:
        data = self.cache.get(key)
        return json.loads(data) if data is not None else data

    async def set(self, key, value) -> None:
        self.cache[key] = json.dumps(value)
