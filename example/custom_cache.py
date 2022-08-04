import asyncio

from enkanetwork import EnkaNetworkAPI, Cache

class CustomCache(Cache):
    def __init__(self):
        super().__init__(1024, 60 * 3)
        self.cache = {}

client = EnkaNetworkAPI(lang="th", cache=True)
client.set_cache(CustomCache())

async def main():
    async with client:
        await client.fetch_user(843715177)
        await asyncio.sleep(2)
        await client.fetch_user(843715177)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())