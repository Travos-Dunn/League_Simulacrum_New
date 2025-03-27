# constants.py

"""
Module containing constants and configuration variables.
"""

LINKS: dict[str, str] = {
    "realm_version": "https://ddragon.leagueoflegends.com/realms/na.json",
    "backup_versions": "https://ddragon.leagueoflegends.com/api/versions.json",
    
    "ddragon_items":   "https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/item.json",
    "cdragon_items":   "https://raw.communitydragon.org/{}/game/items.cdtb.bin.json", # version[:-2]
    
    "ddragon_champs":  "https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json",
    "ddragon_champ":   "https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion/{}.json", # champ_name
    "cdragon_champ":   "https://raw.communitydragon.org/{}/game/data/characters/{}/{}.bin.json", # version[:-2], champ_name.lower(), champ_name.lower()
}