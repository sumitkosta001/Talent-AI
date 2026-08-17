"""Integration Test Suite for Resume Upload History and Processing Status (Day 17).

Tests:
1. Candidate upload history listing and pagination
2. Deterministic sorting (newest upload first: uploaded_at DESC, id DESC)
3. Processing status lifecycle: UPLOADED -> PROCESSING -> PROCESSED
4. Processing failure lifecycle: UPLOADED -> PROCESSING -> FAILED
5. Safe failure reason exposure and timestamp tracking (processing_started_at, processing_completed_at)
6. Retry processing: FAILED -> PROCESSING -> PROCESSED
7. Retry invariants: same resume ID, same version, same object key, same is_current flag
8. Concurrency / conflict handling (409 on duplicate processing, 400 on already processed)
9. Security & IDOR: authentication (401), role access (403), cross-candidate isolation (404)
10. Database and MinIO consistency across retries
"""

import asyncio
import io
import sys
import uuid
from datetime import datetime, timezone
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from app.main import app
from app.database.session import SessionLocal
from app.models.user import User
from app.models.enums import UserRole, ResumeStatus
from app.models.resume import Resume
from app.repositories.candidate.resume_repository import ResumeRepository

# Force UTF-8 output encoding for Windows PowerShell compatibility
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def make_valid_pdf_content(size_bytes: int = 1024) -> bytes:
    """Generate valid PDF content with correct magic bytes."""
    header = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n"
    padding = b"0" * max(0, size_bytes - len(header))
    return header + padding


async def upload_resume_file(client, headers, filename="test.pdf", size=1024):
    """Helper to upload a resume and return the response."""
    content = make_valid_pdf_content(size)
    files = {"file": (filename, io.BytesIO(content), "application/pdf")}
    res = await client.post("/api/v1/candidates/me/resumes", headers=headers, files=files)
    return res


async def run_resume_history_tests():
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("\n============================================================", flush=True)
        print("RUNNING RESUME UPLOAD HISTORY & PROCESSING TESTS (DAY 17)", flush=True)
        print("============================================================", flush=True)

        passed = 0
        failed = 0
        total = 0

        def check(condition: bool, test_name: str, detail: str = ""):
            nonlocal passed, failed, total
            total += 1
            if condition:
                passed += 1
                print(f"  PASS [{total:02d}] {test_name}", flush=True)
            else:
                failed += 1
                print(f"  FAIL [{total:02d}] {test_name} - {detail}", flush=True)

        # ------------------------------------------------------------------
        # Setup test candidates and recruiter
        # ------------------------------------------------------------------
        uid_a = uuid.uuid4().hex[:8]
        uid_b = uuid.uuid4().hex[:8]
        uid_r = uuid.uuid4().hex[:8]

        email_a = f"history_cand_a_{uid_a}@example.com"
        email_b = f"history_cand_b_{uid_b}@example.com"
        email_r = f"history_recruiter_{uid_r}@example.com"
        password = "Password123!"

        res_a = await client.post("/api/v1/auth/register", json={
            "email": email_a, "password": password, "confirm_password": password,
            "first_name": "History", "last_name": "CandA",
        })
        assert res_a.status_code == 201, f"Register A failed: {res_a.text}"
        user_a_id = uuid.UUID(res_a.json()["user"]["id"])

        res_b = await client.post("/api/v1/auth/register", json={
            "email": email_b, "password": password, "confirm_password": password,
            "first_name": "History", "last_name": "CandB",
        })
        assert res_b.status_code == 201, f"Register B failed: {res_b.text}"
        user_b_id = uuid.UUID(res_b.json()["user"]["id"])

        res_r = await client.post("/api/v1/auth/register", json={
            "email": email_r, "password": password, "confirm_password": password,
            "first_name": "History", "last_name": "Recruiter",
        })
        assert res_r.status_code == 201, f"Register R failed: {res_r.text}"
        user_r_id = uuid.UUID(res_r.json()["user"]["id"])

        # Mark verified & set roles
        async with SessionLocal() as db:
            for uid, role in [(user_a_id, UserRole.CANDIDATE), (user_b_id, UserRole.CANDIDATE), (user_r_id, UserRole.RECRUITER)]:
                u = await db.get(User, uid)
                if u:
                    u.is_verified = True
                    u.role = role
            await db.commit()

        login_a = await client.post("/api/v1/auth/login", json={"email": email_a, "password": password})
        token_a = login_a.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        login_b = await client.post("/api/v1/auth/login", json={"email": email_b, "password": password})
        token_b = login_b.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        login_r = await client.post("/api/v1/auth/login", json={"email": email_r, "password": password})
        token_r = login_r.json()["tokens"]["access_token"]
        headers_r = {"Authorization": f"Bearer {token_r}"}

        # Initialize profile
        await client.get("/api/v1/candidates/me", headers=headers_a)
        await client.get("/api/v1/candidates/me", headers=headers_b)


        # ==================================================================
        # SECTION 1: Empty History & Auth Security
        # ==================================================================
        print("\n--- Section 1: Empty History & Auth Security ---", flush=True)
        res_empty = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_a)
        check(res_empty.status_code == 200, "Empty history returns 200")
        check(res_empty.json()["total"] == 0, "Empty history total is 0")
        check(len(res_empty.json()["items"]) == 0, "Empty history items list is empty")

        res_unauth = await client.get("/api/v1/candidates/me/resumes/history")
        check(res_unauth.status_code == 401, "Unauthenticated request returns 401")

        res_recruiter = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_r)
        check(res_recruiter.status_code == 403, "Recruiter role returns 403")

        # ==================================================================
        # SECTION 2: Uploads & Upload History Ordering
        # ==================================================================
        print("\n--- Section 2: Uploads & Ordering (uploaded_at DESC) ---", flush=True)
        # Upload v1
        u1 = await upload_resume_file(client, headers_a, filename="resume_v1.pdf")
        check(u1.status_code == 201, "Upload v1 returns 201")
        r1_id = u1.json()["resume"]["id"]

        await asyncio.sleep(0.05)
        # Upload v2
        u2 = await upload_resume_file(client, headers_a, filename="resume_v2.pdf")
        check(u2.status_code == 201, "Upload v2 returns 201")
        r2_id = u2.json()["resume"]["id"]

        await asyncio.sleep(0.05)
        # Upload v3
        u3 = await upload_resume_file(client, headers_a, filename="resume_v3.pdf")
        check(u3.status_code == 201, "Upload v3 returns 201")
        r3_id = u3.json()["resume"]["id"]

        # Retrieve history
        h_res = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_a)
        check(h_res.status_code == 200, "Get history returns 200")
        h_data = h_res.json()
        check(h_data["total"] == 3, "Total resumes in history is 3")
        items = h_data["items"]
        check(len(items) == 3, "History items count is 3")
        check(items[0]["id"] == r3_id, "History item 1 is newest upload (v3)")
        check(items[1]["id"] == r2_id, "History item 2 is earlier upload (v2)")
        check(items[2]["id"] == r1_id, "History item 3 is oldest upload (v1)")

        # Verify initial fields
        check(items[0]["status"] == "uploaded", "Initial status is 'uploaded'")
        check(items[0]["uploaded_at"] is not None, "uploaded_at is populated")
        check(items[0]["processing_started_at"] is None, "processing_started_at is initially None")
        check(items[0]["processing_completed_at"] is None, "processing_completed_at is initially None")
        check(items[0]["failure_reason"] is None, "failure_reason is initially None")

        # ==================================================================
        # SECTION 3: Pagination and Custom Sorting
        # ==================================================================
        print("\n--- Section 3: Pagination and Sorting ---", flush=True)
        p1 = await client.get("/api/v1/candidates/me/resumes/history?page=1&page_size=2", headers=headers_a)
        check(p1.status_code == 200, "Page 1 returns 200")
        p1_data = p1.json()
        check(len(p1_data["items"]) == 2, "Page 1 has 2 items")
        check(p1_data["total"] == 3, "Total is 3")
        check(p1_data["total_pages"] == 2, "Total pages is 2")
        check(p1_data["has_next"] is True, "Page 1 has_next is True")
        check(p1_data["has_previous"] is False, "Page 1 has_previous is False")

        p2 = await client.get("/api/v1/candidates/me/resumes/history?page=2&page_size=2", headers=headers_a)
        check(p2.status_code == 200, "Page 2 returns 200")
        p2_data = p2.json()
        check(len(p2_data["items"]) == 1, "Page 2 has 1 item")
        check(p2_data["has_next"] is False, "Page 2 has_next is False")
        check(p2_data["has_previous"] is True, "Page 2 has_previous is True")
        check(p2_data["items"][0]["id"] == r1_id, "Page 2 item is oldest upload (v1)")

        # Ascending sort
        s_asc = await client.get("/api/v1/candidates/me/resumes/history?sort_by=uploaded_at&sort_order=asc", headers=headers_a)
        check(s_asc.status_code == 200, "Sort by uploaded_at asc returns 200")
        s_items = s_asc.json()["items"]
        check(s_items[0]["id"] == r1_id, "Ascending sort first item is v1")
        check(s_items[2]["id"] == r3_id, "Ascending sort last item is v3")

        # Invalid sort parameters
        bad_sort = await client.get("/api/v1/candidates/me/resumes/history?sort_by=malicious_col", headers=headers_a)
        check(bad_sort.status_code == 400, "Invalid sort_by returns 400")

        bad_order = await client.get("/api/v1/candidates/me/resumes/history?sort_order=sideways", headers=headers_a)
        check(bad_order.status_code == 400, "Invalid sort_order returns 400")

        # ==================================================================
        # SECTION 4: Processing Lifecycle (UPLOADED -> PROCESSING -> PROCESSED)
        # ==================================================================
        print("\n--- Section 4: Successful Processing Lifecycle ---", flush=True)
        proc_res = await client.post(f"/api/v1/candidates/me/resumes/{r1_id}/process", headers=headers_a)
        check(proc_res.status_code == 200, "Process v1 returns 200")
        proc_data = proc_res.json()
        check(proc_data["success"] is True, "Process response success is True")
        r1_updated = proc_data["resume"]
        check(r1_updated["status"] == "processed", "v1 status is now 'processed'")
        check(r1_updated["processing_started_at"] is not None, "processing_started_at is populated")
        check(r1_updated["processing_completed_at"] is not None, "processing_completed_at is populated")
        check(r1_updated["failure_reason"] is None, "failure_reason is None on success")

        # Verify history reflects updated status
        h_after_proc = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_a)
        v1_in_h = next(item for item in h_after_proc.json()["items"] if item["id"] == r1_id)
        check(v1_in_h["status"] == "processed", "History shows v1 is 'processed'")
        check(v1_in_h["processing_completed_at"] is not None, "History exposes v1 processing_completed_at")

        # Double processing an already processed resume
        double_proc = await client.post(f"/api/v1/candidates/me/resumes/{r1_id}/process", headers=headers_a)
        check(double_proc.status_code == 400, "Processing already processed resume returns 400")

        # ==================================================================
        # SECTION 5: Processing Failure Lifecycle (UPLOADED -> FAILED)
        # ==================================================================
        print("\n--- Section 5: Processing Failure Lifecycle ---", flush=True)
        # Simulate processing failure on v2 by mocking storage object not found
        with patch("app.services.storage.minio_service.MinioStorageService.object_exists", return_value=False):
            fail_proc = await client.post(f"/api/v1/candidates/me/resumes/{r2_id}/process", headers=headers_a)
            check(fail_proc.status_code == 200, "Failed process call returns 200 with failed status")
            fail_data = fail_proc.json()
            check(fail_data["success"] is False, "Failure response success is False")
            r2_updated = fail_data["resume"]
            check(r2_updated["status"] == "failed", "v2 status is 'failed'")
            check(r2_updated["failure_reason"] is not None, "failure_reason is populated")
            check("not found in storage" in r2_updated["failure_reason"].lower(), "failure_reason contains safe error description")
            check(r2_updated["processing_started_at"] is not None, "processing_started_at is populated")
            check(r2_updated["processing_completed_at"] is None, "processing_completed_at is None on failure")


        # Verify history reflects failure
        h_after_fail = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_a)
        v2_in_h = next(item for item in h_after_fail.json()["items"] if item["id"] == r2_id)
        check(v2_in_h["status"] == "failed", "History shows v2 status is 'failed'")
        check(v2_in_h["failure_reason"] is not None, "History shows v2 failure_reason")

        # ==================================================================
        # SECTION 6: Retry Processing (FAILED -> PROCESSED)
        # ==================================================================
        print("\n--- Section 6: Retry Processing Lifecycle ---", flush=True)
        # Get original v2 metadata before retry
        v2_meta_before = await client.get(f"/api/v1/candidates/me/resumes/{r2_id}", headers=headers_a)
        v2_orig = v2_meta_before.json()

        # Retry v2 processing (normal storage check passes)
        retry_res = await client.post(f"/api/v1/candidates/me/resumes/{r2_id}/retry", headers=headers_a)
        check(retry_res.status_code == 200, "Retry v2 returns 200")
        retry_data = retry_res.json()
        check(retry_data["success"] is True, "Retry response success is True")
        v2_after = retry_data["resume"]

        # Verify retry invariants
        check(v2_after["id"] == r2_id, "Retry preserves same resume ID")
        check(v2_after["version"] == v2_orig["version"], "Retry preserves same version number (no version increment)")
        check(v2_after["is_current"] == v2_orig["is_current"], "Retry preserves same is_current flag")
        check(v2_after["object_key"] == v2_orig["object_key"], "Retry preserves same MinIO object key")
        check(v2_after["status"] == "processed", "Retry transitions status to 'processed'")
        check(v2_after["failure_reason"] is None, "Retry clears failure_reason")
        check(v2_after["processing_completed_at"] is not None, "Retry populates processing_completed_at")

        # Total resumes count must not increase
        h_after_retry = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_a)
        check(h_after_retry.json()["total"] == 3, "Total resumes in history remains 3 after retry (no duplicate record)")

        # Retrying an already processed resume
        retry_already_proc = await client.post(f"/api/v1/candidates/me/resumes/{r2_id}/retry", headers=headers_a)
        check(retry_already_proc.status_code == 400, "Retrying already processed resume returns 400")

        # ==================================================================
        # SECTION 7: Retry Security & IDOR Protection
        # ==================================================================
        print("\n--- Section 7: Retry Security & IDOR Protection ---", flush=True)
        # Candidate B attempts to retry Candidate A's resume
        idor_retry = await client.post(f"/api/v1/candidates/me/resumes/{r1_id}/retry", headers=headers_b)
        check(idor_retry.status_code == 404, "Candidate B cannot retry Candidate A's resume (404)")

        # Unauthenticated retry
        unauth_retry = await client.post(f"/api/v1/candidates/me/resumes/{r1_id}/retry")
        check(unauth_retry.status_code == 401, "Unauthenticated retry returns 401")

        # Recruiter retry
        recruiter_retry = await client.post(f"/api/v1/candidates/me/resumes/{r1_id}/retry", headers=headers_r)
        check(recruiter_retry.status_code == 403, "Recruiter role retry returns 403")

        # Nonexistent resume UUID
        fake_uuid = str(uuid.uuid4())
        nonexistent_retry = await client.post(f"/api/v1/candidates/me/resumes/{fake_uuid}/retry", headers=headers_a)
        check(nonexistent_retry.status_code == 404, "Nonexistent resume retry returns 404")

        # Malformed UUID
        malformed_retry = await client.post("/api/v1/candidates/me/resumes/not-a-valid-uuid/retry", headers=headers_a)
        check(malformed_retry.status_code == 422, "Malformed UUID retry returns 422")

        # ==================================================================
        # SECTION 8: Soft-Deleted Resume Cannot Be Retried
        # ==================================================================
        print("\n--- Section 8: Deleted Resume Protection ---", flush=True)
        # Delete v2
        del_v2 = await client.delete(f"/api/v1/candidates/me/resumes/{r2_id}", headers=headers_a)
        check(del_v2.status_code == 200, "Delete v2 returns 200")

        # Attempt to retry deleted resume
        retry_del = await client.post(f"/api/v1/candidates/me/resumes/{r2_id}/retry", headers=headers_a)
        check(retry_del.status_code == 404, "Deleted resume retry returns 404")

        # History excludes deleted resume
        h_after_del = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_a)
        check(h_after_del.json()["total"] == 2, "History excludes soft-deleted resume (total=2)")

        # ==================================================================
        # SECTION 9: Candidate Isolation in History
        # ==================================================================
        print("\n--- Section 9: Candidate Isolation in History ---", flush=True)
        # Candidate B uploads 1 resume
        ub1 = await upload_resume_file(client, headers_b, filename="cand_b_resume.pdf")
        check(ub1.status_code == 201, "Candidate B upload returns 201")
        rb1_id = ub1.json()["resume"]["id"]

        hb_res = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_b)
        check(hb_res.status_code == 200, "Candidate B history returns 200")
        check(hb_res.json()["total"] == 1, "Candidate B history total is 1")
        check(hb_res.json()["items"][0]["id"] == rb1_id, "Candidate B history contains only B's resume")

        ha_res = await client.get("/api/v1/candidates/me/resumes/history", headers=headers_a)
        check(ha_res.json()["total"] == 2, "Candidate A history total is still 2 (independent of B)")

        # ==================================================================
        # CLEANUP
        # ==================================================================
        print("\n--- Cleaning up test data ---", flush=True)
        async with SessionLocal() as db:
            from sqlalchemy import text
            await db.execute(
                text("DELETE FROM candidate_resumes WHERE candidate_profile_id IN (SELECT id FROM candidate_profiles WHERE user_id IN (SELECT id FROM users WHERE email LIKE 'history_%'))")
            )
            await db.execute(
                text("DELETE FROM candidate_profiles WHERE user_id IN (SELECT id FROM users WHERE email LIKE 'history_%')")
            )
            await db.execute(
                text("DELETE FROM users WHERE email LIKE 'history_%'")
            )
            await db.commit()
        print("[OK] Test database entries cleaned up.", flush=True)

        patcher.stop()

        print("\n============================================================", flush=True)
        print(f"RESUME HISTORY TESTS: {passed} passed, {failed} failed, {total} total", flush=True)
        print("============================================================\n", flush=True)

        if failed > 0:
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_resume_history_tests())
