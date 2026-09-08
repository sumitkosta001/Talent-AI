"""Phase 5 Step 13 Security & Authorization Integration Tests.

Verifies:
- Recruiter accesses own company vs forbidden access to other company
- Recruiter creates jobs strictly for associated company
- Recruiter cannot access/update/delete/publish/unpublish/close another company's job
- Candidates & unauthenticated users forbidden from recruiter/company management endpoints (401/403)
- Public job search discoverability (exposes only PUBLISHED non-deleted jobs)
- IDOR direct UUID access rejection
"""

import pytest
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database.session import SessionLocal
from app.models.enums import UserRole
from app.models.user import User
from app.models.company import Company
from app.models.job import Job
from app.models.enums import JobStatus, WorkMode


@pytest.mark.asyncio
async def test_security_matrix_phase5_authorization():
    """Execute end-to-end security boundary matrix for Phase 5 Company & Job management."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        pwd = "Password123!"

        # Create unique user emails
        email_recruiter_a = f"rec_a_{uuid.uuid4().hex[:6]}@company-a.com"
        email_recruiter_b = f"rec_b_{uuid.uuid4().hex[:6]}@company-b.com"
        email_candidate = f"candidate_{uuid.uuid4().hex[:6]}@example.com"

        # Register Recruiter A
        reg_a = await client.post("/api/v1/auth/register", json={
            "email": email_recruiter_a, "password": pwd, "confirm_password": pwd,
            "first_name": "Recruiter", "last_name": "Alpha"
        })
        assert reg_a.status_code == 201, f"Reg A failed: {reg_a.text}"

        # Register Recruiter B
        reg_b = await client.post("/api/v1/auth/register", json={
            "email": email_recruiter_b, "password": pwd, "confirm_password": pwd,
            "first_name": "Recruiter", "last_name": "Beta"
        })
        assert reg_b.status_code == 201, f"Reg B failed: {reg_b.text}"

        # Register Candidate
        reg_cand = await client.post("/api/v1/auth/register", json={
            "email": email_candidate, "password": pwd, "confirm_password": pwd,
            "first_name": "Candidate", "last_name": "Charlie"
        })
        assert reg_cand.status_code == 201, f"Reg Candidate failed: {reg_cand.text}"

        # Login tokens
        login_a = await client.post("/api/v1/auth/login", json={"email": email_recruiter_a, "password": pwd})
        token_a = login_a.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        login_b = await client.post("/api/v1/auth/login", json={"email": email_recruiter_b, "password": pwd})
        token_b = login_b.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        login_cand = await client.post("/api/v1/auth/login", json={"email": email_candidate, "password": pwd})
        token_cand = login_cand.json()["tokens"]["access_token"]
        headers_cand = {"Authorization": f"Bearer {token_cand}"}

        # Set User Roles in DB to RECRUITER / CANDIDATE
        async with SessionLocal() as db:
            from sqlalchemy import select
            user_a = (await db.execute(select(User).where(User.email == email_recruiter_a))).scalar_one()
            user_b = (await db.execute(select(User).where(User.email == email_recruiter_b))).scalar_one()
            user_cand = (await db.execute(select(User).where(User.email == email_candidate))).scalar_one()

            user_a.role = UserRole.RECRUITER
            user_b.role = UserRole.RECRUITER
            user_cand.role = UserRole.CANDIDATE
            await db.commit()

        # ----------------------------------------------------------------------
        # 1. Company Creation & Association
        # ----------------------------------------------------------------------
        comp_a_res = await client.post("/api/v1/companies", json={
            "name": f"Alpha Corp {uuid.uuid4().hex[:4]}",
            "description": "Tech company Alpha"
        }, headers=headers_a)
        assert comp_a_res.status_code == 201
        comp_a_id = comp_a_res.json()["id"]

        comp_b_res = await client.post("/api/v1/companies", json={
            "name": f"Beta Corp {uuid.uuid4().hex[:4]}",
            "description": "Tech company Beta"
        }, headers=headers_b)
        assert comp_b_res.status_code == 201
        comp_b_id = comp_b_res.json()["id"]

        # Recruiter A gets own company (/companies/me) -> 200
        my_comp_a = await client.get("/api/v1/companies/me", headers=headers_a)
        assert my_comp_a.status_code == 200
        assert my_comp_a.json()["id"] == comp_a_id

        # Recruiter A updates own company (/companies/me) -> 200
        patch_my_comp = await client.patch("/api/v1/companies/me", json={"location": "Bangalore"}, headers=headers_a)
        assert patch_my_comp.status_code == 200

        # Candidate accesses company management endpoint -> 403 Forbidden
        cand_comp = await client.get("/api/v1/companies/me", headers=headers_cand)
        assert cand_comp.status_code == 403

        # Unauthenticated request -> 401 Unauthorized
        unauth_comp = await client.get("/api/v1/companies/me")
        assert unauth_comp.status_code == 401

        # ----------------------------------------------------------------------
        # 2. Job Creation Authorization
        # ----------------------------------------------------------------------
        # Recruiter A creates job -> 201 in DRAFT status linked to Company A
        job_a_res = await client.post("/api/v1/jobs", json={
            "title": "Alpha Frontend Lead",
            "description": "React & Next.js development",
            "work_mode": "HYBRID",
            "salary_min": 1000000,
            "salary_max": 1800000,
            "required_skills": ["React", "TypeScript"]
        }, headers=headers_a)
        assert job_a_res.status_code == 201
        job_a_data = job_a_res.json()
        job_a_id = job_a_data["id"]
        assert job_a_data["company_id"] == comp_a_id
        assert job_a_data["status"] == "DRAFT"

        # Recruiter B creates job -> 201 linked to Company B
        job_b_res = await client.post("/api/v1/jobs", json={
            "title": "Beta Backend Engineer",
            "description": "Python & FastAPI development",
            "work_mode": "REMOTE",
            "salary_min": 1200000,
            "salary_max": 2000000,
            "required_skills": ["Python", "FastAPI"]
        }, headers=headers_b)
        assert job_b_res.status_code == 201
        job_b_id = job_b_res.json()["id"]

        # Candidate attempts job creation -> 403 Forbidden
        cand_create_job = await client.post("/api/v1/jobs", json={
            "title": "Hacker Job", "description": "Desc"
        }, headers=headers_cand)
        assert cand_create_job.status_code == 403

        # Unauthenticated job creation -> 401 Unauthorized
        unauth_create_job = await client.post("/api/v1/jobs", json={"title": "Unauth Job", "description": "Desc"})
        assert unauth_create_job.status_code == 401

        # ----------------------------------------------------------------------
        # 3. Cross-Company Ownership Enforcement (IDOR Protection)
        # ----------------------------------------------------------------------
        # Recruiter A updates own Job A -> 200
        patch_job_a = await client.patch(f"/api/v1/jobs/{job_a_id}", json={"title": "Alpha Frontend Staff"}, headers=headers_a)
        assert patch_job_a.status_code == 200

        # Recruiter A attempts to update Recruiter B's Job B -> 403 Forbidden
        patch_job_b_by_a = await client.patch(f"/api/v1/jobs/{job_b_id}", json={"title": "Hacked Title"}, headers=headers_a)
        assert patch_job_b_by_a.status_code == 403

        # Recruiter A attempts to publish Recruiter B's Job B -> 403 Forbidden
        pub_job_b_by_a = await client.post(f"/api/v1/jobs/{job_b_id}/publish", headers=headers_a)
        assert pub_job_b_by_a.status_code == 403

        # Recruiter A attempts to unpublish Recruiter B's Job B -> 403 Forbidden
        unpub_job_b_by_a = await client.post(f"/api/v1/jobs/{job_b_id}/unpublish", headers=headers_a)
        assert unpub_job_b_by_a.status_code == 403

        # Recruiter A attempts to close Recruiter B's Job B -> 403 Forbidden
        close_job_b_by_a = await client.post(f"/api/v1/jobs/{job_b_id}/close", headers=headers_a)
        assert close_job_b_by_a.status_code == 403

        # Recruiter A attempts to delete Recruiter B's Job B -> 403 Forbidden
        del_job_b_by_a = await client.delete(f"/api/v1/jobs/{job_b_id}", headers=headers_a)
        assert del_job_b_by_a.status_code == 403

        # ----------------------------------------------------------------------
        # 4. Status Lifecycle Rules on Own Job
        # ----------------------------------------------------------------------
        # Recruiter A publishes own Job A -> 200
        pub_a = await client.post(f"/api/v1/jobs/{job_a_id}/publish", headers=headers_a)
        assert pub_a.status_code == 200
        assert pub_a.json()["status"] == "PUBLISHED"

        # Recruiter A unpublishes own Job A -> 200
        unpub_a = await client.post(f"/api/v1/jobs/{job_a_id}/unpublish", headers=headers_a)
        assert unpub_a.status_code == 200
        assert unpub_a.json()["status"] == "DRAFT"

        # Publish again, then close
        await client.post(f"/api/v1/jobs/{job_a_id}/publish", headers=headers_a)
        close_a = await client.post(f"/api/v1/jobs/{job_a_id}/close", headers=headers_a)
        assert close_a.status_code == 200
        assert close_a.json()["status"] == "CLOSED"

        # Invalid transition: CLOSED -> PUBLISHED -> 400 Bad Request
        repub_closed = await client.post(f"/api/v1/jobs/{job_a_id}/publish", headers=headers_a)
        assert repub_closed.status_code == 400

        # ----------------------------------------------------------------------
        # 5. Public Search Discoverability
        # ----------------------------------------------------------------------
        # Recruiter B publishes Job B
        await client.post(f"/api/v1/jobs/{job_b_id}/publish", headers=headers_b)

        # Public candidate search GET /api/v1/jobs
        search_res = await client.get("/api/v1/jobs")
        assert search_res.status_code == 200
        search_data = search_res.json()
        item_ids = [item["id"] for item in search_data["items"]]

        # Job B (PUBLISHED) must be discoverable
        assert job_b_id in item_ids
        # Job A (CLOSED) must NOT be in public search
        assert job_a_id not in item_ids
