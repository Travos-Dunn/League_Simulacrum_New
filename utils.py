# utils.py
import json
import logging
from typing import Any
from urllib.parse import urlparse

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_url(url: str) -> bool:
    """
    Validate that the URL is syntactically valid and returns a successful HTTP response.

    :param url: The URL to check.
    :type url: str

    :return: `True` if the URL is valid and returns a status code below `400`, otherwise `False`.
    :rtype: bool
    """
    parsed_url = urlparse(url)
    if not (parsed_url.scheme and parsed_url.netloc):
        return False
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        return response.status_code < 400
    except requests.RequestException:
        return False

def fetch_json(url: str, value: Any = None) -> dict[str, Any] | Any:
    """
    Fetch JSON data from a URL.
    
    :param url: The URL to fetch JSON data from.
    :type url: str

    :param value: A value to return if the `response` request is unsuccessful (defaults to `None`).
    :type value: Any, optional
    
    :return: JSON data if the `response` request is successful, otherwise `value`.
    :rtype: dict[str, Any] | Any
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.JSONDecodeError, ValueError):
        logging.error(f"Invalid JSON response from {url}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Fetching fetching {url}: {e}")
    
    return value

def read_json(filename: str, value: Any = None) -> dict[str, Any] | Any:
    """
    Read JSON data from a file.

    :param filename: The name of the file to read from.
    :type filename: str

    :param value: A value to return if unsuccessful (defaults to `None`).
    :type value: Any, optional

    :return: JSON data if the successful, otherwise `value`.
    :rtype: dict[str, Any] | Any
    """
    if not filename.endswith(".json"):
        filename += ".json"
    
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"File not found: {filename}")
    except json.JSONDecodeError:
        logging.error(f"Invalid JSON format in {filename}")
    
    return value

def write_json(filename: str, data: dict[str, Any]) -> bool:
    """
    Write JSON data to a file.
    
    :param filename: The name of the file to write to.
    :type filename: str

    :param data: JSON-compatible data to write.
    :type data: dict[str, Any]

    :return: `True` if the operation was succesful, otherwise `False`.
    :rtype: bool
    """
    if not filename.endswith(".json"):
        filename += ".json"
    
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            return True
    except (OSError, TypeError) as e:
        logging.error(f"Failed to write {filename}: {e}")
        return False

def update_json_key(filename: str, data: dict[str, Any]) -> bool:
    """
    Insert the specified key-value pair into JSON data.
    Replaces the current values with new values if the key exists, or inserts if the key does not exist.
    
    :param filename: The name of the file to write to.
    :type filename: str

    :param data: JSON-compatible data to write.
    :type data: dict[str, Any]

    :return: `True` if successful, otherwise `False`.
    :rtype: bool
    """
    json_data = read_json(filename)
    if json_data is None:
        logging.error(f"Empty data received from {filename}")
        return False

    for key, value in data.items():
        json_data[key] = value
    
    return write_json(filename, json_data)

def update_json_value(filename: str, data: dict[str, Any]) -> bool:
    """
    Insert the specified key-value pair into JSON data.
    Updates the current values with new values if the key exists, or inserts if the key does not exist.

    :param filename: The name of the file to write to.
    :type filename: str

    :param data: JSON-compatible data to write.
    :type data: dict[str, Any]

    :return: `True` if successful, otherwise `False`.
    :rtype: bool
    """
    json_data = read_json(filename)
    if json_data is None:
        logging.error(f"Empty data received from {filename}")
        return False
    
    for key, value in data.items():
        json_data[key] = {**json_data[key], **value}
    
    return write_json(filename, json_data)