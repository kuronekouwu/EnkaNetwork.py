from enum import Enum

__all__ = (
    'Language',
    'EquipmentsType',
    'DigitType',
    'ElementType',
    'EquipType'
)

class Language(str, Enum):
    EN = "en"
    RU = "ru"
    VI = "vi"
    TH = "th"
    PT = "pt"
    KR = "kr"
    JP = "jp"
    ID = "id"
    FR = "fr"
    ES = "es"
    DE = "de"
    IT = "it"
    TR = "tr"

    """
        zh-CN: CHT
        zh-TW: CHS
    """
    TW = "cht"
    CN = "chs"
    CHT = "cht"
    CHS = "chs"


class EquipmentsType(int, Enum):
    UNKNOWN = -1
    ARTIFACT = 0
    WEAPON = 1


class DigitType(int, Enum):
    NUMBER = 0
    PERCENT = 1


class ElementType(str, Enum):
    Unknown = "Unknown"
    Cryo = "Ice"
    Hydro = "Water"
    Anemo = "Wind"
    Pyro = "Fire"
    Geo = "Rock"
    Electro = "Electric"
    Dendro = "Grass"

class EquipType(str, Enum):
    Unknown = "UNKNOWN"
    Flower = "EQUIP_BRACER"
    Feather = "EQUIP_NECKLACE"
    Sands = "EQUIP_SHOES"
    Goblet = "EQUIP_RING"
    Circlet = "EQUIP_DRESS"

class ProfileRank(int, Enum):
    TIER_LEGACY = -1
    TIER_NONE = 0
    TIER_1 = 1
    TIER_2 = 2
    TIER_3 = 3
