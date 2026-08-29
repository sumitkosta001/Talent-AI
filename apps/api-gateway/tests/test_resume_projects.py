"""Unit and Integration Tests for Phase 4 Day 27 Project Extraction.

Verifies:
1. Basic single project extraction (name, technologies, description).
2. Multiple project extraction without merging or dropping.
3. Technology extraction and normalization (reusing Day 24 SKILL_DICTIONARY & ALIAS_MAP).
4. Technology detection from project descriptions vs global SKILLS section.
5. Original verbatim project description preservation (no LLM rewriting).
6. Deterministic project classification (FULL_STACK, MACHINE_LEARNING, MOBILE_APPLICATION, DEVOPS, EMBEDDED, ARTIFICIAL_INTELLIGENCE).
7. Layout formats (Parentheses format, Separator format, Colon format, Multiline headers).
8. Project dates parsing (start_year, end_year, Present date handling).
9. Academic projects support.
10. False positive rejection (Education, Experience, Skills section, Certifications, Bullets, Section labels, Subtitles).
11. Evidence-based confidence scoring.
12. Record deduplication.
13. Input non-mutation.
14. Exception handling on None or empty input.
15. Multiple project sections handling.
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
# 4. PARENTHESIS, SEPARATOR & COLON LAYOUT TESTS
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


def test_colon_layout_header():
    text = (
        "PROJECTS\n\n"
        "SmartLock System: IoT Door Access Control\n"
        "Arduino, C++, Raspberry Pi\n"
        "Built a smart door lock system using microcontrollers.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 1
    assert result.projects[0].name == "SmartLock System"


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


def test_present_date_handling():
    text = (
        "PROJECTS\n\n"
        "Distributed Task Queue\n"
        "2023 - Present\n"
        "Go, Redis\n"
        "High-performance worker queue system.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 1
    rec = result.projects[0]
    assert rec.start_year == 2023
    assert rec.end_year is None


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


def test_missing_and_empty_projects_section():
    # No PROJECTS section
    proc = _make_dummy_processed_text("John Doe\nDeveloper")
    result = extract_projects(proc)
    assert result.total_count == 0

    # Empty PROJECTS section content
    sections = [("PROJECTS", "PROJECTS", "   \n\n  ")]
    proc_empty = _make_dummy_processed_text("PROJECTS", sections)
    result_empty = extract_projects(proc_empty)
    assert result_empty.total_count == 0


def test_multiple_projects_sections():
    sec1 = ("PROJECTS", "TECHNICAL PROJECTS", "Project Alpha\nPython, Django\nWeb app.")
    sec2 = ("PROJECTS", "PERSONAL PROJECTS", "Project Beta\nReact, Firebase\nMobile app.")
    proc = _make_dummy_processed_text("Content", [sec1, sec2])

    result = extract_projects(proc)
    assert result.total_count == 2
    names = [p.name for p in result.projects]
    assert "Project Alpha" in names
    assert "Project Beta" in names


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


# ==============================================================================
# 10. REAL CV REGRESSION TESTS
# ==============================================================================

def test_real_cv_two_projects_extraction():
    """Verify that exactly 2 major projects are extracted from the test CV without false positive bullets."""
    text = (
        "PROJECTS\n"
        "Learnify – AI-Powered Learning Platform\n"
        "TypeScript, Next.js, Tailwind CSS, PostgreSQL, Prisma, Gemini API\n"
        "- Architected a personalized AI learning platform generating dynamic roadmaps and quizzes.\n"
        "- Integrated Google Gemini API for real-time concept explanation and feedback.\n"
        "- Designed responsive UI with Next.js App Router and Tailwind CSS.\n\n"
        "QuickHotelPost – AI Content Generator for Hotels\n"
        "React.js, Node.js, Express.js, MongoDB, OpenAI API\n"
        "- Built an automated marketing content generator for hospitality businesses.\n"
        "- Developed multi-channel social media scheduler reducing manual effort by 60%.\n"
        "- Integrated OpenAI API for custom brand voice copy generation.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 2
    assert len(result.projects) == 2

    # Project 1: Learnify
    p1 = result.projects[0]
    assert p1.name is not None
    assert "Learnify" in p1.name
    assert any("Next.js" in t for t in p1.technologies)
    assert any("TypeScript" in t for t in p1.technologies)
    assert any("Gemini" in t for t in p1.technologies)

    # Project 2: QuickHotelPost
    p2 = result.projects[1]
    assert p2.name is not None
    assert "QuickHotelPost" in p2.name
    assert any("React" in t for t in p2.technologies)
    assert any("Node" in t for t in p2.technologies)
    assert any("MongoDB" in t for t in p2.technologies)
    assert any("OpenAI" in t for t in p2.technologies)


def test_user_actual_cv_two_projects_extraction():
    """Verify that exactly 2 major projects (Learnify and QuickHotelPost) are extracted from the user's actual CV without any false positives."""
    text = (
        "Projects\n\n"
        "Learnify – AI-Powered Learning Platform\n\n"
        "Technologies:\n"
        "- Next.js\n"
        "- React.js\n"
        "- Tailwind CSS\n"
        "- TypeScript\n"
        "- PostgreSQL\n"
        "- Gemini API\n"
        "- Clerk\n\n"
        "Description:\n"
        "- Built an AI-powered learning platform using Next.js, TypeScript, PostgreSQL, and Gemini API for personalized courses and quizzes.\n"
        "- Integrated Gemini API and Clerk authentication, reducing content generation time from 20s to 8s.\n"
        "- Developed a responsive UI with Next.js and Tailwind CSS using reusable and scalable components.\n\n"
        "Date:\n"
        "- August 2025\n\n"
        "QuickHotelPost – AI Content Generator for Hotels\n\n"
        "Technologies:\n"
        "- Next.js\n"
        "- React.js\n"
        "- Tailwind CSS\n"
        "- JavaScript\n"
        "- Gemini API\n"
        "- Hugging Face\n\n"
        "Description:\n"
        "- Built an AI-powered platform using Next.js to generate personalized hotel social media posts with AI images.\n"
        "- Integrated Gemini API and Hugging Face for multilingual content and AI image generation.\n"
        "- Optimized APIs for sub-8s generation and built a responsive UI using Next.js and Tailwind CSS.\n\n"
        "Date:\n"
        "- March 2025\n"
    )
    sections = [("PROJECTS", "Projects", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)

    # Must extract EXACTLY 2 projects — zero false positive records!
    assert result.total_count == 2
    assert len(result.projects) == 2

    p1 = result.projects[0]
    assert p1.name is not None
    assert "Learnify" in p1.name
    assert "Next.js" in p1.technologies
    assert "React.js" in p1.technologies
    assert "Tailwind CSS" in p1.technologies
    assert "TypeScript" in p1.technologies
    assert "PostgreSQL" in p1.technologies
    assert any("Gemini" in t for t in p1.technologies)
    assert p1.start_year == 2025

    p2 = result.projects[1]
    assert p2.name is not None
    assert "QuickHotelPost" in p2.name
    assert "Next.js" in p2.technologies
    assert "React.js" in p2.technologies
    assert "Tailwind CSS" in p2.technologies
    assert "JavaScript" in p2.technologies
    assert any("Gemini" in t for t in p2.technologies)
    assert p2.start_year == 2025

    # False positive string assertions — ensure NONE of these became project names!
    extracted_names = [p.name for p in result.projects]
    rejected_strings = [
        "Architected", "Integrated", "Built", "Developed", "Optimized",
        "Responsive UI", "Next.js", "React.js", "PostgreSQL", "Gemini API",
        "GitHub", "August 2025", "March 2025", "Description", "Date", "Technologies"
    ]
    for r_str in rejected_strings:
        assert r_str not in extracted_names


# ==============================================================================
# 11. FALSE POSITIVE REJECTION TESTS (BULLETS, ACTION VERBS & SUBTITLES)
# ==============================================================================

def test_action_verbs_and_descriptions_rejection():
    """Verify that bullet points, action verb lines, and full sentences do NOT create false project records."""
    text = (
        "PROJECTS\n\n"
        "Talent AI System\n"
        "FastAPI, React.js\n"
        "Architected an automated candidate matching system.\n"
        "Integrated spaCy for entity recognition and resume parsing.\n"
        "Designed responsive UI components using React.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 1
    assert result.projects[0].name == "Talent AI System"


def test_github_and_url_lines_rejection():
    """Verify that GitHub URLs and Demo link lines do NOT become project names."""
    text = (
        "PROJECTS\n\n"
        "Learnify\n"
        "GitHub: https://github.com/user/learnify\n"
        "Live Demo: https://learnify.app\n"
        "Next.js, PostgreSQL\n"
        "AI-powered learning platform.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 1
    assert result.projects[0].name == "Learnify"
    extracted_names = [p.name for p in result.projects]
    assert "GitHub" not in extracted_names
    assert "Live Demo" not in extracted_names


def test_same_technologies_different_project_names_remain_separate():
    """Verify that two projects with the exact same technology stack are NOT merged."""
    text = (
        "PROJECTS\n\n"
        "Learnify\n"
        "Next.js, React.js, Tailwind CSS, Gemini API\n"
        "Built an AI-powered learning platform.\n\n"
        "QuickHotelPost\n"
        "Next.js, React.js, Tailwind CSS, Gemini API\n"
        "Built an AI content generator for hotels.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 2
    names = [p.name for p in result.projects]
    assert "Learnify" in names
    assert "QuickHotelPost" in names


def test_tech_inside_description_extraction():
    """Verify technologies mentioned only inside description body text are extracted."""
    text = (
        "PROJECTS\n\n"
        "Data Pipeline\n"
        "Built automated streaming pipeline using FastAPI and PostgreSQL for real-time analytics.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)
    assert result.total_count == 1
    techs = result.projects[0].technologies
    assert any("FastAPI" in t for t in techs) or any("PostgreSQL" in t for t in techs)



def test_confidence_scores_vary_by_evidence_quality():
    """Verify confidence score reflects the number of evidence signals."""
    # High evidence (Name, Techs, Subtitle, Description, Date)
    text_high = (
        "PROJECTS\n\n"
        "Learnify – AI Learning Platform\n"
        "2024 - 2025\n"
        "FastAPI, React\n"
        "Built an AI-powered learning platform using FastAPI and React for personalized quizzes.\n"
    )
    proc_high = _make_dummy_processed_text(text_high, [("PROJECTS", "PROJECTS", text_high)])
    res_high = extract_projects(proc_high)
    assert res_high.projects[0].confidence >= 0.95

    # Low evidence (Name only, minimal description)
    text_low = (
        "PROJECTS\n\n"
        "Simple App\n"
        "Small utility.\n"
    )
    proc_low = _make_dummy_processed_text(text_low, [("PROJECTS", "PROJECTS", text_low)])
    res_low = extract_projects(proc_low)
    assert res_low.projects[0].confidence < 0.95


def test_achievements_certifications_and_certificate_non_project_rejection():
    """Verify that Achievements/Certifications and Certificate headings are NEVER extracted as projects."""
    text = (
        "PROJECTS\n\n"
        "Learnify – AI-Powered Learning Platform\n"
        "August 2025\n"
        "Next.js, React.js, PostgreSQL\n"
        "- Built an AI-powered learning platform.\n\n"
        "QuickHotelPost – AI Content Generator for Hotels\n"
        "March 2025\n"
        "Next.js, React.js, MongoDB\n"
        "- Built an AI-powered hotel post generator.\n\n"
        "Achievements/Certifications\n\n"
        "- Flipkart GRiD 7.0 National Semi-Finalist\n"
        "August 2025\n"
        "Recognized as a National Semi-Finalist among 50,000+ candidates.\n\n"
        "Certificate\n\n"
        "- AWS Cloud Practitioner Essentials\n"
        "Completed training for AWS Cloud Services.\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)

    # Must extract EXACTLY 2 projects!
    assert result.total_count == 2
    names = [p.name for p in result.projects]
    assert names == ["Learnify", "QuickHotelPost"]
    assert "Achievements/Certifications" not in names
    assert "Certificate" not in names
    assert "Flipkart GRiD 7.0 National Semi-Finalist" not in names
    assert "AWS Cloud Practitioner Essentials" not in names


def test_section_detector_recognizes_achievements_certifications():
    """Verify that section_detector.py detects Achievements/Certifications as a section heading."""
    from app.services.resume_processing.section_detector import detect_sections

    text = "PROJECTS\nLearnify\n\nAchievements/Certifications\n- Flipkart GRiD"
    sections = detect_sections(text)

    sec_names = [s.name for s in sections]
    assert "PROJECTS" in sec_names
    assert "CERTIFICATIONS" in sec_names or "ACHIEVEMENTS" in sec_names


def test_inline_non_project_section_boundary_termination():
    """Verify that non-project section headings inside PROJECTS content terminate project extraction immediately."""
    text = (
        "PROJECTS\n\n"
        "Learnify\n"
        "FastAPI, React\n"
        "AI recruitment platform.\n\n"
        "Awards & Honors\n"
        "- Hackathon Winner 2025\n\n"
        "Extracurricular Activities\n"
        "- Club President\n"
    )
    sections = [("PROJECTS", "PROJECTS", text)]
    proc = _make_dummy_processed_text(text, sections)

    result = extract_projects(proc)

    assert result.total_count == 1
    assert result.projects[0].name == "Learnify"
    names = [p.name for p in result.projects]
    assert "Awards & Honors" not in names
    assert "Extracurricular Activities" not in names

