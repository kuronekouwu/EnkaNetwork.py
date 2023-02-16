import asyncio
import json

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th")

async def main():
    async with client:
        # Fetch data
        raw = await client.fetch_raw_data(843715177)
        # Write JSON file
        with open(f"./{raw['uid']}.json", "w", encoding="utf-8") as w:
            json.dump(raw, w, indent=4)

asyncio.run(main())