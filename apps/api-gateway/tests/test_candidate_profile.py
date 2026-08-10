"""Integration Test Suite for Candidate Profile, Education, Experience, and Skills API endpoints."""

import asyncio
import uuid
from datetime import date, timedelta
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.enums import UserRole
from app.database.session import SessionLocal
from app.models.user import User
from app.auth.jwt import create_access_token



async def run_candidate_profile_tests():
    from unittest.mock import patch
    patcher = patch("app.services.email_service.EmailService.send_verification_email", return_value=True)
    patcher.start()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:



        print("\n============================================================")
        print("RUNNING CANDIDATE PROFILE INTEGRATION TESTS")
        print("============================================================")

        # 1. SETUP: Create two test users (Candidate A and Candidate B) and one Recruiter.
        # We will register them and bypass email verification constraints by marking them verified in db.
        email_candidate_a = f"candidate_a_{uuid.uuid4().hex[:6]}@example.com"
        email_candidate_b = f"candidate_b_{uuid.uuid4().hex[:6]}@example.com"
        email_recruiter = f"recruiter_{uuid.uuid4().hex[:6]}@example.com"
        password = "Password123!"

        # Register Candidate A
        reg_res_a = await client.post("/api/v1/auth/register", json={
            "email": email_candidate_a,
            "password": password,
            "confirm_password": password,
            "first_name": "Candidate",
            "last_name": "Alpha"
        })
        assert reg_res_a.status_code == 201, reg_res_a.text
        user_a_id = reg_res_a.json()["user"]["id"]

        # Register Candidate B
        reg_res_b = await client.post("/api/v1/auth/register", json={
            "email": email_candidate_b,
            "password": password,
            "confirm_password": password,
            "first_name": "Candidate",
            "last_name": "Beta"
        })
        assert reg_res_b.status_code == 201, reg_res_b.text
        user_b_id = reg_res_b.json()["user"]["id"]

        # Register Recruiter (registers as Candidate first, then we update role to recruiter in db)
        reg_res_r = await client.post("/api/v1/auth/register", json={
            "email": email_recruiter,
            "password": password,
            "confirm_password": password,
            "first_name": "Recruiter",
            "last_name": "One"
        })
        assert reg_res_r.status_code == 201, reg_res_r.text
        recruiter_id = reg_res_r.json()["user"]["id"]

        # Update user statuses directly in DB (mark verified, update recruiter role)
        async with SessionLocal() as db:
            for uid in [user_a_id, user_b_id, recruiter_id]:
                db_user = await db.get(User, uuid.UUID(uid))
                if db_user:
                    db_user.is_verified = True
                    if uid == recruiter_id:
                        db_user.role = UserRole.RECRUITER
            await db.commit()

        # Login to get authentic tokens
        login_res_a = await client.post("/api/v1/auth/login", json={"email": email_candidate_a, "password": password})
        assert login_res_a.status_code == 200
        token_a = login_res_a.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        login_res_b = await client.post("/api/v1/auth/login", json={"email": email_candidate_b, "password": password})
        assert login_res_b.status_code == 200
        token_b = login_res_b.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        login_res_r = await client.post("/api/v1/auth/login", json={"email": email_recruiter, "password": password})
        assert login_res_r.status_code == 200
        token_r = login_res_r.json()["tokens"]["access_token"]
        headers_r = {"Authorization": f"Bearer {token_r}"}

        print("✔ Setup completed: users created and authenticated.")

        # ==============================================================================
        # TEST 1: GET /candidates/me -> verify auto-initialization and default completion (0%)
        # ==============================================================================
        print("\nTEST 1: GET /candidates/me (Auto-initialization)")
        res = await client.get("/api/v1/candidates/me", headers=headers_a)
        assert res.status_code == 200, res.text
        profile_a = res.json()
        assert profile_a["profile_completion_percentage"] == 0
        assert profile_a["phone_number"] is None
        assert profile_a["headline"] is None
        print("✔ Profile auto-initialized with 0% completion.")

        # ==============================================================================
        # TEST 2: PATCH /candidates/me -> update profile fields and verify completion scoring
        # ==============================================================================
        print("\nTEST 2: PATCH /candidates/me (Profile Field Scores)")
        # Update phone_number (+10%), location (+10%), headline (+10%), bio (+10%), profile_picture_url (+10%), linkedin_url (+5%), github_url (+5%), portfolio_url (+5%)
        # Let's verify URL validation
        bad_url_res = await client.patch("/api/v1/candidates/me", headers=headers_a, json={
            "linkedin_url": "invalid-url-no-http"
        })
        assert bad_url_res.status_code == 422, "Expected URL validation failure"

        # Valid update (updating 4 fields: phone, location, headline, bio) -> should result in 40% completion
        update_payload = {
            "phone_number": "+1234567890",
            "location": "Berlin, Germany",
            "headline": "Fullstack Python Engineer",
            "bio": "Passionate developer working with FastAPI and Next.js."
        }
        res = await client.patch("/api/v1/candidates/me", headers=headers_a, json=update_payload)
        assert res.status_code == 200, res.text
        profile_a = res.json()
        assert profile_a["phone_number"] == "+1234567890"
        assert profile_a["location"] == "Berlin, Germany"
        assert profile_a["profile_completion_percentage"] == 40
        print("✔ Profile updated; completion scored 40% correctly.")

        # Update remaining social URLs -> total 55% completion
        res = await client.patch("/api/v1/candidates/me", headers=headers_a, json={
            "profile_picture_url": "https://example.com/avatar.png",
            "linkedin_url": "https://linkedin.com/in/candidatea",
            "github_url": "https://github.com/candidatea",
            "portfolio_url": "https://candidatea.dev"
        })
        assert res.status_code == 200, res.text
        profile_a = res.json()
        assert profile_a["profile_completion_percentage"] == 65
        print("✔ Social URLs updated; completion scored 65% correctly.")

        # ==============================================================================
        # TEST 3: EDUCATION CRUD & DATE VALIDATION & SCORING (+15%)
        # ==============================================================================
        print("\nTEST 3: EDUCATION CRUD & VALIDATION")
        # Validate date range (start_date > end_date should fail)
        bad_edu_payload = {
            "degree": "B.Sc Computer Science",
            "institution": "University of Tech",
            "start_date": "2024-01-01",
            "end_date": "2020-01-01"
        }
        res = await client.post("/api/v1/candidates/me/education", headers=headers_a, json=bad_edu_payload)
        assert res.status_code == 422, "Expected date validation error"

        # Valid education addition
        edu_payload = {
            "degree": "B.Sc Computer Science",
            "institution": "University of Tech",
            "start_date": "2020-09-01",
            "end_date": "2024-06-30",
            "grade_or_cgpa": "3.8 GPA"
        }
        res = await client.post("/api/v1/candidates/me/education", headers=headers_a, json=edu_payload)
        assert res.status_code == 201, res.text
        edu_a = res.json()
        assert edu_a["degree"] == "B.Sc Computer Science"
        assert edu_a["id"] is not None

        # Verify profile completion updated (65% + 15% = 80%)
        res = await client.get("/api/v1/candidates/me", headers=headers_a)
        assert res.json()["profile_completion_percentage"] == 80
        print("✔ Education entry added; completion scored 80%.")

        # Update education
        res = await client.patch(
            f"/api/v1/candidates/me/education/{edu_a['id']}",
            headers=headers_a,
            json={"degree": "B.Sc Computer Science (Honours)"}
        )
        assert res.status_code == 200, res.text
        assert res.json()["degree"] == "B.Sc Computer Science (Honours)"
        print("✔ Education entry updated successfully.")

        # ==============================================================================
        # TEST 4: EXPERIENCE CRUD & SCORING (+10%)
        # ==============================================================================
        print("\nTEST 4: EXPERIENCE CRUD & VALIDATION")
        # Valid experience addition
        exp_payload = {
            "company": "Tech Corp",
            "job_title": "Backend Engineer",
            "start_date": "2024-07-01",
            "description": "Building microservices using FastAPI."
        }
        res = await client.post("/api/v1/candidates/me/experience", headers=headers_a, json=exp_payload)
        assert res.status_code == 201, res.text
        exp_a = res.json()
        assert exp_a["company"] == "Tech Corp"
        assert exp_a["end_date"] is None

        # Verify profile completion updated (80% + 10% = 90%)
        res = await client.get("/api/v1/candidates/me", headers=headers_a)
        assert res.json()["profile_completion_percentage"] == 90
        print("✔ Experience entry added; completion scored 90%.")

        # ==============================================================================
        # TEST 5: SKILLS CRUD & DUPLICATE PREVENTION & NORMALIZATION & SCORING (+10%)
        # ==============================================================================
        print("\nTEST 5: SKILLS CRUD & DUPLICATE PREVENTION")
        # Add skill Python
        skill_payload = {
            "skill_name": "Python ", # note the trailing whitespace for testing strip
            "category": "programming",
            "proficiency": "expert"
        }
        res = await client.post("/api/v1/candidates/me/skills", headers=headers_a, json=skill_payload)
        assert res.status_code == 201, res.text
        skill_a = res.json()
        assert skill_a["skill_name"] == "Python" # Verify strip
        assert skill_a["normalized_skill_name"] == "python"

        # Attempt to add duplicate "python" (case-insensitive) -> should return 409 Conflict
        res = await client.post("/api/v1/candidates/me/skills", headers=headers_a, json={
            "skill_name": "  PYTHON  ",
            "category": "programming",
            "proficiency": "advanced"
        })
        assert res.status_code == 409, f"Expected 409, got {res.status_code}"
        print("✔ Duplicate skill insertion blocked correctly with HTTP 409.")

        # Verify profile completion updated (90% + 10% = 100%)
        res = await client.get("/api/v1/candidates/me", headers=headers_a)
        assert res.json()["profile_completion_percentage"] == 100
        print("✔ Skill added; completion scored 100%.")

        # ==============================================================================
        # TEST 6: AUTHORIZATION AND ROLE-BASED ACCESS CONTROL (RBAC)
        # ==============================================================================
        print("\nTEST 6: ROLE-BASED ACCESS CONTROL")
        # Recruiter accessing candidate profile endpoint -> 403 Forbidden
        res = await client.get("/api/v1/candidates/me", headers=headers_r)
        assert res.status_code == 403, f"Expected 403, got {res.status_code}"

        # Anonymous user accessing endpoint -> 401 Unauthorized
        res = await client.get("/api/v1/candidates/me")
        assert res.status_code == 401, f"Expected 401, got {res.status_code}"
        print("✔ Endpoint access restrictions enforced correctly (403 for recruiters, 401 for anonymous).")

        # ==============================================================================
        # TEST 7: IDOR PROTECTION (CANDIDATE B ATTEMPTING TO ACCESS CANDIDATE A'S RECORDS)
        # ==============================================================================
        print("\nTEST 7: IDOR PROTECTION")
        # Candidate B attempts to update Candidate A's education -> 404 Not Found (or 403, we return 404 for non-existent/inaccessible records)
        res = await client.patch(
            f"/api/v1/candidates/me/education/{edu_a['id']}",
            headers=headers_b,
            json={"degree": "Hacked degree"}
        )
        assert res.status_code == 404, f"Expected 404, got {res.status_code}"

        # Candidate B attempts to delete Candidate A's experience -> 404 Not Found
        res = await client.delete(
            f"/api/v1/candidates/me/experience/{exp_a['id']}",
            headers=headers_b
        )
        assert res.status_code == 404, f"Expected 404, got {res.status_code}"

        # Candidate B attempts to delete Candidate A's skill -> 404 Not Found
        res = await client.delete(
            f"/api/v1/candidates/me/skills/{skill_a['id']}",
            headers=headers_b
        )
        assert res.status_code == 404, f"Expected 404, got {res.status_code}"
        print("✔ IDOR protection verified: Candidate B cannot modify Candidate A's sub-entities.")

        # ==============================================================================
        # TEST 8: DELETION AND COMPLETION RECALCULATION
        # ==============================================================================
        print("\nTEST 8: SUB-ENTITY DELETION & SCORE PROGRESSION")
        # Delete education -> completion should decrease (100% - 15% = 85%)
        res = await client.delete(f"/api/v1/candidates/me/education/{edu_a['id']}", headers=headers_a)
        assert res.status_code == 200, res.text

        res = await client.get("/api/v1/candidates/me", headers=headers_a)
        assert res.json()["profile_completion_percentage"] == 85

        # Delete experience -> completion should decrease (85% - 10% = 75%)
        res = await client.delete(f"/api/v1/candidates/me/experience/{exp_a['id']}", headers=headers_a)
        assert res.status_code == 200, res.text

        res = await client.get("/api/v1/candidates/me", headers=headers_a)
        assert res.json()["profile_completion_percentage"] == 75

        # Delete skill -> completion should decrease (75% - 10% = 65%)
        res = await client.delete(f"/api/v1/candidates/me/skills/{skill_a['id']}", headers=headers_a)
        assert res.status_code == 200, res.text

        res = await client.get("/api/v1/candidates/me", headers=headers_a)
        assert res.json()["profile_completion_percentage"] == 65
        print("✔ Sub-entities deleted successfully; profile completion score recalculated accurately.")

        print("\n============================================================")
        print("ALL CANDIDATE PROFILE INTEGRATION TESTS PASSED SUCCESSFULLY!")
        print("============================================================\n")

    patcher.stop()




if __name__ == "__main__":
    asyncio.run(run_candidate_profile_tests())
