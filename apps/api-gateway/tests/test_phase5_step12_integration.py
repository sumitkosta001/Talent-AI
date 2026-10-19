"""Phase 5 Step 12: Full Backend Integration Test Suite.

Verifies end-to-end correctness of the complete backend after Steps 1–11:
1. Authentication & authorization — valid/invalid tokens, roles, recruiter-company.
2. Company management — create, read, update, delete, ownership enforcement.
3. Job management — CRUD, validation, publishing, unpublishing, closing, soft-delete.
4. Public job search — published-only, filters, sorting, pagination, empty results.
5. Candidate job browsing — list, details, missing/invalid job IDs.
6. Phase 4 ML compatibility — ATS scoring, similarity, recommendations, interview Qs.
7. Database integrity — relationships, required fields, transaction isolation.

Uses unittest.mock to suppress real email delivery.
"""

import uuid
import pytest
from unittest.mock import patch, AsyncMock
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select

from app.main import app
from app.database.session import SessionLocal
from app.models.enums import UserRole, JobStatus, WorkMode, ResumeStatus
from app.models.user import User
from app.models.company import Company
from app.models.job import Job
from app.models.candidate_profile import CandidateProfile
from app.models.resume import Resume
from app.services.resume_processing.models import (
    JobRequirements,
    StructuredResume,
    ExtractedSkills,
    ExtractedSkill,
    ExtractedEducation,
    EducationRecord,
    ExtractedExperience,
    ExperienceRecord,
    ExtractedProjects,
    ProjectRecord,
    ResumeClassification,
)
from app.services.resume_processing import (
    calculate_ats_score,
    calculate_similarity_match,
    generate_interview_questions,
    QuestionDifficulty,
)
from app.auth.jwt import create_access_token


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

JOB_PAYLOAD = {
    "title": "Step12 Integration Engineer",
    "description": "Full-stack engineer for integration testing the entire Phase 5 pipeline.",
    "work_mode": "REMOTE",
    "salary_min": 1000000,
    "salary_max": 2000000,
    "currency": "INR",
    "required_skills": ["Python", "FastAPI", "PostgreSQL"],
    "preferred_skills": ["Docker", "Redis"],
    "required_experience_months": 24,
    "education_requirements": ["Bachelor's in Computer Science"],
    "required_keywords": ["backend", "microservices"],
}


async def _register_and_promote(client: AsyncClient, email: str, pwd: str, role: UserRole) -> dict:
    """Register a user and immediately set their role and verification in DB."""
    res = await client.post("/api/v1/auth/register", json={
        "email": email,
        "password": pwd,
        "confirm_password": pwd,
        "first_name": "Test",
        "last_name": "User",
    })
    assert res.status_code == 201, f"Registration failed for {email}: {res.text}"
    user_id = uuid.UUID(res.json()["user"]["id"])

    async with SessionLocal() as db:
        user = (await db.execute(select(User).where(User.id == user_id))).scalar_one()
        user.role = role
        user.is_verified = True
        await db.commit()

    return {"id": user_id, "email": email}


async def _login(client: AsyncClient, email: str, pwd: str) -> str:
    """Login and return access token."""
    res = await client.post("/api/v1/auth/login", json={"email": email, "password": pwd})
    assert res.status_code == 200, f"Login failed: {res.text}"
    return res.json()["tokens"]["access_token"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _create_structured_resume(resume_uuid: uuid.UUID, candidate_uuid: uuid.UUID) -> StructuredResume:
    """Build a realistic structured resume for ML testing."""
    return StructuredResume(
        resume_id=str(resume_uuid),
        candidate_profile_id=str(candidate_uuid),
        full_name="Test Engineer",
        email="test@example.com",
        skills=ExtractedSkills(
            skills=[
                ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
                ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
                ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL"),
            ],
            total_count=3,
        ),
        education=ExtractedEducation(
            educations=[
                EducationRecord(
                    degree="Bachelor of Technology in Computer Science",
                    normalized_degree="bachelor_of_technology",
                    degree_level="UNDERGRADUATE",
                    field_of_study="Computer Science",
                    institution="NIT",
                    graduation_year=2024,
                )
            ],
            total_count=1,
        ),
        experience=ExtractedExperience(
            experiences=[
                ExperienceRecord(
                    company="TechCorp",
                    job_title="Backend Engineer",
                    duration_months=24,
                    seniority="MID",
                    responsibilities=["Built REST APIs using FastAPI and PostgreSQL."],
                )
            ],
            total_experience_months=24,
        ),
        projects=ExtractedProjects(
            projects=[
                ProjectRecord(
                    name="API Platform",
                    description="Microservices platform built with FastAPI and PostgreSQL.",
                    technologies=["Python", "FastAPI", "PostgreSQL"],
                )
            ],
            total_count=1,
        ),
        classification=ResumeClassification(
            domain="SOFTWARE_ENGINEERING",
            role="BACKEND_DEVELOPER",
            experience_level="MID",
        ),
    )


# ===========================================================================
# AREA 1: Authentication & Authorization
# ===========================================================================

@pytest.mark.asyncio
async def test_auth_unauthenticated_returns_401():
    """Protected endpoints reject missing tokens with 401."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        dummy_id = str(uuid.uuid4())
        cases = [
            ("POST", "/api/v1/jobs"),
            ("GET", "/api/v1/jobs/company/me"),
            ("PATCH", f"/api/v1/jobs/{dummy_id}"),
            ("DELETE", f"/api/v1/jobs/{dummy_id}"),
            ("POST", f"/api/v1/jobs/{dummy_id}/publish"),
            ("POST", "/api/v1/companies"),
        ]
        for method, url in cases:
            r = await client.request(method, url, json=JOB_PAYLOAD)
            assert r.status_code == 401, f"Unauthenticated {method} {url}: {r.status_code}"


@pytest.mark.asyncio
async def test_auth_invalid_token_returns_401():
    """Malformed tokens return 401."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        bad_headers = {"Authorization": "Bearer totally.invalid.token"}
        r = await client.post("/api/v1/jobs", headers=bad_headers, json=JOB_PAYLOAD)
        assert r.status_code == 401


@pytest.mark.asyncio
async def test_auth_candidate_denied_recruiter_ops():
    """Candidate role receives 403 on all recruiter-only endpoints."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            email = f"cand_s12_{uuid.uuid4().hex[:6]}@test.com"
            await _register_and_promote(client, email, pwd, UserRole.CANDIDATE)
            token = await _login(client, email, pwd)
            hdrs = _auth(token)

            recruiter_ops = [
                ("POST", "/api/v1/jobs", JOB_PAYLOAD),
                ("GET", "/api/v1/jobs/company/me", None),
            ]
            for method, url, body in recruiter_ops:
                r = await client.request(method, url, headers=hdrs, json=body)
                assert r.status_code == 403, f"Candidate {method} {url}: {r.status_code}"


# ===========================================================================
# AREA 2: Company Management
# ===========================================================================

@pytest.mark.asyncio
async def test_company_crud_and_ownership():
    """Full company lifecycle: create, read, update, delete with ownership checks."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]

            # Recruiter A creates company A
            rec_a_email = f"rec_a_{suffix}@test.com"
            await _register_and_promote(client, rec_a_email, pwd, UserRole.RECRUITER)
            token_a = await _login(client, rec_a_email, pwd)
            auth_a = _auth(token_a)

            comp_res = await client.post("/api/v1/companies", json={
                "name": f"Company A {suffix}",
                "description": "Test company A",
                "industry": "Technology",
            }, headers=auth_a)
            assert comp_res.status_code == 201, f"Company create: {comp_res.text}"
            comp_a_id = comp_res.json()["id"]

            # Read company
            get_res = await client.get(f"/api/v1/companies/{comp_a_id}")
            assert get_res.status_code == 200
            assert get_res.json()["name"] == f"Company A {suffix}"

            # Update company
            patch_res = await client.patch(f"/api/v1/companies/{comp_a_id}", json={
                "description": "Updated description"
            }, headers=auth_a)
            assert patch_res.status_code == 200
            assert patch_res.json()["description"] == "Updated description"

            # Recruiter B cannot update company A (cross-company IDOR)
            rec_b_email = f"rec_b_{suffix}@test.com"
            await _register_and_promote(client, rec_b_email, pwd, UserRole.RECRUITER)
            token_b = await _login(client, rec_b_email, pwd)
            auth_b = _auth(token_b)

            # Create company B for recruiter B
            comp_b_res = await client.post("/api/v1/companies", json={
                "name": f"Company B {suffix}",
                "description": "Test company B",
            }, headers=auth_b)
            assert comp_b_res.status_code == 201

            # B tries to update A — should be 403
            cross_patch = await client.patch(f"/api/v1/companies/{comp_a_id}", json={
                "description": "Hacked by B"
            }, headers=auth_b)
            assert cross_patch.status_code == 403, f"Cross-company PATCH: {cross_patch.status_code}"

            # B tries to delete A — should be 403
            cross_del = await client.delete(f"/api/v1/companies/{comp_a_id}", headers=auth_b)
            assert cross_del.status_code == 403, f"Cross-company DELETE: {cross_del.status_code}"

            # A deletes own company — should work
            del_res = await client.delete(f"/api/v1/companies/{comp_a_id}", headers=auth_a)
            assert del_res.status_code == 204


# ===========================================================================
# AREA 3: Job Management (CRUD + Lifecycle)
# ===========================================================================

@pytest.mark.asyncio
async def test_job_crud_and_lifecycle():
    """Full job lifecycle: create draft, update, publish, unpublish, close, delete."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            rec_email = f"rec_job_{suffix}@test.com"
            await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            token = await _login(client, rec_email, pwd)
            auth = _auth(token)

            # Create company
            comp = await client.post("/api/v1/companies", json={
                "name": f"JobCo {suffix}", "description": "Jobs testing"
            }, headers=auth)
            assert comp.status_code == 201

            # 1. CREATE job (DRAFT)
            job_res = await client.post("/api/v1/jobs", json=JOB_PAYLOAD, headers=auth)
            assert job_res.status_code == 201, f"Job create: {job_res.text}"
            job_data = job_res.json()
            job_id = job_data["id"]
            assert job_data["status"] == "DRAFT"
            assert job_data["title"] == JOB_PAYLOAD["title"]
            assert job_data["required_skills"] == JOB_PAYLOAD["required_skills"]

            # 2. READ job by ID
            get_job = await client.get(f"/api/v1/jobs/{job_id}", headers=auth)
            assert get_job.status_code == 200
            assert get_job.json()["id"] == job_id

            # 3. UPDATE job
            patch_job = await client.patch(f"/api/v1/jobs/{job_id}", json={
                "title": "Updated Integration Engineer",
                "salary_min": 1200000,
            }, headers=auth)
            assert patch_job.status_code == 200
            assert patch_job.json()["title"] == "Updated Integration Engineer"
            assert patch_job.json()["salary_min"] == 1200000

            # 4. PUBLISH — DRAFT -> PUBLISHED
            pub_res = await client.post(f"/api/v1/jobs/{job_id}/publish", headers=auth)
            assert pub_res.status_code == 200
            assert pub_res.json()["status"] == "PUBLISHED"

            # 5. PUBLISH again — already published, should fail
            pub_again = await client.post(f"/api/v1/jobs/{job_id}/publish", headers=auth)
            assert pub_again.status_code == 400

            # 6. UNPUBLISH — PUBLISHED -> DRAFT
            unpub_res = await client.post(f"/api/v1/jobs/{job_id}/unpublish", headers=auth)
            assert unpub_res.status_code == 200
            assert unpub_res.json()["status"] == "DRAFT"

            # 7. UNPUBLISH again — already draft, should fail
            unpub_again = await client.post(f"/api/v1/jobs/{job_id}/unpublish", headers=auth)
            assert unpub_again.status_code == 400

            # 8. Re-publish and CLOSE — PUBLISHED -> CLOSED
            await client.post(f"/api/v1/jobs/{job_id}/publish", headers=auth)
            close_res = await client.post(f"/api/v1/jobs/{job_id}/close", headers=auth)
            assert close_res.status_code == 200
            assert close_res.json()["status"] == "CLOSED"

            # 9. CLOSE again — already closed
            close_again = await client.post(f"/api/v1/jobs/{job_id}/close", headers=auth)
            assert close_again.status_code == 400

            # 10. PUBLISH closed — should fail
            pub_closed = await client.post(f"/api/v1/jobs/{job_id}/publish", headers=auth)
            assert pub_closed.status_code == 400

            # 11. UNPUBLISH closed — should fail
            unpub_closed = await client.post(f"/api/v1/jobs/{job_id}/unpublish", headers=auth)
            assert unpub_closed.status_code == 400

            # 12. CLOSE draft — should fail (need publish first)
            draft_job = await client.post("/api/v1/jobs", json={
                "title": "Draft Only", "description": "Stays draft", "work_mode": "REMOTE",
                "required_skills": ["Python"],
            }, headers=auth)
            draft_id = draft_job.json()["id"]
            close_draft = await client.post(f"/api/v1/jobs/{draft_id}/close", headers=auth)
            assert close_draft.status_code == 400

            # 13. SOFT DELETE
            del_res = await client.delete(f"/api/v1/jobs/{draft_id}", headers=auth)
            assert del_res.status_code == 204

            # After soft-delete, GET should return 404
            get_deleted = await client.get(f"/api/v1/jobs/{draft_id}", headers=auth)
            assert get_deleted.status_code == 404


@pytest.mark.asyncio
async def test_job_validation():
    """Job creation rejects invalid payloads."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            rec_email = f"rec_val_{suffix}@test.com"
            await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            token = await _login(client, rec_email, pwd)
            auth = _auth(token)

            await client.post("/api/v1/companies", json={
                "name": f"ValCo {suffix}", "description": "Validation"
            }, headers=auth)

            # Missing required fields
            empty_res = await client.post("/api/v1/jobs", json={}, headers=auth)
            assert empty_res.status_code == 422

            # Missing description
            no_desc = await client.post("/api/v1/jobs", json={"title": "No Desc"}, headers=auth)
            assert no_desc.status_code == 422

            # Non-existent job ID for lifecycle ops
            fake_id = str(uuid.uuid4())
            r = await client.post(f"/api/v1/jobs/{fake_id}/publish", headers=auth)
            assert r.status_code == 404


@pytest.mark.asyncio
async def test_job_cross_company_idor():
    """Recruiter A cannot modify Recruiter B's jobs."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]

            # Recruiter A
            rec_a = f"rec_idor_a_{suffix}@test.com"
            await _register_and_promote(client, rec_a, pwd, UserRole.RECRUITER)
            token_a = await _login(client, rec_a, pwd)
            auth_a = _auth(token_a)
            await client.post("/api/v1/companies", json={
                "name": f"IDOR-A {suffix}", "description": "A"
            }, headers=auth_a)

            job_a = await client.post("/api/v1/jobs", json={
                "title": "A's Job", "description": "Belongs to A",
                "work_mode": "REMOTE", "required_skills": ["Python"],
            }, headers=auth_a)
            assert job_a.status_code == 201
            job_a_id = job_a.json()["id"]

            # Recruiter B
            rec_b = f"rec_idor_b_{suffix}@test.com"
            await _register_and_promote(client, rec_b, pwd, UserRole.RECRUITER)
            token_b = await _login(client, rec_b, pwd)
            auth_b = _auth(token_b)
            await client.post("/api/v1/companies", json={
                "name": f"IDOR-B {suffix}", "description": "B"
            }, headers=auth_b)

            # B tries to modify A's job
            patch_r = await client.patch(f"/api/v1/jobs/{job_a_id}", json={"title": "Hacked"}, headers=auth_b)
            assert patch_r.status_code == 403

            del_r = await client.delete(f"/api/v1/jobs/{job_a_id}", headers=auth_b)
            assert del_r.status_code == 403

            pub_r = await client.post(f"/api/v1/jobs/{job_a_id}/publish", headers=auth_b)
            assert pub_r.status_code == 403


# ===========================================================================
# AREA 4: Public Job Search
# ===========================================================================

@pytest.mark.asyncio
async def test_public_search_published_only():
    """Public search returns ONLY published, non-deleted jobs."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            unique_keyword = f"SRCH{suffix}"

            rec_email = f"rec_srch_{suffix}@test.com"
            await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            token = await _login(client, rec_email, pwd)
            auth = _auth(token)

            await client.post("/api/v1/companies", json={
                "name": f"SearchCo {suffix}", "description": "Search test"
            }, headers=auth)

            # Job 1: PUBLISHED (should appear)
            j1 = await client.post("/api/v1/jobs", json={
                "title": f"Published Engineer {unique_keyword}",
                "description": f"Active job {unique_keyword}",
                "work_mode": "REMOTE", "required_skills": ["Python"],
            }, headers=auth)
            j1_id = j1.json()["id"]
            await client.post(f"/api/v1/jobs/{j1_id}/publish", headers=auth)

            # Job 2: DRAFT (should NOT appear)
            j2 = await client.post("/api/v1/jobs", json={
                "title": f"Draft Engineer {unique_keyword}",
                "description": f"Draft job {unique_keyword}",
                "work_mode": "REMOTE", "required_skills": ["Python"],
            }, headers=auth)
            j2_id = j2.json()["id"]

            # Job 3: CLOSED (should NOT appear)
            j3 = await client.post("/api/v1/jobs", json={
                "title": f"Closed Engineer {unique_keyword}",
                "description": f"Closed job {unique_keyword}",
                "work_mode": "REMOTE", "required_skills": ["Python"],
            }, headers=auth)
            j3_id = j3.json()["id"]
            await client.post(f"/api/v1/jobs/{j3_id}/publish", headers=auth)
            await client.post(f"/api/v1/jobs/{j3_id}/close", headers=auth)

            # Job 4: Soft-deleted (should NOT appear)
            j4 = await client.post("/api/v1/jobs", json={
                "title": f"Deleted Engineer {unique_keyword}",
                "description": f"Deleted job {unique_keyword}",
                "work_mode": "REMOTE", "required_skills": ["Python"],
            }, headers=auth)
            j4_id = j4.json()["id"]
            await client.post(f"/api/v1/jobs/{j4_id}/publish", headers=auth)
            await client.delete(f"/api/v1/jobs/{j4_id}", headers=auth)

            # Search using unique keyword
            search_res = await client.get(f"/api/v1/jobs?q={unique_keyword}&size=50")
            assert search_res.status_code == 200
            data = search_res.json()
            found_ids = {j["id"] for j in data["items"]}

            assert j1_id in found_ids, "Published job must appear in search"
            assert j2_id not in found_ids, "Draft job must NOT appear in search"
            assert j3_id not in found_ids, "Closed job must NOT appear in search"
            assert j4_id not in found_ids, "Deleted job must NOT appear in search"


@pytest.mark.asyncio
async def test_public_search_empty_results():
    """Search with impossible query returns empty results."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        bogus_q = f"impossible_query_{uuid.uuid4().hex}"
        res = await client.get(f"/api/v1/jobs?q={bogus_q}")
        assert res.status_code == 200
        assert res.json()["total"] == 0
        assert res.json()["items"] == []


@pytest.mark.asyncio
async def test_public_search_pagination():
    """Search supports pagination parameters."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        res = await client.get("/api/v1/jobs?page=1&size=1")
        assert res.status_code == 200
        data = res.json()
        assert data["page"] == 1
        assert data["size"] == 1
        assert len(data["items"]) <= 1


@pytest.mark.asyncio
async def test_public_search_work_mode_validation_and_filters():
    """Verify accepted values (remote, hybrid, onsite), invalid values (422), and combined filters."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        # 1. Accepted work_mode values return 200
        for mode in ["remote", "hybrid", "onsite"]:
            res = await client.get(f"/api/v1/jobs?work_mode={mode}")
            assert res.status_code == 200, f"Expected 200 for work_mode={mode}, got {res.status_code}"
            data = res.json()
            assert "items" in data
            for item in data["items"]:
                # Serialization returns uppercase enum name
                assert item["work_mode"] == mode.upper()

        # 2. Invalid work_mode values return 422 Unprocessable Entity
        for invalid_mode in ["REMOTE", "invalid", "telecommute", "123", "Any"]:
            res = await client.get(f"/api/v1/jobs?work_mode={invalid_mode}")
            assert res.status_code == 422, f"Expected 422 for invalid work_mode={invalid_mode}, got {res.status_code}"

        # 3. Combined query filters work cleanly with work_mode
        combined_res = await client.get(
            "/api/v1/jobs?work_mode=remote&q=Engineer&location=Remote&experience_months=36&salary_min=100000&sort_by=published_at&sort_order=desc&page=1&size=5"
        )
        assert combined_res.status_code == 200, f"Expected 200 for combined filters, got {combined_res.status_code}"
        combined_data = combined_res.json()
        assert "items" in combined_data
        assert combined_data["page"] == 1
        assert combined_data["size"] == 5


# ===========================================================================
# AREA 5: Candidate Job Browsing
# ===========================================================================

@pytest.mark.asyncio
async def test_candidate_public_search_and_details():
    """Candidate can browse public jobs and view job details."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]

            # Create a published job
            rec_email = f"rec_browse_{suffix}@test.com"
            await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            rec_token = await _login(client, rec_email, pwd)
            rec_auth = _auth(rec_token)

            await client.post("/api/v1/companies", json={
                "name": f"BrowseCo {suffix}", "description": "Browse test"
            }, headers=rec_auth)

            job_res = await client.post("/api/v1/jobs", json={
                "title": f"Browse Test Job {suffix}",
                "description": "Job for candidate browsing test.",
                "work_mode": "REMOTE", "required_skills": ["Python"],
            }, headers=rec_auth)
            job_id = job_res.json()["id"]
            await client.post(f"/api/v1/jobs/{job_id}/publish", headers=rec_auth)

            # Candidate browses public job list (no auth needed)
            search_res = await client.get(f"/api/v1/jobs?q=Browse Test Job {suffix}")
            assert search_res.status_code == 200
            assert search_res.json()["total"] >= 1

            # Candidate views job details
            detail_res = await client.get(f"/api/v1/jobs/{job_id}")
            assert detail_res.status_code == 200
            assert detail_res.json()["id"] == job_id
            assert detail_res.json()["title"] == f"Browse Test Job {suffix}"


@pytest.mark.asyncio
async def test_candidate_invalid_job_id():
    """Request for non-existent job ID returns 404."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        fake_id = str(uuid.uuid4())
        r = await client.get(f"/api/v1/jobs/{fake_id}")
        assert r.status_code == 404


@pytest.mark.asyncio
async def test_candidate_malformed_job_id():
    """Request with malformed UUID returns 422."""
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        r = await client.get("/api/v1/jobs/not-a-uuid")
        assert r.status_code == 422


# ===========================================================================
# AREA 6: Phase 4 ML Compatibility (Unit-level, no DB)
# ===========================================================================

def test_job_to_job_requirements_bridge():
    """Job.to_job_requirements() produces valid JobRequirements."""
    job = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="ML Compat Engineer",
        description="Testing ML bridge compatibility.",
        department="Engineering",
        status=JobStatus.PUBLISHED,
        work_mode=WorkMode.REMOTE,
        location="Remote",
        salary_min=1000000,
        salary_max=2000000,
        currency="INR",
        required_skills=["Python", "FastAPI"],
        preferred_skills=["Docker"],
        required_experience_months=24,
        education_requirements=["Bachelor's in CS"],
        required_keywords=["backend"],
    )

    req = job.to_job_requirements()
    assert isinstance(req, JobRequirements)
    assert req.title == "ML Compat Engineer"
    assert req.required_skills == ["Python", "FastAPI"]
    assert req.preferred_skills == ["Docker"]
    assert req.required_experience_months == 24
    assert req.required_education == ["Bachelor's in CS"]
    assert req.required_keywords == ["backend"]
    assert req.metadata["status"] == "published"
    assert req.metadata["work_mode"] == "remote"
    assert req.metadata["salary_min"] == 1000000


def test_ml_ats_scoring_with_job_bridge():
    """ATS scoring works with JobRequirements from Job.to_job_requirements()."""
    job = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="Python Backend Developer",
        description="Python, FastAPI, PostgreSQL required.",
        status=JobStatus.PUBLISHED,
        work_mode=WorkMode.REMOTE,
        required_skills=["Python", "FastAPI", "PostgreSQL"],
    )
    job_req = job.to_job_requirements()
    resume = _create_structured_resume(uuid.uuid4(), uuid.uuid4())

    ats = calculate_ats_score(resume, job_req)
    assert 0.0 <= ats.overall_score <= 100.0
    assert ats.overall_score >= 40.0
    assert "Python" in ats.matched_required_skills


def test_ml_similarity_with_job_bridge():
    """Similarity scoring works with JobRequirements from Job.to_job_requirements()."""
    job = Job(
        id=uuid.uuid4(),
        company_id=uuid.uuid4(),
        title="Python Backend Developer",
        description="Python, FastAPI, PostgreSQL required.",
        status=JobStatus.PUBLISHED,
        work_mode=WorkMode.REMOTE,
        required_skills=["Python", "FastAPI"],
    )
    job_req = job.to_job_requirements()
    resume = _create_structured_resume(uuid.uuid4(), uuid.uuid4())

    sim = calculate_similarity_match(resume, job_req)
    assert 0.0 <= sim.match_score <= 100.0


def test_ml_interview_questions():
    """Interview question generation works with structured resume."""
    resume = _create_structured_resume(uuid.uuid4(), uuid.uuid4())
    iq = generate_interview_questions(resume, count=3, difficulty=QuestionDifficulty.MEDIUM)
    assert len(iq.questions) == 3
    for q in iq.questions:
        assert q.question is not None
        assert len(q.question) > 0


# ===========================================================================
# AREA 6b: ML via HTTP endpoints
# ===========================================================================

@pytest.mark.asyncio
async def test_ml_http_ats_and_similarity_endpoints():
    """ATS score and similarity endpoints work with relational job requirements."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]

            # Register candidate
            cand_email = f"cand_ml_{suffix}@test.com"
            cand = await _register_and_promote(client, cand_email, pwd, UserRole.CANDIDATE)
            cand_id = cand["id"]
            cand_token = await _login(client, cand_email, pwd)
            cand_auth = _auth(cand_token)

            # Create resume in DB
            resume_uuid = uuid.uuid4()
            structured_data = _create_structured_resume(resume_uuid, cand_id)

            async with SessionLocal() as db:
                profile_res = await db.execute(select(CandidateProfile).where(CandidateProfile.user_id == cand_id))
                profile = profile_res.scalar_one_or_none()
                if not profile:
                    profile = CandidateProfile(user_id=cand_id, profile_completion_percentage=80)
                    db.add(profile)
                    await db.flush()

                resume = Resume(
                    id=resume_uuid,
                    candidate_profile_id=profile.id,
                    original_filename="test_resume.pdf",
                    stored_filename=f"{resume_uuid}.pdf",
                    mime_type="application/pdf",
                    file_extension=".pdf",
                    file_size_bytes=2048,
                    status=ResumeStatus.PROCESSED,
                    version=1,
                    is_current=True,
                    structured_data=structured_data.model_dump(),
                    created_by=cand_id,
                    updated_by=cand_id,
                )
                db.add(resume)
                await db.commit()

            # Create a relational job via recruiter
            rec_email = f"rec_ml2_{suffix}@test.com"
            await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            rec_token = await _login(client, rec_email, pwd)
            rec_auth = _auth(rec_token)

            await client.post("/api/v1/companies", json={
                "name": f"ML2 Corp {suffix}", "description": "ML test"
            }, headers=rec_auth)

            job_res = await client.post("/api/v1/jobs", json={
                "title": "Python Engineer ML Test",
                "description": "Python FastAPI PostgreSQL engineer.",
                "work_mode": "REMOTE",
                "required_skills": ["Python", "FastAPI", "PostgreSQL"],
            }, headers=rec_auth)
            assert job_res.status_code == 201
            db_job_id = job_res.json()["id"]
            await client.post(f"/api/v1/jobs/{db_job_id}/publish", headers=rec_auth)

            # Get the job requirements payload
            async with SessionLocal() as db:
                db_job = (await db.execute(select(Job).where(Job.id == uuid.UUID(db_job_id)))).scalar_one()
                job_req_payload = db_job.to_job_requirements().model_dump()

            # ATS endpoint
            ats_res = await client.post(
                f"/api/v1/candidates/me/resumes/{resume_uuid}/ats-score",
                headers=cand_auth,
                json=job_req_payload,
            )
            assert ats_res.status_code == 200, f"ATS: {ats_res.text}"
            assert 0.0 <= ats_res.json()["score"] <= 100.0

            # Similarity endpoint
            sim_res = await client.post(
                f"/api/v1/candidates/me/resumes/{resume_uuid}/similarity-score",
                headers=cand_auth,
                json=job_req_payload,
            )
            assert sim_res.status_code == 200, f"Similarity: {sim_res.text}"
            assert 0.0 <= sim_res.json()["similarity_score"] <= 100.0

            # Interview questions endpoint
            iq_res = await client.post(
                f"/api/v1/candidates/me/resumes/{resume_uuid}/interview-questions?count=3&difficulty=MEDIUM",
                headers=cand_auth,
            )
            assert iq_res.status_code == 200, f"IQ: {iq_res.text}"
            assert len(iq_res.json()["questions"]) == 3


# ===========================================================================
# AREA 7: Database Integrity
# ===========================================================================

@pytest.mark.asyncio
async def test_db_job_company_relationship():
    """Job correctly references its parent company via company_id FK."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            rec_email = f"rec_fk_{suffix}@test.com"
            await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            token = await _login(client, rec_email, pwd)
            auth = _auth(token)

            comp_res = await client.post("/api/v1/companies", json={
                "name": f"FK Co {suffix}", "description": "FK test"
            }, headers=auth)
            comp_id = comp_res.json()["id"]

            job_res = await client.post("/api/v1/jobs", json={
                "title": "FK Test Job", "description": "Testing FK.",
                "work_mode": "REMOTE", "required_skills": ["Python"],
            }, headers=auth)
            job_id = job_res.json()["id"]

            # Verify FK in database
            async with SessionLocal() as db:
                job = (await db.execute(select(Job).where(Job.id == uuid.UUID(job_id)))).scalar_one()
                assert str(job.company_id) == comp_id
                assert job.recruiter_id is not None
                assert job.status == JobStatus.DRAFT
                assert job.is_deleted is False


@pytest.mark.asyncio
async def test_db_user_company_association():
    """Recruiter is auto-associated with company on creation."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            rec_email = f"rec_assoc_{suffix}@test.com"
            user_data = await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            token = await _login(client, rec_email, pwd)
            auth = _auth(token)

            # Before company creation: no company_id
            async with SessionLocal() as db:
                user = (await db.execute(select(User).where(User.id == user_data["id"]))).scalar_one()
                assert user.company_id is None

            # Create company
            comp_res = await client.post("/api/v1/companies", json={
                "name": f"Assoc Co {suffix}", "description": "Association test"
            }, headers=auth)
            assert comp_res.status_code == 201
            comp_id = comp_res.json()["id"]

            # After company creation: auto-associated
            async with SessionLocal() as db:
                user = (await db.execute(select(User).where(User.id == user_data["id"]))).scalar_one()
                assert str(user.company_id) == comp_id


@pytest.mark.asyncio
async def test_db_soft_delete_isolation():
    """Soft-deleted records are excluded from queries but remain in DB."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            rec_email = f"rec_soft_{suffix}@test.com"
            await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            token = await _login(client, rec_email, pwd)
            auth = _auth(token)

            await client.post("/api/v1/companies", json={
                "name": f"SoftDel Co {suffix}", "description": "Soft delete test"
            }, headers=auth)

            job_res = await client.post("/api/v1/jobs", json={
                "title": "Soft Delete Test", "description": "Will be soft deleted.",
                "work_mode": "REMOTE", "required_skills": ["Python"],
            }, headers=auth)
            job_id = job_res.json()["id"]

            # Delete the job
            del_res = await client.delete(f"/api/v1/jobs/{job_id}", headers=auth)
            assert del_res.status_code == 204

            # API returns 404
            get_res = await client.get(f"/api/v1/jobs/{job_id}")
            assert get_res.status_code == 404

            # But record still exists in DB with is_deleted=True
            async with SessionLocal() as db:
                job = (await db.execute(
                    select(Job).where(Job.id == uuid.UUID(job_id))
                )).scalar_one()
                assert job.is_deleted is True
                assert job.deleted_at is not None


@pytest.mark.asyncio
async def test_recruiter_company_me_jobs():
    """GET /jobs/company/me returns the recruiter's own company jobs (all statuses)."""
    with patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock):
        transport = ASGITransport(app=app, raise_app_exceptions=False)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            async with SessionLocal() as db:
                from sqlalchemy import text
                await db.execute(text("SELECT 1"))

            pwd = "Password123!"
            suffix = uuid.uuid4().hex[:6]
            rec_email = f"rec_me_{suffix}@test.com"
            await _register_and_promote(client, rec_email, pwd, UserRole.RECRUITER)
            token = await _login(client, rec_email, pwd)
            auth = _auth(token)

            await client.post("/api/v1/companies", json={
                "name": f"MeCo {suffix}", "description": "Me test"
            }, headers=auth)

            # Create 2 jobs
            for i in range(2):
                await client.post("/api/v1/jobs", json={
                    "title": f"Me Job {i} {suffix}",
                    "description": "Company me test",
                    "work_mode": "REMOTE",
                    "required_skills": ["Python"],
                }, headers=auth)

            # company/me returns them
            me_res = await client.get("/api/v1/jobs/company/me", headers=auth)
            assert me_res.status_code == 200
            data = me_res.json()
            assert data["total"] >= 2
            titles = [j["title"] for j in data["items"]]
            assert any(f"Me Job 0 {suffix}" in t for t in titles)
            assert any(f"Me Job 1 {suffix}" in t for t in titles)
