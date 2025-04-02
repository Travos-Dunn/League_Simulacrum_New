from math import prod
from typing import Any

# FIXME
def max_value(values):
    """Maximum value"""
    return max(values) if hasattr(values, '__iter__') else values

# FIXME
def min_value(values):
    """Minimum value"""
    return min(values) if hasattr(values, '__iter__') else values

# FIXME
def add_stacking(values):
    """Additive stacking"""
    return sum(values) if hasattr(values, '__iter__') else values

# FIXME
def multi_stacking(values):
    """Multiplicative stacking"""
    return prod(1 + value for value in values) if hasattr(values, '__iter__') else 1 + values



# FIXME
def effective_health(health, resist) -> float:
    """
    Effective Health
    
    TODO: Include formula in docs
    """
    health = add_stacking(health)
    resist = add_stacking(resist)
    result = (0.01 * resist + 1) * health
    return max_value(result, 0)

# FIXME
def stat_growth(base, growth, level) -> float:
    """
    Champion stat value at the specified level
    """
    return base + growth * ((level - 1) * (0.7025 + (0.0175 * (level - 1))))

# FIXME
def attack_speed(base, growth, level, ratio, bonus) -> float:
    """
    Champion attack speed at the specified level
    """
    bonus = add_stacking(bonus)
    bonus = bonus + growth * (level - 1) * (0.7025 + 0.0175 * (level - 1))
    return min_value(base + bonus * ratio, 3)

# FIXME
def move_speed(base, flat, percent, multi, slow, slow_res) -> float:
    """
    Champion movement speed at the specified level
    """
    flat = add_stacking(flat)
    percent = add_stacking(percent)
    multi = multi_stacking(multi)
    slow = max_value(slow)
    slow_res = multi_stacking(slow_res)

    ms = (base + flat) * (1 + percent) * multi * (1 - (slow * (1 - slow_res)))
    return (
        ms if ms <= 415
        else (ms * 0.8 + 83) if ms <= 490
        else (ms * 0.5 + 230)
    )

# FIXME
def damage_dealt_modifier(mods) -> float:
    """
    Champion damage dealt modifier
    NOTE: might not work with values less than 1 (e.g. 90% -> .9)
    """
    return add_stacking(mods)

# FIXME
def damage_received_modifier(mods) -> float:
    """
    Champion damage received modifier
    NOTE: might not work with all values
    """
    return multi_stacking(mods)

# FIXME
def damage_reduction_resistances(resist) -> float:
    """
    Champion damage reduction modifier from a resistance type.
    """
    return 1 - 100 / (100 + resist) if resist > 0 else 2 - (100 / (100 + resist))

# FIXME
def resistance_post_pen(base, bonus, flat_red, perc_red, perc_pen, flat_pen) -> tuple[float, float, float]:
    """
    Champion resistance after reduction and penetration are applied
    """
    base = add_stacking(base)
    bonus = add_stacking(bonus)
    flat_red = add_stacking(flat_red)
    perc_red = 1 - multi_stacking(perc_red) - 1
    perc_pen = 1 - multi_stacking(perc_pen) - 1
    flat_pen = add_stacking(flat_pen)

    base_ratio = base / (base + bonus)
    bonus_ratio = bonus / (base + bonus)

    base -= (flat_red * base_ratio)
    bonus -= (flat_red * bonus_ratio)
    total = base + bonus
    if total > 0:
        base *= perc_red * perc_pen
        bonus *= bonus * perc_red * perc_pen
        total = max_value(base + bonus - flat_pen, 0)
    
    return base, bonus, total

# FIXME
def tenacity(group_1, group_2, group_3) -> float:
    """
    Champion tenacity
    """
    # Group 1
    # Elixir of Iron, Runes, Chemtech Dragon, Mercury Treads, Sterak's Gage, Wit's End

    # Group 2
    # Cleanse, Milio's Breath of Life (R)

    # Group 3
    # Garen's Courage (W), Ornn Brittle (P)
    
    # group_1 = [
    #     item_stats.get("mPercentTenacityItemMod", 0)
    #     for item_stats in item_data.values()
    # ]
    group_2 = [
        0.75 if "cleanse" else 0,
        0.65 if "milio" else 0
    ]
    group_3 = [
        0.6 if "garen" else 0,
        -0.3 if "ornn" else 0
    ]
    
    

# FIXME
def post_mitigation_damage():
    """
    Post-mitigation damage
    """
    # The following effects influence damage as non-zero values, in no particular order of calculation.
    # percent damage amplification
    # percent damage reduction
    # flat damage reduction
    # resistances
    # resistance reduction
    # resistance penetration
    # shielding

# FIXME
def avg_damage_per_attack(attack_damage, crit_chance, crit_mod) -> float:
    """
    Average damage per attack
    """
    return attack_damage + (attack_damage * crit_chance * ((crit_mod - 1)))