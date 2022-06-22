from pydantic import BaseModel, Field

class CharacterCombat(BaseModel):
    # Default character combat [1,4,7]
    BASE_HP: int = Field(0, alias="1")
    BASE_ATK: int = Field(0, alias="4")
    BASE_DEF: int = Field(0, alias="7")

    # CRITRATE combat [20-22]
    CRIT_RATE: int = Field(0, alias="20")
    CRIT_DAMAGE: int = Field(0, alias="22")

    # (?) [23, 26 - 29]
    ENERGRY_RECHARGE: int = Field(0, alias="23")
    HEALING_BONUS: int = Field(0, alias="26")
    INCOMING_HEALING_BONUS: int = Field(0, alias="27")
    ELEMENTAL_MASTERY: int = Field(0, alias="28")
    
    # DEF (RES --> DEF) [29, 50 - 56]
    PHYSICAL_DEF: int = Field(0, alias="29")
    PYRO_DEF: int = Field(0, alias="50")
    ELECTRO_DEF: int = Field(0, alias="51")
    HYDRO_DEF: int = Field(0, alias="52")
    DENDRO_DEF: int = Field(0, alias="53")
    ANEMO_DEF: int = Field(0, alias="54")
    GEO_DEF: int = Field(0, alias="55")
    CYRO_DEF: int = Field(0, alias="56")

    # Energy Cost [70 - 76]
    PYRO_COST: int = Field(0, alias="70")
    ELECTRO_COST: int = Field(0, alias="71")
    HYDRO_COST: int = Field(0, alias="72")
    DENDRO_COST: int = Field(0, alias="73")
    ANEMO_COST: int = Field(0, alias="74")
    GEO_COST: int = Field(0, alias="75")
    CYRO_COST: int = Field(0, alias="76")

    # Bonus damage [30, 40-46]
    PHYSICAL_BONUS: int = Field(0, alias="30")
    PYRO_BONUS: int = Field(0, alias="40")
    ELECTRO_BONUS: int = Field(0, alias="41")
    HYDRO_BONUS: int = Field(0, alias="42")
    DENDRO_BONUS: int = Field(0, alias="43")
    ANEMO_BONUS: int = Field(0, alias="44")
    GEO_BONUS: int = Field(0, alias="45")
    CYRO_BONUS: int = Field(0, alias="46")
    
    # DATA SUMMARY [2000-2002]
    MAX_HP: int = Field(0, alias="2000")
    ATK: int = Field(0, alias="2001")
    DEF: int = Field(0, alias="2002")
