"""Common Cross-Cutting Dependency Providers."""

from typing import Optional
from fastapi import Header


def get_request_id(x_request_id: Optional[str] = Header(None, alias="X-Request-ID")) -> Optional[str]:
    """Extract or return client tracking Request ID header value.
    
    Args:
        x_request_id: Optional header string.
        
    Returns:
        Header string or None.
    """
    return x_request_id
