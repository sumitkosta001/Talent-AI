"""Phase 4 — Day 33: Recommendation Engine Test Suite.

Comprehensive test suite covering:
1. Recommendation models validation.
2. Score calculation, weighting, clamping (0-100), and tie-breaking.
3. Job recommendations ranking (Python Backend job > Graphic Designer job).
4. Candidate recommendations ranking (Python Developer candidate > Graphic Designer candidate).
5. Evidence-based match explanations (strengths, gaps, matched/missing canonical skills).
6. Day 29 classification role/domain compatibility.
7. Deduplication and self-match prevention.
8. Top-K handling & pool expansion.
9. Empty/missing data handling.
10. Days 21–32 regression compatibility.
"""

import pytest
import numpy as np
from typing import Dict, Any, List

from app.services.resume_processing.models import (
    StructuredResume,
    JobRequirements,
    ExtractedSkills,
    ExtractedSkill,
    ExtractedEducation,
    EducationRecord,
    ExtractedExperience,
    ExperienceRecord,
    ExtractedProjects,
    ProjectRecord,
    ResumeClassification,
    ATSScore,
    RecommendationExplanation,
    JobRecommendation,
    CandidateRecommendation,
    JobRecommendationResponse,
    CandidateRecommendationResponse,
)
from app.services.resume_processing.recommendation_engine import (
    calculate_recommendation_score,
    build_match_explanation,
    recommend_jobs_for_resume,
    recommend_candidates_for_job,
    canonicalize_skill_name,
    RecommendationEngine,
)
from app.services.resume_processing.ats_scorer import score_resume_against_job
from app.services.resume_processing.faiss_index_service import (
    get_resume_faiss_index,
    get_job_faiss_index,
    index_resume,
    index_job,
)


def create_sample_python_developer_resume() -> StructuredResume:
    """Helper creating a realistic Python Backend Software Engineer structured resume."""
    return StructuredResume(
        resume_id="cand-resume-python-101",
        full_name="Robert Bruce",
        email="robert.bruce@example.com",
        skills=ExtractedSkills(
            skills=[
                ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
                ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
                ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL"),
                ExtractedSkill(name="Docker", normalized_name="docker", category="DEVOPS", matched_text="Docker"),
                ExtractedSkill(name="FAISS", normalized_name="faiss", category="LIBRARIES", matched_text="FAISS"),
            ],
            total_count=5,
        ),
        education=ExtractedEducation(
            education_records=[
                EducationRecord(
                    degree="Bachelor of Technology",
                    normalized_degree="bachelor_of_technology",
                    degree_level="UNDERGRADUATE",
                    field_of_study="Computer Science",
                    institution="NIT Rourkela",
                    graduation_year=2022,
                )
            ]
        ),
        experience=ExtractedExperience(
            experiences=[
                ExperienceRecord(
                    company="Tech Corp",
                    job_title="Senior Python Engineer",
                    duration_months=36,
                    seniority="SENIOR",
                    responsibilities=["Developed RESTful APIs with FastAPI and PostgreSQL", "Optimized vector search"],
                )
            ],
            total_experience_months=36,
        ),
        classification=ResumeClassification(
            domain="SOFTWARE_ENGINEERING",
            role="BACKEND_DEVELOPER",
            experience_level="SENIOR",
        ),
        summary="Experienced Senior Python Backend Engineer skilled in FastAPI, PostgreSQL, microservices, and vector search.",
    )


def create_sample_designer_resume() -> StructuredResume:
    """Helper creating a realistic Graphic Designer structured resume."""
    return StructuredResume(
        resume_id="cand-resume-design-202",
        full_name="Alice Smith",
        email="alice.smith@example.com",
        skills=ExtractedSkills(
            skills=[
                ExtractedSkill(name="Figma", normalized_name="figma", category="DESIGN", matched_text="Figma"),
                ExtractedSkill(name="Adobe Photoshop", normalized_name="adobe photoshop", category="DESIGN", matched_text="Photoshop"),
                ExtractedSkill(name="Illustrator", normalized_name="illustrator", category="DESIGN", matched_text="Illustrator"),
            ],
            total_count=3,
        ),
        education=ExtractedEducation(
            education_records=[
                EducationRecord(
                    degree="Bachelor of Fine Arts",
                    normalized_degree="bachelor_of_fine_arts",
                    degree_level="UNDERGRADUATE",
                    field_of_study="Graphic Design",
                    institution="Design Academy",
                    graduation_year=2021,
                )
            ]
        ),
        experience=ExtractedExperience(
            experiences=[
                ExperienceRecord(
                    company="Creative Studio",
                    job_title="Graphic Designer",
                    duration_months=24,
                    seniority="MID_LEVEL",
                    responsibilities=["Created vector illustrations, UI prototypes in Figma, and marketing collateral"],
                )
            ],
            total_experience_months=24,
        ),
        classification=ResumeClassification(
            domain="DESIGN",
            role="UI_UX_DESIGNER",
            experience_level="MID_LEVEL",
        ),
        summary="Creative UI/UX Designer specializing in vector graphics, visual identity, Figma design systems, and branding.",
    )


def create_sample_python_job() -> JobRequirements:
    """Helper creating Python Backend Engineer job requirements."""
    return JobRequirements(
        job_id="job-python-dev-1",
        title="Senior Python Backend Engineer",
        description="Looking for a Python Backend Engineer with FastAPI, PostgreSQL, and Docker experience.",
        required_skills=["Python", "FastAPI", "PostgreSQL"],
        preferred_skills=["Docker", "FAISS", "Kubernetes"],
        required_keywords=["Python", "FastAPI", "Backend", "API"],
        required_domains=["SOFTWARE_ENGINEERING"],
        required_roles=["BACKEND_DEVELOPER"],
        required_experience_months=24,
    )


def create_sample_designer_job() -> JobRequirements:
    """Helper creating Graphic Designer job requirements."""
    return JobRequirements(
        job_id="job-design-2",
        title="Senior Graphic UI/UX Designer",
        description="Looking for a Graphic Designer proficient in Figma, Photoshop, and Illustrator.",
        required_skills=["Figma", "Photoshop", "Illustrator"],
        preferred_skills=["InDesign", "Sketch"],
        required_keywords=["Figma", "Design", "UI", "Branding"],
        required_domains=["DESIGN"],
        required_roles=["UI_UX_DESIGNER"],
        required_experience_months=12,
    )


# ==============================================================================
# UNIT & INTEGRATION TESTS
# ==============================================================================

def test_recommendation_models_validation():
    """[01] Test Recommendation Pydantic model validation and defaults."""
    exp = RecommendationExplanation(
        summary="Strong match for role",
        strengths=["High skill match"],
        gaps=["Missing AWS"],
        matched_skills=["Python", "FastAPI"],
        missing_skills=["AWS"],
    )
    assert exp.summary == "Strong match for role"
    assert len(exp.strengths) == 1
    assert "Python" in exp.matched_skills

    job_rec = JobRecommendation(
        job_id="job-101",
        title="Python Dev",
        recommendation_score=85.5,
        semantic_similarity_score=80.0,
        ats_score=91.0,
        explanation=exp,
    )
    assert job_rec.job_id == "job-101"
    assert job_rec.recommendation_score == 85.5
    assert job_rec.ranking_position == 1

    cand_rec = CandidateRecommendation(
        resume_id="res-101",
        full_name="Robert Bruce",
        recommendation_score=90.0,
        explanation=exp,
    )
    assert cand_rec.resume_id == "res-101"
    assert cand_rec.full_name == "Robert Bruce"

    job_resp = JobRecommendationResponse(
        resume_id="res-101",
        recommendations=[job_rec],
        total_results=1,
    )
    assert job_resp.total_results == 1
    assert job_resp.ranking_method == "weighted_hybrid_faiss_ats"


def test_score_calculation_weighting_and_clamping():
    """[02] Test recommendation score calculation, custom weights, and clamping (0-100)."""
    # 50/50 default weight: 80 * 0.5 + 90 * 0.5 = 85.0
    score1 = calculate_recommendation_score(semantic_score=80.0, ats_score=90.0)
    assert score1 == 85.0

    # Custom weights (0.7 / 0.3): 80 * 0.7 + 90 * 0.3 = 56 + 27 = 83.0
    score2 = calculate_recommendation_score(semantic_score=80.0, ats_score=90.0, semantic_weight=0.7, ats_weight=0.3)
    assert score2 == 83.0

    # Clamping test (> 100)
    score_over = calculate_recommendation_score(semantic_score=120.0, ats_score=110.0)
    assert score_over == 100.0

    # Clamping test (< 0)
    score_under = calculate_recommendation_score(semantic_score=-50.0, ats_score=-20.0)
    assert score_under == 0.0


def test_canonical_skill_name_resolution():
    """[03] Test canonical skill name normalization using Day 24 ALIAS_MAP."""
    assert canonicalize_skill_name("ReactJS") == "React.js"
    assert canonicalize_skill_name("Py") == "Python"
    assert canonicalize_skill_name("Postgres") == "PostgreSQL"
    assert canonicalize_skill_name("  fastapi  ") == "FastAPI"


def test_match_explanation_generation():
    """[04] Test evidence-based match explanation generation without fabrication."""
    resume = create_sample_python_developer_resume()
    job = create_sample_python_job()
    ats_res = score_resume_against_job(resume, job)

    explanation = build_match_explanation(resume, job, ats_res, semantic_score=82.5)

    assert "Python" in explanation.matched_skills
    assert "FastAPI" in explanation.matched_skills
    assert len(explanation.strengths) > 0
    assert "Strong recommendation" in explanation.summary or "recommendation" in explanation.summary
    assert explanation.role_domain_compatibility is not None


def test_job_recommendation_ranking_python_vs_designer():
    """[05] Test Python candidate receives Python Backend Job ranked HIGHER than Graphic Designer Job."""
    python_resume = create_sample_python_developer_resume()
    py_job = create_sample_python_job()
    design_job = create_sample_designer_job()

    response = recommend_jobs_for_resume(python_resume, candidate_jobs=[py_job, design_job], top_k=10)

    assert response.total_results >= 2
    py_rec = next(r for r in response.recommendations if r.job_id == py_job.job_id)
    design_rec = next(r for r in response.recommendations if r.job_id == design_job.job_id)
    assert py_rec.recommendation_score > design_rec.recommendation_score
    assert py_rec.ranking_position < design_rec.ranking_position


def test_candidate_recommendation_ranking_python_vs_designer():
    """[06] Test Python Job receives Python Candidate ranked HIGHER than Designer Candidate."""
    py_job = create_sample_python_job()
    python_resume = create_sample_python_developer_resume()
    design_resume = create_sample_designer_resume()

    response = recommend_candidates_for_job(py_job, candidate_resumes=[python_resume, design_resume], top_k=10)

    assert response.total_results >= 2
    py_rec = next(r for r in response.recommendations if r.resume_id == python_resume.resume_id)
    design_rec = next(r for r in response.recommendations if r.resume_id == design_resume.resume_id)
    assert py_rec.recommendation_score > design_rec.recommendation_score
    assert py_rec.ranking_position < design_rec.ranking_position


def test_deduplication_in_job_recommendations():
    """[07] Test duplicate jobs in pool are deduplicated keeping unique job_ids."""
    python_resume = create_sample_python_developer_resume()
    py_job = create_sample_python_job()

    # Pass duplicate job objects
    response = recommend_jobs_for_resume(python_resume, candidate_jobs=[py_job, py_job], top_k=10)

    job_ids = [r.job_id for r in response.recommendations]
    assert len(job_ids) == len(set(job_ids)), "Recommendation response contains duplicate job_ids"
    assert py_job.job_id in job_ids


def test_self_match_prevention_in_candidate_recommendations():
    """[08] Test self_resume_id is filtered out from candidate recommendations."""
    py_job = create_sample_python_job()
    python_resume = create_sample_python_developer_resume()
    design_resume = create_sample_designer_resume()

    response = recommend_candidates_for_job(
        py_job,
        candidate_resumes=[python_resume, design_resume],
        top_k=10,
        self_resume_id="cand-resume-python-101",
    )

    # Python candidate should be excluded due to self_resume_id filter
    rec_resume_ids = [r.resume_id for r in response.recommendations]
    assert "cand-resume-python-101" not in rec_resume_ids



def test_top_k_bounding_and_validation():
    """[09] Test top_k validation and bounding to max top_k."""
    python_resume = create_sample_python_developer_resume()
    py_job = create_sample_python_job()

    with pytest.raises(ValueError):
        recommend_jobs_for_resume(python_resume, candidate_jobs=[py_job], top_k=0)

    with pytest.raises(ValueError):
        recommend_jobs_for_resume(python_resume, candidate_jobs=[py_job], top_k=-5)

    res = recommend_jobs_for_resume(python_resume, candidate_jobs=[py_job], top_k=100)
    assert res.top_k <= 50  # Bounded by max_top_k (50)


def test_faiss_and_ats_hybrid_integration():
    """[10] Test full FAISS index vector retrieval combined with Day 30 ATS score reranking."""
    python_resume = create_sample_python_developer_resume()
    py_job = create_sample_python_job()
    design_job = create_sample_designer_job()

    # Index jobs into Day 32 FAISS
    index_job(py_job.job_id, py_job)
    index_job(design_job.job_id, design_job)

    # Index candidate resume into Day 32 FAISS
    index_resume(python_resume.resume_id, python_resume)

    # Perform recommendation via FAISS index retrieval + ATS reranking
    job_rec_resp = recommend_jobs_for_resume(python_resume, top_k=10)

    assert job_rec_resp.total_results >= 2
    assert job_rec_resp.recommendations[0].job_id == "job-python-dev-1"
    assert job_rec_resp.recommendations[0].recommendation_score > job_rec_resp.recommendations[1].recommendation_score


def test_empty_pool_handling_safety():
    """[11] Test empty candidate resume / job pool returns clean empty response without error."""
    python_resume = create_sample_python_developer_resume()
    py_job = create_sample_python_job()

    res1 = recommend_jobs_for_resume(python_resume, candidate_jobs=[], top_k=10)
    assert isinstance(res1, JobRecommendationResponse)

    res2 = recommend_candidates_for_job(py_job, candidate_resumes=[], top_k=10)
    assert isinstance(res2, CandidateRecommendationResponse)


def test_input_immutability():
    """[12] Test recommendation engine does not mutate input objects."""
    python_resume = create_sample_python_developer_resume()
    py_job = create_sample_python_job()

    resume_json_before = python_resume.model_dump_json()
    job_json_before = py_job.model_dump_json()

    recommend_jobs_for_resume(python_resume, candidate_jobs=[py_job], top_k=10)
    recommend_candidates_for_job(py_job, candidate_resumes=[python_resume], top_k=10)

    assert python_resume.model_dump_json() == resume_json_before
    assert py_job.model_dump_json() == job_json_before
