"""Script to test database connectivity using AsyncEngine.

Usage:
    python scripts/test_database.py
"""

import sys
import time
import asyncio
import traceback
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import settings


async def main() -> None:
    """Test AsyncEngine database connection."""
    print("==================================================")
    print("TALENTAI DATABASE CONNECTIVITY TEST")
    print("==================================================")
    print("Target DATABASE_URL:", settings.database.url)
    
    parsed_info = make_url(settings.database.url)
    ssl_mode = parsed_info.query.get("sslmode", "not specified")
    print(f"Driver:       {parsed_info.drivername}")
    print(f"Host:         {parsed_info.host}")
    print(f"Database:     {parsed_info.database}")
    print(f"Username:     {parsed_info.username}")
    print(f"SSL Mode:     {ssl_mode}")
    print("Attempting async connection...")

    db_url = settings.database.url
    # Sanitize query parameters for asyncpg compatibility
    parsed = urlparse(db_url)
    query_params = parse_qs(parsed.query)

    if "sslmode" in query_params:
        sslmode_val = query_params.pop("sslmode")[0]
        if sslmode_val in ["require", "verify-ca", "verify-full"]:
            query_params["ssl"] = ["require"]

    if "channel_binding" in query_params:
        query_params.pop("channel_binding")

    new_query = urlencode(query_params, doseq=True)
    db_url = urlunparse(parsed._replace(query=new_query))

    engine = create_async_engine(
        url=db_url,
        future=True,
        pool_pre_ping=True,
    )

    start_time = time.perf_counter()
    try:
        async with engine.connect() as conn:
            # 1. Execute SELECT version()
            res_ver = await conn.execute(text("SELECT version();"))
            ver_str = res_ver.scalar()

            # 2. Execute SELECT current_database()
            res_db = await conn.execute(text("SELECT current_database();"))
            db_str = res_db.scalar()

            # 3. Execute SELECT current_user
            res_user = await conn.execute(text("SELECT current_user;"))
            user_str = res_user.scalar()

            # 4. Execute SELECT 1
            res1 = await conn.execute(text("SELECT 1;"))
            val1 = res1.scalar()

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            print("==================================================")
            print("DATABASE CONNECTION METRICS:")
            print("==================================================")
            print("Driver:       ", parsed_info.drivername)
            print("Database:     ", db_str)
            print("User:         ", user_str)
            print("Version:      ", ver_str)
            print("Liveness:     ", f"SELECT 1 returned {val1}")
            print("Latency:      ", f"{latency_ms}ms")
            print("==================================================")

        await engine.dispose()
        print("SUCCESS")
        print("==================================================")

    except Exception:
        print("\n==================================================")
        print("DATABASE CONNECTION FAILED!")
        print("Full Traceback Exception:")
        print("==================================================")
        traceback.print_exc()
        print("==================================================")
        await engine.dispose()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
