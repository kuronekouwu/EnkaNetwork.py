import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(debug=True)

async def main():
    async with client:
        await client.update_assets()
        # You can see the progress download new assets in console

loop = asyncio.get_event_loop()
loop.run_until_complete(main())