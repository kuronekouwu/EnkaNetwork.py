import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", cache=True)

async def main():
    async with client:
        data = await client.fetch_user(843715177)
        print("UID: %s" % data.profile.uid)
        print("URL: %s" % data.profile.url)

asyncio.run(main())