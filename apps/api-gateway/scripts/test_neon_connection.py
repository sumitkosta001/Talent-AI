"""Comprehensive diagnostic verification script for Neon PostgreSQL connection.

Usage:
    python scripts/test_neon_connection.py
"""

import sys
import time
import socket
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


async def verify_dns(host: str) -> str:
    """Check DNS resolution for target host."""
    print(f"1. DNS Verification - Resolving host: {host}...")
    try:
        ip = socket.gethostbyname(host)
        print(f"   [DNS Success] Host resolved to IP: {ip}")
        return ip
    except socket.gaierror as err:
        print(f"   [DNS Failure] Failed to resolve host '{host}': {err}")
        print("   This suggests a local network issue, DNS server outage, or invalid host string.")
        return ""


async def verify_port_accessibility(host: str, port: int) -> bool:
    """Check if outgoing TCP port is open or blocked by firewall."""
    print(f"2. TCP Port Verification - Checking outgoing connection to {host}:{port}...")
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=5.0
        )
        writer.close()
        await writer.wait_closed()
        print(f"   [Port Success] Outgoing TCP connection to {host}:{port} established successfully.")
        return True
    except asyncio.TimeoutError:
        print(f"   [Port Timeout] Connection to {host}:{port} timed out after 5.0s.")
        print(f"   WARNING: Outgoing TCP traffic on port {port} is likely BLOCKED by a local firewall or network policy!")
        return False
    except ConnectionRefusedError:
        print(f"   [Connection Refused] Server at {host}:{port} active but rejected connection.")
        return False
    except Exception as exc:
        print(f"   [Port Error] Outgoing port test failed: {exc}")
        return False


async def test_portquiz() -> None:
    """Helper diagnostic to verify if port 5432 is blocked universally by firewall."""
    print("3. Firewall Diagnosis - Checking universal port 5432 outbound access via portquiz.net...")
    success = await verify_port_accessibility("portquiz.net", 5432)
    if not success:
        print("   [Diagnostic Verdict] OUTGOING PORT 5432 IS BLOCKED universally by local network/firewall.")
        print("   Please connect to a VPN, use a different network, or ask your network administrator to allow outgoing port 5432 traffic.")


async def main() -> None:
    print("==================================================")
    print("NEON POSTGRESQL CONNECTION DIAGNOSTIC TOOL")
    print("==================================================")
    
    url_str = settings.database.url
    parsed_info = make_url(url_str)
    
    ssl_mode = parsed_info.query.get("sslmode", "not specified")
    ssl_enabled = "sslmode" in parsed_info.query or "ssl" in parsed_info.query
    
    print("Loaded Database Settings:")
    print(f"  Driver:             {parsed_info.drivername}")
    print(f"  Host:               {parsed_info.host}")
    print(f"  Database:           {parsed_info.database}")
    print(f"  Username:           {parsed_info.username}")
    print(f"  SSL Enabled:        {ssl_enabled}")
    print(f"  SSL Mode Option:    {ssl_mode}")
    print(f"  Connection Timeout: {settings.database.connect_timeout}s")
    print(f"  Pool Timeout:       {settings.database.pool_timeout}s")
    print(f"  Pool Size:          {settings.database.pool_size}")
    print("==================================================")

    # Task 10: Verify Pooler vs Direct Endpoint Recommendation
    host = parsed_info.host or ""
    if "-pooler" in host:
        print("[Endpoint Diagnosis] Using Neon Pooler Endpoint (-pooler).")
        print("  Recommendation: Use the pooler endpoint for serverless deployment / high concurrency.")
        print("  If you execute migrations or long transactions, consider the direct host (omit '-pooler').")
    else:
        print("[Endpoint Diagnosis] Using Neon Direct Endpoint.")
        print("  Recommendation: Use the direct endpoint for heavy schema migrations or direct utility scripts.")

    print("==================================================")

    # 1. DNS check
    ip = await verify_dns(host)
    
    # 2. Port connectivity test
    if ip:
        await verify_port_accessibility(host, 5432)

    # 3. Universal port check
    await test_portquiz()

    print("==================================================")
    print("4. Async Database Connection Test...")
    print("==================================================")

    db_url = url_str
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
        connect_args={
            "timeout": settings.database.connect_timeout,
            "server_settings": {
                "statement_timeout": "10000",
            }
        }
    )

    start_time = time.perf_counter()
    try:
        async with engine.connect() as conn:
            # Run queries
            res_ver = await conn.execute(text("SELECT version();"))
            ver_str = res_ver.scalar()

            res_db = await conn.execute(text("SELECT current_database();"))
            db_str = res_db.scalar()

            res_user = await conn.execute(text("SELECT current_user;"))
            user_str = res_user.scalar()

            res1 = await conn.execute(text("SELECT 1;"))
            val1 = res1.scalar()

            latency_ms = round((time.perf_counter() - start_time) * 1000, 2)

            print("\n==================================================")
            print("DATABASE METRICS RETRIEVED SUCCESSFULLY:")
            print("==================================================")
            print("Driver:       ", parsed_info.drivername)
            print("Database:     ", db_str)
            print("User:         ", user_str)
            print("Version:      ", ver_str)
            print("Liveness:     ", f"SELECT 1 returned {val1}")
            print("Latency:      ", f"{latency_ms}ms")
            print("==================================================")
            print("SUCCESS")
            print("==================================================")
            
    except Exception as exc:
        print("\n==================================================")
        print("DATABASE CONNECTIVITY CHECK FAILED!")
        print(f"Exception Type: {type(exc).__name__}")
        print(f"Exception Repr: {repr(exc)}")
        print("--------------------------------------------------")
        print("Detailed Stack Trace:")
        print("--------------------------------------------------")
        traceback.print_exc()
        print("==================================================")
        
        # Analyze exception cause to explain failure
        exc_str = str(exc).lower()
        if "timeout" in exc_str or type(exc).__name__ == "TimeoutError":
            print("[Verdict] Timeout error occurred.")
            print("This suggests that outbound traffic to port 5432 is blocked by a firewall,")
            print("or the database server did not respond within the connection timeout limit.")
        elif "password" in exc_str or "authentication" in exc_str:
            print("[Verdict] Authentication failed. Check your password and username configuration in settings.")
        elif "ssl" in exc_str or "tls" in exc_str:
            print("[Verdict] SSL negotiation failed. Ensure the server supports SSL and certificates are verified.")
        else:
            print("[Verdict] Connection closed unexpectedly. Please check network/credentials configuration.")
        print("==================================================")
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
