"""Integration Test Suite for Resume Preview and Download API endpoints.

Tests secure preview rendering, download streaming, custom header sanitization,
candidate ownership, role-based access control, and error handling for missing/deleted items.
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
from app.services.storage.minio_service import MinioStorageService

# Force UTF-8 output encoding for Windows PowerShell compatibility
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def make_valid_pdf_content(size_bytes: int = 1024) -> bytes:
    """Generate valid PDF content with correct magic bytes."""
    header = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    padding = b"0" * max(0, size_bytes - len(header))
    return header + padding


def make_valid_docx_content(size_bytes: int = 1024) -> bytes:
    """Generate valid DOCX content with correct ZIP/PK magic bytes."""
    header = b"PK\x03\x04"
    padding = b"\x00" * max(0, size_bytes - len(header))
    return header + padding


async def run_resume_preview_tests():
    # Patch verification email to prevent SMTP issues
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("\n============================================================")
        print("RUNNING RESUME PREVIEW & DOWNLOAD INTEGRATION TESTS")
        print("============================================================")

        # ======================================================================
        # SETUP: Create candidate A, candidate B, and recruiter
        # ======================================================================
        password = "Password123!"
        email_a = f"prev_cand_a_{uuid.uuid4().hex[:6]}@example.com"
        email_b = f"prev_cand_b_{uuid.uuid4().hex[:6]}@example.com"
        email_r = f"prev_rec_{uuid.uuid4().hex[:6]}@example.com"

        # Register Candidate A
        res = await client.post("/api/v1/auth/register", json={
            "email": email_a,
            "password": password,
            "confirm_password": password,
            "first_name": "Preview",
            "last_name": "CandidateA",
        })
        assert res.status_code == 201, f"Register A failed: {res.text}"
        user_a_id = uuid.UUID(res.json()["user"]["id"])

        # Register Candidate B
        res = await client.post("/api/v1/auth/register", json={
            "email": email_b,
            "password": password,
            "confirm_password": password,
            "first_name": "Preview",
            "last_name": "CandidateB",
        })
        assert res.status_code == 201
        user_b_id = uuid.UUID(res.json()["user"]["id"])

        # Register Recruiter
        res = await client.post("/api/v1/auth/register", json={
            "email": email_r,
            "password": password,
            "confirm_password": password,
            "first_name": "Preview",
            "last_name": "Recruiter",
        })
        assert res.status_code == 201
        rec_id = uuid.UUID(res.json()["user"]["id"])

        # Mark users as verified, set Recruiter role
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
        # Candidate A uploads a PDF (with spaces/unicode in filename)
        pdf_content = make_valid_pdf_content(1500)
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("My Resume (Uńicode).pdf", io.BytesIO(pdf_content), "application/pdf")}
        )
        assert res.status_code == 201, res.text
        resume_a_id = uuid.UUID(res.json()["resume"]["id"])

        # Candidate B uploads a DOCX
        docx_content = make_valid_docx_content(2000)
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_b,
            files={"file": ("MyJobFile.docx", io.BytesIO(docx_content), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        )
        assert res.status_code == 201, res.text
        resume_b_id = uuid.UUID(res.json()["resume"]["id"])

        print("[OK] Test files uploaded to MinIO and database.")

        passed = 0
        failed = 0

        def check(test_name, condition, detail=""):
            nonlocal passed, failed
            if condition:
                print(f"  [OK] {test_name}")
                passed += 1
            else:
                print(f"  [FAIL] {test_name} — {detail}")
                failed += 1

        # ======================================================================
        # TEST 1: Authenticated PDF preview (Content-Type & inline disposition)
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/preview", headers=headers_a)
        check("TEST 1: PDF preview status is 200", res.status_code == 200)
        check("TEST 1: PDF preview media_type is application/pdf", res.headers.get("content-type") == "application/pdf")
        disp = res.headers.get("content-disposition", "")
        check("TEST 1: PDF preview disposition is inline", disp.startswith("inline;"))
        check("TEST 1: PDF preview encodes unicode filename", "filename*=UTF-8''My%20Resume%20%28U%C5%84icode%29.pdf" in disp)
        check("TEST 1: PDF preview stream length matches", len(res.content) == 1500)

        # ======================================================================
        # TEST 2: Authenticated PDF download (Content-Disposition attachment)
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/download", headers=headers_a)
        check("TEST 2: PDF download status is 200", res.status_code == 200)
        disp = res.headers.get("content-disposition", "")
        check("TEST 2: PDF download disposition is attachment", disp.startswith("attachment;"))
        check("TEST 2: PDF download stream length matches", len(res.content) == 1500)

        # ======================================================================
        # TEST 3: Authenticated DOCX download (Content-Disposition attachment)
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_b_id}/download", headers=headers_b)
        check("TEST 3: DOCX download status is 200", res.status_code == 200)
        check("TEST 3: DOCX media_type is wordprocessingml.document", res.headers.get("content-type") == "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        disp = res.headers.get("content-disposition", "")
        check("TEST 3: DOCX download disposition is attachment", disp.startswith("attachment;"))
        check("TEST 3: DOCX download stream length matches", len(res.content) == 2000)

        # ======================================================================
        # TEST 4: Unauthenticated preview -> 401
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/preview")
        check("TEST 4: Unauthenticated preview returns 401", res.status_code == 401)

        # ======================================================================
        # TEST 5: Unauthenticated download -> 401
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/download")
        check("TEST 5: Unauthenticated download returns 401", res.status_code == 401)

        # ======================================================================
        # TEST 6: Candidate ownership: A tries to access B's resume preview -> 404
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_b_id}/preview", headers=headers_a)
        check("TEST 6: Candidate A blocked from B's preview with 404", res.status_code == 404)

        # ======================================================================
        # TEST 7: Candidate ownership: B tries to access A's resume download -> 404
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/download", headers=headers_b)
        check("TEST 7: Candidate B blocked from A's download with 404", res.status_code == 404)

        # ======================================================================
        # TEST 8: Recruiter RBAC check -> 403
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/preview", headers=headers_r)
        check("TEST 8: Recruiter forbidden from candidate endpoint with 403", res.status_code == 403)

        # ======================================================================
        # TEST 9: Non-existent resume ID -> 404
        # ======================================================================
        fake_uuid = uuid.uuid4()
        res = await client.get(f"/api/v1/candidates/me/resumes/{fake_uuid}/preview", headers=headers_a)
        check("TEST 9: Non-existent resume ID returns 404", res.status_code == 404)

        # ======================================================================
        # TEST 10: Invalid UUID parameter -> 422
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/not-a-valid-uuid/preview", headers=headers_a)
        check("TEST 10: Malformed resume ID parameter returns 422", res.status_code == 422)

        # ======================================================================
        # TEST 11: Deleted resume protection -> 404
        # ======================================================================
        # Mark resume as deleted in DB
        async with SessionLocal() as db:
            r = await db.get(Resume, resume_a_id)
            if r:
                r.is_deleted = True
            await db.commit()

        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}/preview", headers=headers_a)
        check("TEST 11: Deleted resume preview returns 404", res.status_code == 404)

        # Restore deleted resume for further tests
        async with SessionLocal() as db:
            r = await db.get(Resume, resume_a_id)
            if r:
                r.is_deleted = False
            await db.commit()

        # ======================================================================
        # TEST 12: Missing S3/MinIO physical object -> 404
        # ======================================================================
        # Create a database-only resume for Candidate A that has no MinIO object
        db_only_id = uuid.uuid4()
        async with SessionLocal() as db:
            db.add(Resume(
                id=db_only_id,
                candidate_profile_id=profile_a_id,
                original_filename="db_only.pdf",
                stored_filename=f"stored_db_only_{uuid.uuid4().hex[:6]}.pdf",
                mime_type="application/pdf",
                file_extension=".pdf",
                file_size_bytes=500,
                status=ResumeStatus.UPLOADED,
                version=99,
                is_current=False,
                storage_provider="minio",
                bucket_name="talentai-resumes",
                object_key=f"candidates/{profile_a_id}/resumes/db_only.pdf",
                uploaded_at=datetime.now(timezone.utc)
            ))
            await db.commit()

        res = await client.get(f"/api/v1/candidates/me/resumes/{db_only_id}/preview", headers=headers_a)
        check("TEST 12: Missing storage object returns 404", res.status_code == 404)

        # ======================================================================
        # TEST 13: Missing storage object key / NULL in DB -> 404
        # ======================================================================
        db_null_key_id = uuid.uuid4()
        async with SessionLocal() as db:
            db.add(Resume(
                id=db_null_key_id,
                candidate_profile_id=profile_a_id,
                original_filename="db_null_key.pdf",
                stored_filename=f"stored_db_null_{uuid.uuid4().hex[:6]}.pdf",
                mime_type="application/pdf",
                file_extension=".pdf",
                file_size_bytes=500,
                status=ResumeStatus.UPLOADED,
                version=100,
                is_current=False,
                storage_provider="minio",
                bucket_name="talentai-resumes",
                object_key=None,  # NULL object key
                uploaded_at=datetime.now(timezone.utc)
            ))
            await db.commit()

        res = await client.get(f"/api/v1/candidates/me/resumes/{db_null_key_id}/preview", headers=headers_a)
        check("TEST 13: NULL storage object key reference returns 404", res.status_code == 404)

        # ======================================================================
        # TEST 14: Secure metadata endpoint -> 200
        # ======================================================================
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_a_id}", headers=headers_a)
        check("TEST 14: Metadata status is 200", res.status_code == 200)
        if res.status_code == 200:
            meta = res.json()
            check("TEST 14: Metadata ID matches", meta["id"] == str(resume_a_id))
            check("TEST 14: Metadata original_filename matches", meta["original_filename"] == "My Resume (Uńicode).pdf")
            check("TEST 14: Metadata does not leak stored_filename", "stored_filename" not in meta)
            check("TEST 14: Metadata does not leak private configurations", "secret_key" not in meta and "access_key" not in meta)

        # ======================================================================
        # CLEANUP
        # ======================================================================
        print("\n--- CLEANING UP TEST DATA ---")
        storage = MinioStorageService()
        async with SessionLocal() as db:
            # Delete resumes A, B, and the temporary db-only resumes
            for r_id in [resume_a_id, resume_b_id, db_only_id, db_null_key_id]:
                r = await db.get(Resume, r_id)
                if r:
                    if r.bucket_name and r.object_key:
                        try:
                            storage.delete_object(r.bucket_name, r.object_key)
                        except Exception:
                            pass
                    await db.delete(r)

            # Delete users
            from sqlalchemy import select
            for email in [email_a, email_b, email_r]:
                res = await db.execute(select(User).where(User.email == email))
                user = res.scalar_one_or_none()
                if user:
                    await db.delete(user)
            await db.commit()
        print("[OK] Cleaned up all test database entries and object files.")

        print("\n============================================================")
        print(f"RESUME PREVIEW TESTS COMPLETE: {passed} passed, {failed} failed")
        print("============================================================\n")
        
        if failed > 0:
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_resume_preview_tests())
