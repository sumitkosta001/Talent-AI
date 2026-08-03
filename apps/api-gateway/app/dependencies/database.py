"""Database Dependency Import Adapter.

Re-exports get_db from app.database.dependencies for backward compatibility.
"""

from app.database.dependencies import get_db

__all__ = ["get_db"]
