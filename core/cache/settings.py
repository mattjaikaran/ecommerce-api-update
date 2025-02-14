from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def cache_key_prefix(key: str) -> str:
    """Generate a cache key with the appropriate prefix."""
    return f"{settings.CACHE_KEY_PREFIX}:{key}"

def get_cached_data(key: str, default=None):
    """Get data from cache with proper key prefix."""
    return cache.get(cache_key_prefix(key), default)

def set_cached_data(key: str, value, timeout=CACHE_TTL):
    """Set data in cache with proper key prefix."""
    return cache.set(cache_key_prefix(key), value, timeout)

def delete_cached_data(key: str):
    """Delete data from cache with proper key prefix."""
    return cache.delete(cache_key_prefix(key))

def clear_cache_pattern(pattern: str):
    """Clear all cache keys matching a pattern."""
    keys = cache.keys(f"{settings.CACHE_KEY_PREFIX}:{pattern}")
    return cache.delete_many(keys)
