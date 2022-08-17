import asyncio

from enkanetwork import Assets

assets = Assets(lang="th")

async def main():
    character = assets.character(10000046)
    name = assets.get_hash_map(character.hash_id)

    print("=== Asset character ===")
    print(f"ID: {character.id}")
    print(f"Name (Hash ID): {character.hash_id}")
    print(f"Name (Hashed): {name}")
    print(f"Icon URL: {character.images.icon}")
    print(f"Side Icon URL: {character.images.side}")
    print(f"Banner URL: {character.images.banner}")
    print(f"=== Skills ===")
    for skill in character.skills:
        skill_info = assets.skills(skill)
        name = assets.get_hash_map(skill_info.hash_id)
        print(f"ID: {skill_info.id}")
        print(f"Name (Hash ID): {skill_info.hash_id}")
        print(f"Name (Hashed): {name}")
        print(f"Icon URL: {skill_info.icon}")
    
    print(f"=== Constellations ===")
    for constellation in character.constellations:
        constellation_info = assets.constellations(constellation)
        name = assets.get_hash_map(constellation_info.hash_id)
        print(f"ID: {constellation_info.id}")
        print(f"Name (Hash ID): {constellation_info.hash_id}")
        print(f"Name (Hashed): {name}")
        print(f"Icon URL: {constellation_info.icon}")


asyncio.run(main())