"""Pagination utilities."""

from typing import Any

from django.core.paginator import Paginator
from django.db.models import QuerySet

from ..config import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


def paginate_queryset(
    queryset: QuerySet,
    page: int = 1,
    page_size: int | None = None,
) -> dict[str, Any]:
    """Paginate a queryset and return pagination info.

    Args:
        queryset: Django queryset to paginate
        page: Page number to retrieve (default: 1)
        page_size: Number of items per page (default from constants)

    Returns:
        Dictionary containing paginated results and pagination metadata
    """
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


def get_page_range(current_page: int, total_pages: int, window: int = 5) -> list[int]:
    """Get a range of page numbers around the current page.

    Args:
        current_page: Current page number
        total_pages: Total number of pages
        window: Number of pages to show around current page

    Returns:
        List of page numbers to display
    """
    start = max(1, current_page - window // 2)
    end = min(total_pages + 1, start + window)
    start = max(1, end - window)

    return list(range(start, end))
