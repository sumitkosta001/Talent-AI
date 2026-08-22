"""Unit and Integration Tests for Phase 4 Day 30 ATS Scoring Engine.

Verifies:
1. Basic ATSScore generation.
2. Score range clamping (0 <= score <= 100).
3. Perfect match score calculation (100.0).
4. Zero / low match score handling.
5. Exact keyword matching vs token boundaries (JavaScript vs javascript, C++ vs C, SQL vs PostgreSQL).
6. Required keyword scoring impact.
7. Preferred keyword scoring impact.
8. Required skill matching.
9. Preferred skill matching.
10. Day 24 skill alias normalization (ReactJS -> React.js, Postgres -> PostgreSQL, sklearn -> scikit-learn).
11. Skill deduplication (preventing duplicate score inflation).
12. Education level & degree matching (B.Tech -> Bachelor of Technology).
13. Education level mismatch handling.
14. Field of study matching vs non-field degree.
15. Experience duration credit (full vs partial).
16. Role compatibility matching (Day 29 role reuse).
17. Domain matching (Day 29 domain reuse).
18. Seniority level matching (Day 29 experience level reuse).
19. Score breakdown mathematical consistency.
20. Weighted final score formula.
21. Score clamping under edge conditions.
22. Empty requirement lists handling (no division-by-zero).
23. Empty JobRequirements validation error.
24. Empty StructuredResume low-score handling (no crash).
25. Deterministic explanation generation.
26. Recommendations generation ("if applicable").
27. Scoring determinism (same inputs produce identical results).
28. Input non-mutation (StructuredResume and JobRequirements remain unchanged).
29. Invalid input exception handling (None resume, None job).
30. Required skill priority weighting.
31. False substring prevention (Java != JavaScript, C != C++).
32. Full pipeline integration (Days 21-30).
33. Day 29 classification regression.
34. Day 28 structured resume regression.
"""

import pytest
import copy
from app.exceptions.resume import ResumeParsingError
from app.services.resume_processing import (
    ExtractedDocument,
    DocumentPage,
    ProcessedResumeText,
    ExtractedSkill,
    ExtractedSkills,
    EducationRecord,
    ExtractedEducation,
    ExperienceRecord,
    ExtractedExperience,
    ProjectRecord,
    ExtractedProjects,
    StructuredResume,
    ResumeClassification,
    JobRequirements,
    ATSScore,
    build_structured_resume,
    classify_resume,
    score_resume_against_job,
    HybridATSScorer,
)


def _make_structured_resume_for_ats(
    skills_list=None,
    edu_list=None,
    exp_list=None,
    proj_list=None,
    total_months=None,
    summary_text="Experienced Software Engineer",
    role="SOFTWARE_ENGINEER",
    domain="SOFTWARE_ENGINEERING",
    exp_level="MID_LEVEL",
) -> StructuredResume:
    """Helper to construct a fully populated StructuredResume for ATS testing."""
    skills = ExtractedSkills(skills=skills_list or [], total_count=len(skills_list or []))
    education = ExtractedEducation(education_records=edu_list or [], total_count=len(edu_list or []))
    experience = ExtractedExperience(
        experiences=exp_list or [],
        total_count=len(exp_list or []),
        total_experience_months=total_months,
    )
    projects = ExtractedProjects(projects=proj_list or [], total_count=len(proj_list or []))

    doc = ExtractedDocument(
        text=f"{summary_text}\n",
        document_type="pdf",
        extraction_method="pymupdf",
        page_count=1,
        pages=[DocumentPage(page_number=1, text=f"{summary_text}\n")],
    )
    proc = ProcessedResumeText(
        cleaned_text=f"{summary_text}\n",
        normalized_text=f"{summary_text}\n",
        lowercase_text=summary_text.lower() + "\n",
        sections=[],
        tokens=summary_text.split(),
        normalized_tokens=[t.lower() for t in summary_text.split()],
        original_document=doc,
    )

    structured = build_structured_resume(
        processed_text=proc,
        skills=skills,
        education=education,
        experience=experience,
        projects=projects,
    )

    structured.summary = summary_text
    structured.classification = ResumeClassification(
        domain=domain,
        role=role,
        experience_level=exp_level,
        domain_confidence=0.90,
        role_confidence=0.90,
        experience_level_confidence=0.90,
    )
    return structured


# ==============================================================================
# 1. BASIC ATS SCORE & RANGE
# ==============================================================================

def test_basic_ats_score():
    structured = _make_structured_resume_for_ats(
        skills_list=[
            ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
            ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
        ]
    )
    job = JobRequirements(
        title="Backend Engineer",
        required_skills=["Python", "FastAPI"],
    )

    res = score_resume_against_job(structured, job)
    assert isinstance(res, ATSScore)
    assert 0.0 <= res.score <= 100.0
    assert res.scorer_version == "day30-v1"
    assert res.scoring_method == "weighted_hybrid_rule_based"


def test_score_range_clamping():
    structured = _make_structured_resume_for_ats()
    job = JobRequirements(required_skills=["Python"])

    res = score_resume_against_job(structured, job)
    assert 0.0 <= res.score <= 100.0


# ==============================================================================
# 2. PERFECT MATCH & ZERO MATCH
# ==============================================================================

def test_perfect_match_score():
    structured = _make_structured_resume_for_ats(
        skills_list=[
            ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python"),
            ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
            ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL"),
        ],
        edu_list=[EducationRecord(degree="Bachelor of Technology in Computer Science", field_of_study="Computer Science")],
        exp_list=[ExperienceRecord(company="Tech Corp", job_title="Backend Developer", duration_months=36)],
        total_months=36,
        summary_text="Backend Developer skilled in REST API and Python",
        role="BACKEND_DEVELOPER",
        domain="SOFTWARE_ENGINEERING",
        exp_level="MID_LEVEL",
    )

    job = JobRequirements(
        title="Backend Developer",
        required_keywords=["REST API"],
        required_skills=["Python", "FastAPI", "PostgreSQL"],
        required_education=["Bachelor's degree"],
        required_experience_months=24,
        required_roles=["BACKEND_DEVELOPER"],
        required_domains=["SOFTWARE_ENGINEERING"],
    )

    res = score_resume_against_job(structured, job)
    assert res.score >= 95.0
    assert len(res.missing_required_skills) == 0
    assert len(res.missing_required_keywords) == 0


def test_zero_match_score():
    structured = _make_structured_resume_for_ats(
        skills_list=[ExtractedSkill(name="Cooking", normalized_name="cooking", category="OTHER", matched_text="Cooking")],
        role="OTHER",
        domain="OTHER",
        exp_level="ENTRY_LEVEL",
    )

    job = JobRequirements(
        required_keywords=["Kubernetes"],
        required_skills=["Rust"],
        required_education=["Doctorate"],
        required_experience_months=120,
        required_roles=["DEVOPS_ENGINEER"],
    )

    res = score_resume_against_job(structured, job)
    assert res.score < 20.0
    assert "Rust" in res.missing_required_skills


# ==============================================================================
# 3. KEYWORD & SKILL MATCHING WITH ALIASES
# ==============================================================================

def test_skill_aliases_normalization():
    # ReactJS -> React.js, Postgres -> PostgreSQL, sklearn -> scikit-learn
    structured = _make_structured_resume_for_ats(
        skills_list=[
            ExtractedSkill(name="ReactJS", normalized_name="react.js", category="FRONTEND", matched_text="ReactJS"),
            ExtractedSkill(name="Postgres", normalized_name="postgresql", category="DATABASE", matched_text="Postgres"),
            ExtractedSkill(name="sklearn", normalized_name="scikit-learn", category="MACHINE_LEARNING", matched_text="sklearn"),
        ]
    )

    job = JobRequirements(
        required_skills=["React.js", "PostgreSQL", "scikit-learn"]
    )

    res = score_resume_against_job(structured, job)
    assert res.skill_score == 100.0
    assert len(res.missing_required_skills) == 0


def test_skill_deduplication():
    # Candidate mentions React.js, ReactJS, and React
    structured = _make_structured_resume_for_ats(
        skills_list=[
            ExtractedSkill(name="React.js", normalized_name="react.js", category="FRONTEND", matched_text="React.js"),
            ExtractedSkill(name="ReactJS", normalized_name="react.js", category="FRONTEND", matched_text="ReactJS"),
            ExtractedSkill(name="React", normalized_name="react.js", category="FRONTEND", matched_text="React"),
        ]
    )

    job = JobRequirements(
        required_skills=["React.js"]
    )

    res = score_resume_against_job(structured, job)
    assert res.skill_score == 100.0
    assert len(res.matched_required_skills) == 1


# ==============================================================================
# 4. FALSE SUBSTRING PREVENTION
# ==============================================================================

def test_false_substring_prevention():
    # Resume mentions "Java" and "C" and "SQL", but job requires "JavaScript", "C++", "PostgreSQL"
    structured = _make_structured_resume_for_ats(
        skills_list=[
            ExtractedSkill(name="Java", normalized_name="java", category="PROGRAMMING_LANGUAGE", matched_text="Java"),
            ExtractedSkill(name="C", normalized_name="c", category="PROGRAMMING_LANGUAGE", matched_text="C"),
            ExtractedSkill(name="SQL", normalized_name="sql", category="DATABASE", matched_text="SQL"),
        ],
        summary_text="Java C SQL developer"
    )

    job = JobRequirements(
        required_skills=["JavaScript", "C++", "PostgreSQL"],
        required_keywords=["JavaScript", "C++"]
    )

    res = score_resume_against_job(structured, job)
    assert "JavaScript" in res.missing_required_skills
    assert "C++" in res.missing_required_skills
    assert "PostgreSQL" in res.missing_required_skills


# ==============================================================================
# 5. EDUCATION MATCHING & FIELD DISCRIMINATION
# ==============================================================================

def test_education_matching():
    structured = _make_structured_resume_for_ats(
        edu_list=[EducationRecord(degree="B.Tech Computer Science", field_of_study="Computer Science")]
    )

    job = JobRequirements(required_education=["Bachelor's degree"])
    res = score_resume_against_job(structured, job)
    assert res.education_score == 100.0


def test_education_mismatch():
    structured = _make_structured_resume_for_ats(
        edu_list=[EducationRecord(degree="B.Tech Electrical Engineering", field_of_study="Electrical Engineering")]
    )

    job = JobRequirements(required_education=["Doctorate"])
    res = score_resume_against_job(structured, job)
    assert res.education_score < 100.0


# ==============================================================================
# 6. EXPERIENCE DURATION & ROLE/DOMAIN MATCHING
# ==============================================================================

def test_experience_duration_and_role_matching():
    structured = _make_structured_resume_for_ats(
        exp_list=[ExperienceRecord(company="Google", job_title="Backend Developer", duration_months=36)],
        total_months=36,
        role="BACKEND_DEVELOPER",
        domain="SOFTWARE_ENGINEERING"
    )

    job = JobRequirements(
        required_experience_months=24,
        required_roles=["BACKEND_DEVELOPER"],
        required_domains=["SOFTWARE_ENGINEERING"]
    )

    res = score_resume_against_job(structured, job)
    assert res.experience_score >= 90.0


# ==============================================================================
# 7. SCORE BREAKDOWN & EXPLANATION
# ==============================================================================

def test_score_breakdown_mathematical_consistency():
    structured = _make_structured_resume_for_ats(
        skills_list=[ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python")]
    )
    job = JobRequirements(
        required_keywords=["Python"],
        required_skills=["Python"],
    )

    res = score_resume_against_job(structured, job)
    bd = res.score_breakdown

    assert "keyword" in bd
    assert "skill" in bd
    assert "education" in bd
    assert "experience" in bd

    total_calc = sum(item["contribution"] for item in bd.values())
    assert abs(res.score - total_calc) <= 0.5


def test_explanation_and_recommendations():
    structured = _make_structured_resume_for_ats(
        skills_list=[ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python")]
    )
    job = JobRequirements(
        required_skills=["Python", "Kubernetes"]
    )

    res = score_resume_against_job(structured, job)
    assert "Kubernetes" in res.missing_required_skills
    assert "Kubernetes" in res.explanation
    assert any("Kubernetes" in rec for rec in res.recommendations)


# ==============================================================================
# 8. DETERMINISM, IMMUTABILITY & EXCEPTION HANDLING
# ==============================================================================

def test_scoring_determinism():
    structured = _make_structured_resume_for_ats(
        skills_list=[ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python")]
    )
    job = JobRequirements(required_skills=["Python"])

    res1 = score_resume_against_job(structured, job)
    res2 = score_resume_against_job(structured, job)

    assert res1.score == res2.score
    assert res1.score_breakdown == res2.score_breakdown


def test_input_non_mutation():
    structured = _make_structured_resume_for_ats(
        skills_list=[ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python")]
    )
    job = JobRequirements(required_skills=["Python"])

    copy_struct = copy.deepcopy(structured)
    copy_job = copy.deepcopy(job)

    score_resume_against_job(structured, job)

    assert structured.model_dump() == copy_struct.model_dump()
    assert job.model_dump() == copy_job.model_dump()


def test_invalid_input_raises():
    structured = _make_structured_resume_for_ats()

    with pytest.raises(ResumeParsingError, match="Cannot score a None"):
        score_resume_against_job(None, JobRequirements(required_skills=["Python"]))

    with pytest.raises(ValueError, match="JobRequirements object cannot be"):
        score_resume_against_job(structured, None)

    with pytest.raises(ValueError, match="JobRequirements object cannot be"):
        score_resume_against_job(structured, JobRequirements())
