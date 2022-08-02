import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", cache=True)

async def main():
    data = await client.fetch_user(843715177)
    print("TTL: %s" % data.ttl)
    await asyncio.sleep(2)
    data_catched = await client.fetch_user(843715177)
    print("TTL: %s" % data_catched.ttl)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())