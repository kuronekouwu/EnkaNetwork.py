import asyncio

from enkanetwork import EnkaNetworkAPI
from enkanetwork.model.stats import Stats

client = EnkaNetworkAPI(lang="th")

async def main():
    async with client:
        data = await client.fetch_user(843715177)

        for character in data.characters:
            print(f"=== Stats of {character.name} ===")
            for stat in character.stats:
                print(f"- {stat[0]}: {stat[1].to_rounded() if isinstance(stat[1], Stats) else stat[1].to_percentage_symbol()}")
            print("="*18)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())