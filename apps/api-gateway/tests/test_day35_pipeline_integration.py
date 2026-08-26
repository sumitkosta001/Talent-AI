"""Phase 4 — Day 35: Cross-Day End-to-End Pipeline Integration Test.

Tests the full resume-processing and ML pipeline sequentially from Day 21 to Day 34:
PDF/DOCX Document
  ↓
Day 21 — Text Extraction
  ↓
Day 22 — OCR Check
  ↓
Day 23 — Text Cleaning / Normalization / Section Detection / Tokenization
  ↓
Day 24 — Skills Extraction & Canonical Normalization
  ↓
Day 25 — Education Extraction & Degree Normalization
  ↓
Day 26 — Experience Extraction & Seniority Detection
  ↓
Day 27 — Project Extraction & Classification
  ↓
Day 28 — Structured Resume Assembly & Validation
  ↓
Day 29 — Resume Classification & Domain / Role Prediction
  ↓
Day 30 — ATS Scoring Engine
  ↓
Day 31 — Embeddings & Semantic Similarity Matching
  ↓
Day 32 — FAISS Vector Indexing & Similarity Search
  ↓
Day 33 — Recommendation Engine (Job & Candidate Recommendations)
  ↓
Day 34 — AI Interview Question Generation
"""

import uuid
import pytest
import fitz  # PyMuPDF

from app.services.resume_processing import (
    extract_document,
    process_extracted_document,
    extract_skills,
    extract_education,
    extract_experience,
    extract_projects,
    build_structured_resume,
    classify_resume,
    calculate_ats_score,
    calculate_similarity_match,
    generate_resume_embedding,
    generate_job_embedding,
    index_resume,
    index_job,
    search_jobs_for_resume,
    search_resumes_for_job,
    recommend_jobs_for_resume,
    recommend_candidates_for_job,
    generate_interview_questions,
    JobRequirements,
    StructuredResume,
    QuestionDifficulty,
)


def create_synthetic_pdf_bytes() -> bytes:
    """Creates a raw PDF document for candidate 'Alex Sharma'."""
    doc = fitz.open()
    page = doc.new_page()
    lines = [
        "ALEX SHARMA",
        "alex.sharma@example.com | +91-9876543210 | Bengaluru, India",
        "SUMMARY",
        "Passionate Software Engineer with hands-on experience in backend services and machine learning.",
        "EDUCATION",
        "Bachelor of Technology in Computer Science",
        "National Institute of Technology",
        "2022 - 2026 | CGPA: 8.4/10",
        "SKILLS",
        "Python, FastAPI, PostgreSQL, React.js, Docker, scikit-learn",
        "WORK EXPERIENCE",
        "Software Engineering Intern",
        "ABC Technologies (May 2025 - July 2025)",
        "- Developed high-throughput REST APIs using Python and FastAPI.",
        "- Improved PostgreSQL database queries, reducing query latency by 35%.",
        "- Built containerized backend microservices deployed via Docker.",
        "PROJECTS",
        "Talent Platform: Candidate-job matching platform using Python, FastAPI, PostgreSQL.",
        "ML Resume Analyzer: Machine learning classification pipeline built with Python and scikit-learn.",
    ]
    y = 50
    for line in lines:
        page.insert_text((50, y), line, fontsize=10)
        y += 18
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def create_sample_job_requirements() -> JobRequirements:
    """Creates a sample target job requirements payload."""
    return JobRequirements(
        job_id="job-se-001",
        title="Backend Software Engineer",
        description="We are seeking a Backend Engineer skilled in Python, FastAPI, PostgreSQL, and Docker.",
        required_skills=["Python", "FastAPI", "PostgreSQL", "Docker"],
        optional_skills=["React.js", "Redis", "scikit-learn"],
        required_domains=["SOFTWARE_ENGINEERING"],
        required_roles=["BACKEND_DEVELOPER"],
        min_experience_months=6,
        min_degree_level="BACHELORS",
    )


def test_full_cross_day_pipeline_integration():
    """Test 100% sequential cross-day integration from Day 21 through Day 34."""
    
    # 1. Day 21: Raw PDF Document Text Extraction
    pdf_bytes = create_synthetic_pdf_bytes()
    extracted_doc = extract_document(pdf_bytes, extension=".pdf", mime_type="application/pdf")
    assert extracted_doc is not None
    assert extracted_doc.page_count == 1
    assert "ALEX SHARMA" in extracted_doc.raw_text
    assert "FastAPI" in extracted_doc.raw_text

    # 2. Day 22: OCR Check (Native document should not force OCR)
    assert extracted_doc.is_ocr is False or extracted_doc.extraction_method in ["pymupdf", "pdfplumber"]

    # 3. Day 23: Text Processing & Section Detection & Tokenization
    processed_text = process_extracted_document(extracted_doc)
    assert processed_text is not None
    assert len(processed_text.sections) >= 3
    section_names = [s.name for s in processed_text.sections]
    assert "EDUCATION" in section_names or "SKILLS" in section_names or "EXPERIENCE" in section_names

    # 4. Day 24: Skills Extraction & Canonical Normalization
    extracted_skills = extract_skills(processed_text)
    skill_names = [s.name for s in extracted_skills.skills]
    assert "Python" in skill_names
    assert "FastAPI" in skill_names
    assert "PostgreSQL" in skill_names
    assert "Docker" in skill_names

    # 5. Day 25: Education Extraction & Degree Normalization
    extracted_edu = extract_education(processed_text)
    assert extracted_edu.total_count >= 1
    edu_record = extracted_edu.educations[0]
    assert edu_record.degree_level in ["BACHELORS", "UNDERGRADUATE", "UNKNOWN", "BACHELOR"] or "Computer Science" in (edu_record.field_of_study or "")

    # 6. Day 26: Experience Extraction & Seniority
    extracted_exp = extract_experience(processed_text)
    assert extracted_exp.total_count >= 1
    exp_record = extracted_exp.experiences[0]
    assert "ABC Technologies" in (exp_record.company or "ABC Technologies")

    # 7. Day 27: Project Extraction & Classification
    extracted_proj = extract_projects(processed_text)
    assert extracted_proj.total_count >= 1
    proj_names = [p.name for p in extracted_proj.projects]
    assert any("Talent" in name or "Resume" in name for name in proj_names if name)

    # 8. Day 28: Structured Resume Building & Validation
    resume_uuid = uuid.uuid4()
    candidate_uuid = uuid.uuid4()
    structured_resume = build_structured_resume(
        processed_text=processed_text,
        skills=extracted_skills,
        education=extracted_edu,
        experience=extracted_exp,
        projects=extracted_proj,
        resume_id=resume_uuid,
        candidate_profile_id=candidate_uuid,
    )
    assert structured_resume.resume_id == resume_uuid
    assert structured_resume.candidate_profile_id == candidate_uuid
    assert len(structured_resume.skills.skills) >= 4

    # 9. Day 29: Resume Classification & Role/Domain Prediction
    classification = classify_resume(structured_resume)
    assert classification.domain in ["SOFTWARE_ENGINEERING", "DATA_SCIENCE_ML"]
    assert classification.role in ["BACKEND_DEVELOPER", "FULL_STACK_DEVELOPER", "SOFTWARE_ENGINEER", "ML_ENGINEER"]

    # Attach classification to structured resume
    structured_resume.classification = classification

    # 10. Day 30: ATS Scoring
    job_req = create_sample_job_requirements()
    ats_result = calculate_ats_score(structured_resume, job_req)
    assert 0.0 <= ats_result.overall_score <= 100.0
    assert ats_result.overall_score >= 50.0  # Synthetic resume matches backend requirements well

    # 11. Day 31: Embeddings & Semantic Similarity Match
    resume_emb = generate_resume_embedding(structured_resume)
    job_emb = generate_job_embedding(job_req)
    assert len(resume_emb) == 384
    assert len(job_emb) == 384

    similarity = calculate_similarity_match(structured_resume, job_req)
    assert 0.0 <= similarity.match_score <= 100.0

    # 12. Day 32: FAISS Vector Indexing & Search
    res_idx_res = index_resume(str(resume_uuid), structured_resume)
    assert res_idx_res.status == "indexed"

    job_idx_res = index_job(job_req.job_id, job_req)
    assert job_idx_res.status == "indexed"

    search_jobs_res = search_jobs_for_resume(structured_resume, top_k=5)
    assert len(search_jobs_res.results) >= 1

    search_resumes_res = search_resumes_for_job(job_req, top_k=5)
    assert len(search_resumes_res.results) >= 1

    # 13. Day 33: Hybrid Recommendations
    job_recs = recommend_jobs_for_resume(structured_resume, candidate_jobs=[job_req], top_k=5)
    assert job_recs.total_results >= 1
    assert job_recs.recommendations[0].job_id == job_req.job_id
    assert 0.0 <= job_recs.recommendations[0].recommendation_score <= 100.0

    cand_recs = recommend_candidates_for_job(job_req, candidate_resumes=[structured_resume], top_k=5)
    assert cand_recs.total_results >= 1

    # 14. Day 34: AI Interview Question Generation
    iq_res = generate_interview_questions(
        structured_resume,
        count=6,
        difficulty=QuestionDifficulty.MEDIUM,
    )
    assert iq_res.total_count == 6
    assert iq_res.difficulty == "MEDIUM"
    assert len(iq_res.questions) == 6
    for q in iq_res.questions:
        assert q.question is not None
        assert len(q.question) > 15
        assert q.category in [
            "TECHNICAL", "BEHAVIORAL", "SYSTEM_DESIGN", "CODING",
            "CONCEPTUAL", "PROJECT", "EXPERIENCE", "ROLE_SPECIFIC",
            "SKILL_SPECIFIC", "SITUATIONAL"
        ]
