"""In-memory ASGI Integration Test Runner using httpx.AsyncClient."""

import asyncio
import io
import uuid
import sys

# Force UTF-8 stdout encoding for Windows compatibility
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from httpx import AsyncClient, ASGITransport
from app.main import app

async def run_integration_tests():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("\n============================================================")
        print("RUNNING IN-MEMORY HTTP INTEGRATION TESTS")
        print("============================================================")
        
        # Test 1: Register
        test_email = f"integration_test_{uuid.uuid4().hex[:8]}@example.com"
        reg_payload = {
            "email": test_email,
            "password": "Password123!",
            "confirm_password": "Password123!",
            "first_name": "Integration",
            "last_name": "TestUser",
        }
        res = await client.post("/api/v1/auth/register", json=reg_payload)
        print("1. POST /api/v1/auth/register -> Status:", res.status_code)
        assert res.status_code == 201, res.text
        data = res.json()
        assert "access_token" in data["tokens"]
        access_token = data["tokens"]["access_token"]
        print("   [OK] Register successful!")

        headers = {"Authorization": f"Bearer {access_token}"}

        # Test 2: GET /api/v1/candidates/me (Verify automatic profile creation)
        res = await client.get("/api/v1/candidates/me", headers=headers)
        print("2. GET /api/v1/candidates/me -> Status:", res.status_code)
        assert res.status_code == 200, res.text
        profile = res.json()
        assert profile["linkedin_url"] is None
        assert profile["github_url"] is None
        assert profile["portfolio_url"] is None or profile["portfolio_url"] == ""
        print("   [OK] Candidate profile loaded and is empty!")

        # Test 3: PATCH /api/v1/candidates/me (Update social accounts)
        update_payload = {
            "linkedin_url": "https://linkedin.com/in/integration-test",
            "github_url": "https://github.com/integration-test",
            "portfolio_url": "https://integration-test.dev",
        }
        res = await client.patch("/api/v1/candidates/me", json=update_payload, headers=headers)
        print("3. PATCH /api/v1/candidates/me -> Status:", res.status_code)
        assert res.status_code == 200, res.text
        updated = res.json()
        assert updated["linkedin_url"] == "https://linkedin.com/in/integration-test"
        assert updated["github_url"] == "https://github.com/integration-test"
        assert updated["portfolio_url"] == "https://integration-test.dev"
        print("   [OK] Candidate profile social links updated successfully!")

        # Test 4: Verify Social Links Persisted (Re-fetch profile)
        res = await client.get("/api/v1/candidates/me", headers=headers)
        print("4. GET /api/v1/candidates/me (Refetch) -> Status:", res.status_code)
        assert res.status_code == 200, res.text
        profile_refetched = res.json()
        assert profile_refetched["linkedin_url"] == "https://linkedin.com/in/integration-test"
        assert profile_refetched["github_url"] == "https://github.com/integration-test"
        assert profile_refetched["portfolio_url"] == "https://integration-test.dev"
        print("   [OK] Candidate profile social links verified as persisted in DB!")

        # Test 5: POST /api/v1/candidates/me/resume/upload
        dummy_pdf_content = b"%PDF-1.4 mock pdf content integration test"
        files = {"file": ("my_integration_resume.pdf", dummy_pdf_content, "application/pdf")}
        res = await client.post("/api/v1/candidates/me/resume/upload", files=files, headers=headers)
        print("5. POST /api/v1/candidates/me/resume/upload -> Status:", res.status_code)
        assert res.status_code == 200, res.text
        assert res.json()["success"] is True
        print("   [OK] Candidate resume upload succeeded!")

        # Test 6: Verify resume_url populated in CandidateProfile
        res = await client.get("/api/v1/candidates/me", headers=headers)
        profile_refetched_2 = res.json()
        assert profile_refetched_2["resume_url"] == "/api/v1/candidates/me/resume/download"
        print("   [OK] Candidate profile resume_url verified as set to download endpoint!")

        # Test 7: GET /api/v1/candidates/me/resume/download
        res = await client.get("/api/v1/candidates/me/resume/download", headers=headers)
        print("7. GET /api/v1/candidates/me/resume/download -> Status:", res.status_code)
        assert res.status_code == 200, res.text
        assert res.content == dummy_pdf_content
        assert "attachment" in res.headers["content-disposition"]
        print("   [OK] Candidate resume downloaded and bytes verified matches exactly!")

        print("\n============================================================")
        print("ALL INTEGRATION TESTS PASSED SUCCESSFULLY!")
        print("============================================================\n")

if __name__ == "__main__":
    asyncio.run(run_integration_tests())
