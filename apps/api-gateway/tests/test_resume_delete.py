"""Integration Test Suite for Resume Delete API endpoints.

Tests soft deletion behavior in database, physical object deletion in MinIO,
unauthenticated/unauthorized checks, IDOR security between candidates, listing
cleanup, preview/download regression blocks, and failure compensation flows.
"""

import asyncio
import io
import sys
import uuid
import urllib.parse
from datetime import datetime, timezone
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from app.main import app
from app.database.session import SessionLocal
from app.models.user import User
from app.models.enums import UserRole, ResumeStatus
from app.models.resume import Resume
from app.repositories.candidate.resume_repository import ResumeRepository
from app.services.storage.minio_service import MinioStorageService

# Force UTF-8 output encoding for Windows PowerShell compatibility
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def make_valid_pdf_content(size_bytes: int = 1024) -> bytes:
    """Generate valid PDF content with correct magic bytes."""
    header = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    padding = b"0" * max(0, size_bytes - len(header))
    return header + padding


async def run_resume_delete_tests():
    # Patch verification email to prevent SMTP issues
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("\n============================================================")
        print("RUNNING RESUME DELETE INTEGRATION TESTS")
        print("============================================================")

        # ======================================================================
        # SETUP: Create candidate A, candidate B, and recruiter
        # ======================================================================
        password = "Password123!"
        email_a = f"del_cand_a_{uuid.uuid4().hex[:6]}@example.com"
        email_b = f"del_cand_b_{uuid.uuid4().hex[:6]}@example.com"
        email_r = f"del_rec_{uuid.uuid4().hex[:6]}@example.com"

        # Register Candidate A
        res = await client.post("/api/v1/auth/register", json={
            "email": email_a,
            "password": password,
            "confirm_password": password,
            "first_name": "Delete",
            "last_name": "CandidateA",
        })
        assert res.status_code == 201, f"Register A failed: {res.text}"
        user_a_id = uuid.UUID(res.json()["user"]["id"])

        # Register Candidate B
        res = await client.post("/api/v1/auth/register", json={
            "email": email_b,
            "password": password,
            "confirm_password": password,
            "first_name": "Delete",
            "last_name": "CandidateB",
        })
        assert res.status_code == 201
        user_b_id = uuid.UUID(res.json()["user"]["id"])

        # Register Recruiter
        res = await client.post("/api/v1/auth/register", json={
            "email": email_r,
            "password": password,
            "confirm_password": password,
            "first_name": "Delete",
            "last_name": "Recruiter",
        })
        assert res.status_code == 201
        rec_id = uuid.UUID(res.json()["user"]["id"])

        # Mark users as verified, set Recruiter/Candidate roles
        async with SessionLocal() as db:
            for uid, role in [(user_a_id, UserRole.CANDIDATE), (user_b_id, UserRole.CANDIDATE), (rec_id, UserRole.RECRUITER)]:
                u = await db.get(User, uid)
                if u:
                    u.is_verified = True
                    u.role = role
            await db.commit()

        # Login and get headers
        res = await client.post("/api/v1/auth/login", json={"email": email_a, "password": password})
        token_a = res.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        res = await client.post("/api/v1/auth/login", json={"email": email_b, "password": password})
        token_b = res.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        res = await client.post("/api/v1/auth/login", json={"email": email_r, "password": password})
        token_r = res.json()["tokens"]["access_token"]
        headers_r = {"Authorization": f"Bearer {token_r}"}

        # Resolve candidate profiles
        res_a = await client.get("/api/v1/candidates/me", headers=headers_a)
        profile_a_id = uuid.UUID(res_a.json()["id"])
        
        res_b = await client.get("/api/v1/candidates/me", headers=headers_b)
        profile_b_id = uuid.UUID(res_b.json()["id"])

        print("[OK] Setup completed: test users and profiles initialized.")

        # ======================================================================
        # UPLOAD RESUMES VIA E2E UPLOAD FLOW
        # ======================================================================
        # Candidate A uploads a PDF
        pdf_content = make_valid_pdf_content(1500)
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("ResumeA.pdf", io.BytesIO(pdf_content), "application/pdf")}
        )
        assert res.status_code == 201, res.text
        resume_a_id = uuid.UUID(res.json()["resume"]["id"])

        # Candidate B uploads a PDF
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_b,
            files={"file": ("ResumeB.pdf", io.BytesIO(pdf_content), "application/pdf")}
        )
        assert res.status_code == 201, res.text
        resume_b_id = uuid.UUID(res.json()["resume"]["id"])

        print("[OK] Test files uploaded to MinIO and database.")

        passed = 0
        failed = 0

        def check(test_name: str, condition: bool):
            nonlocal passed, failed
            if condition:
                print(f"  [OK] {test_name}")
                passed += 1
            else:
                print(f"  [FAIL] {test_name}")
                failed += 1

        storage = MinioStorageService()

        # ======================================================================
        # TEST 1: Delete requires authentication
        # ======================================================================
        res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_a_id}")
        check("TEST 1: Unauthenticated request returns 401", res.status_code == 401)

        # ======================================================================
        # TEST 2: Recruiter forbidden from candidate endpoint
        # ======================================================================
        res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_a_id}", headers=headers_r)
        check("TEST 2: Recruiter is Forbidden (403)", res.status_code == 403)

        # ======================================================================
        # TEST 3: Candidate A cannot delete Candidate B's resume (IDOR Protection)
        # ======================================================================
        res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_b_id}", headers=headers_a)
        check("TEST 3: Cross-candidate deletion returns 404", res.status_code == 404)
        
        # Verify B's record is still active in database
        async with SessionLocal() as db:
            r_b = await db.get(Resume, resume_b_id)
            check("TEST 3: Candidate B's DB record remains untouched", r_b is not None and r_b.is_deleted is False)

        # Verify B's file is still present in storage
        check("TEST 3: Candidate B's S3 file remains intact", storage.object_exists(r_b.bucket_name, r_b.object_key))

        # ======================================================================
        # TEST 4: Delete nonexistent UUID
        # ======================================================================
        random_id = uuid.uuid4()
        res = await client.delete(f"/api/v1/candidates/me/resumes/{random_id}", headers=headers_a)
        check("TEST 4: Nonexistent resume ID returns 404", res.status_code == 404)

        # ======================================================================
        # TEST 5: Delete malformed resume ID
        # ======================================================================
        res = await client.delete("/api/v1/candidates/me/resumes/not-a-valid-uuid", headers=headers_a)
        check("TEST 5: Malformed UUID format returns 422", res.status_code == 422)

        # ======================================================================
        # TEST 6: Candidate deletes own resume (Positive Flow)
        # ======================================================================
        async with SessionLocal() as db:
            r_a = await db.get(Resume, resume_a_id)
            bucket_name_a = r_a.bucket_name
            object_key_a = r_a.object_key

        res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_a_id}", headers=headers_a)
        check("TEST 6: Successful delete returns 200", res.status_code == 200)
        if res.status_code == 200:
            data = res.json()
            check("TEST 6: Response shows success=True", data.get("success") is True)
            check("TEST 6: Response contains correct resume_id", data.get("resume_id") == str(resume_a_id))

        # Database Check: Soft delete status
        async with SessionLocal() as db:
            r_a_deleted = await db.get(Resume, resume_a_id)
            check("TEST 6: DB is_deleted flag is True", r_a_deleted.is_deleted is True)
            check("TEST 6: DB deleted_at timestamp is populated", r_a_deleted.deleted_at is not None)
            check("TEST 6: DB is_current flag is set to False", r_a_deleted.is_current is False)
            check("TEST 6: DB candidate_profile_id is preserved", r_a_deleted.candidate_profile_id == profile_a_id)

        # S3 / Storage Check: Hard delete status
        check("TEST 6: MinIO physical file is deleted", not storage.object_exists(bucket_name_a, object_key_a))

        # ======================================================================
        # TEST 7: Already deleted resume returns 404
        # ======================================================================
        res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_a_id}", headers=headers_a)
        check("TEST 7: Already deleted resume returns 404 on retry", res.status_code == 404)

        # ======================================================================
        # TEST 8: Listing cleanup (Deleted resume disappears from listing)
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes", headers=headers_a)
        check("TEST 8: Get active resumes list succeeds", res.status_code == 200)
        if res.status_code == 200:
            items = res.json()["items"]
            check("TEST 8: Deleted resume is absent from active listing", not any(i["id"] == str(resume_a_id) for i in items))

        # ======================================================================
        # TEST 9: Preview Regression (Deleted resume cannot be previewed)
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/preview", headers=headers_a)
        check("TEST 9: Preview deleted resume returns 404", res.status_code == 404)

        # ======================================================================
        # TEST 10: Download Regression (Deleted resume cannot be downloaded)
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/download", headers=headers_a)
        check("TEST 10: Download deleted resume returns 404", res.status_code == 404)

        # ======================================================================
        # TEST 11: MinIO Deletion Failure Transaction Safety
        # ======================================================================
        # Create a new resume for A
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("ResumeA_FailStorage.pdf", io.BytesIO(pdf_content), "application/pdf")}
        )
        assert res.status_code == 201
        resume_fail_storage_id = uuid.UUID(res.json()["resume"]["id"])

        # Mock S3 delete to raise an error
        with patch.object(MinioStorageService, "delete_object", side_effect=Exception("Simulated S3 Delete Failure")):
            res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_fail_storage_id}", headers=headers_a)
            check("TEST 11: MinIO deletion failure returns 500 or StorageError", res.status_code == 500)

            # Database record MUST remain active (is_deleted = False)
            async with SessionLocal() as db:
                r_fail = await db.get(Resume, resume_fail_storage_id)
                check("TEST 11: DB record is NOT soft-deleted on storage failure", r_fail.is_deleted is False)

        # ======================================================================
        # TEST 12: Database Deletion Failure Compensation Rollback
        # ======================================================================
        # Create a new resume for A
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("ResumeA_FailDB.pdf", io.BytesIO(pdf_content), "application/pdf")}
        )
        assert res.status_code == 201
        resume_fail_db_id = uuid.UUID(res.json()["resume"]["id"])

        async with SessionLocal() as db:
            r_fail_db = await db.get(Resume, resume_fail_db_id)
            bucket_name_fail_db = r_fail_db.bucket_name
            object_key_fail_db = r_fail_db.object_key

        # Mock Repository delete to raise a database error
        with patch.object(ResumeRepository, "delete_no_commit", side_effect=Exception("Simulated Database Delete Failure")):
            res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_fail_db_id}", headers=headers_a)
            check("TEST 12: DB deletion failure returns 500", res.status_code == 500)

            # S3 / MinIO object MUST be restored/re-uploaded
            check("TEST 12: MinIO object was successfully restored", storage.object_exists(bucket_name_fail_db, object_key_fail_db))

            # Database record remains active
            async with SessionLocal() as db:
                r_fail_db_check = await db.get(Resume, resume_fail_db_id)
                check("TEST 12: DB record is NOT soft-deleted", r_fail_db_check.is_deleted is False)

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n--- CLEANING UP TEST DATA ---")
        async with SessionLocal() as db:
            # Delete S3 objects for remaining active resumes in test
            for r_id in [resume_b_id, resume_fail_storage_id, resume_fail_db_id]:
                r = await db.get(Resume, r_id)
                if r and r.bucket_name and r.object_key:
                    try:
                        storage.delete_object(r.bucket_name, r.object_key)
                    except Exception:
                        pass
                if r:
                    await db.delete(r)

            # Delete soft-deleted A resume
            r = await db.get(Resume, resume_a_id)
            if r:
                await db.delete(r)

            # Purge test users
            from sqlalchemy import select
            for email in [email_a, email_b, email_r]:
                res_user = await db.execute(select(User).where(User.email == email))
                user = res_user.scalar_one_or_none()
                if user:
                    await db.delete(user)
            await db.commit()

        print("[OK] Cleaned up all test database entries and object files.")

        print("\n============================================================")
        print(f"RESUME DELETE TESTS COMPLETE: {passed} passed, {failed} failed")
        print("============================================================\n")

        if failed > 0:
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_resume_delete_tests())
