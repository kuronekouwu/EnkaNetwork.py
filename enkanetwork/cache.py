import json

from cachetools import TTLCache


class Cache:
    def __init__(self, maxsize, ttl):
        self.cache = TTLCache(maxsize, ttl)

    def get(self, key):
        return json.loads(self.cache.get(key))

    def set(self, key, value):
        self.cache[key] = json.dumps(value)
