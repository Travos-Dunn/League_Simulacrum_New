# versions.py
import logging
import utils
from constants import LINKS

"""
This modules provides utility functions for data processing.

Functions:
"""

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

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