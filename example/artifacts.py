import asyncio

from enkanetwork import EnkaNetworkAPI
from enkanetwork.enum import EquipmentsType, DigitType

client = EnkaNetworkAPI(lang="th")

async def main():
    data = await client.fetch_user(843715177)
    for character in data.characters:
        print(f"=== Artifacts of {character.name} ===")
        for artifact in filter(lambda x: x.type == EquipmentsType.ARTIFACT,character.equipments):
            print(f"ID: {artifact.id}")
            print(f"Name: {artifact.detail.name}")
            print(f"Type: {artifact.detail.artifact_type}")
            print(f"Icon: {artifact.detail.icon}")
            print(f"Level: {artifact.level}")
            print("--- Main Stats ---")
            print(f"Name: {artifact.detail.mainstats.name}")
            print(f"Value: {artifact.detail.mainstats.value}{'%' if artifact.detail.mainstats.type == DigitType.PERCENT else ''}")
            print("--- Sub Stats ---")
            for substate in artifact.detail.substats:
                print(f"Name: {substate.name}")
                print(f"Value: {substate.value}{'%' if substate.type == DigitType.PERCENT else ''}")
                print("-"*18)

        print("="*18)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())