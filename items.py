# items.py
import logging
from typing import Any
import utils
from constants import LINKS, REMOVE_KEYS, SAVE_KEYS, STAT_MAP

def fetch_ddragon_items(version: str, value: Any = None) -> dict[str, Any]:
    """
    Fetch data for all items from Data Dragon.
    
    :param version: The game version.
    :type version: str

    :param value: A value to return if unsuccessful (defaults to `None`).
    :type value: Any, optional

    :return: Data Dragon item data if successful, otherwise `value`.
    :rtype:
    """
    url = LINKS["ddragon_items"].format(version)
    item_data = utils.fetch_json(url, {})

    if not item_data or item_data.get("version") != version or "data" not in item_data:
        logging.warning(f"Failed to fetch data for all items from Data Dragon (v{version}).")
        return value
    
    return item_data

def clean_ddragon_items(ddragon: dict[str, Any]) -> dict[str, Any]:
    """
    Filter data for all items from Data Dragon.

    :param ddragon: Data Dragon item data.
    :type ddragon: dict[str, Any]

    :return: Filtered Dragon Dragon item data.
    :rtype: dict[str, Any]
    """
    if not ddragon or not isinstance(ddragon.get("data"), dict):
        logging.warning("Invalid item data received from `fetch_ddragon_items`.")
        return {}
    
    ddragon = ddragon["data"]

    filtered_data = {}
    for item_id, subdata in ddragon.items():
        if not isinstance(subdata, dict) or int(item_id) > 10000:
            continue

        # Extract relevant fields
        tags = subdata.get("tags", [])
        maps = subdata.get("maps", {})
        required_champion = subdata.get("requiredChampion", False)

        # Early exits based on conditions
        if not tags or not maps.get("11", False) or required_champion:
            continue

        # Retrieve additional information only if needed
        into = subdata.get("into")
        in_store = subdata.get("inStore", False)
        special_recipe = subdata.get("specialRecipe")
        gold = subdata.get("gold", {})
        purchasable = gold.get("purchasable", False)

        # Continue only if required attributes are present
        if not (into or in_store or special_recipe or purchasable):
            continue

        stacks = subdata.get("stacks", 0)

        # Continue if certain tags or stacks are present
        if "Jungle" in tags or "Trinket" in tags or stacks > 0:
            continue

        # Add to filtered data if all conditions are met!
        filtered_data[item_id] = {
            "name": subdata.get("name", ""),
            "description": subdata.get("description", ""),
            "gold": gold.get("total", -1),
            "tags": tags
        }

    return filtered_data

def fetch_cdragon_items(version: str, value: Any = None) -> dict[str, Any]:
    """
    Fetch data for all items from Community Dragon.

    :param version: The game version.
    :type version: str

    :param value: A value to return if unsuccessful (defaults to `None`).
    :type value: Any

    :return: Community Dragon item data if successful, otherwise `value`.
    :rtype: dict[str, Any]
    """
    url = LINKS["cdragon_items"].format(version[:-2])
    item_data = utils.fetch_json(url, {})

    if not item_data:
        logging.warning(f"Failed to fetch data for all items from Community Dragon (v{version}).")
        return value
    
    return item_data

def clean_cdragon_items(cdragon: dict[str, Any]) -> dict[str, Any]:
    """
    Filter data for all items from Community Dragon.

    :param cdragon: Community Dragon item data.
    :type cdragon: dict[str, Any]

    :return: Filtered Community Dragon item data.
    :rtype: dict[str, Any]
    """
    if not cdragon:
        logging.warning("Invalid item data received from `fetch_cdragon_items`.")
        return {}

    filtered_data = {}
    for item_id, subdata in cdragon.items():
        if not isinstance(subdata, dict):
            continue
        
        base_keys = set(subdata.keys()).intersection(SAVE_KEYS)
        filtered_keys = set(subdata.keys()).difference(REMOVE_KEYS)
        stat_keys = filtered_keys.difference(SAVE_KEYS)

        structured_item = {key: subdata[key] for key in base_keys}
        structured_item["stats"] = {key: subdata[key] for key in stat_keys}

        tooltip = subdata.get("mItemDataClient", {}).get("mTooltipData", {})
        stats = tooltip.get("mLists", {}).get("Stats", {}).get("elements")

        if isinstance(stats, list):
            stat_types = {stat["type"] for stat in stats if isinstance(stat, dict) and "type" in stat}
            filtered_stats = stat_types.intersection(set(STAT_MAP.keys()) - {"GoldPer10"})

            structured_item["stats"].update({
                STAT_MAP[stat]: subdata.get(STAT_MAP[stat])
                for stat in filtered_stats
            })
        
        structured_item.pop("mItemDataClient", None)

        if isinstance(structured_item.get("mEffectAmount"), list) and all(val == 0 for val in structured_item["mEffectAmount"]):
            structured_item.pop("mEffectAmount", None)
        
        mDataValues = structured_item.get("mDataValues")
        if mDataValues and isinstance(mDataValues, list):
            structured_item["mDataValues"] = {
                entry.get("mName"): entry.get("mValue")
                for entry in structured_item.get("mDataValues", [])
            }
        
        filtered_data[item_id] = structured_item
    
    return filtered_data

def merge_items(ddragon: dict[str, Any], cdragon: dict[str, Any]) -> dict[str, Any]:
    """
    Combine Data Dragon and Community Dragon item data.

    :param ddragon: Data Dragon item data.
    :type ddragon: dict[str, Any]

    :param cdragon: Community Dragon item data.
    :type cdragon: dict[str, Any]

    :return: Combined item data from Data Dragon and Community Dragon.
    :rtype: dict[str, Any]
    """
    if not all(isinstance(var, dict) for var in (ddragon, cdragon)):
        culprit = {name: value for name, value in locals().items() if not isinstance(value, dict)}
        logging.warning(f"Invalid or empty item data received: {', '.join(f'{key} = {type(value).__name__}' for key, value in culprit.items())}")
        return {}

    item_data = {}
    for ddragon_id, ddragon_subdata in ddragon.items():
        cdragon_subdata = cdragon.get(f"Items/{ddragon_id}", {})
        if not cdragon_subdata:
            logging.warning(f"Failed to find item: {ddragon_id}, {ddragon_subdata.get('name', '')}")
            continue
        
        item_data[ddragon_id] = {**ddragon_subdata, **cdragon_subdata}
    
    return item_data

def check_items(filename: str, version: str, update: bool = False) -> dict[str, Any]:
    """
    Check if the item data file is correct, and update if not.

    :param filename: The item data file to read.
    :type filename: str

    :param version: The game version.
    :type version: str

    :param update: Debug flag to force update item data (defaults to `False`).
    :type update: bool

    :return: Combined item data from Data Dragon and Community Dragon.
    :rtype: dict[str, Any]
    """
    item_data = utils.read_json(filename, {})

    if not item_data or update:
        logging.info(f"Fetching item data (version {version}).")
        ddragon = fetch_ddragon_items(version, {})
        ddragon = clean_ddragon_items(ddragon)

        cdragon = fetch_cdragon_items(version, {})
        cdragon = clean_cdragon_items(cdragon)
        
        item_data = merge_items(ddragon, cdragon)
        utils.write_json(filename, item_data)
    
    return item_data

def check_item_list(filename_list: str, filename_data: str, version: str, update: bool = False) -> dict[str, Any]:
    """
    Check if the item list file is correct, and update if not.

    :param filename_list: The item list file to read.
    :type filename: str

    :param filename_data: The item data file to read if the item list file is invalid.
    :type filename_data: str

    :version: The game version.
    :type version: str

    :param update: Debug flag to force update item list (defaults to `False`).
    :type update: bool

    :return: Item list.
    :rtype: dict[str, Any]
    """
    item_list = utils.read_json(filename_list, {})

    if not item_list or update:
        logging.info(f"Fetching item list (version {version}).")
        item_list = utils.read_json(filename_data, {})
        item_list = {
            item_id: subdata.get("name", "")
            for item_id, subdata in item_list.items()
        }
        if not item_list:
            logging.warning(f"Invalid or empty data received from {filename_data}.")
            return {}
        utils.write_json(filename_list, item_list)
    
    return item_list
