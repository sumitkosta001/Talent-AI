"""Unit and Integration Tests for Phase 4 Day 29 Resume Classification.

Verifies:
1. Candidate domain classification (SOFTWARE_ENGINEERING, MACHINE_LEARNING, EMBEDDED_SYSTEMS, etc.).
2. Candidate role prediction (FULL_STACK_DEVELOPER, BACKEND_DEVELOPER, FRONTEND_DEVELOPER, ML_ENGINEER, etc.).
3. Experience level prediction (INTERN, ENTRY_LEVEL, MID_LEVEL, SENIOR, LEAD, etc.).
4. Title alias resolution (SDE, SDE-1, SDE II -> SOFTWARE_ENGINEER).
5. Non-dominance of education (software skills/experience override electrical degree).
6. Heuristic confidence scores bounded between 0.0 and 1.0.
7. Explainable evidence generation.
8. Determinism and input immutability.
9. Classification versioning (day29-v1) and method (hybrid_rule_based).
10. Exception handling for None input.
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
    build_structured_resume,
    classify_resume,
    ResumeClassification,
)


def _make_dummy_structured_resume(
    skills_list=None,
    edu_list=None,
    exp_list=None,
    proj_list=None,
    total_months=None,
) -> StructuredResume:
    """Helper fixture to construct a StructuredResume for classifier testing."""
    skills = ExtractedSkills(
        skills=skills_list or [],
        total_count=len(skills_list or []),
    )
    education = ExtractedEducation(
        education_records=edu_list or [],
        total_count=len(edu_list or []),
    )
    experience = ExtractedExperience(
        experiences=exp_list or [],
        total_count=len(exp_list or []),
        total_experience_months=total_months,
    )
    projects = ExtractedProjects(
        projects=proj_list or [],
        total_count=len(proj_list or []),
    )

    doc = ExtractedDocument(
        text="John Doe\n",
        document_type="pdf",
        extraction_method="pymupdf",
        page_count=1,
        pages=[DocumentPage(page_number=1, text="John Doe\n")],
    )

    proc = ProcessedResumeText(
        cleaned_text="John Doe\n",
        normalized_text="John Doe\n",
        lowercase_text="john doe\n",
        sections=[],
        tokens=["John", "Doe"],
        normalized_tokens=["john", "doe"],
        original_document=doc,
    )

    return build_structured_resume(
        processed_text=proc,
        skills=skills,
        education=education,
        experience=experience,
        projects=projects,
    )


# ==============================================================================
# 1. BASIC CLASSIFICATION & VERSIONING
# ==============================================================================

def test_basic_classification_structure():
    structured = _make_dummy_structured_resume(
        skills_list=[
            ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING", matched_text="Python"),
            ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
        ]
    )

    res: ResumeClassification = structured.classification or classify_resume(structured)

    assert isinstance(res, ResumeClassification)
    assert res.classifier_version == "day29-v1"
    assert res.classification_method == "hybrid_rule_based"
    assert 0.0 <= res.domain_confidence <= 1.0
    assert 0.0 <= res.role_confidence <= 1.0
    assert 0.0 <= res.experience_level_confidence <= 1.0
    assert "domain_evidence" in res.evidence


# ==============================================================================
# 2. DOMAIN CLASSIFICATION TESTS
# ==============================================================================

def test_software_engineering_domain():
    structured = _make_dummy_structured_resume(
        skills_list=[
            ExtractedSkill(name="React", normalized_name="react.js", category="FRAMEWORK", matched_text="React"),
            ExtractedSkill(name="Node.js", normalized_name="node.js", category="FRAMEWORK", matched_text="Node.js"),
            ExtractedSkill(name="PostgreSQL", normalized_name="postgresql", category="DATABASE", matched_text="PostgreSQL"),
        ],
        exp_list=[ExperienceRecord(company="Tech Corp", job_title="Full Stack Developer")],
    )

    res = classify_resume(structured)
    assert res.domain == "SOFTWARE_ENGINEERING"
    assert res.role == "FULL_STACK_DEVELOPER"


def test_machine_learning_domain():
    structured = _make_dummy_structured_resume(
        skills_list=[
            ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING", matched_text="Python"),
            ExtractedSkill(name="TensorFlow", normalized_name="tensorflow", category="MACHINE_LEARNING", matched_text="TensorFlow"),
            ExtractedSkill(name="PyTorch", normalized_name="pytorch", category="MACHINE_LEARNING", matched_text="PyTorch"),
        ],
        proj_list=[ProjectRecord(name="Object Detector", classification="MACHINE_LEARNING")],
    )

    res = classify_resume(structured)
    assert res.domain == "MACHINE_LEARNING"
    assert res.role == "MACHINE_LEARNING_ENGINEER"


def test_embedded_systems_domain():
    structured = _make_dummy_structured_resume(
        skills_list=[
            ExtractedSkill(name="Embedded C", normalized_name="embedded c", category="PROGRAMMING", matched_text="Embedded C"),
            ExtractedSkill(name="Arduino", normalized_name="arduino", category="OTHER", matched_text="Arduino"),
            ExtractedSkill(name="STM32", normalized_name="stm32", category="OTHER", matched_text="STM32"),
        ],
        exp_list=[ExperienceRecord(company="Hardware Inc", job_title="Embedded Engineer")],
    )

    res = classify_resume(structured)
    assert res.domain == "EMBEDDED_SYSTEMS"
    assert res.role == "EMBEDDED_ENGINEER"


# ==============================================================================
# 3. NON-DOMINANCE OF EDUCATION
# ==============================================================================

def test_education_non_dominance():
    # Electrical degree, but Software Engineer experience and Full-Stack skills
    structured = _make_dummy_structured_resume(
        edu_list=[EducationRecord(degree="B.Tech Electrical Engineering", field_of_study="Electrical Engineering")],
        skills_list=[
            ExtractedSkill(name="React", normalized_name="react.js", category="FRAMEWORK", matched_text="React"),
            ExtractedSkill(name="FastAPI", normalized_name="fastapi", category="FRAMEWORK", matched_text="FastAPI"),
        ],
        exp_list=[ExperienceRecord(company="ABC Software", job_title="Software Engineer")],
    )

    res = classify_resume(structured)
    assert res.domain == "SOFTWARE_ENGINEERING"
    assert res.role in {"SOFTWARE_ENGINEER", "FULL_STACK_DEVELOPER"}


# ==============================================================================
# 4. TITLE ALIAS RESOLUTION & SENIORITY
# ==============================================================================

def test_title_aliases_and_seniority():
    structured = _make_dummy_structured_resume(
        exp_list=[ExperienceRecord(company="Amazon", job_title="SDE-1", seniority="ENTRY_LEVEL")],
        total_months=10,
    )

    res = classify_resume(structured)
    assert res.role == "SOFTWARE_ENGINEER"
    assert res.experience_level == "ENTRY_LEVEL"


def test_internship_classification():
    structured = _make_dummy_structured_resume(
        exp_list=[ExperienceRecord(company="Google", job_title="Software Engineering Intern")],
        total_months=6,
    )

    res = classify_resume(structured)
    assert res.experience_level == "INTERN"


def test_senior_experience_level():
    structured = _make_dummy_structured_resume(
        exp_list=[
            ExperienceRecord(company="Google", job_title="Senior Software Engineer", seniority="SENIOR"),
            ExperienceRecord(company="Amazon", job_title="Software Engineer"),
        ],
        total_months=60,
    )

    res = classify_resume(structured)
    assert res.experience_level == "SENIOR"


# ==============================================================================
# 5. UNKNOWN & LOW CONFIDENCE RESUME
# ==============================================================================

def test_unknown_empty_resume():
    structured = _make_dummy_structured_resume()

    res = classify_resume(structured)
    assert res.domain in {"UNKNOWN", "SOFTWARE_ENGINEERING"}
    assert res.role in {"UNKNOWN", "SOFTWARE_ENGINEER"}
    assert res.experience_level == "ENTRY_LEVEL"


# ==============================================================================
# 6. DETERMINISM & IMMUTABILITY
# ==============================================================================

def test_determinism_and_immutability():
    structured = _make_dummy_structured_resume(
        skills_list=[ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING", matched_text="Python")]
    )

    copy_structured = copy.deepcopy(structured)

    res1 = classify_resume(structured)
    res2 = classify_resume(structured)

    assert res1.domain == res2.domain
    assert res1.role == res2.role
    assert res1.experience_level == res2.experience_level
    assert structured.model_dump() == copy_structured.model_dump()


def test_none_input_raises_exception():
    with pytest.raises(ResumeParsingError, match="Cannot classify a None"):
        classify_resume(None)
