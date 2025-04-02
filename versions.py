# versions.py
import logging
import utils
from constants import LINKS, FILES

"""
This modules provides utility functions for data processing.

Functions:
"""

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def update_filenames(version: str) -> dict[str, str]:
    """
    Generatesa a dictionar with filenames updated for the given version.

    :param version: The game version.
    :type version: str

    :return: A new dictionary with update filenames.
    :rtype: dict[str, str]
    """
    return {file_type: file_name.format(version) for file_type, file_name in FILES.items()}

def fetch_version() -> str | None:
    """
    Fetch the latest game version for North America from the Data Dragon API.

    :return: The latest game version if successful, otherwise `None`.
    :rtype: str | None
    """
    url = LINKS["realm_version"]

    try:
        response = utils.fetch_json(url, {})
        return response.get("v")
    except Exception as e:
        logging.error(f"Error fetching version from {url}: {e}")
        return None

def fetch_versions() -> list[str] | None:
    """
    Fetch a list of available versions from the Data Dragon API.

    :return: A list of available game versions if successful, otherwise `None`.
    :rtype: list[str] | None
    """
    url = LINKS["backup_versions"]

    try:
        response = utils.fetch_json(url, [])
        return response
    except Exception as e:
        logging.error(f"Error fetching versions from {url}: {e}")
        return None

def validate_version_urls(version: str) -> bool:
    """
    Checks whether all necessary URLs are valid for a given game version.

    :param version: The game version.
    :type version: str

    :return: `True` if all URLs are valid, otherwise `False`.
    :rtype: bool
    """
    champ_name = "Aatrox"

    urls = [
        LINKS["ddragon_items"].format(version),
        LINKS["cdragon_items"].format(version[:-2]),
        LINKS["ddragon_champs"].format(version),
        LINKS["ddragon_champ"].format(version, champ_name),
        LINKS["cdragon_champ"].format(version[:-2], champ_name.lower(), champ_name.lower()),
    ]

    return all(utils.check_url(url) for url in urls)

def check_version() -> str | None:
    """
    Find the latest available game version for all data types.

    :return: The latest available game version if successful, otherwise `None`.
    :rtype: str | None
    """
    latest_version = fetch_version()
    
    if validate_version_urls(latest_version):
        return latest_version
    
    logging.info(f"Latest game version {latest_version} not available for all data, rolling back now.")

    version_list = fetch_versions()
    for version in version_list:
        if version == latest_version:
            continue

        if validate_version_urls(version):
            return version
        
        logging.info(f"Game version {version} not available for all data, checking previous now.")

    return None # No valid version found
