"""Utility functions used across the ecommerce API.

This module contains common utility functions that are used
throughout the application for various purposes.
"""

import hashlib
import secrets
import string
from decimal import Decimal
from typing import Any
from urllib.parse import urljoin

from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.text import slugify

from .constants import (
    CACHE_TIMEOUT_MEDIUM,
    DEFAULT_PAGE_SIZE,
    MAX_PAGE_SIZE,
)


def generate_unique_id(length: int = 12) -> str:
    """Generate a unique alphanumeric ID."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_order_number() -> str:
    """Generate a unique order number."""
    timestamp = str(int(timezone.now().timestamp()))
    random_part = generate_unique_id(6)
    return f"ORD-{timestamp[-6:]}-{random_part}"


def generate_secure_hash(data: str) -> str:
    """Generate a secure hash for the given data."""
    return hashlib.sha256(data.encode()).hexdigest()


def calculate_discount_amount(
    original_price: Decimal, discount_percentage: float
) -> Decimal:
    """Calculate discount amount based on percentage."""
    if not 0 <= discount_percentage <= 100:
        msg = "Discount percentage must be between 0 and 100"
        raise ValueError(msg)

    discount_amount = original_price * Decimal(str(discount_percentage / 100))
    return discount_amount.quantize(Decimal("0.01"))


def calculate_tax_amount(subtotal: Decimal, tax_rate: float) -> Decimal:
    """Calculate tax amount based on subtotal and tax rate."""
    tax_amount = subtotal * Decimal(str(tax_rate))
    return tax_amount.quantize(Decimal("0.01"))


def calculate_shipping_cost(
    weight: float, distance: float, shipping_type: str = "standard"
) -> Decimal:
    """Calculate shipping cost based on weight, distance, and type."""
    base_cost = Decimal("5.00")
    weight_cost = Decimal(str(weight * 0.5))
    distance_cost = Decimal(str(distance * 0.1))

    if shipping_type == "express":
        base_cost *= 2

    total_cost = base_cost + weight_cost + distance_cost
    return total_cost.quantize(Decimal("0.01"))


def create_slug(text: str, max_length: int = 255) -> str:
    """Create a URL-friendly slug from text."""
    slug = slugify(text)
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")
    return slug


def paginate_queryset(
    queryset: QuerySet,
    page: int = 1,
    page_size: int | None = None,
) -> dict[str, Any]:
    """Paginate a queryset and return pagination info."""
    if page_size is None:
        page_size = DEFAULT_PAGE_SIZE

    # Ensure page_size doesn't exceed maximum
    page_size = min(page_size, MAX_PAGE_SIZE)

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)

    return {
        "results": page_obj.object_list,
        "pagination": {
            "page": page_obj.number,
            "page_size": page_size,
            "total_pages": paginator.num_pages,
            "total_count": paginator.count,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "next_page": page_obj.next_page_number() if page_obj.has_next() else None,
            "previous_page": page_obj.previous_page_number()
            if page_obj.has_previous()
            else None,
        },
    }


def cache_key_builder(*args: str) -> str:
    """Build a cache key from multiple arguments."""
    return ":".join(str(arg) for arg in args)


def get_cached_data(key: str, default: Any = None) -> Any:
    """Get data from cache with optional default."""
    return cache.get(key, default)


def set_cached_data(key: str, value: Any, timeout: int = CACHE_TIMEOUT_MEDIUM) -> None:
    """Set data in cache with timeout."""
    cache.set(key, value, timeout)


def invalidate_cache_pattern(pattern: str) -> None:
    """Invalidate cache keys matching a pattern."""
    # This would need to be implemented based on your cache backend
    # For Redis, you could use cache.delete_pattern()


def send_email_template(
    template_name: str,
    context: dict[str, Any],
    recipient_email: str,
    subject: str,
    from_email: str | None = None,
) -> bool:
    """Send an email using a template."""
    try:
        html_content = render_to_string(template_name, context)

        send_mail(
            subject=subject,
            message="",  # Plain text version
            html_message=html_content,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return True
    except Exception:
        # Log the error
        return False


def upload_file_to_storage(file, folder: str = "") -> str:
    """Upload a file to the configured storage backend."""
    file_path = f"{folder}/{file.name}" if folder else file.name

    return default_storage.save(file_path, file)


def get_file_url(file_path: str) -> str:
    """Get the full URL for a file in storage."""
    if settings.USE_S3:
        return default_storage.url(file_path)
    return urljoin(settings.MEDIA_URL, file_path)


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format."""
    import re

    # Remove all non-digit characters
    digits_only = re.sub(r"\D", "", phone)

    # Check if it's a valid length (10-15 digits)
    return 10 <= len(digits_only) <= 15


def format_currency(amount: float | Decimal, currency: str = "USD") -> str:
    """Format an amount as currency."""
    if isinstance(amount, (int, float)):
        amount = Decimal(str(amount))

    # Simple formatting - in production you'd use proper locale formatting
    if currency == "USD":
        return f"${amount:.2f}"
    if currency == "EUR":
        return f"€{amount:.2f}"
    if currency == "GBP":
        return f"£{amount:.2f}"
    return f"{amount:.2f} {currency}"


def get_client_ip(request: HttpRequest) -> str:
    """Get the client IP address from the request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def is_ajax(request: HttpRequest) -> bool:
    """Check if the request is an AJAX request."""
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length with optional suffix."""
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def convert_to_bool(value: Any) -> bool:
    """Convert various types to boolean."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def safe_divide(dividend: float, divisor: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if divisor is zero."""
    if divisor == 0:
        return default
    return dividend / divisor


def chunks(lst: list[Any], chunk_size: int) -> list[list[Any]]:
    """Yield successive chunks from a list."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


def deep_merge_dicts(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]:
    """Deep merge two dictionaries."""
    result = dict1.copy()

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename for safe storage."""
    import re

    # Replace any character that isn't alphanumeric, dot, hyphen, or underscore
    sanitized = re.sub(r"[^a-zA-Z0-9.\-_]", "_", filename)

    # Remove multiple consecutive underscores
    sanitized = re.sub(r"_+", "_", sanitized)

    # Remove leading/trailing underscores
    return sanitized.strip("_")
