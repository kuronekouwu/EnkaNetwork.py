import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th", cache=True)

async def main():
    async with client:
        data = await client.fetch_user_by_username("Algoinde")
        print(f"=== Build(s) info ===")
        for hoyos in data.hoyos:
            for avatarId in hoyos.builds.get_avatar_list():
                avatarSets = hoyos.builds.get_character(avatarId)
                print(f"AvatarID: {avatarId}")
                for avatarSetInfo in avatarSets:
                    print(f"Name: {'Current' if avatarSetInfo.live else avatarSetInfo.name}")
                    print(f"Public: {avatarSetInfo.public}")
                    print("=== Characters info ===")
                    print(f"ID: {avatarSetInfo.avatar_data.id}")
                    print(f"Name: {avatarSetInfo.avatar_data.name}")
                    print(f"Level: {avatarSetInfo.avatar_data.level} / {avatarSetInfo.avatar_data.max_level}")
                    print(f"Rarity: {avatarSetInfo.avatar_data.rarity}")
                    print(f"Element: {avatarSetInfo.avatar_data.element}")
                    print(f"Friendship Level: {avatarSetInfo.avatar_data.friendship_level}")
                    print(f"Ascension: {'⭐'*avatarSetInfo.avatar_data.ascension}")
                    print(f"Constellations unlocked: C{avatarSetInfo.avatar_data.constellations_unlocked}")
                    print(f"XP: {avatarSetInfo.avatar_data.xp}")
                    print(f"Icon: {avatarSetInfo.avatar_data.image.icon.url}")
                    print(f"Side icon: {avatarSetInfo.avatar_data.image.side.url}")
                    print(f"Wish banner: {avatarSetInfo.avatar_data.image.banner.url}")
                    print(f"Card icon: {avatarSetInfo.avatar_data.image.card.url}")
                    print("="*18)

asyncio.run(main())