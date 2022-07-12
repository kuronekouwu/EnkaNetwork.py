from enum import Enum

class EquipmentsType(int, Enum):
    UNKNOWN = -1
    ARTIFACT = 0
    WEAPON = 1

class DigitType(int, Enum):
    NUMBER = 0
    PERCENT = 1
    
class ElementType(str, Enum):
    Unknown = "Unknown"
    Ice = "Cyro"
    Water = "Hydro"
    Wind = "Anemo"
    Fire = "Pyro"
    Rock = "Geo"
    Electric = "Electro"

class EquipType(str, Enum):
    UNKNOWN = "Unknown"
    EQUIP_BRACER = "Flower"
    EQUIP_NECKLACE = "Feather"
    EQUIP_SHOES = "Sands"
    EQUIP_RING = "Goblet"
    EQUIP_DRESS = "Circlet"