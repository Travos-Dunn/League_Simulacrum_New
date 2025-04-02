from typing import Any
import utils
import logging
from constants import LINKS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_ddragon_champs(version: str, value: Any = None) -> dict[str, Any]:
    """
    TODO
    """
    url = LINKS["ddragon_champs"].format(version)
    champ_data = utils.fetch_json(url)

    if not champ_data or champ_data.get("version") != version or "data" not in champ_data:
        logging.warning(f"Failed to fetch Data Dragon champion data (version {version}).")
        return value

    return champ_data

def clean_ddragon_champs(ddragon: dict[str, Any]) -> dict[str, Any]:
    """
    TODO
    """
    if not ddragon or "data" not in ddragon:
        logging.warning(f"Invalid or empty Data Dragon data received.")
        return {}
    
    ddragon = ddragon.get("data", {})
    if not isinstance(ddragon, dict):
        logging.warning("Unexpected format in champion data.")
        return {}
    
    return {
        name: {
            "key": subdata.get("key", ""),
            "name": subdata.get("name", ""),
            "partype": subdata.get("partype", ""),
            "stats": subdata.get("stats", {})
        }
        for name, subdata in ddragon.items()
    }

def fetch_ddragon_champ(version: str, champ_name: str, value: Any = None) -> dict[str, Any]:
    """
    TODO
    """
    url = LINKS["ddragon_champ"].format(version, champ_name)
    champ_data = utils.fetch_json(url)

    if not champ_data or champ_data.get("version") != version or "data" not in champ_data:
        logging.warning(f"Failed to fetch Data Dragon data for {champ_name} (version {version}).")
        return value
    
    return champ_data

def clean_ddragon_champ(ddragon: dict[str, Any]) -> dict[str, Any]:
    """
    TODO
    """
    if not ddragon or "data" not in ddragon:
        logging.warning("Invalid or empty Data Dragon data received.")
        return {}
    
    ddragon = ddragon.get("data", {})
    if not isinstance(ddragon, dict):
        logging.warning("Unexpected format in champion data.")
        return {}
    
    champ_info = next(iter(ddragon.values()), {})
    spells = {
        spell["id"]: {key: value for key, value in spell.items() if key != "id"}
        for spell in champ_info.get("spells", [])
    }
    spells["passive"] = champ_info.get("passive", {})

    return spells

def fetch_cdragon_champ(version: str, champ_name: str, value: Any = None) -> dict[str, Any]:
    """
    TODO
    """
    url = LINKS["cdragon_champ"].format(version[:-2], champ_name.lower(), champ_name.lower())
    champ_data = utils.fetch_json(url)

    if not champ_data:
        logging.warning(f"Failed to fetch Community Dragon data for {champ_name} (version {version}).")
        return value

    return champ_data

def clean_cdragon_champ(cdragon: dict[str, Any], champ_name: str) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """
    TODO
    """
    if not cdragon or not isinstance(cdragon, dict):
        logging.warning("Invalid or empty Community Dragon data received.")
        return {}, {}
    
    records = cdragon.get(f"Characters/{champ_name}/CharacterRecords/Root", {})
    records_stats = {
        "rangeidentity": records.get("purchaseIdentities", []),
        "attackspeedratio": records.get("attackSpeedRatio", 0)
    }
    records_spells = {
        "spellNames": records.get("spellNames", []),
        "mAbilities": records.get("mAbilities", [])
    }

    spells = {
        spell_name.split("Spells/")[1]: subdata
        for spell_name, subdata in cdragon.items()
        if spell_name.startswith(f"Characters/{champ_name}/Spells/")
    }

    return records_stats, records_spells, spells

def merge_champs(version: str, ddragon: dict[str, Any]) -> dict[str, Any]:
    """
    TODO
    """
    if not isinstance(ddragon, dict):
        logging.warning("Invalid or empty Data Dragon data received.")
        return {}
    
    champ_data = {}
    for ddragon_id, ddragon_subdata in ddragon.items():
        ddragon_champ = fetch_ddragon_champ(version, ddragon_id, {})
        ddragon_spells = clean_ddragon_champ(ddragon_champ)

        cdragon_champ = fetch_cdragon_champ(version, ddragon_id, {})
        cdragon_records_stats, cdragon_records_spells, cdragon_spells = clean_cdragon_champ(cdragon_champ, ddragon_id)

        ddragon_subdata["rangeidentity"] = cdragon_records_stats.get("rangeidentity", [])
        ddragon_subdata["stats"]["attackspeedratio"] = cdragon_records_stats.get("attackspeedratio", 0)

        champ_data[ddragon_id] = {
            "records_ddragon": ddragon_subdata,
            "spells_ddragon": ddragon_spells,
            "records_cdragon": cdragon_records_spells,
            "spells_cdragon": cdragon_spells
        }
        logging.info(f"Complete merging data for: {ddragon_id}")
    
    return champ_data
    
def check_champs(filename: str, version: str, update: bool = False) -> dict[str, Any]:
    """
    TODO
    """
    champ_data = utils.read_json(filename, {})

    if not champ_data or update:
        logging.error(f"Fetching champ data for version {version}")
        ddragon = fetch_ddragon_champs(version, {})
        ddragon = clean_ddragon_champs(ddragon)

        champ_data = merge_champs(version, ddragon)
        utils.write_json(filename, champ_data)
    
    return champ_data

def check_champ_list(filename_list: str, filename_data: str, version: str, update: bool = False) -> dict[str, Any]:
    """
    TODO
    """
    champ_list = utils.read_json(filename_list, {})

    if not champ_list or update:
        logging.info(f"Fetching champ list (version {version}).")
        champ_list = utils.read_json(filename_data, {})
        champ_list = {
            champ_id: subdata.get("records_ddragon", {}).get("name", "")
            for champ_id, subdata in champ_list.items()
        }
        if not champ_list:
            logging.warning(f"Invalid or empty data received from {filename_data}.")
            return {}
        utils.write_json(filename_list, champ_list)
    
    return champ_list