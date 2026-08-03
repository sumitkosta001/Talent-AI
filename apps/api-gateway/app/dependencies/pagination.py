"""Pagination Parameters Dependency Injection Provider."""

from typing import Dict, Any
from fastapi import Query
from app.constants.settings import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


def get_pagination_params(
    page: int = Query(1, ge=1, description="Page number starting at 1"),
    size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Items per page"),
) -> Dict[str, int]:
    """Parse and validate list pagination query parameters.
    
    Args:
        page: Requested 1-indexed page.
        size: Requested number of items per page.
        
    Returns:
        Dictionary with page, size, and calculated offset.
    """
    offset = (page - 1) * size
    return {"page": page, "size": size, "offset": offset}
