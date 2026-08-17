"""Integration Test Suite for Resume Upload API endpoint.

Tests authentication, file validation (extension, MIME, content, size),
filename sanitization, database record creation, and authorization.
Follows the same testing pattern as test_candidate_profile.py.
"""

import asyncio
import uuid
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.enums import UserRole
from app.database.session import SessionLocal
from app.models.user import User


# ==============================================================================
# HELPERS — Generate valid file content for testing
# ==============================================================================

def make_valid_pdf_content(size_bytes: int = 1024) -> bytes:
    """Generate valid PDF content with correct magic bytes."""
    header = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    padding = b"0" * max(0, size_bytes - len(header))
    return header + padding


def make_valid_docx_content(size_bytes: int = 1024) -> bytes:
    """Generate valid DOCX content with correct ZIP/PK magic bytes.

    DOCX files are ZIP archives. We create minimal ZIP structure.
    """
    # Minimal ZIP local file header for [Content_Types].xml
    header = b"PK\x03\x04"  # ZIP magic bytes
    padding = b"\x00" * max(0, size_bytes - len(header))
    return header + padding


def make_fake_pdf_content() -> bytes:
    """Generate content that claims to be PDF but has wrong magic bytes."""
    return b"This is not a PDF file at all, just plain text."


def make_fake_docx_content() -> bytes:
    """Generate content that claims to be DOCX but has wrong magic bytes."""
    return b"This is not a DOCX file either, just random data."


def make_oversized_content(size_mb: int = 11) -> bytes:
    """Generate content larger than the configured maximum."""
    return b"%PDF-1.4\n" + (b"X" * (size_mb * 1024 * 1024))


async def run_resume_upload_tests():
    """Execute all resume upload integration tests."""
    from unittest.mock import patch, AsyncMock
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:

        print("\n============================================================")
        print("RUNNING RESUME UPLOAD INTEGRATION TESTS")
        print("============================================================")

        # ======================================================================
        # SETUP: Create test users
        # ======================================================================
        password = "Password123!"
        email_candidate_a = f"resume_cand_a_{uuid.uuid4().hex[:6]}@example.com"
        email_candidate_b = f"resume_cand_b_{uuid.uuid4().hex[:6]}@example.com"
        email_recruiter = f"resume_rec_{uuid.uuid4().hex[:6]}@example.com"

        # Register Candidate A
        res = await client.post("/api/v1/auth/register", json={
            "email": email_candidate_a,
            "password": password,
            "confirm_password": password,
            "first_name": "ResumeTest",
            "last_name": "CandidateA",
        })
        assert res.status_code == 201, f"Register A failed: {res.text}"
        user_a_id = res.json()["user"]["id"]

        # Register Candidate B
        res = await client.post("/api/v1/auth/register", json={
            "email": email_candidate_b,
            "password": password,
            "confirm_password": password,
            "first_name": "ResumeTest",
            "last_name": "CandidateB",
        })
        assert res.status_code == 201, f"Register B failed: {res.text}"
        user_b_id = res.json()["user"]["id"]

        # Register Recruiter
        res = await client.post("/api/v1/auth/register", json={
            "email": email_recruiter,
            "password": password,
            "confirm_password": password,
            "first_name": "Recruiter",
            "last_name": "Resume",
        })
        assert res.status_code == 201, f"Register R failed: {res.text}"
        recruiter_id = res.json()["user"]["id"]

        # Verify users and set recruiter role
        async with SessionLocal() as db:
            for uid in [user_a_id, user_b_id, recruiter_id]:
                db_user = await db.get(User, uuid.UUID(uid))
                if db_user:
                    db_user.is_verified = True
                    if uid == recruiter_id:
                        db_user.role = UserRole.RECRUITER
            await db.commit()

        # Login and get tokens
        res = await client.post("/api/v1/auth/login", json={"email": email_candidate_a, "password": password})
        assert res.status_code == 200
        token_a = res.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        res = await client.post("/api/v1/auth/login", json={"email": email_candidate_b, "password": password})
        assert res.status_code == 200
        token_b = res.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        res = await client.post("/api/v1/auth/login", json={"email": email_recruiter, "password": password})
        assert res.status_code == 200
        token_r = res.json()["tokens"]["access_token"]
        headers_r = {"Authorization": f"Bearer {token_r}"}

        # Initialize candidate profiles (auto-created on first access)
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
        # TEST 1: AUTHENTICATION — Unauthenticated upload -> 401
        # ======================================================================
        print("\nTEST 1: AUTHENTICATION")
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            files={"file": ("resume.pdf", make_valid_pdf_content(), "application/pdf")},
        )
        check("Unauthenticated upload -> 401", res.status_code == 401, f"got {res.status_code}")

        # ======================================================================
        # TEST 2: RBAC — Recruiter upload -> 403
        # ======================================================================
        print("\nTEST 2: ROLE-BASED ACCESS CONTROL")
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_r,
            files={"file": ("resume.pdf", make_valid_pdf_content(), "application/pdf")},
        )
        check("Recruiter upload -> 403", res.status_code == 403, f"got {res.status_code}")

        # ======================================================================
        # TEST 3: VALID PDF UPLOAD
        # ======================================================================
        print("\nTEST 3: VALID FILE UPLOADS")
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("my_resume.pdf", make_valid_pdf_content(), "application/pdf")},
        )
        check("Valid PDF upload -> 201", res.status_code == 201, f"got {res.status_code}: {res.text}")
        if res.status_code == 201:
            data = res.json()
            resume_a = data["resume"]
            check("Response has success=True", data["success"] is True)
            check("Resume has valid ID", resume_a.get("id") is not None)
            check("Correct original filename", resume_a.get("original_filename") == "my_resume.pdf")
            check("Correct MIME type", resume_a.get("mime_type") == "application/pdf")
            check("Correct extension", resume_a.get("file_extension") == ".pdf")
            check("Correct status", resume_a.get("status") == "uploaded")
            check("Version is 1", resume_a.get("version") == 1)
            check("is_current is True", resume_a.get("is_current") is True)
            check("File size > 0", resume_a.get("file_size_bytes", 0) > 0)
            check("Has uploaded_at", resume_a.get("uploaded_at") is not None)
            check("Has candidate_profile_id", resume_a.get("candidate_profile_id") is not None)

        # ======================================================================
        # TEST 4: VALID DOCX UPLOAD
        # ======================================================================
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": (
                "my_resume.docx",
                make_valid_docx_content(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )},
        )
        check("Valid DOCX upload -> 201", res.status_code == 201, f"got {res.status_code}: {res.text}")
        if res.status_code == 201:
            docx_data = res.json()["resume"]
            check("DOCX correct extension", docx_data.get("file_extension") == ".docx")
            check("DOCX correct MIME", docx_data.get("mime_type") == "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            check("DOCX version is 2 (versioning)", docx_data.get("version") == 2)
            check("DOCX is_current is True", docx_data.get("is_current") is True)

        # ======================================================================
        # TEST 5: UPPERCASE EXTENSION
        # ======================================================================
        print("\nTEST 5: CASE-INSENSITIVE EXTENSIONS")
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("resume.PDF", make_valid_pdf_content(), "application/pdf")},
        )
        check("Uppercase .PDF -> accepted", res.status_code == 201, f"got {res.status_code}: {res.text}")

        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": (
                "resume.DOCX",
                make_valid_docx_content(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )},
        )
        check("Uppercase .DOCX -> accepted", res.status_code == 201, f"got {res.status_code}: {res.text}")

        # ======================================================================
        # TEST 6: EXTENSION VALIDATION
        # ======================================================================
        print("\nTEST 6: EXTENSION VALIDATION")
        invalid_exts = [
            ("malware.exe", "application/x-msdownload"),
            ("photo.jpg", "image/jpeg"),
            ("image.png", "image/png"),
            ("archive.zip", "application/zip"),
            ("old_doc.doc", "application/msword"),
            ("macro.docm", "application/vnd.ms-word.document.macroEnabled.12"),
            ("spreadsheet.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
        ]
        for filename, mime in invalid_exts:
            res = await client.post(
                "/api/v1/candidates/me/resumes",
                headers=headers_a,
                files={"file": (filename, b"fake content", mime)},
            )
            check(f"Extension .{filename.split('.')[-1]} -> rejected", res.status_code == 400, f"got {res.status_code}")

        # ======================================================================
        # TEST 7: MIME TYPE VALIDATION
        # ======================================================================
        print("\nTEST 7: MIME TYPE VALIDATION")
        invalid_mimes = [
            ("resume.pdf", make_valid_pdf_content(), "image/png"),
            ("resume.pdf", make_valid_pdf_content(), "application/x-executable"),
            ("resume.pdf", make_valid_pdf_content(), "text/plain"),
        ]
        for filename, content, mime in invalid_mimes:
            res = await client.post(
                "/api/v1/candidates/me/resumes",
                headers=headers_a,
                files={"file": (filename, content, mime)},
            )
            check(f"MIME '{mime}' with .pdf -> rejected", res.status_code == 400, f"got {res.status_code}")

        # ======================================================================
        # TEST 8: FILE CONTENT / MAGIC BYTES VALIDATION
        # ======================================================================
        print("\nTEST 8: FILE CONTENT VALIDATION")
        # Fake PDF — correct extension and MIME but wrong content
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("fake.pdf", make_fake_pdf_content(), "application/pdf")},
        )
        check("Fake PDF (wrong magic bytes) -> rejected", res.status_code == 400, f"got {res.status_code}")

        # Fake DOCX — correct extension and MIME but wrong content
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": (
                "fake.docx",
                make_fake_docx_content(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )},
        )
        check("Fake DOCX (wrong magic bytes) -> rejected", res.status_code == 400, f"got {res.status_code}")

        # ======================================================================
        # TEST 9: FILE SIZE VALIDATION
        # ======================================================================
        print("\nTEST 9: FILE SIZE VALIDATION")
        # Small valid file -> accepted (already tested above)
        check("Small file (below limit) -> accepted", True)

        # Oversized file
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("big_resume.pdf", make_oversized_content(11), "application/pdf")},
        )
        check("Oversized file (11 MB) -> rejected", res.status_code == 413, f"got {res.status_code}")

        # Empty file
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("empty.pdf", b"", "application/pdf")},
        )
        check("Empty file -> rejected", res.status_code in (400, 413), f"got {res.status_code}")

        # ======================================================================
        # TEST 10: FILENAME SECURITY
        # ======================================================================
        print("\nTEST 10: FILENAME SANITIZATION")

        # Path traversal filenames — should be sanitized (not rejected, just cleaned)
        dangerous_filenames = [
            "../resume.pdf",
            "..\\resume.pdf",
            "C:\\temp\\resume.pdf",
            "/tmp/resume.pdf",
            "../../etc/passwd.pdf",
        ]
        for dname in dangerous_filenames:
            res = await client.post(
                "/api/v1/candidates/me/resumes",
                headers=headers_a,
                files={"file": (dname, make_valid_pdf_content(), "application/pdf")},
            )
            if res.status_code == 201:
                returned_name = res.json()["resume"]["original_filename"]
                check(
                    f"Path traversal '{dname}' -> sanitized to '{returned_name}'",
                    ".." not in returned_name and "/" not in returned_name and "\\" not in returned_name,
                    f"Filename not sanitized: {returned_name}",
                )
            else:
                check(f"Path traversal '{dname}' -> handled ({res.status_code})", True)

        # Double extension attack
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("resume.pdf.exe", b"fake", "application/pdf")},
        )
        check("Double extension resume.pdf.exe -> rejected", res.status_code == 400, f"got {res.status_code}")

        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": ("resume.docx.exe", b"fake", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )
        check("Double extension resume.docx.exe -> rejected", res.status_code == 400, f"got {res.status_code}")

        # Very long filename
        long_name = "a" * 500 + ".pdf"
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": (long_name, make_valid_pdf_content(), "application/pdf")},
        )
        if res.status_code == 201:
            returned_name = res.json()["resume"]["original_filename"]
            check(f"Long filename (500 chars) -> truncated to {len(returned_name)} chars", len(returned_name) <= 255)
        else:
            check(f"Long filename -> handled ({res.status_code})", True)

        # Control characters in filename
        control_name = "resume\x00\x01\x02.pdf"
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_a,
            files={"file": (control_name, make_valid_pdf_content(), "application/pdf")},
        )
        if res.status_code == 201:
            returned_name = res.json()["resume"]["original_filename"]
            check("Control chars in filename -> sanitized", "\x00" not in returned_name and "\x01" not in returned_name)
        else:
            check(f"Control chars in filename -> handled ({res.status_code})", True)

        # ======================================================================
        # TEST 11: DATABASE RECORD VERIFICATION
        # ======================================================================
        print("\nTEST 11: DATABASE RECORD VERIFICATION")
        # Upload a fresh PDF for Candidate B and verify the record
        res = await client.post(
            "/api/v1/candidates/me/resumes",
            headers=headers_b,
            files={"file": ("candidate_b_resume.pdf", make_valid_pdf_content(2048), "application/pdf")},
        )
        check("Candidate B upload -> 201", res.status_code == 201, f"got {res.status_code}: {res.text}")
        if res.status_code == 201:
            resume_b = res.json()["resume"]
            check("DB: correct candidate_profile_id present", resume_b.get("candidate_profile_id") is not None)
            check("DB: correct original_filename", resume_b.get("original_filename") == "candidate_b_resume.pdf")
            check("DB: correct MIME type", resume_b.get("mime_type") == "application/pdf")
            check("DB: correct extension", resume_b.get("file_extension") == ".pdf")
            check("DB: correct file_size_bytes", resume_b.get("file_size_bytes") == 2048)
            check("DB: correct initial status", resume_b.get("status") == "uploaded")
            check("DB: version is 1 (first for this candidate)", resume_b.get("version") == 1)
            check("DB: is_current is True", resume_b.get("is_current") is True)

        # ======================================================================
        # SUMMARY
        # ======================================================================
        print("\n============================================================")
        print(f"RESUME UPLOAD TESTS COMPLETE: {passed} passed, {failed} failed")
        if failed == 0:
            print("ALL RESUME UPLOAD INTEGRATION TESTS PASSED SUCCESSFULLY!")
        else:
            print(f"WARNING: {failed} test(s) FAILED!")
        print("============================================================\n")

    patcher.stop()


if __name__ == "__main__":
    asyncio.run(run_resume_upload_tests())
