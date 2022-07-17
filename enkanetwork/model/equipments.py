import logging

from pydantic import BaseModel, Field
from typing import Any, List

from ..enum import EquipmentsType, DigitType, EquipType
from ..assets import Assets
from ..utils import create_ui_path

LOGGER = logging.getLogger(__name__)

class EquipmentsStats(BaseModel):
    prop_id: str = ""
    type: DigitType = DigitType.NUMBER
    name: str = ""
    value: int = 0

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        if isinstance(data["statValue"], float):
            __pydantic_self__.type = DigitType.PERCENT

        __pydantic_self__.value = data["statValue"]

        LOGGER.debug(f"=== Fight prop ===")

        if "mainPropId" in data:
            __pydantic_self__.prop_id = str(data["mainPropId"])
            fight_prop = Assets.get_hash_map(str(data["mainPropId"]))
        else:
            __pydantic_self__.prop_id = str(data["appendPropId"])
            fight_prop = Assets.get_hash_map(str(data["appendPropId"]))

        if not fight_prop:
            return

        __pydantic_self__.name = fight_prop


class EquipmentsDetail(BaseModel):
    """
        API Response
    """
    nameTextMapHash: str = ""
    setnameTextMapHash: str = ""

    """
        Custom data
    """
    name: str = "" # Get from name hash map
    artifactType: EquipType = EquipType.Unknown # Type of artifact
    icon: str = "" 
    rarity: int = Field(0, alias="rankLevel")
    mainstats: EquipmentsStats = Field(None, alias="reliquaryMainstat")
    substats: List[EquipmentsStats] = []

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        if data["itemType"] == "ITEM_RELIQUARY": # AKA. Artifact
            LOGGER.debug(f"=== Artifact ===")
            __pydantic_self__.icon = Assets.create_icon_path(data["icon"])
            __pydantic_self__.artifactType = EquipType(data["equipType"]).name
            # Sub Stats
            for stats in data["reliquarySubstats"]:
                __pydantic_self__.substats.append(EquipmentsStats.parse_obj(stats))

        if data["itemType"] == "ITEM_WEAPON": # AKA. Weapon
            LOGGER.debug(f"=== Weapon ===")
            __pydantic_self__.icon = create_ui_path(data["icon"])

            # Main and Sub Stats
            __pydantic_self__.mainstats = EquipmentsStats.parse_obj(data["weaponStats"][0])
            for stats in data["weaponStats"][1:]:
                __pydantic_self__.substats.append(EquipmentsStats.parse_obj(stats))

        _name = Assets.get_hash_map(str(data["nameTextMapHash"]))

        if _name is None:
            return

        __pydantic_self__.name = _name


    class Config:
        use_enum_values = True

class Equipments(BaseModel):
    """
        API Response data
    """
    id: int = Field(0, alias="itemId")
    detail: EquipmentsDetail = Field({}, alias="flat")

    """
        Custom data
    """
    level: int = 0 # Get form key "reliquary" and "weapon"
    type: EquipmentsType = EquipmentsType.UNKNOWN # Type of equipments (Ex. Artifact, Weapon)
    refinement: int = 0 # Refinement  of equipments (Weapon only)
    ascension: int = 0 # Ascension (Weapon only)

    class Config:
        use_enum_values = True

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        if data["flat"]["itemType"] == "ITEM_RELIQUARY": # AKA. Artifact
            __pydantic_self__.type = EquipmentsType.ARTIFACT
            __pydantic_self__.level = data["reliquary"]["level"] - 1
        
        if data["flat"]["itemType"] == "ITEM_WEAPON": # AKA. Weapon
            __pydantic_self__.type = EquipmentsType.WEAPON
            __pydantic_self__.level = data["weapon"]["level"]
            if "affixMap" in data["weapon"]:
                __pydantic_self__.refinement = data["weapon"]["affixMap"][list(data["weapon"]["affixMap"].keys())[0]] + 1 
            if "promoteLevel" in data["weapon"]:
                __pydantic_self__.ascension = data["weapon"]["promoteLevel"]
