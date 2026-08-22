"""Localhost integration test script for Day 31 Similarity Score API."""

import httpx, json, sys

BASE_URL = "http://127.0.0.1:8000/api/v1"
CANDIDATE_EMAIL = "candidate@example.com"
CANDIDATE_PASSWORD = "Candidate123!"

def test_localhost_similarity_api():
    client = httpx.Client(base_url=BASE_URL, timeout=30.0)

    # 1. Login
    print("1. Logging in as candidate...")
    login_resp = client.post("/auth/login", json={"email": CANDIDATE_EMAIL, "password": CANDIDATE_PASSWORD})
    if login_resp.status_code != 200:
        print(f"FAILED to login: {login_resp.status_code} {login_resp.text}")
        sys.exit(1)

    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful.")

    # 2. Get resumes
    print("2. Fetching candidate resumes...")
    res_resp = client.get("/candidates/me/resumes", headers=headers)
    if res_resp.status_code != 200:
        print(f"FAILED to fetch resumes: {res_resp.status_code} {res_resp.text}")
        sys.exit(1)

    resumes = res_resp.json()
    if isinstance(resumes, dict) and "items" in resumes:
        resumes = resumes["items"]

    if not resumes:
        print("No resumes found for candidate.")
        sys.exit(1)

    processed_resume = None
    for r in resumes:
        if r.get("structured_data"):
            processed_resume = r
            break

    if not processed_resume:
        print("No processed resume with structured_data found. Please process a resume first.")
        sys.exit(1)

    resume_id = processed_resume["id"]
    print(f"Using Resume ID: {resume_id}")

    # 3. Test Matching Job Similarity Score
    python_job = {
        "job_id": "job-python-101",
        "title": "Senior Python Backend Engineer",
        "description": "Building scalable microservices with Python, FastAPI, PostgreSQL, and Docker containers.",
        "required_keywords": ["Python", "FastAPI", "PostgreSQL"],
        "required_skills": ["Python", "FastAPI"],
        "required_education": ["Bachelor of Science"],
        "required_roles": ["Backend Developer", "Software Engineer"],
        "required_domains": ["Software Engineering"],
    }

    print("3. Testing similarity score endpoint for matching Python job...")
    match_resp = client.post(
        f"/candidates/me/resumes/{resume_id}/similarity-score",
        headers=headers,
        json=python_job,
    )
    if match_resp.status_code != 200:
        print(f"FAILED similarity score request: {match_resp.status_code} {match_resp.text}")
        sys.exit(1)

    match_result = match_resp.json()
    print("Matching Job Result:")
    print(json.dumps(match_result, indent=2))

    # 4. Test Unrelated Job Similarity Score
    designer_job = {
        "job_id": "job-design-202",
        "title": "Graphic Designer & Illustrator",
        "description": "Create visual assets, logos, and digital branding using Adobe Photoshop, Illustrator, and Figma.",
        "required_keywords": ["Photoshop", "Illustrator", "Figma"],
        "required_skills": ["Photoshop", "Illustrator"],
        "required_roles": ["Graphic Designer"],
        "required_domains": ["Design & Creative"],
    }

    print("4. Testing similarity score endpoint for unrelated Graphic Designer job...")
    unrelated_resp = client.post(
        f"/candidates/me/resumes/{resume_id}/similarity-score",
        headers=headers,
        json=designer_job,
    )
    if unrelated_resp.status_code != 200:
        print(f"FAILED similarity score request: {unrelated_resp.status_code} {unrelated_resp.text}")
        sys.exit(1)

    unrelated_result = unrelated_resp.json()
    print("Unrelated Job Result:")
    print(json.dumps(unrelated_result, indent=2))

    # 5. Assertions
    rel_score = match_result["similarity_score"]
    unrel_score = unrelated_result["similarity_score"]
    assert rel_score > unrel_score, f"Matching score ({rel_score}) should be > Unrelated score ({unrel_score})"
    assert match_result["model_name"] == "sentence-transformers/all-MiniLM-L6-v2"
    assert match_result["embedding_dimension"] == 384

    print("\nSUCCESS: All localhost HTTP API similarity score tests passed 100%!")

if __name__ == "__main__":
    test_localhost_similarity_api()
