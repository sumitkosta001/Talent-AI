"""
SQLAlchemy Async Engine Configuration
"""

import ssl

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
)

from app.config.settings import settings

# Sanitize connection URL for asyncpg compatibility
db_url = settings.database.url
if db_url.startswith("postgresql://"):
    db_url = "postgresql+asyncpg://" + db_url[len("postgresql://"):]

from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
parsed = urlparse(db_url)
query_params = parse_qs(parsed.query)

# Remove options that asyncpg does not accept as direct connection parameters
if "sslmode" in query_params:
    query_params.pop("sslmode")
if "channel_binding" in query_params:
    query_params.pop("channel_binding")

new_query = urlencode(query_params, doseq=True)
db_url = urlunparse(parsed._replace(query=new_query))

# Debug
print("=" * 80)
print("DATABASE URL:", db_url)
print("=" * 80)

ssl_context = ssl.create_default_context()

engine: AsyncEngine = create_async_engine(
    db_url,
    echo=settings.database.echo,
    future=True,
    pool_pre_ping=True,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_timeout=settings.database.pool_timeout,
    pool_recycle=settings.database.pool_recycle,
    connect_args={
        "ssl": ssl_context,
        "timeout": settings.database.connect_timeout,
        "server_settings": {
            "statement_timeout": "15000",
        },
    },
)