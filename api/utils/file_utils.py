"""File handling and storage utilities."""

import re
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import default_storage


def upload_file_to_storage(file, folder: str = "") -> str:
    """Upload a file to the configured storage backend.

    Args:
        file: File object to upload
        folder: Optional folder path

    Returns:
        The stored file path
    """
    file_path = f"{folder}/{file.name}" if folder else file.name
    return default_storage.save(file_path, file)


def get_file_url(file_path: str) -> str:
    """Get the full URL for a file in storage.

    Args:
        file_path: Path to the file in storage

    Returns:
        Full URL to access the file
    """
    if getattr(settings, "USE_S3", False):
        return default_storage.url(file_path)
    return urljoin(settings.MEDIA_URL, file_path)


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename for safe storage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename safe for storage
    """
    # Replace any character that isn't alphanumeric, dot, hyphen, or underscore
    sanitized = re.sub(r"[^a-zA-Z0-9.\-_]", "_", filename)

    # Remove multiple consecutive underscores
    sanitized = re.sub(r"_+", "_", sanitized)

    # Remove leading/trailing underscores
    return sanitized.strip("_")


def get_file_extension(filename: str) -> str:
    """Get file extension from filename.

    Args:
        filename: Name of the file

    Returns:
        File extension (including the dot)
    """
    return filename.split(".")[-1].lower() if "." in filename else ""


def is_allowed_file_type(filename: str, allowed_extensions: list[str]) -> bool:
    """Check if file type is allowed.

    Args:
        filename: Name of the file
        allowed_extensions: List of allowed extensions (with dots)

    Returns:
        True if file type is allowed, False otherwise
    """
    extension = f".{get_file_extension(filename)}"
    return extension.lower() in [ext.lower() for ext in allowed_extensions]


def get_file_size_mb(file) -> float:
    """Get file size in megabytes.

    Args:
        file: File object

    Returns:
        File size in MB
    """
    return file.size / (1024 * 1024)


def generate_unique_filename(filename: str) -> str:
    """Generate a unique filename by appending timestamp.

    Args:
        filename: Original filename

    Returns:
        Unique filename with timestamp
    """
    import time

    name, ext = filename.rsplit(".", 1) if "." in filename else (filename, "")
    timestamp = str(int(time.time()))
    return f"{name}_{timestamp}.{ext}" if ext else f"{name}_{timestamp}"
