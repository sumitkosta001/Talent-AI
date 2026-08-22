"""Experience Normalizer and Deduplicator for Day 26.

Provides deterministic functions for normalizing company names, job titles,
seniority levels, employment types, employment dates, durations, and deduplicating experience records.
"""

from typing import List, Tuple, Optional, Dict, Any, Set
import re
import logging

from .models import ExperienceRecord
from .job_title_dictionary import (
    TITLE_ALIAS_MAP,
    COMPANY_ALIAS_MAP,
    SENIORITY_LEVELS,
    EMPLOYMENT_TYPES,
)

logger = logging.getLogger("talentai.resume_processing.experience_normalizer")

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def normalize_company(raw_company: str) -> Tuple[Optional[str], Optional[str]]:
    """Clean and normalize raw company string.

    Returns:
        (cleaned_company, normalized_company)
    """
    if not raw_company or not raw_company.strip():
        return None, None

    cleaned = raw_company.strip(" ,.-|:\t\n")
    cleaned = re.sub(r'\s+', ' ', cleaned)

    if not cleaned:
        return None, None

    lowered = cleaned.lower()

    if lowered in COMPANY_ALIAS_MAP:
        canonical = COMPANY_ALIAS_MAP[lowered]
        return canonical, canonical.lower()

    return cleaned, lowered


def detect_seniority(title_str: str) -> str:
    """Classify seniority level from job title string using word boundary matching."""
    if not title_str:
        return "UNKNOWN"

    lowered = title_str.lower()

    if re.search(r'\b(?:intern|internship|trainee|assistant)\b', lowered):
        return "INTERN"
    if re.search(r'\b(?:junior|jr\.|associate)\b', lowered):
        return "JUNIOR"
    if re.search(r'\b(?:director|head\s+of|vp|vice\s+president)\b', lowered):
        return "DIRECTOR"
    if re.search(r'\b(?:executive|c-level|cto|ceo|cio|cfo)\b', lowered):
        return "EXECUTIVE"
    if re.search(r'\b(?:manager|management|engineering\s+manager)\b', lowered):
        return "MANAGER"
    if re.search(r'\b(?:principal)\b', lowered):
        return "PRINCIPAL"
    if re.search(r'\b(?:staff)\b', lowered):
        return "STAFF"
    if re.search(r'\b(?:lead|tech\s+lead|team\s+lead)\b', lowered):
        return "LEAD"
    if re.search(r'\b(?:senior|sr\.)\b', lowered):
        return "SENIOR"
    if re.search(r'\b(?:entry|fresher)\b', lowered):
        return "ENTRY_LEVEL"

    # Default for standard professional titles e.g. 'Software Engineer'
    return "MID_LEVEL"


def normalize_job_title(raw_title: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Clean job title, map canonical alias, and detect seniority.

    Returns:
        (canonical_job_title, normalized_job_title, seniority)
    """
    if not raw_title or not raw_title.strip():
        return None, None, None

    cleaned = raw_title.strip(" ,.-|:\t\n")
    cleaned = re.sub(r'\s+', ' ', cleaned)

    if not cleaned:
        return None, None, None

    lowered = cleaned.lower()

    if lowered in TITLE_ALIAS_MAP:
        canonical = TITLE_ALIAS_MAP[lowered]
        seniority = detect_seniority(canonical)
        return canonical, canonical.lower().replace(" ", "_"), seniority

    # Clean capitalization for raw title
    canonical = cleaned.title()
    seniority = detect_seniority(canonical)
    return canonical, canonical.lower().replace(" ", "_"), seniority


def detect_employment_type(text_str: str) -> str:
    """Detect employment type from job title or context string."""
    if not text_str:
        return "FULL_TIME"

    lowered = text_str.lower()

    if re.search(r'\b(?:intern|internship|trainee)\b', lowered):
        return "INTERNSHIP"
    if re.search(r'\b(?:contract|contractor)\b', lowered):
        return "CONTRACT"
    if re.search(r'\b(?:freelance|freelancer|self-employed)\b', lowered):
        return "FREELANCE"
    if re.search(r'\b(?:part\s+time|part-time)\b', lowered):
        return "PART_TIME"
    if re.search(r'\b(?:temporary|temp)\b', lowered):
        return "TEMPORARY"
    if re.search(r'\b(?:apprenticeship|apprentice)\b', lowered):
        return "APPRENTICESHIP"
    if re.search(r'\b(?:volunteer)\b', lowered):
        return "VOLUNTEER"
    if re.search(r'\b(?:research\s+assistant|researcher)\b', lowered):
        return "RESEARCH"

    return "FULL_TIME"


def parse_dates_and_duration(
    text: str,
) -> Tuple[
    Optional[str],
    Optional[str],
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[int],
    Optional[str],
    Optional[bool],
]:
    """Parse start_date, end_date, start_year, start_month, end_year, end_month, duration_months, duration_text, is_current.

    Returns:
        (start_date, end_date, start_year, start_month, end_year, end_month, duration_months, duration_text, is_current)
    """
    if not text:
        return None, None, None, None, None, None, None, None, None

    start_year: Optional[int] = None
    start_month: Optional[int] = None
    end_year: Optional[int] = None
    end_month: Optional[int] = None
    is_current: Optional[bool] = None

    # Check for Present / Current / Ongoing
    if re.search(r'\b(?:present|current|currently|now|ongoing)\b', text, re.IGNORECASE):
        is_current = True

    # Month Year range pattern e.g. Jan 2022 - Dec 2023 or Jan 2024 - Present
    month_year_pattern = re.compile(
        r'\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s*(20[0-3]\d|19[7-9]\d)'
        r'\s*(?:-|–|—|to)\s*'
        r'(?:(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s*(20[0-3]\d|19[7-9]\d)|(Present|Current|Currently|Ongoing))\b',
        re.IGNORECASE,
    )
    m_match = month_year_pattern.search(text)
    if m_match:
        sm_str, sy_str = m_match.group(1), m_match.group(2)
        start_year = int(sy_str)
        start_month = MONTH_MAP.get(sm_str.lower(), 1)

        if m_match.group(5):  # Present
            is_current = True
        elif m_match.group(3) and m_match.group(4):
            em_str, ey_str = m_match.group(3), m_match.group(4)
            end_year = int(ey_str)
            end_month = MONTH_MAP.get(em_str.lower(), 12)
            if is_current is None:
                is_current = False

    # Year-only range pattern e.g. 2022 - 2024 or 2022 - Present
    if start_year is None:
        year_pattern = re.compile(
            r'\b(20[0-3]\d|19[7-9]\d)\s*(?:-|–|—|to)\s*(?:(20[0-3]\d|19[7-9]\d)|(Present|Current|Currently|Ongoing))\b',
            re.IGNORECASE,
        )
        y_match = year_pattern.search(text)
        if y_match:
            start_year = int(y_match.group(1))
            if y_match.group(3):  # Present
                is_current = True
            elif y_match.group(2):
                end_year = int(y_match.group(2))
                if is_current is None:
                    is_current = False

    # Format dates
    start_date = f"{start_year:04d}-{start_month:02d}" if start_year and start_month else (f"{start_year:04d}" if start_year else None)
    end_date = f"{end_year:04d}-{end_month:02d}" if end_year and end_month else (f"{end_year:04d}" if end_year else None)

    # Calculate duration
    duration_months: Optional[int] = None
    duration_text: Optional[str] = None

    if start_year and end_year:
        s_m = start_month or 1
        e_m = end_month or 12
        duration_months = (end_year - start_year) * 12 + (e_m - s_m + 1)
        if duration_months > 0:
            yrs = duration_months // 12
            mos = duration_months % 12
            if yrs > 0 and mos > 0:
                duration_text = f"{yrs} yrs {mos} mos"
            elif yrs > 0:
                duration_text = f"{yrs} yrs" if yrs > 1 else "1 yr"
            else:
                duration_text = f"{mos} mos"

    return (
        start_date,
        end_date,
        start_year,
        start_month,
        end_year,
        end_month,
        duration_months,
        duration_text,
        is_current,
    )


def deduplicate_experience_records(records: List[ExperienceRecord]) -> List[ExperienceRecord]:
    """Deduplicate experience records while preserving promotions at the same company.

    Returns deduplicated records.
    """
    if not records:
        return []

    seen: Set[Tuple[str, str, Optional[int], Optional[int]]] = set()
    deduped: List[ExperienceRecord] = []

    for rec in records:
        key = (
            (rec.normalized_company or "").lower(),
            (rec.normalized_job_title or "").lower(),
            rec.start_year,
            rec.end_year,
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(rec)

    return deduped
