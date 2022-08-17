import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th")

async def main():
    async with client:
        data = await client.fetch_user(843715177)
        for character in data.characters:
            print(f"=== Constellations of {character.name} ===")
            for constellation in character.constellations:
                print(f"ID: {constellation.id}")
                print(f"Name: {constellation.name}")
                print(f"Icon: {constellation.icon.url}")
                print(f"Unlocked: {constellation.unlocked}")
                print("="*18)

asyncio.run(main())