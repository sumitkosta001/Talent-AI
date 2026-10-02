import asyncio
import uuid
import sys
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.enums import UserRole, JobStatus
from app.api.v1.auth import get_auth_service
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.database.dependencies import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.services.email_service import EmailService
from unittest.mock import AsyncMock, MagicMock

# Mock email service so tests never hit external network SMTP
class MockEmailService(EmailService):
    def __init__(self) -> None:
        pass

    async def send_verification_email(self, email: str, name: str, token: str, is_resend: bool = False) -> bool:
        return True

    async def send_resend_verification_email(self, email: str, name: str, token: str) -> bool:
        return True

def override_get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(
        user_repository=UserRepository(db),
        refresh_repository=RefreshTokenRepository(db),
        email_service=MockEmailService(),
    )

app.dependency_overrides[get_auth_service] = override_get_auth_service

async def run_tests():
    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        pwd = "Password123!"

        # ----------------------------------------------------
        # 1. Register Recruiter A with role='recruiter'
        # ----------------------------------------------------
        email_a = f"rec_a_{uuid.uuid4().hex[:6]}@techcorp.com"
        reg_a = await client.post("/api/v1/auth/register", json={
            "email": email_a,
            "password": pwd,
            "confirm_password": pwd,
            "first_name": "Alice",
            "last_name": "Recruiter",
            "role": "recruiter"
        })
        assert reg_a.status_code == 201, f"Register A failed: {reg_a.text}"
        assert reg_a.json()["user"]["role"] == "recruiter", f"Role mismatch: {reg_a.json()}"
        print("PASS 1: Recruiter A registered with role=recruiter", flush=True)

        # ----------------------------------------------------
        # 2. Login Recruiter A & Verify /auth/me
        # ----------------------------------------------------
        login_a = await client.post("/api/v1/auth/login", json={"email": email_a, "password": pwd})
        assert login_a.status_code == 200, f"Login A failed: {login_a.text}"
        token_a = login_a.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        me_a = await client.get("/api/v1/auth/me", headers=headers_a)
        assert me_a.status_code == 200
        assert me_a.json()["user"]["role"] == "recruiter"
        print("PASS 2: /auth/me verified recruiter role", flush=True)

        # ----------------------------------------------------
        # 3. Register Candidate & Verify Candidate Forbidden from Job Creation
        # ----------------------------------------------------
        email_cand = f"cand_{uuid.uuid4().hex[:6]}@gmail.com"
        reg_cand = await client.post("/api/v1/auth/register", json={
            "email": email_cand,
            "password": pwd,
            "confirm_password": pwd,
            "first_name": "Charlie",
            "last_name": "Candidate",
            "role": "candidate"
        })
        assert reg_cand.status_code == 201
        login_cand = await client.post("/api/v1/auth/login", json={"email": email_cand, "password": pwd})
        token_cand = login_cand.json()["tokens"]["access_token"]
        headers_cand = {"Authorization": f"Bearer {token_cand}"}

        cand_create_job = await client.post("/api/v1/jobs", json={
            "title": "Illegal Candidate Job",
            "description": "Trying to create job as candidate"
        }, headers=headers_cand)
        assert cand_create_job.status_code == 403, f"Candidate should be 403: {cand_create_job.text}"
        print("PASS 3: Candidate forbidden from creating jobs (403)", flush=True)

        # ----------------------------------------------------
        # 4. Recruiter A (without company) cannot create job yet
        # ----------------------------------------------------
        rec_no_comp = await client.post("/api/v1/jobs", json={
            "title": "No Company Job",
            "description": "Trying before company creation"
        }, headers=headers_a)
        assert rec_no_comp.status_code == 403
        assert "associated with a company" in rec_no_comp.text
        print("PASS 4: Recruiter without company cannot create jobs (403)", flush=True)

        # ----------------------------------------------------
        # 5. Recruiter A creates Company -> Auto-associated
        # ----------------------------------------------------
        comp_a_res = await client.post("/api/v1/companies", json={
            "name": f"TechCorp {uuid.uuid4().hex[:4]}",
            "description": "Leading Tech Solutions",
            "website": "https://techcorp.example.com",
            "location": "San Francisco, CA"
        }, headers=headers_a)
        assert comp_a_res.status_code == 201, f"Company creation failed: {comp_a_res.text}"
        comp_a_id = comp_a_res.json()["id"]
        print(f"PASS 5: Company created with ID {comp_a_id}", flush=True)

        # ----------------------------------------------------
        # 6. Verify /companies/me returns Recruiter A company
        # ----------------------------------------------------
        my_comp = await client.get("/api/v1/companies/me", headers=headers_a)
        assert my_comp.status_code == 200
        assert my_comp.json()["id"] == comp_a_id
        print("PASS 6: GET /companies/me returned recruiter company", flush=True)

        # ----------------------------------------------------
        # 7. Recruiter A creates Job POST /api/v1/jobs
        # ----------------------------------------------------
        job_payload = {
            "title": "Senior Backend Engineer",
            "description": "Develop scalable distributed microservices in Python & FastAPI.",
            "department": "Engineering",
            "work_mode": "REMOTE",
            "location": "San Francisco, CA",
            "salary_min": 140000,
            "salary_max": 190000,
            "currency": "USD",
            "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
            "preferred_skills": ["Kubernetes", "Redis"],
            "required_experience_months": 48,
            "education_requirements": ["Bachelor's Degree in Computer Science"],
            "required_keywords": ["FastAPI", "PostgreSQL", "AsyncIO"]
        }
        job_create_res = await client.post("/api/v1/jobs", json=job_payload, headers=headers_a)
        assert job_create_res.status_code == 201, f"Job creation failed: {job_create_res.text}"
        job_data = job_create_res.json()
        job_id = job_data["id"]
        assert job_data["company_id"] == comp_a_id
        assert job_data["status"] == "DRAFT"
        assert job_data["title"] == "Senior Backend Engineer"
        print(f"PASS 7: POST /api/v1/jobs succeeded, created job {job_id} in DRAFT status", flush=True)

        # ----------------------------------------------------
        # 8. GET /jobs/company/me returns company jobs
        # ----------------------------------------------------
        comp_jobs_res = await client.get("/api/v1/jobs/company/me", headers=headers_a)
        assert comp_jobs_res.status_code == 200
        comp_jobs = comp_jobs_res.json()
        assert comp_jobs["total"] >= 1
        assert any(j["id"] == job_id for j in comp_jobs["items"])
        print("PASS 8: GET /jobs/company/me listed the created job", flush=True)

        # ----------------------------------------------------
        # 9. GET /jobs/{job_id} & PATCH /jobs/{job_id}
        # ----------------------------------------------------
        get_job_res = await client.get(f"/api/v1/jobs/{job_id}", headers=headers_a)
        assert get_job_res.status_code == 200
        assert get_job_res.json()["id"] == job_id

        patch_job_res = await client.patch(f"/api/v1/jobs/{job_id}", json={"salary_max": 210000}, headers=headers_a)
        assert patch_job_res.status_code == 200
        assert patch_job_res.json()["salary_max"] == 210000
        print("PASS 9: GET and PATCH /jobs/{job_id} verified", flush=True)

        # ----------------------------------------------------
        # 10. Lifecycle: Publish -> Unpublish -> Publish -> Close
        # ----------------------------------------------------
        pub_res = await client.post(f"/api/v1/jobs/{job_id}/publish", headers=headers_a)
        assert pub_res.status_code == 200
        assert pub_res.json()["status"] == "PUBLISHED"

        unpub_res = await client.post(f"/api/v1/jobs/{job_id}/unpublish", headers=headers_a)
        assert unpub_res.status_code == 200
        assert unpub_res.json()["status"] == "DRAFT"

        await client.post(f"/api/v1/jobs/{job_id}/publish", headers=headers_a)
        close_res = await client.post(f"/api/v1/jobs/{job_id}/close", headers=headers_a)
        assert close_res.status_code == 200
        assert close_res.json()["status"] == "CLOSED"
        print("PASS 10: Status transitions (Publish -> Unpublish -> Publish -> Close) verified", flush=True)

        # ----------------------------------------------------
        # 11. Security: Recruiter B cannot modify Recruiter A's Job
        # ----------------------------------------------------
        email_b = f"rec_b_{uuid.uuid4().hex[:6]}@rivalcorp.com"
        await client.post("/api/v1/auth/register", json={
            "email": email_b, "password": pwd, "confirm_password": pwd,
            "first_name": "Bob", "last_name": "Rival", "role": "recruiter"
        })
        login_b = await client.post("/api/v1/auth/login", json={"email": email_b, "password": pwd})
        token_b = login_b.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        comp_b = await client.post("/api/v1/companies", json={"name": f"RivalCorp {uuid.uuid4().hex[:4]}"}, headers=headers_b)
        assert comp_b.status_code == 201

        # Recruiter B attempts update on Job A
        idor_patch = await client.patch(f"/api/v1/jobs/{job_id}", json={"title": "Hacked Title"}, headers=headers_b)
        assert idor_patch.status_code == 403

        # Recruiter B attempts delete on Job A
        idor_del = await client.delete(f"/api/v1/jobs/{job_id}", headers=headers_b)
        assert idor_del.status_code == 403
        print("PASS 11: Cross-company IDOR prevention verified (403)", flush=True)

        # ----------------------------------------------------
        # 12. Recruiter A deletes own job DELETE /api/v1/jobs/{job_id}
        # ----------------------------------------------------
        del_res = await client.delete(f"/api/v1/jobs/{job_id}", headers=headers_a)
        assert del_res.status_code == 204
        print("PASS 12: DELETE /jobs/{job_id} returned 204 No Content", flush=True)

        print("\n=======================================================", flush=True)
        print(">>> ALL 12 VERIFICATION TESTS PASSED SUCCESSFULLY! <<<", flush=True)
        print("=======================================================\n", flush=True)

if __name__ == "__main__":
    asyncio.run(run_tests())
