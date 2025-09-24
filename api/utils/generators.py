"""ID and data generation utilities."""

import hashlib
import secrets
import string

from django.utils import timezone


def generate_unique_id(length: int = 12) -> str:
    """Generate a unique alphanumeric ID.

    Args:
        length: Length of the generated ID (default: 12)

    Returns:
        A unique alphanumeric string
    """
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_order_number() -> str:
    """Generate a unique order number.

    Returns:
        A unique order number in format ORD-XXXXXX-YYYYYY
    """
    timestamp = str(int(timezone.now().timestamp()))
    random_part = generate_unique_id(6)
    return f"ORD-{timestamp[-6:]}-{random_part}"


def generate_secure_hash(data: str) -> str:
    """Generate a secure hash for the given data.

    Args:
        data: The string data to hash

    Returns:
        A SHA256 hash of the input data
    """
    return hashlib.sha256(data.encode()).hexdigest()


def generate_invoice_number() -> str:
    """Generate a unique invoice number.

    Returns:
        A unique invoice number in format INV-XXXXXX-YYYYYY
    """
    timestamp = str(int(timezone.now().timestamp()))
    random_part = generate_unique_id(6)
    return f"INV-{timestamp[-6:]}-{random_part}"


def generate_tracking_number() -> str:
    """Generate a unique tracking number.

    Returns:
        A unique tracking number in format TRK-XXXXXX-YYYYYY
    """
    timestamp = str(int(timezone.now().timestamp()))
    random_part = generate_unique_id(8)
    return f"TRK-{timestamp[-6:]}-{random_part}"


def generate_coupon_code(length: int = 8) -> str:
    """Generate a unique coupon code.

    Args:
        length: Length of the coupon code (default: 8)

    Returns:
        A unique coupon code
    """
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
