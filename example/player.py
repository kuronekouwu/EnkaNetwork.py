import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th")

async def main():
    async with client:
        data = await client.fetch_user(843715177)
        print("=== Player Info ===")
        print(f"Nickname: {data.player.nickname}")
        print(f"Level: {data.player.level}")
        print(f"Icon: {data.player.icon.url}")
        print(f"Signature: {data.player.signature}")
        print(f"Achievement: {data.player.achievement}")
        print(f"Abyss floor: {data.player.abyss_floor} - {data.player.abyss_room}")
        print(f"Cache timeout: {data.ttl}")
        print("=== Characters Preview ===")
        for charactersPreview in data.player.characters_preview:
            print("ID:", charactersPreview.id)
            print("Name:", charactersPreview.name)
            print("Icon:", charactersPreview.icon.url)
            print("Level:", charactersPreview.level)
            print("="*18)

asyncio.run(main())