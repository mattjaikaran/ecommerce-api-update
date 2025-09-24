"""API configuration module.

This module contains configuration constants and settings for the ecommerce API.
"""

from .constants import *
from .error_messages import ERROR_MESSAGES, SUCCESS_MESSAGES
from .settings import *

__all__ = [
    # Constants
    "API_VERSION",
    "API_PREFIX",
    "DEFAULT_PAGE_SIZE",
    "MAX_PAGE_SIZE",
    "CACHE_KEY_PREFIX",
    "CACHE_TIMEOUT_SHORT",
    "CACHE_TIMEOUT_MEDIUM",
    "CACHE_TIMEOUT_LONG",
    "CACHE_TIMEOUT_DAY",
    "REDIS_KEYS",
    "MAX_UPLOAD_SIZE",
    "ALLOWED_IMAGE_EXTENSIONS",
    "ALLOWED_DOCUMENT_EXTENSIONS",
    "EMAIL_TEMPLATES",
    "ORDER_STATUS_CHOICES",
    "PAYMENT_STATUS_CHOICES",
    "FULFILLMENT_STATUS_CHOICES",
    "DEFAULT_CURRENCY",
    "SUPPORTED_CURRENCIES",
    "DEFAULT_TAX_RATE",
    "TAX_EXEMPT_STATES",
    "FREE_SHIPPING_THRESHOLD",
    "DEFAULT_SHIPPING_COST",
    "EXPRESS_SHIPPING_COST",
    # Error and success messages
    "ERROR_MESSAGES",
    "SUCCESS_MESSAGES",
]
