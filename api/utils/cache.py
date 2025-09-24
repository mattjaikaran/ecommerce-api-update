"""Cache utilities for the ecommerce API."""

from typing import Any

from django.core.cache import cache

from ..config.constants import CACHE_TIMEOUT_MEDIUM


def cache_key_builder(*args: str) -> str:
    """Build a cache key from multiple arguments.

    Args:
        *args: Arguments to join into a cache key

    Returns:
        A cache key string
    """
    return ":".join(str(arg) for arg in args)


def get_cached_data(key: str, default: Any = None) -> Any:
    """Get data from cache with optional default.

    Args:
        key: Cache key to retrieve
        default: Default value if key not found

    Returns:
        Cached data or default value
    """
    return cache.get(key, default)


def set_cached_data(key: str, value: Any, timeout: int = CACHE_TIMEOUT_MEDIUM) -> None:
    """Set data in cache with timeout.

    Args:
        key: Cache key to set
        value: Value to cache
        timeout: Timeout in seconds
    """
    cache.set(key, value, timeout)


def invalidate_cache_pattern(pattern: str) -> None:
    """Invalidate cache keys matching a pattern.

    Args:
        pattern: Pattern to match cache keys for deletion

    Note:
        This would need to be implemented based on your cache backend.
        For Redis, you could use cache.delete_pattern()
    """
    # Implementation would depend on cache backend
    # For Redis: cache.delete_pattern(pattern)
    # For now, this is a placeholder


def delete_cache_key(key: str) -> None:
    """Delete a specific cache key.

    Args:
        key: Cache key to delete
    """
    cache.delete(key)


def clear_all_cache() -> None:
    """Clear all cached data."""
    cache.clear()


def get_or_set_cache(
    key: str, callable_func, timeout: int = CACHE_TIMEOUT_MEDIUM
) -> Any:
    """Get from cache or set if not exists.

    Args:
        key: Cache key
        callable_func: Function to call if cache miss
        timeout: Cache timeout in seconds

    Returns:
        Cached or newly computed value
    """
    value = cache.get(key)
    if value is None:
        value = callable_func()
        cache.set(key, value, timeout)
    return value
