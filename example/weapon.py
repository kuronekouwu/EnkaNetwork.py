import asyncio

from enkanetwork import EnkaNetworkAPI
from enkanetwork.enum import DigitType

client = EnkaNetworkAPI(lang="th")

async def main():
    data = await client.fetch_user(843715177)
    for character in data.characters:
        print(f"=== Weapon of {character.name} ===")
        weapon = character.equipments[-1]
        print(f"ID: {weapon.id}")
        print(f"Name: {weapon.detail.name}")
        print(f"Icon: {weapon.detail.icon}")
        print(f"Level: {weapon.level}")
        print(f"Refinement (R): {weapon.refinement}")
        print("--- Main Stats ---")
        print(f"Name: {weapon.detail.mainstats.name}")
        print(f"Value: {weapon.detail.mainstats.value}{'%' if weapon.detail.mainstats.type == DigitType.PERCENT else ''}")
        print("--- Sub Stats ---")
        for substate in weapon.detail.substats:
            print(f"Name: {substate.name}")
            print(f"Value: {substate.value}{'%' if substate.type == DigitType.PERCENT else ''}")
            print("-"*18)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())