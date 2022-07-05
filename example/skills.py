import asyncio

from enkanetwork import EnkaNetworkAPI, Config

client = EnkaNetworkAPI(lang="th")

async def main():
    data = await client.fetch_user(843715177)
    for character in data.characters:
        print(f"=== Skill of {character.name} ===")
        for constellation in character.constellations:
            print(f"ID: {constellation.id}")
            print(f"Name: {constellation.name}")
            print(f"Icon: {constellation.icon}")
            print(f"Unlocked: {constellation.unlocked}")
            print("="*18)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())