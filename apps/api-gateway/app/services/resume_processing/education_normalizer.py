"""Education Normalizer and Deduplicator for Day 25.

Provides deterministic functions for normalizing extracted degree names, degree levels,
institutions, academic years, score types, and deduplicating education records.
"""

from typing import List, Tuple, Optional, Dict, Any, Set
import re
import logging

from .models import EducationRecord
from .degree_dictionary import (
    DEGREE_DICTIONARY,
    DEGREE_ALIAS_MAP,
    INSTITUTION_ALIASES,
)

logger = logging.getLogger("talentai.resume_processing.education_normalizer")


def normalize_degree(raw_degree: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Map raw degree text to canonical degree name, normalized degree ID, and degree level.

    Returns:
        (canonical_degree, normalized_degree, degree_level)
    """
    if not raw_degree or not raw_degree.strip():
        return None, None, None

    cleaned = raw_degree.strip()
    lowered = cleaned.lower()

    # Check exact alias dictionary match
    if lowered in DEGREE_ALIAS_MAP:
        canonical, level = DEGREE_ALIAS_MAP[lowered]
        return canonical, canonical.lower().replace(" ", "_"), level

    # Match via regex patterns in DEGREE_DICTIONARY
    for canonical_name, info in DEGREE_DICTIONARY.items():
        pattern: re.Pattern = info["pattern"]
        if pattern.search(cleaned):
            level = info["level"]
            return canonical_name, canonical_name.lower().replace(" ", "_"), level

    # Fallback: clean up title-cased degree string
    fallback_canonical = cleaned.title()
    return fallback_canonical, fallback_canonical.lower().replace(" ", "_"), "OTHER"


def normalize_institution(raw_institution: str) -> Tuple[Optional[str], Optional[str]]:
    """Clean and normalize raw institution string.

    Returns:
        (cleaned_institution, normalized_institution)
    """
    if not raw_institution or not raw_institution.strip():
        return None, None

    # Remove unwanted leading/trailing punctuation and extra whitespace
    cleaned = raw_institution.strip(" ,.-|:;\t\n")
    cleaned = re.sub(r'\s+', ' ', cleaned)

    if not cleaned:
        return None, None

    lowered = cleaned.lower()

    # Explicit alias resolution if present
    if lowered in INSTITUTION_ALIASES:
        canonical = INSTITUTION_ALIASES[lowered]
        return canonical, canonical.lower()

    return cleaned, lowered


def parse_year_and_status(text: str) -> Tuple[Optional[int], Optional[int], Optional[int], Optional[str]]:
    """Extract start_year, end_year, graduation_year, and graduation_status from text snippet.

    Returns:
        (start_year, end_year, graduation_year, graduation_status)
    """
    if not text:
        return None, None, None, None

    start_year: Optional[int] = None
    end_year: Optional[int] = None
    graduation_year: Optional[int] = None
    status: Optional[str] = None

    # Check for range: e.g. 2022 - 2026, 2022–2026, 2022 to 2026
    range_match = re.search(r'\b(19[7-9]\d|20[0-3]\d)\s*(?:-|–|—|to)\s*(19[7-9]\d|20[0-3]\d)\b', text, re.IGNORECASE)
    if range_match:
        start_year = int(range_match.group(1))
        end_year = int(range_match.group(2))
        graduation_year = end_year
        status = "COMPLETED"

    # Check expected graduation phrases
    expected_match = re.search(
        r'(?:expected|present|pursuing|class\s+of)\b.*?\b(20[2-3]\d)\b',
        text,
        re.IGNORECASE,
    )
    if expected_match:
        grad_yr = int(expected_match.group(1))
        if graduation_year is None:
            graduation_year = grad_yr
        if end_year is None:
            end_year = grad_yr
        status = "EXPECTED"

    # Check single completion year phrase if no range found yet
    if graduation_year is None:
        grad_match = re.search(
            r'(?:graduated|completed|passout|passing\s+year|year\s*:\s*|in\s+)?\b(19[7-9]\d|20[0-3]\d)\b',
            text,
            re.IGNORECASE,
        )
        if grad_match:
            # Verify context is not phone or CGPA
            candidate_yr = int(grad_match.group(1))
            if not re.search(r'cgpa|gpa|cpi|phone|tel|mobile', text, re.IGNORECASE):
                graduation_year = candidate_yr
                status = "COMPLETED"

    if status is None and graduation_year is not None:
        status = "COMPLETED"

    return start_year, end_year, graduation_year, status


def parse_score(text: str) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """Parse CGPA, GPA, CPI, or Percentage from text snippet.

    Returns:
        (cgpa, percentage, score_type)
    """
    if not text:
        return None, None, None

    # CGPA / GPA / CPI match (e.g. CGPA: 8.2, CGPA 7.99/10, GPA 3.8, CPI 8.1)
    cgpa_match = re.search(
        r'\b(?:CGPA|GPA|CPI)\s*(?:-|:|\s)\s*([0-9]\.[0-9]{1,2})(?:\s*/\s*10|\b)',
        text,
        re.IGNORECASE,
    )
    if cgpa_match:
        val = float(cgpa_match.group(1))
        if 0.0 <= val <= 10.0:
            return val, None, "CGPA"

    # Match raw score ratio like 8.2/10
    ratio_match = re.search(r'\b([0-9]\.[0-9]{1,2})\s*/\s*10\b', text)
    if ratio_match:
        val = float(ratio_match.group(1))
        if 0.0 <= val <= 10.0:
            return val, None, "CGPA"

    # Percentage match (e.g. Percentage: 85%, 85.5%, 94%)
    pct_match = re.search(
        r'\b(?:Percentage|Score|Marks)?\s*(?:-|:|\s)?\s*([1-9][0-9](?:\.[0-9]{1,2})?|\d{1,2}(?:\.[0-9]{1,2})?)\s*%(?!\w)',
        text,
        re.IGNORECASE,
    )
    if pct_match:
        # Avoid matching remote % or non-academic percentages unless education keyword is near
        if not re.search(r'remote|coverage|discount|growth', text, re.IGNORECASE):
            val = float(pct_match.group(1))
            if 0.0 <= val <= 100.0:
                return None, val, "PERCENTAGE"

    return None, None, None


def deduplicate_education_records(records: List[EducationRecord]) -> List[EducationRecord]:
    """Deduplicate records based on canonical degree, institution, and year range.

    Preserves original order and evidence.
    """
    if not records:
        return []

    seen: Set[Tuple[str, str, Optional[int]]] = set()
    deduped: List[EducationRecord] = []

    for rec in records:
        key = (
            (rec.degree or "").lower(),
            (rec.institution or "").lower(),
            rec.graduation_year,
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(rec)

    return deduped
