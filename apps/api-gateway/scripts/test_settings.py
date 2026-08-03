"""Script to verify Pydantic Settings loading from .env.development.

Usage:
    python scripts/test_settings.py
"""

import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config.settings import settings


def main() -> None:
    """Verify settings loading."""
    print("==================================================")
    print("TALENTAI SETTINGS VALIDATION")
    print("==================================================")
    print("settings.database.url:        ", settings.database.url)
    print("settings.database.pool_size:  ", settings.database.pool_size)
    print("settings.database.echo:       ", settings.database.echo)
    print("settings.server.host:         ", settings.server.host)
    print("settings.server.port:         ", settings.server.port)
    print("==================================================")


if __name__ == "__main__":
    main()
