# constants.py
"""
Module containing constants and configuration variables.
"""

LINKS: dict[str, str] = {
    "realm_version": "https://ddragon.leagueoflegends.com/realms/na.json",
    "backup_versions": "https://ddragon.leagueoflegends.com/api/versions.json",
    
    "ddragon_items":   "https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json", # version
    "cdragon_items":   "https://raw.communitydragon.org/{}/game/items.cdtb.bin.json", # version[:-2]
    
    "ddragon_champs":  "https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json", # version
    "ddragon_champ":   "https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json", # version, champ_name
    "cdragon_champ":   "https://raw.communitydragon.org/{}/game/data/characters/{}/{}.bin.json", # version[:-2], champ_name.lower(), champ_name.lower()
}

FILES: dict[str, str] = {
    "item_data": "{}_Item_Data.json",
    "item_list": "{}_Item_List.json",
    "champ_data": "{}_Champ_Data.json",
    "champ_list": "{}_Champ_list.json"
}

# Mapping for filtering or renaming item stats (with special cases noted)
STAT_MAP: dict[str, str] = {
    "MoveSpeed": "mFlatMovementSpeedMod",
    "BaseManaRegen": "percentBaseMPRegenMod",
    "BaseHealthRegen": "mPercentBaseHPRegenMod",
    "Health": "mFlatHPPoolMod",
    "CritChance": "mFlatCritChanceMod",
    "AbilityPower": "mFlatMagicDamageMod",
    "Mana": "flatMPPoolMod",
    "Armor": "mFlatArmorMod",
    "MagicResist": "mFlatSpellBlockMod",
    "AttackDamage": "mFlatPhysicalDamageMod",
    "AttackSpeed": "mPercentAttackSpeedMod",
    "LifeSteal": "mPercentLifeStealMod",
    "AbilityHaste": "mAbilityHasteMod",
    "Lethality": "PhysicalLethality",
    "MoveSpeedPercent": "mPercentMovementSpeedMod",
    "HealShieldPower": "mPercentHealingAmountMod",
    "MagicPen": "mFlatMagicPenetrationMod",
    "CritDamageFlat": "mFlatCritDamageMod",
    "ArmorPenPercent": "mPercentArmorPenetrationMod",
    "Tenacity": "mPercentTenacityItemMod",
    "MagicPenPercent": "mPercentMagicPenetrationMod",
    "Omnivamp": "PercentOmnivampMod",

    # Special cases
    "mFlatHPRegenMod": "mFlatHPRegenMod",
    "mPercentSlowResistMod": "mPercentSlowResistMod",
    "mFlatMovementSpeedMod": "mFlatMovementSpeedMod"
}

# Set for filtering community dragon items
SAVE_KEYS: set[str] = {
    "mEffectByLevelAmount",
    "mItemCalculations",
    "mEffectAmount",
    "mDataValues",
    "mItemDataClient"
}

# Set for filtering community dragon items
REMOVE_KEYS: set[str] = {
    "requiredItemLinks",
    "ShopOrderPriority",
    "mRequiredPurchaseIdentities",
    "mHiddenFromOpponents",
    "mCooldownShowDisabledDuration",
    "mItemModifiers",
    "mBuildDepth",
    "mRequiredBuffCurrencyCost",
    "sidegradeItemLinks",
    "mRequiredSpellName",
    "mDisabledDescriptionOverride",
    "consumeOnAcquire",
    "specialRecipe",
    "RecommendationTags",
    "StringCalculations",
    "mRequiredLevel",
    "mItemDataBuild",
    "mRequiredChampion",
    "RestrictedBuffName",
    "LastMajorChangeMajorPatchVersion",
    "LastMajorChangeMinorPatchVersion",
    "usableInStore",
    "itemVOGroup",
    "mItemCalloutPlayer",
    "mRequiredBuffCurrencyName",
    "consumed",
    "mScripts",
    "DataValuesModeOverride",
    "ShowCooldownInPings",
    "mDeathRecapName",
    "sellBackModifier",
    "ShowCooldownVfxToAllies",
    "clickable",
    "spellName",
    "mItemAdviceAttributes",
    "mItemCalloutSpectator",
    "mVFXResourceResolver",
    "recipeItemLinks",
    "price",
    "mItemDataAvailability",
    "mCanBeSold",
    "epicness",
    "mItemAttributes",
    "maxStack",
    "mDisplayName",
    "itemID",
    "mItemGroups",
    "__type",
    "mCategories"
}
