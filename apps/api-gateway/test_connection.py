"""Standalone Database Connection & Pipeline Diagnostic Script.

Verifies end-to-end configuration pipeline:
    os.environ -> Pydantic Settings -> SQLAlchemy Engine -> Async PostgreSQL Connection -> DB Diagnostics
"""

import os
import sys
import time
import asyncio
from sqlalchemy import text

# Force UTF-8 output encoding for Windows PowerShell/CMD compatibility
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Step 1: Environment Loading Inspection
print("=" * 60)
print("PART 1: ENVIRONMENT & PIPELINE AUDIT")
print("=" * 60)

raw_env_url = os.environ.get("DATABASE_URL", "[Not set in os.environ (loaded from .env.development)]")
print(f"1. Raw os.environ DATABASE_URL : {raw_env_url}")

from app.config.settings import settings

print(f"2. Pydantic Settings DATABASE_URL : {settings.database.url}")

from app.database.engine import engine

print(f"3. SQLAlchemy Engine URL         : {engine.url}")

# Verify pipeline parity
engine_url_str = engine.url.render_as_string(hide_password=False)
if settings.database.url == engine_url_str:
    print("   [OK] Settings URL and Engine URL are IDENTICAL.")
else:
    print("   [WARNING] Settings URL and Engine URL mismatch!")



# Step 2: Database Connectivity Test
async def run_diagnostic():
    print("\n" + "=" * 60)
    print("PART 2: ASYNC POSTGRESQL CONNECTIVITY TEST")
    print("=" * 60)
    print("Connecting to Neon PostgreSQL...")

    start_time = time.perf_counter()
    try:
        async with engine.connect() as conn:
            elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
            print(f"[SUCCESS] Connected in {elapsed_ms}ms!")

            # Retrieve database name
            db_res = await conn.execute(text("SELECT current_database();"))
            db_name = db_res.scalar()
            print(f"  Current Database  : {db_name}")

            # Retrieve current user
            user_res = await conn.execute(text("SELECT current_user;"))
            user_name = user_res.scalar()
            print(f"  Current User      : {user_name}")

            # Retrieve PostgreSQL version
            version_res = await conn.execute(text("SELECT version();"))
            version_str = version_res.scalar()
            print(f"  PostgreSQL Version : {version_str}")

            print(f"  Connection Latency : {elapsed_ms}ms")
            print("\n[VERDICT] Database configuration & connection pipeline operational!")

    except Exception as exc:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        print(f"\n[FAILURE] Connection failed after {elapsed_ms}ms")
        print(f"  Error Type    : {type(exc).__name__}")
        print(f"  Error Message : {exc}")
        print("\nNote on network timeouts: If port 5432 is blocked on your network/ISP/firewall,")
        print("connect via VPN or mobile hotspot to allow outbound TCP port 5432 traffic.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(run_diagnostic())