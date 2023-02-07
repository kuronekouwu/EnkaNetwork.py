import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", cache=True)

async def main():
    async with client:
        data = await client.fetch_user_by_username("Algoinde")
        print("Username: %s" % data.username)
        print("Level: %s" % data.profile.level)
        print("Image: %s" % data.profile.image_url)
        print(f"=== Hoyos Info ===")
        for hoyos in data.hoyos:
            print(f"Hash ID: {hoyos.hash}")
            print(f"UID Public: {hoyos.uid_public}")
            print(f"Verified: {hoyos.verified}")
            print(f"=== Player Info ===")
            print(f"Nickname: {hoyos.player_info.nickname}")
            print(f"Level: {hoyos.player_info.level}")
            print(f"Icon: {hoyos.player_info.avatar.icon.url}")
            print(f"Signature: {hoyos.player_info.signature}")
            print(f"Achievement: {hoyos.player_info.achievement}")
            print(f"Abyss floor: {hoyos.player_info.abyss_floor} - {hoyos.player_info.abyss_room}")
            print("=== Characters Preview ===")
            for charactersPreview in hoyos.player_info.characters_preview:
                print("ID:", charactersPreview.id)
                print("Name:", charactersPreview.name)
                print("Icon:", charactersPreview.icon.url)
                print("Level:", charactersPreview.level)
                print("="*18)

asyncio.run(main())