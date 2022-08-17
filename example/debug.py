import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", debug=True)

async def main():
    async with client:
        await client.fetch_user(843715177)
        # You can see the debug log in console.

asyncio.run(main())