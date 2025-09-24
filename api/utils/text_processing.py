"""Text processing and data manipulation utilities."""

from typing import Any


def chunks(lst: list[Any], chunk_size: int) -> list[list[Any]]:
    """Yield successive chunks from a list.

    Args:
        lst: List to chunk
        chunk_size: Size of each chunk

    Yields:
        Chunks of the original list
    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def deep_merge_dicts(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries.

    Args:
        dict1: First dictionary
        dict2: Second dictionary (takes precedence)

    Returns:
        Merged dictionary
    """
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def flatten_list(nested_list: list[Any]) -> list[Any]:
    """Flatten a nested list.

    Args:
        nested_list: List that may contain nested lists

    Returns:
        Flattened list
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def remove_duplicates_preserve_order(seq: list[Any]) -> list[Any]:
    """Remove duplicates from list while preserving order.

    Args:
        seq: List with potential duplicates

    Returns:
        List with duplicates removed, order preserved
    """
    seen = set()
    result = []
    for item in seq:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def group_by_key(items: list[dict], key: str) -> dict[Any, list[dict]]:
    """Group list of dictionaries by a specific key.

    Args:
        items: List of dictionaries
        key: Key to group by

    Returns:
        Dictionary with grouped items
    """
    groups = {}
    for item in items:
        group_key = item.get(key)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)
    return groups


def extract_numbers(text: str) -> list[int]:
    """Extract all numbers from a text string.

    Args:
        text: Input text

    Returns:
        List of numbers found in the text
    """
    import re

    return [int(match) for match in re.findall(r"\d+", text)]


def word_count(text: str) -> int:
    """Count words in text.

    Args:
        text: Input text

    Returns:
        Number of words
    """
    return len(text.split()) if text else 0
