# models.py
from dataclasses import dataclass, asdict
from typing import Any, Mapping

def get_stat(stats: dict[str, Any], key: str, value: float = 0.0) -> float:
    """
    Fetch a stat from a dictionary with a default value.
    
    TODO
    """
    stats = stats.get("stats", {})
    return float(stats.get(key, value))

@dataclass
class ChampionStats:
    """Encapsulates champion stats, including base, per-level, bonus, current, and missing values."""
    health_base: float
    health_level: float

    health_regen_base: float
    health_regen_level: float
    
    armor_base: float
    armor_level: float

    magic_resist_base: float
    magic_resist_level: float

    attack_speed_ratio: float
    attack_speed_base: float
    attack_speed_level: float

    attack_damage_base: float
    attack_damage_level: float

    crit_chance: float

    resource_base: float
    resource_level: float
    
    resource_regen_base: float
    resource_regen_level: float

    attack_range_base: float

    move_speed_base: float

    # Derived attributes (not required in init)
    health_bonus: float
    health: float
    health_current: float
    health_missing: float

    health_regen_bonus: float
    health_regen: float

    heal_shield_power: float

    armor_bonus: float
    armor: float

    magic_resist_bonus: float
    magic_resist: float

    tenacity: float
    slow_resist: float

    attack_speed_bonus: float
    attack_speed: float

    attack_damage_bonus: float
    attack_damage: float

    ability_power: float

    crit_damage: float

    ar_red_flat: float
    ar_red_perc: float
    ar_pen_perc: float
    ar_pen_flat: float

    mr_red_flat: float
    mr_red_perc: float
    mr_pen_perc: float
    mr_pen_flat: float

    life_steal: float
    phys_vamp: float
    omni_vamp: float

    ability_haste_basic: float
    ability_haste_ultim: float
    ability_haste: float

    resource_bonus: float
    resource: float
    resource_current: float
    resource_missing: float

    resource_regen_bonus: float
    resource_regen: float

    attack_range_bonus: float
    attack_range: float

    move_speed_bonus_flat: float
    move_speed_bonus_perc: float
    move_speed_bonus_mult: float

@dataclass
class Champion:
    """Represents a League of Legends champion with stats and methods."""

    name: str
    level: int
    resource_type: str
    range_type: list[str]
    stats: ChampionStats

    @classmethod
    def from_json(cls, champ_name: str, champ_stats: Mapping[str, Any]) -> "Champion":
        """
        Creates a Champion instance from a JSON dictionary.

        TODO
        """
        stats = ChampionStats(
            **{key: get_stat(champ_stats, key, 0.0) for key in [
                "hp",
                "hpperlevel",
                "hpregen",
                "hpregenperlevel",
                "armor",
                "armorperlevel",
                "spellblock",
                "spellblockperlevel",
                "attackspeedratio",
                "attackspeed",
                "attackspeedperlevel",
                "attackdamage",
                "attackdamageperlevel",
                "crit",
                "mp",
                "mpperlevel",
                "mpregen",
                "mpregenperlevel",
                "attackrange",
                "movespeed",
            ]}
        )
        resource_type = champ_stats.get("partype", "")
        range_type = champ_stats.get("rangeidentity", [])
        
        return cls(name=champ_name, level=1, resource_type=resource_type, stats=stats)
    
    def as_dict(self) -> dict[str, Any]:
        """Returns the champion data as a dictionary."""
        return asdict(self)
    
    def take_damage(self, amount: float = 0.0) -> float:
        """
        Reduces current health when taking damage and returns the updated current health.
        """
        self.stats.health_current = max(self.stats.health_current - amount, 0.0)
        self.stats.health_missing = self.stats.health - self.stats.health_current
        return self.stats.health_current