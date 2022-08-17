import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(debug=True)

async def main():
    async with client:
        await client.update_assets()
        # You can see the progress download new assets in console

asyncio.run(main())