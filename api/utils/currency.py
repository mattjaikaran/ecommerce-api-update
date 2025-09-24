"""Currency formatting utilities."""

from decimal import Decimal


def format_currency(amount: float | Decimal, currency: str = "USD") -> str:
    """Format an amount as currency.

    Args:
        amount: Amount to format
        currency: Currency code (default: "USD")

    Returns:
        Formatted currency string
    """
    if isinstance(amount, (int, float)):
        amount = Decimal(str(amount))

    # Simple formatting - in production you'd use proper locale formatting
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$",
    }

    symbol = currency_symbols.get(currency, currency)

    if currency == "JPY":
        # Japanese Yen doesn't use decimal places
        return f"{symbol}{amount:.0f}"

    return f"{symbol}{amount:.2f}"


def convert_currency(
    amount: Decimal, from_currency: str, to_currency: str, rates: dict[str, float]
) -> Decimal:
    """Convert amount between currencies using provided rates.

    Args:
        amount: Amount to convert
        from_currency: Source currency code
        to_currency: Target currency code
        rates: Dictionary of exchange rates with USD as base

    Returns:
        Converted amount
    """
    if from_currency == to_currency:
        return amount

    # Convert to USD first if needed
    if from_currency != "USD":
        amount = amount / Decimal(str(rates[from_currency]))

    # Convert from USD to target currency
    if to_currency != "USD":
        amount = amount * Decimal(str(rates[to_currency]))

    return amount.quantize(Decimal("0.01"))


def get_currency_symbol(currency_code: str) -> str:
    """Get currency symbol for a given currency code.

    Args:
        currency_code: Three-letter currency code

    Returns:
        Currency symbol or the code itself if symbol not found
    """
    symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "JPY": "¥",
        "CAD": "C$",
        "AUD": "A$",
        "CHF": "Fr",
        "CNY": "¥",
        "INR": "₹",
        "KRW": "₩",
        "BRL": "R$",
        "MXN": "$",
        "RUB": "₽",
    }

    return symbols.get(currency_code.upper(), currency_code)
