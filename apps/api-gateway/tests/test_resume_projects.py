"""Unit and Integration Tests for Phase 4 Day 27 Project Extraction.

Verifies:
1. Basic single project extraction (name, technologies, description).
2. Multiple project extraction without merging or dropping.
3. Technology extraction and normalization (reusing Day 24 SKILL_DICTIONARY & ALIAS_MAP).
4. Technology detection from project descriptions vs global SKILLS section.
5. Original verbatim project description preservation (no LLM rewriting).
6. Deterministic project classification (FULL_STACK, MACHINE_LEARNING, MOBILE_APPLICATION, DEVOPS, EMBEDDED, ARTIFICIAL_INTELLIGENCE).
7. Layout formats (Parentheses format, Separator format, Multiline headers).
8. Project dates parsing (start_year, end_year).
9. Academic projects support.
10. False positive rejection (Education, Experience, Skills section, Certifications).
11. Record deduplication.
12. Input non-mutation.
13. Exception handling on None or empty input.
"""

import pytest
from app.exceptions.resume import ResumeParsingError
from app.services.resume_processing import (
    ExtractedDocument,
    DocumentPage,
    ProcessedResumeText,
    ProcessedSection,
    ProjectRecord,
    ExtractedProjects,
    extract_projects,
    normalize_project_name,
    normalize_technologies,
    classify_project,
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
# 1. PROJECT NAME & TECH NORMALIZATION TESTS
# ==============================================================================

def test_project_name_normalization():
    name, norm_name = normalize_project_name("  Talent   AI  ")
    assert name == "Talent AI"
    assert norm_name == "talent ai"


def test_technology_normalization():
    raw_techs = ["ReactJS", "Node", "Postgres", "sklearn", "FastAPI"]
    can_techs, norm_techs = normalize_technologies(raw_techs)

    assert "React.js" in can_techs
    assert "Node.js" in can_techs
    assert "PostgreSQL" in can_techs
    assert "scikit-learn" in can_techs
    assert "FastAPI" in can_techs


# ==============================================================================
# 2. SINGLE PROJECT EXTRACTION TEST
# ==============================================================================

def test_single_project_extraction():
    text = (
        "PROJECTS\n\n"
        "Talent AI\n"
        "Technologies: FastAPI, React, PostgreSQL\n\n"
        "AI-powered recruitment platform that extracts resume information "
        "and matches candidates with jobs.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result: ExtractedProjects = extract_projects(proc)

    assert result.total_count == 1
    rec: ProjectRecord = result.projects[0]
    assert rec.name == "Talent AI"
    assert rec.normalized_name == "talent ai"
    assert "FastAPI" in rec.technologies
    assert "React.js" in rec.technologies
    assert "PostgreSQL" in rec.technologies
    assert "AI-powered recruitment platform" in rec.description
    assert rec.classification == "FULL_STACK"


# ==============================================================================
# 3. MULTIPLE PROJECTS EXTRACTION TEST
# ==============================================================================

def test_multiple_projects_extraction():
    text = (
        "PROJECTS\n\n"
        "Talent AI\n"
        "FastAPI, React, PostgreSQL\n"
        "AI-powered recruitment platform.\n\n"
        "QuickHotelPost\n"
        "Next.js, TypeScript, PostgreSQL\n"
        "AI-powered hotel social media post generator.\n\n"
        "ClinicalAI\n"
        "FastAPI, React, Python\n"
        "Hospital appointment system.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 3
    assert result.projects[0].name == "Talent AI"
    assert result.projects[1].name == "QuickHotelPost"
    assert result.projects[2].name == "ClinicalAI"


# ==============================================================================
# 4. PARENTHESIS & SEPARATOR LAYOUT TESTS
# ==============================================================================

def test_parentheses_and_separator_layouts():
    text = (
        "PROJECTS\n\n"
        "Resume Analyzer (Python, spaCy, FastAPI)\n"
        "AI-powered resume analysis tool.\n\n"
        "E-Commerce Portal | React | Node.js | MongoDB\n"
        "Full stack online shopping portal.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 2

    p1 = result.projects[0]
    assert p1.name == "Resume Analyzer"
    assert "Python" in p1.technologies
    assert "spaCy" in p1.technologies
    assert "FastAPI" in p1.technologies

    p2 = result.projects[1]
    assert p2.name == "E-Commerce Portal"
    assert "React.js" in p2.technologies
    assert "Node.js" in p2.technologies
    assert "MongoDB" in p2.technologies


# ==============================================================================
# 5. DETERMINISTIC CLASSIFICATION TESTS
# ==============================================================================

def test_project_classifications():
    cls_ml, _ = classify_project("House Predictor", "Predicts prices", ["Python", "TensorFlow", "scikit-learn"])
    assert cls_ml == "MACHINE_LEARNING"

    cls_mob, _ = classify_project("Fitness Tracker", "Mobile app", ["React Native", "Firebase"])
    assert cls_mob == "MOBILE_APPLICATION"

    cls_dev, _ = classify_project("CI Pipeline", "Infrastructure deployment", ["Docker", "Kubernetes", "AWS"])
    assert cls_dev == "DEVOPS"

    cls_emb, _ = classify_project("Smart Lock", "IoT door lock", ["Arduino", "C++", "Sensors"])
    assert cls_emb == "EMBEDDED"


# ==============================================================================
# 6. ACADEMIC & DATE PARSING TESTS
# ==============================================================================

def test_academic_project_and_dates():
    text = (
        "ACADEMIC PROJECTS\n\n"
        "Smart Attendance System\n"
        "2024 - 2025\n"
        "Python, OpenCV\n"
        "Face-recognition based attendance system at university.\n"
    )
    sections = [("PROJECTS", "ACADEMIC PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 1
    rec = result.projects[0]
    assert rec.name == "Smart Attendance System"
    assert rec.start_year == 2024
    assert rec.end_year == 2025
    assert rec.project_type == "ACADEMIC"
    assert rec.classification == "ARTIFICIAL_INTELLIGENCE"


# ==============================================================================
# 7. FALSE POSITIVE REJECTION TESTS
# ==============================================================================

def test_false_positive_rejection_skills_and_experience():
    text = (
        "SKILLS\n"
        "Python, React, Docker, PostgreSQL\n\n"
        "EXPERIENCE\n"
        "Software Engineer\n"
        "Google\n"
        "2022 - Present\n"
        "- Built internal platform using React.\n\n"
        "EDUCATION\n"
        "B.Tech in Computer Science\n"
        "NIT Rourkela\n"
    )
    sections = [
        ("SKILLS", "SKILLS", "Python, React, Docker, PostgreSQL"),
        ("EXPERIENCE", "EXPERIENCE", "Software Engineer\nGoogle\n2022 - Present\n- Built internal platform."),
        ("EDUCATION", "EDUCATION", "B.Tech in Computer Science\nNIT Rourkela"),
    ]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 0


# ==============================================================================
# 8. DEDUPLICATION & IMMUTABILITY TESTS
# ==============================================================================

def test_deduplication():
    text = (
        "PROJECTS\n\n"
        "Talent AI\n"
        "FastAPI, React\n"
        "AI recruitment platform.\n\n"
        "Talent AI\n"
        "FastAPI, React\n"
        "AI recruitment platform.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 1


def test_input_non_mutation():
    text = "PROJECTS\nTalent AI\nFastAPI, React\nAI recruitment platform."
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    orig_cleaned = proc.cleaned_text
    orig_doc_text = proc.original_document.text

    extract_projects(proc)

    assert proc.cleaned_text == orig_cleaned
    assert proc.original_document.text == orig_doc_text


# ==============================================================================
# 9. EXCEPTION & INPUT VALIDATION TESTS
# ==============================================================================

def test_none_input_raises_exception():
    with pytest.raises(ResumeParsingError, match="Cannot extract projects from a None ProcessedResumeText"):
        extract_projects(None)


def test_empty_text_raises_exception():
    proc = _make_dummy_processed_text("")
    with pytest.raises(ResumeParsingError, match="contains no text"):
        extract_projects(proc)
