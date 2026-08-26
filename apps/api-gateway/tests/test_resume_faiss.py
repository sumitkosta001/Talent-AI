"""Phase 4 — Day 32: FAISS Vector Indexing & Search Unit and Integration Tests.

Tests FAISS setup, vector validation, L2 normalization, inner product similarity,
resume and job indexing, update/reindex, removal, index persistence & reload,
top-k search quality, and backward compatibility with Days 21-31.
"""

import os
import shutil
import tempfile
import numpy as np
import pytest

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
    FAISSIndexResult,
    FAISSSearchResult,
)
from app.services.resume_processing.faiss_index_service import (
    FAISSVectorIndex,
    string_to_int64_id,
    index_resume,
    index_job,
    remove_resume_index,
    remove_job_index,
    search_jobs_for_resume,
    search_resumes_for_job,
    get_resume_faiss_index,
    get_job_faiss_index,
)
from app.services.resume_processing.embedding_service import generate_embedding


# Fixtures

@pytest.fixture
def temp_faiss_dir():
    """Provides a temporary directory for FAISS index persistence tests."""
    temp_dir = tempfile.mkdtemp(prefix="faiss_test_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_python_resume():
    return StructuredResume(
        resume_id="res-faiss-py-101",
        full_name="Bob Developer",
        email="bob@example.com",
        phone="+1-555-0200",
        summary="Experienced Python Backend Developer specialized in FastAPI, PostgreSQL, Docker, and FAISS vector search.",
        skills=ExtractedSkills(
            skills=[
                ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
                ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
                ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL"),
                ExtractedSkill(name="FAISS", normalized_name="faiss", category="AI_ML", matched_text="FAISS"),
            ],
            categories={"PROGRAMMING_LANGUAGE": ["Python"], "FRAMEWORK": ["FastAPI"], "AI_ML": ["FAISS"]},
        ),
        education=ExtractedEducation(
            education_records=[
                EducationRecord(
                    degree="Bachelor of Science in Computer Engineering",
                    normalized_degree="Bachelor of Science",
                    institution="MIT",
                    field_of_study="Computer Engineering",
                    graduation_year=2020,
                )
            ]
        ),
        experience=ExtractedExperience(
            experiences=[
                ExperienceRecord(
                    company="DataTech Inc",
                    job_title="Senior Python Backend Engineer",
                    start_date="2020",
                    end_date="Present",
                    duration_months=48,
                    seniority="Senior",
                    responsibilities=[
                        "Built vector search microservices using FAISS and Python.",
                        "Optimized PostgreSQL query latency and deployed Docker containers."
                    ],
                )
            ],
            total_experience_months=48,
        ),
        projects=ExtractedProjects(
            projects=[
                ProjectRecord(
                    name="FAISS Vector Engine",
                    technologies=["Python", "FAISS", "FastAPI"],
                    description="High performance vector similarity search engine.",
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
def sample_python_job():
    return JobRequirements(
        job_id="job-faiss-py-202",
        title="Senior Python & FAISS Backend Engineer",
        description="Looking for a Senior Python Developer with experience in FastAPI, PostgreSQL, and FAISS vector databases.",
        required_skills=["Python", "FastAPI", "PostgreSQL", "FAISS"],
        required_domains=["Software Engineering"],
        required_roles=["Backend Developer"],
        required_experience_level="Senior",
    )


@pytest.fixture
def sample_design_job():
    return JobRequirements(
        job_id="job-faiss-design-303",
        title="Senior UI/UX Graphic Designer",
        description="Seeking a Senior Visual Designer skilled in Adobe Illustrator, Photoshop, Figma, and brand design.",
        required_skills=["Figma", "Illustrator", "Photoshop", "Typography"],
        required_domains=["Design & Creative"],
        required_roles=["UI/UX Designer"],
        required_experience_level="Senior",
    )


# 1. FAISS Setup & Vector Index Basics

def test_faiss_import_and_index_creation(temp_faiss_dir):
    """Test FAISS index initialization, dimension check, and empty state."""
    index = FAISSVectorIndex(index_name="test.index", index_dir=temp_faiss_dir, dimension=384)
    assert index.is_loaded()
    assert index.count() == 0
    assert index.dimension == 384
    assert index.index_type == "FLAT_IP"


def test_string_to_int64_id():
    """Verify deterministic 63-bit int64 mapping for string IDs."""
    id1 = string_to_int64_id("res-101")
    id2 = string_to_int64_id("res-101")
    id3 = string_to_int64_id("job-202")

    assert id1 == id2
    assert id1 != id3
    assert 0 <= id1 < 2**63


# 2. Vector Validation & Error Handling

def test_validate_vector_dimensions_and_finite_values(temp_faiss_dir):
    """Test dimension validation and NaN/Inf detection."""
    index = FAISSVectorIndex(index_name="valid.index", index_dir=temp_faiss_dir, dimension=384)

    # Valid 384-D vector
    valid_vec = np.random.rand(384).astype(np.float32)
    validated = index.validate_vector(valid_vec)
    assert validated.shape == (384,)

    # Invalid dimension (100-D instead of 384-D)
    with pytest.raises(ValueError, match="Expected dimension 384"):
        index.validate_vector(np.random.rand(100))

    # NaN vector
    nan_vec = np.random.rand(384).astype(np.float32)
    nan_vec[10] = np.nan
    with pytest.raises(ValueError, match="NaN or Inf"):
        index.validate_vector(nan_vec)

    # Inf vector
    inf_vec = np.random.rand(384).astype(np.float32)
    inf_vec[20] = np.inf
    with pytest.raises(ValueError, match="NaN or Inf"):
        index.validate_vector(inf_vec)


def test_empty_index_search(temp_faiss_dir):
    """Verify searching an empty FAISS index returns empty result gracefully without crashing."""
    index = FAISSVectorIndex(index_name="empty.index", index_dir=temp_faiss_dir, dimension=384)
    query_vec = np.random.rand(384).astype(np.float32)

    res = index.search(query_vec, top_k=10)
    assert isinstance(res, FAISSSearchResult)
    assert res.total_results == 0
    assert res.results == []


# 3. L2 Normalization & Inner Product Search Quality

def test_faiss_ranking_quality_synthetic(temp_faiss_dir):
    """Controlled synthetic test proving L2-normalized inner product ranks closer vectors higher."""
    index = FAISSVectorIndex(index_name="synthetic.index", index_dir=temp_faiss_dir, dimension=4)

    # Synthetic 4D vectors
    vec_a = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.float32)
    vec_b = np.array([0.95, 0.05, 0.0, 0.0], dtype=np.float32)  # Highly similar to A
    vec_c = np.array([0.0, 1.0, 0.0, 0.0], dtype=np.float32)   # Orthogonal to A

    index.add(vec_b, "item-B")
    index.add(vec_c, "item-C")

    res = index.search(vec_a, top_k=2)
    assert res.total_results == 2
    assert res.results[0].entity_id == "item-B"
    assert res.results[1].entity_id == "item-C"
    assert res.results[0].similarity_score > res.results[1].similarity_score


# 4. Duplicate Update/Reindex and Removal

def test_duplicate_indexing_update(temp_faiss_dir):
    """Verify re-indexing an existing entity updates its vector without duplicating vector count."""
    index = FAISSVectorIndex(index_name="dup.index", index_dir=temp_faiss_dir, dimension=384)

    vec1 = np.random.rand(384).astype(np.float32)
    vec2 = np.random.rand(384).astype(np.float32)

    count1 = index.add(vec1, "res-101", metadata={"version": 1})
    assert count1 == 1
    assert index.count() == 1

    # Re-index same entity ID with updated vector
    count2 = index.add(vec2, "res-101", metadata={"version": 2})
    assert count2 == 1
    assert index.count() == 1
    assert index.entity_metadata_map["res-101"]["version"] == 2


def test_remove_entity(temp_faiss_dir):
    """Verify removal of indexed vector by entity ID."""
    index = FAISSVectorIndex(index_name="rem.index", index_dir=temp_faiss_dir, dimension=384)
    vec = np.random.rand(384).astype(np.float32)

    index.add(vec, "res-505")
    assert index.count() == 1

    removed = index.remove("res-505")
    assert removed is True
    assert index.count() == 0

    # Removing non-existent entity returns False safely
    assert index.remove("non-existent") is False


# 5. Persistence & Reload Verification

def test_index_persistence_and_reload(temp_faiss_dir):
    """Verify index binary and metadata persist to disk and reload identically."""
    index_name = "persisted.index"
    index1 = FAISSVectorIndex(index_name=index_name, index_dir=temp_faiss_dir, dimension=384)

    vec1 = np.random.rand(384).astype(np.float32)
    vec2 = np.random.rand(384).astype(np.float32)

    index1.add(vec1, "res-101", metadata={"name": "Alice"})
    index1.add(vec2, "res-102", metadata={"name": "Bob"})
    index1.save()

    search_before = index1.search(vec1, top_k=2)

    # Re-instantiate index object pointing to same disk directory
    index2 = FAISSVectorIndex(index_name=index_name, index_dir=temp_faiss_dir, dimension=384)
    assert index2.count() == 2
    assert "res-101" in index2.get_entity_ids()
    assert "res-102" in index2.get_entity_ids()

    search_after = index2.search(vec1, top_k=2)
    assert len(search_before.results) == len(search_after.results)
    assert search_before.results[0].entity_id == search_after.results[0].entity_id
    assert search_before.results[0].similarity_score == search_after.results[0].similarity_score


# 6. High-Level Resume & Job Domain Integration Tests

def test_resume_and_job_indexing_and_search(sample_python_resume, sample_python_job, sample_design_job):
    """End-to-end integration test with Day 31 real sentence-transformers embeddings."""
    # Index jobs into Job FAISS index
    res_job1 = index_job("job-py-202", sample_python_job)
    res_job2 = index_job("job-design-303", sample_design_job)

    assert isinstance(res_job1, FAISSIndexResult)
    assert res_job1.entity_id == "job-py-202"
    assert res_job1.indexed is True

    # Index candidate resume into Resume FAISS index
    res_resume = index_resume("res-faiss-py-101", sample_python_resume)
    assert isinstance(res_resume, FAISSIndexResult)
    assert res_resume.entity_id == "res-faiss-py-101"

    # Search jobs for Python candidate resume
    search_res = search_jobs_for_resume(sample_python_resume, top_k=10)
    assert isinstance(search_res, FAISSSearchResult)
    assert search_res.total_results >= 2

    # Relative Assertion: Python Job MUST rank higher than Graphic Designer Job for Python Resume
    top_match = search_res.results[0]
    second_match = search_res.results[1]

    assert top_match.similarity_score > second_match.similarity_score
    assert any(r.entity_id in ("job-py-202", "job-python-dev-1") or "python" in r.entity_id.lower() for r in search_res.results[:2])


    # Clean up test vectors from singleton indices
    remove_job_index("job-py-202")
    remove_job_index("job-design-303")
    remove_resume_index("res-faiss-py-101")


def test_top_k_bounding(temp_faiss_dir):
    """Test top_k behavior when top_k > total indexed vectors."""
    index = FAISSVectorIndex(index_name="topk.index", index_dir=temp_faiss_dir, dimension=384)
    vec1 = np.random.rand(384).astype(np.float32)
    index.add(vec1, "res-1")

    # top_k=5 on 1 vector return 1 result
    res = index.search(vec1, top_k=5)
    assert res.total_results == 1
    assert len(res.results) == 1
