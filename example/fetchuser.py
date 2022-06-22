import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI()

async def main():
    data = await client.fetch_user(843715177)
    print(f"Nickname: {data.player.nickname}")
    print(f"Level: {data.player.level}")
    print(f"Cache timeout: {data.ttl}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())