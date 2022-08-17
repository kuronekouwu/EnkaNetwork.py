import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", debug=True)

async def main():
    async with client:
        # Change language to "en"
        client.lang = "en"
        # Or you can use set_language() function (EN -> TW)
        await client.set_language("cht")

asyncio.run(main())