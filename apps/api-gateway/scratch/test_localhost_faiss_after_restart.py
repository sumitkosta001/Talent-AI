"""Post-Server-Restart FAISS Verification Script.

Queries the live server after restart to verify FAISS vector indices and metadata
persisted on disk in data/faiss/ survive application restart.
"""

import sys
import asyncio
import httpx


async def run_restart_verification():
    base_url = "http://127.0.0.1:8000"
    client = httpx.AsyncClient(base_url=base_url, timeout=30.0)

    print("==================================================================")
    print("VERIFYING FAISS PERSISTENCE AFTER SERVER RESTART")
    print("==================================================================")

    # 1. Check Job FAISS status
    status_resp = await client.get("/api/v1/jobs/faiss-status")
    assert status_resp.status_code == 200, f"FAISS status failed: {status_resp.text}"
    status_data = status_resp.json()
    print(f"1. Job FAISS Index Status: {status_data}")
    assert status_data["vector_count"] >= 2, f"Expected at least 2 vectors in job index, got {status_data['vector_count']}"

    # 2. Perform search on persisted job index
    py_job_req = {
        "job_id": "job-py-dev-101",
        "title": "Senior Python Backend Engineer",
        "description": "Seeking a Senior Python Backend Developer skilled in FastAPI, PostgreSQL, Docker, and FAISS vector search.",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "FAISS"],
        "required_domains": ["Software Engineering"],
        "required_roles": ["Backend Developer"],
        "required_experience_level": "Senior",
    }

    print("2. Performing vector search on persisted FAISS index after server restart...")
    search_resumes_resp = await client.post("/api/v1/jobs/search-resumes?top_k=10", json=py_job_req)
    assert search_resumes_resp.status_code == 200, f"Resume search failed: {search_resumes_resp.text}"
    search_data = search_resumes_resp.json()

    print(f"   Retrieved {search_data['total_results']} matching resumes from persisted FAISS index:")
    for item in search_data["results"]:
        print(f"     - Resume ID: {item['entity_id']} | Score: {item['similarity_score']}/100 ({item['similarity_tier']})")

    assert search_data["total_results"] > 0, "No results returned from persisted FAISS index after restart!"
    print("\n==================================================================")
    print("PERSISTENCE AFTER SERVER RESTART VERIFIED 100% SUCCESS!")
    print("==================================================================")
    await client.aclose()


if __name__ == "__main__":
    asyncio.run(run_restart_verification())
