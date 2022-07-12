import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", debug=True)

async def main():
    await client.download_data()
    # You can see the progress download new content in console

loop = asyncio.get_event_loop()
loop.run_until_complete(main())