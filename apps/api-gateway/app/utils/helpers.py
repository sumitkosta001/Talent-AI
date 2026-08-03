"""General Pure Helper Functions."""

import uuid


def generate_uuid_string() -> str:
    """Generate a random UUID v4 string.
    
    Returns:
        UUID v4 string.
    """
    return str(uuid.uuid4())
