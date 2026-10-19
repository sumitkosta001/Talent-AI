"""Phase 5 Step 10 — Security & Authorization Regression Tests.

Covers:
- Unauthenticated requests return 401 on every protected endpoint.
- Recruiter manages own-company jobs (CRUD + lifecycle).
- Cross-company IDOR protection: Recruiter A cannot touch Recruiter B's resources.
- Candidate role denied all recruiter-only job/company operations (403).
- Public job search exposes ONLY PUBLISHED non-deleted jobs.
- DRAFT, CLOSED, and soft-deleted jobs are invisible in public search.
- Invalid lifecycle transitions rejected (400).
- Company PATCH/DELETE ownership enforced server-side.
- PATCH /companies/{id} by wrong recruiter → 403.
- DELETE /companies/{id} by wrong recruiter → 403.

Uses unittest.mock to suppress real email delivery (prevents test from hanging).
Uses create_access_token to forge tokens for role-based testing without full login.
"""

import uuid
import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select

from app.main import app
from app.database.session import SessionLocal
from app.models.enums import UserRole, JobStatus
from app.models.user import User
from app.auth.jwt import create_access_token


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

JOB_PAYLOAD = {
    "title": "Security Test Engineer",
    "description": "Writing security tests for TalentAI",
    "work_mode": "REMOTE",
    "salary_min": 800000,
    "salary_max": 1500000,
    "currency": "INR",
    "required_skills": ["Python", "pytest"],
}


async def _register_and_promote(client: AsyncClient, email: str, pwd: str, role: UserRole) -> dict:
    """Register a user and immediately set their role in the DB."""
    res = await client.post("/api/v1/auth/register", json={
        "email": email,
        "password": pwd,
        "confirm_password": pwd,
        "first_name": "Test",
        "last_name": "User",
    })
    assert res.status_code == 201, f"Registration failed for {email}: {res.text}"
    user_id = res.json()["user"]["id"]

    async with SessionLocal() as db:
        user = (await db.execute(select(User).where(User.email == email))).scalar_one()
        user.role = role
        await db.commit()

    return {"id": user_id, "email": email}


async def _login(client: AsyncClient, email: str, pwd: str) -> str:
    """Login and return access token."""
    res = await client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert res.status_code == 200, f"Login failed for {email}: {res.text}"
    return res.json()["tokens"]["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Test 1 — Unauthenticated access returns 401
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_unauthenticated_returns_401():
    """All recruiter/company write endpoints must reject missing tokens with 401."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        dummy_id = str(uuid.uuid4())

        cases = [
            ("POST", f"/api/v1/jobs"),
            ("PATCH", f"/api/v1/jobs/{dummy_id}"),
            ("DELETE", f"/api/v1/jobs/{dummy_id}"),
            ("POST", f"/api/v1/jobs/{dummy_id}/publish"),
            ("POST", f"/api/v1/jobs/{dummy_id}/unpublish"),
            ("POST", f"/api/v1/jobs/{dummy_id}/close"),
            ("GET", "/api/v1/jobs/company/me"),
            ("GET", "/api/v1/companies/me"),
            ("PATCH", "/api/v1/companies/me"),
            ("PATCH", f"/api/v1/companies/{dummy_id}"),
            ("DELETE", f"/api/v1/companies/{dummy_id}"),
            ("POST", f"/api/v1/companies/{dummy_id}/join"),
        ]

        for method, url in cases:
            r = await client.request(method, url, json={"title": "x", "description": "y"})
            assert r.status_code == 401, (
                f"Expected 401 for unauthenticated {method} {url}, got {r.status_code}: {r.text[:200]}"
            )


# ---------------------------------------------------------------------------
# Test 2 — Invalid JWT token returns 401
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_invalid_token_returns_401():
    """Malformed/expired tokens must return 401, not a 500."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        bad_headers = {"Authorization": "Bearer totally.invalid.token"}
        dummy_id = str(uuid.uuid4())

        r = await client.post(f"/api/v1/jobs", headers=bad_headers, json=JOB_PAYLOAD)
        assert r.status_code == 401, f"Expected 401, got {r.status_code}"

        r = await client.get("/api/v1/companies/me", headers=bad_headers)
        assert r.status_code == 401


# ---------------------------------------------------------------------------
# Test 3 — Candidate role denied recruiter operations (403)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_candidate_denied_recruiter_operations():
    """A candidate JWT must receive 403 on all recruiter-only job and company endpoints."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            # Warm up DB
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            email = f"cand_role_{uuid.uuid4().hex[:6]}@example.com"
            await _register_and_promote(client, email, pwd, UserRole.CANDIDATE)
            token = await _login(client, email, pwd)
            headers = _auth(token)

            dummy_id = str(uuid.uuid4())

            recruiter_ops = [
                ("POST", "/api/v1/jobs", JOB_PAYLOAD),
                ("PATCH", f"/api/v1/jobs/{dummy_id}", {"title": "hack"}),
                ("DELETE", f"/api/v1/jobs/{dummy_id}", None),
                ("POST", f"/api/v1/jobs/{dummy_id}/publish", None),
                ("POST", f"/api/v1/jobs/{dummy_id}/unpublish", None),
                ("POST", f"/api/v1/jobs/{dummy_id}/close", None),
                ("GET", "/api/v1/jobs/company/me", None),
                ("GET", "/api/v1/companies/me", None),
                ("PATCH", "/api/v1/companies/me", {"location": "Anywhere"}),
                ("PATCH", f"/api/v1/companies/{dummy_id}", {"name": "Hacked"}),
                ("DELETE", f"/api/v1/companies/{dummy_id}", None),
            ]

            for method, url, body in recruiter_ops:
                r = await client.request(method, url, headers=headers, json=body)
                assert r.status_code == 403, (
                    f"Expected 403 for candidate {method} {url}, got {r.status_code}: {r.text[:200]}"
                )


# ---------------------------------------------------------------------------
# Test 4 — Job creation: company association required
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_recruiter_without_company_cannot_create_job():
    """A recruiter with no company_id must receive 403 when creating a job."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            email = f"recruiter_nocomp_{uuid.uuid4().hex[:6]}@example.com"
            await _register_and_promote(client, email, pwd, UserRole.RECRUITER)
            token = await _login(client, email, pwd)

            r = await client.post("/api/v1/jobs", headers=_auth(token), json=JOB_PAYLOAD)
            assert r.status_code == 403, f"Expected 403 for recruiter without company, got {r.status_code}: {r.text}"


# ---------------------------------------------------------------------------
# Test 5 — Full cross-company IDOR protection matrix
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_cross_company_idor_protection():
    """Recruiter A must be denied all access to Recruiter B's jobs and company."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]

            email_a = f"rec_a_{suffix}@co-alpha.com"
            email_b = f"rec_b_{suffix}@co-beta.com"

            # Register and set roles
            await _register_and_promote(client, email_a, pwd, UserRole.RECRUITER)
            await _register_and_promote(client, email_b, pwd, UserRole.RECRUITER)

            token_a = await _login(client, email_a, pwd)
            token_b = await _login(client, email_b, pwd)
            ha = _auth(token_a)
            hb = _auth(token_b)

            # Create Company A (auto-associates recruiter A)
            comp_a = await client.post("/api/v1/companies", json={
                "name": f"Alpha Corp {suffix}",
                "description": "Alpha company",
            }, headers=ha)
            assert comp_a.status_code == 201, f"Company A creation failed: {comp_a.text}"
            comp_a_id = comp_a.json()["id"]

            # Create Company B (auto-associates recruiter B)
            comp_b = await client.post("/api/v1/companies", json={
                "name": f"Beta Corp {suffix}",
                "description": "Beta company",
            }, headers=hb)
            assert comp_b.status_code == 201, f"Company B creation failed: {comp_b.text}"
            comp_b_id = comp_b.json()["id"]

            # Recruiter A creates Job A
            job_a_res = await client.post("/api/v1/jobs", headers=ha, json=JOB_PAYLOAD)
            assert job_a_res.status_code == 201, f"Job A creation failed: {job_a_res.text}"
            job_a = job_a_res.json()
            job_a_id = job_a["id"]
            assert job_a["company_id"] == comp_a_id, "Job A must be owned by Company A"
            assert job_a["status"] == "DRAFT"

            # Recruiter B creates Job B
            job_b_res = await client.post("/api/v1/jobs", headers=hb, json={**JOB_PAYLOAD, "title": "Beta Role"})
            assert job_b_res.status_code == 201, f"Job B creation failed: {job_b_res.text}"
            job_b_id = job_b_res.json()["id"]

            # ---------------------------------------------------------------
            # Cross-company job write denials (Recruiter A → Job B)
            # ---------------------------------------------------------------
            r = await client.patch(f"/api/v1/jobs/{job_b_id}", headers=ha, json={"title": "Hacked"})
            assert r.status_code == 403, f"PATCH Job B by A should be 403, got {r.status_code}"

            r = await client.post(f"/api/v1/jobs/{job_b_id}/publish", headers=ha)
            assert r.status_code == 403, f"Publish Job B by A should be 403, got {r.status_code}"

            r = await client.post(f"/api/v1/jobs/{job_b_id}/unpublish", headers=ha)
            assert r.status_code == 403, f"Unpublish Job B by A should be 403, got {r.status_code}"

            r = await client.post(f"/api/v1/jobs/{job_b_id}/close", headers=ha)
            assert r.status_code == 403, f"Close Job B by A should be 403, got {r.status_code}"

            r = await client.delete(f"/api/v1/jobs/{job_b_id}", headers=ha)
            assert r.status_code == 403, f"Delete Job B by A should be 403, got {r.status_code}"

            # ---------------------------------------------------------------
            # Cross-company company write denials (Recruiter A → Company B)
            # ---------------------------------------------------------------
            r = await client.patch(f"/api/v1/companies/{comp_b_id}", headers=ha, json={"location": "Hacked"})
            assert r.status_code == 403, f"PATCH Company B by A should be 403, got {r.status_code}"

            r = await client.delete(f"/api/v1/companies/{comp_b_id}", headers=ha)
            assert r.status_code == 403, f"DELETE Company B by A should be 403, got {r.status_code}"

            # ---------------------------------------------------------------
            # Own-company operations succeed
            # ---------------------------------------------------------------
            r = await client.patch(f"/api/v1/jobs/{job_a_id}", headers=ha, json={"title": "Alpha Updated Role"})
            assert r.status_code == 200, f"Recruiter A PATCH own job failed: {r.text}"

            r = await client.get("/api/v1/companies/me", headers=ha)
            assert r.status_code == 200
            assert r.json()["id"] == comp_a_id

            r = await client.patch("/api/v1/companies/me", headers=ha, json={"location": "Bangalore"})
            assert r.status_code == 200


# ---------------------------------------------------------------------------
# Test 6 — Job lifecycle authorization
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_job_lifecycle_authorization():
    """Verify DRAFT→PUBLISHED→DRAFT→PUBLISHED→CLOSED lifecycle rules and invalid transitions."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            email = f"rec_lifecycle_{suffix}@lifecycle.com"

            await _register_and_promote(client, email, pwd, UserRole.RECRUITER)
            token = await _login(client, email, pwd)
            ha = _auth(token)

            # Create company (auto-associates)
            comp = await client.post("/api/v1/companies", json={
                "name": f"Lifecycle Corp {suffix}",
                "description": "Lifecycle test",
            }, headers=ha)
            assert comp.status_code == 201

            # Create job
            job = await client.post("/api/v1/jobs", headers=ha, json=JOB_PAYLOAD)
            assert job.status_code == 201
            jid = job.json()["id"]

            # DRAFT → PUBLISHED
            r = await client.post(f"/api/v1/jobs/{jid}/publish", headers=ha)
            assert r.status_code == 200 and r.json()["status"] == "PUBLISHED"

            # PUBLISHED → PUBLISHED (invalid)
            r = await client.post(f"/api/v1/jobs/{jid}/publish", headers=ha)
            assert r.status_code == 400, f"Re-publish should be 400, got {r.status_code}"

            # PUBLISHED → DRAFT
            r = await client.post(f"/api/v1/jobs/{jid}/unpublish", headers=ha)
            assert r.status_code == 200 and r.json()["status"] == "DRAFT"

            # DRAFT → CLOSED (invalid — must publish first)
            r = await client.post(f"/api/v1/jobs/{jid}/close", headers=ha)
            assert r.status_code == 400, f"Close from DRAFT should be 400, got {r.status_code}"

            # DRAFT → PUBLISHED → CLOSED
            await client.post(f"/api/v1/jobs/{jid}/publish", headers=ha)
            r = await client.post(f"/api/v1/jobs/{jid}/close", headers=ha)
            assert r.status_code == 200 and r.json()["status"] == "CLOSED"

            # CLOSED → PUBLISHED (invalid)
            r = await client.post(f"/api/v1/jobs/{jid}/publish", headers=ha)
            assert r.status_code == 400, f"Re-publish closed job should be 400, got {r.status_code}"

            # CLOSED → DRAFT (invalid)
            r = await client.post(f"/api/v1/jobs/{jid}/unpublish", headers=ha)
            assert r.status_code == 400, f"Unpublish closed job should be 400, got {r.status_code}"


# ---------------------------------------------------------------------------
# Test 7 — Public search visibility (status filtering)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_public_search_only_shows_published_jobs():
    """Public GET /api/v1/jobs must only surface PUBLISHED, non-deleted jobs."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            email = f"rec_search_{suffix}@search.com"

            await _register_and_promote(client, email, pwd, UserRole.RECRUITER)
            token = await _login(client, email, pwd)
            ha = _auth(token)

            # Create company
            comp = await client.post("/api/v1/companies", json={
                "name": f"Search Corp {suffix}",
                "description": "Search test",
            }, headers=ha)
            assert comp.status_code == 201

            unique_kw = f"UNIQUESECTEST{suffix}"

            # Job A — stays DRAFT
            ja = await client.post("/api/v1/jobs", headers=ha, json={
                **JOB_PAYLOAD, "title": f"Draft Job {unique_kw}"
            })
            assert ja.status_code == 201
            jid_draft = ja.json()["id"]

            # Job B — published then unpublished (back to DRAFT)
            jb = await client.post("/api/v1/jobs", headers=ha, json={
                **JOB_PAYLOAD, "title": f"Unpublished Job {unique_kw}"
            })
            assert jb.status_code == 201
            jid_unpub = jb.json()["id"]
            await client.post(f"/api/v1/jobs/{jid_unpub}/publish", headers=ha)
            await client.post(f"/api/v1/jobs/{jid_unpub}/unpublish", headers=ha)

            # Job C — published then closed
            jc = await client.post("/api/v1/jobs", headers=ha, json={
                **JOB_PAYLOAD, "title": f"Closed Job {unique_kw}"
            })
            assert jc.status_code == 201
            jid_closed = jc.json()["id"]
            await client.post(f"/api/v1/jobs/{jid_closed}/publish", headers=ha)
            await client.post(f"/api/v1/jobs/{jid_closed}/close", headers=ha)

            # Job D — soft-deleted
            jd = await client.post("/api/v1/jobs", headers=ha, json={
                **JOB_PAYLOAD, "title": f"Deleted Job {unique_kw}"
            })
            assert jd.status_code == 201
            jid_deleted = jd.json()["id"]
            await client.delete(f"/api/v1/jobs/{jid_deleted}", headers=ha)

            # Job E — PUBLISHED and visible
            je = await client.post("/api/v1/jobs", headers=ha, json={
                **JOB_PAYLOAD, "title": f"Published Job {unique_kw}"
            })
            assert je.status_code == 201
            jid_pub = je.json()["id"]
            await client.post(f"/api/v1/jobs/{jid_pub}/publish", headers=ha)

            # Public search (no auth, using unique keyword to narrow results)
            search = await client.get(f"/api/v1/jobs?q={unique_kw}&size=100")
            assert search.status_code == 200
            items = search.json()["items"]
            found_ids = {item["id"] for item in items}

            assert jid_pub in found_ids, "PUBLISHED job must appear in public search"
            assert jid_draft not in found_ids, "DRAFT job must NOT appear in public search"
            assert jid_unpub not in found_ids, "Unpublished (DRAFT) job must NOT appear in public search"
            assert jid_closed not in found_ids, "CLOSED job must NOT appear in public search"
            assert jid_deleted not in found_ids, "Soft-deleted job must NOT appear in public search"

            # Verify all returned jobs have PUBLISHED status
            for item in items:
                assert item["status"] == "PUBLISHED", (
                    f"Public search returned non-PUBLISHED job: {item['id']} status={item['status']}"
                )


# ---------------------------------------------------------------------------
# Test 8 — Soft-deleted job cannot be modified or republished
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_soft_deleted_job_cannot_be_modified():
    """A soft-deleted job must be treated as not found (404) for all operations."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            email = f"rec_del_{suffix}@deleted.com"

            await _register_and_promote(client, email, pwd, UserRole.RECRUITER)
            token = await _login(client, email, pwd)
            ha = _auth(token)

            comp = await client.post("/api/v1/companies", json={
                "name": f"Del Corp {suffix}", "description": "del test"
            }, headers=ha)
            assert comp.status_code == 201

            job = await client.post("/api/v1/jobs", headers=ha, json=JOB_PAYLOAD)
            assert job.status_code == 201
            jid = job.json()["id"]

            # Soft delete the job
            r = await client.delete(f"/api/v1/jobs/{jid}", headers=ha)
            assert r.status_code == 204

            # All subsequent operations must return 404 (deleted job not found)
            r = await client.get(f"/api/v1/jobs/{jid}")
            assert r.status_code == 404, f"Soft-deleted job GET should 404, got {r.status_code}"

            r = await client.patch(f"/api/v1/jobs/{jid}", headers=ha, json={"title": "Ghost Update"})
            assert r.status_code == 404, f"PATCH soft-deleted job should 404, got {r.status_code}"

            r = await client.post(f"/api/v1/jobs/{jid}/publish", headers=ha)
            assert r.status_code == 404, f"Publish soft-deleted job should 404, got {r.status_code}"

            r = await client.delete(f"/api/v1/jobs/{jid}", headers=ha)
            assert r.status_code == 404, f"Re-delete soft-deleted job should 404, got {r.status_code}"


# ---------------------------------------------------------------------------
# Test 9 — Public GET /api/v1/jobs is accessible without auth
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_public_search_no_auth_required():
    """Public job search endpoint must work without any Authorization header."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        r = await client.get("/api/v1/jobs")
        assert r.status_code == 200
        data = r.json()
        assert "items" in data
        assert "total" in data


# ---------------------------------------------------------------------------
# Test 10 — Payload validation (422)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_invalid_job_payload_returns_422():
    """Job creation with missing required fields must return 422."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            email = f"rec_422_{suffix}@val.com"

            await _register_and_promote(client, email, pwd, UserRole.RECRUITER)
            token = await _login(client, email, pwd)

            # Create company so authorization passes (reaches validation)
            await client.post("/api/v1/companies", json={
                "name": f"Val Corp {suffix}", "description": "validation test"
            }, headers=_auth(token))

            # Missing required "title" and "description"
            r = await client.post("/api/v1/jobs", headers=_auth(token), json={
                "work_mode": "REMOTE"
            })
            assert r.status_code == 422, f"Missing required fields should be 422, got {r.status_code}"

            # salary_min negative (ge=0 violated)
            r = await client.post("/api/v1/jobs", headers=_auth(token), json={
                **JOB_PAYLOAD, "salary_min": -1
            })
            assert r.status_code == 422, f"Negative salary should be 422, got {r.status_code}"
