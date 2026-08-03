"""Pagination Response Wrapper Utilities."""

from typing import List, TypeVar, Generic, Dict, Any

T = TypeVar("T")


def build_paginated_response(items: List[Any], total_count: int, page: int, size: int) -> Dict[str, Any]:
    """Construct standard paginated payload dictionary.
    
    Args:
        items: List of page items.
        total_count: Total database records count.
        page: Current page number.
        size: Items per page size.
        
    Returns:
        Structured pagination dictionary.
    """
    total_pages = (total_count + size - 1) // size if size > 0 else 0
    return {
        "items": items,
        "meta": {
            "total_count": total_count,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
    }
