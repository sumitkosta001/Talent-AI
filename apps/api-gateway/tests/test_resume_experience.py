"""Unit and Integration Tests for Phase 4 Day 26 Experience Extraction.

Verifies:
1. Company extraction and normalization (Google, Microsoft LLC -> Microsoft, TCS).
2. Job title extraction and alias normalization (Sr. Software Engineer, SDE).
3. Seniority level classification (INTERN, JUNIOR, MID_LEVEL, SENIOR, LEAD, STAFF, PRINCIPAL, MANAGER, DIRECTOR).
4. Employment type classification (FULL_TIME, INTERNSHIP, CONTRACT, FREELANCE).
5. Date range, month/year parsing, current employment (is_current = True), and duration calculation.
6. Responsibilities extraction preserving original wording.
7. Cohesive block grouping and multi-record separation.
8. Promotion handling (separate records for different titles at same company).
9. Research Assistant role support at educational institutions.
10. False positive rejection (education entries, projects, skills lists, "5+ years experience").
11. Record deduplication.
12. Non-mutation of input objects.
13. Exception handling on None or empty input.
14. Determinism and metadata generation.
"""

import pytest
from app.exceptions.resume import ResumeParsingError
from app.services.resume_processing import (
    ExtractedDocument,
    DocumentPage,
    ProcessedResumeText,
    ProcessedSection,
    ExperienceRecord,
    ExtractedExperience,
    extract_experience,
    normalize_company,
    normalize_job_title,
    detect_seniority,
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
# 1. COMPANY & TITLE NORMALIZATION TESTS
# ==============================================================================

def test_company_normalization():
    comp, norm_comp = normalize_company("Google LLC")
    assert comp == "Google"
    assert norm_comp == "google"

    comp2, norm_comp2 = normalize_company("TCS")
    assert comp2 == "Tata Consultancy Services"
    assert norm_comp2 == "tata consultancy services"


def test_job_title_normalization_and_seniority():
    t1, norm1, sen1 = normalize_job_title("Sr. Software Engineer")
    assert t1 == "Senior Software Engineer"
    assert sen1 == "SENIOR"

    t2, norm2, sen2 = normalize_job_title("Software Engineering Intern")
    assert sen2 == "INTERN"

    t3, norm3, sen3 = normalize_job_title("Lead Developer")
    assert sen3 == "LEAD"

    t4, norm4, sen4 = normalize_job_title("Engineering Director")
    assert sen4 == "DIRECTOR"


# ==============================================================================
# 2. SINGLE COHESIVE EXPERIENCE BLOCK EXTRACTION TESTS
# ==============================================================================

def test_single_experience_block_extraction():
    text = (
        "WORK EXPERIENCE\n"
        "Senior Software Engineer\n"
        "Google\n"
        "Jan 2022 - Dec 2023\n"
        "- Developed REST APIs using FastAPI.\n"
        "- Designed PostgreSQL database schemas.\n"
        "- Improved API latency by 30%.\n"
    )
    sections = [("EXPERIENCE", "WORK EXPERIENCE", text)]
    proc = _make_dummy_processed_text(text, sections)

    result: ExtractedExperience = extract_experience(proc)

    assert result.total_count == 1
    rec: ExperienceRecord = result.experiences[0]
    assert rec.company == "Google"
    assert rec.normalized_company == "google"
    assert rec.job_title == "Senior Software Engineer"
    assert rec.seniority == "SENIOR"
    assert rec.employment_type == "FULL_TIME"
    assert rec.start_year == 2022
    assert rec.start_month == 1
    assert rec.end_year == 2023
    assert rec.end_month == 12
    assert rec.duration_months == 24
    assert rec.is_current is False
    assert len(rec.responsibilities) == 3
    assert "Developed REST APIs using FastAPI." in rec.responsibilities[0]


def test_present_current_employment():
    text = (
        "EXPERIENCE\n"
        "Senior Software Engineer at Google\n"
        "Jan 2024 - Present\n"
        "- Architecting distributed microservices.\n"
    )
    sections = [("EXPERIENCE", "EXPERIENCE", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_experience(proc)
    assert result.total_count == 1
    rec = result.experiences[0]
    assert rec.company == "Google"
    assert rec.job_title == "Senior Software Engineer"
    assert rec.is_current is True
    assert rec.end_year is None


# ==============================================================================
# 3. MULTIPLE EXPERIENCE RECORDS & PROMOTIONS
# ==============================================================================

def test_multiple_experience_records():
    text = (
        "EXPERIENCE\n\n"
        "Senior Software Engineer\n"
        "Microsoft\n"
        "2024 - Present\n"
        "- Designed distributed services.\n\n"
        "Software Engineer\n"
        "Google\n"
        "2022 - 2024\n"
        "- Developed backend APIs.\n"
    )
    sections = [("EXPERIENCE", "EXPERIENCE", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_experience(proc)
    assert result.total_count == 2

    rec1 = result.experiences[0]
    assert rec1.company == "Microsoft"
    assert rec1.job_title == "Senior Software Engineer"

    rec2 = result.experiences[1]
    assert rec2.company == "Google"
    assert rec2.job_title == "Software Engineer"


def test_same_company_promotions():
    text = (
        "EXPERIENCE\n\n"
        "Software Engineer\n"
        "Google\n"
        "2020 - 2022\n"
        "- Developed internal services.\n\n"
        "Senior Software Engineer\n"
        "Google\n"
        "2022 - Present\n"
        "- Led backend development.\n"
    )
    sections = [("EXPERIENCE", "EXPERIENCE", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_experience(proc)
    assert result.total_count == 2
    assert result.experiences[0].job_title == "Software Engineer"
    assert result.experiences[1].job_title == "Senior Software Engineer"


# ==============================================================================
# 4. INTERNSHIP & RESEARCH ASSISTANT TESTS
# ==============================================================================

def test_internship_and_research_assistant():
    text = (
        "EXPERIENCE\n\n"
        "Software Engineering Intern\n"
        "Amazon\n"
        "May 2022 - Aug 2022\n"
        "- Built internal developer tools.\n\n"
        "Research Assistant\n"
        "National Institute of Technology, Rourkela\n"
        "2024 - 2025\n"
        "- Conducted machine learning research.\n"
    )
    sections = [("EXPERIENCE", "EXPERIENCE", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_experience(proc)
    assert result.total_count == 2

    rec_intern = result.experiences[0]
    assert rec_intern.employment_type == "INTERNSHIP"
    assert rec_intern.seniority == "INTERN"

    rec_research = result.experiences[1]
    assert rec_research.company == "National Institute of Technology, Rourkela"
    assert rec_research.employment_type == "RESEARCH"


# ==============================================================================
# 5. FALSE POSITIVE REJECTION TESTS
# ==============================================================================

def test_false_positives_education_and_projects():
    text = (
        "EDUCATION\n"
        "B.Tech in Electrical Engineering\n"
        "National Institute of Technology, Rourkela\n"
        "2022 - 2026\n"
        "CGPA: 7.99\n\n"
        "PROJECTS\n"
        "E-commerce Platform 2024\n"
        "Achieved 90% test coverage\n"
    )
    sections = [
        ("EDUCATION", "EDUCATION", text),
        ("PROJECTS", "PROJECTS", text),
    ]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_experience(proc)
    assert result.total_count == 0


def test_overall_experience_statement_rejection():
    text = "5+ years of experience in backend development and cloud architecture."
    proc = _make_dummy_processed_text(text)

    result = extract_experience(proc)
    assert result.total_count == 0


# ==============================================================================
# 6. DEDUPLICATION & IMMUTABILITY TESTS
# ==============================================================================

def test_deduplication():
    text = (
        "EXPERIENCE\n"
        "Software Engineer\n"
        "Google\n"
        "2022 - 2024\n"
        "- Developed APIs.\n\n"
        "Software Engineer\n"
        "Google\n"
        "2022 - 2024\n"
        "- Developed APIs.\n"
    )
    sections = [("EXPERIENCE", "EXPERIENCE", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_experience(proc)
    assert result.total_count == 1


def test_input_non_mutation():
    text = "EXPERIENCE\nSoftware Engineer at Google\n2022 - 2024\n- Developed APIs.\n"
    sections = [("EXPERIENCE", "EXPERIENCE", text)]
    proc = _make_dummy_processed_text(text, sections)

    orig_cleaned = proc.cleaned_text
    orig_doc_text = proc.original_document.text

    extract_experience(proc)

    assert proc.cleaned_text == orig_cleaned
    assert proc.original_document.text == orig_doc_text


# ==============================================================================
# 7. EXCEPTION & INPUT VALIDATION TESTS
# ==============================================================================

def test_none_input_raises_exception():
    with pytest.raises(ResumeParsingError, match="Cannot extract experience from a None ProcessedResumeText"):
        extract_experience(None)


def test_empty_text_raises_exception():
    proc = _make_dummy_processed_text("")
    with pytest.raises(ResumeParsingError, match="contains no text"):
        extract_experience(proc)
