import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th")

async def main():
    data = await client.fetch_user(843715177)
    print("=== Characters ===")
    for character in data.characters:
        print(f"ID: {character.id}")
        print(f"Name: {character.name}")
        print(f"Level: {character.level}")
        print(f"Element: {character.element}")
        print(f"Ascension: {'⭐'*character.ascension}")
        print(f"XP: {character.xp}")
        print(f"Icon: {character.image.icon}")
        print(f"Side icon: {character.image.side}")
        print(f"Wish banner: {character.image.gacha}")
        print("="*18)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())