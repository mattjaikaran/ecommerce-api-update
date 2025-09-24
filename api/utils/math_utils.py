"""Mathematical calculation utilities."""

from decimal import Decimal


def calculate_discount_amount(
    original_price: Decimal, discount_percentage: float
) -> Decimal:
    """Calculate discount amount based on percentage.

    Args:
        original_price: The original price before discount
        discount_percentage: Discount percentage (0-100)

    Returns:
        The discount amount

    Raises:
        ValueError: If discount percentage is not between 0 and 100
    """
    if not 0 <= discount_percentage <= 100:
        msg = "Discount percentage must be between 0 and 100"
        raise ValueError(msg)

    discount_amount = original_price * Decimal(str(discount_percentage / 100))
    return discount_amount.quantize(Decimal("0.01"))


def calculate_tax_amount(subtotal: Decimal, tax_rate: float) -> Decimal:
    """Calculate tax amount based on subtotal and tax rate.

    Args:
        subtotal: The subtotal amount before tax
        tax_rate: Tax rate as a decimal (e.g., 0.08 for 8%)

    Returns:
        The calculated tax amount
    """
    tax_amount = subtotal * Decimal(str(tax_rate))
    return tax_amount.quantize(Decimal("0.01"))


def calculate_shipping_cost(
    weight: float, distance: float, shipping_type: str = "standard"
) -> Decimal:
    """Calculate shipping cost based on weight, distance, and type.

    Args:
        weight: Package weight in pounds
        distance: Shipping distance in miles
        shipping_type: Type of shipping ("standard" or "express")

    Returns:
        The calculated shipping cost
    """
    base_cost = Decimal("5.00")
    weight_cost = Decimal(str(weight * 0.5))
    distance_cost = Decimal(str(distance * 0.1))

    if shipping_type == "express":
        base_cost *= 2

    total_cost = base_cost + weight_cost + distance_cost
    return total_cost.quantize(Decimal("0.01"))


def safe_divide(dividend: float, divisor: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if divisor is zero.

    Args:
        dividend: The number to be divided
        divisor: The number to divide by
        default: Value to return if divisor is zero

    Returns:
        The division result or default value
    """
    if divisor == 0:
        return default
    return dividend / divisor


def calculate_percentage(part: Decimal, whole: Decimal) -> float:
    """Calculate percentage of part relative to whole.

    Args:
        part: The part value
        whole: The whole value

    Returns:
        The percentage (0-100)
    """
    if whole == 0:
        return 0.0
    return float((part / whole) * 100)


def round_to_nearest_cent(amount: Decimal) -> Decimal:
    """Round amount to nearest cent.

    Args:
        amount: The amount to round

    Returns:
        The amount rounded to 2 decimal places
    """
    return amount.quantize(Decimal("0.01"))
