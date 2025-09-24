import hashlib
import time
from typing import Any

from django.conf import settings
from django.core.cache import cache


class CacheVersion:
    """Manages cache versioning to handle cache invalidation.
    Usage:
        version = CacheVersion('products')
        version.increment()  # Invalidates all product cache
        version.get()  # Get current version
    """

    def __init__(self, namespace: str):
        self.namespace = namespace
        self._version_key = f"{settings.CACHE_KEY_PREFIX}:version:{namespace}"

    def get(self) -> str:
        """Get current version for namespace."""
        version = cache.get(self._version_key)
        if version is None:
            version = self._generate_version()
            cache.set(self._version_key, version)
        return version

    def increment(self) -> str:
        """Increment version to invalidate cache."""
        new_version = self._generate_version()
        cache.set(self._version_key, new_version)
        return new_version

    def _generate_version(self) -> str:
        """Generate a new version hash."""
        timestamp = str(time.time())
        return hashlib.md5(f"{self.namespace}:{timestamp}".encode()).hexdigest()[:8]


class VersionedCache:
    """Cache wrapper that includes versioning.
    Usage:
        cache = VersionedCache('products')
        cache.set('item:1', item_data)
        item = cache.get('item:1')
    """

    def __init__(self, namespace: str):
        self.namespace = namespace
        self.version = CacheVersion(namespace)

    def _versioned_key(self, key: str) -> str:
        """Generate versioned cache key."""
        version = self.version.get()
        return f"{settings.CACHE_KEY_PREFIX}:{self.namespace}:{version}:{key}"

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache with versioning."""
        return cache.get(self._versioned_key(key), default)

    def set(self, key: str, value: Any, timeout: int | None = None) -> bool:
        """Set value in cache with versioning."""
        return cache.set(self._versioned_key(key), value, timeout)

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        return cache.delete(self._versioned_key(key))

    def invalidate_all(self) -> None:
        """Invalidate all cache for this namespace."""
        self.version.increment()
