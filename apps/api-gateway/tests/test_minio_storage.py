"""Integration Test Suite for MinIO Storage and Transactional Safety."""

import asyncio
import io
import uuid
import sys
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock, AsyncMock

from app.main import app
from app.config.settings import settings
from app.models.enums import UserRole
from app.database.session import SessionLocal
from app.models.user import User
from app.models.resume import Resume
from app.services.storage.minio_service import MinioStorageService

def make_valid_pdf_content(size_bytes: int = 1024) -> bytes:
    """Generate valid PDF content with correct magic bytes."""
    header = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    padding = b"0" * max(0, size_bytes - len(header))
    return header + padding

def make_valid_docx_content(size_bytes: int = 1024) -> bytes:
    """Generate valid DOCX content with ZIP/PK magic bytes."""
    header = b"PK\x03\x04"
    padding = b"\x00" * max(0, size_bytes - len(header))
    return header + padding

async def run_minio_storage_tests():
    # Mock send_verification_email
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("\n============================================================")
        print("RUNNING MINIO STORAGE INTEGRATION TESTS")
        print("============================================================")

        # ======================================================================
        # SETUP: Create test users
        # ======================================================================
        password = "Password123!"
        email_candidate_a = f"minio_cand_a_{uuid.uuid4().hex[:6]}@example.com"
        email_candidate_b = f"minio_cand_b_{uuid.uuid4().hex[:6]}@example.com"

        # Register Candidate A
        res = await client.post("/api/v1/auth/register", json={
            "email": email_candidate_a,
            "password": password,
            "confirm_password": password,
            "first_name": "Minio",
            "last_name": "CandidateA",
        })
        assert res.status_code == 201, f"Register A failed: {res.text}"
        user_a_id = res.json()["user"]["id"]

        # Register Candidate B
        res = await client.post("/api/v1/auth/register", json={
            "email": email_candidate_b,
            "password": password,
            "confirm_password": password,
            "first_name": "Minio",
            "last_name": "CandidateB",
        })
        assert res.status_code == 201, f"Register B failed: {res.text}"
        user_b_id = res.json()["user"]["id"]

        # Mark users verified
        async with SessionLocal() as db:
            for uid in [user_a_id, user_b_id]:
                db_user = await db.get(User, uuid.UUID(uid))
                if db_user:
                    db_user.is_verified = True
            await db.commit()

        # Login and get tokens
        res = await client.post("/api/v1/auth/login", json={"email": email_candidate_a, "password": password})
        token_a = res.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        res = await client.post("/api/v1/auth/login", json={"email": email_candidate_b, "password": password})
        token_b = res.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # Initialize candidate profiles
        await client.get("/api/v1/candidates/me", headers=headers_a)
        await client.get("/api/v1/candidates/me", headers=headers_b)

        print("[OK] Setup completed: test users created and authenticated.")

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
        # TEST 1: MINIO CONFIGURATION
        # ======================================================================
        print("\nTEST 1: MINIO CONFIGURATION")
        check("Minio endpoint loaded", settings.minio.endpoint is not None)
        check("Minio access key loaded", settings.minio.access_key is not None)
        check("Minio secret key loaded", settings.minio.secret_key is not None)
        check("Minio bucket loaded", settings.minio.bucket == "talentai-resumes")
        check("Minio secure flag is False for dev", settings.minio.secure is False)

        # ======================================================================
        # TEST 2: MINIO CLIENT CONNECTION
        # ======================================================================
        print("\nTEST 2: MINIO CLIENT CONNECTION")
        storage = MinioStorageService()
        try:
            storage.ensure_bucket(settings.minio.bucket)
            check("Client connection & ensure_bucket succeed", True)
        except Exception as e:
            check("Client connection & ensure_bucket succeed", False, str(e))

        # Check bucket exists
        exists = storage.client.bucket_exists(settings.minio.bucket)
        check("talentai-resumes bucket exists", exists is True)

        # Check bucket is private (ensure it has no public read access policy set)
        policy = None
        try:
            policy = storage.client.get_bucket_policy(settings.minio.bucket)
        except Exception:
            pass
        check("Bucket is private", policy == "" or policy is None)

        # ======================================================================
        # TEST 3: VALID UPLOADS (PDF & DOCX)
        # ======================================================================
        print("\nTEST 3: VALID UPLOADS")
        # Upload valid PDF
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("candidate_a_resume.pdf", make_valid_pdf_content(1500), "application/pdf")},
        )
        check("Upload PDF returns 201", res.status_code == 201, f"got {res.status_code}: {res.text}")
        
        pdf_object_key = None
        if res.status_code == 201:
            resume_data = res.json()["resume"]
            check("storage_provider is minio", resume_data.get("storage_provider") == "minio")
            check("bucket_name is correct", resume_data.get("bucket_name") == settings.minio.bucket)
            pdf_object_key = resume_data.get("object_key")
            check("object_key is not None", pdf_object_key is not None)
            
            # Check unique format: candidates/{candidate_profile_id}/resumes/{resume_uuid}/resume.pdf
            check("object_key structure is correct", pdf_object_key.startswith("candidates/") and pdf_object_key.endswith(".pdf"))
            check("object_key does not contain path traversal", "../" not in pdf_object_key and ".." not in pdf_object_key)
            check("object_key does not contain backslashes", "\\" not in pdf_object_key)
            check("Original filename is not directly used as object key", "candidate_a_resume.pdf" not in pdf_object_key)
            
            # Verify file exists in MinIO
            exists_in_minio = storage.object_exists(settings.minio.bucket, pdf_object_key)
            check("Object actually exists in MinIO", exists_in_minio is True)

        # Upload valid DOCX
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("my_doc.docx", make_valid_docx_content(2000), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
        check("Upload DOCX returns 201", res.status_code == 201, f"got {res.status_code}: {res.text}")
        
        docx_object_key = None
        if res.status_code == 201:
            resume_data = res.json()["resume"]
            check("DOCX storage_provider is minio", resume_data.get("storage_provider") == "minio")
            docx_object_key = resume_data.get("object_key")
            check("DOCX object_key is not None", docx_object_key is not None)
            check("DOCX object_key ends with .docx", docx_object_key.endswith(".docx"))
            
            # Verify file exists in MinIO
            exists_in_minio = storage.object_exists(settings.minio.bucket, docx_object_key)
            check("DOCX object actually exists in MinIO", exists_in_minio is True)

        # Verify object keys are unique
        if pdf_object_key and docx_object_key:
            check("Object keys are unique", pdf_object_key != docx_object_key)

        # ======================================================================
        # TEST 4: CANDIDATE OWNERSHIP AND UNAUTHENTICATED
        # ======================================================================
        print("\nTEST 4: CANDIDATE OWNERSHIP AND AUTHENTICATION")
        # Unauthenticated upload
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            files={"file": ("resume.pdf", make_valid_pdf_content(), "application/pdf")},
        )
        check("Unauthenticated returns 401", res.status_code == 401)

        # ======================================================================
        # TEST 5: TRANSACTION SAFETY — CASE A: MINIO UPLOAD FAILS
        # ======================================================================
        print("\nTEST 5: TRANSACTION SAFETY — MINIO UPLOAD FAILS")
        # Force MinIO upload to fail by patching upload_object
        with patch.object(MinioStorageService, "upload_object", side_effect=Exception("Simulated MinIO failure")):
            res = await client.post(
                "/api/v1/candidates/me/resumes",
                headers=headers_b,
                files={"file": ("failure_test.pdf", make_valid_pdf_content(), "application/pdf")},
            )
            # Should fail
            check("Upload returns 500 on MinIO failure", res.status_code == 500 or res.status_code == 400)
            
            # Verify that no Resume record was created for Candidate B
            async with SessionLocal() as db:
                from sqlalchemy import select
                stmt = select(Resume).where(Resume.original_filename == "failure_test.pdf")
                db_res = await db.execute(stmt)
                resume_record = db_res.scalar_one_or_none()
                check("No DB record created when MinIO fails", resume_record is None)

        # ======================================================================
        # TEST 6: TRANSACTION SAFETY — CASE B & C: DATABASE PERSISTENCE FAILS
        # ======================================================================
        print("\nTEST 6: TRANSACTION SAFETY — DATABASE COMMIT FAILS")
        # Force DB commit to fail by patching the repository create method to raise an error
        captured_object_key = None
        
        # We wrap storage_service.upload_object to capture the object key generated during the call
        original_upload = MinioStorageService.upload_object
        def spy_upload(self, bucket_name, object_key, data, length, content_type, metadata=None):
            nonlocal captured_object_key
            captured_object_key = object_key
            return original_upload(self, bucket_name=bucket_name, object_key=object_key, data=data, length=length, content_type=content_type, metadata=metadata)
            
        with patch.object(MinioStorageService, "upload_object", spy_upload):
            # Patch ResumeRepository.create to raise exception
            with patch("app.repositories.candidate.resume_repository.ResumeRepository.create", side_effect=Exception("Simulated DB failure")):
                res = await client.post(
                    "/api/v1/candidates/me/resumes",
                    headers=headers_b,
                    files={"file": ("db_fail_test.pdf", make_valid_pdf_content(), "application/pdf")},
                )
                check("Upload returns 500 on DB failure", res.status_code == 500)
                
                # Check that the object key was generated and upload attempted
                check("Object key was generated", captured_object_key is not None)
                if captured_object_key:
                    # Check if the MinIO object was successfully cleaned up/deleted
                    exists_in_minio = storage.object_exists(settings.minio.bucket, captured_object_key)
                    check("MinIO object cleaned up (does not exist)", exists_in_minio is False)

        # ======================================================================
        # SUMMARY
        # ======================================================================
        print("\n============================================================")
        print(f"MINIO STORAGE TESTS COMPLETE: {passed} passed, {failed} failed")
        if failed == 0:
            print("ALL MINIO STORAGE INTEGRATION TESTS PASSED SUCCESSFULLY!")
        else:
            print(f"WARNING: {failed} test(s) FAILED!")
        print("============================================================\n")

    patcher.stop()

if __name__ == "__main__":
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(run_minio_storage_tests())
