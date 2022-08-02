import asyncio

from enkanetwork import EnkaNetworkAPI, Cache

class CustomCache(Cache):
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache[key] = value

client = EnkaNetworkAPI(lang="th", cache=True)
client.set_cache(CustomCache())

async def main():
    await client.fetch_user(843715177)
    await asyncio.sleep(2)
    await client.fetch_user(843715177)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())