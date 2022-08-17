import asyncio

from enkanetwork import Assets

assets = Assets(lang="th")

async def main():
    namecard = assets.namecards(210059)
    name = assets.get_hash_map(namecard.hash_id)

    print("=== Asset character ===")
    print(f"ID: {namecard.id}")
    print(f"Name (Hash ID): {namecard.hash_id}")
    print(f"Name (Hashed): {name}")
    print(f"Icon: {namecard.icon}")
    print(f"Banner URL: {namecard.banner}")
    print(f"Navbar (Alpha) URL: {namecard.navbar}")

asyncio.run(main())