"""Text formatting and string manipulation utilities."""

from django.utils.text import slugify


def create_slug(text: str, max_length: int = 255) -> str:
    """Create a URL-friendly slug from text.

    Args:
        text: Text to convert to slug
        max_length: Maximum length of the slug

    Returns:
        URL-friendly slug
    """
    slug = slugify(text)
    if len(slug) > max_length:
        slug = slug[:max_length].rstrip("-")
    return slug


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """Truncate text to a maximum length with optional suffix.

    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: String to append when truncating

    Returns:
        Truncated text with suffix if needed
    """
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def title_case(text: str) -> str:
    """Convert text to title case, handling special cases.

    Args:
        text: Text to convert

    Returns:
        Text in title case
    """
    # Words that should remain lowercase in titles
    minor_words = {
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "for",
        "if",
        "in",
        "is",
        "nor",
        "of",
        "on",
        "or",
        "so",
        "the",
        "to",
        "up",
        "yet",
    }

    words = text.lower().split()
    title_words = []

    for i, word in enumerate(words):
        if i == 0 or i == len(words) - 1 or word not in minor_words:
            title_words.append(word.capitalize())
        else:
            title_words.append(word)

    return " ".join(title_words)


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case.

    Args:
        name: String in camelCase

    Returns:
        String in snake_case
    """
    import re

    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase.

    Args:
        name: String in snake_case

    Returns:
        String in camelCase
    """
    components = name.split("_")
    return components[0] + "".join(word.capitalize() for word in components[1:])


def format_bytes(bytes_value: int) -> str:
    """Format bytes into human readable format.

    Args:
        bytes_value: Number of bytes

    Returns:
        Human readable byte format (e.g., "1.2 MB")
    """
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"
