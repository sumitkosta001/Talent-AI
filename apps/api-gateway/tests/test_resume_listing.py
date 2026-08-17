"""Integration Test Suite for Resume Listing endpoint GET /api/v1/candidates/me/resumes."""

import asyncio
import sys
import uuid
from datetime import datetime, timedelta, timezone
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, AsyncMock

from app.main import app
from app.config.settings import settings
from app.database.session import SessionLocal
from app.models.user import User
from app.models.candidate_profile import CandidateProfile
from app.models.resume import Resume
from app.models.enums import ResumeStatus, UserRole

# Force UTF-8 output encoding for Windows PowerShell compatibility
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

async def run_resume_listing_tests():
    # Patch verification email to prevent SMTP issues
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("\n============================================================")
        print("RUNNING RESUME LISTING INTEGRATION TESTS")
        print("============================================================")

        # ======================================================================
        # SETUP: Create candidate A, candidate B, and recruiter
        # ======================================================================
        password = "Password123!"
        email_a = f"list_cand_a_{uuid.uuid4().hex[:6]}@example.com"
        email_b = f"list_cand_b_{uuid.uuid4().hex[:6]}@example.com"
        email_r = f"list_rec_{uuid.uuid4().hex[:6]}@example.com"

        # Register Candidate A
        res = await client.post("/api/v1/auth/register", json={
            "email": email_a,
            "password": password,
            "confirm_password": password,
            "first_name": "Listing",
            "last_name": "CandidateA",
        })
        assert res.status_code == 201, f"Register A failed: {res.text}"
        user_a_id = uuid.UUID(res.json()["user"]["id"])

        # Register Candidate B
        res = await client.post("/api/v1/auth/register", json={
            "email": email_b,
            "password": password,
            "confirm_password": password,
            "first_name": "Listing",
            "last_name": "CandidateB",
        })
        assert res.status_code == 201
        user_b_id = uuid.UUID(res.json()["user"]["id"])

        # Register Recruiter
        res = await client.post("/api/v1/auth/register", json={
            "email": email_r,
            "password": password,
            "confirm_password": password,
            "first_name": "Listing",
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

        # Initialize profiles
        res_a = await client.get("/api/v1/candidates/me", headers=headers_a)
        profile_a_id = uuid.UUID(res_a.json()["id"])
        
        res_b = await client.get("/api/v1/candidates/me", headers=headers_b)
        profile_b_id = uuid.UUID(res_b.json()["id"])

        print("[OK] Setup completed: test users and profiles initialized.")

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
        # TEST 1: Unauthenticated request
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes")
        check("TEST 1: Unauthenticated -> 401", res.status_code == 401, f"got {res.status_code}")

        # ======================================================================
        # TEST 2: Authenticated candidate with zero resumes
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes", headers=headers_b)
        check("TEST 2: Zero resumes -> 200", res.status_code == 200, f"got {res.status_code}: {res.text}")
        if res.status_code == 200:
            data = res.json()
            check("TEST 2: Empty items list", data["items"] == [])
            check("TEST 2: total is 0", data["total"] == 0)
            check("TEST 2: page is 1", data["page"] == 1)
            check("TEST 2: total_pages is 0", data["total_pages"] == 0)
            check("TEST 2: has_next is False", data["has_next"] is False)
            check("TEST 2: has_previous is False", data["has_previous"] is False)

        # ======================================================================
        # TEST 3: Authenticated candidate with one resume
        # ======================================================================
        # Seed 1 resume for Candidate B via direct DB insert to make it fast
        resume_b_id = uuid.uuid4()
        b_stored = f"stored_b_{uuid.uuid4().hex[:8]}.pdf"
        async with SessionLocal() as db:
            db.add(Resume(
                id=resume_b_id,
                candidate_profile_id=profile_b_id,
                original_filename="cand_b_resume.pdf",
                stored_filename=b_stored,
                mime_type="application/pdf",
                file_extension=".pdf",
                file_size_bytes=1500,
                status=ResumeStatus.UPLOADED,
                version=1,
                is_current=True,
                storage_provider="minio",
                bucket_name="talentai-resumes",
                object_key=f"candidates/{profile_b_id}/resumes/{b_stored}",
                uploaded_at=datetime.now(timezone.utc)
            ))
            await db.commit()

        res = await client.get("/api/v1/candidates/me/resumes", headers=headers_b)
        check("TEST 3: One resume -> 200", res.status_code == 200)
        if res.status_code == 200:
            data = res.json()
            check("TEST 3: items count is 1", len(data["items"]) == 1)
            check("TEST 3: total is 1", data["total"] == 1)
            check("TEST 3: original_filename matches", data["items"][0]["original_filename"] == "cand_b_resume.pdf")

        # ======================================================================
        # SEED DATA FOR CANDIDATE A (25 Resumes)
        # ======================================================================
        # Seed 25 resumes with predictable sizes and times to test pagination/sorting
        base_time = datetime(2026, 8, 16, 12, 0, 0, tzinfo=timezone.utc)
        statuses = [ResumeStatus.UPLOADED, ResumeStatus.PROCESSING, ResumeStatus.PROCESSED, ResumeStatus.FAILED]
        run_uid = uuid.uuid4().hex[:6]
        resumes_a = []
        for i in range(1, 26):
            stored_name = f"stored_{run_uid}_{i:02d}.pdf"
            resumes_a.append(Resume(
                id=uuid.uuid4(),
                candidate_profile_id=profile_a_id,
                original_filename=f"resume_{i:02d}.pdf",
                stored_filename=stored_name,
                mime_type="application/pdf",
                file_extension=".pdf",
                file_size_bytes=1000 + i * 100, # 1100 to 3500 bytes
                status=statuses[i % len(statuses)], # cycled status
                version=i,
                is_current=(i == 25), # only the last one is current
                storage_provider="minio",
                bucket_name="talentai-resumes",
                object_key=f"candidates/{profile_a_id}/resumes/{stored_name}",
                uploaded_at=base_time + timedelta(minutes=i) # deterministic ascending timestamps
            ))
        async with SessionLocal() as db:
            db.add_all(resumes_a)
            await db.commit()
        print(f"[OK] Seeded 25 resumes for Candidate A.")

        # ======================================================================
        # TEST 4: Multiple resumes retrieval
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page_size=30", headers=headers_a)
        check("TEST 4: Retrieve all resumes -> 200", res.status_code == 200)
        if res.status_code == 200:
            data = res.json()
            check("TEST 4: items count is 25", len(data["items"]) == 25)
            check("TEST 4: total count is 25", data["total"] == 25)

        # ======================================================================
        # TEST 5: Candidate ownership (Candidate Isolation)
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page_size=30", headers=headers_b)
        check("TEST 5: Candidate B gets only B's resumes", len(res.json()["items"]) == 1)

        # ======================================================================
        # TEST 6: Pagination Page 1
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page=1&page_size=10", headers=headers_a)
        check("TEST 6: Pagination Page 1 -> 200", res.status_code == 200)
        if res.status_code == 200:
            data = res.json()
            check("TEST 6: Item count is 10", len(data["items"]) == 10)
            check("TEST 6: has_next is True", data["has_next"] is True)
            check("TEST 6: has_previous is False", data["has_previous"] is False)

        # ======================================================================
        # TEST 7: Pagination Page 2
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page=2&page_size=10", headers=headers_a)
        check("TEST 7: Pagination Page 2 -> 200", res.status_code == 200)
        if res.status_code == 200:
            data = res.json()
            check("TEST 7: Item count is 10", len(data["items"]) == 10)
            check("TEST 7: has_next is True", data["has_next"] is True)
            check("TEST 7: has_previous is True", data["has_previous"] is True)

        # ======================================================================
        # TEST 8: Pagination Page 3
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page=3&page_size=10", headers=headers_a)
        check("TEST 8: Pagination Page 3 -> 200", res.status_code == 200)
        if res.status_code == 200:
            data = res.json()
            check("TEST 8: Item count is 5", len(data["items"]) == 5)
            check("TEST 8: has_next is False", data["has_next"] is False)
            check("TEST 8: has_previous is True", data["has_previous"] is True)

        # ======================================================================
        # TEST 9: Pagination Metadata
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page=1&page_size=10", headers=headers_a)
        if res.status_code == 200:
            data = res.json()
            check("TEST 9: total is 25", data["total"] == 25)
            check("TEST 9: page is 1", data["page"] == 1)
            check("TEST 9: page_size is 10", data["page_size"] == 10)
            check("TEST 9: total_pages is 3", data["total_pages"] == 3)

        # ======================================================================
        # TEST 10: page_size=1
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page=1&page_size=1", headers=headers_a)
        check("TEST 10: page_size=1 -> 200", res.status_code == 200)
        if res.status_code == 200:
            data = res.json()
            check("TEST 10: Item count is 1", len(data["items"]) == 1)
            check("TEST 10: total_pages is 25", data["total_pages"] == 25)

        # ======================================================================
        # TEST 11: page_size maximum limit
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page_size=51", headers=headers_a)
        check("TEST 11: page_size=51 rejected with 422", res.status_code == 422)

        res = await client.get("/api/v1/candidates/me/resumes?page_size=50", headers=headers_a)
        check("TEST 11: page_size=50 accepted with 200", res.status_code == 200)

        # ======================================================================
        # TEST 12: page=0
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page=0", headers=headers_a)
        check("TEST 12: page=0 rejected with 422", res.status_code == 422)

        # ======================================================================
        # TEST 13: negative page
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?page=-5", headers=headers_a)
        check("TEST 13: negative page rejected with 422", res.status_code == 422)

        # ======================================================================
        # TEST 14: invalid sort_by
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=dangerous_column", headers=headers_a)
        check("TEST 14: invalid sort_by rejected with 400", res.status_code == 400)

        # ======================================================================
        # TEST 15: invalid sort_order
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?sort_order=invalid_dir", headers=headers_a)
        check("TEST 15: invalid sort_order rejected with 400", res.status_code == 400)

        # ======================================================================
        # TEST 16: sort uploaded_at descending
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=uploaded_at&sort_order=desc&page_size=5", headers=headers_a)
        check("TEST 16: sort uploaded_at desc -> 200", res.status_code == 200)
        if res.status_code == 200:
            items = res.json()["items"]
            # Since i ranges 1..25, i=25 was uploaded latest, so desc should return resume_25 first, then resume_24...
            check("TEST 16: Newest first (resume_25)", items[0]["original_filename"] == "resume_25.pdf")
            check("TEST 16: Second newest (resume_24)", items[1]["original_filename"] == "resume_24.pdf")

        # ======================================================================
        # TEST 17: sort uploaded_at ascending
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=uploaded_at&sort_order=asc&page_size=5", headers=headers_a)
        check("TEST 17: sort uploaded_at asc -> 200", res.status_code == 200)
        if res.status_code == 200:
            items = res.json()["items"]
            check("TEST 17: Oldest first (resume_01)", items[0]["original_filename"] == "resume_01.pdf")
            check("TEST 17: Second oldest (resume_02)", items[1]["original_filename"] == "resume_02.pdf")

        # ======================================================================
        # TEST 18: sort file size ascending
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=file_size_bytes&sort_order=asc&page_size=5", headers=headers_a)
        check("TEST 18: sort file size asc -> 200", res.status_code == 200)
        if res.status_code == 200:
            items = res.json()["items"]
            # Smallest size is resume_01 (1100 bytes)
            check("TEST 18: Smallest first (resume_01)", items[0]["original_filename"] == "resume_01.pdf")
            check("TEST 18: Smallest size is 1100", items[0]["file_size_bytes"] == 1100)

        # ======================================================================
        # TEST 19: sort file size descending
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=file_size_bytes&sort_order=desc&page_size=5", headers=headers_a)
        check("TEST 19: sort file size desc -> 200", res.status_code == 200)
        if res.status_code == 200:
            items = res.json()["items"]
            # Largest size is resume_25 (3500 bytes)
            check("TEST 19: Largest first (resume_25)", items[0]["original_filename"] == "resume_25.pdf")
            check("TEST 19: Largest size is 3500", items[0]["file_size_bytes"] == 3500)

        # ======================================================================
        # TEST 20: sort status
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=status&sort_order=asc&page_size=30", headers=headers_a)
        check("TEST 20: sort status asc -> 200", res.status_code == 200)

        # ======================================================================
        # TEST 21: stable sorting
        # ======================================================================
        # Add two resumes with the exact same uploaded_at timestamp to test tie-breaking
        same_time = datetime(2026, 8, 16, 20, 0, 0, tzinfo=timezone.utc)
        u1, u2 = uuid.uuid4(), uuid.uuid4()
        resume_id_x = min(u1, u2)
        resume_id_y = max(u1, u2)
        
        tie_uid = uuid.uuid4().hex[:6]
        async with SessionLocal() as db:
            db.add(Resume(
                id=resume_id_x,
                candidate_profile_id=profile_a_id,
                original_filename="resume_tie_x.pdf",
                stored_filename=f"stored_tie_x_{tie_uid}.pdf",
                mime_type="application/pdf",
                file_extension=".pdf",
                file_size_bytes=2000,
                status=ResumeStatus.UPLOADED,
                version=100,
                is_current=False,
                storage_provider="minio",
                bucket_name="talentai-resumes",
                object_key=f"candidates/{profile_a_id}/resumes/stored_tie_x_{tie_uid}.pdf",
                uploaded_at=same_time
            ))
            db.add(Resume(
                id=resume_id_y,
                candidate_profile_id=profile_a_id,
                original_filename="resume_tie_y.pdf",
                stored_filename=f"stored_tie_y_{tie_uid}.pdf",
                mime_type="application/pdf",
                file_extension=".pdf",
                file_size_bytes=2000,
                status=ResumeStatus.UPLOADED,
                version=101,
                is_current=False,
                storage_provider="minio",
                bucket_name="talentai-resumes",
                object_key=f"candidates/{profile_a_id}/resumes/stored_tie_y_{tie_uid}.pdf",
                uploaded_at=same_time
            ))
            await db.commit()

        # In asc sorting: secondary sort on id (uuid string comparison / uuid asc: 3333... comes before 4444...)
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=uploaded_at&sort_order=asc&page_size=30", headers=headers_a)
        items = res.json()["items"]
        tie_items = [it for it in items if it["id"] in [str(resume_id_x), str(resume_id_y)]]
        check("TEST 21: Stable sort asc tie-breaking", tie_items[0]["id"] == str(resume_id_x) and tie_items[1]["id"] == str(resume_id_y))

        # In desc sorting: secondary sort on id desc (4444... comes before 3333...)
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=uploaded_at&sort_order=desc&page_size=30", headers=headers_a)
        items = res.json()["items"]
        tie_items = [it for it in items if it["id"] in [str(resume_id_x), str(resume_id_y)]]
        check("TEST 21: Stable sort desc tie-breaking", tie_items[0]["id"] == str(resume_id_y) and tie_items[1]["id"] == str(resume_id_x))

        # ======================================================================
        # TEST 22: status returned correctly
        # ======================================================================
        check("TEST 22: status matches enum values", items[0]["status"] in ["uploaded", "processing", "processed", "failed"])

        # ======================================================================
        # TEST 23: file size returned
        # ======================================================================
        check("TEST 23: file size is numeric and accurate", isinstance(items[0]["file_size_bytes"], int))

        # ======================================================================
        # TEST 24: upload date returned
        # ======================================================================
        check("TEST 24: upload date (uploaded_at) is returned", items[0].get("uploaded_at") is not None)

        # ======================================================================
        # TEST 25: current resume returned
        # ======================================================================
        # resume_25.pdf is current
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=version&sort_order=desc&page_size=5", headers=headers_a)
        items = res.json()["items"]
        res_25 = next(it for it in items if it["original_filename"] == "resume_25.pdf")
        check("TEST 25: is_current is True for newest version", res_25["is_current"] is True)
        res_24 = next(it for it in items if it["original_filename"] == "resume_24.pdf")
        check("TEST 25: is_current is False for old versions", res_24["is_current"] is False)

        # ======================================================================
        # TEST 26: current resume uniqueness
        # ======================================================================
        # Verify that only 1 resume has is_current = True for candidate A
        res = await client.get("/api/v1/candidates/me/resumes?page_size=30", headers=headers_a)
        items = res.json()["items"]
        current_resumes = [it for it in items if it["is_current"] is True]
        check("TEST 26: Exactly one current resume", len(current_resumes) == 1)

        # ======================================================================
        # TEST 27: recruiter authorization
        # ======================================================================
        res = await client.get("/api/v1/candidates/me/resumes", headers=headers_r)
        check("TEST 27: Recruiter is Forbidden -> 403", res.status_code == 403)

        # ======================================================================
        # CLEANUP TEST DATA
        # ======================================================================
        print("\n--- CLEANING UP TEST DATA ---")
        async with SessionLocal() as db:
            try:
                from sqlalchemy import delete
                profile_ids = [pid for pid in [profile_a_id, profile_b_id] if pid]
                user_ids = [uid for uid in [user_a_id, user_b_id, rec_id] if uid]
                if profile_ids:
                    await db.execute(delete(Resume).where(Resume.candidate_profile_id.in_(profile_ids)))
                    await db.execute(delete(CandidateProfile).where(CandidateProfile.id.in_(profile_ids)))
                if user_ids:
                    await db.execute(delete(User).where(User.id.in_(user_ids)))
                await db.commit()
                print("✔ Cleaned up all seeded databases entries.")
            except Exception as e:
                print(f"Note: Cleanup encountered an error (ignorable): {e}")

        # ======================================================================
        # SUMMARY
        # ======================================================================
        print("\n============================================================")
        print(f"RESUME LISTING TESTS COMPLETE: {passed} passed, {failed} failed")
        if failed == 0:
            print("ALL RESUME LISTING INTEGRATION TESTS PASSED SUCCESSFULLY!")
        else:
            print(f"WARNING: {failed} test(s) FAILED!")
        print("============================================================\n")
        
        if failed > 0:
            sys.exit(1)

    patcher.stop()

if __name__ == "__main__":
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    asyncio.run(run_resume_listing_tests())
