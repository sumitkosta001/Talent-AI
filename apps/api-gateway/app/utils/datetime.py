"""UTC DateTime Parsing and Formatting Helpers."""

from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return timezone-aware current UTC datetime instance.
    
    Returns:
        Current datetime in UTC timezone.
    """
    return datetime.now(timezone.utc)
