import asyncio

from enkanetwork import EnkaNetworkAPI

client = EnkaNetworkAPI(lang="th")

async def main():
    data = await client.fetch_user(843715177)
    print("=== Namecard main ===")
    print(f"ID: {data.player.namecard.id}")
    print(f"Name: {data.player.namecard.name}")
    print(f"Banner URL: {data.player.namecard.banner}")
    print(f"Navbar URL: {data.player.namecard.navbar}")
    print(f"Icon URL: {data.player.namecard.icon}")
    print("\n")
    print("=== List Namecard ===")
    for namecard in data.player.list_namecard:
        print(f"ID: {namecard.id}")
        print(f"Name: {namecard.name}")
        print(f"Banner URL: {namecard.banner}")
        print(f"Navbar URL: {namecard.navbar}")
        print(f"Icon URL: {namecard.icon}")
        print("-"*18)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())