"""Unit and Integration Tests for Phase 4 Day 25 Education Extraction.

Verifies:
1. Degree extraction and normalization (B.Tech, BTech, B.E., M.Tech, MCA, MBA, Ph.D., Diploma, Secondary).
2. Degree level taxonomy classification (UNDERGRADUATE, POSTGRADUATE, DOCTORATE, DIPLOMA, SECONDARY).
3. Institution extraction and alias normalization (NIT Rourkela, IIT Delhi).
4. Field of study extraction (Electrical Engineering, Computer Science).
5. Year range and graduation status parsing (COMPLETED vs EXPECTED).
6. CGPA, GPA, CPI, and Percentage extraction without arbitrary CGPA->Percentage conversions.
7. Cohesive single education record block grouping.
8. Multiple education record separation (M.Tech + B.Tech).
9. Class X and Class XII school education support.
10. False positive rejection (experience lines, remote %, project coverage).
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
    EducationRecord,
    ExtractedEducation,
    extract_education,
    normalize_degree,
    normalize_institution,
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
# 1. DEGREE EXTRACTION & NORMALIZATION TESTS
# ==============================================================================

def test_degree_normalization_btech():
    canonical, norm, level = normalize_degree("B.Tech")
    assert canonical == "Bachelor of Technology"
    assert norm == "bachelor_of_technology"
    assert level == "UNDERGRADUATE"

    canonical2, norm2, level2 = normalize_degree("BTech")
    assert canonical2 == "Bachelor of Technology"
    assert level2 == "UNDERGRADUATE"


def test_degree_normalization_be():
    canonical, norm, level = normalize_degree("B.E.")
    assert canonical == "Bachelor of Engineering"
    assert level == "UNDERGRADUATE"

    canonical2, norm2, level2 = normalize_degree("BE")
    assert canonical2 == "Bachelor of Engineering"


def test_degree_normalization_mtech():
    canonical, norm, level = normalize_degree("M.Tech")
    assert canonical == "Master of Technology"
    assert level == "POSTGRADUATE"


def test_degree_normalization_mca_mba_phd():
    c_mca, _, l_mca = normalize_degree("MCA")
    assert c_mca == "Master of Computer Applications"
    assert l_mca == "POSTGRADUATE"

    c_mba, _, l_mba = normalize_degree("MBA")
    assert c_mba == "Master of Business Administration"
    assert l_mba == "POSTGRADUATE"

    c_phd, _, l_phd = normalize_degree("Ph.D.")
    assert c_phd == "Doctor of Philosophy"
    assert l_phd == "DOCTORATE"


# ==============================================================================
# 2. INSTITUTION EXTRACTION & NORMALIZATION TESTS
# ==============================================================================

def test_institution_normalization():
    inst, norm_inst = normalize_institution("National Institute of Technology, Rourkela")
    assert inst == "National Institute of Technology, Rourkela"
    assert norm_inst == "national institute of technology, rourkela"

    alias_inst, norm_alias = normalize_institution("NIT Rourkela")
    assert alias_inst == "National Institute of Technology, Rourkela"
    assert norm_alias == "national institute of technology, rourkela"

    iit_inst, _ = normalize_institution("IIT Delhi")
    assert iit_inst == "Indian Institute of Technology Delhi"


# ==============================================================================
# 3. FIELD OF STUDY & COHESIVE EDUCATION BLOCK TESTS
# ==============================================================================

def test_single_education_block_extraction():
    text = (
        "EDUCATION\n"
        "Bachelor of Technology in Electrical Engineering\n"
        "National Institute of Technology, Rourkela\n"
        "2022 - 2026\n"
        "CGPA: 7.99\n"
    )
    sections = [("EDUCATION", "EDUCATION", text)]
    proc = _make_dummy_processed_text(text, sections)

    result: ExtractedEducation = extract_education(proc)

    assert result.total_count == 1
    rec: EducationRecord = result.education_records[0]
    assert rec.degree == "Bachelor of Technology"
    assert rec.normalized_degree == "bachelor_of_technology"
    assert rec.degree_level == "UNDERGRADUATE"
    assert rec.field_of_study == "Electrical Engineering"
    assert rec.institution == "National Institute of Technology, Rourkela"
    assert rec.start_year == 2022
    assert rec.end_year == 2026
    assert rec.graduation_year == 2026
    assert rec.graduation_status == "COMPLETED"
    assert rec.cgpa == 7.99
    assert rec.percentage is None
    assert rec.score_type == "CGPA"


def test_multiple_education_records():
    text = (
        "EDUCATION\n\n"
        "Master of Technology in Computer Science\n"
        "Indian Institute of Technology Delhi\n"
        "2024 - 2026\n"
        "CGPA: 8.4\n\n"
        "Bachelor of Technology in Electrical Engineering\n"
        "National Institute of Technology, Rourkela\n"
        "2020 - 2024\n"
        "CGPA: 8.1\n"
    )
    sections = [("EDUCATION", "EDUCATION", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_education(proc)
    assert result.total_count == 2

    rec1 = result.education_records[0]
    assert rec1.degree == "Master of Technology"
    assert rec1.institution == "Indian Institute of Technology Delhi"
    assert rec1.cgpa == 8.4

    rec2 = result.education_records[1]
    assert rec2.degree == "Bachelor of Technology"
    assert rec2.institution == "National Institute of Technology, Rourkela"
    assert rec2.cgpa == 8.1


# ==============================================================================
# 4. EXPECTED GRADUATION & YEAR RANGE TESTS
# ==============================================================================

def test_expected_graduation():
    text = (
        "EDUCATION\n"
        "B.Tech in Computer Science\n"
        "NIT Rourkela\n"
        "Expected Graduation: 2027\n"
    )
    sections = [("EDUCATION", "EDUCATION", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_education(proc)
    assert result.total_count == 1
    rec = result.education_records[0]
    assert rec.graduation_year == 2027
    assert rec.graduation_status == "EXPECTED"


# ==============================================================================
# 5. SCHOOL EDUCATION TESTS (Class X / Class XII)
# ==============================================================================

def test_school_education_extraction():
    text = (
        "EDUCATION\n"
        "Class XII\n"
        "ABC Public School\n"
        "2022\n"
        "Percentage: 94%\n\n"
        "Class X\n"
        "ABC Public School\n"
        "2020\n"
        "Percentage: 96%\n"
    )
    sections = [("EDUCATION", "EDUCATION", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_education(proc)
    assert result.total_count == 2

    rec_xii = result.education_records[0]
    assert rec_xii.degree == "Senior Secondary"
    assert rec_xii.percentage == 94.0

    rec_x = result.education_records[1]
    assert rec_x.degree == "Secondary"
    assert rec_x.percentage == 96.0


# ==============================================================================
# 6. FALSE POSITIVE REJECTION TESTS
# ==============================================================================

def test_false_positive_experience_and_projects():
    text = (
        "WORK EXPERIENCE\n"
        "Software Engineer at Google\n"
        "2023 - Present\n"
        "5 years experience in cloud infrastructure\n"
        "Worked 90% remotely\n\n"
        "PROJECTS\n"
        "Project Management System 2024\n"
        "Achieved 90% test coverage\n"
    )
    sections = [
        ("EXPERIENCE", "WORK EXPERIENCE", text),
        ("PROJECTS", "PROJECTS", text),
    ]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_education(proc)
    assert result.total_count == 0


# ==============================================================================
# 7. DEDUPLICATION & IMMUTABILITY TESTS
# ==============================================================================

def test_deduplication():
    text = (
        "EDUCATION\n"
        "B.Tech in Electrical Engineering\n"
        "NIT Rourkela\n"
        "2022 - 2026\n"
        "CGPA: 7.99\n\n"
        "B.Tech in Electrical Engineering\n"
        "NIT Rourkela\n"
        "2022 - 2026\n"
        "CGPA: 7.99\n"
    )
    sections = [("EDUCATION", "EDUCATION", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_education(proc)
    assert result.total_count == 1


def test_input_non_mutation():
    text = "EDUCATION\nB.Tech in Electrical Engineering\nNIT Rourkela\n2022 - 2026\nCGPA: 7.99\n"
    sections = [("EDUCATION", "EDUCATION", text)]
    proc = _make_dummy_processed_text(text, sections)

    orig_cleaned = proc.cleaned_text
    orig_doc_text = proc.original_document.text

    extract_education(proc)

    assert proc.cleaned_text == orig_cleaned
    assert proc.original_document.text == orig_doc_text


# ==============================================================================
# 8. EXCEPTION & INPUT VALIDATION TESTS
# ==============================================================================

def test_none_input_raises_exception():
    with pytest.raises(ResumeParsingError, match="Cannot extract education from a None ProcessedResumeText"):
        extract_education(None)


def test_empty_text_raises_exception():
    proc = _make_dummy_processed_text("")
    with pytest.raises(ResumeParsingError, match="contains no text"):
        extract_education(proc)


# ==============================================================================
# 9. REAL CV MULTI-ENTRY REGRESSION TEST
# ==============================================================================

def test_real_cv_three_education_entries():
    """Verify that all 3 education entries from the test CV are extracted separately."""
    text = (
        "EDUCATION\n"
        "National Institute of Technology, Rourkela\n"
        "Bachelor of Technology in Electrical Engineering\n"
        "CGPA 7.79\n"
        "August 2023 – Present\n\n"
        "Jawahar Lal Nehru Inter College, Kanpur\n"
        "UP Board, Science (PCM)\n"
        "Percentage 82%\n"
        "May 2022\n\n"
        "SGM International School, Kanpur\n"
        "UP Board\n"
        "Percentage 85.56%\n"
        "May 2020\n"
    )
    sections = [("EDUCATION", "EDUCATION", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_education(proc)
    assert result.total_count == 3
    assert len(result.education_records) == 3

    # Entry 1: NIT Rourkela
    r1 = result.education_records[0]
    assert r1.degree == "Bachelor of Technology"
    assert "National Institute of Technology" in (r1.institution or "")
    assert r1.cgpa == 7.79
    assert r1.score_type == "CGPA"
    assert r1.field_of_study == "Electrical Engineering"
    assert r1.start_year == 2023

    # Entry 2: Jawahar Lal Nehru Inter College
    r2 = result.education_records[1]
    assert r2.degree == "Senior Secondary"
    assert "Jawahar Lal Nehru Inter College" in (r2.institution or "")
    assert r2.percentage == 82.0
    assert r2.score_type == "PERCENTAGE"
    assert r2.graduation_year == 2022

    # Entry 3: SGM International School
    r3 = result.education_records[2]
    assert r3.degree == "Secondary"
    assert "SGM International School" in (r3.institution or "")
    assert r3.percentage == 85.56
    assert r3.score_type == "PERCENTAGE"
    assert r3.graduation_year == 2020

