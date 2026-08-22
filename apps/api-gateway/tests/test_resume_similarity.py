"""Unit and integration tests for Phase 4 Day 31 — Similarity Matching."""

import pytest
import numpy as np
from uuid import uuid4

from app.services.resume_processing.models import (
    StructuredResume,
    ExtractedSkill,
    ExtractedSkills,

    ExtractedEducation,
    EducationRecord,
    ExtractedExperience,
    ExperienceRecord,
    ExtractedProjects,
    ProjectRecord,
    ResumeClassification,
    JobRequirements,
    SimilarityMatch,
)
from app.services.resume_processing.embedding_service import (
    get_embedding_model,
    build_resume_embedding_text,
    build_job_embedding_text,
    generate_embedding,
    calculate_cosine_similarity,
    normalize_similarity_score,
    get_similarity_tier,
)
from app.services.resume_processing.similarity_matcher import calculate_resume_job_similarity
from app.services.resume_processing.ats_scorer import score_resume_against_job


@pytest.fixture
def sample_python_developer_resume():
    return StructuredResume(
        resume_id="res-py-101",
        full_name="Alice Smith",
        email="alice@example.com",
        phone="+1-555-0199",
        summary="Senior Python Backend Developer with 5 years of experience building scalable APIs, FastAPI microservices, PostgreSQL databases, and Docker containers.",
        skills=ExtractedSkills(
            skills=[
                ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
                ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
                ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL"),
                ExtractedSkill(name="Docker", normalized_name="docker", category="DEVOPS", matched_text="Docker"),
            ],
            categories={"PROGRAMMING_LANGUAGE": ["Python"], "FRAMEWORK": ["FastAPI"], "DATABASE": ["PostgreSQL"]},
        ),

        education=ExtractedEducation(
            education_records=[
                EducationRecord(
                    degree="Bachelor of Science in Computer Science",
                    normalized_degree="Bachelor of Science",
                    institution="Stanford University",
                    field_of_study="Computer Science",
                    graduation_year=2019,
                )
            ]
        ),
        experience=ExtractedExperience(
            experiences=[
                ExperienceRecord(
                    company="Tech Corp",
                    job_title="Senior Python Backend Engineer",
                    start_date="2020",
                    end_date="Present",
                    duration_months=48,
                    seniority="Senior",
                    responsibilities=[
                        "Designed and developed high-performance RESTful microservices using FastAPI and PostgreSQL.",
                        "Optimized database queries and reduced API response latency by 40%.",
                        "Containerized applications using Docker and orchestrated CI/CD pipelines."
                    ],
                )
            ],
            total_experience_months=48,
        ),
        projects=ExtractedProjects(
            projects=[
                ProjectRecord(
                    name="TalentAI API Gateway",
                    technologies=["Python", "FastAPI", "PostgreSQL", "Docker"],
                    description="Built an enterprise API gateway supporting async resume parsing and semantic search.",
                )
            ]
        ),
        classification=ResumeClassification(
            domain="Software Engineering",
            role="Backend Developer",
            experience_level="Senior",
        ),

    )


@pytest.fixture
def python_backend_job():
    return JobRequirements(
        job_id="job-py-202",
        title="Senior Python Backend Developer",
        description="We are seeking a Senior Python Backend Engineer to build robust REST APIs, design database schemas with PostgreSQL, and work with FastAPI, Docker, and Redis in a microservice environment.",
        required_keywords=["Python", "FastAPI", "PostgreSQL", "REST API"],
        preferred_keywords=["Docker", "Redis", "Microservices"],
        required_skills=["Python", "FastAPI", "PostgreSQL"],
        preferred_skills=["Docker", "Redis", "Git"],
        required_education=["Bachelor of Science"],
        required_experience_months=36,
        required_roles=["Backend Developer", "Software Engineer"],
        required_domains=["Software Engineering"],
        required_experience_level="Senior",
    )


@pytest.fixture
def graphic_designer_job():
    return JobRequirements(
        job_id="job-design-303",
        title="Creative Graphic Designer & Illustrator",
        description="Looking for an experienced Graphic Designer proficient in Adobe Photoshop, Illustrator, InDesign, Figma, logo design, typography, and visual branding.",
        required_keywords=["Adobe Photoshop", "Illustrator", "Figma", "Branding"],
        preferred_keywords=["Typography", "InDesign", "Vector Art"],
        required_skills=["Photoshop", "Illustrator", "Figma"],
        preferred_skills=["Typography", "Branding"],
        required_education=["Bachelor of Fine Arts"],
        required_experience_months=24,
        required_roles=["Graphic Designer"],
        required_domains=["Design & Creative"],
        required_experience_level="Mid",
    )


# ------------------------------------------------------------------------------
# Unit Tests: Embedding Service & Model Loader
# ------------------------------------------------------------------------------

def test_embedding_model_singleton():
    """Verify get_embedding_model lazy loads and returns same process-wide instance."""
    m1 = get_embedding_model()
    m2 = get_embedding_model()
    assert m1 is m2


def test_build_resume_embedding_text_clean(sample_python_developer_resume):
    """Verify resume embedding text contains structured data and excludes PII."""
    text = build_resume_embedding_text(sample_python_developer_resume)
    assert "Alice Smith" not in text
    assert "alice@example.com" not in text
    assert "+1-555-0199" not in text
    assert "FastAPI" in text
    assert "Backend Developer" in text
    assert "Stanford University" in text
    assert "Tech Corp" in text


def test_build_job_embedding_text_clean(python_backend_job):
    """Verify job embedding text formats title, description, skills, and roles."""
    text = build_job_embedding_text(python_backend_job)
    assert "Senior Python Backend Developer" in text
    assert "FastAPI" in text
    assert "PostgreSQL" in text


def test_generate_embedding_vector_properties():
    """Verify generated embedding vector is 1D float32 numpy array of dimension 384."""
    vec = generate_embedding("Python Backend Developer FastAPI PostgreSQL")
    assert isinstance(vec, np.ndarray)
    assert vec.dtype == np.float32
    assert vec.ndim == 1
    assert vec.shape[0] == 384
    assert not np.isnan(vec).any()


def test_calculate_cosine_similarity_identity():
    """Verify cosine similarity of identical vectors is 1.0."""
    v = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    sim = calculate_cosine_similarity(v, v)
    assert pytest.approx(sim, 0.0001) == 1.0


def test_calculate_cosine_similarity_orthogonal():
    """Verify cosine similarity of orthogonal vectors is 0.0."""
    v1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    v2 = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    sim = calculate_cosine_similarity(v1, v2)
    assert pytest.approx(sim, 0.0001) == 0.0


def test_calculate_cosine_similarity_opposite():
    """Verify cosine similarity of opposite vectors is -1.0."""
    v1 = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    v2 = np.array([-1.0, -2.0, -3.0], dtype=np.float32)
    sim = calculate_cosine_similarity(v1, v2)
    assert pytest.approx(sim, 0.0001) == -1.0


def test_normalize_similarity_score_bounds():
    """Verify score mapping: -1.0 -> 0.0, 0.0 -> 50.0, 1.0 -> 100.0."""
    assert normalize_similarity_score(-1.0) == 0.0
    assert normalize_similarity_score(0.0) == 50.0
    assert normalize_similarity_score(1.0) == 100.0
    assert 0.0 <= normalize_similarity_score(0.75) <= 100.0


def test_get_similarity_tier_levels():
    """Verify score tier categorization."""
    assert get_similarity_tier(85.0) == "Strong Match"
    assert get_similarity_tier(70.0) == "Good Match"
    assert get_similarity_tier(55.0) == "Moderate Match"
    assert get_similarity_tier(40.0) == "Low Match"


# ------------------------------------------------------------------------------
# Scorer & Relative Matching Assertions
# ------------------------------------------------------------------------------

def test_similar_resume_scores_higher_than_unrelated(
    sample_python_developer_resume, python_backend_job, graphic_designer_job
):
    """Relative assertion: Python Developer resume scores significantly higher against Python Job than Graphic Designer Job."""
    match_relevant = calculate_resume_job_similarity(sample_python_developer_resume, python_backend_job)
    match_unrelated = calculate_resume_job_similarity(sample_python_developer_resume, graphic_designer_job)

    assert match_relevant.similarity_score > match_unrelated.similarity_score
    assert match_relevant.similarity_score >= 70.0
    assert match_unrelated.similarity_score <= match_relevant.similarity_score - 5.0


    assert match_relevant.similarity_tier in ["Strong Match", "Good Match"]
    assert match_unrelated.similarity_tier in ["Moderate Match", "Low Match"]



def test_similarity_match_model_fields(sample_python_developer_resume, python_backend_job):
    """Verify SimilarityMatch model output schema compliance."""
    result = calculate_resume_job_similarity(sample_python_developer_resume, python_backend_job)
    assert isinstance(result, SimilarityMatch)
    assert result.resume_id == "res-py-101"
    assert result.job_id == "job-py-202"
    assert result.embedding_dimension == 384
    assert result.model_name == "sentence-transformers/all-MiniLM-L6-v2"
    assert result.resume_text_length > 0
    assert result.job_text_length > 0


def test_empty_resume_handling(python_backend_job):
    """Verify graceful handling for empty resume."""
    empty_resume = StructuredResume()
    result = calculate_resume_job_similarity(empty_resume, python_backend_job)
    assert isinstance(result, SimilarityMatch)
    assert 0.0 <= result.similarity_score <= 100.0


def test_empty_job_handling(sample_python_developer_resume):
    """Verify graceful handling for empty job."""
    empty_job = JobRequirements()
    result = calculate_resume_job_similarity(sample_python_developer_resume, empty_job)
    assert isinstance(result, SimilarityMatch)
    assert 0.0 <= result.similarity_score <= 100.0


def test_vector_dimension_mismatch_raises_error():
    """Verify calculate_cosine_similarity raises ValueError on dimension mismatch."""
    v1 = np.array([1.0, 2.0], dtype=np.float32)
    v2 = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    with pytest.raises(ValueError, match="Vector dimension mismatch"):
        calculate_cosine_similarity(v1, v2)


def test_coexistence_with_day30_ats(sample_python_developer_resume, python_backend_job):
    """Verify Day 30 ATS score and Day 31 Similarity Score operate independently."""
    ats_score = score_resume_against_job(sample_python_developer_resume, python_backend_job)
    sim_score = calculate_resume_job_similarity(sample_python_developer_resume, python_backend_job)

    assert ats_score.score > 0.0
    assert ats_score.scoring_method == "weighted_hybrid_rule_based"

    assert sim_score.similarity_score > 0.0
    assert sim_score.model_name == "sentence-transformers/all-MiniLM-L6-v2"
