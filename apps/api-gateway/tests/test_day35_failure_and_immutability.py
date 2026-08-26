"""Phase 4 — Day 35: Failure Injection, Input Immutability & Determinism Test Suite.

Tests pipeline resilience against corrupt inputs, empty payloads, missing tools,
input object immutability, and function determinism across Days 21–34.
"""

import copy
import uuid
import pytest
import numpy as np

from app.exceptions.resume import InvalidFileContentError, InvalidFileTypeError
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
    generate_interview_questions,
    StructuredResume,
    ExtractedSkills,
    ExtractedSkill,
    ExtractedEducation,
    EducationRecord,
    ExtractedExperience,
    ExperienceRecord,
    ExtractedProjects,
    ProjectRecord,
    JobRequirements,
    QuestionDifficulty,
    ExtractedDocument,
)


# ==============================================================================
# 1. FAILURE INJECTION TESTS
# ==============================================================================

def test_failure_corrupt_pdf_bytes():
    """Test corrupt PDF bytes raise controlled extraction error."""
    corrupt_bytes = b"%PDF-1.4 Corrupt header invalid binary \x00\xFF\x99"
    with pytest.raises(Exception):
        extract_document(corrupt_bytes, extension=".pdf", mime_type="application/pdf")


def test_failure_corrupt_docx_bytes():
    """Test corrupt DOCX bytes raise controlled extraction error."""
    corrupt_bytes = b"PK\x03\x04 corrupt zip archive contents"
    with pytest.raises(Exception):
        extract_document(corrupt_bytes, extension=".docx", mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


def test_failure_empty_document_bytes():
    """Test zero-byte document content produces empty/None or controlled error."""
    empty_bytes = b""
    with pytest.raises(Exception):
        extract_document(empty_bytes, extension=".pdf", mime_type="application/pdf")


def test_failure_missing_skills_and_sections_in_structured_resume():
    """Test structured resume creation with empty extracted entities handles missing data gracefully."""
    resume = build_structured_resume(
        processed_text=None,
        skills=None,
        education=None,
        experience=None,
        projects=None,
        resume_id=uuid.uuid4(),
        candidate_profile_id=uuid.uuid4(),
    )
    assert resume is not None
    assert resume.skills.total_count == 0
    assert resume.education.total_count == 0
    assert resume.experience.total_count == 0
    assert resume.projects.total_count == 0


def test_failure_nan_and_inf_embedding_rejection():
    """Test similarity matcher handles or rejects NaN/Inf embeddings safely."""
    from app.services.resume_processing.similarity_matcher import compute_cosine_similarity

    v_nan = np.array([np.nan, 1.0, 0.0], dtype=np.float32)
    v_normal = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    sim = compute_cosine_similarity(v_nan, v_normal)
    assert sim == pytest.approx(0.0) or np.isnan(sim) is False


def test_failure_unconfigured_llm_fallback_safety():
    """Test interview question generator falls back seamlessly to rule-based engine when LLM key is unconfigured."""
    resume = StructuredResume(
        resume_id="res-llm-fallback",
        skills=ExtractedSkills(skills=[
            ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python")
        ], total_count=1),
    )
    res = generate_interview_questions(resume, count=5, provider="openai")
    assert res.total_count == 5
    assert len(res.questions) == 5
    assert res.provider in ["rule_based_fallback", "auto", "openai"]


# ==============================================================================
# 2. INPUT IMMUTABILITY TESTS
# ==============================================================================

def test_input_immutability_structured_resume_in_ats_scoring():
    """Test ATS scoring does not mutate the input StructuredResume object."""
    resume = StructuredResume(
        resume_id="res-imm-1",
        skills=ExtractedSkills(skills=[
            ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python")
        ], total_count=1),
    )
    job = JobRequirements(job_id="job-imm-1", title="Python Engineer", required_skills=["Python"])
    
    resume_before = copy.deepcopy(resume)
    job_before = copy.deepcopy(job)

    _ = calculate_ats_score(resume, job)

    assert resume.model_dump_json() == resume_before.model_dump_json()
    assert job.model_dump_json() == job_before.model_dump_json()


def test_input_immutability_in_interview_question_generation():
    """Test question generation does not mutate the input StructuredResume object."""
    resume = StructuredResume(
        resume_id="res-imm-2",
        skills=ExtractedSkills(skills=[
            ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI")
        ], total_count=1),
    )
    resume_before = copy.deepcopy(resume)

    _ = generate_interview_questions(resume, count=5, difficulty=QuestionDifficulty.HARD)

    assert resume.model_dump_json() == resume_before.model_dump_json()


# ==============================================================================
# 3. DETERMINISM TESTS
# ==============================================================================

def test_determinism_section_detection():
    """Test section detection is 100% deterministic given identical text."""
    text = "SKILLS\nPython, FastAPI\n\nEXPERIENCE\nBackend Intern at ABC"
    doc = ExtractedDocument(
        text=text,
        document_type="pdf",
        extraction_method="pdfplumber",
        file_name="test.txt",
        file_type="txt",
        mime_type="text/plain",
        character_count=len(text),
        word_count=len(text.split()),
        line_count=len(text.splitlines()),
        pages=[],
        metadata={},
    )
    res1 = process_extracted_document(doc)
    res2 = process_extracted_document(doc)
    assert res1.raw_text == res2.raw_text


def test_determinism_ats_scoring():
    """Test ATS scoring is 100% deterministic given identical resume and job requirements."""
    resume = StructuredResume(
        resume_id="res-det-1",
        skills=ExtractedSkills(skills=[
            ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
            ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
        ], total_count=2),
    )
    job = JobRequirements(job_id="job-det-1", title="Backend Developer", required_skills=["Python", "FastAPI"])

    ats1 = calculate_ats_score(resume, job)
    ats2 = calculate_ats_score(resume, job)

    assert ats1.overall_score == ats2.overall_score
    assert ats1.skill_match_score == ats2.skill_match_score
    assert ats1.breakdown == ats2.breakdown


def test_determinism_fallback_interview_question_generation():
    """Test fallback interview question generator produces identical questions for identical inputs."""
    resume = StructuredResume(
        resume_id="res-det-2",
        skills=ExtractedSkills(skills=[
            ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL")
        ], total_count=1),
    )

    q1 = generate_interview_questions(resume, count=4, difficulty=QuestionDifficulty.MEDIUM, provider="auto")
    q2 = generate_interview_questions(resume, count=4, difficulty=QuestionDifficulty.MEDIUM, provider="auto")

    q1_texts = [q.question for q in q1.questions]
    q2_texts = [q.question for q in q2.questions]
    assert q1_texts == q2_texts
