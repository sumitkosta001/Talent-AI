"""Integration Test Suite for Resume Versioning API (Day 16).

Tests:
- Version auto-increment on upload
- is_current flag management across uploads
- GET /current endpoint
- POST /restore endpoint
- Auto-promotion on delete
- Listing includes version/is_current metadata
- Edge cases and error handling
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
    """Helper to upload a resume and return the response JSON."""
    content = make_valid_pdf_content(size)
    files = {"file": (filename, io.BytesIO(content), "application/pdf")}
    res = await client.post("/api/v1/candidates/me/resumes", headers=headers, files=files)
    return res


async def run_resume_versioning_tests():
    patcher = patch("app.services.email_service.EmailService.send_verification_email", new_callable=AsyncMock)
    patcher.start()

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        print("\n============================================================", flush=True)
        print("RUNNING RESUME VERSIONING INTEGRATION TESTS (DAY 16)", flush=True)
        print("============================================================", flush=True)

        passed = 0
        failed = 0
        total = 0

        def check(test_name, condition, detail=""):
            nonlocal passed, failed, total
            total += 1
            if condition:
                passed += 1
                print(f"  PASS [{total:02d}] {test_name}", flush=True)
            else:
                failed += 1
                print(f"  FAIL [{total:02d}] {test_name} — {detail}", flush=True)

        # ==============================================================
        # SETUP: Create candidate A, candidate B
        # ==============================================================
        password = "Password123!"
        email_a = f"ver_cand_a_{uuid.uuid4().hex[:6]}@example.com"
        email_b = f"ver_cand_b_{uuid.uuid4().hex[:6]}@example.com"

        # Register Candidate A
        res = await client.post("/api/v1/auth/register", json={
            "email": email_a, "password": password, "confirm_password": password,
            "first_name": "Version", "last_name": "CandA",
        })
        assert res.status_code == 201, f"Register A failed: {res.text}"
        user_a_id = uuid.UUID(res.json()["user"]["id"])

        # Register Candidate B
        res = await client.post("/api/v1/auth/register", json={
            "email": email_b, "password": password, "confirm_password": password,
            "first_name": "Version", "last_name": "CandB",
        })
        assert res.status_code == 201
        user_b_id = uuid.UUID(res.json()["user"]["id"])

        # Mark verified & set roles
        async with SessionLocal() as db:
            for uid in [user_a_id, user_b_id]:
                u = await db.get(User, uid)
                if u:
                    u.is_verified = True
                    u.role = UserRole.CANDIDATE
            await db.commit()

        # Login
        res = await client.post("/api/v1/auth/login", json={"email": email_a, "password": password})
        token_a = res.json()["tokens"]["access_token"]
        headers_a = {"Authorization": f"Bearer {token_a}"}

        res = await client.post("/api/v1/auth/login", json={"email": email_b, "password": password})
        token_b = res.json()["tokens"]["access_token"]
        headers_b = {"Authorization": f"Bearer {token_b}"}

        # Trigger profile creation
        await client.get("/api/v1/candidates/me", headers=headers_a)
        await client.get("/api/v1/candidates/me", headers=headers_b)

        # ==============================================================
        # TEST GROUP 1: VERSION AUTO-INCREMENT
        # ==============================================================
        print("\n--- Version Auto-Increment ---", flush=True)

        # Upload first resume (v1)
        res1 = await upload_resume_file(client, headers_a, "resume_v1.pdf")
        check("First upload returns 201", res1.status_code == 201, f"got {res1.status_code}")
        d1 = res1.json()["resume"]
        resume_v1_id = d1["id"]
        check("First upload has version=1", d1["version"] == 1, f"got {d1['version']}")
        check("First upload has is_current=True", d1["is_current"] is True, f"got {d1['is_current']}")

        # Upload second resume (v2)
        res2 = await upload_resume_file(client, headers_a, "resume_v2.pdf")
        check("Second upload returns 201", res2.status_code == 201, f"got {res2.status_code}")
        d2 = res2.json()["resume"]
        resume_v2_id = d2["id"]
        check("Second upload has version=2", d2["version"] == 2, f"got {d2['version']}")
        check("Second upload has is_current=True", d2["is_current"] is True, f"got {d2['is_current']}")

        # Upload third resume (v3)
        res3 = await upload_resume_file(client, headers_a, "resume_v3.pdf")
        check("Third upload returns 201", res3.status_code == 201, f"got {res3.status_code}")
        d3 = res3.json()["resume"]
        resume_v3_id = d3["id"]
        check("Third upload has version=3", d3["version"] == 3, f"got {d3['version']}")
        check("Third upload has is_current=True", d3["is_current"] is True, f"got {d3['is_current']}")

        # ==============================================================
        # TEST GROUP 2: is_current MANAGEMENT
        # ==============================================================
        print("\n--- is_current Management ---", flush=True)

        # Check v1 is no longer current
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_v1_id}", headers=headers_a)
        check("v1 is no longer current", res.json()["is_current"] is False, f"got {res.json().get('is_current')}")

        # Check v2 is no longer current
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_v2_id}", headers=headers_a)
        check("v2 is no longer current", res.json()["is_current"] is False, f"got {res.json().get('is_current')}")

        # Check v3 is still current
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_v3_id}", headers=headers_a)
        check("v3 is current", res.json()["is_current"] is True, f"got {res.json().get('is_current')}")

        # ==============================================================
        # TEST GROUP 3: GET /current ENDPOINT
        # ==============================================================
        print("\n--- GET /current Endpoint ---", flush=True)

        res = await client.get("/api/v1/candidates/me/resumes/current", headers=headers_a)
        check("GET /current returns 200", res.status_code == 200, f"got {res.status_code}")
        cur = res.json()
        check("GET /current returns v3", cur["id"] == resume_v3_id, f"got {cur.get('id')}")
        check("GET /current shows is_current=True", cur["is_current"] is True)
        check("GET /current shows version=3", cur["version"] == 3, f"got {cur.get('version')}")

        # Unauthenticated
        res = await client.get("/api/v1/candidates/me/resumes/current")
        check("GET /current unauthenticated returns 401", res.status_code == 401, f"got {res.status_code}")

        # Candidate B has no resumes
        res = await client.get("/api/v1/candidates/me/resumes/current", headers=headers_b)
        check("GET /current with no resumes returns 404", res.status_code == 404, f"got {res.status_code}")

        # ==============================================================
        # TEST GROUP 4: POST /restore ENDPOINT
        # ==============================================================
        print("\n--- POST /restore Endpoint ---", flush=True)

        # Restore v1 as current
        res = await client.post(f"/api/v1/candidates/me/resumes/{resume_v1_id}/restore", headers=headers_a)
        check("Restore v1 returns 200", res.status_code == 200, f"got {res.status_code}: {res.text}")
        rd = res.json()
        check("Restore response has success=True", rd["success"] is True)
        check("Restored resume is v1", rd["resume"]["id"] == resume_v1_id)
        check("Restored resume is_current=True", rd["resume"]["is_current"] is True)

        # Verify v3 is no longer current
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_v3_id}", headers=headers_a)
        check("After restore v1: v3 is no longer current", res.json()["is_current"] is False)

        # Verify v2 is still not current
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_v2_id}", headers=headers_a)
        check("After restore v1: v2 is still not current", res.json()["is_current"] is False)

        # GET /current should return v1 now
        res = await client.get("/api/v1/candidates/me/resumes/current", headers=headers_a)
        check("GET /current now returns v1", res.json()["id"] == resume_v1_id)

        # ==============================================================
        # TEST GROUP 5: RESTORE EDGE CASES
        # ==============================================================
        print("\n--- Restore Edge Cases ---", flush=True)

        # Restore already-current resume → 400
        res = await client.post(f"/api/v1/candidates/me/resumes/{resume_v1_id}/restore", headers=headers_a)
        check("Restore already-current returns 400", res.status_code == 400, f"got {res.status_code}: {res.text}")

        # Restore nonexistent resume → 404
        fake_id = str(uuid.uuid4())
        res = await client.post(f"/api/v1/candidates/me/resumes/{fake_id}/restore", headers=headers_a)
        check("Restore nonexistent resume returns 404", res.status_code == 404, f"got {res.status_code}")

        # Restore with no auth → 401
        res = await client.post(f"/api/v1/candidates/me/resumes/{resume_v2_id}/restore")
        check("Restore unauthenticated returns 401", res.status_code == 401, f"got {res.status_code}")

        # IDOR: Candidate B tries to restore Candidate A's resume
        res = await client.post(f"/api/v1/candidates/me/resumes/{resume_v2_id}/restore", headers=headers_b)
        check("IDOR: B cannot restore A's resume (404)", res.status_code == 404, f"got {res.status_code}")

        # ==============================================================
        # TEST GROUP 6: RESTORE THEN UPLOAD (version continues from max)
        # ==============================================================
        print("\n--- Restore Then Upload ---", flush=True)

        # Currently v1 is current. Upload v4.
        res4 = await upload_resume_file(client, headers_a, "resume_v4.pdf")
        check("Upload after restore returns 201", res4.status_code == 201, f"got {res4.status_code}")
        d4 = res4.json()["resume"]
        resume_v4_id = d4["id"]
        check("New upload after restore is version=4", d4["version"] == 4, f"got {d4['version']}")
        check("New upload is_current=True", d4["is_current"] is True)

        # v1 should no longer be current
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_v1_id}", headers=headers_a)
        check("After v4 upload: v1 no longer current", res.json()["is_current"] is False)

        # ==============================================================
        # TEST GROUP 7: DELETE + AUTO-PROMOTION
        # ==============================================================
        print("\n--- Delete + Auto-Promotion ---", flush=True)

        # v4 is current. Delete v4 → v3 should be promoted.
        res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_v4_id}", headers=headers_a)
        check("Delete v4 returns 200", res.status_code == 200, f"got {res.status_code}")

        # v3 should now be current
        res = await client.get(f"/api/v1/candidates/me/resumes/{resume_v3_id}", headers=headers_a)
        check("After deleting v4: v3 is auto-promoted to current", res.json()["is_current"] is True, f"got {res.json().get('is_current')}")

        # GET /current should return v3
        res = await client.get("/api/v1/candidates/me/resumes/current", headers=headers_a)
        check("GET /current returns v3 after auto-promotion", res.json()["id"] == resume_v3_id)

        # Delete non-current (v2) → no promotion change
        res = await client.delete(f"/api/v1/candidates/me/resumes/{resume_v2_id}", headers=headers_a)
        check("Delete non-current v2 returns 200", res.status_code == 200, f"got {res.status_code}")

        # v3 should still be current
        res = await client.get("/api/v1/candidates/me/resumes/current", headers=headers_a)
        check("After deleting non-current v2: v3 still current", res.json()["id"] == resume_v3_id)

        # ==============================================================
        # TEST GROUP 8: VERSION NEVER REUSES DELETED NUMBERS
        # ==============================================================
        print("\n--- Version Number Non-Reuse ---", flush=True)

        # v2 and v4 are deleted. Upload v5 — must NOT be v2 or v4.
        res5 = await upload_resume_file(client, headers_a, "resume_v5.pdf")
        check("Upload after delete returns 201", res5.status_code == 201, f"got {res5.status_code}")
        d5 = res5.json()["resume"]
        resume_v5_id = d5["id"]
        check("Version after deleting v2 and v4 is v5 (not v2)", d5["version"] == 5, f"got {d5['version']}")

        # ==============================================================
        # TEST GROUP 9: RESTORE DELETED RESUME → 404
        # ==============================================================
        print("\n--- Restore Deleted Resume ---", flush=True)

        res = await client.post(f"/api/v1/candidates/me/resumes/{resume_v4_id}/restore", headers=headers_a)
        check("Restore deleted resume returns 404", res.status_code == 404, f"got {res.status_code}")

        res = await client.post(f"/api/v1/candidates/me/resumes/{resume_v2_id}/restore", headers=headers_a)
        check("Restore another deleted resume returns 404", res.status_code == 404, f"got {res.status_code}")

        # ==============================================================
        # TEST GROUP 10: LISTING INCLUDES VERSION METADATA
        # ==============================================================
        print("\n--- Listing Includes Version Metadata ---", flush=True)

        res = await client.get("/api/v1/candidates/me/resumes", headers=headers_a)
        check("Listing returns 200", res.status_code == 200, f"got {res.status_code}")
        items = res.json()["items"]
        check("Listing shows 3 active resumes (v1, v3, v5)", len(items) == 3, f"got {len(items)}")

        # Check all items have version and is_current fields
        all_have_version = all("version" in item for item in items)
        all_have_is_current = all("is_current" in item for item in items)
        check("All listed resumes have 'version' field", all_have_version)
        check("All listed resumes have 'is_current' field", all_have_is_current)

        # Sort by version asc
        res = await client.get("/api/v1/candidates/me/resumes?sort_by=version&sort_order=asc", headers=headers_a)
        sorted_items = res.json()["items"]
        versions = [item["version"] for item in sorted_items]
        check("Sort by version asc works correctly", versions == sorted(versions), f"got {versions}")

        # ==============================================================
        # TEST GROUP 11: DELETE ALL → NO CURRENT
        # ==============================================================
        print("\n--- Delete All Resumes ---", flush=True)

        # Delete v1, v3, v5 (all remaining)
        for rid, vlabel in [(resume_v1_id, "v1"), (resume_v3_id, "v3"), (resume_v5_id, "v5")]:
            res = await client.delete(f"/api/v1/candidates/me/resumes/{rid}", headers=headers_a)
            check(f"Delete {vlabel} returns 200", res.status_code == 200, f"got {res.status_code}")

        # GET /current should return 404
        res = await client.get("/api/v1/candidates/me/resumes/current", headers=headers_a)
        check("GET /current returns 404 after all deleted", res.status_code == 404, f"got {res.status_code}")

        # List should be empty
        res = await client.get("/api/v1/candidates/me/resumes", headers=headers_a)
        check("Listing returns 0 after all deleted", res.json()["total"] == 0, f"got {res.json()['total']}")

        # ==============================================================
        # TEST GROUP 12: FRESH UPLOAD AFTER ALL DELETED
        # ==============================================================
        print("\n--- Fresh Upload After All Deleted ---", flush=True)

        # Version should continue from 5 (never reuse)
        res6 = await upload_resume_file(client, headers_a, "resume_fresh.pdf")
        check("Fresh upload after all deleted returns 201", res6.status_code == 201, f"got {res6.status_code}")
        d6 = res6.json()["resume"]
        check("Fresh upload version is 6 (continues from max)", d6["version"] == 6, f"got {d6['version']}")
        check("Fresh upload is_current=True", d6["is_current"] is True)

        # GET /current now works
        res = await client.get("/api/v1/candidates/me/resumes/current", headers=headers_a)
        check("GET /current returns 200 after fresh upload", res.status_code == 200, f"got {res.status_code}")

        # ==============================================================
        # TEST GROUP 13: CANDIDATE ISOLATION
        # ==============================================================
        print("\n--- Candidate Isolation ---", flush=True)

        # Candidate B uploads their own resume
        resb1 = await upload_resume_file(client, headers_b, "b_resume.pdf")
        check("Candidate B upload returns 201", resb1.status_code == 201, f"got {resb1.status_code}")
        db1 = resb1.json()["resume"]
        check("Candidate B's first upload is version=1", db1["version"] == 1, f"got {db1['version']}")

        # A's version counter is independent from B's
        res7 = await upload_resume_file(client, headers_a, "resume_v7.pdf")
        check("A's next upload is version=7 (independent of B)", res7.json()["resume"]["version"] == 7, f"got {res7.json()['resume']['version']}")

        # ==============================================================
        # SUMMARY
        # ==============================================================
        print("\n============================================================", flush=True)
        print(f"RESUME VERSIONING TESTS: {passed} passed, {failed} failed, {total} total", flush=True)
        print("============================================================\n", flush=True)

        if failed > 0:
            sys.exit(1)

    patcher.stop()


if __name__ == "__main__":
    asyncio.run(run_resume_versioning_tests())
