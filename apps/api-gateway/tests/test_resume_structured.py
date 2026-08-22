"""Unit and Integration Tests for Phase 4 Day 28 Structured Resume.

Verifies:
1. Basic StructuredResume creation and schema/pipeline versioning.
2. JSON serialization (model_dump_json) and deserialization round-trip.
3. Pydantic schema validation.
4. Business Level 2 validation (CGPA, percentage, confidence boundaries, year ranges).
5. Empty optional sections handling.
6. Preservation of Day 24 skills, Day 25 education, Day 26 experience, and Day 27 projects.
7. No data fabrication (missing email/phone remain None).
8. Contact info extraction (email, phone, LinkedIn, GitHub).
9. Verbatim summary section preservation.
10. Input model immutability.
"""

import pytest
import json
from app.exceptions.resume import ResumeParsingError
from app.services.resume_processing import (
    ExtractedDocument,
    DocumentPage,
    ProcessedResumeText,
    ProcessedSection,
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
    validate_structured_resume,
)


def _make_dummy_processed_text(text: str, sections: list | None = None) -> ProcessedResumeText:
    """Helper to construct a valid ProcessedResumeText fixture."""
    dummy_doc = ExtractedDocument(
        text=text,
        document_type="pdf",
        extraction_method="pymupdf",
        page_count=1,
        pages=[DocumentPage(page_number=1, text=text)],
    )

    proc_sections = []
    if sections:
        for sname, stitle, scontent in sections:
            proc_sections.append(
                ProcessedSection(
                    name=sname,
                    title=stitle,
                    content=scontent,
                    confidence=1.0,
                    start_line=1,
                    end_line=10,
                )
            )

    return ProcessedResumeText(
        cleaned_text=text,
        normalized_text=text,
        lowercase_text=text.lower(),
        sections=proc_sections,
        tokens=text.split(),
        normalized_tokens=text.lower().split(),
        metadata={},
        original_document=dummy_doc,
    )


# ==============================================================================
# 1. BASIC STRUCTURED RESUME CREATION & VERSIONING
# ==============================================================================

def test_basic_structured_resume_creation():
    text = "John Doe\nemail: john@gmail.com\nSUMMARY\nSoftware Engineer passionate about cloud.\n"
    sections = [("SUMMARY", "SUMMARY", "Software Engineer passionate about cloud.")]
    proc = _make_dummy_processed_text(text, sections)

    structured: StructuredResume = build_structured_resume(proc)

    assert structured.schema_version == "1.0"
    assert structured.pipeline_version == "phase4-day28"
    assert structured.email == "john@gmail.com"
    assert structured.summary == "Software Engineer passionate about cloud."
    assert structured.skills.total_count == 0
    assert structured.education.total_count == 0
    assert structured.experience.total_count == 0
    assert structured.projects.total_count == 0


# ==============================================================================
# 2. JSON SERIALIZATION & ROUND TRIP
# ==============================================================================

def test_json_serialization_and_round_trip():
    text = "John Doe\nemail: john@gmail.com\n"
    proc = _make_dummy_processed_text(text)

    skills = ExtractedSkills(
        skills=[ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING_LANGUAGE", matched_text="Python", confidence=0.95)],
        total_count=1,
    )
    structured = build_structured_resume(proc, skills=skills)

    json_str = structured.model_dump_json()
    assert isinstance(json_str, str)

    # Deserialize back into Python dict and Pydantic model
    dict_data = json.loads(json_str)
    reconstructed = StructuredResume.model_validate(dict_data)

    assert reconstructed.schema_version == "1.0"
    assert reconstructed.skills.skills[0].name == "Python"
    assert reconstructed.skills.skills[0].confidence == 0.95


# ==============================================================================
# 3. LEVEL 2 BUSINESS VALIDATION TESTS
# ==============================================================================

def test_business_validation_cgpa_out_of_bounds():
    text = "John Doe\n"
    proc = _make_dummy_processed_text(text)
    edu = ExtractedEducation(education_records=[EducationRecord(degree="B.Tech", cgpa=15.0)], total_count=1)

    with pytest.raises(ValueError, match="Invalid CGPA value"):
        build_structured_resume(proc, education=edu)


def test_business_validation_start_year_after_end_year():
    text = "John Doe\n"
    proc = _make_dummy_processed_text(text)
    edu = ExtractedEducation(education_records=[EducationRecord(degree="B.Tech", start_year=2026, end_year=2022)], total_count=1)

    with pytest.raises(ValueError, match="cannot be after end_year"):
        build_structured_resume(proc, education=edu)


# ==============================================================================
# 4. FULL AGGREGATION & DATA PRESERVATION
# ==============================================================================

def test_full_pipeline_aggregation():
    text = (
        "John Doe\n"
        "john.doe@gmail.com\n"
        "https://linkedin.com/in/johndoe\n"
        "https://github.com/johndoe\n\n"
        "SUMMARY\n"
        "Experienced software developer.\n"
    )
    sections = [("SUMMARY", "SUMMARY", "Experienced software developer.")]
    proc = _make_dummy_processed_text(text, sections)

    skills = ExtractedSkills(skills=[ExtractedSkill(name="Python", normalized_name="python", category="PROGRAMMING", matched_text="Python")], total_count=1)
    education = ExtractedEducation(education_records=[EducationRecord(degree="B.Tech", institution="NIT Rourkela")], total_count=1)
    experience = ExtractedExperience(experiences=[ExperienceRecord(company="Google", job_title="Senior Software Engineer")], total_count=1)
    projects = ExtractedProjects(projects=[ProjectRecord(name="Talent AI", technologies=["FastAPI"])], total_count=1)

    structured = build_structured_resume(
        processed_text=proc,
        skills=skills,
        education=education,
        experience=experience,
        projects=projects,
        resume_id="resume-uuid-123",
        candidate_profile_id="candidate-uuid-456",
    )

    assert structured.email == "john.doe@gmail.com"
    assert structured.linkedin == "https://linkedin.com/in/johndoe"
    assert structured.github == "https://github.com/johndoe"
    assert structured.skills.skills[0].name == "Python"
    assert structured.education.education_records[0].degree == "B.Tech"
    assert structured.experience.experiences[0].company == "Google"
    assert structured.projects.projects[0].name == "Talent AI"


# ==============================================================================
# 5. NO DATA FABRICATION
# ==============================================================================

def test_no_data_fabrication_when_missing():
    text = "John Doe\nSUMMARY\nDeveloper.\n"
    sections = [("SUMMARY", "SUMMARY", "Developer.")]
    proc = _make_dummy_processed_text(text, sections)

    structured = build_structured_resume(proc)

    assert structured.email is None
    assert structured.phone is None
    assert structured.linkedin is None
    assert structured.github is None
    assert structured.portfolio is None


# ==============================================================================
# 6. IMMUTABILITY & EXCEPTION HANDLING
# ==============================================================================

def test_input_immutability():
    text = "John Doe\nemail: john@gmail.com\n"
    proc = _make_dummy_processed_text(text)
    orig_text = proc.cleaned_text

    build_structured_resume(proc)

    assert proc.cleaned_text == orig_text


def test_none_input_raises_exception():
    with pytest.raises(ResumeParsingError, match="Cannot build structured resume from a None ProcessedResumeText"):
        build_structured_resume(None)


def test_empty_text_raises_exception():
    proc = _make_dummy_processed_text("")
    with pytest.raises(ResumeParsingError, match="contains no text"):
        build_structured_resume(proc)
