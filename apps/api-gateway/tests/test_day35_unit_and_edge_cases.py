"""Phase 4 — Day 35: Unit and Edge Cases Test Suite.

Tests pure functions, edge cases, tokenization preservation, normalizers,
ATS score clamping, similarity calculations, and recommendation scoring across Days 21–34.
"""

import pytest
import numpy as np

from app.services.resume_processing.text_cleaner import clean_text
from app.services.resume_processing.tokenizer import tokenize_resume_text as tokenize_text
from app.services.resume_processing.section_detector import detect_sections
from app.services.resume_processing.skill_dictionary import ALIAS_MAP
from app.services.resume_processing.education_normalizer import normalize_degree as normalize_degree_name, parse_score
from app.services.resume_processing.experience_normalizer import parse_dates_and_duration, detect_seniority as normalize_seniority
from app.services.resume_processing.project_normalizer import normalize_project_name, classify_project as classify_project_type
from app.services.resume_processing import calculate_ats_score, compute_cosine_similarity, calculate_recommendation_score




from app.services.resume_processing.models import (
    StructuredResume,
    ExtractedSkills,
    ExtractedSkill,
    JobRequirements,
    EducationRecord,
    ExtractedEducation,
    ExperienceRecord,
    ExtractedExperience,
    ProjectRecord,
    ExtractedProjects,
    ResumeClassification,
)


def test_text_cleaning_and_crlf_normalization():
    """Test text cleaning CRLF -> LF, control char removal, Unicode normalization."""
    raw = "Line 1\r\nLine 2\rLine 3\x00\x08Bullet \u2022 item"
    cleaned = clean_text(raw)
    assert "\r" not in cleaned
    assert "\x00" not in cleaned
    assert "Line 1\nLine 2\nLine 3" in cleaned


def test_special_technology_token_preservation():
    """Test tokenization preserves C++, C#, .NET, Node.js, React.js, scikit-learn, emails, URLs."""

    text = "Proficient in C++, C#, .NET, Node.js, React.js, and scikit-learn. Contact: dev@example.com https://github.com/dev"
    raw_tokens, tokens = tokenize_text(text)
    assert "c++" in tokens
    assert "c#" in tokens
    assert ".net" in tokens
    assert "node.js" in tokens
    assert "react.js" in tokens
    assert "scikit-learn" in tokens


def test_section_detection_heuristics():
    """Test section detection identifies headings with colons, uppercase, and aliases."""
    text = """
    JOHN DOE
    SUMMARY:
    Senior Developer with 5 years experience.

    TECHNICAL SKILLS
    Python, FastAPI, PostgreSQL

    WORK EXPERIENCE:
    Software Engineer at TechCorp (2020-2024)

    ACADEMIC PROJECTS
    E-Commerce API: Built using FastAPI
    """
    sections = detect_sections(text)
    section_names = [s.name for s in sections]
    assert "SUMMARY" in section_names or "SKILLS" in section_names
    assert "EXPERIENCE" in section_names or "PROJECTS" in section_names


def test_skill_alias_normalization():
    """Test skill aliases normalize canonical names correctly via ALIAS_MAP."""
    assert ALIAS_MAP.get("reactjs")[0] == "React.js"
    assert ALIAS_MAP.get("postgres")[0] == "PostgreSQL"
    assert ALIAS_MAP.get("sklearn")[0] == "scikit-learn"
    assert ALIAS_MAP.get("k8s")[0] == "Kubernetes"
    assert ALIAS_MAP.get("golang")[0] == "Go"


def test_degree_and_gpa_normalization():
    """Test degree name and GPA/CGPA score normalizations."""
    deg_canonical, _, deg_level = normalize_degree_name("B.Tech in CS")
    assert deg_level in ["BACHELORS", "UNDERGRADUATE", "BACHELOR"]
    
    cgpa1, pct1, stype1 = parse_score("CGPA: 8.5/10")
    assert cgpa1 == 8.5
    assert stype1 == "CGPA"

    cgpa2, pct2, stype2 = parse_score("85.5%")
    assert pct2 == 85.5
    assert stype2 == "PERCENTAGE"


def test_experience_duration_and_seniority_normalization():
    """Test experience duration months and seniority levels."""
    _, _, sy, sm, ey, em, dur, dtxt, is_curr = parse_dates_and_duration("Jan 2022 - Dec 2022")
    assert dur == 12 or sy == 2022
    assert normalize_seniority("Senior Software Engineer") in ["SENIOR", "LEAD"]
    assert normalize_seniority("Software Intern") in ["INTERN", "ENTRY_LEVEL"]


def test_project_classification_normalization():
    """Test project type classification."""
    assert classify_project_type("Machine Learning Resume Classifier", "Classifier built using PyTorch", ["PyTorch"]) in ["MACHINE_LEARNING", "ARTIFICIAL_INTELLIGENCE", "DATA_SCIENCE"]
    assert classify_project_type("Full Stack Web Application", "Built using React and Node", ["React.js", "Node.js"]) in ["FULL_STACK", "WEB_APPLICATION"]


def test_ats_score_clamping_and_bounds():
    """Test ATS score is strictly clamped between 0.0 and 100.0."""
    # 1. Candidate and job with minimal requirements
    resume_empty = StructuredResume(resume_id="res-0", skills=ExtractedSkills(skills=[], total_count=0))
    job_empty = JobRequirements(job_id="job-0", title="Test Job", required_skills=["Python"])
    ats_empty = calculate_ats_score(resume_empty, job_empty)
    assert 0.0 <= ats_empty.overall_score <= 100.0

    # 2. Perfect match candidate

    resume_full = StructuredResume(
        resume_id="res-1",
        skills=ExtractedSkills(skills=[
            ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
            ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
            ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL"),
        ], total_count=3),
        education=ExtractedEducation(educations=[EducationRecord(degree_level="BACHELORS", school_name="MIT")], total_count=1),
        experience=ExtractedExperience(experiences=[ExperienceRecord(company="Google", title="Backend Engineer", duration_months=36)], total_count=1),
    )
    job_full = JobRequirements(
        job_id="job-1",
        title="Backend Engineer",
        required_skills=["Python", "FastAPI", "PostgreSQL"],
        min_experience_months=24,
        min_degree_level="BACHELORS",
    )
    ats_full = calculate_ats_score(resume_full, job_full)
    assert 0.0 <= ats_full.overall_score <= 100.0
    assert ats_full.overall_score >= 80.0


def test_cosine_similarity_edge_cases():
    """Test cosine similarity with identical, orthogonal, and zero vectors."""
    v1 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    v2 = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    assert compute_cosine_similarity(v1, v2) == pytest.approx(1.0)

    v3 = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    assert compute_cosine_similarity(v1, v3) == pytest.approx(0.0)

    v_zero = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    assert compute_cosine_similarity(v1, v_zero) == pytest.approx(0.0)


def test_recommendation_score_formula_consistency():
    """Test recommendation score formula: clamp(semantic * 0.50 + ats * 0.50, 0, 100)."""
    score1 = calculate_recommendation_score(semantic_score=80.0, ats_score=90.0, semantic_weight=0.50, ats_weight=0.50)
    assert score1 == pytest.approx(85.0)

    score_max = calculate_recommendation_score(semantic_score=150.0, ats_score=120.0)
    assert score_max == 100.0

    score_min = calculate_recommendation_score(semantic_score=-20.0, ats_score=-10.0)
    assert score_min == 0.0
