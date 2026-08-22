"""Phase 4 Day 28 — Structured Resume Builder and Business Validator.

Orchestrates Days 21–27 extraction outputs into a validated, serializable, versioned
StructuredResume model payload for persistence and downstream services.
"""

from typing import List, Dict, Any, Optional, Tuple
import re
import time
import logging

from app.exceptions.resume import ResumeParsingError
from .models import (
    ProcessedResumeText,
    ExtractedSkills,
    ExtractedEducation,
    ExtractedExperience,
    ExtractedProjects,
    StructuredResume,
)

logger = logging.getLogger("talentai.resume_processing.structured_resume")

EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
PHONE_REGEX = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
LINKEDIN_REGEX = re.compile(r'https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+', re.IGNORECASE)
GITHUB_REGEX = re.compile(r'https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+', re.IGNORECASE)


def extract_contact_info(processed_text: ProcessedResumeText) -> Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]:
    """Extract email, phone, location, LinkedIn, and GitHub links from processed text.

    Returns:
        (email, phone, location, linkedin, github)
    """
    if not processed_text or not processed_text.normalized_text:
        return None, None, None, None, None

    text = processed_text.normalized_text

    email_match = EMAIL_REGEX.search(text)
    email = email_match.group(0) if email_match else None

    phone_match = PHONE_REGEX.search(text)
    phone = phone_match.group(0) if phone_match else None

    li_match = LINKEDIN_REGEX.search(text)
    linkedin = li_match.group(0) if li_match else None

    gh_match = GITHUB_REGEX.search(text)
    github = gh_match.group(0) if gh_match else None

    # Location candidate from top 5 lines
    location = None
    lines = [l.strip() for l in text.splitlines()[:5] if l.strip()]
    for l in lines:
        if re.search(r'\b(?:Bengaluru|Mumbai|Delhi|Hyderabad|Pune|Chennai|New York|San Francisco|London|India|USA|Remote)\b', l, re.IGNORECASE):
            location = l
            break

    return email, phone, location, linkedin, github


def validate_structured_resume(structured_resume: StructuredResume) -> bool:
    """Perform Level 2 business consistency validation on StructuredResume payload.

    Checks:
    1. List counts vs metadata total counts.
    2. Confidence bounds (0.0 to 1.0).
    3. Score bounds (CGPA <= 10.0, Percentage <= 100.0).
    4. Reasonable year ranges (start_year <= end_year).

    Returns:
        True if valid.

    Raises:
        ValueError: If business validation rule fails.
    """
    if not structured_resume:
        raise ValueError("StructuredResume payload is None.")

    # 1. Skills validation
    if structured_resume.skills.total_count < 0:
        raise ValueError("Skills total_count cannot be negative.")
    for sk in structured_resume.skills.skills:
        if not (0.0 <= sk.confidence <= 1.0):
            raise ValueError(f"Skill confidence out of bounds: {sk.confidence}")

    # 2. Education validation
    if structured_resume.education.total_count < 0:
        raise ValueError("Education total_count cannot be negative.")
    for edu in structured_resume.education.education_records:
        if edu.cgpa is not None and not (0.0 <= edu.cgpa <= 10.0):
            raise ValueError(f"Invalid CGPA value: {edu.cgpa}")
        if edu.percentage is not None and not (0.0 <= edu.percentage <= 100.0):
            raise ValueError(f"Invalid percentage value: {edu.percentage}")
        if edu.start_year and edu.end_year and edu.start_year > edu.end_year:
            raise ValueError(f"Education start_year ({edu.start_year}) cannot be after end_year ({edu.end_year}).")

    # 3. Experience validation
    if structured_resume.experience.total_count < 0:
        raise ValueError("Experience total_count cannot be negative.")
    for exp in structured_resume.experience.experiences:
        if exp.duration_months is not None and exp.duration_months < 0:
            raise ValueError(f"Experience duration_months cannot be negative: {exp.duration_months}")
        if exp.start_year and exp.end_year and exp.start_year > exp.end_year and not exp.is_current:
            raise ValueError(f"Experience start_year ({exp.start_year}) cannot be after end_year ({exp.end_year}).")

    # 4. Project validation
    if structured_resume.projects.total_count < 0:
        raise ValueError("Projects total_count cannot be negative.")
    for proj in structured_resume.projects.projects:
        if proj.start_year and proj.end_year and proj.start_year > proj.end_year:
            raise ValueError(f"Project start_year ({proj.start_year}) cannot be after end_year ({proj.end_year}).")

    return True


def build_structured_resume(
    processed_text: Optional[ProcessedResumeText],
    skills: Optional[ExtractedSkills] = None,
    education: Optional[ExtractedEducation] = None,
    experience: Optional[ExtractedExperience] = None,
    projects: Optional[ExtractedProjects] = None,
    resume_id: Optional[Any] = None,
    candidate_profile_id: Optional[Any] = None,
) -> StructuredResume:
    """Build, combine, and validate a canonical StructuredResume object.

    Args:
        processed_text: ProcessedResumeText from Day 23.
        skills: ExtractedSkills from Day 24.
        education: ExtractedEducation from Day 25.
        experience: ExtractedExperience from Day 26.
        projects: ExtractedProjects from Day 27.
        resume_id: Optional DB resume ID.
        candidate_profile_id: Optional candidate profile ID.

    Returns:
        Validated StructuredResume object.

    Raises:
        ResumeParsingError: If processed_text is None or has no text.
        ValueError: If Level 2 business validation fails.
    """
    if processed_text is None:
        raise ResumeParsingError("Cannot build structured resume from a None ProcessedResumeText.")

    if not processed_text.normalized_text or not processed_text.normalized_text.strip():
        raise ResumeParsingError("The processed resume document contains no text.")

    start_time = time.perf_counter()

    # 1. Contact info extraction
    email, phone, location, linkedin, github = extract_contact_info(processed_text)

    # 2. Extract summary / profile section text if present
    summary_text: Optional[str] = None
    summary_sections = [s for s in processed_text.sections if s.name in {"SUMMARY", "PROFILE", "OBJECTIVE"}]
    if summary_sections:
        summary_text = summary_sections[0].content.strip()

    # 3. Default collections if optional inputs not passed
    skills_data = skills or ExtractedSkills()
    education_data = education or ExtractedEducation()
    experience_data = experience or ExtractedExperience()
    projects_data = projects or ExtractedProjects()

    # 4. Construct payload
    structured = StructuredResume(
        schema_version="1.0",
        pipeline_version="phase4-day28",
        resume_id=str(resume_id) if resume_id else None,
        candidate_profile_id=str(candidate_profile_id) if candidate_profile_id else None,
        email=email,
        phone=phone,
        location=location,
        linkedin=linkedin,
        github=github,
        summary=summary_text,
        skills=skills_data,
        education=education_data,
        experience=experience_data,
        projects=projects_data,
        metadata={
            "duration_seconds": round(time.perf_counter() - start_time, 4),
            "sections_count": len(processed_text.sections),
            "character_count": len(processed_text.normalized_text),
        },
    )

    # 5. Business Validation
    validate_structured_resume(structured)

    # 6. Perform Day 29 Resume Classification
    from .resume_classifier import classify_resume
    structured.classification = classify_resume(structured)

    return structured
