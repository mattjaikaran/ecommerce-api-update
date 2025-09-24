"""API utilities module.

This module provides common utility functions and helpers used across the ecommerce API.
"""

from .cache import (
    cache_key_builder,
    get_cached_data,
    invalidate_cache_pattern,
    set_cached_data,
)
from .currency import format_currency
from .email import send_email_template
from .file_utils import get_file_url, sanitize_filename, upload_file_to_storage
from .formatting import create_slug, truncate_text
from .generators import generate_order_number, generate_secure_hash, generate_unique_id
from .http import get_client_ip, is_ajax
from .math_utils import (
    calculate_discount_amount,
    calculate_shipping_cost,
    calculate_tax_amount,
    safe_divide,
)
from .pagination import paginate_queryset
from .text_processing import chunks, deep_merge_dicts
from .validation import convert_to_bool, validate_phone_number

__all__ = [
    # Cache utilities
    "cache_key_builder",
    "get_cached_data",
    "invalidate_cache_pattern",
    "set_cached_data",
    # Currency utilities
    "format_currency",
    # Email utilities
    "send_email_template",
    # File utilities
    "get_file_url",
    "sanitize_filename",
    "upload_file_to_storage",
    # Formatting utilities
    "create_slug",
    "truncate_text",
    # Generator utilities
    "generate_order_number",
    "generate_secure_hash",
    "generate_unique_id",
    # HTTP utilities
    "get_client_ip",
    "is_ajax",
    # Math utilities
    "calculate_discount_amount",
    "calculate_shipping_cost",
    "calculate_tax_amount",
    "safe_divide",
    # Pagination utilities
    "paginate_queryset",
    # Text processing utilities
    "chunks",
    "deep_merge_dicts",
    # Validation utilities
    "convert_to_bool",
    "validate_phone_number",
]
