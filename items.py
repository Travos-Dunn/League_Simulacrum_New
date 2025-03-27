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
        logging.warning(f"Failed to fetch data for all items from Data Dragon, version {version}")
        return value

def clean_ddragon_items(ddragon: dict[str, Any]) -> dict[str, Any]:
    """
    Filter data for all items from Data Dragon.

    :param ddragon: Data Dragon item data.
    :type ddragon: dict[str, Any]

    :return: Filtered Dragon Dragon item data.
    :rtype: dict[str, Any]
    """
    if not ddragon or not isinstance(ddragon.get("data"), dict):
        logging.warning("Invalid item data received")
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
        logging.warning(f"Failed to fetch data for all items from Community Dragon, version {version}")
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
        logging.warning("Invalid item data received.")
        return {}

    filtered_data = {}
    for item_id, subdata in cdragon.items():
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

def create_item_list(item_data: dict[str, Any]) -> dict[str, Any]:
    """
    Create an item list for debugging purposes.
    """
    if not isinstance(item_data, dict):
        logging.warning(f"Invalid or empty item data received: item_data = {type(item_data).__name__}")
        return {}
    
    return {
        item_id: subdata.get("name", "")
        for item_id, subdata in item_data.items()
    }