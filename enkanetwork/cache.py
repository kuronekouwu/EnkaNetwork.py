import json

from cachetools import TTLCache

__all__ = ('Cache',)

class Cache:
    def __init__(self, maxsize, ttl):
        self.cache = TTLCache(maxsize, ttl)

    async def get(self, key):
        data = self.cache.get(key)
        return json.loads(data) if data is not None else data

    async def set(self, key, value):
        self.cache[key] = json.dumps(value)
