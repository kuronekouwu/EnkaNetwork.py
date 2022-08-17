import math

from pydantic import BaseModel

from typing import Any

__all__ = (
    'Stats',
    'StatsPercentage',
    'CharacterStats'
)

class Stats(BaseModel):
    id: int = 0
    value: float = 0

    def to_rounded(self) -> float:
        return math.ceil(self.value)


class StatsPercentage(BaseModel):
    id: int = 0
    value: float = 0.0

    def to_percentage(self) -> float:
        return round((round(self.value, 3) * 100), 1)

    def to_percentage_symbol(self) -> str:
        return f"{self.to_percentage()}%"


class CharacterStats(BaseModel):
    BASE_HP: Stats = Stats(id=1, value=0)
    FIGHT_PROP_HP: Stats = Stats(id=2, value=0)
    FIGHT_PROP_HP_PERCENT: StatsPercentage = StatsPercentage(id=3, value=0)
    FIGHT_PROP_BASE_ATTACK: Stats = Stats(id=4, value=0)
    FIGHT_PROP_ATTACK: Stats = Stats(id=5, value=0)
    FIGHT_PROP_ATTACK_PERCENT: StatsPercentage = StatsPercentage(id=6, value=0)
    FIGHT_PROP_BASE_DEFENSE: Stats = Stats(id=7, value=0)
    FIGHT_PROP_DEFENSE: Stats = Stats(id=8, value=0)
    FIGHT_PROP_DEFENSE_PERCENT: StatsPercentage = StatsPercentage(id=9, value=0)
    FIGHT_PROP_BASE_SPEED: Stats = Stats(id=10, value=0)
    FIGHT_PROP_SPEED_PERCENT: StatsPercentage = StatsPercentage(id=11, value=0)
    FIGHT_PROP_HP_MP_PERCENT: StatsPercentage = StatsPercentage(id=12, value=0)
    FIGHT_PROP_ATTACK_MP_PERCENT: Stats = Stats(id=13, value=0)
    FIGHT_PROP_CRITICAL: StatsPercentage = StatsPercentage(id=20, value=0)
    FIGHT_PROP_ANTI_CRITICAL: StatsPercentage = StatsPercentage(id=21, value=0)
    FIGHT_PROP_CRITICAL_HURT: StatsPercentage = StatsPercentage(id=22, value=0)
    FIGHT_PROP_CHARGE_EFFICIENCY: StatsPercentage = StatsPercentage(id=23, value=0)
    FIGHT_PROP_ADD_HURT: StatsPercentage = StatsPercentage(id=24, value=0)
    FIGHT_PROP_SUB_HURT: StatsPercentage = StatsPercentage(id=25, value=0)
    FIGHT_PROP_HEAL_ADD: StatsPercentage = StatsPercentage(id=26, value=0)
    FIGHT_PROP_HEALED_ADD: StatsPercentage = StatsPercentage(id=27, value=0)
    FIGHT_PROP_ELEMENT_MASTERY: Stats = Stats(id=28, value=0)
    FIGHT_PROP_PHYSICAL_SUB_HURT: StatsPercentage = StatsPercentage(id=29, value=0)
    FIGHT_PROP_PHYSICAL_ADD_HURT: StatsPercentage = StatsPercentage(id=30, value=0)
    FIGHT_PROP_DEFENCE_IGNORE_RATIO: Stats = Stats(id=31, value=0)
    FIGHT_PROP_DEFENCE_IGNORE_DELTA: Stats = Stats(id=32, value=0)
    FIGHT_PROP_FIRE_ADD_HURT: StatsPercentage = StatsPercentage(id=40, value=0)
    FIGHT_PROP_ELEC_ADD_HURT: StatsPercentage = StatsPercentage(id=41, value=0)
    FIGHT_PROP_WATER_ADD_HURT: StatsPercentage = StatsPercentage(id=42, value=0)
    FIGHT_PROP_GRASS_ADD_HURT: StatsPercentage = StatsPercentage(id=43, value=0)
    FIGHT_PROP_WIND_ADD_HURT: StatsPercentage = StatsPercentage(id=44, value=0)
    FIGHT_PROP_ROCK_ADD_HURT: StatsPercentage = StatsPercentage(id=45, value=0)
    FIGHT_PROP_ICE_ADD_HURT: StatsPercentage = StatsPercentage(id=46, value=0)
    FIGHT_PROP_HIT_HEAD_ADD_HURT: StatsPercentage = StatsPercentage(id=47, value=0)
    FIGHT_PROP_FIRE_SUB_HURT: StatsPercentage = StatsPercentage(id=50, value=0)
    FIGHT_PROP_ELEC_SUB_HURT: StatsPercentage = StatsPercentage(id=51, value=0)
    FIGHT_PROP_WATER_SUB_HURT: StatsPercentage = StatsPercentage(id=52, value=0)
    FIGHT_PROP_GRASS_SUB_HURT: StatsPercentage = StatsPercentage(id=53, value=0)
    FIGHT_PROP_WIND_SUB_HURT: StatsPercentage = StatsPercentage(id=54, value=0)
    FIGHT_PROP_ROCK_SUB_HURT: StatsPercentage = StatsPercentage(id=55, value=0)
    FIGHT_PROP_ICE_SUB_HURT: StatsPercentage = StatsPercentage(id=56, value=0)
    FIGHT_PROP_EFFECT_HIT: Stats = Stats(id=60, value=0)
    FIGHT_PROP_EFFECT_RESIST: Stats = Stats(id=61, value=0)
    FIGHT_PROP_FREEZE_RESIST: Stats = Stats(id=62, value=0)
    FIGHT_PROP_TORPOR_RESIST: Stats = Stats(id=63, value=0)
    FIGHT_PROP_DIZZY_RESIST: Stats = Stats(id=64, value=0)
    FIGHT_PROP_FREEZE_SHORTEN: Stats = Stats(id=65, value=0)
    FIGHT_PROP_TORPOR_SHORTEN: Stats = Stats(id=66, value=0)
    FIGHT_PROP_DIZZY_SHORTEN: Stats = Stats(id=67, value=0)
    FIGHT_PROP_MAX_FIRE_ENERGY: Stats = Stats(id=70, value=0)
    FIGHT_PROP_MAX_ELEC_ENERGY: Stats = Stats(id=71, value=0)
    FIGHT_PROP_MAX_WATER_ENERGY: Stats = Stats(id=72, value=0)
    FIGHT_PROP_MAX_GRASS_ENERGY: Stats = Stats(id=73, value=0)
    FIGHT_PROP_MAX_WIND_ENERGY: Stats = Stats(id=74, value=0)
    FIGHT_PROP_MAX_ICE_ENERGY: Stats = Stats(id=75, value=0)
    FIGHT_PROP_MAX_ROCK_ENERGY: Stats = Stats(id=76, value=0)
    FIGHT_PROP_SKILL_CD_MINUS_RATIO: Stats = Stats(id=80, value=0)
    FIGHT_PROP_SHIELD_COST_MINUS_RATIO: Stats = Stats(id=81, value=0)

    FIGHT_PROP_CUR_FIRE_ENERGY: Stats = Stats(id=1000, value=0)
    FIGHT_PROP_CUR_ELEC_ENERGY: Stats = Stats(id=1001, value=0)
    FIGHT_PROP_CUR_WATER_ENERGY: Stats = Stats(id=1002, value=0)
    FIGHT_PROP_CUR_GRASS_ENERGY: Stats = Stats(id=1003, value=0)
    FIGHT_PROP_CUR_WIND_ENERGY: Stats = Stats(id=1004, value=0)
    FIGHT_PROP_CUR_ICE_ENERGY: Stats = Stats(id=1005, value=0)
    FIGHT_PROP_CUR_ROCK_ENERGY: Stats = Stats(id=1006, value=0)
    FIGHT_PROP_CUR_HP: Stats = Stats(id=1010, value=0)

    FIGHT_PROP_MAX_HP: Stats = Stats(id=2000, value=0)
    FIGHT_PROP_CUR_ATTACK: Stats = Stats(id=2001, value=0)
    FIGHT_PROP_CUR_DEFENSE: Stats = Stats(id=2002, value=0)
    FIGHT_PROP_CUR_SPEED: Stats = Stats(id=2003, value=0)

    FIGHT_PROP_NONEXTRA_ATTACK: Stats = Stats(id=3000, value=0)
    FIGHT_PROP_NONEXTRA_DEFENSE: Stats = Stats(id=3001, value=0)
    FIGHT_PROP_NONEXTRA_CRITICAL: StatsPercentage = StatsPercentage(id=3002, value=0)
    FIGHT_PROP_CUR_SPEED: Stats = Stats(id=3003, value=0)
    FIGHT_PROP_NONEXTRA_CRITICAL_HURT: StatsPercentage = StatsPercentage(id=3004, value=0)
    FIGHT_PROP_NONEXTRA_CHARGE_EFFICIENCY: StatsPercentage = StatsPercentage(id=3005, value=0)
    FIGHT_PROP_NONEXTRA_ELEMENT_MASTERY: Stats = Stats(id=3006, value=0)
    FIGHT_PROP_NONEXTRA_PHYSICAL_SUB_HURT: StatsPercentage = StatsPercentage(id=3007, value=0)
    FIGHT_PROP_NONEXTRA_FIRE_ADD_HURT: StatsPercentage = StatsPercentage(id=3008, value=0)
    FIGHT_PROP_NONEXTRA_ELEC_ADD_HURT: StatsPercentage = StatsPercentage(id=3009, value=0)
    FIGHT_PROP_NONEXTRA_WATER_ADD_HURT: StatsPercentage = StatsPercentage(id=3010, value=0)
    FIGHT_PROP_NONEXTRA_GRASS_ADD_HURT: StatsPercentage = StatsPercentage(id=3011, value=0)
    FIGHT_PROP_NONEXTRA_WIND_ADD_HURT: StatsPercentage = StatsPercentage(id=3012, value=0)
    FIGHT_PROP_NONEXTRA_ROCK_ADD_HURT: StatsPercentage = StatsPercentage(id=3013, value=0)
    FIGHT_PROP_NONEXTRA_ICE_ADD_HURT: StatsPercentage = StatsPercentage(id=3014, value=0)
    FIGHT_PROP_NONEXTRA_FIRE_SUB_HURT: StatsPercentage = StatsPercentage(id=3015, value=0)
    FIGHT_PROP_NONEXTRA_ELEC_SUB_HURT: StatsPercentage = StatsPercentage(id=3016, value=0)
    FIGHT_PROP_NONEXTRA_WATER_SUB_HURT: StatsPercentage = StatsPercentage(id=3017, value=0)
    FIGHT_PROP_NONEXTRA_GRASS_SUB_HURT: StatsPercentage = StatsPercentage(id=3018, value=0)
    FIGHT_PROP_NONEXTRA_WIND_SUB_HURT: StatsPercentage = StatsPercentage(id=3019, value=0)
    FIGHT_PROP_NONEXTRA_ROCK_SUB_HURT: StatsPercentage = StatsPercentage(id=3020, value=0)
    FIGHT_PROP_NONEXTRA_ICE_SUB_HURT: StatsPercentage = StatsPercentage(id=3021, value=0)
    FIGHT_PROP_NONEXTRA_SKILL_CD_MINUS_RATIO: Stats = Stats(id=3022, value=0)
    FIGHT_PROP_NONEXTRA_SHIELD_COST_MINUS_RATIO: Stats = Stats(id=3023, value=0)
    FIGHT_PROP_NONEXTRA_PHYSICAL_ADD_HURT: StatsPercentage = StatsPercentage(id=3024, value=0)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        _stats = self.__dict__
        for key in _stats:
            _stats[key].value = data[str(_stats[key].id)] if str(_stats[key].id) in data else 0
