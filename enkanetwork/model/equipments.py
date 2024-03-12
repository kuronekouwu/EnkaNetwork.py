import logging

from pydantic import BaseModel, Field
from typing import Any, List, Union

from .utils import IconAsset

from ..enum import EquipmentsType, DigitType, EquipType
from ..assets import Assets

LOGGER = logging.getLogger(__name__)

__all__ = (
    'EquipmentsStats',
    'EquipmentsDetail',
    'Equipments'
)


class EquipmentsStats(BaseModel):
    prop_id: str = ""
    type: DigitType = DigitType.NUMBER
    name: str = ""
    value: int | float = Field(0, alias="statValue")

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        LOGGER.debug("=== Fight prop ===")

        if "mainPropId" in data:
            self.prop_id = str(data["mainPropId"])
            fight_prop = Assets.get_hash_map(str(data["mainPropId"]))
        else:
            self.prop_id = str(data["appendPropId"])
            fight_prop = Assets.get_hash_map(str(data["appendPropId"]))

        prod_id = ["HURT", "CRITICAL", "EFFICIENCY", "PERCENT", "ADD"]

        if self.prop_id.split("_")[-1] in prod_id:
            self.value = float(data["statValue"])
            self.type = DigitType.PERCENT

        if not fight_prop:
            return

        self.name = fight_prop


class EquipmentsDetail(BaseModel):
    """
        Custom data
    """
    name: str = ""  # Get from name hash map
    artifact_name_set: str = ""  # Name set artifacts
    artifact_type: EquipType = EquipType.Unknown  # Type of artifact
    icon: IconAsset = None
    rarity: int = Field(0, alias="rankLevel")
    mainstats: EquipmentsStats = Field(None, alias="reliquaryMainstat")
    substats: List[EquipmentsStats] = []

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        if data["itemType"] == "ITEM_RELIQUARY":  # AKA. Artifact
            LOGGER.debug("=== Artifact ===")
            self.artifact_type = EquipType(data["equipType"])
            # Sub Stats
            for stats in data["reliquarySubstats"] if "reliquarySubstats" in data else []:
                self.substats.append(EquipmentsStats.model_validate(stats))

        if data["itemType"] == "ITEM_WEAPON":  # AKA. Weapon
            LOGGER.debug("=== Weapon ===")

            # Main and Sub Stats
            self.mainstats = EquipmentsStats.model_validate(
                data["weaponStats"][0])
            for stats in data["weaponStats"][1:]:
                self.substats.append(EquipmentsStats.model_validate(stats))

        _name = Assets.get_hash_map(data.get("nameTextMapHash"))
        if "setNameTextMapHash" in data:
            _artifact_name_set = Assets.get_hash_map(str(data["setNameTextMapHash"]))
            self.artifact_name_set = _artifact_name_set or ""

        self.name = _name if _name is not None else ""

    class Config:
        use_enum_values = True

class EquipmentsProps(BaseModel):
    id: int = 0
    prop_id: str = ''
    name: str = ''
    digit: DigitType = DigitType.NUMBER
    value: int | float = 0
    
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self.name = Assets.get_hash_map(self.prop_id)

    def get_value_symbol(self):
        return f"{self.value}{'%' if self.digit == DigitType.PERCENT else ''}"

    def get_full_name(self):
        raw = self.value
        return f"{self.name}{str(raw) if raw < 0 else '+'+str(raw)}{'%' if self.digit == DigitType.PERCENT else ''}"

class Equipments(BaseModel):
    """
        API Response data
    """
    id: int = Field(0, alias="itemId")
    detail: EquipmentsDetail = Field({}, alias="flat")

    """
        Custom data
    """
    level: int = 0  # Get form key "reliquary" and "weapon"
    max_level: int = 0
    # Type of equipments (Ex. Artifact, Weapon)
    type: EquipmentsType = EquipmentsType.UNKNOWN
    refinement: int = 1  # Refinement  of equipments (Weapon only)
    ascension: int = 0  # Ascension (Weapon only)
    props: List[EquipmentsProps] = []

    class Config:
        use_enum_values = True

    def __init__(self, **data: Any) -> None:
        data["flat"]["icon"] = IconAsset(filename=data["flat"]["icon"])
        super().__init__(**data)

        if data["flat"]["itemType"] == "ITEM_RELIQUARY":  # AKA. Artifact
            self.type = EquipmentsType.ARTIFACT
            self.level = data["reliquary"]["level"] - 1
            self.max_level = 4 * data["flat"]["rankLevel"]

            for props in data["reliquary"].get("appendPropIdList", []):
                props_info = Assets.artifact_props(props)
                if props_info: 
                    self.props.append(EquipmentsProps(**{
                        "id": props_info.id,
                        "prop_id": props_info.type,
                        "digit": DigitType.PERCENT if props_info.digit == 'PERCENT' else DigitType.NUMBER,
                        "value": props_info.value
                    }))

        if data["flat"]["itemType"] == "ITEM_WEAPON":  # AKA. Weapon
            self.type = EquipmentsType.WEAPON
            self.level = data["weapon"]["level"]

            if "affixMap" in data["weapon"]:
                self.refinement = data["weapon"]["affixMap"][
                                                   list(data["weapon"]["affixMap"].keys())[0]] + 1

            if "promoteLevel" in data["weapon"]:
                self.ascension = data["weapon"]["promoteLevel"]
                self.max_level = (self.ascension * 10) + (
                    10 if self.ascension > 0 else 0) + 20
                
                if self.ascension >= 2:
                    self.detail.icon = IconAsset(filename=self.detail.icon.filename + "_Awaken")
            