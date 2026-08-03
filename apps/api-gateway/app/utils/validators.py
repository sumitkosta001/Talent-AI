"""Custom File and String Input Validation Utilities."""

import re

EMAIL_REGEX = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_email_format(email: str) -> bool:
    """Validate string matches standard email address pattern.
    
    Args:
        email: Email string to test.
        
    Returns:
        True if valid format, False otherwise.
    """
    return bool(EMAIL_REGEX.match(email))
