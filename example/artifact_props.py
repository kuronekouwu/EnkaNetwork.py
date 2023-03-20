import asyncio

from enkanetwork import EnkaNetworkAPI
from enkanetwork import EquipmentsType, DigitType

client = EnkaNetworkAPI(lang="th")

async def main():
    async with client:
        data = await client.fetch_user(843715177)
        for character in data.characters:
            print(f"=== Artifacts props of {character.name} ===")
            for artifact in filter(lambda x: x.type == EquipmentsType.ARTIFACT, character.equipments):
                print(f"ID: {artifact.id}")
                print(f"Name: {artifact.detail.name}")
                print(f"Type: {artifact.detail.artifact_type}")
                print("--- Props ---")
                for props in artifact.props:
                    print(f"ID: {props.id}")
                    print(f"Type: {props.prop_id}")
                    print(f"Raw name: {props.name}")
                    print(f"Full name: {props.get_full_name()}")
                    print(f"Value (Formatted): {props.get_value_symbol()}")
                    print("-"*18)
                    
            print("="*18)

asyncio.run(main())