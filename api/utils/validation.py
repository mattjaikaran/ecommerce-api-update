"""Data validation utilities."""

import re
from typing import Any


def validate_phone_number(phone: str) -> bool:
    """Validate phone number format.

    Args:
        phone: Phone number string to validate

    Returns:
        True if phone number is valid, False otherwise
    """
    # Remove all non-digit characters
    digits_only = re.sub(r"\D", "", phone)

    # Check if it's a valid length (10-15 digits)
    return 10 <= len(digits_only) <= 15


def convert_to_bool(value: Any) -> bool:
    """Convert various types to boolean.

    Args:
        value: Value to convert to boolean

    Returns:
        Boolean representation of the value
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "on")
    if isinstance(value, (int, float)):
        return bool(value)
    return False


def validate_email_format(email: str) -> bool:
    """Validate email format using regex.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> dict[str, bool]:
    """Validate password strength requirements.

    Args:
        password: Password string to validate

    Returns:
        Dictionary with validation results for each requirement
    """
    return {
        "min_length": len(password) >= 8,
        "has_uppercase": bool(re.search(r"[A-Z]", password)),
        "has_lowercase": bool(re.search(r"[a-z]", password)),
        "has_digit": bool(re.search(r"\d", password)),
        "has_special": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
    }


def validate_credit_card_number(card_number: str) -> bool:
    """Validate credit card number using Luhn algorithm.

    Args:
        card_number: Credit card number to validate

    Returns:
        True if card number is valid, False otherwise
    """
    # Remove spaces and non-digits
    card_number = re.sub(r"\D", "", card_number)

    if len(card_number) < 13 or len(card_number) > 19:
        return False

    # Luhn algorithm
    def luhn_check(card_num):
        total = 0
        reverse_digits = card_num[::-1]

        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n = (n // 10) + (n % 10)
            total += n

        return total % 10 == 0

    return luhn_check(card_number)


def validate_zip_code(zip_code: str, country: str = "US") -> bool:
    """Validate zip/postal code format.

    Args:
        zip_code: Zip/postal code to validate
        country: Country code (default: "US")

    Returns:
        True if zip code format is valid, False otherwise
    """
    if country.upper() == "US":
        # US zip code: 12345 or 12345-6789
        pattern = r"^\d{5}(-\d{4})?$"
    elif country.upper() == "CA":
        # Canadian postal code: A1A 1A1
        pattern = r"^[A-Za-z]\d[A-Za-z] ?\d[A-Za-z]\d$"
    elif country.upper() == "UK":
        # UK postal code: various formats
        pattern = r"^[A-Za-z]{1,2}\d[A-Za-z\d]? ?\d[A-Za-z]{2}$"
    else:
        # Generic: 3-10 alphanumeric characters
        pattern = r"^[A-Za-z\d\s-]{3,10}$"

    return bool(re.match(pattern, zip_code))
