"""Security Utilities and Authorization Header Parsers.

Extracts bearer tokens from incoming HTTP request headers and coordinates
credential validation.
"""

from typing import Optional


def extract_bearer_token(authorization_header: Optional[str]) -> Optional[str]:
    """Extract raw JWT bearer token from Authorization header value.
    
    Args:
        authorization_header: Value of HTTP 'Authorization' header.
        
    Returns:
        Extracted token string or None if header is missing/invalid.
    """
    if not authorization_header or not authorization_header.startswith("Bearer "):
        return None
    return authorization_header.split(" ")[1]
