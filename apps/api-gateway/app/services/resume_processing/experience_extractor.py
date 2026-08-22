"""Phase 4 Day 26 — Experience Extraction Engine.

Rule-based, section-aware, deterministic work experience extractor for resume processing.
Consumes ProcessedResumeText without mutating input objects.
"""

from typing import List, Dict, Any, Optional, Set, Tuple
import re
import time
import logging

from app.exceptions.resume import ResumeParsingError
from .models import ProcessedResumeText, ExperienceRecord, ExtractedExperience
from .job_title_dictionary import (
    JOB_TITLE_PATTERNS,
    TITLE_ALIAS_MAP,
    COMPANY_ALIAS_MAP,
)
from .experience_normalizer import (
    normalize_company,
    normalize_job_title,
    detect_seniority,
    detect_employment_type,
    parse_dates_and_duration,
    deduplicate_experience_records,
)
from .degree_dictionary import INSTITUTION_KEYWORDS
from .spacy_service import get_spacy_nlp

logger = logging.getLogger("talentai.resume_processing.experience_extractor")

# False positive indicators for education and project sections
EDUCATION_GUARDS = re.compile(
    r'(?<!\w)(?:B\.?\s*Tech|M\.?\s*Tech|BTech|MTech|B\.?\s*E\.|M\.?\s*E\.|B\.?\s*Sc|M\.?\s*Sc|BCA|MCA|MBA|Ph\.?\s*D|Doctor\s+of\s+Philosophy|Diploma|Class\s+(?:X|XII|10|12)|10th|12th|Higher\s+Secondary|Senior\s+Secondary)(?!\w)',
    re.IGNORECASE,
)

OVERALL_EXP_GUARD = re.compile(
    r'\b\d+\+?\s*years?\s+(?:of\s+)?experience\b',
    re.IGNORECASE,
)

KNOWN_CORPORATE_INDICATORS = re.compile(
    r'\b(?:Inc\.?|LLC|Corp\.?|Corporation|Ltd\.?|Limited|Pvt\.?|Private|Technologies|Systems|Solutions|Software|Services|Group|Consulting|Labs)\b',
    re.IGNORECASE,
)

ACTION_VERBS = re.compile(
    r'^(?:Developed|Designed|Built|Implemented|Architected|Created|Managed|Led|Maintained|Optimized|Automated|Deployed|Tested|Analyzed|Improved|Integrated|Configured|Collaborated|Conducted|Achieved)\b',
    re.IGNORECASE,
)


def _is_education_or_project_line(line: str) -> bool:
    """Check if line is clearly from an education or project context."""
    if EDUCATION_GUARDS.search(line):
        # Allow Research Assistant roles at educational institutions
        if not re.search(r'\bResearch\s+Assistant\b', line, re.IGNORECASE):
            return True
    if re.search(r'\b(?:test\s+coverage|code\s+coverage|project\s+completed)\b', line, re.IGNORECASE):
        return True
    return False


def _is_bullet_or_responsibility_line(line: str) -> bool:
    """Check if line is a bullet point or starts with a responsibility action verb."""
    cleaned = line.strip()
    if not cleaned:
        return False
    if cleaned.startswith(("-", "•", "*", "▪", "◦", "‣")):
        return True
    clean_text = cleaned.lstrip("- •*▪◦‣\t")
    if ACTION_VERBS.search(clean_text):
        return True
    return False


def _extract_title_and_company_from_block(block_lines: List[str], sec_name: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract job title and company from a candidate block's non-bullet header lines."""
    raw_title: Optional[str] = None
    raw_company: Optional[str] = None

    header_lines = [l for l in block_lines if not _is_bullet_or_responsibility_line(l)]

    for line in header_lines:
        # Check "Title at Company" pattern e.g. "Software Engineer at Google"
        at_match = re.search(
            r'\b([A-Za-z\s]{3,35})\s+at\s+([A-Za-z0-9\s&.,]{2,40})\b',
            line,
            re.IGNORECASE,
        )
        if at_match:
            t_cand, c_cand = at_match.group(1).strip(), at_match.group(2).strip()
            for pat in JOB_TITLE_PATTERNS:
                if pat.search(t_cand):
                    return t_cand, c_cand

        # Check separator pattern e.g. "Google | Senior Software Engineer" or "Microsoft - Software Engineer"
        sep_match = re.search(
            r'^([A-Za-z0-9\s&.,]{2,35})\s*(?:\||—|–|-)\s*([A-Za-z\s]{3,35})\s*(?:\||—|–|-|\d|$)',
            line,
        )
        if sep_match:
            part1, part2 = sep_match.group(1).strip(), sep_match.group(2).strip()
            part1_is_title = any(p.search(part1) for p in JOB_TITLE_PATTERNS)
            part2_is_title = any(p.search(part2) for p in JOB_TITLE_PATTERNS)

            if part1_is_title and not part2_is_title:
                return part1, part2
            elif part2_is_title and not part1_is_title:
                return part2, part1

    # Multiline header extraction: Line 1 = Title, Line 2 = Company (or vice-versa)
    for i, line in enumerate(header_lines):
        # Skip date-only lines
        if re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d\d|Present|Current)\b', line, re.IGNORECASE):
            continue

        for pat in JOB_TITLE_PATTERNS:
            m = pat.search(line)
            if m:
                if len(line.strip()) < 50 and not _is_bullet_or_responsibility_line(line):
                    if not raw_title:
                        raw_title = line.strip()

                    # Look at next header line for company name
                    if i + 1 < len(header_lines) and not raw_company:
                        next_l = header_lines[i + 1].strip()
                        if not re.search(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|20\d\d|Present|Current)\b', next_l, re.IGNORECASE):
                            if not any(p.search(next_l) for p in JOB_TITLE_PATTERNS):
                                raw_company = next_l
                break

    # Fallback spaCy ORG entity detection for company if title found but company still missing
    if raw_title and not raw_company and sec_name == "EXPERIENCE":
        nlp = get_spacy_nlp()
        if nlp is not None:
            block_text = " ".join(header_lines)
            doc = nlp(block_text)
            for ent in doc.ents:
                if ent.label_ == "ORG":
                    ent_text = ent.text.strip()
                    if not any(kw.lower() in ent_text.lower() for kw in INSTITUTION_KEYWORDS):
                        raw_company = ent_text
                        break

    return raw_title, raw_company


def extract_experience(processed_text: Optional[ProcessedResumeText]) -> ExtractedExperience:
    """Extract, normalize, group, and deduplicate work experience entries from ProcessedResumeText.

    Args:
        processed_text: ProcessedResumeText object from Day 23.

    Returns:
        ExtractedExperience container with extracted ExperienceRecord items and metadata.

    Raises:
        ResumeParsingError: If processed_text is None or has no text.
    """
    if processed_text is None:
        raise ResumeParsingError("Cannot extract experience from a None ProcessedResumeText.")

    if not processed_text.normalized_text or not processed_text.normalized_text.strip():
        raise ResumeParsingError("The processed resume document contains no text.")

    start_time = time.perf_counter()
    records: List[ExperienceRecord] = []

    # 1. Identify Experience Sections vs Fallback Full Text Lines
    exp_sections = [s for s in processed_text.sections if s.name == "EXPERIENCE"]

    lines_to_process: List[Tuple[str, str, float]] = []  # (line_text, section_name, base_confidence)

    if exp_sections:
        for sec in exp_sections:
            sec_lines = [l.strip() for l in sec.content.splitlines() if l.strip()]
            for l in sec_lines:
                lines_to_process.append((l, sec.name, 0.95))
    else:
        # Fallback: scan all lines with lower base confidence
        all_lines = [l.strip() for l in processed_text.normalized_text.splitlines() if l.strip()]
        for l in all_lines:
            lines_to_process.append((l, "EXPERIENCE_FALLBACK", 0.80))

    # 2. Group lines into cohesive Experience Candidate Blocks
    # Split blocks on blank lines or new job title matches
    blocks: List[List[Tuple[str, str, float]]] = []
    current_block: List[Tuple[str, str, float]] = []

    for line_text, sec_name, base_conf in lines_to_process:
        # Skip pure overall experience lines e.g. "5+ years of experience in Python"
        if OVERALL_EXP_GUARD.search(line_text) and not any(p.search(line_text) for p in JOB_TITLE_PATTERNS):
            continue

        # Check if line starts a new job title (non-bullet header line)
        has_new_title = False
        if not _is_bullet_or_responsibility_line(line_text):
            for pat in JOB_TITLE_PATTERNS:
                if pat.search(line_text):
                    has_new_title = True
                    break

        if has_new_title and current_block:
            blocks.append(current_block)
            current_block = []

        current_block.append((line_text, sec_name, base_conf))

    if current_block:
        blocks.append(current_block)

    # 3. Process each Candidate Block
    for block in blocks:
        block_lines = [item[0] for item in block]
        block_text = " ".join(block_lines)
        sec_name = block[0][1]
        base_confidence = block[0][2]

        # Guard against education / project false positive blocks
        if any(_is_education_or_project_line(l) for l in block_lines):
            continue

        # Extract Job Title & Company from block header lines
        raw_title, raw_company = _extract_title_and_company_from_block(block_lines, sec_name)

        if not raw_title and not raw_company:
            # Skip block if neither title nor company matched
            continue

        # Normalize Title, Seniority & Company
        can_title, norm_title, seniority = normalize_job_title(raw_title or "")
        can_company, norm_company = normalize_company(raw_company or "")
        emp_type = detect_employment_type(block_text)

        # Parse Dates & Duration
        (
            start_date,
            end_date,
            start_yr,
            start_mo,
            end_yr,
            end_mo,
            dur_months,
            dur_text,
            is_current,
        ) = parse_dates_and_duration(block_text)

        # Extract Responsibilities (bullet points or descriptive lines)
        responsibilities: List[str] = []
        for l in block_lines:
            if _is_bullet_or_responsibility_line(l):
                clean_l = l.lstrip("- •*▪◦‣\t").strip()
                if clean_l and len(clean_l) > 10:
                    responsibilities.append(clean_l)

        # Compute heuristic confidence score
        confidence = base_confidence
        if can_title and can_company and (start_yr or end_yr) and responsibilities:
            confidence = min(0.98, base_confidence + 0.03)
        elif can_title and can_company:
            confidence = base_confidence
        elif can_title or can_company:
            confidence = max(0.70, base_confidence - 0.15)

        record = ExperienceRecord(
            company=can_company,
            normalized_company=norm_company,
            job_title=can_title,
            normalized_job_title=norm_title,
            employment_type=emp_type,
            start_date=start_date,
            end_date=end_date,
            start_year=start_yr,
            start_month=start_mo,
            end_year=end_yr,
            end_month=end_mo,
            duration_months=dur_months,
            duration_text=dur_text,
            is_current=is_current,
            responsibilities=responsibilities,
            seniority=seniority,
            source_text=block_text[:300],
            section=sec_name,
            source="pattern" if sec_name == "EXPERIENCE" else "fallback",
            confidence=round(confidence, 2),
        )
        records.append(record)

    # 4. Deduplicate Records
    deduped_records = deduplicate_experience_records(records)
    elapsed_sec = round(time.perf_counter() - start_time, 4)

    # Calculate overall experience months
    total_months = sum(r.duration_months for r in deduped_records if r.duration_months)

    logger.info(
        "Extracted %d experience records (%d deduplicated) in %.4fs",
        len(records),
        len(deduped_records),
        elapsed_sec,
    )

    return ExtractedExperience(
        experiences=deduped_records,
        total_count=len(deduped_records),
        total_experience_months=total_months if total_months > 0 else None,
        metadata={
            "duration_seconds": elapsed_sec,
            "raw_candidate_blocks": len(blocks),
            "accepted_records_count": len(deduped_records),
        },
    )
