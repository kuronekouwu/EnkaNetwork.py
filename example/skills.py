import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th")

async def main():
    async with client:
        data = await client.fetch_user(843715177)
        for character in data.characters:
            print(f"=== Skill of {character.name} ===")
            for skill in character.skills:
                print(f"ID: {skill.id}")
                print(f"Name: {skill.name}")
                print(f"Icon: {skill.icon.url}")
                print(f"Level: {skill.level}")
                print("="*18)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())