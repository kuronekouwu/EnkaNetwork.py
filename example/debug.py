import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", debug=True)

async def main():
    async with client:
        await client.fetch_user(843715177)
        # You can see the debug log in console.

loop = asyncio.get_event_loop()
loop.run_until_complete(main())