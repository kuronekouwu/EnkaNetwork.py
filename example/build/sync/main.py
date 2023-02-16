import asyncio
import json

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th")

async def main():
    async with client:
        # Load old data build
        with open("./raw.json", "r") as f:
            old = json.load(f)
            export = await client.sync_build(old["uid"], old)
            # Export new data
            with open("./export.json", "w", encoding="utf-8") as w:
                json.dump(export, w, indent=4)

asyncio.run(main())