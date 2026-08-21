"""Section detection module for Day 23.

Implements rule-based, multi-signal section header detection and text segmentation
using a centralized canonical taxonomy and alias dictionary without external ML dependencies.

Taxonomy:
    EXPERIENCE, SKILLS, EDUCATION, PROJECTS, SUMMARY, OBJECTIVE, PROFILE,
    CERTIFICATIONS, ACHIEVEMENTS, AWARDS, PUBLICATIONS, LANGUAGES, INTERESTS,
    REFERENCES, CONTACT, UNKNOWN
"""

import re
import logging
from typing import List, Dict, Tuple, Optional

from .models import ProcessedSection, ExtractedDocument

logger = logging.getLogger("talentai.resume_processing.section_detector")

# Centralized section alias dictionary mapping lowercase phrases to canonical names
SECTION_ALIASES: Dict[str, List[str]] = {
    "EXPERIENCE": [
        "work experience",
        "professional experience",
        "employment history",
        "experience",
        "work history",
        "career history",
        "employment",
        "positions held",
        "relevant experience",
        "industry experience",
        "job history",
        "professional background",
    ],
    "SKILLS": [
        "technical skills",
        "skills",
        "core competencies",
        "technologies",
        "tech stack",
        "skills & tools",
        "skills and tools",
        "areas of expertise",
        "programming languages",
        "technical proficiencies",
        "key skills",
        "technical background",
        "technical expertise",
        "skills summary",
        "tools & technologies",
    ],
    "EDUCATION": [
        "education",
        "academic background",
        "educational qualifications",
        "academic qualifications",
        "education & credentials",
        "educational background",
        "academic history",
        "qualifications",
        "education and training",
    ],
    "PROJECTS": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
        "project experience",
        "technical projects",
        "selected projects",
        "featured projects",
        "major projects",
    ],
    "SUMMARY": [
        "summary",
        "professional summary",
        "career summary",
        "executive summary",
        "about me",
        "profile summary",
        "summary of qualifications",
        "overview",
    ],
    "PROFILE": [
        "profile",
        "personal profile",
        "biography",
    ],
    "OBJECTIVE": [
        "objective",
        "career objective",
        "professional objective",
    ],
    "CERTIFICATIONS": [
        "certifications",
        "licenses & certifications",
        "licenses and certifications",
        "certificates",
        "professional certifications",
        "courses & certifications",
        "certifications & licenses",
    ],
    "ACHIEVEMENTS": [
        "achievements",
        "honors & awards",
        "key achievements",
        "accomplishments",
        "awards & honors",
        "major achievements",
    ],
    "AWARDS": [
        "awards",
        "honors",
        "recognitions",
        "awards and honors",
    ],
    "PUBLICATIONS": [
        "publications",
        "research papers",
        "patents & publications",
        "patents",
    ],
    "LANGUAGES": [
        "languages",
        "language proficiency",
        "languages spoken",
        "foreign languages",
    ],
    "INTERESTS": [
        "interests",
        "hobbies",
        "activities & interests",
        "hobbies & interests",
    ],
    "REFERENCES": [
        "references",
        "referees",
        "professional references",
    ],
    "CONTACT": [
        "contact",
        "contact information",
        "personal info",
        "contact details",
        "personal details",
    ],
}

# Reverse lookup dictionary: lowercase alias -> canonical name
ALIAS_TO_CANONICAL: Dict[str, str] = {}
for canonical, aliases in SECTION_ALIASES.items():
    for alias in aliases:
        ALIAS_TO_CANONICAL[alias.lower()] = canonical

# List of single programming languages / tools to NEVER misclassify as section headers on their own
SINGLE_TECH_KEYWORDS = {
    "python", "java", "c++", "c#", ".net", "javascript", "typescript", "react", "node.js",
    "html", "css", "sql", "postgresql", "mongodb", "docker", "kubernetes", "aws", "git",
    "linux", "bash", "django", "flask", "fastapi", "vue", "angular", "c", "go", "rust",
}


def detect_sections(
    text: str,
    doc: Optional[ExtractedDocument] = None,
) -> List[ProcessedSection]:
    """Detect resume section headings and segment text into structured ProcessedSection objects.

    Args:
        text: Denoised and cleaned resume text string.
        doc: Optional ExtractedDocument to inspect paragraph styles or page breaks.

    Returns:
        List of ProcessedSection objects in original document sequence.
    """
    if not text:
        return [
            ProcessedSection(
                name="UNKNOWN",
                title="Unassigned Content",
                content="",
                confidence=1.0,
                start_line=1,
                end_line=1,
            )
        ]

    lines = text.split("\n")
    total_lines = len(lines)

    # Step 1: Scan lines and identify heading candidates
    headings: List[Tuple[int, str, str, float]] = []  # (line_idx_0, raw_line, canonical_name, confidence)

    # Extract DOCX heading style line numbers if available
    docx_heading_lines = set()
    if doc and doc.paragraphs:
        for p in doc.paragraphs:
            if p.is_heading and p.text:
                p_text_clean = p.text.strip().lower()
                for idx, line in enumerate(lines):
                    if line.strip().lower() == p_text_clean:
                        docx_heading_lines.add(idx)

    for idx, line in enumerate(lines):
        line_str = line.strip()
        if not line_str:
            continue

        canonical_name, confidence = _evaluate_heading_candidate(
            line=line_str,
            is_docx_heading=(idx in docx_heading_lines),
        )

        if canonical_name is not None and confidence >= 0.60:
            headings.append((idx, line_str, canonical_name, round(confidence, 2)))

    # Step 2: Build section objects by dividing lines between headings
    sections: List[ProcessedSection] = []

    if not headings:
        # No section headings detected at all -> entire text becomes UNKNOWN section
        sections.append(
            ProcessedSection(
                name="UNKNOWN",
                title="Unassigned Content",
                content=text,
                confidence=1.0,
                start_line=1,
                end_line=total_lines,
                page_number=1,
            )
        )
        return sections

    # Check if there is initial content before the first heading
    first_heading_idx = headings[0][0]
    if first_heading_idx > 0:
        initial_lines = lines[:first_heading_idx]
        initial_text = "\n".join(initial_lines).strip()
        if initial_text:
            sections.append(
                ProcessedSection(
                    name="UNKNOWN",
                    title="Header Content",
                    content=initial_text,
                    confidence=0.50,
                    start_line=1,
                    end_line=first_heading_idx,
                    page_number=1,
                )
            )

    # Process each detected section heading
    for h_i, (line_idx, raw_line, canonical_name, conf) in enumerate(headings):
        # Start line for content is line after heading
        content_start_idx = line_idx + 1

        # End line is up to line before next heading (or end of document)
        if h_i + 1 < len(headings):
            content_end_idx = headings[h_i + 1][0]
        else:
            content_end_idx = total_lines

        section_lines = lines[content_start_idx:content_end_idx]
        section_content = "\n".join(section_lines).strip()

        # Clean title (remove trailing colon if present)
        clean_title = raw_line.rstrip(":").strip()

        sections.append(
            ProcessedSection(
                name=canonical_name,
                title=clean_title,
                content=section_content,
                confidence=conf,
                start_line=line_idx + 1,  # 1-indexed
                end_line=content_end_idx,
                page_number=_estimate_page_number(line_idx, total_lines, doc),
            )
        )

    logger.info("Section detection completed: detected %d sections", len(sections))
    return sections


def _evaluate_heading_candidate(line: str, is_docx_heading: bool = False) -> Tuple[Optional[str], float]:
    """Evaluate a single line string to determine if it is a section heading.

    Args:
        line: Stripped line text.
        is_docx_heading: Whether the line comes from a DOCX paragraph marked with a Heading style.

    Returns:
        Tuple of (canonical_name_or_None, confidence_score).
    """
    # 1. Normalize line string for matching (strip trailing colon)
    line_clean = line.rstrip(":").strip().lower()

    # Reject empty lines or lines that are too long (>6 words or >50 chars)
    words = line_clean.split()
    if not words or len(words) > 6 or len(line_clean) > 50:
        return None, 0.0

    # Reject single tech keywords (e.g. "PYTHON", "JAVA") to prevent false positives
    if len(words) == 1 and line_clean in SINGLE_TECH_KEYWORDS:
        return None, 0.0

    # Reject lines containing email or URL patterns
    if "@" in line_clean or "http" in line_clean or "www." in line_clean:
        return None, 0.0

    # 2. Alias dictionary lookup
    matched_canonical = ALIAS_TO_CANONICAL.get(line_clean)

    base_score = 0.0

    if matched_canonical:
        # Exact alias match!
        base_score += 0.70
    else:
        # Check partial/fuzzy match (e.g., "1. WORK EXPERIENCE" or "TECHNICAL SKILLS & TOOLS")
        cleaned_no_digits = re.sub(r'^\d+[\.\)]\s*', '', line_clean)
        if cleaned_no_digits in ALIAS_TO_CANONICAL:
            matched_canonical = ALIAS_TO_CANONICAL[cleaned_no_digits]
            base_score += 0.65

    if not matched_canonical:
        return None, 0.0

    # 3. Apply formatting signals to boost confidence
    # All uppercase (e.g., "WORK EXPERIENCE")
    if line.isupper():
        base_score += 0.15
    # Title Case (e.g., "Work Experience")
    elif line.istitle():
        base_score += 0.10

    # Ended with colon (e.g., "SKILLS:")
    if line.endswith(":"):
        base_score += 0.10

    # DOCX heading style match
    if is_docx_heading:
        base_score += 0.15

    final_score = min(1.0, base_score)
    return matched_canonical, final_score


def _estimate_page_number(line_idx: int, total_lines: int, doc: Optional[ExtractedDocument]) -> Optional[int]:
    """Estimate 1-indexed page number for a given line index."""
    if not doc or not doc.pages or doc.page_count <= 1:
        return 1

    lines_per_page = max(1, total_lines // doc.page_count)
    estimated_page = min(doc.page_count, (line_idx // lines_per_page) + 1)
    return estimated_page
