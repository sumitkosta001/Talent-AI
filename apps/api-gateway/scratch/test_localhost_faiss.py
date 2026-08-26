"""Localhost Live Server Verification Script for Day 32 FAISS Vector Indexing & Search.

Executes end-to-end API calls against live Uvicorn server (http://127.0.0.1:8000):
1. Registers candidate user and logs in.
2. Uploads sample resume PDF and triggers Day 21-28 processing pipeline.
3. Indexes processed candidate resume into FAISS Resume Index via API.
4. Indexes two jobs (Python Developer vs Graphic Designer) into FAISS Job Index via API.
5. Searches Job FAISS Index using Candidate Resume vector via API.
6. Searches Resume FAISS Index using Job Requirements vector via API.
7. Verifies relative ranking quality (Python job ranks higher than Graphic Designer job).
8. Verifies index persistence and status endpoints.
"""

import io
import sys
import time
import asyncio
import httpx
import fitz  # PyMuPDF


def create_sample_resume_pdf() -> bytes:
    """Generates a sample PDF resume in memory."""
    doc = fitz.open()
    page = doc.new_page()

    text = (
        "Alice Smith\n"
        "Email: alice.smith@example.com | Phone: +1-555-0199\n"
        "Summary: Senior Python Backend Engineer with 5 years of experience in FastAPI, PostgreSQL, Docker, and FAISS vector databases.\n\n"
        "SKILLS:\n"
        "Python, FastAPI, PostgreSQL, Docker, FAISS, PyTest, REST APIs, Microservices, AsyncIO\n\n"
        "EXPERIENCE:\n"
        "TechCorp Inc - Senior Python Engineer (2020 - Present)\n"
        "- Developed high performance REST APIs using FastAPI and PostgreSQL.\n"
        "- Implemented vector search services using FAISS and sentence-transformers.\n"
        "- Containerized microservices using Docker.\n\n"
        "EDUCATION:\n"
        "Bachelor of Science in Computer Science - Stanford University (2019)\n\n"
        "PROJECTS:\n"
        "TalentAI API Gateway: Built AI search service using FAISS and Python.\n"
    )

    page.insert_text(fitz.Point(50, 50), text, fontsize=11)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


async def run_localhost_faiss_verification():
    base_url = "http://127.0.0.1:8000"
    client = httpx.AsyncClient(base_url=base_url, timeout=30.0)

    print("==================================================================")
    print("DAY 32 — LOCALHOST FAISS VERIFICATION")
    print("==================================================================")

    # 1. Register candidate user
    email = f"faiss_test_{int(time.time())}@example.com"
    password = "TestPassword123!"

    print(f"1. Registering candidate user ({email})...")
    reg_resp = await client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "confirm_password": password,
        "first_name": "Alice",
        "last_name": "Smith",
        "role": "candidate",
    })


    if reg_resp.status_code not in (200, 201):
        print(f"FAILED to register user: {reg_resp.status_code} - {reg_resp.text}")
        sys.exit(1)

    reg_data = reg_resp.json()
    token = reg_data.get("tokens", {}).get("access_token") or reg_data.get("access_token")
    assert token, "Access token missing from registration response"
    headers = {"Authorization": f"Bearer {token}"}
    print("   User registered and authenticated successfully.")

    # 2. Upload resume PDF
    print("2. Uploading sample resume PDF...")
    pdf_bytes = create_sample_resume_pdf()
    files = {"file": ("alice_smith_resume.pdf", pdf_bytes, "application/pdf")}
    upload_resp = await client.post("/api/v1/candidates/me/resumes", headers=headers, files=files)
    assert upload_resp.status_code == 201, f"Resume upload failed: {upload_resp.text}"
    resume_data = upload_resp.json()
    resume_id = resume_data["id"]
    print(f"   Uploaded resume ID: {resume_id}")

    # 3. Process resume (Days 21-28)
    print("3. Processing resume into structured representation...")
    proc_resp = await client.post(f"/api/v1/candidates/me/resumes/{resume_id}/process", headers=headers)
    assert proc_resp.status_code == 200, f"Resume processing failed: {proc_resp.text}"
    proc_data = proc_resp.json()
    assert proc_data["status"] == "processed"
    print("   Resume processed successfully. Structured data present.")

    # 4. Index candidate resume into FAISS
    print("4. Indexing candidate resume vector into Resume FAISS index...")
    idx_res_resp = await client.post(f"/api/v1/candidates/me/resumes/{resume_id}/faiss-index", headers=headers)
    assert idx_res_resp.status_code == 200, f"FAISS resume indexing failed: {idx_res_resp.text}"
    idx_res_data = idx_res_resp.json()
    print(f"   Indexed Resume ID: {idx_res_data['entity_id']}, Total vectors: {idx_res_data['vector_count']}")

    # 5. Index jobs into Job FAISS index
    print("5. Indexing realistic jobs into Job FAISS index...")
    py_job_req = {
        "job_id": "job-py-dev-101",
        "title": "Senior Python Backend Engineer",
        "description": "Seeking a Senior Python Backend Developer skilled in FastAPI, PostgreSQL, Docker, and FAISS vector search.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "FAISS"],
        "required_domains": ["Software Engineering"],
        "required_roles": ["Backend Developer"],
        "required_experience_level": "Senior",
    }
    design_job_req = {
        "job_id": "job-design-202",
        "title": "Creative UI/UX Graphic Designer",
        "description": "Looking for a Visual Designer skilled in Adobe Photoshop, Figma, Illustrator, and typography.",
        "required_skills": ["Figma", "Photoshop", "Illustrator"],
        "required_domains": ["Design & Creative"],
        "required_roles": ["UI/UX Designer"],
        "required_experience_level": "Senior",
    }

    job1_resp = await client.post("/api/v1/jobs/index", json=py_job_req)
    assert job1_resp.status_code == 200, f"Job 1 indexing failed: {job1_resp.text}"
    print(f"   Job 1 (Python) indexed: {job1_resp.json()['entity_id']}")

    job2_resp = await client.post("/api/v1/jobs/index", json=design_job_req)
    assert job2_resp.status_code == 200, f"Job 2 indexing failed: {job2_resp.text}"
    print(f"   Job 2 (Design) indexed: {job2_resp.json()['entity_id']}")

    # Check Job FAISS status
    status_resp = await client.get("/api/v1/jobs/faiss-status")
    assert status_resp.status_code == 200
    print(f"   Job FAISS Index Status: {status_resp.json()}")

    # 6. Search Job FAISS Index using Candidate Resume vector
    print("6. Searching Job FAISS index using candidate resume vector...")
    search_jobs_resp = await client.post(f"/api/v1/candidates/me/resumes/{resume_id}/search-jobs?top_k=10", headers=headers)
    assert search_jobs_resp.status_code == 200, f"Job search failed: {search_jobs_resp.text}"
    search_jobs_data = search_jobs_resp.json()
    print(f"   Found {search_jobs_data['total_results']} matching jobs:")
    for item in search_jobs_data["results"]:
        print(f"     - Entity ID: {item['entity_id']} | Score: {item['similarity_score']}/100 ({item['similarity_tier']}) | Raw Cosine: {item['raw_similarity']}")

    top_job = search_jobs_data["results"][0]
    assert top_job["entity_id"] == "job-py-dev-101", f"Expected top match 'job-py-dev-101', got '{top_job['entity_id']}'"
    print("   PASSED: Python job ranked HIGHER than Graphic Designer job!")

    # 7. Search Resume FAISS Index using Job Requirements vector
    print("7. Searching Resume FAISS index using Python Job requirements vector...")
    search_resumes_resp = await client.post("/api/v1/jobs/search-resumes?top_k=10", json=py_job_req)
    assert search_resumes_resp.status_code == 200, f"Resume search failed: {search_resumes_resp.text}"
    search_resumes_data = search_resumes_resp.json()
    print(f"   Found {search_resumes_data['total_results']} matching candidate resumes:")
    for item in search_resumes_data["results"]:
        print(f"     - Resume ID: {item['entity_id']} | Score: {item['similarity_score']}/100 ({item['similarity_tier']}) | Raw Cosine: {item['raw_similarity']}")

    assert search_resumes_data["results"][0]["entity_id"] == str(resume_id)
    print("   PASSED: Candidate resume correctly retrieved from FAISS Resume Index!")

    print("\n==================================================================")
    print("ALL DAY 32 LOCALHOST FAISS VERIFICATIONS PASSED 100%!")
    print("==================================================================")
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(run_localhost_faiss_verification())
