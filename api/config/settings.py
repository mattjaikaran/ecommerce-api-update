"""Runtime configuration settings.

This module contains settings that may be configured at runtime
or through environment variables.
"""

import os
from typing import Any

from django.conf import settings


def get_setting(name: str, default: Any = None) -> Any:
    """Get a setting value with fallback to default.

    Args:
        name: Setting name
        default: Default value if setting not found

    Returns:
        Setting value or default
    """
    return getattr(settings, name, default)


def get_env_setting(name: str, default: Any = None) -> Any:
    """Get a setting from environment variables.

    Args:
        name: Environment variable name
        default: Default value if not found

    Returns:
        Environment variable value or default
    """
    return os.environ.get(name, default)


# Dynamic settings that can be overridden
class DynamicSettings:
    """Dynamic settings class for runtime configuration."""

    @property
    def debug_mode(self) -> bool:
        """Check if debug mode is enabled."""
        return get_setting("DEBUG", False)

    @property
    def maintenance_mode(self) -> bool:
        """Check if maintenance mode is enabled."""
        return get_env_setting("MAINTENANCE_MODE", "false").lower() == "true"

    @property
    def feature_flags(self) -> dict[str, bool]:
        """Get feature flags configuration."""
        from .constants import FEATURES

        return FEATURES

    @property
    def max_upload_size(self) -> int:
        """Get maximum upload size in bytes."""
        return int(get_env_setting("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))

    @property
    def rate_limit_enabled(self) -> bool:
        """Check if rate limiting is enabled."""
        return get_env_setting("RATE_LIMIT_ENABLED", "true").lower() == "true"

    @property
    def cache_enabled(self) -> bool:
        """Check if caching is enabled."""
        return get_env_setting("CACHE_ENABLED", "true").lower() == "true"

    @property
    def analytics_enabled(self) -> bool:
        """Check if analytics tracking is enabled."""
        return get_env_setting("ANALYTICS_ENABLED", "true").lower() == "true"

    @property
    def email_backend_enabled(self) -> bool:
        """Check if email backend is enabled."""
        return get_env_setting("EMAIL_ENABLED", "true").lower() == "true"

    @property
    def celery_enabled(self) -> bool:
        """Check if Celery task queue is enabled."""
        return get_env_setting("CELERY_ENABLED", "true").lower() == "true"


# Global instance
dynamic_settings = DynamicSettings()
