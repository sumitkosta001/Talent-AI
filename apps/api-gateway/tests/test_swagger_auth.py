"""Automated Regression Tests for Swagger Authentication & Resume Ownership Enforcement (Day 35)."""

import pytest
import uuid
import asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database.session import SessionLocal
from app.models.enums import UserRole
from app.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_swagger_openapi_schema_security():
    """Verify that GET /openapi.json contains HTTPBearer scheme with bearerFormat: JWT."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        res = await client.get("/openapi.json")
        assert res.status_code == 200, f"Failed to get openapi.json: {res.text}"
        data = res.json()
        
        # 1. Verify components.securitySchemes.HTTPBearer
        sec_schemes = data.get("components", {}).get("securitySchemes", {})
        assert "HTTPBearer" in sec_schemes, "HTTPBearer missing from securitySchemes"
        assert sec_schemes["HTTPBearer"]["type"] == "http"
        assert sec_schemes["HTTPBearer"]["scheme"] == "bearer"
        assert sec_schemes["HTTPBearer"]["bearerFormat"] == "JWT"

        # 2. Verify protected operation /api/v1/candidates/me/resumes/{resume_id}/process has security
        process_path = data.get("paths", {}).get("/api/v1/candidates/me/resumes/{resume_id}/process", {})
        assert "post" in process_path, "POST /api/v1/candidates/me/resumes/{resume_id}/process missing"
        op_sec = process_path["post"].get("security", [])
        assert {"HTTPBearer": []} in op_sec, f"HTTPBearer security missing on process endpoint: {op_sec}"


@pytest.mark.asyncio
async def test_protected_endpoint_without_token_returns_401():
    """Verify that calling protected process endpoint without authorization header returns 401."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        dummy_id = str(uuid.uuid4())
        res = await client.post(f"/api/v1/candidates/me/resumes/{dummy_id}/process")
        assert res.status_code == 401
        data = res.json()
        assert data["success"] is False
        assert "Authorization bearer token required" in str(data)


@pytest.mark.asyncio
async def test_protected_endpoint_with_invalid_token_returns_401():
    """Verify that calling protected endpoint with malformed/invalid token returns 401."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        dummy_id = str(uuid.uuid4())
        headers = {"Authorization": "Bearer invalid_malformed_jwt_token_string"}
        res = await client.post(f"/api/v1/candidates/me/resumes/{dummy_id}/process", headers=headers)
        assert res.status_code == 401
        data = res.json()
        assert data["success"] is False


@pytest.mark.asyncio
async def test_resume_ownership_validation_rejects_unowned_resume():
    """Verify that user A cannot access or process user B's resume or pass user_id as resume_id."""
    from unittest.mock import patch, AsyncMock
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Warm up remote DB connection pool
        async with SessionLocal() as db:
            from sqlalchemy import text
            await db.execute(text("SELECT 1"))

        email_a = f"owner_a_{uuid.uuid4().hex[:6]}@example.com"
        email_b = f"owner_b_{uuid.uuid4().hex[:6]}@example.com"
        pwd = "Password123!"

        # Register User A
        res_a = await client.post("/api/v1/auth/register", json={
            "email": email_a, "password": pwd, "confirm_password": pwd,
            "first_name": "User", "last_name": "Alpha"
        })
        assert res_a.status_code == 201
        user_a_id = res_a.json()["user"]["id"]

        # Register User B
        res_b = await client.post("/api/v1/auth/register", json={
            "email": email_b, "password": pwd, "confirm_password": pwd,
            "first_name": "User", "last_name": "Beta"
        })
        assert res_b.status_code == 201
        user_b_id = res_b.json()["user"]["id"]

        # Login User A & B
        login_a = await client.post("/api/v1/auth/login", json={"email": email_a, "password": pwd})
        assert login_a.status_code == 200, f"Login failed: {login_a.text}"
        token_a = login_a.json()["tokens"]["access_token"]


        headers_a = {"Authorization": f"Bearer {token_a}"}

        # 1. User A tries to pass user_id as resume_id -> must fail with 404 (Resume not found for profile)
        res_fail1 = await client.post(f"/api/v1/candidates/me/resumes/{user_a_id}/process", headers=headers_a)
        assert res_fail1.status_code == 404

        # 2. User A tries to pass user B's user_id as resume_id -> must fail with 404
        res_fail2 = await client.post(f"/api/v1/candidates/me/resumes/{user_b_id}/process", headers=headers_a)
        assert res_fail2.status_code == 404

        # 3. User A tries to pass a non-existent random UUID as resume_id -> must fail with 404
        random_uuid = str(uuid.uuid4())
        res_fail3 = await client.post(f"/api/v1/candidates/me/resumes/{random_uuid}/process", headers=headers_a)
        assert res_fail3.status_code == 404

    patcher.stop()
